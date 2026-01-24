import re
from custom_command_engine import load_custom_commands

# ---------------- CONFIG ----------------

KNOWN_APPS = {
    "calculator": "calc",
    "notepad": "notepad",
    "chrome": "chrome",
    "firefox": "firefox",
    "edge": "msedge",
    "paint": "mspaint"
}

WAKE_WORDS = ["celestial", "hey celestial", "ok celestial"]

# ---------------- LEARNING ----------------

def parse_learning_sequence(sequence):
    actions = []

    for cmd in sequence:
        cmd = cmd.lower().strip()

        if cmd.startswith("open"):
            app = cmd.replace("open", "").strip()
            actions.append({
                "action": "open_app",
                "app": app
            })

        elif cmd.startswith("close"):
            app = cmd.replace("close", "").strip()
            actions.append({
                "action": "close_app",
                "app": app
            })

    return actions


# ---------------- HELPERS ----------------

def remove_wake_word(text: str) -> str:
    text = text.lower().strip()
    for w in WAKE_WORDS:
        if text.startswith(w):
            return text[len(w):].strip()
    return text


# ---------------- MAIN PARSER ----------------

def parse_command(text: str) -> dict:
    if not text or not isinstance(text, str):
        return {"action": "none"}

    text = text.lower().strip()
    text = remove_wake_word(text)

    # -------- LEARN COMMAND --------
    if text in ["learn command", "teach command"]:
        return {"action": "learn_command"}

    # -------- DELETE LEARNED COMMAND --------
    if text.startswith("delete learned command"):
        name = text.replace("delete learned command", "").strip()
        if name.startswith("called"):
            name = name.replace("called", "").strip()

        return {
            "action": "delete_custom_command",
            "name": name
        }

    # -------- EXIT --------
    if text in ["exit", "quit", "shutdown", "stop"]:
        return {"action": "exit"}

    # -------- CUSTOM COMMANDS --------
    custom_commands = load_custom_commands()
    if text in custom_commands:
        return {
            "action": "custom_command",
            "name": text
        }

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
    if text == "start camera":
        return {"action": "start_camera"}

    if text == "stop camera":
        return {"action": "stop_camera"}

    # -------- MOUSE CONTROL --------
    if text in ["mouse control on", "enable mouse control", "start mouse control"]:
        return {"action": "mouse_on"}

    if text in ["mouse control off", "disable mouse control", "stop mouse control"]:
        return {"action": "mouse_off"}

    # -------- MODE --------
    if text == "text mode":
        return {"action": "set_mode", "mode": "text"}

    if text == "voice mode":
        return {"action": "set_mode", "mode": "voice"}

    return {"action": "unknown", "raw": text}
