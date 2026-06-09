from gpiozero import LED
from gpiozero import AngularServo

led_blue = LED(17)
led_yellow = LED(27)
led_red = LED(22)

servo = AngularServo(
    18,
    min_angle=0,
    max_angle=90
)

def blue_on():
    led_blue.on()

def blue_off():
    led_blue.off()

def yellow_on():
    led_yellow.on()

def yellow_off():
    led_yellow.off()

def red_on():
    led_red.on()

def red_off():
    led_red.off()

def open_door():
    servo.angle = 90

def close_door():
    servo.angle = 0