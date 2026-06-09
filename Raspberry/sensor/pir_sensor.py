from gpiozero import MotionSensor

pir = MotionSensor(23)

def motion_detected():
    return pir.motion_detected