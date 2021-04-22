print("initialising...")

import time
import board
from digitalio import DigitalInOut, Direction, DriveMode, Pull

import gc
import sys

# keyboard imports
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode as KC
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.consumer_control import ConsumerControl

# rotary encoder
import rotaryio
encoder = rotaryio.IncrementalEncoder(board.P1_11,board.P0_29)
encoder_last_position = encoder.position

encoder_switch_pin = DigitalInOut(board.P0_31)
encoder_switch_pin.direction = Direction.INPUT
encoder_switch_pin.pull = Pull.UP

encoder_switch_last_position = True


def encoder_update():
    global encoder_last_position
    global encoder_switch_last_position
    if encoder_last_position > encoder.position:
        encoder_last_position = encoder.position
        keyboard_consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)
    elif encoder_last_position < encoder.position:
        encoder_last_position = encoder.position
        keyboard_consumer_control.send(ConsumerControlCode.VOLUME_DECREMENT)

    if encoder_switch_last_position != encoder_switch_pin.value:
        encoder_switch_last_position = encoder_switch_pin.value
        if not encoder_switch_last_position:
            keyboard_consumer_control.send(ConsumerControlCode.MUTE)


# display imports
import displayio
import framebufferio
import sharpdisplay
import busio

from adafruit_display_text.label import Label
from terminalio import FONT

# Release the existing display, if any
displayio.release_displays()

bus = busio.SPI(board.P0_12,board.P0_04)
chip_select_pin = board.P0_08
framebuffer = sharpdisplay.SharpMemoryFramebuffer(bus, chip_select_pin, 400, 240, baudrate=2000000)

display_on_in = DigitalInOut(board.P0_30)
display_on_in.direction = Direction.OUTPUT
display_on_in.value = True



display = framebufferio.FramebufferDisplay(framebuffer)


my_label = Label(FONT,text="hello hal", y=120,x=20,scale=4)
display.show(my_label)


# initialise pins
rows = [DigitalInOut(pin) for pin in [board.P1_04, board.P0_09, board.P0_10, board.P1_06]]
num_rows = len(rows)
for row in rows:
    row.direction = Direction.INPUT
    row.pull = Pull.DOWN

cols = [DigitalInOut(pin) for pin in [board.P0_22,board.P0_24,board.P1_00, board.P1_02,board.P0_02,board.P0_20,board.P0_17,board.P0_15,board.P0_05,board.P0_06]]
num_cols = len(cols)
for col in cols:
    col.direction = Direction.OUTPUT
    col.drive_mode = DriveMode.PUSH_PULL
    col.value = False

num_keys = num_cols * num_rows


# The keyboard object!
# time.sleep(0.5)  # Sleep for a bit to avoid a race condition on some systems

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)
keyboard_consumer_control = ConsumerControl(usb_hid.devices)

special_keys_that_need_checks = []

# in nanoseconds or 10s of nanoseconds?
TAPPING_TERM = 280*1e4

class KeySendBuffer():
    # could try and override the adafruit keyboard class
    # have it swap first instance. no need to keep track of position in buffer.
    # the freeze should affect both press and release
    def __init__(self, send_all_func) -> None:
        self.buffer = []
        self.index = 0
        self.frozen = 0 # a counter to allow multiple keys to express freeze on buffer
        self.send_all_func = send_all_func

    def put(self,key_code):
        self.buffer.append(key_code)
        self.index += 1
        return self.index -1
    
    def replace_keycode(self,keycode,position):
        self.buffer[position] = keycode
    
    def freeze(self):
        self.frozen += 1

    def unfreeze(self):
        self.frozen -= 1

    def reset(self):
        self.frozen = 0
        self.index = 0
        self.buffer = [] # have a look for mem management here

    def send_all(self):
        if self.frozen == 0 and self.index != 0:
            print("Cycle: ", cycle_counter, "Sending ", len(self.buffer), " keys by", self.send_all_func.__name__)
            try:
                self.send_all_func(*self.buffer)
            except ValueError:
                print("ERROR: PROBS TRIED PRESSING MORE THAN 6 ")
            self.reset()


depress_buffer = KeySendBuffer(keyboard.press)
release_buffer = KeySendBuffer(keyboard.release)

class NormalKey():
    def __init__(self,tap_key_code):
        self.tap_key_code = tap_key_code

    def depress(self):
        depress_buffer.put(self.tap_key_code)
    
    def release(self):
        release_buffer.put(self.tap_key_code)

