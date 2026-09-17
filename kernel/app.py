from __future__ import annotations

import re
import uuid
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file

from converters import convert_file, supported_extensions, supported_label

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
MAX_CONTENT_LENGTH = 25 * 1024 * 1024  # 25 MB

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH


def safe_stem(filename: str) -> str:
    stem = Path(filename).stem
    cleaned = re.sub(r"[^\w\-]+", "_", stem, flags=re.UNICODE).strip("_")
    return cleaned[:80] or "documento"


@app.get("/")
def index():
    return render_template(
        "index.html",
        formats=supported_label(),
        extensions=",".join(supported_extensions()),
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
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": f"No se pudo convertir el archivo: {exc}"}), 500

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
    app.run(host="0.0.0.0", port=5000, debug=True)
