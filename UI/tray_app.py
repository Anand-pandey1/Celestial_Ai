# UI/tray_app.py
import threading
from PIL import Image
import pystray
import os

from UI.floating_panel import toggle_ui

def run_tray(on_exit_callback=None):
    icon_path = os.path.join(
        os.path.dirname(__file__),
        "..", "assets", "icon.png"
    )

    image = Image.open(icon_path)

    def on_show_hide(icon, item):
        toggle_ui()

    def on_exit(icon, item):
        icon.stop()
        if on_exit_callback:
            on_exit_callback()

    menu = pystray.Menu(
        pystray.MenuItem("Show / Hide", on_show_hide),
        pystray.MenuItem("Exit", on_exit)
    )

    icon = pystray.Icon("CelestialAI", image, "Celestial AI", menu)
    icon.run()
