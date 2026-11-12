import anthropic

client = anthropic.Anthropic()  # lee la key de la variable de entorno automáticamente

message = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Preséntate como si fueras Jarvis, el asistente de Tony Stark, en una frase."}
    ]
)

if message.stop_reason == "refusal":
    print("El modelo rechazó la petición.")
else:
    # Con pensamiento adaptativo activo por defecto, el primer bloque puede ser
    # de tipo "thinking"; nos quedamos solo con los bloques de texto.
    print("".join(block.text for block in message.content if block.type == "text"))
