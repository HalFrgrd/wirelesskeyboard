import time
import board
from digitalio import DigitalInOut, Direction, Pull

led = DigitalInOut(board.P1_10) # blue led
led.direction = Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)