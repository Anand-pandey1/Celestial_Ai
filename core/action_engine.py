import os
import subprocess
import pyautogui
import time
from camera import start_camera, stop_camera
from state import state

def open_app(app_name):
    # Level 1: Native Windows shell
    try:
        os.startfile(app_name)
        return f"Opened {app_name} (native)"
    except:
        pass

    # Level 2: PATH executable
    try:
        subprocess.Popen(app_name)
        return f"Opened {app_name} (PATH)"
    except:
        pass

    # Level 3: UI automation fallback
    try:
        pyautogui.press("win")
        time.sleep(0.6)
        pyautogui.write(app_name, interval=0.05)
        time.sleep(0.6)
        pyautogui.press("enter")
        return f"Opened {app_name} (UI automation)"
    except:
        return f"Failed to open {app_name}"


def execute_action(action):
    if action["action"] == "camera_on":
        return start_camera()

    if action["action"] == "camera_off":
        return stop_camera()

    if action["action"] == "mouse_on":
        state["mouse_control"] = True
        return "Mouse control enabled"

    if action["action"] == "mouse_off":
        state["mouse_control"] = False
        return "Mouse control disabled"
    
    if action["action"] == "open_app":
        return open_app(action["app"])


    return "Command executed"

