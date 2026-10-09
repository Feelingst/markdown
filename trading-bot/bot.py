#!/usr/bin/env python3
"""Bot de swing trading para Trading 212 con stop loss / take profit fijos.

Subcomandos:
  estado     Saldo, posiciones del bot y resumen del diario.
  gestionar  Cierra posiciones en +TP% / -SL% y asegura un stop en el bróker.
  escanear   Calcula señales del universo y devuelve candidatos ordenados.
  comprar T  Compra el símbolo T (p.ej. AAPL) respetando todos los límites.
  informe    Resumen de resultados del diario.
  adoptar    Pone bajo gestión (SL/TP) posiciones compradas a mano.

Variables de entorno:
  T212_API_KEY     (obligatoria)  clave de API de Trading 212
  T212_API_SECRET  (opcional)     secreto, si tu clave lo usa (auth Basic)
  T212_ENV         demo | live    (por defecto demo)

Solo usa la biblioteca estándar para que funcione en cualquier sesión.
"""
from __future__ import annotations

import argparse
import base64
import csv
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.json"
JOURNAL = ROOT / "journal" / "trades.csv"
JOURNAL_FIELDS = ["fecha", "entorno", "accion", "simbolo", "ticker", "cantidad",
                  "precio", "coste_eur", "pnl_eur", "order_id", "motivo"]


class GuardrailError(Exception):
    """Una operación viola los límites de config.json."""


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------
# Trading 212 API
# --------------------------------------------------------------------------
class T212:
    def __init__(self, env: str, key: str, secret: str | None = None):
        if env not in ("demo", "live"):
            raise ValueError("T212_ENV debe ser demo o live")
        self.env = env
        self.base = f"https://{env}.trading212.com/api/v0"
        if secret:
            token = base64.b64encode(f"{key}:{secret}".encode()).decode()
            self.auth = f"Basic {token}"
        else:
            self.auth = key

    def _req(self, method: str, path: str, body: dict | None = None, retries: int = 3):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method)
        req.add_header("Authorization", self.auth)
        req.add_header("Content-Type", "application/json")
        for attempt in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    raw = r.read()
                    return json.loads(raw) if raw else None
            except urllib.error.HTTPError as e:
                if e.code == 429 and attempt < retries - 1:
                    time.sleep(int(e.headers.get("x-ratelimit-reset-in", 0) or 0) or 6)
                    continue
                detail = e.read().decode(errors="replace")[:500]
                raise RuntimeError(f"T212 {method} {path} -> HTTP {e.code}: {detail}") from None

    def cash(self) -> dict:
        return self._req("GET", "/equity/account/cash")

    def portfolio(self) -> list[dict]:
        return self._req("GET", "/equity/portfolio") or []

    def orders(self) -> list[dict]:
        return self._req("GET", "/equity/orders") or []

    def cancel(self, order_id) -> None:
        self._req("DELETE", f"/equity/orders/{order_id}")

    def market(self, ticker: str, quantity: float) -> dict:
        return self._req("POST", "/equity/orders/market",
                         {"ticker": ticker, "quantity": quantity}, retries=1)

    def stop(self, ticker: str, quantity: float, stop_price: float) -> dict:
        return self._req("POST", "/equity/orders/stop",
                         {"ticker": ticker, "quantity": quantity,
                          "stopPrice": stop_price, "timeValidity": "GOOD_TILL_CANCEL"},
                         retries=1)


def client_from_env(cfg: dict) -> T212:
    key = os.environ.get("T212_API_KEY")
    if not key:
        sys.exit("Falta T212_API_KEY en el entorno.")
    env = os.environ.get("T212_ENV", "demo")
    if env == "live" and not cfg.get("live_enabled"):
        raise GuardrailError("T212_ENV=live pero config.json tiene live_enabled=false.")
    return T212(env, key, os.environ.get("T212_API_SECRET"))


# --------------------------------------------------------------------------
# Datos de mercado (Yahoo Finance, velas diarias)
# --------------------------------------------------------------------------
def fetch_daily(symbol: str, rng: str = "1y") -> dict:
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/"
           f"{urllib.parse.quote(symbol)}?range={rng}&interval=1d")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.loads(r.read())["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    rows = [(t, h, l, c) for t, h, l, c in zip(res["timestamp"], q["high"], q["low"], q["close"])
            if None not in (h, l, c)]
    # Descarta la vela de hoy si el mercado sigue abierto (está incompleta).
    today = datetime.now(timezone.utc).date()
    if rows and datetime.fromtimestamp(rows[-1][0], timezone.utc).date() == today \
            and res["meta"].get("currentTradingPeriod", {}).get("regular", {}).get("end", 0) > time.time():
        rows = rows[:-1]
    return {"high": [r[1] for r in rows], "low": [r[2] for r in rows],
            "close": [r[3] for r in rows], "last": res["meta"].get("regularMarketPrice")}


def eurusd() -> float:
    return fetch_daily("EURUSD=X", "5d")["last"]


# --------------------------------------------------------------------------
# Indicadores
# --------------------------------------------------------------------------
def sma(xs: list[float], n: int) -> float:
    return sum(xs[-n:]) / n


def rsi(closes: list[float], n: int = 14) -> float:
    gains, losses = 0.0, 0.0
    for i in range(1, n + 1):
        d = closes[i] - closes[i - 1]
        gains += max(d, 0)
        losses += max(-d, 0)
    ag, al = gains / n, losses / n
    for i in range(n + 1, len(closes)):
        d = closes[i] - closes[i - 1]
        ag = (ag * (n - 1) + max(d, 0)) / n
        al = (al * (n - 1) + max(-d, 0)) / n
    return 100.0 if al == 0 else 100 - 100 / (1 + ag / al)


def atr_pct(high: list[float], low: list[float], close: list[float], n: int = 14) -> float:
    trs = [max(high[i] - low[i], abs(high[i] - close[i - 1]), abs(low[i] - close[i - 1]))
           for i in range(len(close) - n, len(close))]
    return 100 * (sum(trs) / n) / close[-1]


@dataclass
class Signal:
    simbolo: str
    precio: float
    sma20: float
    sma50: float
    sma200: float
    rsi14: float
    atr_pct: float
    mom_63d: float
    apto: bool
    motivos: list[str]

    @property
    def puntuacion(self) -> float:
        # Prefiere tendencia fuerte (momentum) con retroceso moderado (RSI bajo dentro del rango).
        return round(self.mom_63d - 0.3 * (self.rsi14 - 50), 2) if self.apto else -999.0


def evaluate(simbolo: str, d: dict, f: dict) -> Signal:
    c = d["close"]
    if len(c) < 200:
        return Signal(simbolo, c[-1] if c else 0, 0, 0, 0, 0, 0, 0, False, ["histórico insuficiente"])
    s20, s50, s200 = sma(c, 20), sma(c, 50), sma(c, 200)
    r, a = rsi(c), atr_pct(d["high"], d["low"], c)
    mom = 100 * (c[-1] / c[-64] - 1)
    motivos = []
    if not c[-1] > s50 > s200:
        motivos.append("sin tendencia alcista (precio>SMA50>SMA200)")
    if not f["rsi_min"] <= r <= f["rsi_max"]:
        motivos.append(f"RSI {r:.0f} fuera de [{f['rsi_min']},{f['rsi_max']}]")
    if not f["atr_pct_min"] <= a <= f["atr_pct_max"]:
        motivos.append(f"ATR {a:.1f}% fuera de [{f['atr_pct_min']},{f['atr_pct_max']}]")
    if mom <= 0:
        motivos.append("momentum 3m negativo")
    return Signal(simbolo, round(c[-1], 2), round(s20, 2), round(s50, 2), round(s200, 2),
                  round(r, 1), round(a, 2), round(mom, 2), not motivos, motivos)


# --------------------------------------------------------------------------
# Diario
# --------------------------------------------------------------------------
def read_journal() -> list[dict]:
    if not JOURNAL.exists():
        return []
    with JOURNAL.open(newline="") as fh:
        return list(csv.DictReader(fh))


