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
