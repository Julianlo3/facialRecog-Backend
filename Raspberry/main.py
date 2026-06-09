import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from sensor.pir_sensor import motion_detected

from actuator.leds import (
    blue_on,
    blue_off
)

from sensor.camera import (
    capture_frame
)

from logic.face_detector import (
    detect_face
)

from logic.face_recognition import (
    recognize_face
)

from services.mqtt.mqtt_client import (
    connect_mqtt
)

from utils.event_manager import (
    add_event
)

from utils.state_manager import (
    update_state
)


mqtt_client = connect_mqtt()

last_detection=0
COOLDOWN = 10

print("Sistema iniciado...")

while True:

    current_time = time.time()

    if (motion_detected() and current_time - last_detection >= COOLDOWN):


        last_detection = current_time
        print("Movimiento detectado")

        add_event(
            "Sensor PIR",
            "Movimiento detectado",
            mqtt_client
        )

        update_state(
            "motionDetected",
            True,
            mqtt_client
        )

        blue_on()

        add_event(
            "LED Azul",
            "Indicador de captura activado",
            mqtt_client
        )

        update_state(
            "blueLed",
            True,
            mqtt_client
        )

        time.sleep(10)

        frame = capture_frame()

        if frame is not None:

            add_event(
                "Cámara",
                "Captura de imagen realizada",
                mqtt_client
            )

            face_found = detect_face(frame)

            if face_found:

                print("Rostro detectado")

                add_event(
                    "OpenCV",
                    "Rostro detectado",
                    mqtt_client
                )

                update_state(
                    "faceDetected",
                    True,
                    mqtt_client
                )

                result = recognize_face(frame)

                print(result)

                if result and result.get("recognized"):

                    add_event(
                        "Reconocimiento Facial",
                        f"Usuario reconocido: {result['name']}",
                        mqtt_client
                    )

                    update_state(
                        "lastRecognition",
                        result["name"],
                        mqtt_client
                    )

                else:

                    add_event(
                        "Reconocimiento Facial",
                        "Usuario no reconocido",
                        mqtt_client
                    )

            else:

                add_event(
                    "OpenCV",
                    "No se detectó ningún rostro",
                    mqtt_client
                )

        else:

            add_event(
                "Cámara",
                "Error al capturar imagen",
                mqtt_client
            )

        blue_off()

        add_event(
            "LED Azul",
            "Indicador de captura desactivado",
            mqtt_client
        )

        update_state(
            "blueLed",
            False,
            mqtt_client
        )

        update_state(
            "motionDetected",
            False,
            mqtt_client
        )

        update_state(
            "faceDetected",
            False,
            mqtt_client
        )

        time.sleep(2)

    time.sleep(0.1)