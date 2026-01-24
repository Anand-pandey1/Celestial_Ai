import os
import time
import subprocess
import pyautogui
import pygetwindow as gw
import psutil
import shutil
from camera import start_camera, stop_camera
from state import state

# Map spoken names → window keywords / exe hints
APP_ALIASES = {
    "calculator": ["calculator", "calc"],
    "notepad": ["notepad"],
    "chrome": ["chrome"],
    "edge": ["edge"],
    "paint": ["paint"]
}

WINDOWS_APP_MAP = {
    "calculator": "calc",
    "calc": "calc",
    "camera": "start microsoft.windows.camera:",
    "clock": "start ms-clock:",
    "photos": "start ms-photos:",
    "settings": "start ms-settings:",
    "store": "start ms-windows-store:",
    "edge": "msedge",
    "explorer": "explorer",
    "task manager": "taskmgr",
}

def open_app(app):
    app = app.lower().strip()

    # ---------- METHOD 1: Windows URI ----------
    if app in WINDOWS_APP_MAP:
        subprocess.Popen(
            WINDOWS_APP_MAP[app],
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.8)
        return f"{app} opened (windows)"

    # ---------- METHOD 2: SYSTEM ONLY IF EXECUTABLE EXISTS ----------
    exe_path = shutil.which(app)
    if exe_path:
        subprocess.Popen(
            exe_path,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.6)
        return f"{app} opened (system)"

    # ---------- METHOD 3: UI FALLBACK (FOR UNKNOWN APPS) ----------
    try:
        # Ensure focus
        pyautogui.click(10, 10)
        time.sleep(0.3)

        # Open Start
        pyautogui.press("win")
        time.sleep(0.8)

        # Type app name
        pyautogui.write(app, interval=0.05)
        time.sleep(0.5)

        # Launch
        pyautogui.press("enter")
        time.sleep(1.3)

        return f"{app} opened (ui)"

    except Exception as e:
        return f"Failed to open {app}: {e}"


def close_app(app):
    keywords = APP_ALIASES.get(app, [app])

    # ---------- METHOD 1: Close by window ----------
    for win in gw.getAllWindows():
        title = win.title.lower()
        if any(k in title for k in keywords):
            try:
                win.activate()
                time.sleep(0.3)
                win.close()
                return f"{app} closed (window)"
            except Exception:
                pass

    # ---------- METHOD 2: Kill process ----------
    for proc in psutil.process_iter(["name"]):
        try:
            pname = proc.info["name"].lower()
            if any(k in pname for k in keywords):
                proc.terminate()
                return f"{app} closed (process)"
        except Exception:
            pass

    # ---------- METHOD 3: ALT+F4 fallback ----------
    try:
        pyautogui.hotkey("alt", "f4")
        return f"{app} closed (ui fallback)"
    except Exception:
        return f"Could not close {app}"


def execute_action(action):
    act = action.get("action")

    if act == "open_app":
        return open_app(action["app"])

    if act == "close_app":
        return close_app(action["app"])

    if act == "start_camera":
        return start_camera()

    if act == "stop_camera":
        return stop_camera()

    if act == "mouse_on":
        state["mouse_control"] = True
        return "Mouse control enabled"

    if act == "mouse_off":
        state["mouse_control"] = False
        return "Mouse control disabled"
    
    return "Unknown action"
