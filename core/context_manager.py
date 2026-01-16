class ContextManager:
    def __init__(self):
        self.last_app = None
        self.last_action = None

    def update(self, action: dict):
        if action.get("action") == "open_app":
            self.last_app = action.get("app")
        self.last_action = action.get("action")

    def resolve_pronoun(self, command: str):
        if "close it" in command and self.last_app:
            return f"close {self.last_app}"
        return command
