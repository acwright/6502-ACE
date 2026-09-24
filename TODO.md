# TODO

## Rev 1.1: shared lines that a push-pull output can hold high

The 65C02's `IRQB`, `NMIB` and `RESB` lines are each shared by several devices,
and each device may only pull its line low. A device that also drives its line
high fights every other device on that line. When one of the others pulls low,
the line settles at a voltage the 65C02 still reads as high, so the signal never
arrives.

### 1. Pico9918 `/INT` to `IRQB`: add a diode (required)

**Change:** fit a Schottky diode (BAT85) between U3 pin 16 (`/INT`) and the
`IRQB` net, with the cathode toward U3 and the anode on `IRQB`.

**Why:** the Pico9918 drives `/INT` push-pull at 5 V, both high and low. On the
v1.3 and the PRO v2.0, the RP2040/RP2350's GPIO 22 feeds a 74AHC126 buffer (U9 on
the card), and the buffer's output enable is tied to the card's `RST` input. The
buffer therefore drives `/INT` whenever the 6502 is out of reset, and no firmware
can make it open-drain. The stock firmware and PICOVDP both hold `/INT` high when
no interrupt is pending.

The VIA (U2, W65C22N), the ACIA (U4, R6551) and the clock (U18, DS1511Y) all pull
`IRQB` low with open-drain outputs, so each one fights the Pico9918's buffer.
With a pico9918 PRO fitted, `IRQB` measured 3.8 V while the VIA was asserting.
That is above the W65C02S's input-high threshold of 0.7 × VDD (about 3.5 V), so
the 65C02 never took the interrupt and the VIA's flag was never cleared. The
keyboard and serial input were both dead, even with video disabled by the DIP
switch. A pico9918 v1.3 has the same circuit and happened to work, so the v1.3
was only ever working by luck.

**Tested:** on Rev 1.0, 2026-09-24. A socket stack under the PRO with pin 16
routed through a BAT85 fixed the keyboard and serial input on BIOS 1.6 and
BIOS 2.0.

**What the diode costs:** the Pico9918 can still pull `IRQB` low, to about
0.4 V through the diode, which is well below the 65C02's input-low threshold.
Neither BIOS 1.x nor BIOS 2.x uses the VDP's interrupt: BIOS 1.x leaves it
disabled, and BIOS 2.x's `WaitVBlank` polls the status register instead. A
program that does enable VDP interrupts would also need an IRQ handler that
reads the VDP's status register, because the Kernal's `Irq` does not.

### 2. ATmega `RESB` output: add a pull-up, and drive PC7 open-drain (decided)

**Board change:** add a 10 k pull-up from the `RESB` net to 5 V. No diode.
Rev 1.1 gets it on the board; the Rev 1.0 on the bench gets it as a bodge on
the underside.

**Firmware change (done 2026-09-24, `assertRESB` and `releaseRESB` in
`Firmware/AB Controller/src/main.cpp`):** in the AB Controller, drive PC7
(U6 pin 29) open-drain.
To assert reset, make PC7 an output and write it low. To release reset, make
PC7 an input with its internal pull-up on (`INPUT_PULLUP`). Nothing in the
firmware may write PC7 high while it is an output. This applies to power-on
(`setup()`) and to the reset button (`loop()`).

The internal pull-up (20–50 k) raises `RESB` on its own, so the new firmware
also works on a Rev 1.0 board without the bodge, and the firmware and the
resistor can go in in either order. The external 10 k is a stiffer pull-up than
the internal one, which is worth having on a reset line that runs out to the
`CART` and `BUS` connectors. It is recommended on Rev 1.1 and optional as a
bodge on Rev 1.0. (The ATmega is never programmed in circuit on this board.
During its own start-up, before `setup()` runs, `RESB` has no pull-up unless
the 10 k is fitted, but `setup()` then holds `RESB` low for 250 ms, so the 6502
still gets a clean reset either way.)

**Why:** today the firmware drives `RESB` push-pull. It sets PC7 as an output,
writes it low to hold the 6502 in reset, and writes it high to release it. The
DS1511Y's `RST` output (U18 pin 4) is open-drain on the same net, as is
anything on the `CART` (J18) and `BUS` (J19) connectors that pulls reset. While
the ATmega holds `RESB` high, none of them can reset the machine. The DS1511Y
asserts `RST` on a power failure and when its watchdog times out.

**Why the pull-up:** `RESB` has no pull-up today; the ATmega is the only thing
holding it high. Once PC7 only ever pulls low, something else has to raise the
line: the ATmega's internal pull-up, and on Rev 1.1 the 10 k as well.

**Why not a diode:** a diode on PC7 would also work, but the firmware change
does the same job with one part fewer.

### 3. ATmega `NMIB` output: firmware only, no board change

`NMIB` already has a pull-up (R2). In the default firmware build, PD7 is left as
an input and never drives `NMIB`. With `ENABLE_SQW` defined, the firmware makes
PD7 an output and holds it high between jiffy-clock pulses, which would stop a
cartridge or bus card from ever raising an NMI. Before enabling that option,
change the pulse to open-drain: switch PD7 to an output driven low to assert,
and back to an input to release.

### 4. Cards on the `CART` and `BUS` connectors

J18 and J19 carry `IRQB`, `NMIB` and `RESB`. Anything plugged into them must
only pull those lines low. In particular, a video card built around a pico9918
has the same `/INT` problem as U3, and needs the same diode on the card.
