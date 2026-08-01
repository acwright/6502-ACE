# AB Controller

## Overview

The AB Controller is firmware for the ATMega1284P microcontroller that provides dual keyboard input support for 6502-based computer systems. It can simultaneously handle both PS/2 keyboard input and custom keyboard matrix input, converting keypresses to ASCII codes and outputting them through a 6522 VIA (Versatile Interface Adapter) interface.

## Features

- **Dual Input Support**: Handles both PS/2 keyboards and 8x8 keyboard matrix simultaneously
- **ASCII Conversion**: Converts PS/2 scancodes and matrix keypresses to ASCII characters
- **Always Uppercase Letters**: Letters are always output as uppercase ASCII regardless of modifiers
- **Modifier Keys**: Shift (symbols/numbers only) and Ctrl (control codes)
- **Buffered Input**: Uses circular buffers to prevent data loss during rapid typing
- **Debounced Matrix Scanning**: Hardware debouncing for reliable matrix keyboard operation
- **Enable/Disable Control**: Independent enable signals for PS/2 and matrix inputs
- **Shared Joystick Ports**: Releases PORT A / PORT B when disabled so the 6502 can read the two Atari 2600-compatible joysticks that share those ports
- **6502 Reset Control**: Drives the 6502 RESB line, providing power-on reset and a debounced reset button
- **Jiffy Clock (optional)**: Can generate periodic 6502 NMIs from a DS1511Y RTC square-wave input. Disabled by default; enabled at build time via the `ENABLE_SQW` define

## Hardware Connections

### ATMega1284P Pin Assignments

#### VIA PORT A (Pins 24-31)
Used for row scanning (matrix mode) or ASCII output (PS/2 mode):
- PA0 (Pin 24) - VIA_PA0 / Row 0 / Data Bit 0
- PA1 (Pin 25) - VIA_PA1 / Row 1 / Data Bit 1
- PA2 (Pin 26) - VIA_PA2 / Row 2 / Data Bit 2
- PA3 (Pin 27) - VIA_PA3 / Row 3 / Data Bit 3
- PA4 (Pin 28) - VIA_PA4 / Row 4 / Data Bit 4
- PA5 (Pin 29) - VIA_PA5 / Row 5 / Data Bit 5
- PA6 (Pin 30) - VIA_PA6 / Row 6 / Data Bit 6
- PA7 (Pin 31) - VIA_PA7 / Row 7 / Data Bit 7

#### VIA PORT B (Pins 0-7)
Used for column scanning (matrix mode) or ASCII output (matrix output):
- PB0 (Pin 0) - VIA_PB0 / Column 0 / Data Bit 0
- PB1 (Pin 1) - VIA_PB1 / Column 1 / Data Bit 1
- PB2 (Pin 2) - VIA_PB2 / Column 2 / Data Bit 2
- PB3 (Pin 3) - VIA_PB3 / Column 3 / Data Bit 3
- PB4 (Pin 4) - VIA_PB4 / Column 4 / Data Bit 4
- PB5 (Pin 5) - VIA_PB5 / Column 5 / Data Bit 5
- PB6 (Pin 6) - VIA_PB6 / Column 6 / Data Bit 6
- PB7 (Pin 7) - VIA_PB7 / Column 7 / Data Bit 7

#### Control Signals
- Pin 8 (VIA_CA1) - PS/2 Data Ready strobe (output)
- Pin 9 (VIA_CA2) - PS/2 Enable (input, active low)
- Pin 10 (PS2CLK) - PS/2 Clock input
- Pin 11 (PS2DATA) - PS/2 Data input
- Pin 12 (VIA_CB1) - Matrix Data Ready strobe (output)
- Pin 13 (VIA_CB2) - Matrix Enable (input, active low)

