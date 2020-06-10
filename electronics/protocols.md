## Protocols



### SPI (Serial Peripheral Interface)
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

### UART (Universal Asynchronous Receiver / Transmitter)
- Asynchronous => devices need precise timing
- Requires hardware overhead
- At least on start and stop bit are needed. This eats into data rate.
- **RX** and **TX** lines
- Can be slow compared to SPI and I2C.

A UART is a block of circuitry that implements serial communication. Can act as an intermediary between parallel and serial interfaces.
They can exist as stand-alone ICs but most commonly found inside MCs.

Simplex serial communication: slaves don't need to reply, so only a TX line is required.

Read more: https://learn.sparkfun.com/tutorials/serial-communication/

### I2C (Inter-integrated Circuit)
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