import json

import paho.mqtt.client as mqtt

from services.mqtt.control_listener import (
    handle_control_message
)


def on_message(
    client,
    userdata,
    msg
):
    
    print("MENSAJE RECIBIDO")

    try:

        payload = json.loads(
            msg.payload.decode()
        )

        print(
            msg.topic,
            payload
        )

        if (
            msg.topic ==
            "facialRecog/control"
        ):

            handle_control_message(
                client,
                payload
            )

    except Exception as e:

        print(
            "Error MQTT:",
            e
        )


def connect_mqtt():

    client = mqtt.Client()

    client.on_message = (
        on_message
    )

    client.connect(
        "localhost",
        1883,
        60
    )

    client.subscribe(
        "facialRecog/control"
    )

    print("Suscrito a facialRecog/control")

    client.loop_start()

    print(
        "MQTT conectado"
    )

    return client