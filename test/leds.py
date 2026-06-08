from gpiozero import LED
from time import sleep
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from Raspberry.services.mqtt.state import update_state
from Raspberry.services.mqtt.mqtt_client import client

verde = LED(17)
rojo = LED(27)
azul = LED(22)

while True:

    verde.on()

    update_state(
        "greenLed",
        True,
        client
    )

    sleep(10)

    verde.off()

    update_state(
        "greenLed",
        False,
        client
    )

    rojo.on()

    update_state(
        "redLed",
        True,
        client
    )

    sleep(10)

    rojo.off()

    update_state(
        "redLed",
        False,
        client
    )

    azul.on()

    update_state(
        "blueLed",
        True,
        client
    )

    sleep(10)

    azul.off()

    update_state(
        "blueLed",
        False,
        client
    )