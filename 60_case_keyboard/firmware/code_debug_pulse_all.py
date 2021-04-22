import time
import board
from digitalio import DigitalInOut, Direction, Pull

pins = []

pins.append(DigitalInOut(board.P1_04)) # row 00
pins.append(DigitalInOut(board.P0_09)) # row 01
pins.append(DigitalInOut(board.P0_10)) # row 02
pins.append(DigitalInOut(board.P1_06)) # row 03
pins.append(DigitalInOut(board.P0_22)) # col 00
pins.append(DigitalInOut(board.P0_24)) # col 01
pins.append(DigitalInOut(board.P1_00)) # col 02
pins.append(DigitalInOut(board.P1_02)) # col 03
pins.append(DigitalInOut(board.P0_02)) # col 04
pins.append(DigitalInOut(board.P0_20)) # col 05
pins.append(DigitalInOut(board.P0_17)) # col 06
pins.append(DigitalInOut(board.P0_15)) # col 07
pins.append(DigitalInOut(board.P0_05)) # col 08
pins.append(DigitalInOut(board.P0_06)) # col 09
pins.append(DigitalInOut(board.P1_10)) # blue led

for pin in pins:
    pin.direction = Direction.OUTPUT

while True:
    for pin in pins:
        pin.value = True
    time.sleep(0.5)
    for pin in pins:
        pin.value = False
    time.sleep(0.5)