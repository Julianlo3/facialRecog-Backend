import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

ret, frame = cap.read()

if ret:
    cv2.imwrite("test.jpg", frame)
    print("Imagen guardada")
else:
    print("Error capturando imagen")

cap.release()

