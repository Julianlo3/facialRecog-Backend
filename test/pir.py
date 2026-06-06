from gpiozero import LED, MotionSensor
from time import sleep

# LEDs
verde = LED(17)
rojo = LED(27)
azul = LED(22)

# PIR
pir = MotionSensor(23)

print("Esperando movimiento...")

while True:

    pir.wait_for_motion()

    print("MOVIMIENTO DETECTADO")

    verde.on()
    rojo.on()
    azul.on()

    pir.wait_for_no_motion()

    print("Sin movimiento")

    verde.off()
    rojo.off()
    azul.off()

    sleep(0.5)