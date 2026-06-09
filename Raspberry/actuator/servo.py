from gpiozero import AngularServo

servo = AngularServo(
    18,
    min_angle=0,
    max_angle=90
)

def open_door():
    servo.angle = 90

def close_door():
    servo.angle = 0