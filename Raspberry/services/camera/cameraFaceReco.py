import cv2
from gpiozero import LED
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

# LEDs
verde = LED(17)
rojo = LED(27)
azul = LED(22)


# Cámara
camera = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Detector de rostros
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def generate_frames():

    while True:

        success, frame = camera.read()

        if not success:
            continue

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(50, 50)
        )

        # Control LEDs
        if len(faces) > 0:

            verde.on()
            rojo.off()

        else:

            verde.off()
            rojo.on()

        # Dibujar rostros
        for (x, y, w, h) in faces:

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                "Rostro",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        _, buffer = cv2.imencode(
            ".jpg",
            frame
        )

        frame_bytes = buffer.tobytes()

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + frame_bytes +
            b"\r\n"
        )


@app.get("/video")
def video_feed():

    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )