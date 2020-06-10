# Protocols and concepts



## SPI (Serial Peripheral Interface)
- Synchronous
- Separate lines for data and clock
- Receiving hardware can be very simple, unlike what UART requires.
- Supports multiple slaves.
- Master controls all of the communication (slaves can't communicate between themselves).
- Can require a lot of pins.
- Generally faster than UART.

The master generates the serial clock **(SCK)**. 
Only ever one master.
Master sends data on line **MOSI** (Master Out / Slave In). 
If the slave needs to respond, it replies on **MISO** (Master In / Slave Out).
The master needs to know in advance when a slave needs to reply and how much data it will send.
The master will need to keep generating clock signals so that the slave can reply.

SPI is *full duplex*. Can receive and send at the same time.

Slave select **(SS)** is another line used by the master. Normally held high. Pulled low when the master wants to communication to occur.

Multiple slaves: You could have one SS line for each slave. This can take a up a lot of pins. Another option is to daisy chain them together.

Read more: https://learn.sparkfun.com/tutorials/serial-peripheral-interface-spi/all

## UART (Universal Asynchronous Receiver / Transmitter)
- Asynchronous => devices need precise timing
- Requires hardware overhead
- At least on start and stop bit are needed. This eats into data rate.
- **RX** and **TX** lines
- Can be slow compared to SPI and I2C.

A UART is a block of circuitry that implements serial communication. Can act as an intermediary between parallel and serial interfaces.
They can exist as stand-alone ICs but most commonly found inside MCs.

Simplex serial communication: slaves don't need to reply, so only a TX line is required.

Read more: https://learn.sparkfun.com/tutorials/serial-communication/

## I2C (Inter-integrated Circuit)
- Two wires for communication.
- Scales nicely with a lot devices (doesn't require a lot of pins)
- Fast compared to UART. Slower than SPI.
- More complex hardware than SPI but less than asynchronous serial.
- Can be implemented in software. 
- Uses **SDA** and **SCL**.
- Supports systems with multiple masters, unlike SPI.
- Master devices can't talk to each other over the bus and must take turns using the lines.


Each I2C bus has two signals: SCL (clock) and SDA (data).
The lines need to be pulled-up. 4.7k resistors are a good standard.

Read more: https://learn.sparkfun.com/tutorials/i2c/all

## Serial Wire Debug (SWD)
Provides a debug port in only two pins. A clock pin (SWCLK) and a bi-directional data pin (SWDIO). It can be used to program the board and debug. For the nrfMicro, we use it to put the bootloader on. The bootloader allows for more convenient updates over USB.

ST-Link V2 and BluePill are such programmers.

You can use the SWD and SWC pins as general gpio, but you won't be able to flash to the device using them. So a bad idea.

## JTAG
Provides debugging with 5 pins.

## Bootloader

A bootloader is some code that runs before any other software runs. It is stored in a special area of memory and usually hard to overwrite. It is used to update the microcontroller's firmware.

Microcontrollers start with nothing in their memory so external programming is the only way to get the first program into one.

[Read more](https://electronics.stackexchange.com/questions/27486/what-is-a-boot-loader-and-how-would-i-develop-one)

A DFU (Device Firmware Update) bootloader is one that supports updating the firmware. On startup, it checks if there is a valid program and tries to run it. Otherwise, it will enter DFU mode.