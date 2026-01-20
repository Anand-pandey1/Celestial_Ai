import json
import os
from action_engine import execute_action

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMMANDS_FILE = os.path.join(BASE_DIR, "data", "custom_commands.json")


def load_custom_commands():
    if not os.path.exists(COMMANDS_FILE):
        print("⚠️ custom_commands.json not found")
        return {}

    with open(COMMANDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def run_custom_command(command_name):
    commands = load_custom_commands()
    command = commands.get(command_name)

    if not command:
        return None

    if command["type"] == "sequence":
        results = []
        for action in command["actions"]:
            results.append(execute_action(action))
        return " | ".join(results)

    if command["type"] == "system":
        return command["action"]

    return None

def save_custom_command(trigger, actions):
    commands = load_custom_commands()
    commands[trigger] = {
        "type": "sequence",
        "actions": actions
    }

    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(commands, f, indent=2)

def delete_custom_command(command_name):
    commands = load_custom_commands()

    if command_name not in commands:
        return False

    del commands[command_name]

    with open(COMMANDS_FILE, "w", encoding="utf-8") as f:
        json.dump(commands, f, indent=2)

    return True
