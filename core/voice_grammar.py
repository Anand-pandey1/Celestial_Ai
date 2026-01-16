COMMAND_GRAMMAR = [
    "open chrome",
    "open notepad",
    "open calculator",
    "close chrome",
    "close notepad",
    "close calculator",

    "start camera",
    "stop camera",

    "scroll up",
    "scroll down",
    "left click",
    "right click",

    "exit",
    "shutdown"
]

WAKE_WORDS = [
    "celestial",
    "hey celestial",
    "ok celestial"
]

def build_grammar():
    grammar = []
    for w in WAKE_WORDS:
        grammar.append(w)
        for cmd in COMMAND_GRAMMAR:
            grammar.append(f"{w} {cmd}")
    return grammar
