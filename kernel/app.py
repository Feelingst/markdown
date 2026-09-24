from __future__ import annotations

import os
import re
import time
import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

from converters import convert_file, supported_extensions, supported_label

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB
OUTPUT_TTL_SECONDS = 60 * 60  # los .md generados se borran tras 1 hora

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

CONTENT_SECURITY_POLICY = "; ".join(
    [
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self' https://fonts.googleapis.com",
        "font-src https://fonts.gstatic.com",
        "img-src 'self' data:",
        "connect-src 'self'",
        "manifest-src 'self'",
        "object-src 'none'",
        "base-uri 'none'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ]
)


@app.after_request
def security_headers(response):
    response.headers.setdefault("Content-Security-Policy", CONTENT_SECURITY_POLICY)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    return response


def purge_expired_outputs() -> None:
    cutoff = time.time() - OUTPUT_TTL_SECONDS
    for path in OUTPUT_DIR.glob("*.md"):
        try:
            if path.stat().st_mtime < cutoff:
                path.unlink()
        except FileNotFoundError:
            pass


def safe_stem(filename: str) -> str:
    stem = Path(filename).stem
    cleaned = re.sub(r"[^\w\-]+", "_", stem, flags=re.UNICODE).strip("_")
    return cleaned[:80] or "documento"


ACCEPT_MIME = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xlsm": "application/vnd.ms-excel.sheet.macroEnabled.12",
    ".html": "text/html",
    ".htm": "text/html",
    ".csv": "text/csv",
    ".tsv": "text/tab-separated-values",
    ".json": "application/json",
    ".xml": "application/xml",
    ".txt": "text/plain",
    ".md": "text/markdown",
    ".markdown": "text/markdown",
    ".yaml": "application/yaml",
    ".yml": "application/yaml",
    ".rtf": "application/rtf",
}


def build_accept() -> str:
    parts: list[str] = []
    for ext in supported_extensions():
        parts.append(ext)
        mime = ACCEPT_MIME.get(ext)
        if mime and mime not in parts:
            parts.append(mime)
    return ",".join(parts)


@app.get("/")
def index():
    return render_template(
        "index.html",
        formats=supported_label(),
        extensions=",".join(supported_extensions()),
        accept=build_accept(),
        max_mb=MAX_CONTENT_LENGTH // (1024 * 1024),
    )


@app.get("/api/formats")
def formats():
    return jsonify(
        {
            "extensions": supported_extensions(),
            "labels": supported_label(),
            "max_upload_mb": MAX_CONTENT_LENGTH // (1024 * 1024),
        }
    )


@app.post("/api/convert")
def convert():
    if "file" not in request.files:
        return jsonify({"error": "No se envió ningún archivo."}), 400

    uploaded = request.files["file"]
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "El archivo está vacío o sin nombre."}), 400

    filename = Path(uploaded.filename).name
    data = uploaded.read()
    if not data:
        return jsonify({"error": "El archivo está vacío."}), 400

    try:
        markdown = convert_file(data, filename)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:  # noqa: BLE001
        app.logger.exception("Fallo al convertir %r", filename)
        return jsonify({"error": "No se pudo convertir el archivo. Comprueba que no esté dañado."}), 500

    purge_expired_outputs()
    token = uuid.uuid4().hex
    out_name = f"{safe_stem(filename)}.md"
    out_path = OUTPUT_DIR / f"{token}_{out_name}"
    out_path.write_text(markdown, encoding="utf-8")

    chars = len(markdown)
    approx_tokens = max(1, chars // 4)

    return jsonify(
        {
            "ok": True,
            "filename": out_name,
            "download_id": token,
            "markdown": markdown,
            "stats": {
                "characters": chars,
                "lines": markdown.count("\n") + (0 if markdown.endswith("\n") else 1),
                "approx_tokens": approx_tokens,
            },
        }
    )


@app.get("/api/download/<download_id>")
def download(download_id: str):
    if not re.fullmatch(r"[a-f0-9]{32}", download_id):
        return jsonify({"error": "Identificador inválido."}), 400

    purge_expired_outputs()
    matches = list(OUTPUT_DIR.glob(f"{download_id}_*.md"))
    if not matches:
        return jsonify({"error": "Archivo no encontrado o expirado."}), 404

    path = matches[0]
    download_name = path.name.split("_", 1)[1]
    return send_file(
        path,
        as_attachment=True,
        download_name=download_name,
        mimetype="text/markdown",
    )


@app.errorhandler(413)
def too_large(_error):
    return jsonify({"error": f"El archivo supera el límite de {MAX_CONTENT_LENGTH // (1024 * 1024)} MB."}), 413


if __name__ == "__main__":
    # El depurador de Werkzeug permite ejecutar código: solo se activa a
    # propósito (KERNEL_DEBUG=1) y, en ese caso, escucha solo en local.
    debug = os.environ.get("KERNEL_DEBUG") == "1"
    host = os.environ.get("KERNEL_HOST", "127.0.0.1" if debug else "0.0.0.0")
    port = int(os.environ.get("KERNEL_PORT", "5000"))
    app.run(host=host, port=port, debug=debug)
