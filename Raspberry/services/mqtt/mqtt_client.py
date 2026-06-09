import paho.mqtt.client as mqtt

def connect_mqtt():

    client = mqtt.Client()

    client.connect(
        "localhost",
        1883,
        60
    )

    return client
