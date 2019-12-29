from app import messages_en, messages_pl
from app.messages_enums import Message


def send(message: Message, lang: str):
    if lang == "pl":
        text = messages_pl.messages[message.name]
    else:
        # fallback to English
        text = messages_en.messages[message.name]

    return {"message": text}
