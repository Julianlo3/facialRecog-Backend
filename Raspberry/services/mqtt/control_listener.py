import json

from actuator.leds import (
    blue_on,
    blue_off,
    red_on,
    red_off,
    yellow_on,
    yellow_off
)

from actuator.servo import (
    open_door,
    close_door
)

from utils.state_manager import (
    update_state
)

from utils.event_manager import (
    add_event
)

print("Escuchando comandos MQTT")


def handle_control_message(
    client,
    payload
):
    
    print("Mensaje MQTT llegado")

    device = payload.get(
        "device"
    )

    action = payload.get(
        "action"
    )

    print(
        f"{device} -> {action}"
    )

    if device == "ledBlue":

        if action == "on":

            blue_on()

            update_state(
                "blueLed",
                True,
                client
            )

        else:

            blue_off()

            update_state(
                "blueLed",
                False,
                client
            )

    elif device == "ledRed":

        if action == "on":

            red_on()

            update_state(
                "redLed",
                True,
                client
            )

        else:

            red_off()

            update_state(
                "redLed",
                False,
                client
            )

    elif device == "ledYellow":

        if action == "on":

            yellow_on()

            update_state(
                "yellowLed",
                True,
                client
            )

        else:

            yellow_off()

            update_state(
                "yellowLed",
                False,
                client
            )

    elif device == "servo01":

        if action == "on":

            open_door()

            update_state(
                "door",
                "open",
                client
            )

        else:

            close_door()

            update_state(
                "door",
                "closed",
                client
            )

    add_event(
        device,
        f"Comando manual: {action}",
        client
    )