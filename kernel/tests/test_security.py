from __future__ import annotations

import io
import os
import time
import zipfile

import pytest
from docx import Document

import app as kernel_app
from converters import convert_file, utils


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(kernel_app, "OUTPUT_DIR", tmp_path)
    kernel_app.app.config["TESTING"] = True
    return kernel_app.app.test_client()


def make_docx(text: str = "Hola") -> bytes:
    document = Document()
    document.add_paragraph(text)
    buffer = io.BytesIO()
    document.save(buffer)
    return buffer.getvalue()


def upload(client, data: bytes, filename: str):
    return client.post(
        "/api/convert",
        data={"file": (io.BytesIO(data), filename)},
        content_type="multipart/form-data",
    )


def test_security_headers(client):
    response = client.get("/")
    csp = response.headers["Content-Security-Policy"]
    assert "script-src 'self'" in csp
    assert "frame-ancestors 'none'" in csp
    assert response.headers["X-Content-Type-Options"] == "nosniff"
    assert response.headers["X-Frame-Options"] == "DENY"


def test_valid_docx_still_converts(client):
    response = upload(client, make_docx("Contenido de prueba"), "ok.docx")
    assert response.status_code == 200
    assert "Contenido de prueba" in response.get_json()["markdown"]


def test_unexpected_errors_do_not_leak_details(client, monkeypatch):
    def boom(data, filename):
        raise RuntimeError("/srv/secreto/ruta interna")

    monkeypatch.setattr(kernel_app, "convert_file", boom)
    response = upload(client, b"hola", "a.txt")
    assert response.status_code == 500
    assert "secreto" not in response.get_json()["error"]


def test_zip_bomb_is_rejected(client, monkeypatch):
    monkeypatch.setattr(utils, "MAX_ZIP_UNCOMPRESSED_BYTES", 1024 * 1024)
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("word/document.xml", b"0" * (2 * 1024 * 1024))
    data = buffer.getvalue()
    assert len(data) < 20 * 1024

    response = upload(client, data, "bomba.docx")
    assert response.status_code == 400
    assert "descomprimirse" in response.get_json()["error"]


def test_corrupt_office_file_is_rejected(client):
    response = upload(client, b"no es un zip", "roto.xlsx")
    assert response.status_code == 400


def test_xml_external_entities_are_not_resolved():
    payload = b'<?xml version="1.0"?><!DOCTYPE r [<!ENTITY x SYSTEM "file:///etc/passwd">]><r>&x;</r>'
    assert "root:" not in convert_file(payload, "xxe.xml")


def test_download_rejects_invalid_ids(client):
    assert client.get("/api/download/..%2F..%2Fapp.py").status_code in (400, 404)
    assert client.get("/api/download/not-a-token").status_code == 400


def test_expired_outputs_are_purged(client, tmp_path):
    old = tmp_path / f"{'a' * 32}_viejo.md"
    old.write_text("x", encoding="utf-8")
    past = time.time() - kernel_app.OUTPUT_TTL_SECONDS - 60
    os.utime(old, (past, past))

    response = client.get(f"/api/download/{'a' * 32}")
    assert response.status_code == 404
    assert not old.exists()


def test_debug_is_off_by_default():
    source = (kernel_app.BASE_DIR / "app.py").read_text(encoding="utf-8")
    assert "debug=True" not in source
