from gpiozero import LED
from time import sleep
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from Raspberry.utils.state_manager import update_state



azul = LED(17)
amarillo = LED(27)
rojo = LED(22)

while True:

    azul.on()

 

    sleep(10)

    azul.off()

   

    amarillo.on()

    sleep(10)

    amarillo.off()

   

    rojo.on()

   
    sleep(10)

    rojo.off()

  