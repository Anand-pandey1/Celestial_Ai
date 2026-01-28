import cv2
import mediapipe as mp
import threading
import pyautogui
import numpy as np
import time
import os
import sys

# Add parent directory to path for UI imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from state import state
from UI.floating_panel import update_status

# ===================== TUNING PARAMETERS =====================
SMOOTHING = 0.75           # 0.6–0.85 (higher = smoother, slower)
PINCH_THRESHOLD = 0.04     # pinch sensitivity
SCROLL_THRESHOLD = 0.035
SCROLL_SPEED = 300         # scroll intensity
CLICK_COOLDOWN = 0.6       # seconds
MOVE_DURATION = 0.02       # mouse move speed
FRAME_WIDTH = 480
FRAME_HEIGHT = 360
# =============================================================

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

SCREEN_W, SCREEN_H = pyautogui.size()

last_left_click = 0
last_right_click = 0

# Smoothed cursor position
prev_x, prev_y = 0, 0


def dist(a, b):
    return np.hypot(a.x - b.x, a.y - b.y)


def smooth(current, previous):
    return previous * SMOOTHING + current * (1 - SMOOTHING)


def camera_loop():
    global last_left_click, last_right_click, prev_x, prev_y

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    while state["camera_active"]:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            hand = results.multi_hand_landmarks[0]
            lm = hand.landmark

            mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

            thumb = lm[4]
            index = lm[8]
            middle = lm[12]
            ring = lm[16]

            # -------- PAUSE GESTURE (FIST) --------
            fist = (
                dist(index, thumb) < 0.04 and
                dist(middle, thumb) < 0.04 and
                dist(ring, thumb) < 0.04
            )

            state["mouse_paused"] = fist

            if state["mouse_control"] and not state["mouse_paused"]:
                # -------- MOUSE MOVE (SMOOTHED) --------
                raw_x = index.x * SCREEN_W
                raw_y = index.y * SCREEN_H

                smooth_x = smooth(raw_x, prev_x)
                smooth_y = smooth(raw_y, prev_y)

                pyautogui.moveTo(
                    int(smooth_x),
                    int(smooth_y),
                    duration=MOVE_DURATION
                )

                prev_x, prev_y = smooth_x, smooth_y

                now = time.time()

                # -------- LEFT CLICK --------
                if dist(index, thumb) < PINCH_THRESHOLD:
                    if now - last_left_click > CLICK_COOLDOWN:
                        pyautogui.click()
                        last_left_click = now

                # -------- RIGHT CLICK --------
                if dist(middle, thumb) < PINCH_THRESHOLD:
                    if now - last_right_click > CLICK_COOLDOWN:
                        pyautogui.rightClick()
                        last_right_click = now

                # -------- SCROLL --------
                if dist(index, middle) < SCROLL_THRESHOLD:
                    scroll_delta = int((index.y - middle.y) * SCROLL_SPEED)
                    scroll_delta = max(min(scroll_delta, 50), -50)  # clamp
                    pyautogui.scroll(scroll_delta)

        cv2.imshow("Celestial Camera", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        time.sleep(0.005)  # FPS stability

    cap.release()
    cv2.destroyAllWindows()


def start_camera():
    if state["camera_active"]:
        update_status("Camera already ON")
        return "Camera already running"

    state["camera_active"] = True
    update_status("📷 Camera ON")
    threading.Thread(target=camera_loop, daemon=True).start()
    return "Camera started"


def stop_camera():
    state["camera_active"] = False
    update_status("📷 Camera OFF")
    return "Camera stopped"