def append_journal(**row) -> None:
    JOURNAL.parent.mkdir(parents=True, exist_ok=True)
    new = not JOURNAL.exists()
    with JOURNAL.open("a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=JOURNAL_FIELDS)
        if new:
            w.writeheader()
        w.writerow({"fecha": now_iso(), **{k: row.get(k, "") for k in JOURNAL_FIELDS[1:]}})


def journal_state(rows: list[dict], env: str) -> dict:
    """Posiciones abiertas por el bot, P&L realizado y bloqueos por la regla de los 2 meses."""
    open_pos: dict[str, dict] = {}
    realized, wins, losses = 0.0, 0, 0
    loss_dates: dict[str, date] = {}
    buys_by_day: dict[str, int] = {}
    for r in rows:
        if r["entorno"] != env:
            continue
        if r["accion"] == "COMPRA":
            open_pos[r["ticker"]] = r
            day = r["fecha"][:10]
            buys_by_day[day] = buys_by_day.get(day, 0) + 1
        elif r["accion"].startswith("VENTA"):
            open_pos.pop(r["ticker"], None)
            pnl = float(r["pnl_eur"] or 0)
            realized += pnl
            if pnl < 0:
                losses += 1
                loss_dates[r["ticker"]] = datetime.fromisoformat(r["fecha"][:10]).date()
            else:
                wins += 1
    return {"abiertas": open_pos, "realizado_eur": round(realized, 2), "ganadoras": wins,
            "perdedoras": losses, "fechas_perdida": loss_dates, "compras_por_dia": buys_by_day}


# --------------------------------------------------------------------------
# Lógica de negocio
# --------------------------------------------------------------------------
def floor_qty(q: float, decimals: int) -> float:
    f = 10 ** decimals
    return math.floor(q * f) / f


def check_buy_allowed(cfg: dict, st: dict, ticker: str, cash_free: float,
                      bot_equity: float, today: date) -> float:
    """Devuelve el presupuesto en EUR para la compra o lanza GuardrailError."""
    if ticker not in cfg["universo"].values():
        raise GuardrailError(f"{ticker} no está en el universo permitido.")
    if ticker in st["abiertas"]:
        raise GuardrailError(f"Ya hay una posición abierta en {ticker}.")
    if len(st["abiertas"]) >= cfg["max_posiciones"]:
        raise GuardrailError(f"Máximo de {cfg['max_posiciones']} posiciones alcanzado.")
    if st["compras_por_dia"].get(today.isoformat(), 0) >= cfg["max_compras_por_dia"]:
        raise GuardrailError("Límite de compras diarias alcanzado.")
    if bot_equity < cfg["kill_switch_eur"]:
        raise GuardrailError(f"Kill switch: capital del bot {bot_equity:.2f} € < {cfg['kill_switch_eur']} €.")
    last_loss = st["fechas_perdida"].get(ticker)
    if last_loss and (today - last_loss).days < cfg["dias_bloqueo_tras_perdida"]:
        raise GuardrailError(f"{ticker} vendida con pérdida el {last_loss}: bloqueada por la regla de los 2 meses.")
    slots = cfg["max_posiciones"] - len(st["abiertas"])
    invested = sum(float(p["coste_eur"] or 0) for p in st["abiertas"].values())
    budget = min((bot_equity - invested) / slots, cash_free)
    if budget < 5:
        raise GuardrailError(f"Presupuesto insuficiente ({budget:.2f} €).")
    return round(budget, 2)


def bot_positions(api: T212, cfg: dict, st: dict) -> list[dict]:
    return [p for p in api.portfolio() if p["ticker"] in st["abiertas"]]


def cmd_adoptar(api: T212, cfg: dict, tickers: list[str]) -> list[str]:
    """Registra en el diario posiciones abiertas a mano para que el bot las gestione (SL/TP).

    Sin argumentos lista lo que hay en cartera y no adopta nada."""
    st = journal_state(read_journal(), api.env)
    portfolio = {p["ticker"]: p for p in api.portfolio()}
    if not tickers:
        return [f"{t}: {p['quantity']} @ {p['averagePrice']} (actual {p['currentPrice']})"
                + (" [ya gestionada]" if t in st["abiertas"] else "")
                for t, p in portfolio.items()] or ["Cartera vacía."]
    fx = None
    log = []
    for t in tickers:
        t = cfg["universo"].get(t.upper(), t)
        p = portfolio.get(t)
        if p is None:
            log.append(f"{t}: no está en la cartera")
            continue
        if t in st["abiertas"]:
            log.append(f"{t}: ya gestionada")
            continue
        if t.endswith("_US_EQ"):
            fx = fx or eurusd()
            coste = p["quantity"] * p["averagePrice"] / fx
        else:
            coste = p["quantity"] * p["averagePrice"]
        sym = {v: k for k, v in cfg["universo"].items()}.get(t, t.split("_")[0])
        append_journal(entorno=api.env, accion="COMPRA", simbolo=sym, ticker=t, cantidad=p["quantity"],
                       precio=p["averagePrice"], coste_eur=round(coste, 2),
                       motivo="Adoptada: compra manual del usuario")
        log.append(f"{t}: adoptada ({p['quantity']} @ {p['averagePrice']}, ~{coste:.2f} €)")
    return log


def cmd_estado(api: T212, cfg: dict) -> dict:
    st = journal_state(read_journal(), api.env)
    pos = bot_positions(api, cfg, st)
    unreal = sum(p.get("ppl", 0) for p in pos)
    return {"entorno": api.env, "cash": api.cash(),
            "capital_bot_eur": round(cfg["capital_inicial_eur"] + st["realizado_eur"] + unreal, 2),
            "realizado_eur": st["realizado_eur"], "no_realizado_eur": round(unreal, 2),
            "posiciones": [{"ticker": p["ticker"], "cantidad": p["quantity"],
                            "precio_medio": p["averagePrice"], "precio_actual": p["currentPrice"],
                            "pnl_pct": round(100 * (p["currentPrice"] / p["averagePrice"] - 1), 2),
                            "pnl_eur": p.get("ppl")} for p in pos],
            "ganadoras": st["ganadoras"], "perdedoras": st["perdedoras"]}


def cmd_gestionar(api: T212, cfg: dict) -> list[str]:
    log = []
    st = journal_state(read_journal(), api.env)
    portfolio = {p["ticker"]: p for p in api.portfolio()}
    pending = api.orders()
    sym_of = {v: k for k, v in cfg["universo"].items()}
    tp, sl = cfg["take_profit_pct"], cfg["stop_loss_pct"]

    for ticker, entry in st["abiertas"].items():
        p = portfolio.get(ticker)
        if p is None:
            # Ya no está en cartera: lo cerró el stop del bróker entre ejecuciones.
            pnl = -float(entry["coste_eur"] or 0) * sl / 100
            append_journal(entorno=api.env, accion="VENTA_STOP_BROKER", simbolo=sym_of.get(ticker, ""),
                           ticker=ticker, cantidad=entry["cantidad"], pnl_eur=round(pnl, 2),
                           motivo="Posición desaparecida: stop ejecutado en el bróker (P&L estimado)")
            log.append(f"{ticker}: cerrada por el stop del bróker (P&L estimado {pnl:.2f} €)")
            continue
        chg = 100 * (p["currentPrice"] / p["averagePrice"] - 1)
        mine = [o for o in pending if o["ticker"] == ticker]
        if chg >= tp or chg <= -sl:
            for o in mine:
                api.cancel(o["id"])
            time.sleep(2)
            res = api.market(ticker, -p["quantity"])
            accion = "VENTA_TP" if chg >= tp else "VENTA_SL"
            append_journal(entorno=api.env, accion=accion, simbolo=sym_of.get(ticker, ""), ticker=ticker,
                           cantidad=p["quantity"], precio=p["currentPrice"], pnl_eur=round(p.get("ppl", 0), 2),
                           order_id=res.get("id", ""), motivo=f"Variación {chg:+.2f}%")
            log.append(f"{ticker}: {accion} a {p['currentPrice']} ({chg:+.2f}%, {p.get('ppl', 0):+.2f} €)")
        elif not any(o.get("type") == "STOP" for o in mine):
            stop_price = round(p["averagePrice"] * (1 - sl / 100), 2)
            try:
                res = api.stop(ticker, -p["quantity"], stop_price)
                append_journal(entorno=api.env, accion="STOP_COLOCADO", simbolo=sym_of.get(ticker, ""),
                               ticker=ticker, cantidad=p["quantity"], precio=stop_price,
                               order_id=res.get("id", ""), motivo="Stop de protección en el bróker")
                log.append(f"{ticker}: stop colocado en {stop_price}")
            except RuntimeError as e:
                log.append(f"{ticker}: AVISO, no se pudo colocar el stop ({e}); se vigila en cada ejecución")
        else:
            log.append(f"{ticker}: mantener ({chg:+.2f}%)")
    return log or ["Sin posiciones abiertas del bot."]


def cmd_escanear(cfg: dict) -> list[dict]:
    out = []
    for sym in cfg["universo"]:
        try:
            s = evaluate(sym, fetch_daily(sym), cfg["filtros"])
            out.append({**s.__dict__, "puntuacion": s.puntuacion})
        except Exception as e:  # un símbolo con datos raros no debe tumbar el escaneo
            out.append({"simbolo": sym, "apto": False, "motivos": [f"error de datos: {e}"], "puntuacion": -999})
        time.sleep(0.3)
    return sorted(out, key=lambda x: x["puntuacion"], reverse=True)


def cmd_comprar(api: T212, cfg: dict, simbolo: str, motivo: str) -> str:
    simbolo = simbolo.upper()
    ticker = cfg["universo"].get(simbolo)
    if not ticker:
        raise GuardrailError(f"{simbolo} no está en el universo permitido.")
    st = journal_state(read_journal(), api.env)
    pos = bot_positions(api, cfg, st)
    equity = cfg["capital_inicial_eur"] + st["realizado_eur"] + sum(p.get("ppl", 0) for p in pos)
    cash_free = float(api.cash().get("free", 0))
    budget = check_buy_allowed(cfg, st, ticker, cash_free, equity, datetime.now(timezone.utc).date())

    d = fetch_daily(simbolo, "5d")
    price_usd = d["last"]
    qty_raw = budget * (1 - cfg["margen_fx_pct"] / 100) * eurusd() / price_usd
    res, qty, err = None, 0.0, None
    for dec in (4, 3, 2, 1, 0):  # la precisión fraccionaria varía según el instrumento
        qty = floor_qty(qty_raw, dec)
        if qty <= 0:
            break
        try:
            res = api.market(ticker, qty)
            break
        except RuntimeError as e:
            err = e
            if "quantity" not in str(e).lower() and "precision" not in str(e).lower():
                raise
            time.sleep(2)
    if res is None:
        raise RuntimeError(f"No se pudo comprar {ticker}: {err}")

    append_journal(entorno=api.env, accion="COMPRA", simbolo=simbolo, ticker=ticker, cantidad=qty,
                   precio=price_usd, coste_eur=budget, order_id=res.get("id", ""), motivo=motivo)
    msg = f"COMPRA {qty} {ticker} (~{budget} €, precio ref. {price_usd})"

    time.sleep(8)  # esperar a que la orden se ejecute antes de poner el stop
    p = next((p for p in api.portfolio() if p["ticker"] == ticker), None)
    if p:
        stop_price = round(p["averagePrice"] * (1 - cfg["stop_loss_pct"] / 100), 2)
        try:
            s = api.stop(ticker, -p["quantity"], stop_price)
            append_journal(entorno=api.env, accion="STOP_COLOCADO", simbolo=simbolo, ticker=ticker,
                           cantidad=p["quantity"], precio=stop_price, order_id=s.get("id", ""),
                           motivo="Stop de protección en el bróker")
            msg += f"; stop en {stop_price}"
        except RuntimeError as e:
            msg += f"; AVISO stop no colocado ({e})"
    else:
        msg += "; orden aún sin ejecutar, el stop se pondrá en la próxima gestión"
    return msg


def cmd_informe(cfg: dict, env: str) -> dict:
    rows = [r for r in read_journal() if r["entorno"] == env]
    st = journal_state(rows, env)
    closed = st["ganadoras"] + st["perdedoras"]
    return {"entorno": env, "operaciones_cerradas": closed,
            "tasa_acierto_pct": round(100 * st["ganadoras"] / closed, 1) if closed else None,
            "pnl_realizado_eur": st["realizado_eur"],
            "rentabilidad_realizada_pct": round(100 * st["realizado_eur"] / cfg["capital_inicial_eur"], 2),
            "abiertas": list(st["abiertas"])}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("estado")
    sub.add_parser("gestionar")
    sub.add_parser("escanear")
    b = sub.add_parser("comprar")
    b.add_argument("simbolo")
    b.add_argument("--motivo", required=True, help="Justificación breve que queda en el diario")
    sub.add_parser("informe")
    a = sub.add_parser("adoptar", help="Gestionar posiciones abiertas a mano (sin args: listar)")
    a.add_argument("tickers", nargs="*")
    args = ap.parse_args()
    cfg = load_config()

    try:
        if args.cmd == "escanear":
            result = cmd_escanear(cfg)
        elif args.cmd == "informe":
            result = cmd_informe(cfg, os.environ.get("T212_ENV", "demo"))
        else:
            api = client_from_env(cfg)
            if args.cmd == "estado":
                result = cmd_estado(api, cfg)
            elif args.cmd == "adoptar":
                result = cmd_adoptar(api, cfg, args.tickers)
            elif args.cmd == "gestionar":
                result = cmd_gestionar(api, cfg)
            else:
                result = cmd_comprar(api, cfg, args.simbolo, args.motivo)
    except GuardrailError as e:
        print(json.dumps({"bloqueado": str(e)}, ensure_ascii=False))
        sys.exit(2)
    print(json.dumps(result, ensure_ascii=False, indent=2, default=str))


if __name__ == "__main__":
    main()
