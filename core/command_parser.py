def parse_command(command: str) -> dict:
    command = command.lower().strip()

    # -------- SYSTEM --------
    if command in ["exit", "quit", "shutdown"]:
        return {"action": "exit"}

    # -------- MODE CONTROL --------
    if "set mode" in command:
        mode = command.replace("set mode", "").strip()
        return {"action": "set_mode", "mode": mode}

    # -------- CAMERA CONTROL (DAY 2) --------
    if "switch to camera" in command or "camera on" in command:
        return {"action": "camera_on"}

    if "exit camera" in command or "camera off" in command:
        return {"action": "camera_off"}

    # -------- APP CONTROL (DAY 1) --------
    if command.startswith("open "):
        app_name = command.replace("open", "").strip()
        return {"action": "open_app", "app": app_name}

    # -------- FALLBACK --------
    return {"action": "unknown"}
