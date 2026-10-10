# Jarvis de Tomás (versión local con micrófono)

Asistente con voz femenina que te llama Tomás y habla en español. Escucha con el micrófono abierto de forma continua: cuando dejas de hablar envía lo que has dicho, responde en voz alta y vuelve a escuchar.

## Cómo usarlo

1. Descarga la carpeta `jarvis-web` completa (necesita `index.html`, `anthropic-sdk.js` y `simli-sdk.js` juntos).
2. Abre `index.html` con **Chrome** o **Edge** (doble clic). Firefox no tiene reconocimiento de voz.
3. Pega tu clave de API de Anthropic (créala en console.anthropic.com → API Keys). Se guarda solo en ese navegador.
   Opcional: pega también tu clave de ElevenLabs y el ID de tu voz para que hable con esa voz (el ID está en ElevenLabs → Voices → tu voz → "Copy voice ID").
4. Pulsa **Activar micrófono** y acepta el permiso.

Si Chrome te pide permiso de micrófono una y otra vez, sírvela desde localhost para que lo recuerde:

```bash
cd jarvis-web
python3 -m http.server 8000
# y abre http://localhost:8000
```

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
- `simli-sdk.js` es el cliente oficial `simli-client` 3.0.2 (con `livekit-client`) empaquetado para navegador.
