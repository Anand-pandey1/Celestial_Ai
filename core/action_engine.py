import os
import subprocess
from camera import start_camera, stop_camera
from automation import open_app_via_search


def open_app_windows(app_name: str) -> bool:
    # 1️⃣ Native Windows shell
    try:
        os.startfile(app_name)
        return True
    except:
        pass

    # 2️⃣ PATH executable
    try:
        subprocess.Popen(app_name)
        return True
    except:
        pass

    # 3️⃣ UI automation fallback
    return open_app_via_search(app_name)


def execute_action(action: dict):
    action_type = action.get("action")

    if action_type == "open_app":
        app = action.get("app")

        if open_app_windows(app):
            return f"Opening {app}"
        else:
            return f"Failed to open {app}"

    elif action_type == "camera_on":
        start_camera()
        return "Camera activated"

    elif action_type == "camera_off":
        stop_camera()
        return "Camera stopped"

    elif action_type == "unknown":
        return "I didn't understand that command"

    return "Action not supported yet"
