import json
from pathlib import Path
from datetime import datetime

EVENTS_PATH = Path(
    "Raspberry/state/events.json"
)

def add_event(event, data=None):

    with open(
        EVENTS_PATH,
        "r",
        encoding="utf-8"
    ) as file:

        events = json.load(file)

    new_event = {
        "timestamp":
        datetime.now().isoformat(
            timespec="seconds"
        ),
        "event": event
    }

    if data:
        new_event.update(data)

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