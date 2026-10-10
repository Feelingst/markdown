# Jarvis de Tomás (versión local con micrófono)

Asistente con voz femenina que te llama Tomás y habla en español. Escucha con el micrófono abierto de forma continua: cuando dejas de hablar envía lo que has dicho, responde en voz alta y vuelve a escuchar.

## Abrir Jarvis como aplicación

Descarga la carpeta `jarvis-web` completa y abre Jarvis con doble clic en el lanzador de tu sistema. Se abre en su propia ventana, sin barra de direcciones, con el icono de Jarvis.

| Sistema | Lanzador | Requisitos |
|---|---|---|
| **Windows** | `Jarvis.bat` | Google Chrome o Microsoft Edge (Edge ya viene con Windows) |
| **macOS** | `Jarvis.command` | Chrome o Edge, y `python3` |
| **Linux** | `jarvis.sh` | Chrome, Chromium o Edge, y `python3` |

En Windows, `crear-acceso-directo.bat` pone un acceso directo **Jarvis** con icono en el escritorio.

El lanzador sirve la carpeta en `http://localhost:8765` y abre el navegador en modo aplicación con un perfil propio de Jarvis. Así el permiso del micrófono y las claves se recuerdan. Al cerrar la ventana, el servidor se cierra solo. Firefox no sirve: no tiene reconocimiento de voz.

La primera vez:
1. Pega tu clave de API de Anthropic (console.anthropic.com → API Keys). Opcionalmente, las de ElevenLabs y Simli.
2. Pulsa **Activar micrófono** y acepta el permiso.

Las claves se guardan en el perfil de la aplicación. Si antes abrías `index.html` directamente, tendrás que volver a pegarlas una vez.

Si Windows avisa de que el archivo viene de internet, pulsa "Más información → Ejecutar de todas formas", o antes de abrirlo haz clic derecho en el ZIP → Propiedades → **Desbloquear**.

También puedes seguir abriendo `index.html` directamente con doble clic, pero en ese modo Chrome puede pedir permiso del micrófono cada vez.

## El avatar

Mientras Jarvis habla, el avatar reacciona a lo que dice:

- **Labios sincronizados con la voz.** Cada palabra que pronuncia la voz mueve la boca según sus vocales (la "a" abre más, la "o" y la "u" redondean, la "e" y la "i" estiran). Si tu voz no avisa de cada palabra, usa un ritmo silábico aproximado.
- **Emociones.** Claude etiqueta cada respuesta (alegre, divertida, pensativa, sorprendida, preocupada o neutral) y el avatar cambia de expresión (sonrisa, cejas, inclinación de cabeza, risa) y de color del aro.
- **Gestos.** Parpadea, asiente al terminar una frase, levanta las cejas al preguntar, mira hacia arriba mientras piensa y asiente de vez en cuando mientras te escucha.

### Foto real

- Guarda una foto como `jarvis-avatar.jpg` dentro de la carpeta y aparecerá sola, o
- pulsa **Cambiar foto** y elige una imagen (se recorta en círculo y se guarda en el navegador).
- Pulsa **Ajustar boca** y haz clic en el centro de su boca para que la mandíbula se mueva en el sitio correcto.

Con foto, el avatar abre la boca, mueve la cabeza y cambia el color del aro, pero no cambia la sonrisa ni las cejas: eso solo lo hace el retrato ilustrado. Funciona mejor con una foto de frente, con la boca cerrada y la cara centrada.

## Voz de ElevenLabs

Con la clave y el ID de voz de ElevenLabs, cada frase se pide a ElevenLabs (modelo `eleven_flash_v2_5`, en español) junto con el momento exacto de cada letra. Mientras suena, la boca del avatar se mueve con esos tiempos y con el volumen real del audio, así que el lip sync es mucho más preciso que con la voz del navegador. La siguiente frase se pide mientras suena la anterior para que no haya pausas. Si ElevenLabs falla (clave incorrecta, voz no encontrada, sin saldo), lo avisa y usa la voz del navegador. Las claves se cambian o se quitan en **Ajustes y claves**.

## Vídeo realista con Simli (opcional)

Simli anima en tiempo real la cara de una foto a partir del audio, con lip sync de verdad. Necesita la voz de ElevenLabs.

1. En [app.simli.com](https://app.simli.com) crea una cara a partir de tu foto y copia su **Face ID**. Copia también tu **clave de API**.
2. En **Ajustes y claves**, pega la clave de Simli y el Face ID y guarda.
3. Pulsa **Activar vídeo realista**. El círculo del avatar pasa a mostrar el vídeo de Simli.

Mientras está conectado, cada frase de ElevenLabs (audio PCM de 16 kHz) se envía a Simli, que devuelve el vídeo y el audio ya sincronizados. Pulsa el mismo botón para desconectar: Simli cobra por minuto conectado. Si pasan 5 minutos sin hablar, Simli cierra la sesión y vuelve el avatar local.

## Detalles

- Modelo: `claude-sonnet-5` (constante `MODEL` en `index.html`). El uso se factura en tu cuenta de API, aparte de la suscripción de Claude.
- Mientras Jarvis habla, el micrófono se pausa para que no se oiga a sí misma.
- La voz depende de las voces en español instaladas en tu sistema; elige otra en la lista si la que sale no te convence.
- La conversación no se guarda al recargar la página.
- `anthropic-sdk.js` es el SDK oficial `@anthropic-ai/sdk` 0.128.0 empaquetado para navegador.
- `iniciar-jarvis.ps1` es el servidor local y lanzador de Windows (PowerShell, sin instalar nada). Los datos de la aplicación quedan en `%LOCALAPPDATA%\JarvisTomas`; en macOS y Linux, en `~/.jarvis-tomas`.
- `simli-sdk.js` es el cliente oficial `simli-client` 3.0.2 (con `livekit-client`) empaquetado para navegador.
