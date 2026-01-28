import sys
import os
import threading
import keyboard

# Add parent directory to path for imports FIRST
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from camera import start_camera, stop_camera

from command_parser import parse_command
from action_engine import execute_action
from mode_manager import get_mode, set_mode
from voice_listener import VoiceListener
from custom_command_engine import run_custom_command
from custom_command_engine import save_custom_command
from learned_commands import add_or_update_command, get_command
from command_parser import parse_learning_sequence
from executor import execute_actions

from custom_command_engine import delete_custom_command


import threading
from UI.floating_panel import start_ui, update_status, toggle_ui, register_callbacks


import keyboard
keyboard.add_hotkey("ctrl+shift+u", toggle_ui)

from UI.tray_app import run_tray
from command_parser import parse_command
from action_engine import execute_action



RUNNING = True

def ui_command_handler(text):
    try:
        print(f"[UI Command] {text}")
        update_status("Processing...")
        action = parse_command(text)
        handle_action(action)
    except Exception as e:
        print(f"UI Command error: {e}")
        update_status("Error processing command")



def ui_voice_toggle(enabled):
    global VOICE_ENABLED
    VOICE_ENABLED = enabled
    update_status("Listening" if enabled else "Voice Paused")

def ui_camera_toggle(enabled):
    if enabled:
        start_camera()
        update_status("Camera ON")
    else:
        stop_camera()
        update_status("Listening")



def learn_command_interactive():
    print("\n🧠 Learning mode activated")
    update_status("🧠 Learning mode active")

    trigger = input("Trigger phrase: ").strip().lower()
    if not trigger:
        print("❌ Invalid trigger")
        update_status("Listening")
        return

    print("Enter actions (one per line). Type 'done' when finished:")

    actions = []
    while True:
        cmd = input(">> ").strip().lower()
        if cmd == "done":
            break

        action = parse_command(cmd)
        if action.get("action") in ["open_app", "close_app"]:
            actions.append(action)
        else:
            print("⚠️ Unsupported action, skipped")

    if not actions:
        print("❌ No actions learned")
        update_status("Listening")
        return

    save_custom_command(trigger, actions)
    print(f"✅ Learned new command: '{trigger}'")
    update_status(f"✓ Learned: {trigger}")


def learn_command(command_name, spoken_steps):
    actions = parse_learning_sequence(spoken_steps)
    add_or_update_command(command_name, actions)
    print(f"Updated command: {command_name}")

def run_learned_command(command_name):
    actions = get_command(command_name)
    if actions:
        execute_actions(actions)
    else:
        print("Command not found")



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
        update_status("Listening")
        return

    act = action["action"]

    if act == "exit":
        emergency_exit()

    elif act == "set_mode":
        mode_result = set_mode(action["mode"])
        print(mode_result)
        update_status(f"Mode: {action['mode'].upper()}")

    elif act == "custom_command":
        update_status(f"Executing: {action['name']}")
        result = run_custom_command(action["name"])
        if result == "exit":
            emergency_exit()
        elif result:
            print(result)
        update_status("Listening")
    
    elif act == "learn_command":
        # Run in separate thread to avoid blocking UI
        threading.Thread(target=learn_command_interactive, daemon=True).start()

    elif act == "delete_custom_command":
        success = delete_custom_command(action["name"])
        if success:
            print(f"🗑 Deleted learned command: {action['name']}")
            update_status(f"✓ Deleted: {action['name']}")
        else:
            print(f"⚠ Command '{action['name']}' not found")
        update_status("Listening")

    else:
        result = execute_action(action)
        if result:
            print(result)
        update_status("Listening")


# ----------------- MAIN -----------------
def main():
    print("🚀 Celestial_AI Started ")
    print("Mode:", get_mode())
    print("Emergency Exit: CTRL + SHIFT + Q")

    # Start voice listener thread
    threading.Thread(target=voice_loop, daemon=True).start()
    
    # Start UI with callbacks
    print("Starting UI...")
    ui_thread = threading.Thread(
        target=start_ui,
        args=(ui_voice_toggle, ui_camera_toggle, ui_command_handler),
        daemon=True
    )
    ui_thread.start()
    
    # Give UI time to initialize
    import time
    time.sleep(0.5)

    update_status("Listening")
    print("UI started successfully")

    tray_thread = threading.Thread(
        target=run_tray,
        args=(lambda: os._exit(0),),
        daemon=True
    )
    tray_thread.start()


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
