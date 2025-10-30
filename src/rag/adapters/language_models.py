from ..core import ports


class Parrot(ports.LanguageModel):
    def answer(self, message: str, context: None | list[str] = None):
        # context = "\n".join(context) if context else ""
        return f"{message}"
