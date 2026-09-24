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

## Rev 1.1: running at 2 MHz

Found on 2026-09-24, while 6502-PICOVDP's Phase 14 tested its first release in
this Rev 1.0 board (`docs/results/phase-14.md` in that repository, "Found on
the way"). With J1 (PHI2 SELECT) at 1 MHz none of this happened. None of it
involves the video card: at 2 MHz the card passed a bus test of 500 passes,
over 7 million accesses a run with none wrong. Find the causes before Rev 1.1
is fixed, in case one of them needs a board change, such as a chip select's
timing.

### 5. The SID and the CompactFlash card are not always found at 2 MHz

**Symptom:** at 1 MHz the Kernal finds every card (`HW_PRESENT`, `$030D`,
reads `$FD`), except that the SID was missed once in about a dozen boots. At
2 MHz, under BIOS 1.6 and BIOS 2.0 alike, some boots found neither the SID nor
the CF card (`$B5`, and BIOS 2.0's header reads `RAM RTC SER VIA VDP`), and
others found both.

**To check:**

- Which SID is fitted. A 6581 or 8580 is rated for a 1 MHz bus; an ARMSID or
  similar may not care.
- Whether the CF card works at 2 MHz once booted (`LOAD "NAME.PRG"`), or only
  its probe fails.
- Whether either probe depends on timing: a delay or timeout counted in CPU
  cycles is half as long at 2 MHz.
- The SID's and the CF card's chip selects against PHI2 at 2 MHz, on a scope.

### 6. Serial input replays old input under BIOS 1.6 at 2 MHz

**Symptom:** after an XMODEM `LOAD`, or after a program had run, BASIC ran
again lines that had been typed seconds or minutes before. Twice the replayed
line was an old `LOAD`, and the machine waited in it. BIOS 1.6 keeps its serial
input ring at `$0200`–`$02FF` with the read pointer at `$00` and the write
pointer at `$01`. The replays ran from 5 to about 230 bytes long, so the read
pointer was taking a wrong value. The ring survives a reset, so a replay can
bring back input from before one. The boot text sent over serial was also
garbled at 2 MHz with the video card switched off by its DIP switch.

**What is known:**

- It happened only at 2 MHz under BIOS 1.6: never at 1 MHz under either BIOS,
  and never under BIOS 2.0 at 2 MHz in a full test run.
- The emulator, running BIOS 1.6 with the same XMODEM stream at 2 MHz byte
  spacing, did not do it in 20 tries. The emulator does not model the ACIA's
  transmit time or the bus's timing.
- Pulling and refitting the R6551AP (date code 9922) stopped it for 12 tries,
  and then it came back.
- An R65C51P2 (date code 8706) fitted in its place received nothing at all,
  at 2 MHz, with the video card on or off.

**Suspects:**

- The ACIA holding the data bus too long after a read. The Kernal reads the
  ring's pointers a few cycles after `lda SC_DATA`, so a late release by the
  ACIA would corrupt exactly those reads.
- The ACIA's socket.
- A race in BIOS 1.6's serial code that BIOS 2.0 does not have.

**To check:**

- Put the ACIA's chip select, PHI2 and a data line on a scope at 2 MHz, and
  measure when the ACIA lets go of the bus after a read.
- Try another 2 MHz-rated R6551AP. A W65C51N has its own transmit bug (TDRE is
  always set), so it is not a like-for-like test.
- If the ACIA's timing is marginal at 2 MHz, BIOS 2.0 may only be missing it by
  luck, so settle the timing before relying on 2.0.

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
    build has no USB of its own, so every update needs BOOT again. Say whether
    it may be flashed in the ACE's socket, and whether USB-C and BOOT can be
    reached with the ACE in its case: neither was recorded.
  - Burn BIOS 2.0 to U8. The ACE tested ran `v2.0.2` (SHA-256 `7a71252d…`).
  - The first boot shows the AC6502 logo, then `AC6502 BIOS v2.0`,
    `BASIC v2.0 30718 BYTES FREE` and `RAM RTC CF SER VIA SID VDP`. `VDP`
    missing from that line means the card isn't running 6502-PICOVDP.
  - The builder's check for the `MDE1` pin, from BASIC 2.0:
    `POKE 39939,4:POKE 39939,142:PRINT PEEK(39939):POKE 39939,0:POKE 39939,142`
    prints 172.
- **The /INT diode** (item 1 above) belongs in the assembly notes as well.
