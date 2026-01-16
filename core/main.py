import threading
from voice_listener import VoiceListener
from command_parser import parse_command
from action_engine import execute_action
from keyword_actions import handle_keyword_action
from context_manager import ContextManager


WAKE_WORDS = ["celestial", "hey celestial", "ok celestial"]


def has_wake_word(text):
    return any(text.startswith(w) for w in WAKE_WORDS)


def strip_wake_word(text):
    for w in WAKE_WORDS:
        if text.startswith(w):
            return text[len(w):].strip()
    return text


def voice_loop(voice, context):
    print("🎙 Continuous voice listening ON")

    while True:
        spoken = voice.listen_continuous()
        spoken = spoken.lower()

        if not has_wake_word(spoken):
            continue

        command = strip_wake_word(spoken)
        print("🗣", command)

        command = context.resolve_pronoun(command)

        keyword = handle_keyword_action(command)
        if keyword.get("handled"):
            print("🤖", keyword["response"])
            continue

        action = parse_command(command)
        if not action:
            print("❓ Unknown command")
            continue

        execute_action(action)
        context.update(action)


def main():
    print("🌌 Celestial_AI Online")

    context = ContextManager()
    voice = VoiceListener()

    # Start voice thread
    threading.Thread(
        target=voice_loop,
        args=(voice, context),
        daemon=True
    ).start()

    # Text mode still works
    while True:
        cmd = input("> ").lower().strip()

        if cmd in ("exit", "quit"):
            print("👋 Shutting down")
            break

        cmd = context.resolve_pronoun(cmd)

        action = parse_command(cmd)
        if action:
            execute_action(action)
            context.update(action)
        else:
            print("❓ Unknown command")


if __name__ == "__main__":
    main()
