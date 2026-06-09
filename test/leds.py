from gpiozero import LED
from time import sleep
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from Raspberry.utils.state_manager import update_state
from Raspberry.services.mqtt.mqtt_client import client

azul = LED(17)
amarillo = LED(27)
rojo = LED(22)

while True:

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

    amarillo.on()

    update_state(
        "yellowLed",
        True,
        client
    )

    sleep(10)

    amarillo.off()

    update_state(
        "yellowLed",
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