import board
import displayio
import framebufferio
import sharpdisplay
import time
import math

from digitalio import DigitalInOut, Direction, Pull


import busio

        
# Release the existing display, if any
displayio.release_displays()

bus = busio.SPI(board.P0_12,board.P0_04)
chip_select_pin = board.P0_08
# Select JUST ONE of the following lines:
# For the 400x240 display (can only be operated at 2MHz)
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, 400, 240, baudrate=2000000)
# For the 144x168 display (can be operated at up to 8MHz)
#framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, width=144, height=168, baudrate=8000000)

display_on_in = DigitalInOut(board.P0_30)
display_on_in.direction = Direction.OUTPUT
display_on_in.value = True

display = framebufferio.FramebufferDisplay(framebuffer)

from adafruit_display_text.label import Label
from terminalio import FONT


# rotary encoder
import rotaryio

encoder = rotaryio.IncrementalEncoder(board.P0_29,board.P1_11)

last_position = encoder.position

# buzzer

buzzer_pin = board.P0_03
# import pulseio
# buzzer = pulseio.PWMOut(board.P0_03, variable_frequency=True)
# buzzer.frequency = 430
# OFF = 0
# ON = 2**15
# buzzer.duty_cycle = ON
# time.sleep(1)
# buzzer.duty_cycle = OFF

# import simpleio

# TONE_FREQ = [ 262,  # C4
#               294,  # D4
#               330,  # E4
#               349,  # F4
#               392,  # G4
#               440,  # A4
#               494 ] # B4

# tone_pos = 3

# simpleio.tone(buzzer_pin, TONE_FREQ[0],duration=0.3)
# simpleio.tone(buzzer_pin, TONE_FREQ[1],duration=0.3)
# simpleio.tone(buzzer_pin, TONE_FREQ[2],duration=0.3)
# simpleio.tone(buzzer_pin, TONE_FREQ[3],duration=0.3)

from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle

my_display_group = displayio.Group(max_size=25)
display.show(my_display_group)

WHITE = 0xFFFFFF

roundrect = RoundRect(50, 100, 40, 80, 10, fill=WHITE, stroke=3)
my_display_group.append(roundrect)

label = Label(FONT, text="My Label Text asd lkasjd alksjd laksdj lksa \njdlksajdlsakjd lkas jdlksa jdalsk \njdalskjd alsjdalskdj lkjsad lakjsd hello", x = 50, y = 20, color=0xFFFFFF)
my_display_group.append(label)

while True:

    time.sleep(0.1)
    
    # position = encoder.position
    # if position != last_position:
    #     # tone = TONE_FREQ[tone_pos]
    #     print("here")
    #     time.sleep(0.1)

    #     # print(str(position) + ' '+ str(tone))
    #     # simpleio.tone(buzzer_pin, tone, duration=0.2)
    #     # if last_position > position:
    #     #     tone_pos += 1
    #     # else:
    #     #     tone_pos -= 1
    #     # tone_pos = min(tone_pos,len(TONE_FREQ)-1)
    #     # tone_pos = max(tone_pos,0)
    # last_position = position