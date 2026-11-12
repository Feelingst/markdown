# Jarvis de Tomás (versión local con micrófono)

Asistente con voz femenina que te llama Tomás y habla en español. Escucha con el micrófono abierto de forma continua: cuando dejas de hablar envía lo que has dicho, responde en voz alta y vuelve a escuchar.

**Gratis por defecto:** el "cerebro" es [Ollama](https://ollama.com), un modelo de IA que funciona en tu propio ordenador, sin internet ni coste. Opcionalmente se puede usar Claude (API de Anthropic, de pago) desde los ajustes.

## Instalar Ollama (una sola vez)

1. Descarga e instala Ollama desde **ollama.com** (Windows, macOS o Linux). Se queda abierto en segundo plano: en Windows verás el icono de la llama junto al reloj.
2. Abre una terminal (en Windows, PowerShell) y descarga el modelo:
   ```
   ollama pull llama3.2:3b
   ```
   Son unos 2 GB. Cuando termine, Jarvis ya puede pensar.

**Qué modelo elegir** (se cambia en **Ajustes y claves** → Modelo de Ollama):

| Modelo | Tamaño aprox. | Para qué |
|---|---|---|
| `llama3.2:3b` | 2 GB | Opción por defecto: buen equilibrio entre rapidez y calidad en español |
| `gemma3:1b` | 1 GB | El más rápido, para ordenadores modestos; respuestas más simples |
| `gemma3:4b` | 3 GB | Mejor calidad, pero más lento |

En un PC sin tarjeta gráfica (por ejemplo, con un Intel N150 y 16 GB de RAM) cuenta con unos segundos de espera por respuesta, más que con Claude. La primera pregunta tarda más porque el modelo se carga en memoria; después se queda cargado 30 minutos.

Abre Jarvis con el lanzador (`Jarvis.bat`) y no desde un enlace de internet: Ollama solo acepta peticiones de páginas abiertas en tu propio ordenador.

## Abrir Jarvis como aplicación

Descarga la carpeta `jarvis-web` completa y abre Jarvis con doble clic en el lanzador de tu sistema. Se abre en su propia ventana, sin barra de direcciones, con el icono de Jarvis.

| Sistema | Lanzador | Requisitos |
|---|---|---|
| **Windows** | `Jarvis.bat` | Microsoft Edge (ya viene con Windows) o Google Chrome |
| **macOS** | `Jarvis.command` | Chrome o Edge, y `python3` |
| **Linux** | `jarvis.sh` | Chrome, Chromium o Edge, y `python3` |

En Windows, `crear-acceso-directo.bat` pone un acceso directo **Jarvis** con icono en el escritorio.

El lanzador sirve la carpeta en `http://localhost:8765` y abre el navegador en modo aplicación con un perfil propio de Jarvis. Así el permiso del micrófono y las claves se recuerdan. Al cerrar la ventana, el servidor se cierra solo. Firefox no sirve: no tiene reconocimiento de voz.

La primera vez:
1. Comprueba que Ollama está abierto y que descargaste el modelo. Si falta algo, Jarvis te lo dice al abrirse.
2. Pulsa **Activar micrófono** y acepta el permiso.

En Windows el lanzador abre **Edge** si lo encuentra: trae voces femeninas naturales en español (Elvira, Dalia…) y su reconocimiento de voz suele funcionar en redes donde el de Chrome falla.

Las claves se guardan en el perfil de la aplicación. Si antes abrías `index.html` directamente, tendrás que volver a pegarlas una vez.

Si Windows avisa de que el archivo viene de internet, pulsa "Más información → Ejecutar de todas formas", o antes de abrirlo haz clic derecho en el ZIP → Propiedades → **Desbloquear**.

También puedes seguir abriendo `index.html` directamente con doble clic, pero en ese modo Chrome puede pedir permiso del micrófono cada vez.

## Conexiones

Se configuran en **Ajustes y claves** → **Conexiones**. Jarvis decide solo cuándo usarlas: si le preguntas por el tiempo, mira el tiempo; si le pides encender una luz, se lo pide a Home Assistant; si charláis, no usa ninguna.

### Internet: el tiempo y Wikipedia (gratis, activado de serie)
- **El tiempo:** con [Open-Meteo](https://open-meteo.com), sin clave. Escribe tu ciudad en Ajustes para que "¿qué tiempo hace?" funcione sin decirla.
- **Wikipedia en español:** para preguntas sobre personas, lugares, historia o ciencia.
- No es un buscador general: no sabe noticias ni resultados deportivos.

### Home Assistant (gratis)
Jarvis pasa tus órdenes de casa a **Assist**, el asistente de Home Assistant, que ya conoce tus dispositivos y entiende español ("enciende la luz de Tomás", "¿qué temperatura hay en el salón?", "pon el robot a limpiar").

1. **Crea un token:** en Home Assistant, abre tu perfil (abajo a la izquierda) → **Seguridad** → **Tokens de acceso de larga duración** → **Crear token**. Ponle de nombre "Jarvis" y copia el token, que solo se muestra una vez.
2. **Deja que Jarvis se conecte.** En Home Assistant 2026.11 o posterior: Ajustes → Sistema → Red → **Servidor HTTP** → Más opciones → **Orígenes permitidos por CORS** → añade `http://localhost:8765` → Guardar → **Confirmar**. En versiones anteriores, añade esto al final de `configuration.yaml` (por ejemplo con el complemento **File editor**, en Ajustes → Complementos):
   ```yaml
   http:
     cors_allowed_origins:
       - http://localhost:8765
   ```
   Si ya tienes una sección `http:`, añade solo las líneas de `cors_allowed_origins`. Después reinicia Home Assistant (Ajustes → Sistema → Reiniciar).
3. **En Jarvis**, en Ajustes → Conexiones: pon la dirección de Home Assistant (normalmente `http://homeassistant.local:8123`, o la IP, por ejemplo `http://192.168.1.50:8123`) y pega el token. Al guardar, Jarvis comprueba la conexión y te dice si algo falla.

Si no conecta, Jarvis dice por qué. Lo más habitual en Windows es que no reconozca `homeassistant.local`: usa la IP de Home Assistant (Ajustes → Sistema → Red, o en tu router), por ejemplo `http://192.168.1.50:8123`.

Lo que Home Assistant pueda hacer con Assist, Jarvis lo puede hacer por voz. Las órdenes de casa van directamente a Assist, sin pasar por el modelo. Si Assist no reconoce cómo llamas a un dispositivo, añádele un **alias** en Home Assistant (Ajustes → Asistentes de voz → Exponer → el dispositivo → Alias), por ejemplo "luz de Tomás". Si una orden no funciona, prueba a decirla con el nombre exacto del dispositivo tal como aparece en Home Assistant.

## Jarvis en el iPhone (con Home Assistant)

Jarvis también funciona desde el iPhone, en casa y fuera (con datos móviles), a través de Home Assistant y Home Assistant Cloud. No tiene avatar, pero habla con la misma personalidad y controla la casa.

1. **Ollama accesible en la red de casa.** En PowerShell como administrador:
   ```powershell
   setx OLLAMA_HOST "0.0.0.0" /M
   New-NetFirewallRule -DisplayName "Ollama (Home Assistant)" -Direction Inbound -Protocol TCP -LocalPort 11434 -RemoteAddress 192.168.1.0/24 -Action Allow
   ```
   Reinicia Ollama (o el PC). Comprueba que `netstat -ano | findstr 11434` muestra `0.0.0.0:11434`.
2. **Integración Ollama en Home Assistant:** Ajustes → Dispositivos y servicios → Añadir integración → Ollama, con la URL `http://IP-DEL-PC:11434` (sin clave API). Crea un agente de conversación:
   - nombre `Jarvis`, modelo `llama3.2:3b` y las instrucciones de personalidad;
   - herramientas de IA sin marcar;
   - contexto 4096, historial 10, "Mantener vivo" en -1 y "Pensar antes de responder" desactivado.
3. **Asistente de voz:** Ajustes → Asistentes de voz → Añadir asistente "Jarvis":
   - idioma español y agente Jarvis;
   - **"Preferir manejar comandos localmente"** activado;
   - voz a texto y texto a voz con Home Assistant Cloud en español de España, voz **Elvira**;
   - márcalo como preferido.
4. **En el iPhone:** en la app Home Assistant, botón Assist → Jarvis. Para usar **"Oye Siri, Jarvis"**, crea un atajo en la app Atajos con la acción Assist de Home Assistant.

Las órdenes de casa funcionan aunque el PC esté apagado, porque las resuelve Home Assistant. Para charlar, el PC tiene que estar encendido con Ollama. Si el router cambia la IP del PC, actualiza la URL de la integración Ollama, o reserva la IP en el router.

## El avatar

Mientras Jarvis habla, el avatar reacciona a lo que dice:

- **Labios sincronizados con la voz.** Cada palabra que pronuncia la voz mueve la boca según sus vocales (la "a" abre más, la "o" y la "u" redondean, la "e" y la "i" estiran). Si tu voz no avisa de cada palabra, usa un ritmo silábico aproximado.
- **Emociones.** Claude etiqueta cada respuesta (alegre, divertida, pensativa, sorprendida, preocupada o neutral) y el avatar cambia de expresión (sonrisa, cejas, inclinación de cabeza, risa) y de color del aro.
- **Gestos.** Parpadea, asiente al terminar una frase, levanta las cejas al preguntar, mira hacia arriba mientras piensa y asiente de vez en cuando mientras te escucha.

### Foto real

- Guarda una foto como `jarvis-avatar.jpg` dentro de la carpeta y aparecerá sola, o
- pulsa **Cambiar foto** y elige una imagen (se recorta en círculo y se guarda en el navegador).
- Pulsa **Ajustar boca** y haz clic en el centro de su boca para que la mandíbula se mueva en el sitio correcto.

Con foto, el avatar abre la boca, mueve la cabeza y cambia el color del aro, pero no cambia la sonrisa ni las cejas: eso solo lo hace el retrato ilustrado. Funciona mejor con una foto de frente, con la boca cerrada y la cara centrada.

## Voz de ElevenLabs

Con la clave y el ID de voz de ElevenLabs, cada frase se pide a ElevenLabs (modelo `eleven_flash_v2_5`, en español) junto con el momento exacto de cada letra. Mientras suena, la boca del avatar se mueve con esos tiempos y con el volumen real del audio, así que el lip sync es mucho más preciso que con la voz del navegador. La siguiente frase se pide mientras suena la anterior para que no haya pausas. Si ElevenLabs falla (clave incorrecta, voz no encontrada, sin saldo), lo avisa y usa la voz del navegador. Las claves se cambian o se quitan en **Ajustes y claves**.

## Vídeo realista con Simli (opcional)

Simli anima en tiempo real la cara de una foto a partir del audio, con lip sync de verdad. Necesita la voz de ElevenLabs.

1. En [app.simli.com](https://app.simli.com) crea una cara a partir de tu foto y copia su **Face ID**. Copia también tu **clave de API**.
2. En **Ajustes y claves**, pega la clave de Simli y el Face ID y guarda.
3. Pulsa **Activar vídeo realista**. El círculo del avatar pasa a mostrar el vídeo de Simli.

Mientras está conectado, cada frase de ElevenLabs (audio PCM de 16 kHz) se envía a Simli, que devuelve el vídeo y el audio ya sincronizados. Pulsa el mismo botón para desconectar: Simli cobra por minuto conectado. Si pasan 5 minutos sin hablar, Simli cierra la sesión y vuelve el avatar local.

## Detalles

- Cerebro por defecto: Ollama con `llama3.2:3b` (constantes `OLLAMA_DEFAULT_MODEL` y `OLLAMA_DEFAULT_URL` en `index.html`), gratis.
- Cerebro opcional de pago: Claude `claude-sonnet-5` (constante `MODEL`). Su uso se factura en tu cuenta de la API de Anthropic, aparte de la suscripción de Claude. ElevenLabs y Simli también son de pago.
- Mientras Jarvis habla, el micrófono se pausa para que no se oiga a sí misma.
- La voz depende de las voces en español instaladas en tu sistema; elige otra en la lista si la que sale no te convence.
- La conversación no se guarda al recargar la página.
- `anthropic-sdk.js` es el SDK oficial `@anthropic-ai/sdk` 0.128.0 empaquetado para navegador.
- `iniciar-jarvis.ps1` es el servidor local y lanzador de Windows (PowerShell, sin instalar nada). Los datos de la aplicación quedan en `%LOCALAPPDATA%\JarvisTomas`; en macOS y Linux, en `~/.jarvis-tomas`.
- `simli-sdk.js` es el cliente oficial `simli-client` 3.0.2 (con `livekit-client`) empaquetado para navegador.
