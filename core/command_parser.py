import re

# Known apps (you can extend this safely)
KNOWN_APPS = {
    "calculator": "calc",
    "notepad": "notepad",
    "chrome": "chrome",
    "edge": "msedge",
    "paint": "mspaint"
}

WAKE_WORDS = ["celestial", "hey celestial", "ok celestial"]


def remove_wake_word(text: str) -> str:
    text = text.lower().strip()
    for w in WAKE_WORDS:
        if text.startswith(w):
            return text[len(w):].strip()
    return text


def parse_command(text: str) -> dict:
    if not text or not isinstance(text, str):
        return {"action": "none"}

    text = text.lower().strip()
    text = remove_wake_word(text)

    # -------- EXIT --------
    if text in ["exit", "quit", "shutdown", "stop"]:
        return {"action": "exit"}

    # -------- OPEN APP --------
    match = re.match(r"open (.+)", text)
    if match:
        app_name = match.group(1).strip()
        app = KNOWN_APPS.get(app_name, app_name)
        return {
            "action": "open_app",
            "app": app
        }

    # -------- CLOSE APP --------
    match = re.match(r"close (.+)", text)
    if match:
        app_name = match.group(1).strip()
        app = KNOWN_APPS.get(app_name, app_name)
        return {
            "action": "close_app",
            "app": app
        }

    # -------- CAMERA --------
    if "start camera" in text:
        return {"action": "start_camera"}

    if "stop camera" in text:
        return {"action": "stop_camera"}

    # -------- MODE --------
    if "text mode" in text:
        return {"action": "set_mode", "mode": "text"}

    if "voice mode" in text:
        return {"action": "set_mode", "mode": "voice"}

    return {"action": "unknown", "raw": text}