#### 6502 System Control
- PC0 (Pin 16) - RESET_BTN / Reset button (input, N.O., active low, internal pull-up)
- PC7 (Pin 23) - RESB / 6502 reset output (active low)
- PD6 (Pin 14) - RTC_SQW / DS1511Y square-wave input (jiffy clock source)
- PD7 (Pin 15) - NMIB / 6502 non-maskable interrupt output (active low)

#### Clock
- XTAL1 - 16 MHz full-can oscillator module (external clock source)

### PS/2 Keyboard Interface

Connect a PS/2 keyboard to:
- **CLK**: Pin 10 (PS2CLK)
- **DATA**: Pin 11 (PS2DATA)
- **VCC**: +5V
- **GND**: Ground

### Keyboard Matrix Interface

The firmware supports an 8x8 keyboard matrix (64 keys maximum):
- **Rows**: Connected to PA0-PA7 (Pins 24-31)
- **Columns**: Connected to PB0-PB7 (Pins 0-7)

Each key connects a row to a column when pressed. The matrix is scanned with rows driven low and columns read with pull-ups.

### Joystick Interface

PORT A and PORT B are shared between this encoder and two Atari 2600-compatible
joysticks. Unlike COB's Keyboard Encoder Helper and VCS's Input Board, which
reach a stick through a helper board, the ACE Board carries its own DB-9s —
`J6` JOYSTICK A and `J8` JOYSTICK B — with the 1kΩ pull-ups fitted on board
(`R6`–`R13` on PORT A, `R14`–`R21` on PORT B). The same port lines are also
brought out on the `J9` PORT B / `J10` PORT A 2×6 box headers.

The BIOS reads the two sticks through those same ports:

| BIOS routine | BASIC | VIA port | ACE connector | Encoder released by |
|---|---|---|---|---|
| `ReadJoystick1` (`$A048`) | `JOY(1)` | PORT B | `J8` JOYSTICK B | `CB2` high — matrix encoder off |
| `ReadJoystick2` (`$A04B`) | `JOY(2)` | PORT A | `J6` JOYSTICK A | `CA2` high — PS/2 encoder off |

> Note the naming trap: `J6` *JOYSTICK A* is PORT A, which is `JOY(2)`, and `J8`
> *JOYSTICK B* is PORT B, which is `JOY(1)`.

Each read returns the port raw, as a bitmask:

```
Bit:  7   6   5   4   3   2   1   0
      R   L   D   U   Y   X   B   A
```

The ports are **active low** — every line is pulled high and grounded by the
stick's switch — so a held button reads `0` and an untouched stick reads `$FF`.

Both DB-9s are wired the same way:

| DB-9 pin | Function | `J6` (PORT A) | `J8` (PORT B) |
|---|---|---|---|
| 1 | Up | PA4 | PB4 |
| 2 | Down | PA5 | PB5 |
| 3 | Left | PA6 | PB6 |
| 4 | Right | PA7 | PB7 |
| 5 | Y | PA3 | PB3 |
| 6 | A (fire) | PA0 | PB0 |
| 7 | B | PA1 | PB1 |
| 8 | GND | GND | GND |
| 9 | X | PA2 | PB2 |

Pins 1–4, 6 and 8 match a standard Atari 2600 stick. Pins 5, 7 and 9 carry the
extra Y, B and X buttons rather than the 2600's paddle pots and +5V, so a
2600 stick works with A/fire only, and nothing on the connector sources power.

This is the firmware's obligation in the joystick path: when `CA2` or `CB2`
goes high, it releases the corresponding port within 100 µs so the 6502 can
read the stick directly — the same arrangement a C64 has with a CIA port.
`disablePS2()` releases PORT A and `disableMatrix()` releases PORT B, both by
returning the pins to `INPUT_PULLUP` rather than bare `INPUT`, so an untouched
stick reads `$FF` even on a board relying on the pull-up alone.

