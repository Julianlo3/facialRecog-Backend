import cv2
import requests


def recognize_face(frame):

    success, buffer = cv2.imencode(
        ".jpg",
        frame
    )

    if not success:

        raise Exception(
            "No se pudo convertir el frame"
        )

    response = requests.post(

        "http://localhost:8080/api/person/reconocer/",

        files={
            "imagen": (
                "capture.jpg",
                buffer.tobytes(),
                "image/jpeg"
            )
        }

    )

    print(response.status_code)
    print(response.text)


    return response.json()