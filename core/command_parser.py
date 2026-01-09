def parse_command(command):
    command = command.lower()

    if "camera on" in command:
        return {"action": "camera_on"}

    if "camera off" in command:
        return {"action": "camera_off"}

    if command.startswith("mode"):
        _, mode = command.split(maxsplit=1)
        return {"action": "set_mode", "mode": mode}

    return {"action": "execute", "command": command}
