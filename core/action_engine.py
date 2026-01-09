from camera import start_camera, stop_camera
from state import state

def execute_action(action):
    if action["action"] == "camera_on":
        return start_camera()

    if action["action"] == "camera_off":
        return stop_camera()

    if action["action"] == "mouse_on":
        state["mouse_control"] = True
        return "Mouse control enabled"

    if action["action"] == "mouse_off":
        state["mouse_control"] = False
        return "Mouse control disabled"

    return "Command executed"
