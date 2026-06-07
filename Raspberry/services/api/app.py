from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlparse


RASPBERRY_DIR = Path(__file__).resolve().parents[2]
DEVICE_INFO_PATH = RASPBERRY_DIR / "device-info.json"
STATE_PATH = RASPBERRY_DIR / "state.json"


def read_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def component_status(state):
    if not state:
        return "offline"
    return "online"


def build_devices():
    device_info = read_json(DEVICE_INFO_PATH)
    state = read_json(STATE_PATH)
    last_update = state.get("lastUpdate")
    status = component_status(state)

    devices = [
        {
            "id": device_info.get("deviceId", "rpi-unknown"),
            "name": device_info.get("deviceName", "Raspberry Pi 5"),
            "type": "raspberry",
            "status": status,
            "location": device_info.get("ipAddress", "Raspberry Pi 5"),
            "lastSeen": last_update,
            "currentValue": "Gateway activo",
            "detail": "Controla sensores, actuadores y servicios del pipeline facial.",
        },
        {
            "id": "camera01",
            "name": "Cámara de acceso",
            "type": "camera",
            "status": status,
            "location": "Entrada principal",
            "lastSeen": last_update,
            "currentValue": "Lista para captura",
            "detail": "Fuente de video usada después de la detección PIR.",
        },
        {
            "id": "yolo01",
            "name": "Detector de personas",
            "type": "yolo",
            "status": status,
            "location": "Raspberry Pi 5",
            "lastSeen": last_update,
            "currentValue": "Pendiente de inferencia",
            "detail": "Valida si el movimiento corresponde a una persona.",
        },
        {
            "id": "face-db",
            "name": "Base de rostros autorizados",
            "type": "database",
            "status": status,
            "location": "Backend Python",
            "lastSeen": last_update,
            "currentValue": state.get("lastRecognition", "Sin reconocimiento"),
            "detail": "Consulta si la persona detectada existe en la base de datos.",
        },
    ]

    for sensor in device_info.get("sensors", []):
        sensor_type = sensor.get("type", "other").lower()
        devices.append(
            {
                "id": sensor.get("id"),
                "name": sensor.get("name"),
                "type": "pir" if sensor_type == "pir" else "other",
                "status": status,
                "location": "Entrada principal",
                "lastSeen": last_update,
                "gpio": sensor.get("gpio"),
                "currentValue": state.get("motionDetected", False),
                "detail": "Detecta movimiento e inicia el pipeline de reconocimiento.",
            }
        )

    state_keys = {
        "servo01": "doorState",
        "ledGreen": "greenLed",
        "ledRed": "redLed",
        "ledBlue": "blueLed",
    }

    for actuator in device_info.get("actuators", []):
        actuator_id = actuator.get("id")
        actuator_type = actuator.get("type", "other").lower()
        devices.append(
            {
                "id": actuator_id,
                "name": actuator.get("name"),
                "type": "servo" if actuator_type == "servo" else "led" if actuator_type == "led" else "other",
                "status": status,
                "location": "Entrada principal",
                "lastSeen": last_update,
                "gpio": actuator.get("gpio"),
                "currentValue": state.get(state_keys.get(actuator_id, ""), "Sin datos"),
                "detail": "Actuador físico controlado por el resultado del reconocimiento.",
            }
        )

    return devices


class ApiHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/device-info":
            self.respond_json(read_json(DEVICE_INFO_PATH))
            return

        if path == "/api/status":
            self.respond_json(read_json(STATE_PATH))
            return

        if path == "/api/devices":
            self.respond_json(build_devices())
            return

        self.respond_json({"error": "Not found"}, status=404)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def respond_json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")


def run(host="0.0.0.0", port=8000):
    server = ThreadingHTTPServer((host, port), ApiHandler)
    print(f"API listening on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
