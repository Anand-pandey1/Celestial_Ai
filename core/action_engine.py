from camera import start_camera, stop_camera

def execute_action(action):
    if action["action"] == "camera_on":
        return start_camera()

    if action["action"] == "camera_off":
        return stop_camera()

    return "Command executed"
