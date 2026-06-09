import cv2


def capture_frame():

    camera = cv2.VideoCapture(0)

    ret, frame = camera.read()

    camera.release()

    return frame if ret else None