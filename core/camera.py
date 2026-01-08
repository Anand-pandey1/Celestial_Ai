import cv2

camera_running = False

def start_camera():
    global camera_running
    camera_running = True

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera not accessible")
        return

    print("📷 Camera started")

    while camera_running:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Celestial AI - Camera", frame)

        # Press Q to exit camera manually
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
