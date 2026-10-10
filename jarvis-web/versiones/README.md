# Versiones de Jarvis

- **[HISTORIAL.md](HISTORIAL.md):** qué cambió en cada versión, con un enlace para descargar cada una.
- **Versión actual:** la que indica la constante `VERSION` en `../index.html`. También aparece en la propia aplicación, debajo de "Ajustes y claves".

## Cómo se publica una versión nueva

1. Cambiar la constante `VERSION` en `index.html`.
2. Añadir la versión arriba del todo en `HISTORIAL.md`: número, fecha, título, enlace de descarga, cambios y qué se probó.
3. Hacer el commit, subirlo, y poner en `HISTORIAL.md` los enlaces de ese commit (`https://github.com/Feelingst/markdown/archive/<commit>.zip` para descargar y `https://github.com/Feelingst/markdown/tree/<commit>` para ver el código).

Las versiones antiguas no se copian en esta carpeta: cada commit guarda el proyecto completo tal como estaba. Para recuperar una:
- **Descargarla:** con el enlace de `HISTORIAL.md`.
- **Con git:** `git checkout <commit>` (el commit corto aparece en cada versión del historial).

Al fusionar el PR de Jarvis, usa "Create a merge commit" (no "Squash") para que estos commits sigan existiendo en `main`.

## Etiquetas (opcional)

Cada versión puede llevar además una etiqueta `jarvis-vX.Y.Z` en git, que aparece en GitHub → Tags. Desde la sesión en la nube no se pueden subir etiquetas. Para crearlas desde tu PC, en la carpeta del repositorio:

```bash
git fetch origin
git tag -a jarvis-v0.1.0 7f0b8ec -m "Jarvis v0.1.0"
git tag -a jarvis-v0.2.0 73ddb3b -m "Jarvis v0.2.0"
git tag -a jarvis-v0.3.0 ea7cc3f -m "Jarvis v0.3.0"
git tag -a jarvis-v0.4.0 d2a741e -m "Jarvis v0.4.0"
git tag -a jarvis-v0.5.0 8f8d16b -m "Jarvis v0.5.0"
git tag -a jarvis-v0.6.0 b4dcb9e -m "Jarvis v0.6.0"
git tag -a jarvis-v0.7.0 8c989ba -m "Jarvis v0.7.0"
git push origin --tags
```
