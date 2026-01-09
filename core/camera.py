import cv2
import mediapipe as mp
import threading
import pyautogui
import numpy as np
import time
from state import state

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Screen size
SCREEN_W, SCREEN_H = pyautogui.size()

# Click control
last_click_time = 0
CLICK_DELAY = 0.6  # seconds (prevents spam clicking)


def camera_loop():
    global last_click_time

    cap = cv2.VideoCapture(0)

    while state["camera_active"]:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = hand_landmarks.landmark

            # Draw landmarks
            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

            # Index finger tip (8)
            index_tip = landmarks[8]
            thumb_tip = landmarks[4]

            # Convert to screen coordinates
            x = int(index_tip.x * SCREEN_W)
            y = int(index_tip.y * SCREEN_H)

            # Mouse movement
            if state["mouse_control"]:
                pyautogui.moveTo(x, y, duration=0.03)

                # Distance between thumb & index finger
                distance = np.hypot(
                    index_tip.x - thumb_tip.x,
                    index_tip.y - thumb_tip.y
                )

                current_time = time.time()

                # CLICK gesture (pinch)
                if distance < 0.035:
                    if current_time - last_click_time > CLICK_DELAY:
                        pyautogui.click()
                        last_click_time = current_time

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
