# Historial de versiones de Jarvis

La versión más reciente va arriba. El enlace **Descargar** de cada versión baja un ZIP del repositorio tal como estaba en ese commit. Jarvis está en la carpeta `jarvis-web/` del ZIP; la v0.1.0 es solo `jarvis.py`.

Formato del número: **X.Y.Z**. Sube **Y** cuando hay una función nueva y **Z** cuando es un arreglo. **X** pasará a 1 cuando Jarvis se dé por terminada.

---

## v0.7.1 · 2026-10-10 · Arreglos del micrófono
[Descargar](https://github.com/Feelingst/markdown/archive/d4831a45f68f3cffcf496b53dd309eedcadbc121.zip) · [ver código](https://github.com/Feelingst/markdown/tree/d4831a45f68f3cffcf496b53dd309eedcadbc121) · commit `d4831a4`

- Envía lo que dices tras un silencio aunque el navegador no marque la frase como "final". Safari en iPhone casi nunca la marca, así que antes no enviaba nada.
- Si el navegador no llega a su servicio de reconocimiento de voz (VPN o red de empresa), deja de reintentar y explica qué hacer (probar con Microsoft Edge o quitar la VPN).
- Avisos claros cuando no hay micrófono, cuando está bloqueado o cuando el idioma no está disponible. Muestra "Te escucho" cuando el micrófono está abierto.
- En iPhone, la voz del navegador se activa al pulsar el micrófono, para que pueda hablar luego.
- **Probado:** con un reconocimiento de voz simulado (estilo Safari, estilo Chrome y error de red).

## v0.7.0 · 2026-10-10 · Aplicación de escritorio
[Descargar](https://github.com/Feelingst/markdown/archive/8c989ba45b6287cd22e96646d2fb597ff003ae6a.zip) · [ver código](https://github.com/Feelingst/markdown/tree/8c989ba45b6287cd22e96646d2fb597ff003ae6a) · commit `8c989ba`

- Lanzadores con doble clic: `Jarvis.bat` (Windows), `Jarvis.command` (macOS) y `jarvis.sh` (Linux).
- Abre Jarvis en su propia ventana (Chrome o Edge en modo aplicación) con un servidor local en `localhost:8765`. Usa un perfil propio, así que recuerda el permiso del micrófono y las claves. El servidor se cierra al cerrar la ventana.
- `crear-acceso-directo.bat` pone un acceso directo con icono en el escritorio de Windows.
- Nuevo icono `jarvis.ico`, también como icono de la pestaña.
- Carpeta `versiones/` con este historial. El número de versión aparece en la aplicación.
- **Probado:** el servidor de Windows con PowerShell 7 en Linux y el lanzador de macOS/Linux. **Sin probar:** en Windows real.

## v0.6.0 · 2026-10-10 · Tema oscuro
[Descargar](https://github.com/Feelingst/markdown/archive/b4dcb9ea000a07a765d106c565f700affec4275f.zip) · [ver código](https://github.com/Feelingst/markdown/tree/b4dcb9ea000a07a765d106c565f700affec4275f) · commit `b4dcb9e`

- Fondo casi negro y paneles gris oscuro neutro, texto en blanco puro.
- Campos de texto de los ajustes con el mismo estilo oscuro.
- El panel de ajustes tiene su propio scroll para que el chat siga visible.
- El botón "Activar micrófono" ya no parece desactivado.

## v0.5.0 · 2026-10-10 · Vídeo realista con Simli
[Descargar](https://github.com/Feelingst/markdown/archive/8f8d16b1255a04537c27f37c1d3aa1486a48658a.zip) · [ver código](https://github.com/Feelingst/markdown/tree/8f8d16b1255a04537c27f37c1d3aa1486a48658a) · commit `8f8d16b`

- Opcional: con una clave de Simli y un Face ID, el círculo del avatar muestra un vídeo de la cara de tu foto con lip sync real.
- El audio de ElevenLabs se pide en PCM de 16 kHz, que sirve tanto para Simli como para reproducirlo en la página.
- Botón para conectar y desconectar el vídeo, porque Simli cobra por minuto.
- **Probado:** con Simli simulado. **Sin probar:** con el servicio real.

## v0.4.0 · 2026-10-10 · Voz de ElevenLabs
[Descargar](https://github.com/Feelingst/markdown/archive/d2a741eac3a4088c487b18a4e6e30c95ba863ba0.zip) · [ver código](https://github.com/Feelingst/markdown/tree/d2a741eac3a4088c487b18a4e6e30c95ba863ba0) · commit `d2a741e`

- Opcional: habla con tu voz de ElevenLabs (modelo `eleven_flash_v2_5`).
- Lip sync con el momento exacto de cada letra y el volumen real del audio.
- La frase siguiente se pide mientras suena la anterior.
- Si ElevenLabs falla, usa la voz del navegador y lo avisa.

## v0.3.0 · 2026-10-10 · Avatar que reacciona
[Descargar](https://github.com/Feelingst/markdown/archive/ea7cc3f4ad517d0b6ff6f1971e61174399863122.zip) · [ver código](https://github.com/Feelingst/markdown/tree/ea7cc3f4ad517d0b6ff6f1971e61174399863122) · commit `ea7cc3f`

- Labios sincronizados palabra a palabra con la voz, según sus vocales.
- Emociones: Claude marca cada respuesta (alegre, divertida, pensativa, sorprendida, preocupada o neutral) y el avatar cambia de expresión y el aro de color.
- Parpadeo, asentir al terminar una frase, cejas arriba al preguntar, mirar hacia arriba al pensar.
- Con foto propia: la mandíbula se mueve, con un botón para ajustar dónde está la boca.

## v0.2.0 · 2026-10-10 · Aplicación local con micrófono
[Descargar](https://github.com/Feelingst/markdown/archive/73ddb3bce481366b690b69ea1fee27472cccb146.zip) · [ver código](https://github.com/Feelingst/markdown/tree/73ddb3bce481366b690b69ea1fee27472cccb146) · commit `73ddb3b`

- Página `jarvis-web/index.html` que se abre en Chrome o Edge.
- Micrófono siempre abierto: envía al dejar de hablar y se pausa mientras Jarvis habla.
- Claude (`claude-sonnet-5`) con respuestas en streaming, leídas en voz alta frase a frase.
- Avatar ilustrado de una mujer de unos 40 años, con opción de poner tu propia foto.

## v0.1.0 · 2026-09-28 · Script de prueba
[Descargar](https://github.com/Feelingst/markdown/archive/7f0b8ecadaa984890e39113520863556c448bb22.zip) · [ver código](https://github.com/Feelingst/markdown/tree/7f0b8ecadaa984890e39113520863556c448bb22) · commit `7f0b8ec`

- `jarvis.py`: Jarvis se presenta en una frase usando el SDK de Python de Anthropic.

---

Antes de la v0.2.0 hubo una página publicada en claude.ai ("Jarvis de Tomás") que habla por escrito y lee las respuestas con la voz del navegador. No forma parte del repositorio.
