from command_parser import parse_command
from action_engine import execute_action
from mode_manager import set_mode, get_mode
import keyboard
import sys


def emergency_exit():
    print("\n🚨 EMERGENCY EXIT ACTIVATED")
    sys.exit(0)


# Global hotkey for emergency shutdown
keyboard.add_hotkey("ctrl+shift+q", emergency_exit)

print("🌌 Celestial_Ai Started")
print("Emergency Exit: CTRL + SHIFT + Q")

while True:
    try:
        command = input(f"[{get_mode()}] >> ").strip()

        if not command:
            continue

        action = parse_command(command)

        if action["action"] == "set_mode":
            response = set_mode(action["mode"])

        elif action["action"] == "exit":
            print("👋 Shutting down Celestial_Ai")
            break

        else:
            response = execute_action(action)

        print("Celestial_Ai:", response)

    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
        break
