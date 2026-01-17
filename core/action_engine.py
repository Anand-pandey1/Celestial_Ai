import os
import time
import subprocess
import pyautogui
import pygetwindow as gw
import psutil

# Map spoken names → window keywords / exe hints
APP_ALIASES = {
    "calculator": ["calculator", "calc"],
    "notepad": ["notepad"],
    "chrome": ["chrome"],
    "edge": ["edge"],
    "paint": ["paint"]
}


def open_app(app):
    try:
        subprocess.Popen(app)
        return f"{app} opened"

    except Exception:
        pyautogui.press("win")
        time.sleep(0.5)
        pyautogui.write(app)
        time.sleep(0.5)
        pyautogui.press("enter")
        return f"{app} opened via UI"


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

    return "Unknown action"
