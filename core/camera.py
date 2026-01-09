import cv2
import mediapipe as mp
import threading
from state import state

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def camera_loop():
    cap = cv2.VideoCapture(0)

    while state["camera_active"]:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                mp.solutions.drawing_utils.draw_landmarks(
                    frame, hand, mp_hands.HAND_CONNECTIONS
                )

        cv2.imshow("Celestial Camera", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def start_camera():
    if state["camera_active"]:
        return "Camera already running"

    state["camera_active"] = True
    threading.Thread(target=camera_loop, daemon=True).start()
    return "Camera started"

def stop_camera():
    state["camera_active"] = False
    return "Camera stopped"
