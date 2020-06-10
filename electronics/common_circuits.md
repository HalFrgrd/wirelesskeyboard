## LEDs
Single LED:

![](https://www.electronicshub.org/wp-content/uploads/2017/10/Simple-LED-Circuits-Circuit-1.jpg)
With no resistor, the LED would burn out quickly.

Calculating the resistor value: $R = \frac{V_{source}-V_{LED}}{I_{LED}}$.

[Read more](https://www.electronicshub.org/simple-led-circuits/)

## Joysticks
- 4 / 5 lines
- 5 if we are using it as a button as well
- VCC, GND, X, Y
- X, Y need to go to analog pins.

[Read more](https://www.brainy-bits.com/arduino-joystick-tutorial/)

## Rotary encoders
The encoder generates two offset square wave outputs. Measuring both of them can tell us the direction and speed we are rotating.

Encoders rotate around continuously but potentiometers only rotate one revolution.

[Read more](https://www.electroschematics.com/rotary-encoder-arduino/)

When wiring in a keyboard circuit, treat it like a normal switch but have two extra pins:
![](rotary_encoder_keyboard.png)

[Using multiple encoders in a keyboard:](https://www.youtube.com/watch?v=DyHxccSvsPs) The two pins on every encoder for the two square wave outputs (A and B) are wired to the same two pins on the controller. So we only need to use two pins on the controller for any number of encoders. The C lines are wired through a diode to the rows. A matrix scan can then measure the values for each individual encoder.

![](multiple_rotary_encoders.png)

## Display ILI9341 with touchscreen
https://www.youtube.com/watch?time_continue=33&v=beyDkTBhpgs&feature=emb_title
