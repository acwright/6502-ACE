# TODO

## Rev 1.1: shared lines that a push-pull output can hold high

The 65C02's `IRQB`, `NMIB` and `RESB` lines are each shared by several devices,
and each device may only pull its line low. A device that also drives its line
high fights every other device on that line. When one of the others pulls low,
the line settles at a voltage the 65C02 still reads as high, so the signal never
arrives.

### 1. Pico9918 `/INT` to `IRQB`: add a diode (required)

**In the Rev 1.1 schematic, 2026-09-24:** D4, a BAT85, from U3 pin 16 to
`IRQB`, cathode on U3. `Tests/check-schematics.mjs` fails if `/INT` ever
reaches `IRQB` another way. The Rev 1.1 PCB still has to be updated from the
schematic.

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

**In the Rev 1.1 schematic, 2026-09-24:** R35, 10 k from `RESB` to VCC,
beside R1–R4. `Tests/check-schematics.mjs` fails if `RESB` loses its pull-up.
The Rev 1.1 PCB still has to be updated from the schematic.

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

**Done 2026-09-24.** `NMIB` already has a pull-up (R2). In the default firmware
build, PD7 is left as an input and never drives `NMIB`. With `ENABLE_SQW`
defined, the firmware used to make PD7 an output and hold it high between
jiffy-clock pulses, which would stop a cartridge or bus card from ever raising
an NMI. The pulse is now open-drain: the jiffy ISR switches PD7 to an output
driven low to assert, and back to an input to release. PD7's output latch stays
low throughout.

The default build is byte-for-byte unchanged by this fix, so a board flashed
with the RESB change needs no reflash. The `ENABLE_SQW` build compiles, and its
disassembly shows the pulse as `sbi`/`cbi` on DDRD bit 7 with no write to PORTD,
but the jiffy clock has not been run on hardware.

### 4. Cards on the `CART` and `BUS` connectors

J18 and J19 carry `IRQB`, `NMIB` and `RESB`. Anything plugged into them must
only pull those lines low. In particular, a video card built around a pico9918
has the same `/INT` problem as U3, and needs the same diode on the card.

## The ACE runs at 1 MHz only (decided 2026-09-24)

At 2 MHz, 6502-PICOVDP's Phase 14 found the SID and the CompactFlash card
missing on some boots, and serial input under BIOS 1.6 replaying old lines
(`docs/results/phase-14.md` in that repository, "Found on the way"). The first
two are explained below. The third is not, and a fault that cannot be found
cannot be patched on the Rev 1.0 boards, so the ACE runs at 1 MHz only.

- **Rev 1.1:** J1 (PHI2 SELECT) is gone from the schematic, and U5's 1 MHz
  output (Q3, pin 11) drives PHI2 for the 65C02, VIA, ACIA, SID and the
  `CART` and `BUS` connectors. Q2 is unconnected. `Tests/check-schematics.mjs`
  fails if any of the four chips is clocked from anything else.
- **Rev 1.0:** J1 stays on its 1 MHz pins, 1 and 2.

### 5. The SID at 2 MHz (explained)

The SID's clock (U9 pin 6) was always U5's 1 MHz output, not the jumper, and
its chip select (IO7B) is decoded from the address alone. At 2 MHz the SID's
clock is high for all of one CPU cycle and low for all of the next, so only
every other CPU cycle can reach it: a write in the other cycle is lost, and a
read there returns whatever the bus last held. The Kernal's `ProbeSID` makes its
three setup writes and its read of `SID_OSC3` 1,285 cycles apart, an odd number,
so at 2 MHz either the writes or the read miss. Which one depends on where reset
lands against the 1 MHz clock, which changes from boot to boot. A boot that
"found" the SID found it by accident: the read missed and returned `$98`, the
high byte of `SID_OSC3`'s address still on the bus, which is neither `$00` nor
`$FF`. Reproduced with the emulator's CPU and this clocking added to it: BIOS
1.6 and 2.0.2 both boot with `HW_PRESENT` `$FF` on one parity and `$BF` on the
other. It was never only the probe: at 2 MHz half of every program's SID
accesses miss.

