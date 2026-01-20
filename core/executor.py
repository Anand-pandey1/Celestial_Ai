import subprocess
import time

APP_COMMANDS = {
    "firefox": "firefox",
    "notepad": "notepad",
    "calculator": "calc"
}

def open_app(app):
    cmd = APP_COMMANDS.get(app.lower())
    if cmd:
        subprocess.Popen(cmd, shell=True)
        time.sleep(0.8)  # small delay, NOT blocking

def execute_actions(actions):
    for action in actions:
        if action["type"] == "open":
            open_app(action["target"])