class TapHoldKey():
    # change it so that if nothing else is pressed and it is released slightly over the tapping term, keep it as a tap.
    def __init__(self, tap_key_code, hold_key_code):
        self.tap_key_code = tap_key_code
        self.hold_key_code = hold_key_code
        self.depress_time_ns = 0
        self.state = "tap_key"
    
    def depress(self):
        self.depress_time_ns = time.monotonic_ns()
        self.state = "tap_key"

        # print("depressing tap key")
        depress_buffer.freeze()
        release_buffer.freeze()
        self.depress_buffer_pos = depress_buffer.put(self.tap_key_code)
        
        special_keys_that_need_checks.append(self)
    
    def switch_and_unfreeze(self):
        # print("swapping hold key in for tap key")
        depress_buffer.replace_keycode(self.hold_key_code,self.depress_buffer_pos)
        depress_buffer.unfreeze()
        release_buffer.unfreeze()

    def release_helper_hold(self):
        # here so that it can be overwritten
        release_buffer.put(self.hold_key_code)

    def release(self):

        if self in special_keys_that_need_checks:
            special_keys_that_need_checks.remove(self)

        if time.monotonic_ns() - self.depress_time_ns < TAPPING_TERM:
            # print("sending tap key code", self.tap_key_code )
            release_buffer.put(self.tap_key_code)
            depress_buffer.unfreeze()
            release_buffer.unfreeze()
        else:
            # print("releasing hold key code", self.hold_key_code)
            if self.state == "tap_key":
                self.switch_and_unfreeze()

            self.release_helper_hold()
    
    def check(self): # could have this trigger an event to send buffers, but what about multiple keys
        """ Return true if key no longer needs checking"""
        if  time.monotonic_ns() - self.depress_time_ns > TAPPING_TERM:
            # print("pressing hold key code", self.hold_key_code)
            self.state = "hold_key"
            self.switch_and_unfreeze()
            return True
        return False

KC_NULL = 0


layer_stack = ["base"]


class TapHoldLayer(TapHoldKey):
    def __init__(self, tap_key_code, layer_name):
        super().__init__(tap_key_code, KC_NULL)
        self.layer_name = layer_name
    
    def switch_and_unfreeze(self):
        self.old_layer_index = len(layer_stack)
        layer_stack.append(self.layer_name)
        return super().switch_and_unfreeze()

    def release_helper_hold(self):
        global layer_stack
        layer_stack = layer_stack[:self.old_layer_index]
        return super().release_helper_hold()

# class TapDance:
#     def __init__(self) -> None:
#         pass

import supervisor
class ReloadKey:
    def __init__(self) -> None:
        pass

    def depress(self):
        supervisor.reload()
    
    def release(self):
        print("shouldn't be seeing this")

# aliases
NK = NormalKey
TH = TapHoldKey
TL = TapHoldLayer

layout = {
    "base": [
    [NK(KC.Q),           NK(KC.W),NK(KC.E),    NK(KC.R),    NK(KC.T),NK(KC.Y),NK(KC.U),        NK(KC.I),    NK(KC.O),     NK(KC.P)],
    [TH(KC.A,KC.ALT),TH(KC.S,KC.GUI),TH(KC.D,KC.SHIFT),TH(KC.F,KC.CONTROL),NK(KC.G),NK(KC.H),TH(KC.J,KC.CONTROL), TH(KC.K,KC.RIGHT_SHIFT),TH(KC.L,KC.RIGHT_GUI),TH(KC.ENTER, KC.RIGHT_ALT)],
    [TH(KC.Z,KC.CONTROL),NK(KC.X),NK(KC.C),    NK(KC.V),    NK(KC.B),NK(KC.N),NK(KC.M),        NK(KC.COMMA),NK(KC.PERIOD),NK(KC.FORWARD_SLASH) ],
    [NK(KC_NULL), NK(KC_NULL),TL(KC.TAB,"navigation"),TL(KC.SPACE,"numbers"),NK(KC.A),ReloadKey(),NK(KC.BACKSPACE),NK(KC.A),    NK(KC_NULL),     NK(KC_NULL)]
    ],

    "numbers": [
    [NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.SEVEN),      NK(KC.EIGHT),      NK(KC.NINE),      NK(KC.A)],
    [NK(KC.C),      NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.ZERO),      NK(KC.FOUR),      NK(KC.FIVE),      NK(KC.SIX),      NK(KC.A)],
    [NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.ONE),      NK(KC.TWO),      NK(KC.THREE),      NK(KC.A)],
    [NK(KC.A),      NK(KC.A),      None,          None,          NK(KC.A),      None,      None,      NK(KC.A),      NK(KC.A),      NK(KC.A)],
    ],

    "navigation": [
    [NK(KC.ESCAPE), NK(KC.A),      NK(KC.A),  NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.PAGE_UP),   NK(KC.UP_ARROW),      NK(KC.PAGE_DOWN),      NK(KC.A)],
    [None,          None,          None,      None,          NK(KC.A),      NK(KC.HOME),   NK(KC.LEFT_ARROW),NK(KC.DOWN_ARROW),      NK(KC.RIGHT_ARROW),      NK(KC.END)],
    [NK(KC.A),      NK(KC.A),      NK(KC.A),  NK(KC.A),      NK(KC.A),      NK(KC.A),      NK(KC.A),         NK(KC.A),      NK(KC.A),      NK(KC.A)],
    [NK(KC.A),      NK(KC.A),      None,      None,          NK(KC.A),      NK(KC.A),      NK(KC.A),         NK(KC.A),      NK(KC.A),      NK(KC.A)],
    ]

}



