from typing import Dict

from app import messages_en, messages_pl
from app.messages_enums import Message


class Lang:
    """Represents a language and provides functionality to map messages to different (supported) languages."""

    def __init__(self, lang):
        """
        :param lang: two-character country code.
        """
        self.lang = lang

    def map(self, message: Message) -> Dict[str, str]:
        """
        Internationalization method, used to map responses to different languages.

        :param message: Message enum
        :return: dictionary containing key "message" which maps to **message** in language **self.lang**.

        """

        if self.lang == "pl":
            text = messages_pl.messages[message.name]
        else:
            # fallback to English
            text = messages_en.messages[message.name]

        return {"message": text}
