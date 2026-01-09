def parse_command(command):
    command = command.lower()

    if "camera on" in command:
        return {"action": "camera_on"}

    if "camera off" in command:
        return {"action": "camera_off"}

    if command.startswith("mode"):
        _, mode = command.split(maxsplit=1)
        return {"action": "set_mode", "mode": mode}
    
    if "mouse control on" in command:
        return {"action": "mouse_on"}

    if "mouse control off" in command:
        return {"action": "mouse_off"}

    if command.startswith("open "):
        app_name = command.replace("open ", "").strip()
        return {
            "action": "open_app",
            "app": app_name
        }
    return {"action": "execute", "command": command}
