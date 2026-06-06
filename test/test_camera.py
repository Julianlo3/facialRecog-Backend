import cv2
import time

cap = cv2.VideoCapture(0)

time.sleep(2)

for i in range(10):
    ret, frame = cap.read()

cv2.imwrite("test.jpg", frame)

cap.release()