mask = 0
# last_mask = 0 no need, just use mask
key_mask = 0
key_index = 0


class ByteArrayQueue:
    """Simple fixed length queue implementation"""
    def __init__(self, length):
        self.length = length
        self.q = bytearray(length)
        self.head = 0
        self.tail = 0
        self.size = 0
    
    def enqueue(self, x):
        self.q[self.tail] = x
        self.tail = (self.tail + 1) % self.length
        self.size += 1
    
    def dequeue(self):
        self.size -= 1
        self.head = (self.head + 1) % self.length
        return self.q[(self.head -1 + self.length) % self.length]
    

depress_events = ByteArrayQueue(num_keys)
release_events = ByteArrayQueue(num_keys)


# we need to keep track of which layer a key was depressed on.
# i.e. we can hold a modifier, go to another layer, then release the modifier.
layers_of_depressed_keys = {}

def get_key_that_is_being_depressed(key_index):
    # we are depressing it
    c_index, r_index = divmod(key_index,num_rows)

    # step through active layers to find one that is not transparent
    i = len(layer_stack)-1
    while(layout[layer_stack[i]][r_index][c_index] is None): # transparent
        i -= 1

    layers_of_depressed_keys[key_index] = layer_stack[i]

    print("Cycle: ", cycle_counter, "Depress for: ", c_index,r_index, "Layer: ", layer_stack[i])

    return layout[layer_stack[i]][r_index][c_index]

def get_key_that_is_being_released(key_index):
    # we are releasing it   
    key_layer = layers_of_depressed_keys[key_index]
    c_index, r_index = divmod(key_index,num_rows)
    print("Cycle: ", cycle_counter, "Release for: ", c_index,r_index, "Layer: ", key_layer)

    return layout[key_layer][r_index][c_index]


def handle_depress_events():
    num_events = depress_events.size
    for i in range(num_events):
        key_index = depress_events.dequeue()
        get_key_that_is_being_depressed(key_index).depress()

def handle_release_events():
    num_events = release_events.size
    for i in range(num_events):
        key_index = release_events.dequeue()
        get_key_that_is_being_released(key_index).release()


def handle_special_keys_that_need_checking():
    
    global special_keys_that_need_checks
    special_keys_that_need_checks = [key for key in special_keys_that_need_checks if not key.check() ]



cycles_to_average = 1000
sum_cycle_times = 0
start_time = 0
cycle_counter = 0
# start_time = time.monotonic_ns()
mask_changed = False

my_label.text = "Main loop!"
print("starting poll")

# Main loop
while True:
    if cycle_counter % 500 == 0:
        my_label.text = "hello \njack"#str(cycle_counter)
        my_label.x += 1
        my_label.x %= 300

        my_label.y += 1
        my_label.y %= 200

    

    key_index = -1

    for col in cols:
        col.value = True

        for row in rows:
            key_index += 1
            key_mask = 1 << key_index

            if row.value:
                # having these on seperate lines avoids having to do debounce i think
                if not (mask & key_mask): # first time this key is depressed
                    mask |= key_mask
                    depress_events.enqueue(key_index)

            elif (mask & key_mask): # first time key is released
                mask &= ~key_mask #set bit to zero
                release_events.enqueue(key_index)
            
        col.value = False
    
    handle_depress_events()
    handle_release_events()
    handle_special_keys_that_need_checking()
    depress_buffer.send_all() # may be frozen
    release_buffer.send_all()

    # in case of any stuck keys MAY CAUSE CONFUSION SOMEWHERE ELSE THOUGH
    if mask == 0:
        # keyboard.release_all()
        # depress_buffer.reset()
        # release_buffer.reset()
        if mask_changed:
            mask_changed = False
            print("------- No keys are down -------")
    else:
        mask_changed = True
    
    encoder_update()
    

    # if cycle_counter % cycles_to_average  == 0:
    #     sum_cycle_times = time.monotonic_ns()-start_time
    #     print("Cycle count: ", cycle_counter ,"Average cycle time (ms): ", sum_cycle_times/cycles_to_average/100000)
    #     start_time = time.monotonic_ns()
    cycle_counter += 1
