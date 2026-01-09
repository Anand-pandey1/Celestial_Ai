import cv2
import mediapipe as mp
import pyautogui

pyautogui.FAILSAFE = True

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

screen_w, screen_h = pyautogui.size()
camera_running = False


def start_camera():
    global camera_running
    camera_running = True

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    print("📷 Camera + Hand Tracking started")

    while camera_running:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result = hands.process(rgb)

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

                index_tip = hand.landmark[8]
                x = int(index_tip.x * screen_w)
                y = int(index_tip.y * screen_h)

                pyautogui.moveTo(x, y, duration=0.05)

        cv2.imshow("Celestial AI - Hand Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    stop_camera(cap)


def stop_camera(cap=None):
    global camera_running
    camera_running = False

    if cap:
        cap.release()

    cv2.destroyAllWindows()
    print("📴 Camera stopped")
