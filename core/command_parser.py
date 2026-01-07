def parse_command(text):
    text = text.lower().strip()

    # MODE SWITCHING
    if "camera mode" in text:
        return {"action": "set_mode", "mode": "CAMERA"}

    if "normal mode" in text:
        return {"action": "set_mode", "mode": "NORMAL"}

    # OPEN ANY APP
    if text.startswith("open "):
        app_name = text.replace("open ", "").strip()
        return {"action": "open_app", "app": app_name}

    # ALT TAB
    if "alt tab" in text or "switch window" in text:
        return {"action": "alt_tab"}

    return {"action": "unknown", "raw": text}
