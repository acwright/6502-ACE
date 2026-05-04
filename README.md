6502-ACE
========

<!-- ![6502-ACE.png](./Images/6502-ACE.png) -->

An **AC6502** retro-style 8-bit computer based on the **65C02** microprocessor.

---

## Overview

The AC6502 ecosystem is a family of open-source, 65C02-based computers sharing a common architecture, memory map, and [BIOS](https://github.com/acwright/6502-BIOS). Each computer in the family is purpose-built for a different use case but runs the same software and firmware.

The **ACE** (All-in-one Computer Experience) is a complete, self-contained 65C02 computer on a single PCB. It integrates everything found across the COB's modular cards — CPU, memory, video, audio, storage, serial, GPIO, RTC, and keyboard controller — onto one board, delivering the full COB experience without a backplane or expansion cards.

---

## Architecture

All AC6502 computers share:

- **CPU**: 65C02 (or accurate emulation)
- **Memory**: 32KB RAM + 32KB ROM, with optional banked RAM expansion
- **Memory Map**: Standardized across the ecosystem — zero page, stack, I/O space ($8000–$9FFF), system ROM, and interrupt vectors at $FFFA–$FFFF
- **Bus**: 16-bit address bus, 8-bit bidirectional data bus, standard 65C02 control signals (RW, PHI2, RESET, IRQ, NMI, RDY, SYNC)
- **BIOS**: A common [BIOS](https://github.com/acwright/6502-BIOS) provides the kernel, monitor, and BASIC interpreter across all systems

---

## Hardware

This repository contains KiCad 7.0+ PCB designs for the ACE board.

### ACE Board
`Hardware/ACE/`

The single integrated board hosting the W65C02S CPU and all peripherals. Provides:

- **CPU**: W65C02S running at 1 MHz
- **RAM**: 32KB SRAM (62256) at $0000–$7FFF
- **ROM**: 32KB EEPROM (28C256) at $8000–$FFFF
- **Video**: TMS9918A VDP (composite output, 256×192) or Pico9918 (VGA 640×480)
- **Audio**: ARMSID SID chip emulator (3-voice synthesis, RCA output)
- **Storage**: CompactFlash socket (IDE protocol, up to 128GB)
- **Serial**: 65C51 ACIA with MAX232 level shifter (RS-232 via DB9, 50–19200 baud)
- **GPIO**: 65C22 VIA (20 GPIO pins, 2× 16-bit timers, shift register)
- **RTC**: DS1511Y real-time clock with battery-backed SRAM and Y2K support
- **Keyboard Controller**: ATmega1284P running ACE Controller firmware
- **Input**: PS/2 keyboard connector and 8×8 keyboard matrix header
- **Joystick**: Atari 2600-style joystick port
- **Clock**: On-board oscillator (1–8 MHz, selectable by swapping oscillator)
- **Reset**: Power-on RC reset circuit and manual reset button
- **Power**: 5V DC, 2–3A

---

## Firmware

This repository contains [PlatformIO](https://platformio.org/)-based firmware for the ACE board.

### ACE Controller
`Firmware/ACE Controller/`

Firmware for the ATmega1284P keyboard controller on the ACE board. Provides:

- Dual keyboard input: PS/2 and 8×8 matrix keyboard simultaneously
- PS/2 scancode to ASCII conversion
- Matrix keyboard scanning with hardware debouncing
- Modifier key support: Shift (symbols/punctuation) and Ctrl (control codes)
- Buffered output via 65C22 VIA with CA1/CB1 data-ready strobes
- Independent enable/disable for PS/2 and matrix inputs

See [Firmware/ACE Controller/README.md](./Firmware/ACE%20Controller/README.md) for setup and usage instructions.

---

## CAD
`CAD/`

3D-printable enclosure bases and laser-cut top panels for the ACE system.

---

## Production
`Production/`

JLCPCB-ready Gerber files and BOM/CPL for PCB fabrication and assembly.

---

## Schematics
`Schematics/`

PDF schematics for the ACE board.

---

## Libraries
`Libraries/`

Shared KiCad symbol and footprint libraries used across all AC6502 hardware projects.

---

## AC6502 Projects

| Project | Description |
|---------|-------------|
| [6502-BIOS](https://github.com/acwright/6502-BIOS) | The shared BIOS (kernel, monitor, BASIC) for all AC6502 computers |
| [6502-PRG](https://github.com/acwright/6502-PRG) | Template for writing assembly language programs |
| [6502-CRT](https://github.com/acwright/6502-CRT) | Template for writing assembly language cartridges |
| [6502-EMULATOR](https://github.com/acwright/6502-EMULATOR) | Node.js-based AC6502 emulator |
| [6502-WEBULATOR](https://github.com/acwright/6502-WEBULATOR) | Web-based AC6502 emulator |

---

## AC6502 Systems

| Project | Description |
|---------|-------------|
| [6502-ACE](https://github.com/acwright/6502-ACE) | All-in-one single-PCB computer — the COB experience without the backplane (you are here) |
| [6502-COB](https://github.com/acwright/6502-COB) | Computer on a Backplane — modular desktop computer with expandable card slots |
| [6502-DEV](https://github.com/acwright/6502-DEV) | Development Environment Vehicle — emulation-based dev system |
| [6502-KIM](https://github.com/acwright/6502-KIM) | KIM-1 inspired minimal computer |
| [6502-VCS](https://github.com/acwright/6502-VCS) | Video Computer System — cartridge-based retro gaming console |

---

## License

Hardware designs are released under the [CERN Open Hardware Licence Version 2 – Permissive](https://ohwr.org/cern_ohl_p_v2.txt).  
Firmware is released under the [MIT License](./Firmware/ACE%20Controller/LICENSE).
