import cv2

camera = cv2.VideoCapture(0)

print("Abierta:", camera.isOpened())

ret, frame = camera.read()

print("Ret:", ret)

if ret:
    print("Shape:", frame.shape)
    cv2.imwrite("test.jpg", frame)
    print("Imagen guardada")

camera.release()