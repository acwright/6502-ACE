# Bill of materials: 6502-ACE

Every part for every board in this repository, by revision, with supplier numbers.

## How to use this

1. **Find your board and revision** in [Which revision do I have?](#which-revision-do-i-have)
2. **Read the [known issues](#known-issues)** for that revision, because they change what you buy or fit.
3. **Order from the table for your revision.** Each revision links to files you can upload to Digi-Key and Mouser. Those files are for one board, so multiply the quantities if you're building more. If a site asks which column is which, the first column is its part number and the third is the quantity. A cart only holds what that supplier sells, so check the table for anything else, such as chips from Jameco.
4. **Set the jumpers** before the first power-up. The README's [Jumpers](README.md#jumpers) section says which ones each board needs, and the table for your revision lists the shunts.

**Pre-soldered parts.** Some boards on Tindie come with their surface-mount parts already soldered. Parts marked **Yes** under Pre-soldered are the ones soldered on those boards. Check your listing, because others are sold as a bare PCB. Each revision that has such parts also has a `through-hole` cart that leaves them out. To solder a bare board yourself, use the full cart.

**Suppliers.** Every part has one set of numbers, so the same resistor is the same order line on every board. The numbers were read from Digi-Key and Mouser on 2026-11-04, and stock changes. A blank supplier cell means that supplier doesn't sell the part, or only sells it in bulk.

**The `bom.csv` files** under `Production/` are for JLCPCB assembly. They list the same parts. A blank LCSC cell there means JLCPCB doesn't place that part, and JLCPCB's "missing parts" warning about it is expected.

## Which revision do I have?

Look on the board: the silk prints the revision next to the copyright line. [REVISIONS.md](REVISIONS.md) has the facts for each one, and its history lists what changed between them.

**To make a new board, make the newest revision**, and check its label first. The README's [Which revision to make](README.md#which-revision-to-make) explains the three labels: **Tested**, **Proven design** and **Untested**.

| Board | Revision | What the silk says | Status | Label |
|---|---|---|---|---|
| [ACE Board](#ace-board) | 1.0 | Rev 1.0 | Made, tested | **Tested** |
| [ACE Board](#ace-board) | 1.1 | Rev 1.1 | Drawn, not made yet | **Proven design**: each change is a circuit already tested on a Rev 1.0: the ACE RAM Patch 1.1's bank-latch decode and the video card's `/INT` diode, both run on the bench, and the ACIA's crystal jumpers, which ship open. The audio jack's pins are put right, `SOB` is tied high, the pull-ups are 10k, and the tracks are rerouted, with the decode check passing. The DS1501 option at U18, with its crystal `Y2`, is untested, and so are the 10k pull-ups on the PS/2 lines, a textbook circuit |
| [ACE CF Adapter](#ace-cf-adapter) | 1.0 | Rev 1.0 | Made, tested | **Tested** |
| [ACE CF Adapter](#ace-cf-adapter) | 1.1 | Rev 1.1 | Drawn, not made yet | **Proven design**: the same circuit as the tested Rev 1.0, renumbered and in surface-mount parts for JLCPCB assembly. The new LCSC socket fits the same footprint, but no board has been built with it yet |
| [ACE RAM Patch](#ace-ram-patch) | 1.0 | Rev 1.0 | Made. Failed: Rev 1.1 replaces it | **Tested**: built and tested: its decode is wrong, and Rev 1.1 replaces it |
| [ACE RAM Patch](#ace-ram-patch) | 1.1 | Rev 1.1 | Made. Yes, 2026-11-03 | **Tested**: built and tested on an ACE Board Rev 1.0, 2026-11-03 |
| [ACE SD Adapter Bottom](#ace-sd-adapter-bottom) | 1.1 | Rev 1.1 | Drawn, not made yet | **Untested**: a new board: an SD card the stock BIOS takes for CompactFlash, with a built-in drive; the ACE SD Adapter Top, stacked on it, carries the SD card socket. Not yet made |
| [ACE SD Adapter Top](#ace-sd-adapter-top) | 1.1 | Rev 1.1 | Drawn, not made yet | **Untested**: the ACE SD Adapter Bottom's top board: the SD card socket, the LEDs and the SD card's 3.3 V regulator, stacked on the Bottom. Not yet made |

## Known issues

These change what you buy or fit. The boards themselves stay as they were made.

| Board | Revision | Parts | Issue |
|---|---|---|---|
| ACE Board | 1.0 | R1–R5, R27 | Fit 10k, not the 1k in the original files. See the build notes. |
| ACE Board | 1.0 | J5 | `VDD` is the supply for a real SID at pin 28: 12 V for a 6581, 9 V for an 8580. The standard build does not provide it, and it has never been tested. Leave it unconnected with an ARMSID. |
| ACE Board | 1.0 | U7 | The silk says AS6C62256; fit the Hitachi HM62256LP-70 listed here, from Jameco. The Alliance AS6C62256 that this parts list ordered until 2026-11-28 has misread on the family's machines, now and then returning a byte with one bit wrong, so that programs crash or misbehave; the Hitachi hasn't, in testing on the ACE and the KIM. |
| ACE Board | 1.0 | U9 | The silk says 6581; fit an ARMSID. |
| ACE Board | 1.0 | U4 | The silk says 65C51; fit an R6551AP. |
| ACE Board | 1.0 | BT1 | `BAT-HLD-001-THM`, on the tested boards, is obsolete. `BAT-HLD-001-THM-TR` is its listed continuation, with no stock today and no board built with it yet. |
| ACE Board | 1.1 | BT1 | `BAT-HLD-001-THM`, on the tested boards, is obsolete. `BAT-HLD-001-THM-TR` is its listed continuation, with no stock today and no board built with it yet. |
| ACE RAM Patch | 1.0 |  | Boards were made, and testing showed the decode is wrong. Do not fit one: use Rev 1.1. |

### Build notes

How to build each board, where it needs more than its parts list.

<!-- Build notes: hand-written. Tools/bom/gen_bom.py keeps everything between these two markers. -->

**ACE Board**

**J11 (AUDIO L) and J14 (AUDIO R), the two RCA jacks, are wired together:** both carry the SID's one output, the same signal, so a stereo amplifier's two inputs each get the sound. Either jack alone gives all of it, so a builder can fit just one and leave the other off to save its cost; each jack's parts-list row is the whole of that part. This holds on Rev 1.0 and Rev 1.1, and on Rev 1.0 whether or not change 9 is made.

**RTC:** U18 takes a DS1511Y+, the part every ACE has been tested with. Any revision also takes the [RTC Adapter](https://github.com/acwright/6502-COB#adapters) in its place, a DS1501 and its crystal on a plug, for less; its build notes are in 6502-COB. Rev 1.1 also takes a DS1501YN+ there: the DS1511Y is a DS1501 with its crystal and a lithium cell built in, and Rev 1.1 has the crystal on the board (`Y2`). A Rev 1.0 has no crystal, so it takes the DS1511Y or the adapter. The DS1501 option and the adapter are untested. With the adapter or a DS1501:
- **Keep the CR2032 fitted** (`BT1`). It is the DS1501's only backup, so taking it out loses the time and the NVRAM. A DS1511Y has its own cell as well.
- **Use BIOS 1.8 or 2.2.0 or later.** A new DS1501 may start with its Crystal Select bit set, and then it runs slow on the 6 pF crystal; the BIOS clears the bit at every boot from those releases on ([6502-BIOS #4](https://github.com/acwright/6502-BIOS/issues/4)).
- **The DS1501YN+ is not for new designs** (NRND). Digi-Key lists it (2026-11-20); Mouser doesn't.

**Power:** use a centre-positive 5 V supply only, on either revision. Nothing on the board protects it from a reversed supply: the barrel jack goes straight to the power switch, so `VCC` gets the supply's full 5 V.

**Building a Rev 1.0**

Rev 1.0 is the board on sale. Rev 1.1 fixes each of these on the board; on a Rev 1.0 they're done by hand. The [build notes](Docs/ACE%20Board/Rev%201.0/ACE%20Board%20Build%20Notes.pdf) have each step, with figures and checks. Every step below is done and tested on the owner's Rev 1.0, the optional SID wire (the build notes' change 8) included, except the optional audio-jack change (change 9), which hasn't been tried on a board yet, and the optional RAM change (change 10), whose circuit is tested but whose cuts and wires haven't been done on a board yet.

- **Pull-ups:** fit 10kΩ for `R1`–`R5` and `R27`, not the 1kΩ in Rev 1.0's BOM. Don't leave out `R1`: it is the only thing holding `SOB` (U1 pin 38) high.
- **ACIA:** fit an R6551AP at `U4`, where Rev 1.0's silkscreen and BOM say 65C51.
- **Supply capacitor:** fit a 10µF electrolytic on the underside, across the pads of `J19`, the VCC header. Rev 1.0 has no holes for it.
- **`RESB`:** flash the AB Controller firmware from this repository, which only ever pulls `RESB` low (see [AB Controller](README.md#ab-controller)); older firmware drove it high as well, so nothing else could reset the machine. A 10kΩ pull-up from `RESB` to 5 V, soldered on the underside, is optional: the ATmega's internal pull-up raises the line on its own, but the 10 k is stiffer on a line that runs out to `CART` and `BUS`.
- **PS/2 pull-ups:** nothing to do with the AB Controller firmware from this repository, which ignores the false clock edges they guard against (see [AB Controller](README.md#ab-controller)). Rev 1.1 adds `R39` and `R40`, 10kΩ from `PS2CLK` and `PS2DATA` to VCC, so few spikes reach the lines at all. To add them anyway, solder a 10kΩ on the underside across J13's pins 5 and 4 (`PS2CLK` to VCC) and another across pins 1 and 4 (`PS2DATA` to VCC), the same circuit; untried.
- **Video card `/INT`:** fit a BAT85 between U3 pin 16 and `IRQB`, cathode toward the card, in a socket stack under the card with pin 16 routed through the diode. Without it, a PICO9918 PRO holds `IRQB` at 3.8 V while the VIA asserts it, and the keyboard and serial input are dead. A v1.3 has the same circuit and only works by luck.
- **Clock:** keep the PHI2 SELECT jumper (J1) on its 1 MHz pins, 1 and 2. Rev 1.0's SID stays on U5's 1 MHz output whatever J1 says, so at 2 MHz it answers only every other access; Rev 1.1 puts it on J1's clock. To do the same on a Rev 1.0, optionally, cut one track and fit one wire: change 8 in the [build notes](Docs/ACE%20Board/Rev%201.0/ACE%20Board%20Build%20Notes.pdf) has both, with figures. Tested at 2 MHz with an ARMSID (2026-11-21): the SID is found and plays, an octave higher than at 1 MHz, as a SID's pitch follows its clock. Rev 1.1's U14 is a 74HCT00, which matters only at 2 MHz: a builder who runs a Rev 1.0 at 2 MHz, at their own risk, can fit one in U14's socket.
- **Banked RAM:** fit the [ACE RAM Patch](README.md#ace-ram-patch) Rev 1.1 in place of U12 and U13.
- **RAM output enable (optional):** U7's output enable, pin 22, is `RB`, so the AS6C62256 lets go of the data bus as `PHI2` falls, and under a heavy load (the 1 MB Flash Cart, or 2 MHz) with more than 5.0 V at the board the CPU can read a wrong byte (see [Known issues](#known-issues)). Rev 1.1 takes pin 22 from the inverted `RWB`. To do the same on a Rev 1.0, cut the `RB` track on both sides of U7 pin 22 on the underside, wire U18 pin 22 to U8 pin 22 so the RTC, ROM, banked RAM and CF stay on `RB`, and wire U7 pin 22 to U14 pin 6: change 10 in the [build notes](Docs/ACE%20Board/Rev%201.0/ACE%20Board%20Build%20Notes.pdf) has the cuts, the wires and the meter checks, with figures. The circuit is tested on the owner's Rev 1.0 (2026-11-21 to 2026-11-23) with U7's pin 22 bent out and wired to U14 pin 6; the cuts and wires haven't been done on a board yet. Not needed with a Hitachi HM62256LP-70 at U7.

Rev 1.1's other changes need nothing on a built board, or can't be made on one:
- **The ACIA's crystal jumpers can't be added.** Rev 1.1's R38, C32, JP1 and JP2 let an R65C51P or a W65C51 run; a Rev 1.0 has no pads for them, so fit the R6551AP, which needs none.
- **A bare DS1501 can't be fitted at U18.** Rev 1.1 adds its crystal, `Y2`; a Rev 1.0 has no pads for it, so fit the DS1511Y or the RTC Adapter.
- **Leave J5, the `VDD` header, empty.** It is only for a real SID's 12 V supply; the ARMSID needs nothing at U9 pin 28, and Rev 1.1 drops the header.
- **The audio jacks are wired the wrong way round.** J11 and J14 carry the SID's signal on their sleeve and ground on their tip; Rev 1.1 puts the signal on the tip. Sound still plays, since audio has no polarity, but the signal rides on the cable's shield, so if the amplifier also shares a ground with the ACE through another lead (a USB or serial cable to the same computer) expect hum or quieter sound. Change 9 in the [build notes](Docs/ACE%20Board/Rev%201.0/ACE%20Board%20Build%20Notes.pdf) rewires them, with one track cut, sixteen thermal spokes cut and two wires, before the jacks are fitted; it hasn't been tried on a board yet. Or leave them, and wire a jack on the case to J15, the `AUDIO` header, which is wired right (pin 1 the signal, pin 2 ground).
- **The silkscreen** names the parts Rev 1.1 fits (`R6551AP`, `ARMSID`, `ATmega1284` and the rest), and Rev 1.1 keeps Rev 1.0's designators, so these notes and Rev 1.0's silkscreen agree.

**ACE CF Adapter**

**Building a Rev 1.0:** nothing to do. Rev 1.1 renames the two connectors, `J21` to `J1` and `J3` to `J2`, because Rev 1.0's numbers came from another project; a Rev 1.0's parts list and silkscreen use its own numbers. Rev 1.1 moves the LED and resistors to surface-mount parts and gives every part but J1 an LCSC number, for a board JLCPCB assembles; the circuit is the same, so a Rev 1.0 takes the through-hole parts and the hand-soldered socket in its parts list. Its silkscreen changes need nothing.

**ACE RAM Patch**

**Building a Rev 1.0:** don't. Its decode is wrong: it still loads a bank latch on writes to `$8300`–`$83FE` and `$80FF`–`$82FF` (and the same in the `$8400` window), so a program's writes there change the bank. It can't be fixed on the board, because it plugs into U13's socket alone and the signals the fix needs never reach it. Fit a Rev 1.1, which takes the place of both U12 and U13.

<!-- End of build notes. -->

## ACE Board

### ACE Board Rev 1.1

Drawn, not made yet. **Proven design**: each change is a circuit already tested on a Rev 1.0: the ACE RAM Patch 1.1's bank-latch decode and the video card's `/INT` diode, both run on the bench, and the ACIA's crystal jumpers, which ship open. The audio jack's pins are put right, `SOB` is tied high, the pull-ups are 10k, and the tracks are rerouted, with the decode check passing. The DS1501 option at U18, with its crystal `Y2`, is untested, and so are the 10k pull-ups on the PS/2 lines, a textbook circuit.

Cart files: [digikey.csv](BOM/ACE%20Board/Rev%201.1/digikey.csv), [mouser.csv](BOM/ACE%20Board/Rev%201.1/mouser.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other |
|---|---|---|---|---|---|---|
| BT1 | 1 | CR2032 | TE Connectivity Linx BAT-HLD-001-THM-TR | [343-BAT-HLD-001-THM-TRCT-ND](https://www.digikey.com/en/products/filter?keywords=343-BAT-HLD-001-THM-TRCT-ND) |  |  |
| C1, C9–C30 | 23 | 100nF | KYOCERA AVX SR205C104KAR | [478-3187-ND](https://www.digikey.com/en/products/filter?keywords=478-3187-ND) | [581-SR205C104KAR](https://www.mouser.com/ProductDetail/581-SR205C104KAR) |  |
| C2, C3, C5, C6, C8 | 5 | 1uF | KYOCERA AVX SR205E105MAR | [478-7667-ND](https://www.digikey.com/en/products/filter?keywords=478-7667-ND) | [581-SR205E105MAR](https://www.mouser.com/ProductDetail/581-SR205E105MAR) |  |
| C4, C7 | 2 | 2.2nF | KYOCERA AVX SR155C222KAR | [478-11698-ND](https://www.digikey.com/en/products/filter?keywords=478-11698-ND) | [581-SR155C222KAR](https://www.mouser.com/ProductDetail/581-SR155C222KAR) |  |
| C31 | 1 | 10uF | Panasonic EEA-GA1C100 | [P14482-ND](https://www.digikey.com/en/products/filter?keywords=P14482-ND) | [667-EEA-GA1C100](https://www.mouser.com/ProductDetail/667-EEA-GA1C100) |  |
| C32 | 1 | 22pF | KYOCERA AVX SR151A220JAR | [478-4846-ND](https://www.digikey.com/en/products/filter?keywords=478-4846-ND) | [581-SR151A220JAR](https://www.mouser.com/ProductDetail/581-SR151A220JAR) |  |
| D1 | 1 | POWER LED | Würth Elektronik 151031VS06000 | [732-5008-ND](https://www.digikey.com/en/products/filter?keywords=732-5008-ND) | [710-151031VS06000](https://www.mouser.com/ProductDetail/710-151031VS06000) |  |
| D2–D4 | 3 | BAT85 | Vishay BAT85S-TR | [BAT85SCT-ND](https://www.digikey.com/en/products/filter?keywords=BAT85SCT-ND) | [78-BAT85S](https://www.mouser.com/ProductDetail/78-BAT85S) |  |
| J1 | 1 | PHI2 SELECT | Pin header 1×3, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J2 | 1 | CTS EN | Pin header 1×3, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J3 | 1 | RESET SW | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J4 | 1 | DCD EN | Pin header 1×3, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J6 | 1 | JOYSTICK A | Amphenol D09P33E4GX00LF | [609-1481-ND](https://www.digikey.com/en/products/filter?keywords=609-1481-ND) | [649-D09P33E4GX00LF](https://www.mouser.com/ProductDetail/649-D09P33E4GX00LF) |  |
| J7 | 1 | PADDLES | Pin header 1×4, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J8 | 1 | JOYSTICK B | Amphenol D09P33E4GX00LF | [609-1481-ND](https://www.digikey.com/en/products/filter?keywords=609-1481-ND) | [649-D09P33E4GX00LF](https://www.mouser.com/ProductDetail/649-D09P33E4GX00LF) |  |
| J9 | 1 | PORT B | Adam Tech BHR-12-VUA | [2057-BHR-12-VUA-ND](https://www.digikey.com/en/products/filter?keywords=2057-BHR-12-VUA-ND) | [737-BHR-12-VUA](https://www.mouser.com/ProductDetail/737-BHR-12-VUA) | 2057-BHR-12-VUA-ND |
| J10 | 1 | PORT A | Adam Tech BHR-12-VUA | [2057-BHR-12-VUA-ND](https://www.digikey.com/en/products/filter?keywords=2057-BHR-12-VUA-ND) | [737-BHR-12-VUA](https://www.mouser.com/ProductDetail/737-BHR-12-VUA) | 2057-BHR-12-VUA-ND |
| J11 | 1 | AUDIO L | Switchcraft Inc. PJRAN1X1U02X | [PJRAN1X1U02X-ND](https://www.digikey.com/en/products/filter?keywords=PJRAN1X1U02X-ND) | [502-PJRAN1X1U02X](https://www.mouser.com/ProductDetail/502-PJRAN1X1U02X) |  |
| J12 | 1 | SERIAL (DTE) | Amphenol D09P33E4GX00LF | [609-1481-ND](https://www.digikey.com/en/products/filter?keywords=609-1481-ND) | [649-D09P33E4GX00LF](https://www.mouser.com/ProductDetail/649-D09P33E4GX00LF) |  |
| J13 | 1 | PS/2 | Kycon, Inc. KMDGX-6S-BS | [2092-KMDGX-6S-BS-ND](https://www.digikey.com/en/products/filter?keywords=2092-KMDGX-6S-BS-ND) | [806-KMDGX-6S-BS](https://www.mouser.com/ProductDetail/806-KMDGX-6S-BS) |  |
| J14 | 1 | AUDIO R | Switchcraft Inc. PJRAN1X1U03X | [PJRAN1X1U03X-ND](https://www.digikey.com/en/products/filter?keywords=PJRAN1X1U03X-ND) | [502-PJRAN1X1U03X](https://www.mouser.com/ProductDetail/502-PJRAN1X1U03X) |  |
| J15 | 1 | AUDIO | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J16 | 1 | 5V DC | Same Sky PJ-102AH | [CP-102AH-ND](https://www.digikey.com/en/products/filter?keywords=CP-102AH-ND) | [490-PJ-102AH](https://www.mouser.com/ProductDetail/490-PJ-102AH) |  |
| J17 | 1 | CART | TE Connectivity 5-5530843-4 | [A31723-ND](https://www.digikey.com/en/products/filter?keywords=A31723-ND) | [571-5-5530843-4](https://www.mouser.com/ProductDetail/571-5-5530843-4) |  |
| J18 | 1 | BUS | Würth Elektronik 61204021621 | [732-5401-ND](https://www.digikey.com/en/products/filter?keywords=732-5401-ND) | [710-61204021621](https://www.mouser.com/ProductDetail/710-61204021621) |  |
| J19 | 1 | VCC | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J20 | 1 | POWER LED | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J21 | 1 | STORAGE | Sullins PPPC102LJBN-RC | [S5563-ND](https://www.digikey.com/en/products/filter?keywords=S5563-ND) |  |  |
| J22 | 1 | KEYBOARD | Adam Tech 2PH1-16-UA | [2057-2PH1-16-UA-ND](https://www.digikey.com/en/products/filter?keywords=2057-2PH1-16-UA-ND) | [737-2PH1-16-UA](https://www.mouser.com/ProductDetail/737-2PH1-16-UA) |  |
| R2–R5, R27, R37, R39, R40 | 8 | 10k | YAGEO MFR-12FTF52-10K | [13-MFR-12FTF52-10KCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-10KCT-ND) | [603-MFR-12FTF52-10K](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-10K) |  |
| R6–R14, R16–R25, R28–R36 | 28 | 1k | YAGEO MFR-12FTF52-1K | [13-MFR-12FTF52-1KCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-1KCT-ND) | [603-MFR-12FTF52-1K](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-1K) |  |
| R26 | 1 | 330 | YAGEO MFR-12FTF52-330R | [13-MFR-12FTF52-330RCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-330RCT-ND) | [603-MFR-12FTF52-330R](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-330R) |  |
| R38 | 1 | 1M | YAGEO MFR-12FTF52-1M | [13-MFR-12FTF52-1MCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-1MCT-ND) | [603-MFR-12FTF52-1M](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-1M) |  |
| SW1–SW67 | 67 | Keyswitch | Cherry Americas LLC MX2A-E1NA | [1644-MX2A-E1NA-ND](https://www.digikey.com/en/products/filter?keywords=1644-MX2A-E1NA-ND) | [540-MX2A-E1NA](https://www.mouser.com/ProductDetail/540-MX2A-E1NA) |  |
| SW68 | 1 | POWER | E-Switch 400MSP1R6BLKM6QE | [EG4326-ND](https://www.digikey.com/en/products/filter?keywords=EG4326-ND) | [612-400MSP1R6BLKM6QE](https://www.mouser.com/ProductDetail/612-400MSP1R6BLKM6QE) |  |
| SW69 | 1 | IO ENABLE | CTS Electronic Components 206-8 | [CT2068-ND](https://www.digikey.com/en/products/filter?keywords=CT2068-ND) | [774-2068](https://www.mouser.com/ProductDetail/774-2068) |  |
| SW70 | 1 | RESET | Same Sky (Formerly CUI Devices) TS02-66-50-BK-160-LCR-D | [2223-TS02-66-50-BK-160-LCR-D-ND](https://www.digikey.com/en/products/filter?keywords=2223-TS02-66-50-BK-160-LCR-D-ND) | [179-TS026650BK160LCR](https://www.mouser.com/ProductDetail/179-TS026650BK160LCR) |  |
| U1 | 1 | 65C02 | Western Design Center (WDC) W65C02S6TPG-14 |  | [955-W65C02S6TPG-14](https://www.mouser.com/ProductDetail/955-W65C02S6TPG-14) |  |
| U2 | 1 | 65C22 | Western Design Center (WDC) W65C22N6TPG-14 |  | [955-W65C22N6TPG-14](https://www.mouser.com/ProductDetail/955-W65C22N6TPG-14) |  |
| U3 | 1 | Pico9918A | Pico9918A, DIP-40_W15.24mm |  |  | [Tindie](https://www.tindie.com/products/visrealm/pico9918-pro/) |
| U4 | 1 | R6551AP | Rockwell R6551AP |  |  | [Jameco 43318](https://www.jameco.com/z/R6551AP-Rockwell-IC-6551-Asynchronous-Communication-Interface-Adapter-DIP-28-pin_43318.html) |
| U5 | 1 | 74HC163 | Texas Instruments SN74HC163N | [296-8246-5-ND](https://www.digikey.com/en/products/filter?keywords=296-8246-5-ND) | [595-SN74HC163N](https://www.mouser.com/ProductDetail/595-SN74HC163N) |  |
| U6 | 1 | ATmega1284 | Microchip Technology ATMEGA1284-PU | [ATMEGA1284-PU-ND](https://www.digikey.com/en/products/filter?keywords=ATMEGA1284-PU-ND) | [556-ATMEGA1284-PU](https://www.mouser.com/ProductDetail/556-ATMEGA1284-PU) |  |
| U7 | 1 | HM62256LP-70 | Hitachi HM62256LP-70 |  |  | [Jameco 82472](https://www.jameco.com/z/HM62256LP-70-HITACHI-IC-62256LP-70-Low-Power-CMOS-SRAM-256K-Bit-32Kx8-70ns_82472.html) |
| U8 | 1 | AT28C256 | Microchip Technology AT28C256-15PU | [AT28C256-15PU-ND](https://www.digikey.com/en/products/filter?keywords=AT28C256-15PU-ND) | [556-AT28C25615PU](https://www.mouser.com/ProductDetail/556-AT28C25615PU) |  |
| U9 | 1 | ARMSID | Retrocomp ARMSID |  |  | [Retrocomp](https://retrocomp.cz/produkt?id=2) |
| U10 | 1 | MAX238CNG+ | Maxim MAX238CNG+ | [MAX238CNG+-ND](https://www.digikey.com/en/products/filter?keywords=MAX238CNG%2B-ND) | [700-MAX238CNG](https://www.mouser.com/ProductDetail/700-MAX238CNG) |  |
| U11, U12, U14, U16 | 4 | 74HC00 | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| U13 | 1 | 74HC02 | Texas Instruments SN74HC02N | [296-1564-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1564-5-ND) | [595-SN74HC02N](https://www.mouser.com/ProductDetail/595-SN74HC02N) |  |
| U15 | 1 | AS6C4008 | Alliance Memory AS6C4008-55PCN | [1450-1027-ND](https://www.digikey.com/en/products/filter?keywords=1450-1027-ND) | [913-AS6C4008-55PCN](https://www.mouser.com/ProductDetail/913-AS6C4008-55PCN) |  |
| U17 | 1 | 74HC30 | Texas Instruments CD74HC30E |  | [595-CD74HC30E](https://www.mouser.com/ProductDetail/595-CD74HC30E) |  |
| U18 | 1 | DS1511Y / DS1501 | Maxim DS1511Y+ | [DS1511Y+-ND](https://www.digikey.com/en/products/filter?keywords=DS1511Y%2B-ND) | [700-DS1511Y](https://www.mouser.com/ProductDetail/700-DS1511Y) |  |
| U19, U20 | 2 | 74HC138 | Texas Instruments SN74HC138N | [296-1575-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1575-5-ND) | [595-SN74HC138N](https://www.mouser.com/ProductDetail/595-SN74HC138N) |  |
| U21, U22 | 2 | 74HC573 | Texas Instruments CD74HC573E | [296-12815-5-ND](https://www.digikey.com/en/products/filter?keywords=296-12815-5-ND) | [595-CD74HC573E](https://www.mouser.com/ProductDetail/595-CD74HC573E) |  |
| X1 | 1 | 16 MHz | ECS Inc. ECS-100AX-160 | [X947-ND](https://www.digikey.com/en/products/filter?keywords=X947-ND) | [520-TCF1600-X](https://www.mouser.com/ProductDetail/520-TCF1600-X) |  |
| Y1 | 1 | 1.8432 MHz | Abracon LLC AB-1.8432MHZ-B2 | [535-9009-ND](https://www.digikey.com/en/products/filter?keywords=535-9009-ND) | [815-AB-1.8432-B2](https://www.mouser.com/ProductDetail/815-AB-1.8432-B2) |  |
| Y2 | 1 | 32.768 kHz | Abracon LLC AB26T-32.768KHZ-6 | [535-AB26T-32.768KHZ-6CT-ND](https://www.digikey.com/en/products/filter?keywords=535-AB26T-32.768KHZ-6CT-ND) | [815-AB26T-32.768K-6](https://www.mouser.com/ProductDetail/815-AB26T-32.768K-6) |  |
| U4, U7, U9, U18 | 4 | Socket | IC socket, 28-pin, 0.6 in | [3M5481-ND](https://www.digikey.com/en/products/filter?keywords=3M5481-ND) | [517-4828-6004-CP](https://www.mouser.com/ProductDetail/517-4828-6004-CP) | |
| U8 | 1 | Socket | 28-pin ZIF socket, or an ordinary 28-pin socket | [3M2802-ND](https://www.digikey.com/en/products/filter?keywords=3M2802-ND) | [517-228-1277-00](https://www.mouser.com/ProductDetail/517-228-1277-00) | |
| U21, U22 | 2 | Socket | IC socket, 20-pin, 0.3 in | [3M5477-ND](https://www.digikey.com/en/products/filter?keywords=3M5477-ND) | [517-4820-3004-CP](https://www.mouser.com/ProductDetail/517-4820-3004-CP) | |
| U11–U14, U16, U17 | 6 | Socket | IC socket, 14-pin, 0.3 in | [3M5474-ND](https://www.digikey.com/en/products/filter?keywords=3M5474-ND) | [517-4814-3004-CP](https://www.mouser.com/ProductDetail/517-4814-3004-CP) | |
| U10 | 1 | Socket | IC socket, 24-pin, 0.3 in | [3M5466-ND](https://www.digikey.com/en/products/filter?keywords=3M5466-ND) | [517-4824-3000-CP](https://www.mouser.com/ProductDetail/517-4824-3000-CP) | |
| U1–U3, U6 | 4 | Socket | IC socket, 40-pin, 0.6 in | [3M5471-ND](https://www.digikey.com/en/products/filter?keywords=3M5471-ND) | [517-4840-6000-CP](https://www.mouser.com/ProductDetail/517-4840-6000-CP) | |
| U15 | 1 | Socket | IC socket, 32-pin, 0.6 in | [3M5470-ND](https://www.digikey.com/en/products/filter?keywords=3M5470-ND) | [517-4832-6000-CP](https://www.mouser.com/ProductDetail/517-4832-6000-CP) | |
| U5, U19, U20 | 3 | Socket | IC socket, 16-pin, 0.3 in | [3M5475-ND](https://www.digikey.com/en/products/filter?keywords=3M5475-ND) | [517-4816-3004-CP](https://www.mouser.com/ProductDetail/517-4816-3004-CP) | |
| J1, J2, J4 | 3 | | Shunt, 2.54 mm | [S9337-ND](https://www.digikey.com/en/products/filter?keywords=S9337-ND) |  |  |

Pin headers are cut from strips, and the cart files count whole strips.

- **BT1:** Retainer for a CR2032 cell. BAT-HLD-001-THM, on the tested boards, is obsolete; this is its listed continuation. Digi-Key has none in stock today.
- **D1:** Green shown. The colour is the builder's choice.
- **J16:** Replaces GCT DCJ200-10-A-K1-K, now obsolete, which older builds used. Its pads and body match this footprint on the datasheet. No board has been built with it yet.
- **J18:** Male box header with a keying notch, for a 40-way ribbon cable.
- **J21:** Right-angle socket on the ACE Board; the CF Adapter plugs in here. Digi-Key only.
- **SW1–SW67:** Cherry MX2A RGB Blue, clear housing, as on the owner's Amazon kit. MX1A-E1NN (black housing) is the deeper-stocked alternative; Digi-Key CH196-ND, Mouser 540-MX1A-E1NN.
- **U4:** Rockwell R6551AP, out of production. Do not substitute a W65C51. A Rockwell R65C51P1 or R65C51P2 also works, but only where the board has the ACIA's crystal jumpers and they are closed: the Serial Card and Serial Card Pro (JP2, JP3), the ACE Board 1.1 (JP1, JP2) and the KIM Board 1.1 (JP2, JP3). On a bare crystal it gives no serial.
- **U7:** Hitachi HM62256LP-70, out of production: buy it from Jameco. The parts lists order it from 2026-11-28, in place of the Alliance AS6C62256 they ordered before. The Alliance has misread on the family's machines, now and then returning a byte with one bit wrong, so that programs crash or misbehave; the Hitachi hasn't, in testing on the ACE and the KIM.
- **U9:** A modern replacement for the MOS 6581 SID, which is out of production. Every tested build uses one. A real 6581 also needs 12 V at pin 28, which the standard build does not provide.
- **U18:** Or the RTC Adapter (6502-COB), a DS1501 on a plug, for less, on any revision. See the build notes.
- **U18:** Or a DS1501YN+, which runs on Y2. See the build notes.
- **Y2:** The DS1501's crystal. It must be 6 pF: a 12.5 pF crystal needs a BIOS change. Lay the can flat on its pad and solder it there.
- **Y2:** Fit it with a DS1511Y too, which has no pins to meet it.

### ACE Board Rev 1.0

Made, tested. **Tested**.

Cart files: [digikey.csv](BOM/ACE%20Board/Rev%201.0/digikey.csv), [mouser.csv](BOM/ACE%20Board/Rev%201.0/mouser.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other |
|---|---|---|---|---|---|---|
| BT1 | 1 | CR2032 | TE Connectivity Linx BAT-HLD-001-THM-TR | [343-BAT-HLD-001-THM-TRCT-ND](https://www.digikey.com/en/products/filter?keywords=343-BAT-HLD-001-THM-TRCT-ND) |  |  |
| C1, C9–C30 | 23 | 100nF | KYOCERA AVX SR205C104KAR | [478-3187-ND](https://www.digikey.com/en/products/filter?keywords=478-3187-ND) | [581-SR205C104KAR](https://www.mouser.com/ProductDetail/581-SR205C104KAR) |  |
| C2, C3, C5, C6, C8 | 5 | 1uF | KYOCERA AVX SR205E105MAR | [478-7667-ND](https://www.digikey.com/en/products/filter?keywords=478-7667-ND) | [581-SR205E105MAR](https://www.mouser.com/ProductDetail/581-SR205E105MAR) |  |
| C4, C7 | 2 | 2.2nF | KYOCERA AVX SR155C222KAR | [478-11698-ND](https://www.digikey.com/en/products/filter?keywords=478-11698-ND) | [581-SR155C222KAR](https://www.mouser.com/ProductDetail/581-SR155C222KAR) |  |
| D1 | 1 | POWER LED | Würth Elektronik 151031VS06000 | [732-5008-ND](https://www.digikey.com/en/products/filter?keywords=732-5008-ND) | [710-151031VS06000](https://www.mouser.com/ProductDetail/710-151031VS06000) |  |
| D2, D3 | 2 | BAT85 | Vishay BAT85S-TR | [BAT85SCT-ND](https://www.digikey.com/en/products/filter?keywords=BAT85SCT-ND) | [78-BAT85S](https://www.mouser.com/ProductDetail/78-BAT85S) |  |
| J1 | 1 | PHI2 SELECT | Pin header 1×3, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J2 | 1 | CTS EN | Pin header 1×3, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J3 | 1 | RESET SW | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J4 | 1 | DCD EN | Pin header 1×3, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J5 | 1 | VDD | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J6 | 1 | JOYSTICK A | Amphenol D09P33E4GX00LF | [609-1481-ND](https://www.digikey.com/en/products/filter?keywords=609-1481-ND) | [649-D09P33E4GX00LF](https://www.mouser.com/ProductDetail/649-D09P33E4GX00LF) |  |
| J7 | 1 | PADDLES | Pin header 1×4, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J8 | 1 | JOYSTICK B | Amphenol D09P33E4GX00LF | [609-1481-ND](https://www.digikey.com/en/products/filter?keywords=609-1481-ND) | [649-D09P33E4GX00LF](https://www.mouser.com/ProductDetail/649-D09P33E4GX00LF) |  |
| J9 | 1 | PORT B | Adam Tech BHR-12-VUA | [2057-BHR-12-VUA-ND](https://www.digikey.com/en/products/filter?keywords=2057-BHR-12-VUA-ND) | [737-BHR-12-VUA](https://www.mouser.com/ProductDetail/737-BHR-12-VUA) | 2057-BHR-12-VUA-ND |
| J10 | 1 | PORT A | Adam Tech BHR-12-VUA | [2057-BHR-12-VUA-ND](https://www.digikey.com/en/products/filter?keywords=2057-BHR-12-VUA-ND) | [737-BHR-12-VUA](https://www.mouser.com/ProductDetail/737-BHR-12-VUA) | 2057-BHR-12-VUA-ND |
| J11 | 1 | AUDIO L | Switchcraft Inc. PJRAN1X1U02X | [PJRAN1X1U02X-ND](https://www.digikey.com/en/products/filter?keywords=PJRAN1X1U02X-ND) | [502-PJRAN1X1U02X](https://www.mouser.com/ProductDetail/502-PJRAN1X1U02X) |  |
| J12 | 1 | DB9 MALE (DTE) | Amphenol D09P33E4GX00LF | [609-1481-ND](https://www.digikey.com/en/products/filter?keywords=609-1481-ND) | [649-D09P33E4GX00LF](https://www.mouser.com/ProductDetail/649-D09P33E4GX00LF) |  |
| J13 | 1 | PS/2 | Kycon, Inc. KMDGX-6S-BS | [2092-KMDGX-6S-BS-ND](https://www.digikey.com/en/products/filter?keywords=2092-KMDGX-6S-BS-ND) | [806-KMDGX-6S-BS](https://www.mouser.com/ProductDetail/806-KMDGX-6S-BS) |  |
| J14 | 1 | AUDIO R | Switchcraft Inc. PJRAN1X1U03X | [PJRAN1X1U03X-ND](https://www.digikey.com/en/products/filter?keywords=PJRAN1X1U03X-ND) | [502-PJRAN1X1U03X](https://www.mouser.com/ProductDetail/502-PJRAN1X1U03X) |  |
| J15 | 1 | AUDIO | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J16 | 1 | 5V DC | Same Sky PJ-102AH | [CP-102AH-ND](https://www.digikey.com/en/products/filter?keywords=CP-102AH-ND) | [490-PJ-102AH](https://www.mouser.com/ProductDetail/490-PJ-102AH) |  |
| J17 | 1 | CART | TE Connectivity 5-5530843-4 | [A31723-ND](https://www.digikey.com/en/products/filter?keywords=A31723-ND) | [571-5-5530843-4](https://www.mouser.com/ProductDetail/571-5-5530843-4) |  |
| J18 | 1 | BUS | Würth Elektronik 61204021621 | [732-5401-ND](https://www.digikey.com/en/products/filter?keywords=732-5401-ND) | [710-61204021621](https://www.mouser.com/ProductDetail/710-61204021621) |  |
| J19 | 1 | VCC | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J20 | 1 | POWER LED | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J21 | 1 | STORAGE | Sullins PPPC102LJBN-RC | [S5563-ND](https://www.digikey.com/en/products/filter?keywords=S5563-ND) |  |  |
| J22 | 1 | KEYBOARD | Adam Tech 2PH1-16-UA | [2057-2PH1-16-UA-ND](https://www.digikey.com/en/products/filter?keywords=2057-2PH1-16-UA-ND) | [737-2PH1-16-UA](https://www.mouser.com/ProductDetail/737-2PH1-16-UA) |  |
| R1–R5, R27 | 6 | 10k (the silk says 1k) | YAGEO MFR-12FTF52-10K | [13-MFR-12FTF52-10KCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-10KCT-ND) | [603-MFR-12FTF52-10K](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-10K) |  |
| R6–R14, R16–R25, R28–R36 | 28 | 1k | YAGEO MFR-12FTF52-1K | [13-MFR-12FTF52-1KCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-1KCT-ND) | [603-MFR-12FTF52-1K](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-1K) |  |
| R26 | 1 | 330 | YAGEO MFR-12FTF52-330R | [13-MFR-12FTF52-330RCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-330RCT-ND) | [603-MFR-12FTF52-330R](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-330R) |  |
| SW1–SW67 | 67 | Keyswitch | Cherry Americas LLC MX2A-E1NA | [1644-MX2A-E1NA-ND](https://www.digikey.com/en/products/filter?keywords=1644-MX2A-E1NA-ND) | [540-MX2A-E1NA](https://www.mouser.com/ProductDetail/540-MX2A-E1NA) |  |
| SW68 | 1 | POWER | E-Switch 400MSP1R6BLKM6QE | [EG4326-ND](https://www.digikey.com/en/products/filter?keywords=EG4326-ND) | [612-400MSP1R6BLKM6QE](https://www.mouser.com/ProductDetail/612-400MSP1R6BLKM6QE) |  |
| SW69 | 1 | IO ENABLE | CTS Electronic Components 206-8 | [CT2068-ND](https://www.digikey.com/en/products/filter?keywords=CT2068-ND) | [774-2068](https://www.mouser.com/ProductDetail/774-2068) |  |
| SW70 | 1 | RESET | Same Sky (Formerly CUI Devices) TS02-66-50-BK-160-LCR-D | [2223-TS02-66-50-BK-160-LCR-D-ND](https://www.digikey.com/en/products/filter?keywords=2223-TS02-66-50-BK-160-LCR-D-ND) | [179-TS026650BK160LCR](https://www.mouser.com/ProductDetail/179-TS026650BK160LCR) |  |
| U1 | 1 | 65C02 | Western Design Center (WDC) W65C02S6TPG-14 |  | [955-W65C02S6TPG-14](https://www.mouser.com/ProductDetail/955-W65C02S6TPG-14) |  |
| U2 | 1 | 65C22 | Western Design Center (WDC) W65C22N6TPG-14 |  | [955-W65C22N6TPG-14](https://www.mouser.com/ProductDetail/955-W65C22N6TPG-14) |  |
| U3 | 1 | Pico9918A | Pico9918A, DIP-40_W15.24mm |  |  | [Tindie](https://www.tindie.com/products/visrealm/pico9918-pro/) |
| U4 | 1 | 65C51 | Rockwell R6551AP |  |  | [Jameco 43318](https://www.jameco.com/z/R6551AP-Rockwell-IC-6551-Asynchronous-Communication-Interface-Adapter-DIP-28-pin_43318.html) |
| U5 | 1 | 74HC163 | Texas Instruments SN74HC163N | [296-8246-5-ND](https://www.digikey.com/en/products/filter?keywords=296-8246-5-ND) | [595-SN74HC163N](https://www.mouser.com/ProductDetail/595-SN74HC163N) |  |
| U6 | 1 | ATmega1284-P | Microchip Technology ATMEGA1284-PU | [ATMEGA1284-PU-ND](https://www.digikey.com/en/products/filter?keywords=ATMEGA1284-PU-ND) | [556-ATMEGA1284-PU](https://www.mouser.com/ProductDetail/556-ATMEGA1284-PU) |  |
| U7 | 1 | AS6C62256 | Hitachi HM62256LP-70 |  |  | [Jameco 82472](https://www.jameco.com/z/HM62256LP-70-HITACHI-IC-62256LP-70-Low-Power-CMOS-SRAM-256K-Bit-32Kx8-70ns_82472.html) |
| U8 | 1 | AT28C256 | Microchip Technology AT28C256-15PU | [AT28C256-15PU-ND](https://www.digikey.com/en/products/filter?keywords=AT28C256-15PU-ND) | [556-AT28C25615PU](https://www.mouser.com/ProductDetail/556-AT28C25615PU) |  |
| U9 | 1 | 6581 | Retrocomp ARMSID |  |  | [Retrocomp](https://retrocomp.cz/produkt?id=2) |
| U10 | 1 | MAX238xNG+ | Maxim MAX238CNG+ | [MAX238CNG+-ND](https://www.digikey.com/en/products/filter?keywords=MAX238CNG%2B-ND) | [700-MAX238CNG](https://www.mouser.com/ProductDetail/700-MAX238CNG) |  |
| U11, U14, U16 | 3 | 74HC00 | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| U15 | 1 | AS6C4008 | Alliance Memory AS6C4008-55PCN | [1450-1027-ND](https://www.digikey.com/en/products/filter?keywords=1450-1027-ND) | [913-AS6C4008-55PCN](https://www.mouser.com/ProductDetail/913-AS6C4008-55PCN) |  |
| U17 | 1 | 74HC30 | Texas Instruments CD74HC30E |  | [595-CD74HC30E](https://www.mouser.com/ProductDetail/595-CD74HC30E) |  |
| U18 | 1 | DS1511Y | Maxim DS1511Y+ | [DS1511Y+-ND](https://www.digikey.com/en/products/filter?keywords=DS1511Y%2B-ND) | [700-DS1511Y](https://www.mouser.com/ProductDetail/700-DS1511Y) |  |
| U19, U20 | 2 | 74HC138 | Texas Instruments SN74HC138N | [296-1575-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1575-5-ND) | [595-SN74HC138N](https://www.mouser.com/ProductDetail/595-SN74HC138N) |  |
| U21, U22 | 2 | 74HC573 | Texas Instruments CD74HC573E | [296-12815-5-ND](https://www.digikey.com/en/products/filter?keywords=296-12815-5-ND) | [595-CD74HC573E](https://www.mouser.com/ProductDetail/595-CD74HC573E) |  |
| X1 | 1 | 16MHz | ECS Inc. ECS-100AX-160 | [X947-ND](https://www.digikey.com/en/products/filter?keywords=X947-ND) | [520-TCF1600-X](https://www.mouser.com/ProductDetail/520-TCF1600-X) |  |
| Y1 | 1 | 1.8432 Mhz | Abracon LLC AB-1.8432MHZ-B2 | [535-9009-ND](https://www.digikey.com/en/products/filter?keywords=535-9009-ND) | [815-AB-1.8432-B2](https://www.mouser.com/ProductDetail/815-AB-1.8432-B2) |  |
| U11–U14, U16, U17 | 6 | Socket | IC socket, 14-pin, 0.3 in | [3M5474-ND](https://www.digikey.com/en/products/filter?keywords=3M5474-ND) | [517-4814-3004-CP](https://www.mouser.com/ProductDetail/517-4814-3004-CP) | |
| U4, U7, U9, U18 | 4 | Socket | IC socket, 28-pin, 0.6 in | [3M5481-ND](https://www.digikey.com/en/products/filter?keywords=3M5481-ND) | [517-4828-6004-CP](https://www.mouser.com/ProductDetail/517-4828-6004-CP) | |
| U8 | 1 | Socket | 28-pin ZIF socket, or an ordinary 28-pin socket | [3M2802-ND](https://www.digikey.com/en/products/filter?keywords=3M2802-ND) | [517-228-1277-00](https://www.mouser.com/ProductDetail/517-228-1277-00) | |
| U21, U22 | 2 | Socket | IC socket, 20-pin, 0.3 in | [3M5477-ND](https://www.digikey.com/en/products/filter?keywords=3M5477-ND) | [517-4820-3004-CP](https://www.mouser.com/ProductDetail/517-4820-3004-CP) | |
| U10 | 1 | Socket | IC socket, 24-pin, 0.3 in | [3M5466-ND](https://www.digikey.com/en/products/filter?keywords=3M5466-ND) | [517-4824-3000-CP](https://www.mouser.com/ProductDetail/517-4824-3000-CP) | |
| U1–U3, U6 | 4 | Socket | IC socket, 40-pin, 0.6 in | [3M5471-ND](https://www.digikey.com/en/products/filter?keywords=3M5471-ND) | [517-4840-6000-CP](https://www.mouser.com/ProductDetail/517-4840-6000-CP) | |
| U15 | 1 | Socket | IC socket, 32-pin, 0.6 in | [3M5470-ND](https://www.digikey.com/en/products/filter?keywords=3M5470-ND) | [517-4832-6000-CP](https://www.mouser.com/ProductDetail/517-4832-6000-CP) | |
| U5, U19, U20 | 3 | Socket | IC socket, 16-pin, 0.3 in | [3M5475-ND](https://www.digikey.com/en/products/filter?keywords=3M5475-ND) | [517-4816-3004-CP](https://www.mouser.com/ProductDetail/517-4816-3004-CP) | |
| Added | 1 | | Panasonic EEA-GA1C100, 10 µF, on the underside across J19 | [P14482-ND](https://www.digikey.com/en/products/filter?keywords=P14482-ND) | [667-EEA-GA1C100](https://www.mouser.com/ProductDetail/667-EEA-GA1C100) |  |
| Added | 1 | | Vishay BAT85S-TR, for the video card /INT | [BAT85SCT-ND](https://www.digikey.com/en/products/filter?keywords=BAT85SCT-ND) | [78-BAT85S](https://www.mouser.com/ProductDetail/78-BAT85S) |  |
| J1, J2, J4 | 3 | | Shunt, 2.54 mm | [S9337-ND](https://www.digikey.com/en/products/filter?keywords=S9337-ND) |  |  |

Pin headers are cut from strips, and the cart files count whole strips.

U12 and U13 are not listed: fit the ACE RAM Patch Rev 1.1 in their sockets. See the build notes.

- **BT1:** Retainer for a CR2032 cell. BAT-HLD-001-THM, on the tested boards, is obsolete; this is its listed continuation. Digi-Key has none in stock today.
- **D1:** Green shown. The colour is the builder's choice.
- **J16:** Replaces GCT DCJ200-10-A-K1-K, now obsolete, which older builds used. Its pads and body match this footprint on the datasheet. No board has been built with it yet.
- **J18:** Male box header with a keying notch, for a 40-way ribbon cable.
- **J21:** Right-angle socket on the ACE Board; the CF Adapter plugs in here. Digi-Key only.
- **SW1–SW67:** Cherry MX2A RGB Blue, clear housing, as on the owner's Amazon kit. MX1A-E1NN (black housing) is the deeper-stocked alternative; Digi-Key CH196-ND, Mouser 540-MX1A-E1NN.
- **U4:** Rockwell R6551AP, out of production. Do not substitute a W65C51. A Rockwell R65C51P1 or R65C51P2 also works, but only where the board has the ACIA's crystal jumpers and they are closed: the Serial Card and Serial Card Pro (JP2, JP3), the ACE Board 1.1 (JP1, JP2) and the KIM Board 1.1 (JP2, JP3). On a bare crystal it gives no serial.
- **U7:** Hitachi HM62256LP-70, out of production: buy it from Jameco. The parts lists order it from 2026-11-28, in place of the Alliance AS6C62256 they ordered before. The Alliance has misread on the family's machines, now and then returning a byte with one bit wrong, so that programs crash or misbehave; the Hitachi hasn't, in testing on the ACE and the KIM.
- **U9:** A modern replacement for the MOS 6581 SID, which is out of production. Every tested build uses one. A real 6581 also needs 12 V at pin 28, which the standard build does not provide.
- **U18:** Or the RTC Adapter (6502-COB), a DS1501 on a plug, for less, on any revision. See the build notes.


## ACE CF Adapter

### ACE CF Adapter Rev 1.1

Drawn, not made yet. **Proven design**: the same circuit as the tested Rev 1.0, renumbered and in surface-mount parts for JLCPCB assembly. The new LCSC socket fits the same footprint, but no board has been built with it yet.

Cart files: [digikey.csv](BOM/ACE%20CF%20Adapter/Rev%201.1/digikey.csv), [mouser.csv](BOM/ACE%20CF%20Adapter/Rev%201.1/mouser.csv), [digikey-through-hole.csv](BOM/ACE%20CF%20Adapter/Rev%201.1/digikey-through-hole.csv), [mouser-through-hole.csv](BOM/ACE%20CF%20Adapter/Rev%201.1/mouser-through-hole.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other | Pre-soldered |
|---|---|---|---|---|---|---|---|
| D1 | 1 | ACT | Lite-On Inc. LTST-C170KRKT | [160-1415-1-ND](https://www.digikey.com/en/products/filter?keywords=160-1415-1-ND) | [859-LTST-C170KRKT](https://www.mouser.com/ProductDetail/859-LTST-C170KRKT) | LCSC [C2295](https://www.lcsc.com/search?q=C2295) | Yes |
| J1 | 1 | STORAGE | Amphenol 68021-120HLF | [609-3338-ND](https://www.digikey.com/en/products/filter?keywords=609-3338-ND) | [649-68021-120HLF](https://www.mouser.com/ProductDetail/649-68021-120HLF) |  | |
| J2 | 1 | Compact Flash | ATTEND Technology 101D-TAAB-R01 | [4827-101D-TAAB-R01-ND](https://www.digikey.com/en/products/filter?keywords=4827-101D-TAAB-R01-ND) |  | LCSC [C2962036](https://www.lcsc.com/search?q=C2962036) | Yes |
| R1–R4 | 4 | 1k | YAGEO RC0805FR-071KL | [311-1.00KCRCT-ND](https://www.digikey.com/en/products/filter?keywords=311-1.00KCRCT-ND) | [603-RC0805FR-071KL](https://www.mouser.com/ProductDetail/603-RC0805FR-071KL) | LCSC [C17513](https://www.lcsc.com/search?q=C17513) | Yes |
| R5 | 1 | 330 | YAGEO RC0805FR-07330RL | [311-330CRCT-ND](https://www.digikey.com/en/products/filter?keywords=311-330CRCT-ND) | [603-RC0805FR-07330RL](https://www.mouser.com/ProductDetail/603-RC0805FR-07330RL) | LCSC [C17630](https://www.lcsc.com/search?q=C17630) | Yes |

- **J1:** Right-angle header on the CF and SD Adapters; plugs into the right-angle socket on the ACE Board.
- **J2:** LCSC C2962036 is a different maker (HOAUC HYCW01-CF50-395B), matched to the footprint by datasheet and not yet built. Digi-Key has none in stock today.

### ACE CF Adapter Rev 1.0

Made, tested. **Tested**.

Cart files: [digikey.csv](BOM/ACE%20CF%20Adapter/Rev%201.0/digikey.csv), [mouser.csv](BOM/ACE%20CF%20Adapter/Rev%201.0/mouser.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other |
|---|---|---|---|---|---|---|
| D1 | 1 | ACT | Würth Elektronik 151031VS06000 | [732-5008-ND](https://www.digikey.com/en/products/filter?keywords=732-5008-ND) | [710-151031VS06000](https://www.mouser.com/ProductDetail/710-151031VS06000) |  |
| J3 | 1 | Compact Flash | ATTEND Technology 101D-TAAB-R01 | [4827-101D-TAAB-R01-ND](https://www.digikey.com/en/products/filter?keywords=4827-101D-TAAB-R01-ND) |  | LCSC [C2962036](https://www.lcsc.com/search?q=C2962036) |
| J21 | 1 | STORAGE | Amphenol 68021-120HLF | [609-3338-ND](https://www.digikey.com/en/products/filter?keywords=609-3338-ND) | [649-68021-120HLF](https://www.mouser.com/ProductDetail/649-68021-120HLF) |  |
| R1–R4 | 4 | 1k | YAGEO MFR-12FTF52-1K | [13-MFR-12FTF52-1KCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-1KCT-ND) | [603-MFR-12FTF52-1K](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-1K) |  |
| R5 | 1 | 330 | YAGEO MFR-12FTF52-330R | [13-MFR-12FTF52-330RCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-330RCT-ND) | [603-MFR-12FTF52-330R](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-330R) |  |

- **D1:** Green shown. The colour is the builder's choice.
- **J3:** LCSC C2962036 is a different maker (HOAUC HYCW01-CF50-395B), matched to the footprint by datasheet and not yet built. Digi-Key has none in stock today.
- **J21:** Right-angle header on the CF and SD Adapters; plugs into the right-angle socket on the ACE Board.


## ACE RAM Patch

### ACE RAM Patch Rev 1.1

Made. Yes, 2026-11-03. **Tested**: built and tested on an ACE Board Rev 1.0, 2026-11-03.

Cart files: [digikey.csv](BOM/ACE%20RAM%20Patch/Rev%201.1/digikey.csv), [mouser.csv](BOM/ACE%20RAM%20Patch/Rev%201.1/mouser.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other |
|---|---|---|---|---|---|---|
| J1 | 1 | 74HC00 (U12) | Machined pins, 2.54 mm, cut from a 64-pin strip (Mill-Max 800-10-064-10-001000) | [ED7264-64-ND](https://www.digikey.com/en/products/filter?keywords=ED7264-64-ND) | [575-010064](https://www.mouser.com/ProductDetail/575-010064) |  |
| J2 | 1 | 74HC00 (U13) | Machined pins, 2.54 mm, cut from a 64-pin strip (Mill-Max 800-10-064-10-001000) | [ED7264-64-ND](https://www.digikey.com/en/products/filter?keywords=ED7264-64-ND) | [575-010064](https://www.mouser.com/ProductDetail/575-010064) |  |
| U1 | 1 | 74HC00 | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| U2 | 1 | 74HC02 | Texas Instruments SN74HC02N | [296-1564-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1564-5-ND) | [595-SN74HC02N](https://www.mouser.com/ProductDetail/595-SN74HC02N) |  |

Pin headers are cut from strips, and the cart files count whole strips.

- **J1, J2:** Machined round pins, which plug into a DIP socket without spreading its contacts. Cut a piece for each row of pins: a DIP-28 plug takes two of 14.
- **J1, J2:** Pins, not a chip: the value names the ACE Board socket whose holes they are soldered into. They plug into no socket, so ordinary square header strip does as well: the tested patch was built with it. Try the pins in the holes first, as the build notes say.

### ACE RAM Patch Rev 1.0

Made. Failed: Rev 1.1 replaces it. **Tested**: built and tested: its decode is wrong, and Rev 1.1 replaces it.

Cart files: [digikey.csv](BOM/ACE%20RAM%20Patch/Rev%201.0/digikey.csv), [mouser.csv](BOM/ACE%20RAM%20Patch/Rev%201.0/mouser.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other |
|---|---|---|---|---|---|---|
| J1 | 1 | 74HC00 (U13) | Machined pins, 2.54 mm, cut from a 64-pin strip (Mill-Max 800-10-064-10-001000) | [ED7264-64-ND](https://www.digikey.com/en/products/filter?keywords=ED7264-64-ND) | [575-010064](https://www.mouser.com/ProductDetail/575-010064) |  |
| U1 | 1 | 74HC00 | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| U2 | 1 | 74HC02 | Texas Instruments SN74HC02N | [296-1564-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1564-5-ND) | [595-SN74HC02N](https://www.mouser.com/ProductDetail/595-SN74HC02N) |  |

Pin headers are cut from strips, and the cart files count whole strips.

- **J1:** Machined round pins, which plug into a DIP socket without spreading its contacts. Cut a piece for each row of pins: a DIP-28 plug takes two of 14.
- **J1:** Pins, not a chip: the value names the ACE Board socket whose holes they are soldered into. They plug into no socket, so ordinary square header strip does as well: the tested patch was built with it. Try the pins in the holes first, as the build notes say.


## ACE SD Adapter Bottom

### ACE SD Adapter Bottom Rev 1.1

Drawn, not made yet. **Untested**: a new board: an SD card the stock BIOS takes for CompactFlash, with a built-in drive; the ACE SD Adapter Top, stacked on it, carries the SD card socket. Not yet made.

Cart files: [digikey.csv](BOM/ACE%20SD%20Adapter%20Bottom/Rev%201.1/digikey.csv), [mouser.csv](BOM/ACE%20SD%20Adapter%20Bottom/Rev%201.1/mouser.csv), [digikey-through-hole.csv](BOM/ACE%20SD%20Adapter%20Bottom/Rev%201.1/digikey-through-hole.csv), [mouser-through-hole.csv](BOM/ACE%20SD%20Adapter%20Bottom/Rev%201.1/mouser-through-hole.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other | Pre-soldered |
|---|---|---|---|---|---|---|---|
| C1–C4 | 4 | 100nF | YAGEO CC0805KRX7R9BB104 | [311-1140-1-ND](https://www.digikey.com/en/products/filter?keywords=311-1140-1-ND) | [603-CC805KRX7R9BB104](https://www.mouser.com/ProductDetail/603-CC805KRX7R9BB104) | LCSC [C49678](https://www.lcsc.com/search?q=C49678) | Yes |
| J1 | 1 | STORAGE | Amphenol 68021-120HLF | [609-3338-ND](https://www.digikey.com/en/products/filter?keywords=609-3338-ND) | [649-68021-120HLF](https://www.mouser.com/ProductDetail/649-68021-120HLF) |  | |
| J7 | 1 | STACK SD | Sullins PPTC061LFBN-RC | [S7004-ND](https://www.digikey.com/en/products/filter?keywords=S7004-ND) | [200-SSW10601TS](https://www.mouser.com/ProductDetail/200-SSW10601TS) |  | |
| J9 | 1 | STACK POWER | Sullins PPTC061LFBN-RC | [S7004-ND](https://www.digikey.com/en/products/filter?keywords=S7004-ND) | [200-SSW10601TS](https://www.mouser.com/ProductDetail/200-SSW10601TS) |  | |
| R13–R20 | 8 | 4.7k | YAGEO RC0805FR-074K7L | [311-4.70KCRCT-ND](https://www.digikey.com/en/products/filter?keywords=311-4.70KCRCT-ND) | [603-RC0805FR-074K7L](https://www.mouser.com/ProductDetail/603-RC0805FR-074K7L) | LCSC [C17673](https://www.lcsc.com/search?q=C17673) | Yes |
| R21 | 1 | 10k | YAGEO RC0805FR-0710KL | [311-10.0KCRCT-ND](https://www.digikey.com/en/products/filter?keywords=311-10.0KCRCT-ND) | [603-RC0805FR-0710KL](https://www.mouser.com/ProductDetail/603-RC0805FR-0710KL) | LCSC [C17414](https://www.lcsc.com/search?q=C17414) | Yes |
| U1 | 1 | 74LVC4245A | Texas Instruments SN74LVC4245APWR | [296-12183-1-ND](https://www.digikey.com/en/products/filter?keywords=296-12183-1-ND) | [595-SN74LVC4245APWR](https://www.mouser.com/ProductDetail/595-SN74LVC4245APWR) | LCSC [C7859](https://www.lcsc.com/search?q=C7859) | Yes |
| U2 | 1 | Pico 2 | Raspberry Pi SC1631 | [2648-SC1631CT-ND](https://www.digikey.com/en/products/filter?keywords=2648-SC1631CT-ND) | [358-SC1631](https://www.mouser.com/ProductDetail/358-SC1631) |  | |
| U3 | 1 | W25Q128JVFIQ | Winbond Electronics W25Q128JVFIQ | [W25Q128JVFIQ-ND](https://www.digikey.com/en/products/filter?keywords=W25Q128JVFIQ-ND) | [454-W25Q128JVFIQ](https://www.mouser.com/ProductDetail/454-W25Q128JVFIQ) | LCSC [C2456298](https://www.lcsc.com/search?q=C2456298) | Yes |
| U6 | 1 | 74LVC541 | Nexperia USA Inc. 74LVC541APW,118 | [1727-6370-1-ND](https://www.digikey.com/en/products/filter?keywords=1727-6370-1-ND) | [771-74LVC541APW-T](https://www.mouser.com/ProductDetail/771-74LVC541APW-T) | LCSC [C113281](https://www.lcsc.com/search?q=C113281) | Yes |

Pin headers are cut from strips, and the cart files count whole strips.

- **J1:** Right-angle header on the CF and SD Adapters; plugs into the right-angle socket on the ACE Board.
- **J7, J9:** On Mouser: Samtec SSW-106-01-T-S, the same socket.
- **U2:** Soldered to the board on two 1×20 pin headers, cut from the header strip, not by its castellations. JLCPCB doesn't fit it: solder it yourself.
- **U3:** The built-in drive (16 MB). Digi-Key and Mouser have none in stock today (36-week lead); LCSC does. Any 16-pin 300 mil W25Q with a /RESET pin fits the same footprint, up to the 128 MB W25Q01JVSFIQ (Digi-Key 256-W25Q01JVSFIQ-ND, Mouser 454-W25Q01JVSFIQ, stocked at both); the firmware fits the disks to the size it finds and mirrors the rest.
- **U6:** LCSC C113281 is TI's SN74LVC541APWR, the same part. Digi-Key has none of either in stock today; Mouser has.


## ACE SD Adapter Top

### ACE SD Adapter Top Rev 1.1

Drawn, not made yet. **Untested**: the ACE SD Adapter Bottom's top board: the SD card socket, the LEDs and the SD card's 3.3 V regulator, stacked on the Bottom. Not yet made.

Cart files: [digikey.csv](BOM/ACE%20SD%20Adapter%20Top/Rev%201.1/digikey.csv), [mouser.csv](BOM/ACE%20SD%20Adapter%20Top/Rev%201.1/mouser.csv), [digikey-through-hole.csv](BOM/ACE%20SD%20Adapter%20Top/Rev%201.1/digikey-through-hole.csv), [mouser-through-hole.csv](BOM/ACE%20SD%20Adapter%20Top/Rev%201.1/mouser-through-hole.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other | Pre-soldered |
|---|---|---|---|---|---|---|---|
| C7 | 1 | 100nF | YAGEO CC0805KRX7R9BB104 | [311-1140-1-ND](https://www.digikey.com/en/products/filter?keywords=311-1140-1-ND) | [603-CC805KRX7R9BB104](https://www.mouser.com/ProductDetail/603-CC805KRX7R9BB104) | LCSC [C49678](https://www.lcsc.com/search?q=C49678) | Yes |
| C9, C10 | 2 | 1uF | YAGEO CC0805KKX7R8BB105 | [311-1456-1-ND](https://www.digikey.com/en/products/filter?keywords=311-1456-1-ND) | [603-CC805KKX7R8BB105](https://www.mouser.com/ProductDetail/603-CC805KKX7R8BB105) | LCSC [C28323](https://www.lcsc.com/search?q=C28323) | Yes |
| C25 | 1 | 10uF | Samsung Electro-Mechanics CL21A106KAYNNNE | [1276-CL21A106KAYNNNECT-ND](https://www.digikey.com/en/products/filter?keywords=1276-CL21A106KAYNNNECT-ND) | [187-CL21A106KAYNNNE](https://www.mouser.com/ProductDetail/187-CL21A106KAYNNNE) | LCSC [C15850](https://www.lcsc.com/search?q=C15850) | Yes |
| D1 | 1 | ACT | Lite-On Inc. LTST-C170KRKT | [160-1415-1-ND](https://www.digikey.com/en/products/filter?keywords=160-1415-1-ND) | [859-LTST-C170KRKT](https://www.mouser.com/ProductDetail/859-LTST-C170KRKT) | LCSC [C2295](https://www.lcsc.com/search?q=C2295) | Yes |
| D2 | 1 | SD | Lite-On Inc. LTST-C170KGKT | [160-1414-1-ND](https://www.digikey.com/en/products/filter?keywords=160-1414-1-ND) | [859-LTST-C170KGKT](https://www.mouser.com/ProductDetail/859-LTST-C170KGKT) | LCSC [C2297](https://www.lcsc.com/search?q=C2297) | Yes |
| J4 | 1 | SD CARD | XUNPU SD-106M |  |  | LCSC [C266603](https://www.lcsc.com/search?q=C266603) | Yes |
| J8 | 1 | STACK SD | Pin header 1×6, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  | |
| J10 | 1 | STACK POWER | Pin header 1×6, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  | |
| R1, R5 | 2 | 330 | YAGEO RC0805FR-07330RL | [311-330CRCT-ND](https://www.digikey.com/en/products/filter?keywords=311-330CRCT-ND) | [603-RC0805FR-07330RL](https://www.mouser.com/ProductDetail/603-RC0805FR-07330RL) | LCSC [C17630](https://www.lcsc.com/search?q=C17630) | Yes |
| R4, R23–R27 | 6 | 10k | YAGEO RC0805FR-0710KL | [311-10.0KCRCT-ND](https://www.digikey.com/en/products/filter?keywords=311-10.0KCRCT-ND) | [603-RC0805FR-0710KL](https://www.mouser.com/ProductDetail/603-RC0805FR-0710KL) | LCSC [C17414](https://www.lcsc.com/search?q=C17414) | Yes |
| U5 | 1 | AP2112K-3.3 | Diodes Incorporated AP2112K-3.3TRG1 | [AP2112K-3.3TRG1DICT-ND](https://www.digikey.com/en/products/filter?keywords=AP2112K-3.3TRG1DICT-ND) | [621-AP2112K-3.3TRG1](https://www.mouser.com/ProductDetail/621-AP2112K-3.3TRG1) | LCSC [C51118](https://www.lcsc.com/search?q=C51118) | Yes |

Pin headers are cut from strips, and the cart files count whole strips.

- **C25:** Samsung, not YAGEO, on the boards JLCPCB assembles: LCSC has no YAGEO 10 µF 0805 in stock, and C15850 is one of JLCPCB's basic parts.
- **J4:** Full-size SD, push-push, with card-detect and write-protect switches. LCSC only: the SD Adapter is assembled by JLCPCB, and LCSC stocks this part in thousands where it stocks the Hirose DM1AA in hundreds at eight times the price.
