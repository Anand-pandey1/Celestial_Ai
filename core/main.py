from command_parser import parse_command
from action_engine import execute_action
from mode_manager import set_mode, get_mode
from voice_listener import VoiceListener
import keyboard
import sys
import threading

RUNNING = True


def emergency_exit():
    global RUNNING
    print("\n🛑 Celestial_AI shutting down...")
    RUNNING = False
    sys.exit(0)

# Hotkey exit
keyboard.add_hotkey("ctrl+shift+q", emergency_exit)

voice = VoiceListener()


def voice_loop():
    global RUNNING
    while RUNNING:
        text = voice.listen_continuous()
        if not text:
            continue

        print(f"[VOICE] {text}")
        action = parse_command(text)

        if action["action"] == "exit":
            emergency_exit()
        elif action["action"] == "set_mode":
            print(set_mode(action["mode"]))
        else:
            print(execute_action(action))


# Start voice thread
threading.Thread(target=voice_loop, daemon=True).start()

print("🚀 Celestial_AI Started")
print("Emergency Exit: CTRL + SHIFT + Q")

while RUNNING:
    try:
        command = input(f"[{get_mode()}] >> ")
        action = parse_command(command)

        if action["action"] == "exit":
            emergency_exit()
        elif action["action"] == "set_mode":
            print(set_mode(action["mode"]))
        else:
            print(execute_action(action))

    except KeyboardInterrupt:
        emergency_exit()
