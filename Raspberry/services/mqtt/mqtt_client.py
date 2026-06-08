import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.connect(BROKER, PORT)

client.loop_start()

print("MQTT conectado")
