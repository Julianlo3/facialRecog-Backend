import time
import cv2
import numpy as np
from pathlib import Path


from sensor.camera_service import (
    start_camera,
    capture_frames_for_recognition
)

from sensor.pir_sensor import (
    motion_detected
)

from actuator.servo import *

from actuator.leds import *

from logic.face_detector import (
    find_face_frame
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

start_camera()

mqtt_client = connect_mqtt()

last_detection = 0

COOLDOWN = 10

print("Sistema facialRecog iniciado")

while True:

    current_time = time.time()

    if (
        motion_detected()
        and current_time - last_detection >= COOLDOWN
    ):
        
        print("Moviemito detectado")

        last_detection = current_time

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

        yellow_on()

        update_state(
            "yellowLed",
            True,
            mqtt_client
        )

        time.sleep(2)

        frames = (
            capture_frames_for_recognition(
                duration=2,
                fps=5
            )
        )

        frame = find_face_frame(
            frames
        )
     
        if frame is not None:

            CAPTURE_PATH = (
            "../bdFacialRecog/facilRecog/media/captures/last_capture.jpg"
            )

            print(Path(CAPTURE_PATH).resolve())

            cv2.imwrite(
                CAPTURE_PATH,
                frame
            )

            print("foto guardada")

            mqtt_client.publish(
                "/facialRecog/capture",
                "new_capture"
            )

            add_event(
                "OpenCV",
                "Rostro detectado",
                mqtt_client
            )

            result = recognize_face(frame)

            print(result)

          

            if(result['recognized']):
                add_event(
                "Reconocimiento Facial",
                f"Usuario reconocido: {result['persona']}",
                mqtt_client)

                print("Persona encontrada")
                yellow_off()
                blue_on()
                open_door()
            else:
                print("Persona no encontrada")
                yellow_off()
                red_on()

            

        else:

            add_event(
                "OpenCV",
                "No se encontró rostro",
                mqtt_client
            )

            update_state(
                "motionDetected",
                False,
                mqtt_client
            )

        
        time.sleep(10)
        yellow_off()

        update_state(
            "yellowLed",
            False,
            mqtt_client
        )

    time.sleep(0.1)