**Still open:** at 1 MHz the SID (an ARMSID) was missed once in about a dozen
boots. The 2 MHz fault does not explain that.

### 6. The CompactFlash card at 2 MHz (explained)

`StWaitReadyPoll` waits for the card to leave `BSY` with a loop counted in CPU
cycles: about 851 ms after reset at 1 MHz and 425 ms at 2 MHz, the same in BIOS
1.6 and 2.0.2. The card's `/RESET` is `RESB`, so it starts initialising at the
same moment the 65C02 does. A card that needs between 425 and 851 ms is found at
1 MHz and missed at 2 MHz. The bus timing itself is within PIO mode 0 at both
speeds.

**At 1 MHz:** every boot in Phase 14 found the card, but the loop is still
counted in cycles, and on the boots missed at 2 MHz the card needed more than
425 ms, so the margin at 1 MHz is not known. A slower card could still be
missed. The BIOS fix, a probe that waits a fixed time, is written up in
6502-BIOS `TODO.md` item 1 for the next BIOS update. So is a fault in the SID
probe that item 5 turned up: an empty SID socket reads as a SID (item 2 there).

### 7. Serial input replayed old lines under BIOS 1.6 at 2 MHz (not explained, dropped)

After an XMODEM `LOAD`, or after a program had run, BASIC ran again lines typed
seconds or minutes before. The replayed bytes were the oldest in the input ring,
the ones just ahead of the write pointer, so a pointer jumped forward. The boot
text sent over serial was also garbled at 2 MHz. What was ruled out:

- **A race in BIOS 1.6's serial code:** `Irq`, `ReadBuffer`, `WriteBuffer`,
  `ScRts`, `ScRxPoll` and `SerialChrout` are the same in 1.6 and 2.0.2, and both
  keep the ring's pointers at `$00` and `$01`.
- **The ACIA holding the data bus after a read:** the nearest read of a pointer
  after any `lda SC_DATA` is at least 12 cycles later, and the cycles between are
  instruction fetches, which would crash the machine first.
- **The board's timing:** RAM `/OE` and `/WE` are qualified by PHI2, and every
  setup and hold time on the bus is measured from a PHI2 edge, so none of them
  change with the clock rate.
- **The test programs:** `bus.asm`, `probe.asm` and `graphics-1.asm` do not
  touch `$00` or `$01`.

Two things were left: the R6551AP runs at exactly its 500 ns minimum cycle time
at 2 MHz, and reseating it stopped the replays for a while. The runs also were
not matched (`graphics-1.asm` ran only under 1.6, and 1.6 at 1 MHz got 64
bus-test passes against 500 elsewhere), so "only under 1.6" is weaker evidence
than it looks. None of this matters at 1 MHz.

### 8. The emulator's 2 MHz setting (done)

6502-EMULATOR 3.5.0, released 2026-09-24, runs at 1 MHz only: the toolbar
button and the saved setting are gone, and `--freq 2` is refused. 6502-DOCS
pins 3.5.0 and no longer offers 2 MHz, in either edition (its ACCURACY A77).

## The bank register's address decode (third revision, 2026-09-24)

**The fault:** in Rev 1.0, in Rev 1.1 as drawn, and with the first ACE RAM Patch
fitted, U12B combined `/(A9·A8)` from U12A and `/(A0–A7)` from U17 with a NAND.
A NAND of two active-low signals is the OR of the two conditions, so each bank
latch loaded on 259 addresses instead of one: every write to `$8300`–`$83FF`,
`$80FF`, `$81FF` and `$82FF` for the low latch, and the same in the `$8400`
window for the high one. A write to the top 255 bytes of a bank's window
changed the bank. The BIOS's RAM probe uses offset 0, so it never noticed. The
first patch fixed a different fault in the same path (the latches pulsed
whenever the bus was idle) and took U12B's output as given.

**Rev 1.1 (done in the schematic):** a spare NOR in U23 (U23C, pins 8, 9 and 10)
takes U12A's output and U17's, and drives U13 pins 1 and 4 in U12B's place.
U12B is unused, with its inputs on ground.

