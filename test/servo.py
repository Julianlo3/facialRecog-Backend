from gpiozero import AngularServo
from time import sleep

servo = AngularServo(18)

while True:
    servo.min()
    sleep(2)

    servo.mid()
    sleep(2)

    servo.max()
    sleep(2)