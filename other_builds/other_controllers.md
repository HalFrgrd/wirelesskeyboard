### Raspberry Pi
https://geekhack.org/index.php?topic=99682.0
https://www.youtube.com/watch?v=bqLId-HuUNc

### Esp32

### nrfMicro
Can I use p026 for something else if p04 does the job?
Can I provide pins for: 
- P1.04: yes
- P1.02: DFU, (normal in nrf52840 data sheet)
- P0.22: yes
- P0.07 (boot): ASK JORIC what BOOT is.
- p0.12, yes:
- 25 DCCH: no dc to dc converter
- 23 VDDH: no its high voltage power supply pin
- p0.05 (ain3): yes, its an analog pin

### [Goldfish](https://github.com/Dr-Derivative/Goldfish)
- Opensource (KiCad)
- Pro micro compatible
- USB-C
- Not wireless

### [BLE-Micro-Pro](https://github.com/sekigon-gonnoc/BLE-Micro-Pro)
- Opensource (KiCad)
- Almost pro micro compatible
- Micro USB
- Bluetooth

### [ShiroMicro](https://github.com/elfmimi/MMCProMicro)
- Opensource (KiCad)
- USB-C mid-mount
- Pro micro clone

### [BlueDuino](https://wiki.aprbrother.com/en/BlueDuino_rev2.html)
- Opensource
- Wireless; bluetooth
- Pro micro clone (slightly longer)



More: https://github.com/joric/nrfmicro/wiki/Alternatives