The BIOS reads a stick as `KBDisable` → settle → read the port directly →
`KBEnable`. Nothing is transmitted over the shared lines, so there is nothing
for one stick to corrupt on the other's behalf — **both sticks read correctly
even when held at the same time.** An earlier design had the encoder push
joystick state to the 6502 as control bytes over the keyboard channel instead;
that could not report a held button on the port it was reporting over, and was
abandoned. See
[BIOS `PLAN.md` §2](https://github.com/acwright/6502-BIOS/blob/main/PLAN.md)
for the full account.

**Measured release latency: to be measured later.** This is the figure the
BIOS's `KBDisable` settle wait is sized against. Cycle-counting the compiled
firmware puts the worst-case code path at ~17 µs against a 100 µs budget, but
that excludes a PS/2 interrupt landing in the window and says nothing about how
long the bus takes to charge through a pull-up, so the published number comes
from a scope. See [PLAN.md](../../PLAN.md).

## Keyboard Matrix Layout

```
       PB0    PB1    PB2    PB3    PB4    PB5    PB6    PB7
PA0:    `      1      2      3      4      5      6      7
PA1:    8      9      0      -      =      BS     ESC    TAB
PA2:    Q      W      E      R      T      Y      U      I
PA3:    O      P      [      ]      \      INS    CAPS   A
PA4:    S      D      F      G      H      J      K      L
PA5:    ;      '    ENTER   DEL   SHIFT    Z      X      C
PA6:    V      B      N      M      ,      .      /      UP
PA7:  CTRL   MENU    ALT   SPACE   FN    LEFT   DOWN  RIGHT
```

**Special Keys:**
- BS = Backspace (0x08)
- ESC = Escape (0x1B)
- TAB = Tab (0x09)
- INS = Insert (0x1A)
- DEL = Delete (0x7F)
- ENTER = Enter (0x0D)
- Arrow keys: UP (0x1E), LEFT (0x1C), DOWN (0x1F), RIGHT (0x1D)

**Ignored Keys:**
- Caps Lock, Menu/GUI, Alt, Fn — produce no output and track no state

## Operation Modes

### PS/2 Mode
When VIA_CA2 (Pin 9) is pulled LOW:
- PS/2 keyboard is enabled
- Scancodes are converted to ASCII
- Output appears on PORT A (PA0-PA7)
- VIA_CA1 pulses low when data is ready

### Matrix Mode
When VIA_CB2 (Pin 13) is pulled LOW:
- Matrix keyboard is enabled
- Matrix is scanned every 10ms
- Keys are debounced (stable for 2 scans)
- Output appears on PORT B (PB0-PB7)
- VIA_CB1 pulses low when data is ready

### Dual Mode
Both keyboards can operate simultaneously if both enable signals are active.

### Joystick Reads
When an enable signal goes HIGH the firmware releases that port so the joystick
sharing it can be read by the 6502 — see [Joystick Interface](#joystick-interface).

## 6502 System Control

In addition to keyboard input, the controller manages reset and interrupt timing
for the host 6502.

### Reset Control (RESB)

The controller drives the 6502 RESB line on PC7 (active low):

- **Power-on reset**: At startup RESB is asserted immediately and held low for
  ~250 ms (`POR_HOLD_MS`) so the supply rails and 16 MHz oscillator stabilize
  before the 6502 begins executing.
- **Reset button**: A normally-open, active-low button on PC0 (internal pull-up)
  is polled and debounced (`RESET_DEBOUNCE_MS`, ~20 ms). While the button is
  held, RESB is asserted; releasing it brings the 6502 out of reset.

### Jiffy Clock (NMIB)

> **Disabled by default.** SQW-driven NMI behavior is only compiled in when the
> `ENABLE_SQW` define is enabled (see [Enabling the Jiffy Clock](#enabling-the-jiffy-clock)).
> When it is disabled, NMIB (PD7) is configured as a high-impedance input and is
> held high by the physical pull-up resistor on the PCB, so the 6502 never
> receives an NMI from this board.

When enabled, a DS1511Y RTC drives a square wave into PD6 (RTC_SQW). A pin-change
interrupt counts the rising edges and, every `JIFFY_DIVIDER` edges (default 1),
pulses the 6502 NMIB line on PD7 low for ~5 µs. The NMI is generated directly in
the ISR so its timing is independent of keyboard-scanning load. Set the DS1511Y
SQW output rate (and `JIFFY_DIVIDER`) to obtain the desired jiffy tick frequency.

To protect the 6502 BIOS boot window from a power-up SQW burst (the DS1511Y
powers up with SQW in an undefined, battery-backed state that can default to
32.768 kHz), the interrupt is not armed immediately. Arming is deferred until
`SQW_BOOT_GRACE_MS` (~500 ms) after RESB is released, and is re-deferred each
time the reset button asserts reset.

#### Enabling the Jiffy Clock

The jiffy clock is off unless you opt in at build time. In
[src/main.cpp](src/main.cpp), uncomment the define near the top of the file:

```c
#define ENABLE_SQW
```

Then rebuild and re-flash the firmware. Leaving it commented out keeps NMIB as a
high-impedance input and compiles out all SQW-related code.

## ASCII Character Mapping

### Modifier Priority

1. **Ctrl** — If held, produce control code. Shift is ignored.
2. **Shift** — If held (no Ctrl), produce shifted symbol. Letters unaffected.
3. **Base** — No modifier: produce base ASCII (letters always uppercase).

### Control Characters (Ctrl+Key)

- Ctrl+2 = 0x00 (NUL)
- Ctrl+A-Z = 0x01-0x1A
- Ctrl+[ = 0x1B (ESC)
- Ctrl+\ = 0x1C (FS)
- Ctrl+] = 0x1D (GS)
- Ctrl+6 = 0x1E (RS)
- Ctrl+- = 0x1F (US)

### Shifted Symbols

Shift only affects number and symbol keys (not letters):

| Base | Shifted | | Base | Shifted |
|------|---------|-|------|---------|
| 1 → ! | 2 → @ | | 3 → # | 4 → $ |
| 5 → % | 6 → ^ | | 7 → & | 8 → * |
| 9 → ( | 0 → ) | | - → _ | = → + |
| [ → { | ] → } | | \ → \| | ; → : |
| ' → " | , → < | | . → > | / → ? |
| ` → ~ | | | | |

### Printable Characters

Letters are always uppercase (A-Z). Numbers, symbols, space, and navigation keys follow standard ASCII.

## Build Instructions

### Prerequisites

1. **Install PlatformIO**
   ```bash
   # Using pip
   pip install platformio
   
   # Or install PlatformIO IDE extension for VS Code
   ```

2. **Install MiniPro Programmer Software** (for uploading)
   ```bash
   # macOS (using Homebrew)
   brew install minipro
   
   # Linux
   sudo apt-get install minipro
   
   # Or build from source: https://gitlab.com/DavidGriffith/minipro
   ```

### Building the Firmware

1. **Navigate to the project directory:**
   ```bash
   cd "Firmware/AB Controller"
   ```

2. **Build the firmware:**
   ```bash
   # Build for ATMega1284P (default)
   pio run -e atmega1284p
   
   # Or build for ATMega1284
   pio run -e atmega1284
   ```

3. **Build output:**
   The compiled firmware will be located at:
   ```
   .pio/build/atmega1284p/firmware.hex
   ```

### Uploading the Firmware

The project uses a MiniPro TL866 programmer for uploading.

1. **Connect the MiniPro programmer** to your ATMega1284P chip

2. **Upload firmware and fuses:**
   ```bash
   # Upload to ATMega1284P
   pio run -e atmega1284p -t upload
   
   # Or upload to ATMega1284
   pio run -e atmega1284 -t upload
   ```

3. **Manual upload (if needed):**
   ```bash
   # Flash the program
   minipro -p "ATMEGA1284P@DIP40" -c code -w .pio/build/atmega1284p/firmware.hex
   
   # Flash the fuses
   minipro -p "ATMEGA1284P@DIP40" -c config -w fuses.cfg --fuses
   ```

## Fuse Configuration

The `fuses.cfg` file contains the ATMega1284P fuse settings:

```properties
lfuse = 0xe0   # Low fuse
hfuse = 0xff   # High fuse  
efuse = 0xff   # Extended fuse
lock = 0xff    # Lock bits (unprogrammed, not written)
```

**Fuse Settings:**
- **Low Fuse (0xE0)**: External clock source (16 MHz full-can oscillator on
  XTAL1), slowly-rising-power start-up, no clock divide (CKDIV8 off), clock
  output disabled
- **High Fuse (0xFF)**: Default settings
- **Extended Fuse (0xFF)**: Default settings
- **Lock Bits (0xFF)**: No memory lock protection

> **Note**: The low fuse selects the *external clock* source, which is required
> for a full-can oscillator module driving XTAL1. Do not use a crystal-oscillator
> fuse setting with this hardware. The sibling boards — COB's `KEH Controller`
> and VCS's `IB Controller` — carry an HC49-U crystal across XTAL1/XTAL2 instead
> and therefore use the low power crystal setting (`lfuse = 0xFF`); the two are
> not interchangeable.

> **Note**: Lock bits are left unprogrammed on all of these boards. The upload
> command writes fuses only (`--fuses`, no `--lock`), so the `lock` line above is
> recorded for reference and never programmed.

⚠️ **Warning**: Incorrect fuse settings can brick your microcontroller. Verify fuse values are appropriate for your hardware configuration before programming.

## Dependencies

The firmware requires the following library (automatically installed by PlatformIO):

- **CircularBuffer** (v1.4.0+) by Roberto Lo Giacco
  - Provides interrupt-safe circular buffers for keyboard data

## Project Structure

```
AB Controller/
├── platformio.ini          # PlatformIO configuration
├── fuses.cfg              # AVR fuse configuration
├── src/
│   └── main.cpp           # Main firmware source code
├── include/               # Header files (if any)
├── lib/                   # Local libraries
└── test/                  # Unit tests
```

## Troubleshooting

### Build Issues

**Problem**: PlatformIO not found
```bash
# Solution: Install or update PlatformIO
pip install -U platformio
```

**Problem**: Library dependency errors
```bash
# Solution: Clean and rebuild
pio run -t clean
pio run
```

### Upload Issues

**Problem**: MiniPro not found
```bash
# Solution: Ensure minipro is installed and in PATH
which minipro
```

**Problem**: Chip not detected
- Check that the chip is properly seated in the programmer
- Verify you're using the correct chip model (ATMEGA1284P vs ATMEGA1284)
- Check for proper power supply to the programmer

### Runtime Issues

**Problem**: No keyboard response
- Verify enable signals (CA2/CB2) are at correct logic levels
- Check PS/2 clock and data connections
- Verify matrix keyboard connections
- Ensure VIA interface connections are correct

**Problem**: `JOY(1)`/`JOY(2)` return keystrokes or a stuck value
- Confirm the BIOS is v1.5 or later — older BIOS reads the port before the
  encoder has released it (see [Joystick Interface](#joystick-interface))
- Verify the on-board 1kΩ pull-ups are fitted (`R6`–`R13` for PORT A / `J6`,
  `R14`–`R21` for PORT B / `J8`)

**Problem**: Incorrect characters output
- Check for proper pull-up resistors on PS/2 lines
- Verify keyboard matrix wiring matches the defined layout
- Test with a known-good PS/2 keyboard

## License

See the main repository LICENSE file for licensing information.

## Contributing

This firmware is part of the 6502 computer project. Contributions and improvements are welcome through the main repository.

