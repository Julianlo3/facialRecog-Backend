import json
from pathlib import Path
from datetime import datetime

EVENTS_PATH = Path(
    "state/logs.json"
)


def add_event(
    device,
    message,
    mqtt_client=None
):

    timestamp = datetime.now().isoformat(
        timespec="seconds"
    )

    new_event = {
        "timestamp": timestamp,
        "device": device,
        "message": message
    }

    with open(
        EVENTS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        events = json.load(file)

    events.append(new_event)

    events = events[-100:]

    with open(
        EVENTS_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            events,
            file,
            indent=2,
            ensure_ascii=False
        )

    if mqtt_client:

        mqtt_client.publish(
            "facialRecog/events",
            json.dumps(
                new_event,
                ensure_ascii=False
            )
        )