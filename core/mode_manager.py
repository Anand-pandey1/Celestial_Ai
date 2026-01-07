current_mode = "NORMAL"

def set_mode(mode):
    global current_mode
    current_mode = mode
    return f"Mode switched to {current_mode}"

def get_mode():
    return current_mode
