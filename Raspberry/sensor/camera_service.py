import cv2
import threading
import time

camera = cv2.VideoCapture(
    0,
    cv2.CAP_V4L2
)

current_frame = None


def update_frames():

    global current_frame

    while True:

        success, frame = camera.read()

        if success:
            current_frame = frame.copy()

        time.sleep(0.01)


def start_camera():

    threading.Thread(
        target=update_frames,
        daemon=True
    ).start()


def get_frame():

    return current_frame


def capture_frames_for_recognition(
    duration=2,
    fps=5
):

    frames = []

    total_frames = duration * fps

    print("Tomando rostros")

    for _ in range(total_frames):

        frame = get_frame()

        if frame is not None:

            frames.append(
                frame.copy()
            )

        time.sleep(
            1 / fps
        )

    return frames