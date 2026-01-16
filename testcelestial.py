#import pyautogui
#import keyboard
#while True:
#    cmd = input(">> ")
#
#    if cmd == "alt tab":
#        pyautogui.keyDown("alt")
#        pyautogui.press("tab")
#        pyautogui.keyUp("alt")
#
#    elif cmd == "open notepad":
#        pyautogui.hotkey("win", "r")
#        pyautogui.write("notepad")
#        pyautogui.press("enter")
#
#from mediapipe import tasks
#print(tasks)

import threading
import queue
from voice_listener import VoiceListener
from command_parser import parse_command
from action_engine import execute_action
from keyword_actions import handle_keyword_action

WAKE_WORDS = ["laptop", "hey laptop", "ok laptop"]
voice_queue = queue.Queue()


def normalize_command(text: str) -> str:
    """Normalize user input"""
    return text.lower().strip()


def strip_wake_word(command: str) -> str:
    """Remove wake word if present"""
    for wake in WAKE_WORDS:
        if command.startswith(wake):
            return command[len(wake):].strip()
    return command


def has_wake_word(command: str) -> bool:
    """Check wake word presence"""
    return any(command.startswith(wake) for wake in WAKE_WORDS)


def background_voice_listener(voice):
    """Run in background thread to listen for voice commands in parallel"""
    while True:
        try:
            print("\n🎙 Listening in background... (no wake word needed)")
            spoken = voice.listen(timeout=10)
            
            if spoken:
                spoken = normalize_command(spoken)
                print("\n🗣 You said:", spoken)
                
                # In voice mode, accept commands without wake word
                voice_queue.put(spoken)
        except Exception as e:
            print("🎙 Background listening error:", e)


def main():
    print("🌌 Celestial_AI initialized")
    print("📝 Type commands in TEXT MODE")

    # -----------------------------
    # Initialize voice system
    # -----------------------------
    try:
        voice = VoiceListener()
        print("🎙 Voice system ready (offline)")
    except Exception as e:
        print("❌ Voice system failed:", e)
        voice = None

    # Start background voice listener if available
    if voice:
        voice_thread = threading.Thread(target=background_voice_listener, args=(voice,), daemon=True)
        voice_thread.start()
        print("🎙 Background mic listening started (parallel mode)")

    # Current mode indicator
    current_mode = "TEXT"

    # Mode info
    mode_options = "📍 Available modes: TEXT | VOICE | CAMERA"
    print(f"\n{mode_options}")
    print(f"💡 Commands: 'switch to voice' | 'switch to camera' | 'switch to text'")

    # -----------------------------
    # Main Loop
    # -----------------------------
    while True:
        # Check for voice commands from background thread
        try:
            voice_command = voice_queue.get_nowait()
            print(f"\n📍 MODE: {current_mode}")
            command = voice_command
            print("✅ Processing voice command:", command)
        except queue.Empty:
            # No voice command, get keyboard input
            print(f"\n📍 MODE: {current_mode}")
            command = input("> ").strip()

            if not command:
                continue

            command = normalize_command(command)

        # Exit
        if command in ("exit", "quit", "bye"):
            print("👋 Celestial_AI shutting down")
            break

        # Mode switching
        if "switch to voice" in command:
            current_mode = "VOICE"
            print(f"🎙 Switched to VOICE mode")
            continue

        if "switch to camera" in command:
            current_mode = "CAMERA"
            print(f"📷 Switched to CAMERA mode")
            continue

        if "switch to text" in command:
            current_mode = "TEXT"
            print(f"⌨️ Switched to TEXT mode")
            continue

        if "show modes" in command or "modes" in command:
            print(f"\n{mode_options}")
            print(f"💡 Commands: 'switch to voice' | 'switch to camera' | 'switch to text'")
            continue

        # Keyword Actions (HIGH PRIORITY)
        keyword_result = handle_keyword_action(command)
        if keyword_result.get("handled"):
            print("🤖 Celestial_AI:", keyword_result["response"])
            continue

        # Parse Command
        action = parse_command(command)
        if not action:
            print("❓ I didn't understand that")
            continue

        # Execute Action
        try:
            execute_action(action)
        except Exception as e:
            print("⚠ Action failed:", e)


# -----------------------------
# Entry Point
# -----------------------------
if __name__ == "__main__":
    main()
