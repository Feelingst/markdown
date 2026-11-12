#!/usr/bin/env bash
# Abre Jarvis como aplicación en macOS o Linux: sirve esta carpeta en
# http://127.0.0.1:8765 y abre Chrome o Edge en modo aplicación con un perfil
# propio (recuerda el permiso del micrófono y las claves). Al cerrar la
# ventana se cierra el servidor.
set -u
cd "$(dirname "$0")"
PORT=8765
URL="http://127.0.0.1:$PORT/"
PROFILE="$HOME/.jarvis-tomas/perfil"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Jarvis necesita python3 para el servidor local." >&2
  exit 1
fi

BROWSER=""
for b in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
         "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
         google-chrome google-chrome-stable chromium chromium-browser microsoft-edge; do
  if [ -x "$b" ] || command -v "$b" >/dev/null 2>&1; then BROWSER="$b"; break; fi
done
if [ -z "$BROWSER" ]; then
  echo "No encuentro Google Chrome ni Microsoft Edge. Instala uno de los dos." >&2
  exit 1
fi

python3 -m http.server "$PORT" --bind 127.0.0.1 >/dev/null 2>&1 &
SERVER=$!
trap 'kill "$SERVER" 2>/dev/null' EXIT
sleep 0.5

"$BROWSER" --app="$URL" --user-data-dir="$PROFILE" --window-size=1200,820 \
  --no-first-run --no-default-browser-check
