(() => {
  const form = document.getElementById("convert-form");
  const input = document.getElementById("file-input");
  const surface = document.getElementById("drop-surface");
  const chip = document.getElementById("file-chip");
  const convertBtn = document.getElementById("convert-btn");
  const status = document.getElementById("status");
  const result = document.getElementById("result");
  const preview = document.getElementById("preview");
  const meta = document.getElementById("result-meta");
  const downloadBtn = document.getElementById("download-btn");
  const copyBtn = document.getElementById("copy-btn");
  const shareBtn = document.getElementById("share-btn");
  const againBtn = document.getElementById("again-btn");
  const uploadSection = document.getElementById("upload-section");

  let selectedFile = null;
  let lastMarkdown = "";
  let lastFilename = "documento.md";

  const canShareFiles =
    typeof navigator.share === "function" &&
    typeof navigator.canShare === "function";

  if (canShareFiles || typeof navigator.share === "function") {
    shareBtn.hidden = false;
  }

  function setStatus(message, type = "") {
    status.textContent = message || "";
    status.classList.remove("is-error", "is-busy");
    if (type) status.classList.add(type);
  }

  function showFile(file) {
    selectedFile = file;
    convertBtn.disabled = !file;
    if (!file) {
      chip.hidden = true;
      chip.textContent = "";
      return;
    }
    const mb = (file.size / (1024 * 1024)).toFixed(2);
    chip.hidden = false;
    chip.innerHTML = `Seleccionado: <strong>${escapeHtml(file.name)}</strong> · ${mb} MB`;
    setStatus("");
  }

  function escapeHtml(value) {
    return value
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  function openPicker() {
    input.click();
  }

  surface.addEventListener("click", openPicker);
  surface.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      openPicker();
    }
  });

  input.addEventListener("change", () => {
    const file = input.files && input.files[0];
    showFile(file || null);
  });

  ["dragenter", "dragover"].forEach((name) => {
    surface.addEventListener(name, (event) => {
      event.preventDefault();
      event.stopPropagation();
      form.classList.add("is-drag");
    });
  });

  ["dragleave", "drop"].forEach((name) => {
    surface.addEventListener(name, (event) => {
      event.preventDefault();
      event.stopPropagation();
      form.classList.remove("is-drag");
    });
  });

  surface.addEventListener("drop", (event) => {
    const file = event.dataTransfer && event.dataTransfer.files && event.dataTransfer.files[0];
    if (!file) return;
    showFile(file);
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      setStatus("Elige un archivo primero.", "is-error");
      return;
    }

    convertBtn.disabled = true;
    setStatus("Convirtiendo", "is-busy");

    const body = new FormData();
    body.append("file", selectedFile);

    try {
      const response = await fetch("/api/convert", {
        method: "POST",
        body,
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || "Error al convertir.");
      }

      lastMarkdown = payload.markdown || "";
      lastFilename = payload.filename || "documento.md";
      preview.textContent = lastMarkdown;
      meta.textContent = `${payload.filename} · ${payload.stats.characters.toLocaleString("es")} caracteres · ~${payload.stats.approx_tokens.toLocaleString("es")} tokens`;
      downloadBtn.href = `/api/download/${payload.download_id}`;
      downloadBtn.setAttribute("download", payload.filename);
      result.hidden = false;
      uploadSection.hidden = true;
      setStatus("");
      result.scrollIntoView({ behavior: "smooth", block: "start" });
    } catch (error) {
      setStatus(error.message || "No se pudo convertir el archivo.", "is-error");
      convertBtn.disabled = false;
    }
  });

  copyBtn.addEventListener("click", async () => {
    if (!lastMarkdown) return;
    try {
      await navigator.clipboard.writeText(lastMarkdown);
      copyBtn.textContent = "Copiado";
      setTimeout(() => {
        copyBtn.textContent = "Copiar";
      }, 1600);
    } catch (_error) {
      // Fallback for older iOS Safari
      const range = document.createRange();
      range.selectNodeContents(preview);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      setStatus("Seleccionado. Mantén pulsado → Copiar.", "is-error");
    }
  });

  shareBtn.addEventListener("click", async () => {
    if (!lastMarkdown || typeof navigator.share !== "function") return;
    const file = new File([lastMarkdown], lastFilename, {
      type: "text/markdown",
    });
    try {
      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file],
          title: lastFilename,
          text: "Markdown generado con Kernel",
        });
      } else {
        await navigator.share({
          title: lastFilename,
          text: lastMarkdown.slice(0, 4000),
        });
      }
    } catch (error) {
      if (error && error.name === "AbortError") return;
      setStatus("No se pudo compartir. Usa Copiar o Descargar.", "is-error");
    }
  });

  againBtn.addEventListener("click", () => {
    result.hidden = true;
    uploadSection.hidden = false;
    input.value = "";
    showFile(null);
    lastMarkdown = "";
    lastFilename = "documento.md";
    preview.textContent = "";
    setStatus("");
    convertBtn.disabled = true;
    window.scrollTo({ top: 0, behavior: "smooth" });
  });
})();
