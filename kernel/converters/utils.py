from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path

# Los archivos Office (.docx, .pptx, .xlsx) son ZIP: uno de pocos KB puede
# descomprimirse en gigas y agotar la memoria del servidor.
MAX_ZIP_UNCOMPRESSED_BYTES = 150 * 1024 * 1024
MAX_ZIP_MEMBERS = 5000


def read_text_bytes(data: bytes) -> str:
    """Decode bytes with common encodings, preferring UTF-8."""
    for encoding in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")


def clean_markdown(text: str) -> str:
    """Normalize whitespace and collapse excessive blank lines."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def heading(level: int, title: str) -> str:
    level = max(1, min(6, level))
    return f"{'#' * level} {title.strip()}\n\n"


def code_fence(content: str, language: str = "") -> str:
    fence = "```"
    while fence in content:
        fence += "`"
    return f"{fence}{language}\n{content.rstrip()}\n{fence}\n\n"


def table_from_rows(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    width = max(len(r) for r in rows)
    normalized = [list(r) + [""] * (width - len(r)) for r in rows]
    header = normalized[0]
    body = normalized[1:] if len(normalized) > 1 else []

    def cell(value: str) -> str:
        return str(value).replace("|", "\\|").replace("\n", " ").strip()

    lines = [
        "| " + " | ".join(cell(c) for c in header) + " |",
        "| " + " | ".join("---" for _ in header) + " |",
    ]
    for row in body:
        lines.append("| " + " | ".join(cell(c) for c in row) + " |")
    return "\n".join(lines) + "\n\n"


def stem_title(filename: str) -> str:
    return Path(filename).stem.replace("_", " ").replace("-", " ").strip() or "Documento"


def check_zip_limits(data: bytes) -> None:
    """Reject corrupt or oversized ZIP containers before parsing them."""
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            members = archive.infolist()
    except zipfile.BadZipFile as exc:
        raise ValueError("El archivo está dañado o no es un documento de Office válido.") from exc

    if len(members) > MAX_ZIP_MEMBERS:
        raise ValueError("El documento contiene demasiados elementos internos.")
    if sum(member.file_size for member in members) > MAX_ZIP_UNCOMPRESSED_BYTES:
        limit_mb = MAX_ZIP_UNCOMPRESSED_BYTES // (1024 * 1024)
        raise ValueError(f"El documento ocupa más de {limit_mb} MB al descomprimirse.")
