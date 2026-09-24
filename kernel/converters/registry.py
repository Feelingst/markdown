from __future__ import annotations

from pathlib import Path

from .office import from_docx, from_pdf, from_pptx, from_xlsx
from .text_formats import (
    from_csv,
    from_html,
    from_json,
    from_markdown,
    from_plain_text,
    from_rtf,
    from_xml,
    from_yaml,
)
from .utils import check_zip_limits, clean_markdown, heading, read_text_bytes, stem_title

HANDLERS = {
    ".txt": from_plain_text,
    ".md": from_markdown,
    ".markdown": from_markdown,
    ".json": from_json,
    ".yaml": from_yaml,
    ".yml": from_yaml,
    ".csv": from_csv,
    ".tsv": from_csv,
    ".xml": from_xml,
    ".html": from_html,
    ".htm": from_html,
    ".rtf": from_rtf,
    ".pdf": from_pdf,
    ".docx": from_docx,
    ".pptx": from_pptx,
    ".xlsx": from_xlsx,
    ".xlsm": from_xlsx,
}

ZIP_BASED = {".docx", ".pptx", ".xlsx", ".xlsm"}

LABELS = {
    ".txt": "Texto",
    ".md": "Markdown",
    ".markdown": "Markdown",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".csv": "CSV",
    ".tsv": "TSV",
    ".xml": "XML",
    ".html": "HTML",
    ".htm": "HTML",
    ".rtf": "RTF",
    ".pdf": "PDF",
    ".docx": "Word",
    ".pptx": "PowerPoint",
    ".xlsx": "Excel",
    ".xlsm": "Excel",
}


def supported_extensions() -> list[str]:
    return sorted(HANDLERS.keys())


def supported_label() -> str:
    names = sorted({LABELS[ext] for ext in HANDLERS})
    return ", ".join(names)


def convert_file(data: bytes, filename: str) -> str:
    ext = Path(filename).suffix.lower()
    handler = HANDLERS.get(ext)

    if handler is None:
        try:
            text = read_text_bytes(data).strip()
        except Exception as exc:  # noqa: BLE001
            raise ValueError(
                f"Formato no soportado: {ext or '(sin extensión)'}. "
                f"Usa uno de: {', '.join(supported_extensions())}"
            ) from exc
        if not text:
            raise ValueError(
                f"Formato no soportado: {ext or '(sin extensión)'}. "
                f"Usa uno de: {', '.join(supported_extensions())}"
            )
        return clean_markdown(
            f"{heading(1, stem_title(filename))}"
            f"> Formato `{ext or 'desconocido'}` no reconocido; se interpretó como texto plano.\n\n"
            f"{text}\n"
        )

    if ext in ZIP_BASED:
        check_zip_limits(data)
    return clean_markdown(handler(data, filename))
