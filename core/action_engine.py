import pyautogui
import time

def execute_action(action):
    if action["action"] == "open_app":
        app = action["app"]

        # Open Start Menu
        pyautogui.press("win")
        time.sleep(0.5)

        # Type app name
        pyautogui.write(app, interval=0.05)
        time.sleep(0.5)

        # Press Enter
        pyautogui.press("enter")

        return f"Opening {app}"

    elif action["action"] == "alt_tab":
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        pyautogui.keyUp("alt")
        return "Switched window"

    else:
        return "Unknown action"
