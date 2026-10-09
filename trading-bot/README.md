# Bot de trading (experimento con 100 €)

Swing trading diario en **Trading 212** con stop loss y take profit del **5 %**, revisado una vez al día
por una rutina de Claude Code con la skill `.claude/skills/trading-diario`.

> ⚠️ Experimento educativo, no asesoramiento financiero. Puedes perder el capital.

## Estrategia
- **Universo:** 20 acciones grandes y líquidas de EE. UU. (`config.json`). Los ETFs estadounidenses no están
  disponibles para minoristas de la UE.
- **Señal de entrada:** tendencia alcista (precio > SMA50 > SMA200), momentum de 3 meses positivo,
  RSI(14) entre 40 y 62 (retroceso dentro de la tendencia) y ATR del 1,2–4 % (para que un 5 % sea alcanzable
  en días, sin que sea puro ruido).
- **Filtro de Claude:** descarta valores con resultados próximos o noticias de riesgo.
- **Salida:** +5 % (take profit, se comprueba cada día) o −5 % (orden stop en el bróker y comprobación diaria).

## Límites duros (en el código)
| Límite | Valor |
|---|---|
| Capital | 100 €, máx. 2 posiciones (~50 € cada una) |
| Compras | máx. 1 al día, solo valores del universo, sin apalancamiento ni cortos |
| Kill switch | sin compras si el capital del bot baja de 80 € |
| Regla fiscal de 2 meses | no recompra un valor vendido con pérdidas durante 61 días |
| Real | solo con `T212_ENV=live` **y** `live_enabled: true` en `config.json` |
| Tus otras posiciones | el bot solo toca las que abrió él |

## Uso
```bash
export T212_API_KEY=...        # y T212_API_SECRET si tu clave lo usa
export T212_ENV=demo           # demo | live
python3 bot.py gestionar       # cerrar TP/SL y asegurar stops
python3 bot.py escanear        # señales
python3 bot.py comprar AAPL --motivo "..."
python3 bot.py estado
python3 bot.py informe
python3 -m unittest test_bot   # tests sin red
```

## Requisitos del entorno de Claude Code en la nube
- Dominios permitidos: `demo.trading212.com`, `live.trading212.com`, `query1.finance.yahoo.com`.
- Variables secretas: `T212_API_KEY` (+ `T212_API_SECRET`), `T212_ENV`, y `TRADING_AUTO=1` solo si quieres
  que compre sin tu aprobación.

## Limitaciones conocidas
- En cuenta real, la API de Trading 212 en algunas versiones solo admitía órdenes de mercado; si el stop
  no se puede colocar, el bot lo vigila en cada ejecución diaria (un hueco puede superar el −5 %).
- La API no es idempotente: el bot no reintenta automáticamente las órdenes.
- Si el stop del bróker se ejecuta entre revisiones, el P&L se registra como estimación (−5 %).
