import json
import os

FILE = "data/learned_commands.json"

def load_commands():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)

def save_commands(commands):
    with open(FILE, "w") as f:
        json.dump(commands, f, indent=4)

def add_or_update_command(name, actions):
    commands = load_commands()
    commands[name] = actions
    save_commands(commands)

def get_command(name):
    return load_commands().get(name)