**ACE RAM Patch Rev 1.1 (done in the schematic):** a correct latch needs A8, A9
and U17's output, and none of them reach U13's socket. The new patch therefore
plugs into both sockets, J1 into U12's and J2 into U13's, and replaces both
74HC00s with the same logic as the Rev 1.1 board (a 74HC00 and a 74HC02, as
before). On the Rev 1.0 board both sockets face the same way, and U13's pin 1 is
23.00 mm from U12's along the row. U15 (the banked RAM) sits directly above
both sockets, as it does above U13 for the first patch, and C26 and C27 are
beside them.

**The check:** `Tests/check-schematics.mjs` evaluates both boards' decode from
their netlists, in all 524,288 bus states, against the memory map (README,
"Checking the schematics"). It fails on the Rev 1.0 board alone, on Rev 1.0
with the first patch, and on Rev 1.1 as it was, and passes on both boards now.

**Still to do:**

- Lay out the patch's PCB: add J2 23.00 mm from J1, in the same orientation, and
  route it. Order it.
- Update the Rev 1.1 PCB from the schematic: J1 removed, D4 and R35 added, and
  U12B's and U23C's pins swapped.
- On the bench board: remove the hand bodge, pull the 74HC00s from U12 and U13,
  and fit the new patch.
- Then check the high window. Phase 14's boots read `HW_PRESENT` as `$FD` even at
  1 MHz, which means the Kernal's probe did not find the `$8400` window (bit 1).
  With the new patch fitted and SW70 switch 2 on, a boot should read `$FF`.

## README: the video card and BIOS 2.0

The README still describes a Pico9918 running TMS9918A firmware and BIOS 1.x.
Everything it needs is now proven (6502-PICOVDP `docs/results/phase-14.md`,
"For 6502-ACE"):

- **Software table:** add [6502-PICOVDP](https://github.com/acwright/6502-PICOVDP),
  "Firmware for the ACE's video card, on a PICO9918 PRO v2.0". The BIOS is the
  Kernal, BASIC and Wozmon; BIOS 2.x has no Monitor.
- **Specs line and BOM U3:** PICO9918 PRO v2.0 (RP2354A) running 6502-PICOVDP,
  with one 0.1″ header pin soldered into its `MDE1` pad; RP2040 PICO9918 boards
  (v1.x) cannot run it. The silkscreen and `Production/…/bom.csv` still read
  `Pico9918A`, and stay that way until a new revision.
- **A Firmware section, video card first:**
  - Flash the PRO with `picovdp-v1.0.0.uf2` from
    https://github.com/acwright/6502-PICOVDP/releases/tag/v1.0.0 (SHA-256
    `0b74cd9875cbffc46de7ec48a9bb6e0d4a76a3e796d2563615e17e6bed94afd5`): hold BOOT,
    connect USB-C, `picotool load -v -x -f picovdp-v1.0.0.uf2`. The release
    build has no USB of its own, so every update needs BOOT again. It may be
    flashed in the ACE's socket with the ACE switched off; that is how the
    tested card was flashed.
  - Optionally, back up the stock firmware first, from BOOTSEL:
    `picotool save -a stock.bin`. To restore it, `picotool load -v -x stock.bin`.
    The backup was made; the restore is picotool's ordinary load and has not
    been tried on a PRO.
  - Burn BIOS 2.0 to U8. The ACE tested ran `v2.0.2` (SHA-256 `7a71252d…`).
  - The first boot shows the AC6502 logo, then `AC6502 BIOS v2.0`,
    `BASIC v2.0 30718 BYTES FREE` and `RAM RTC CF SER VIA SID VDP`, at
    power-on and after the reset button (SW17). `VDP` missing from that line
    means the card isn't running 6502-PICOVDP.
  - The builder's check for the `MDE1` pin, from BASIC 2.0:
    `POKE 39939,4:POKE 39939,142:PRINT PEEK(39939):POKE 39939,0:POKE 39939,142`
    prints 172.
- **The /INT diode** (item 1 above) belongs in the assembly notes as well.
