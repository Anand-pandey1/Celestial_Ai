import sys
import keyboard

from command_parser import parse_command
from action_engine import execute_action
from mode_manager import set_mode, get_mode
from voice_listener import VoiceListener


# -------------------------
# Emergency Exit
# -------------------------
def emergency_exit():
    print("\n🚨 EMERGENCY EXIT ACTIVATED")
    sys.exit(0)


keyboard.add_hotkey("ctrl+shift+q", emergency_exit)


# -------------------------
# Initialize Voice System
# -------------------------
try:
    voice = VoiceListener()
except Exception as e:
    print("❌ Voice system failed to initialize:")
    print(e)
    voice = None


# -------------------------
# Startup Banner
# -------------------------
print("=" * 45)
print("✨ Celestial_AI Started")
print("🧠 Current Mode:", get_mode())
print("🎤 Voice Command: voice mode")
print("🚨 Emergency Exit: CTRL + SHIFT + Q")
print("=" * 45)


# -------------------------
# Main Loop
# -------------------------
while True:
    try:
        command = input(f"[{get_mode()}] >> ").strip()

        if not command:
            continue

        # -------------------------
        # Voice Mode Trigger
        # -------------------------
        if command.lower() == "voice mode":
            if not voice:
                print("Celestial_AI: ❌ Voice system unavailable")
                continue

            spoken = voice.listen()

            if not spoken:
                print("Celestial_AI: 🎤 No speech detected")
                continue

            print("🗣️ You said:", spoken)
            command = spoken

        # -------------------------
        # Parse Command
        # -------------------------
        action = parse_command(command)

        if not action:
            print("Celestial_AI: ❓ I didn't understand that")
            continue

        # -------------------------
        # Mode Switch
        # -------------------------
        if action.get("action") == "set_mode":
            response = set_mode(action.get("mode"))

        # -------------------------
        # Execute Action
        # -------------------------
        else:
            response = execute_action(action)

        print("Celestial_AI:", response)

    except KeyboardInterrupt:
        print("\n👋 Shutting down Celestial_AI")
        sys.exit(0)

    except Exception as e:
        print("❌ Runtime Error:", e)
