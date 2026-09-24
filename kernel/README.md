# Kernel

Convierte documentos a Markdown estructurado para reducir tokens en plataformas de IA.

## Formatos

PDF, Word (`.docx`), PowerPoint (`.pptx`), Excel (`.xlsx`), HTML, CSV, JSON, YAML, XML, RTF, TXT, Markdown.

## Arranque

```bash
cd kernel
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Abre `http://127.0.0.1:5000` en el teléfono (misma red) o en la computadora.

## Uso

1. Sube o suelta un archivo.
2. Pulsa **Convertir a Markdown**.
3. Copia el resultado o descarga el `.md`.

## Configuración

| Variable | Por defecto | Uso |
|---|---|---|
| `KERNEL_HOST` | `0.0.0.0` (`127.0.0.1` con depuración) | Interfaz de red en la que escucha. |
| `KERNEL_PORT` | `5000` | Puerto. |
| `KERNEL_DEBUG` | desactivado | `1` activa el modo depuración de Flask. Solo para desarrollo: el depurador permite ejecutar código en el servidor. |

## Seguridad

- Los documentos de Office que ocupen más de 150 MB al descomprimirse se rechazan (protección frente a *zip bombs*).
- Los `.md` generados se borran del servidor al cabo de una hora; el archivo original nunca se guarda.
- Los errores internos se registran en el servidor y el usuario solo ve un mensaje genérico.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest tests
```
