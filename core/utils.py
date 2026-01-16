WAKE_WORD = "celestial"

def normalize_command(text: str):
    if not text:
        return None

    text = text.lower().strip()

    if text.startswith(WAKE_WORD):
        return text.replace(WAKE_WORD, "", 1).strip()

    return text
