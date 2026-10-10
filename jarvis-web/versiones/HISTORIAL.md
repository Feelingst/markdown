# Historial de versiones de Jarvis

La versión más reciente va arriba. Cada versión tiene una etiqueta en git (`jarvis-vX.Y.Z`); el enlace **Descargar** baja un ZIP del repositorio tal como estaba en esa versión. Jarvis está en la carpeta `jarvis-web/` del ZIP; la v0.1.0 es solo `jarvis.py`.

Formato del número: **X.Y.Z**. Sube **Y** cuando hay una función nueva y **Z** cuando es un arreglo. **X** pasará a 1 cuando Jarvis se dé por terminada.

---

## v0.7.0 · 2026-10-10 · Aplicación de escritorio
[Descargar](https://github.com/Feelingst/markdown/archive/refs/tags/jarvis-v0.7.0.zip)

- Lanzadores con doble clic: `Jarvis.bat` (Windows), `Jarvis.command` (macOS) y `jarvis.sh` (Linux).
- Abre Jarvis en su propia ventana (Chrome o Edge en modo aplicación) con un servidor local en `localhost:8765`. Usa un perfil propio, así que recuerda el permiso del micrófono y las claves. El servidor se cierra al cerrar la ventana.
- `crear-acceso-directo.bat` pone un acceso directo con icono en el escritorio de Windows.
- Nuevo icono `jarvis.ico`, también como icono de la pestaña.
- Carpeta `versiones/` con este historial. El número de versión aparece en la aplicación.
- **Probado:** el servidor de Windows con PowerShell 7 en Linux y el lanzador de macOS/Linux. **Sin probar:** en Windows real.

## v0.6.0 · 2026-10-10 · Tema oscuro
[Descargar](https://github.com/Feelingst/markdown/archive/refs/tags/jarvis-v0.6.0.zip)

- Fondo casi negro y paneles gris oscuro neutro, texto en blanco puro.
- Campos de texto de los ajustes con el mismo estilo oscuro.
- El panel de ajustes tiene su propio scroll para que el chat siga visible.
- El botón "Activar micrófono" ya no parece desactivado.

## v0.5.0 · 2026-10-10 · Vídeo realista con Simli
[Descargar](https://github.com/Feelingst/markdown/archive/refs/tags/jarvis-v0.5.0.zip)

- Opcional: con una clave de Simli y un Face ID, el círculo del avatar muestra un vídeo de la cara de tu foto con lip sync real.
- El audio de ElevenLabs se pide en PCM de 16 kHz, que sirve tanto para Simli como para reproducirlo en la página.
- Botón para conectar y desconectar el vídeo, porque Simli cobra por minuto.
- **Probado:** con Simli simulado. **Sin probar:** con el servicio real.

## v0.4.0 · 2026-10-10 · Voz de ElevenLabs
[Descargar](https://github.com/Feelingst/markdown/archive/refs/tags/jarvis-v0.4.0.zip)

- Opcional: habla con tu voz de ElevenLabs (modelo `eleven_flash_v2_5`).
- Lip sync con el momento exacto de cada letra y el volumen real del audio.
- La frase siguiente se pide mientras suena la anterior.
- Si ElevenLabs falla, usa la voz del navegador y lo avisa.

## v0.3.0 · 2026-10-10 · Avatar que reacciona
[Descargar](https://github.com/Feelingst/markdown/archive/refs/tags/jarvis-v0.3.0.zip)

- Labios sincronizados palabra a palabra con la voz, según sus vocales.
- Emociones: Claude marca cada respuesta (alegre, divertida, pensativa, sorprendida, preocupada o neutral) y el avatar cambia de expresión y el aro de color.
- Parpadeo, asentir al terminar una frase, cejas arriba al preguntar, mirar hacia arriba al pensar.
- Con foto propia: la mandíbula se mueve, con un botón para ajustar dónde está la boca.

## v0.2.0 · 2026-10-10 · Aplicación local con micrófono
[Descargar](https://github.com/Feelingst/markdown/archive/refs/tags/jarvis-v0.2.0.zip)

- Página `jarvis-web/index.html` que se abre en Chrome o Edge.
- Micrófono siempre abierto: envía al dejar de hablar y se pausa mientras Jarvis habla.
- Claude (`claude-sonnet-5`) con respuestas en streaming, leídas en voz alta frase a frase.
- Avatar ilustrado de una mujer de unos 40 años, con opción de poner tu propia foto.

## v0.1.0 · 2026-09-28 · Script de prueba
[Descargar](https://github.com/Feelingst/markdown/archive/refs/tags/jarvis-v0.1.0.zip)

- `jarvis.py`: Jarvis se presenta en una frase usando el SDK de Python de Anthropic.

---

Antes de la v0.2.0 hubo una página publicada en claude.ai ("Jarvis de Tomás") que habla por escrito y lee las respuestas con la voz del navegador. No forma parte del repositorio.
