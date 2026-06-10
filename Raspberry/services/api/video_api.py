import cv2
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.responses import FileResponse

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
print(sys.path.append(str(ROOT)))


from sensor.camera_service import (
    get_frame,
    start_camera
)

from logic.face_detector import (
    detect_faces
)

start_camera()

app = FastAPI()


def generate_frames():

    while True:

        frame = get_frame()

        if frame is None:
            continue

        frame = frame.copy()

        faces = detect_faces(
            frame
        )

        for (
            x,
            y,
            w,
            h
        ) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

        _, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )


@app.get("/video")
def video():

    return StreamingResponse(
        generate_frames(),
        media_type=
        "multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/capture")
def get_capture():

    return FileResponse(
        "media/captures/last_capture.jpg"
    )