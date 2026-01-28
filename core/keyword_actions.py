import os
import sys

# Add parent directory to path for UI imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from UI.floating_panel import update_status

def handle_keyword_action(command: str):
    command = command.lower()

    # 🔹 Custom hard actions
    if "self destruct" in command:
        return {
            "handled": True,
            "response": "😅 Nice try. Self destruct disabled."
        }

    if "who are you" in command:
        update_status("🤖 Celestial AI online")
        return {
            "handled": True,
            "response": "I am Celestial_AI, your personal offline assistant."
        }

    if "focus mode" in command:
        update_status("🧠 Focus Mode ON")
        return {
            "handled": True,
            "response": "🧠 Focus mode enabled. Notifications muted."
        }

    # 🔹 Not handled → pass to normal system
    return {
        "handled": False
    }
