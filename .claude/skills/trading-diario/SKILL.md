---
name: trading-diario
description: Ejecuta la revisión diaria del bot de trading (Trading 212, 100 €, SL/TP 5 %). Usar cuando una rutina programada o el usuario pida "revisión de trading", "analiza el mercado" o "ejecuta el bot".
---

# Revisión diaria de trading

Todo pasa por `trading-bot/bot.py`. **Nunca** llames a la API de Trading 212 por otra vía ni edites
`trading-bot/config.json` (límites, universo, `live_enabled`) salvo que el usuario lo pida explícitamente
en esta conversación. Si un comando devuelve `{"bloqueado": ...}`, respétalo: no busques atajos.

Ejecuta desde `trading-bot/`.

## Pasos

1. **Comprobaciones previas**
   - `python3 -m unittest test_bot` debe pasar.
   - Debe existir `T212_API_KEY`. Si falta, o la red bloquea `*.trading212.com` / `query1.finance.yahoo.com`,
     detente y explica al usuario qué falta. No inventes datos.
   - Entorno: `T212_ENV` (por defecto `demo`).

2. **Gestionar posiciones**: `python3 bot.py gestionar`
   (vende con +5 % / −5 % y asegura el stop en el bróker).

3. **Estado**: `python3 bot.py estado`. Si no hay hueco (máx. posiciones) salta al paso 6.

4. **Escanear**: `python3 bot.py escanear`. Toma como mucho los 3 primeros con `apto: true`.

5. **Decidir** (tú eres el filtro final, sé conservador):
   - Para cada candidato, busca en la web noticias de los últimos días. **Descarta** si hay resultados
     trimestrales en los próximos 5 días hábiles, una noticia que pueda provocar un hueco (demanda, regulación,
     fusión) o un día de alta volatilidad macro (FOMC, IPC de EE. UU.) hoy o mañana.
   - Si ninguno pasa, no compres. No operar es una decisión válida.
   - Si uno pasa: `python3 bot.py comprar SIMBOLO --motivo "<señal + por qué las noticias no lo impiden>"`.
   - Modo semiautomático (por defecto): si la variable `TRADING_AUTO` no es `1`, **no compres**; deja la
     propuesta en el informe y notifica al usuario para que la apruebe.

6. **Informe**: `python3 bot.py informe` y escribe `trading-bot/journal/AAAA-MM-DD.md` con:
   estado de la cartera, acciones tomadas, candidatos analizados y por qué se aceptaron o descartaron,
   y P&L acumulado. Breve y en español.

7. **Guardar**: commit de `trading-bot/journal/` y push a la rama `trading-bot`.

## Recordatorios para el informe
- No es asesoramiento financiero; es un experimento.
- Con SL y TP simétricos el resultado esperado ronda 0 menos costes; evalúa tras ≥ 20 operaciones, no antes.
