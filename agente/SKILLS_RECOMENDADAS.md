# Skills recomendadas para nuestros proyectos

Análisis de las 292 skills de [`skills/`](skills/) (ver [INDICE.md](INDICE.md)) frente a los proyectos de la cuenta de GitHub `Feelingst`:

| Proyecto | Qué es | Stack |
|---|---|---|
| **Kernel** (`markdown/kernel`) | Web que convierte documentos (PDF, Word, PowerPoint, Excel, HTML, CSV, JSON…) a Markdown para ahorrar tokens en IA. Pensada para usarse desde el iPhone (PWA). | Python · Flask · pypdf · python-docx/pptx · openpyxl · HTML/JS/CSS sin framework |
| **Jarvis** | Asistente de chat con Claude, con dictado por voz y respuesta hablada (ElevenLabs). Se despliega en Vercel y se instala en el iPhone. | Next.js 14 · React 18 · API de Anthropic · ElevenLabs |

`Hello-world` (2017) no tiene código relevante y queda fuera del análisis.

Ninguno de los dos proyectos tiene tests, CI ni revisión de seguridad. Por eso las recomendaciones de más prioridad son de calidad y seguridad, no de funcionalidad nueva.

---

## Prioridad alta: usar ya

| Skill | Proyecto | Por qué |
|---|---|---|
| [security-review](skills/security-review/SKILL.md) | Ambos | **Kernel** arranca con `app.run(host="0.0.0.0", debug=True)` (`kernel/app.py:151`), lo que expone el depurador de Werkzeug a toda la red local. Además acepta subidas de archivos y devuelve al usuario el texto de las excepciones. En **Jarvis**, `/api/chat` y `/api/speak` son públicos y sin límite de uso, así que cualquiera con la URL consume las claves de Anthropic y ElevenLabs. |
| [python-testing](skills/python-testing/SKILL.md) | Kernel | No hay tests. Los conversores de `kernel/converters/` son funciones puras (`bytes → markdown`), ideales para tests parametrizados con pytest y archivos de ejemplo por formato. |
| [react-testing](skills/react-testing/SKILL.md) | Jarvis | No hay tests. Explica React Testing Library y MSW, que sirve para simular `/api/chat` y `/api/speak` sin gastar llamadas reales. |
| [cost-aware-llm-pipeline](skills/cost-aware-llm-pipeline/SKILL.md) | Jarvis | En cada mensaje se reenvía todo el historial sin *prompt caching* ni control de presupuesto. La skill cubre `cache_control`, el enrutado entre modelos (Haiku para lo simple, Sonnet para lo complejo) y el seguimiento de gasto. Sus ejemplos ya usan identificadores de modelo actuales. |
| [error-handling](skills/error-handling/SKILL.md) | Ambos | Jarvis muestra en el chat el error crudo de la API (`"Error de la API: " + errText`) y Kernel captura cualquier `Exception` y la reenvía tal cual. La skill trata los mensajes de error para el usuario, los reintentos y los errores tipados en Python y TypeScript. |

## Prioridad media: mejoras concretas

### Kernel

| Skill | Por qué |
|---|---|
| [content-hash-cache-pattern](skills/content-hash-cache-pattern/SKILL.md) | Usa como ejemplo justo este caso (caché de extracción de PDF por hash SHA-256). Evita reconvertir un archivo repetido y da una base para limpiar `outputs/`, que ahora crece sin límite porque nada borra los `.md` generados. |
| [regex-vs-llm-structured-text](skills/regex-vs-llm-structured-text/SKILL.md) | Ahora el PDF sale como texto plano por página, sin títulos, listas ni tablas. La skill ayuda a decidir qué estructura detectar con reglas y cuándo merece la pena un LLM, que en Kernel iría contra el objetivo de ahorrar tokens. |
| [python-patterns](skills/python-patterns/SKILL.md) | Convenciones (tipado, estructura, PEP 8) para que los conversores crezcan de forma ordenada. |
| [nutrient-document-processing](skills/nutrient-document-processing/SKILL.md) | *Opcional.* Los PDF escaneados no tienen texto extraíble y Kernel devuelve "Sin texto extraíble". Esta skill añade OCR mediante la API de Nutrient, pero es **de pago**: habría que valorar el coste o buscar una alternativa local (p. ej. Tesseract). |
| [mcp-server-patterns](skills/mcp-server-patterns/SKILL.md) | *Idea a futuro.* Exponer Kernel como servidor MCP para que Claude convierta documentos directamente. La skill usa el SDK de Node/TypeScript, así que en Python solo aprovecharíamos el diseño y no el código. |

