from __future__ import annotations

from .utils import clean_markdown, code_fence, heading, read_text_bytes, stem_title, table_from_rows


def from_plain_text(data: bytes, filename: str) -> str:
    text = read_text_bytes(data)
    title = stem_title(filename)
    body = f"{heading(1, title)}{text.strip()}\n"
    return clean_markdown(body)


def from_markdown(data: bytes, filename: str) -> str:
    text = read_text_bytes(data).strip()
    if text.lstrip().startswith("#"):
        return clean_markdown(text)
    return clean_markdown(f"{heading(1, stem_title(filename))}{text}\n")


def from_json(data: bytes, filename: str) -> str:
    import json

    raw = read_text_bytes(data)
    try:
        parsed = json.loads(raw)
        pretty = json.dumps(parsed, ensure_ascii=False, indent=2)
    except json.JSONDecodeError:
        pretty = raw
    return clean_markdown(
        f"{heading(1, stem_title(filename))}"
        f"{heading(2, 'Contenido JSON')}"
        f"{code_fence(pretty, 'json')}"
    )


def from_yaml(data: bytes, filename: str) -> str:
    import yaml

    raw = read_text_bytes(data)
    try:
        parsed = yaml.safe_load(raw)
        pretty = yaml.safe_dump(parsed, allow_unicode=True, sort_keys=False)
    except Exception:
        pretty = raw
    return clean_markdown(
        f"{heading(1, stem_title(filename))}"
        f"{heading(2, 'Contenido YAML')}"
        f"{code_fence(pretty, 'yaml')}"
    )


def from_csv(data: bytes, filename: str) -> str:
    import csv
    import io

    text = read_text_bytes(data)
    reader = csv.reader(io.StringIO(text))
    rows = [list(row) for row in reader]
    table = table_from_rows(rows) if rows else "_Archivo CSV vacío._\n"
    return clean_markdown(
        f"{heading(1, stem_title(filename))}"
        f"{heading(2, 'Tabla')}"
        f"{table}"
    )


def from_xml(data: bytes, filename: str) -> str:
    from bs4 import BeautifulSoup

    raw = read_text_bytes(data)
    soup = BeautifulSoup(raw, "lxml-xml")
    text = soup.get_text("\n", strip=True)
    return clean_markdown(
        f"{heading(1, stem_title(filename))}"
        f"{heading(2, 'Texto extraído')}\n{text}\n\n"
        f"{heading(2, 'XML original')}"
        f"{code_fence(raw.strip(), 'xml')}"
    )


def from_html(data: bytes, filename: str) -> str:
    import html2text
    from bs4 import BeautifulSoup

    raw = read_text_bytes(data)
    soup = BeautifulSoup(raw, "lxml")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    title_tag = soup.find("title")
    page_title = title_tag.get_text(strip=True) if title_tag else stem_title(filename)

    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.body_width = 0
    converter.unicode_snob = True
    md_body = converter.handle(str(soup))

    return clean_markdown(f"{heading(1, page_title)}{md_body}")


def from_rtf(data: bytes, filename: str) -> str:
    from striprtf.striprtf import rtf_to_text

    raw = read_text_bytes(data)
    text = rtf_to_text(raw)
    return clean_markdown(f"{heading(1, stem_title(filename))}{text.strip()}\n")
