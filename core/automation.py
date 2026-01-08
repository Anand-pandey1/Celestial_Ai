import pyautogui
import time

pyautogui.FAILSAFE = True


def open_app_via_search(app_name: str) -> bool:
    """
    Opens app using Windows Search (Win key)
    """
    try:
        pyautogui.press("win")
        time.sleep(0.5)

        pyautogui.write(app_name, interval=0.05)
        time.sleep(0.5)

        pyautogui.press("enter")
        return True
    except Exception:
        return False
