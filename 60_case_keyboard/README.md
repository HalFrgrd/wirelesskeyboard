# Unnamed keyboard
A PCB to fit into the 60% keyboard case I have.
- 35%
- Wireless
- Low power LCD
- Buzzer
- Rotary encoder
- Electronics based on the [nrfmicro](https://github.com/joric/nrfmicro/).

### LCD Notes
https://makerdyne.com/2015/02/08/large-memory-lcd-breakout-board-details/

The power supply input is 5V. 
But the logic levels are all 3.3V.

### Footprints
https://github.com/daprice/keyswitches.pretty

### Dimensions
These are some dimensions of [the specific case I used.](https://www.aliexpress.com/item/32921993410.html?pid=808_0000_0101&spm=a2g0n.search-amp.list.32921993410&aff_trace_key=2b17650114d94b82bf89c85dab72a30e-1550938224177-03600-UneMJZVf&aff_platform=msite&m_page_id=6878amp-RE3tNnzZA5LCyChfdei61Q1552019685186)


Case to standoff: 4.6mm
Indented case to standoff: 7.0mm
LCD connector height: 1.8mm
Distance from edge of case to LCD connector: 50.0mm
Useable indentation width: 42.1mm
Useable indentation length: 145.0mm
Useable indentation length with drop through rotary encoder: 109.0mm
Useable case width: 90.0mm

### Flashing
These are based on the instructions found in [joric's nrfmicro](https://github.com/joric/nrfmicro/wiki/Bootloader).

#### ST-Link V2 converted to Black Magic Probe
I used two ST-Link V2's and converted one into a [Black Magic Probe](https://github.com/blacksphere/blackmagic) using the instructions found [here](https://web.archive.org/web/20210121183153/http://blog.linuxbits.io/2016/02/15/cheap-chinese-st-link-v-2-programmer-converted-to-black-magic-probe-debugger/).
My notes on the conversion process are [here](https://github.com/HalFrgrd/halfrgrd.github.io/blob/master/black_magic_probe_windows_mingw64.md).
I would recommend this route as the two ST-Link V2's will cost less than $5.

#### Flashing notes
[GDB (GNU Project Debugger)](https://www.gnu.org/software/gdb/) is used to control the Black Magic Probe.
When I ran `target extended-remote COM3`, it'd hang or give an error. 
This was on Windows 10.
I found I could get working on Ubuntu 18.04 using `gdb-multiarch`.
I had to hold down the wires on the keyboard for the scanning to pick up the nrf52.

I ran the code command by command instead of the two lines joric gives.
For reference, the output of the gdb process is as follows:
```
(gdb) target extended-remote /dev/ttyACM0
Remote debugging using /dev/ttyACM0
(gdb) monitor swdp_scan
Target voltage: 3.28V
SW-DP scan failed!
(gdb) monitor swdp_scan
Target voltage: 3.28V
Available Targets:
No. Att Driver
 1      Nordic nRF52 M3/M4
 2      Nordic nRF52 Access Port
(gdb) att 1
Attaching to Remote target
warning: while parsing target description (at line 1): Target description specified unknown architecture "arm"
warning: Could not load XML target description; ignoring
Truncated register 34 in remote 'g' packet
(gdb) Truncated register 34 in remote 'g' packet
(gdb) mon erase_mass
erase..
Truncated register 34 in remote 'g' packet
(gdb) file ~/Downloads/bootloader.hex
A program is being debugged already.
Are you sure you want to change the file? (y or n) y
Reading symbols from ~/Downloads/bootloader.hex...(no debugging symbols found)...done.
Truncated register 34 in remote 'g' packet
(gdb) att 1
A program is being debugged already.  Kill it? (y or n) y
Attaching to program: /home/hfrgrd/Downloads/bootloader.hex, Remote target
warning: while parsing target description (at line 1): Target description specified unknown architecture "arm"
warning: Could not load XML target description; ignoring
Truncated register 34 in remote 'g' packet
(gdb) Truncated register 34 in remote 'g' packet
(gdb) mon erase
erase..
Truncated register 34 in remote 'g' packet
(gdb) load
Loading section .sec1, size 0xb00 lma 0x0
Loading section .sec2, size 0xf000 lma 0x1000
Loading section .sec3, size 0x10000 lma 0x10000
Loading section .sec4, size 0x5de8 lma 0x20000
Loading section .sec5, size 0x70c8 lma 0xf4000
Loading section .sec6, size 0x8 lma 0x10001014
Start address 0x0, load size 182712
Truncated register 34 in remote 'g' packet
```