### Jarvis

| Skill | Por qué |
|---|---|
| [react-patterns](skills/react-patterns/SKILL.md) / [frontend-patterns](skills/frontend-patterns/SKILL.md) | Toda la interfaz está en un solo componente de 206 líneas (`app/page.js`) con 8 estados. Dan pautas para separar chat, voz y audio en hooks y componentes. |
| [frontend-a11y](skills/frontend-a11y/SKILL.md) | Accesibilidad para React/Next.js: botones de micrófono y voz con etiquetas, anuncios de mensajes nuevos para lectores de pantalla, foco del teclado. |
| [api-design](skills/api-design/SKILL.md) | Contrato de `/api/chat` y `/api/speak`: validación de entrada, códigos de estado y límites de tamaño del texto enviado a síntesis de voz. |

### Ambos (interfaz móvil / PWA)

| Skill | Por qué |
|---|---|
| [make-interfaces-feel-better](skills/make-interfaces-feel-better/SKILL.md) | Detalles de acabado (áreas táctiles, tipografía, estados, movimiento). Los dos proyectos se usan sobre todo desde el iPhone. |

## Despliegue y verificación

| Skill | Proyecto | Por qué |
|---|---|---|
| [production-audit](skills/production-audit/SKILL.md) | Ambos | Revisión local de "qué se rompe en producción" antes de publicar, sin enviar el código a servicios externos. Detectaría, por ejemplo, que en `.env.example` de Jarvis faltan `ELEVENLABS_API_KEY` y `ELEVENLABS_VOICE_ID`, y que `manifest.json` tiene `"icons": []`. En iPhone, eso deja la app sin icono al añadirla a la pantalla de inicio. |
| [deployment-patterns](skills/deployment-patterns/SKILL.md) | Ambos | CI/CD y comprobaciones previas a publicar. Kernel no tiene despliegue (solo `run.sh` local) y Jarvis depende de Vercel sin ninguna comprobación automática. |
| [canary-watch](skills/canary-watch/SKILL.md) | Jarvis | Comprobar la URL de Vercel después de cada despliegue: endpoints, recursos estáticos y errores de consola. |
| [browser-qa](skills/browser-qa/SKILL.md) / [e2e-testing](skills/e2e-testing/SKILL.md) | Ambos | Pruebas de extremo a extremo con Playwright: subir un archivo y descargar el `.md` en Kernel, y enviar un mensaje en Jarvis. Incluye emulación de móvil. |
| [verification-loop](skills/verification-loop/SKILL.md) | Ambos | Lista de comprobación para que Claude verifique su trabajo antes de dar un cambio por terminado. |

## Descartadas (aunque parezcan relevantes)

| Skill | Motivo |
|---|---|
| [nextjs-turbopack](skills/nextjs-turbopack/SKILL.md) | Es para Next.js 16 o superior, y Jarvis usa Next.js 14.2.5. Solo sería útil si se actualiza. |
| [ios-icon-gen](skills/ios-icon-gen/SKILL.md) | Genera iconos para catálogos de Xcode (apps nativas), no para una PWA. |
| [fastapi-patterns](skills/fastapi-patterns/SKILL.md), `django-*` | Kernel usa Flask. Solo aplicarían si se migrara el backend. |
| [frontend-slides](skills/frontend-slides/SKILL.md), [visa-doc-translate](skills/visa-doc-translate/SKILL.md) | Tocan documentos o conversión, pero para otros fines (presentaciones, traducción de visados). |
| Skills sectoriales (salud, logística, finanzas, redes, blockchain, Laravel, Spring, Kotlin, Swift, etc.) | No corresponden a ningún stack ni dominio de los proyectos. |

## Orden sugerido

1. **security-review** en ambos proyectos (empezando por el `debug=True` de Kernel y los endpoints abiertos de Jarvis).
2. **python-testing** y **react-testing** para tener una red de seguridad antes de refactorizar.
3. **cost-aware-llm-pipeline** en Jarvis (ahorro directo en la factura de la API).
4. **production-audit** + **deployment-patterns** antes del siguiente despliegue.
5. El resto según las funcionalidades que se quieran añadir.
