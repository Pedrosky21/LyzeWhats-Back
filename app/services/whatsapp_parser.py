import re
from datetime import datetime
from app.models.chat_models import Message
from app.utils.emoji_utils import extract_emojis, split_emojis

LINE_PATTERN = re.compile(
    r"^(\d{1,2}/\d{1,2}/\d{4}), (\d{2}:\d{2}) - (.*?): (.*)$"
)

def parse_whatsapp_chat(text: str):
    messages = []

    # limpiar cosas entre <>
    text = re.sub(r"<[^>]*>", "", text)

    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue

        match = LINE_PATTERN.match(line)
        if not match:
            continue

        date_str, time_str, sender, message = match.groups()

        timestamp = datetime.strptime(
            f"{date_str} {time_str}", "%d/%m/%Y %H:%M"
        )

        # extraer y separar emojis individuales
        emojis_raw = extract_emojis(message)
        emojis = [em for e in emojis_raw for em in split_emojis(e)]

        messages.append(Message(
            timestamp=timestamp,
            sender=sender,
            text=message,
            emojis=emojis
        ))

    return messages
