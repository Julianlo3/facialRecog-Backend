from gpiozero import LED
import paho.mqtt.client as mqtt

verde = LED(17)
rojo = LED(27)

TOPIC = "facialRecog/motion"

def on_connect(client, userdata, flags, rc):

    print("Conectado MQTT")

    client.subscribe(TOPIC)

def on_message(client, userdata, msg):

    mensaje = msg.payload.decode()

    print("Mensaje:", mensaje)

    if mensaje == "detected":

        verde.on()
        rojo.off()

    elif mensaje == "clear":

        verde.off()
        rojo.on()

client = mqtt.Client()

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost",1883)

client.loop_forever()