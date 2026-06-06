from gpiozero import MotionSensor
import paho.mqtt.client as mqtt
from time import sleep

# PIR
pir = MotionSensor(23)

# MQTT
client = mqtt.Client()

client.connect("localhost", 1883, 60)

print("Esperando movimiento...")

while True:

    pir.wait_for_motion()

    print("Movimiento detectado")

    client.publish(
        "facialRecog/motion",
        "detected"
    )

    sleep(2)

    pir.wait_for_no_motion()

    print("Sin movimiento")

    client.publish(
        "facialRecog/motion",
        "clear"
    )