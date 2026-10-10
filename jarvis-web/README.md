# Jarvis de Tomás (versión local con micrófono)

Asistente con voz femenina que te llama Tomás y habla en español. Escucha con el micrófono abierto de forma continua: cuando dejas de hablar envía lo que has dicho, responde en voz alta y vuelve a escuchar.

## Cómo usarlo

1. Descarga la carpeta `jarvis-web` completa (necesita `index.html` y `anthropic-sdk.js` juntos).
2. Abre `index.html` con **Chrome** o **Edge** (doble clic). Firefox no tiene reconocimiento de voz.
3. Pega tu clave de API de Anthropic (créala en console.anthropic.com → API Keys). Se guarda solo en ese navegador.
4. Pulsa **Activar micrófono** y acepta el permiso.

Si Chrome te pide permiso de micrófono una y otra vez, sírvela desde localhost para que lo recuerde:

```bash
cd jarvis-web
python3 -m http.server 8000
# y abre http://localhost:8000
```

## La foto del avatar

- Guarda una foto como `jarvis-avatar.jpg` dentro de la carpeta y aparecerá sola, o
- pulsa **Cambiar foto** y elige una imagen (se recorta en círculo y se guarda en el navegador).

Sin foto se muestra un retrato ilustrado.

## Detalles

- Modelo: `claude-sonnet-5` (constante `MODEL` en `index.html`). El uso se factura en tu cuenta de API, aparte de la suscripción de Claude.
- Mientras Jarvis habla, el micrófono se pausa para que no se oiga a sí misma.
- La voz depende de las voces en español instaladas en tu sistema; elige otra en la lista si la que sale no te convence.
- La conversación no se guarda al recargar la página.
- `anthropic-sdk.js` es el SDK oficial `@anthropic-ai/sdk` 0.128.0 empaquetado para navegador.
