from state import state

def set_mode(mode):
    mode = mode.upper()
    if mode not in ["TEXT", "CAMERA", "CONTROL"]:
        return "Invalid mode"

    state["current_mode"] = mode
    return f"Mode switched to {mode}"

def get_mode():
    return state["current_mode"]
