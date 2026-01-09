from command_parser import parse_command
from action_engine import execute_action
from mode_manager import set_mode, get_mode
import keyboard
import sys

def emergency_exit():
    print("\nEMERGENCY EXIT")
    sys.exit(0)

keyboard.add_hotkey("ctrl+shift+q", emergency_exit)

print("Celestial_Ai Online")
print("CTRL + SHIFT + Q → Emergency Exit")

while True:
    command = input(f"[{get_mode()}] >> ")

    action = parse_command(command)

    if action["action"] == "set_mode":
        response = set_mode(action["mode"])
    else:
        response = execute_action(action)

    print("Celestial_Ai:", response)
