"""Tests sin red: indicadores, límites y gestión de posiciones con una API falsa."""
import unittest
from datetime import date
from unittest import mock

import bot

CFG = bot.load_config()


class FakeAPI:
    env = "demo"

    def __init__(self, portfolio=None, orders=None, free=100.0):
        self._portfolio = portfolio or []
        self._orders = orders or []
        self.free = free
        self.calls = []

    def portfolio(self):
        return self._portfolio

    def orders(self):
        return self._orders

    def cash(self):
        return {"free": self.free}

    def cancel(self, oid):
        self.calls.append(("cancel", oid))

    def market(self, ticker, qty):
        self.calls.append(("market", ticker, qty))
        return {"id": 1}

    def stop(self, ticker, qty, price):
        self.calls.append(("stop", ticker, qty, price))
        return {"id": 2}


def state(**kw):
    base = {"abiertas": {}, "realizado_eur": 0.0, "ganadoras": 0, "perdedoras": 0,
            "fechas_perdida": {}, "compras_por_dia": {}}
    return {**base, **kw}


class Indicators(unittest.TestCase):
    def test_rsi_extremes(self):
        self.assertEqual(bot.rsi([float(i) for i in range(1, 40)]), 100.0)
        self.assertLess(bot.rsi([float(i) for i in range(40, 1, -1)]), 1)

    def test_uptrend_with_pullback_is_eligible(self):
        # Tendencia alcista con dientes de sierra y un retroceso leve al final.
        closes = [100 + i * 0.3 + (2 if i % 4 < 2 else -2) for i in range(250)]
        closes[-3:] = [closes[-4] - 1.5, closes[-4] - 2.5, closes[-4] - 2.0]
        d = {"close": closes, "high": [c * 1.01 for c in closes], "low": [c * 0.99 for c in closes]}
        s = bot.evaluate("TEST", d, CFG["filtros"])
        self.assertTrue(s.apto, s.motivos)

    def test_downtrend_rejected(self):
        closes = [300 - i * 0.5 for i in range(250)]
        d = {"close": closes, "high": [c * 1.01 for c in closes], "low": [c * 0.99 for c in closes]}
        self.assertFalse(bot.evaluate("TEST", d, CFG["filtros"]).apto)


class Guardrails(unittest.TestCase):
    today = date(2026, 10, 9)

    def test_budget_split_across_slots(self):
        self.assertEqual(bot.check_buy_allowed(CFG, state(), "AAPL_US_EQ", 100, 100, self.today), 50)

    def test_rejects_ticker_outside_universe(self):
        with self.assertRaises(bot.GuardrailError):
            bot.check_buy_allowed(CFG, state(), "GME_US_EQ", 100, 100, self.today)

    def test_rejects_when_max_positions(self):
        st = state(abiertas={"A": {"coste_eur": 50}, "B": {"coste_eur": 50}})
        with self.assertRaises(bot.GuardrailError):
            bot.check_buy_allowed(CFG, st, "AAPL_US_EQ", 100, 100, self.today)

    def test_kill_switch(self):
        with self.assertRaises(bot.GuardrailError):
            bot.check_buy_allowed(CFG, state(), "AAPL_US_EQ", 100, 79, self.today)

    def test_two_month_rule(self):
        st = state(fechas_perdida={"AAPL_US_EQ": date(2026, 9, 1)})
        with self.assertRaises(bot.GuardrailError):
            bot.check_buy_allowed(CFG, st, "AAPL_US_EQ", 100, 100, self.today)

    def test_daily_buy_limit(self):
        st = state(compras_por_dia={"2026-10-09": 1})
        with self.assertRaises(bot.GuardrailError):
            bot.check_buy_allowed(CFG, st, "AAPL_US_EQ", 100, 100, self.today)

    def test_budget_capped_by_free_cash(self):
        self.assertEqual(bot.check_buy_allowed(CFG, state(), "AAPL_US_EQ", 20, 100, self.today), 20)

    def test_live_requires_flag(self):
        with mock.patch.dict("os.environ", {"T212_API_KEY": "x", "T212_ENV": "live"}):
            with self.assertRaises(bot.GuardrailError):
                bot.client_from_env({**CFG, "live_enabled": False})


class Manage(unittest.TestCase):
    def run_manage(self, api, journal_rows):
        with mock.patch.object(bot, "read_journal", return_value=journal_rows), \
             mock.patch.object(bot, "append_journal") as app, \
             mock.patch.object(bot.time, "sleep"):
            log = bot.cmd_gestionar(api, CFG)
        return log, app

    buy = [{"fecha": "2026-10-01T15:00:00Z", "entorno": "demo", "accion": "COMPRA", "simbolo": "AAPL",
            "ticker": "AAPL_US_EQ", "cantidad": "0.2", "precio": "200", "coste_eur": "50",
            "pnl_eur": "", "order_id": "1", "motivo": ""}]

    def pos(self, cur):
        return [{"ticker": "AAPL_US_EQ", "quantity": 0.2, "averagePrice": 200.0, "currentPrice": cur, "ppl": 1.0}]

    def test_take_profit_sells_and_cancels_stop(self):
        api = FakeAPI(self.pos(210.5), [{"id": 9, "ticker": "AAPL_US_EQ", "type": "STOP"}])
        _, app = self.run_manage(api, self.buy)
        self.assertIn(("cancel", 9), api.calls)
        self.assertIn(("market", "AAPL_US_EQ", -0.2), api.calls)
        self.assertEqual(app.call_args.kwargs["accion"], "VENTA_TP")

    def test_stop_loss_sells(self):
        api = FakeAPI(self.pos(189.0))
        _, app = self.run_manage(api, self.buy)
        self.assertEqual(app.call_args.kwargs["accion"], "VENTA_SL")

    def test_places_missing_stop(self):
        api = FakeAPI(self.pos(201.0))
        self.run_manage(api, self.buy)
        self.assertIn(("stop", "AAPL_US_EQ", -0.2, 190.0), api.calls)

    def test_ignores_user_positions_not_opened_by_bot(self):
        api = FakeAPI([{"ticker": "MSFT_US_EQ", "quantity": 1, "averagePrice": 100, "currentPrice": 150}])
        log, _ = self.run_manage(api, [])
        self.assertEqual(api.calls, [])
        self.assertEqual(log, ["Sin posiciones abiertas del bot."])

    def test_detects_broker_stop_fill(self):
        api = FakeAPI([])
        _, app = self.run_manage(api, self.buy)
        self.assertEqual(app.call_args.kwargs["accion"], "VENTA_STOP_BROKER")
        self.assertEqual(app.call_args.kwargs["pnl_eur"], -2.5)


if __name__ == "__main__":
    unittest.main()
