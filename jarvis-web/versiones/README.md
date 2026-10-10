# Versiones de Jarvis

- **[HISTORIAL.md](HISTORIAL.md):** qué cambió en cada versión, con un enlace para descargar cada una.
- **Versión actual:** la que indica la constante `VERSION` en `../index.html`. También aparece en la propia aplicación, debajo de "Ajustes y claves".

## Cómo se publica una versión nueva

1. Cambiar la constante `VERSION` en `index.html`.
2. Añadir la versión arriba del todo en `HISTORIAL.md`: número, fecha, título, enlace de descarga, cambios y qué se probó.
3. Hacer el commit y marcarlo con la etiqueta de la versión:
   ```bash
   git tag -a jarvis-v0.8.0 -m "Jarvis v0.8.0"
   git push origin jarvis-v0.8.0
   ```

Las versiones antiguas no se copian en esta carpeta: cada etiqueta guarda el proyecto completo tal como estaba. Para recuperar una:
- **Descargarla:** con el enlace de `HISTORIAL.md`, o en GitHub → Tags.
- **Con git:** `git checkout jarvis-v0.4.0`.
