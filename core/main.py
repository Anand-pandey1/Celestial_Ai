import sys
import threading
import keyboard

from command_parser import parse_command
from action_engine import execute_action
from mode_manager import get_mode, set_mode
from voice_listener import VoiceListener
from custom_command_engine import run_custom_command

RUNNING = True


# ----------------- EXIT HANDLER -----------------
def emergency_exit():
    global RUNNING
    if not RUNNING:
        return
    RUNNING = False
    print("\n🛑 Celestial_AI shutting down safely...")
    sys.exit(0)


# Global hotkey (always works)
keyboard.add_hotkey("ctrl+shift+q", emergency_exit)


# ----------------- VOICE LOOP -----------------
voice = VoiceListener()


def voice_loop():
    global RUNNING
    while RUNNING:
        try:
            text = voice.listen_continuous()
            if not text:
                continue

            print(f"\n🎤 [VOICE] {text}")
            action = parse_command(text)
            handle_action(action)

        except Exception as e:
            print("Voice error:", e)


# ----------------- ACTION HANDLER -----------------
def handle_action(action: dict):
    if not action or "action" not in action:
        return

    act = action["action"]

    if act == "exit":
        emergency_exit()

    elif act == "set_mode":
        print(set_mode(action["mode"]))

    elif act == "custom_command":
        result = run_custom_command(action["name"])
        if result == "exit":
            emergency_exit()
        elif result:
            print(result)

    else:
        result = execute_action(action)
        if result:
            print(result)


# ----------------- MAIN -----------------
def main():
    print("🚀 Celestial_AI Started ")
    print("Mode:", get_mode())
    print("Emergency Exit: CTRL + SHIFT + Q")

    # Start voice listener thread
    threading.Thread(target=voice_loop, daemon=True).start()

    # Text loop
    global RUNNING
    while RUNNING:
        try:
            command = input(f"\n[{get_mode().upper()}] >> ").strip()
            if not command:
                continue

            action = parse_command(command)
            handle_action(action)

        except KeyboardInterrupt:
            emergency_exit()
        except Exception as e:
            print("Main loop error:", e)


if __name__ == "__main__":
    main()
