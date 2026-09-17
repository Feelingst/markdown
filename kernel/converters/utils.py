from __future__ import annotations

import re
from pathlib import Path


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
