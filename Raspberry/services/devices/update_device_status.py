import json
from pathlib import Path
import cv2

from gpiozero import MotionSensor, LED, AngularServo

DEVICE_INFO_PATH = Path("Raspberry/config/device-info.json")

def update_device_status():

    with open(DEVICE_INFO_PATH, "r", encoding="utf-8") as file:
        info = json.load(file)

    # PIR
    try:
        pir = MotionSensor(23)
        info["sensors"][0]["status"] = "online"
        pir.close()
    except:
        info["sensors"][0]["status"] = "offline"

    # Cámara
    try:
        camera = cv2.VideoCapture(0)
        info["sensors"][1]["status"] = (
            "online"
            if camera.isOpened()
            else "offline"
        )
        camera.release()
    except:
        info["sensors"][1]["status"] = "offline"

    # Servo
    try:
        servo = AngularServo(18)
        info["actuators"][0]["status"] = "online"
        servo.close()
    except:
        info["actuators"][0]["status"] = "offline"

    # LEDs
    leds = [
        (17, 1),  # Azul
        (27, 2),  # Amarillo
        (22, 3)   # Rojo
    ]

    for gpio, index in leds:

        try:
            led = LED(gpio)
            info["actuators"][index]["status"] = "online"
            led.close()

        except:
            info["actuators"][index]["status"] = "offline"

    with open(DEVICE_INFO_PATH, "w", encoding="utf-8") as file:
        json.dump(
            info,
            file,
            indent=2,
            ensure_ascii=False
        )