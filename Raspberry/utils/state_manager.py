import json
from pathlib import Path
from datetime import datetime

STATE_PATH = Path("state/state.json")

def update_state(key, value, mqtt_client=None):

    with STATE_PATH.open("r", encoding="utf-8") as file:
        state = json.load(file)

    state[key] = value
    state["lastUpdate"] = datetime.now().isoformat(timespec="seconds")

    with STATE_PATH.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=2, ensure_ascii=False)

    if mqtt_client:

        mqtt_client.publish(
            "facialRecog/state",
            json.dumps(state)
        )

    