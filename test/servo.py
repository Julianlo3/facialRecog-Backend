from gpiozero import AngularServo
from time import sleep

servo = AngularServo(
    18,
    min_angle=0,
    max_angle=180,
    min_pulse_width=0.0005,
    max_pulse_width=0.0025
)

while True:

    print("120°")
    servo.angle = 90
    sleep(5)

    servo.detach()

    sleep(2)

    print("180°")
    servo.angle = 180
    sleep(5)

    servo.detach()

    sleep(2)