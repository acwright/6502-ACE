# Revisions

Every revision of every board in this repository, and what is known about each. The dates of the checks are at the end.

**Status** says what has happened to a revision:

- **Made, matches order:** JLCPCB's own copy of the order is byte-identical to the production zip here, and the PCB file regenerates the same copper, mask, outline and holes. This compares files with the order. It says nothing about whether the board works: that's the **Label**.
- **Made, not compared:** the board exists, but its files haven't been compared with an order.
- **Ordered:** placed, and not yet arrived.
- **Drawn:** the files are complete, and the board hasn't been ordered.
- **Never made**, or **To confirm** where nothing on record says either way.

**Label** says whether a builder can rely on a revision. Make the newest revision of a board, and check its label first:

- **Tested:** This revision was built and tested.
- **Proven design:** Not built at this revision, but its circuit is a tested revision's. The only changes are silkscreen text, part values, mounting holes, outline clean-up, parts moved a fraction of a millimetre onto their grid, capacitor pitch, socket outlines, a footprint swap with the same holes, a solder jumper's default, the solder mask or paste at a card edge, or tracks rerouted or pours refilled with DRC and the netlist check passing. A builder can treat it as tested.
- **Untested:** The circuit, the power path or the layout changed in a way that only a built board proves, or the board has never been built at all.

**Holes** is how far the corner mounting holes sit from the board's edges. The standard is 6 mm, and 5 mm on the ACE Board, the CF Adapter and the Keyboard Helper. A dash means a card or cart, which has no corner holes.

| Board | Rev | Status | Label | Order | Ordered | Made from | Tindie stock | Size (mm) | Holes | Top panel | Enclosure | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ACE Board | 1.0 | Made, matches order | **Tested** | Y91 | 2026-05-13 | `6502-ACE 83b1b1a` | — | 335×250 | 5 mm | yes | — |  |
| ACE Board | 1.1 | Drawn | **Untested**: a new bank-latch decode (its logic is proven on the ACE RAM Patch 1.1), a 74HCT00 at U14, the PHI2 SELECT jumper with the SID on the CPU's clock, the ACIA's crystal jumpers, and a 1N5819 in the power path. On the first build, measure `VCC` at full load: it must stay above 4.5 V |  |  |  | — | 335×250 | 5 mm | yes | — |  |
| ACE CF Adapter | 1.0 | Made, matches order | **Tested** | Y89 | 2026-05-10 | `6502-ACE ef6370e` | — | 75×50 | 5 mm | yes | — |  |
| ACE CF Adapter | 1.1 | Drawn | **Proven design**: annotation only. The new LCSC socket fits the same footprint, but no board has been built with it yet |  |  |  | — | 75×50 | 5 mm | yes | — |  |
| ACE RAM Patch | 1.0 | Made, matches order | **Tested**: built and tested: its decode is wrong, and Rev 1.1 replaces it | Y94 | 2026-06-21 | `728f593` | — | 46×22 | — | — | — |  |
| ACE RAM Patch | 1.1 | Made, matches order | **Tested**: built and tested on an ACE Board Rev 1.0, 2026-11-03 | Y99 | 2026-09-24 | `a216b17` | — | 92.5×13 | — | — | — |  |

JLCPCB's orders were checked on 2026-11-04: each production zip marked *Made, matches order* was compared byte for byte with JLCPCB's copy, and its PCB regenerated to the same copper, mask, outline and holes. Each time this table is written, every PCB is checked again against its production zip, for copper and drill holes. Tindie stock is from the listings as saved on 2026-10-23.

<!-- History: hand-written. Tools/revision-audit/register.py keeps everything from here to the end. -->

## History

What changed in each revision of each board, newest first. The table above has the facts about each one.

**Title blocks, 2026-11-14.** Every schematic's and PCB's title block names the family as it is: `AC6502 <Board>`, not `6502 <Board>`, on all 6 revisions, the made ones included. The ACE RAM Patch's read `ACE RAM Patch`, with no family name. The title block is drawing-sheet text, which no Gerber layer carries: every PCB plots exactly as before (`Tools/revision-audit/gproof.py`), so no board and no label changed, and the made revisions' production zips are as JLCPCB received them. The schematic PDFs are regenerated. The production zip of each revision not yet made (2) is named from the title, so it is now `AC6502_<Board>_<Rev>.zip`, its contents unchanged. The board logos still read "6502". `Tools/revision-audit/audit.py` checks the titles.

**Reference text size, 2026-11-14.** Every reference printed on the silkscreen of a revision not yet made is 1.0 mm high and wide, with a 0.15 mm stroke, as 970 of the family's 991 already were. `Tools/revision-audit/audit.py` checks it. Resized: the ACE Board 1.1's BT1 (from 1.4 mm) and the ACE CF Adapter 1.1's J2 (from 1.27 mm with a 0.254 mm stroke). Each grew or shrank about its own centre, clear of pads and other silk. Silk only: no copper moved, and no label changed. The made revisions keep their silk as made.

**IC designators and values, 2026-11-13.** On every revision not yet made, each IC's designator sits centred at one short end of its footprint, the text running along that end, and a through-hole IC's value sits at the other end. Where the centre is taken, the text is aligned to the end's left or right edge. A surface-mount IC's value is hidden, because a small package leaves no room for it. A ZIF socket's texts sit on its silk outline, not its lever. `Tools/revision-audit/audit.py` checks the values. The ACE Board 1.1 already follows the rule, and the ACE CF Adapter 1.1 has no IC, so nothing here changed.

**The board logo's place, 2026-11-13.** Every board logo on a revision not yet made sits in one place for its kind of board. A card's or cart's logo reads bottom to top on the left, 2.5 mm from the edge and centred on the body; any other board's runs along its edge on the line of that edge's corner holes, centred or with its end 11.5 mm from the corner (`Tools/logos/standard.json`, checked by `Tools/logos/placement.py`). Moved, each by at most 2.5 mm: ACE Board 1.1 and ACE CF Adapter 1.1. Silk only: no copper moved, DRC is unchanged, and no label changed. The made revisions keep their logos where they are.

**JLCPCB's order-number marker, 2026-11-13.** The `JLCJLCJLCJLC` text is gone from the silkscreen of every revision not yet made: ACE Board 1.1 and ACE CF Adapter 1.1. It told JLCPCB where to print its order number. JLCPCB stopped printing order numbers in May 2026, and its help page now asks for the text not to be there. Only the front silkscreen changed, so no label did. The made revisions keep the text, which JLCPCB ignores.

**Schematic drawing, 2026-11-06.** Every schematic's 6502 bus, cart and card connectors are drawn one way, made revisions included: a short wire and a global label on each used pin, a no-connect flag on each unused one, and GND and VCC as global labels. Bus lines, bus entries and local labels for the bus are gone. Each label's name matches the board's silk. Where pins 4 and 6 carry `EXP1` and `EXP0`, or a cartridge grounds them, a note on the schematic says what `HRDB` does with them (see the README's *Extra pins*). No netlist changed, so no board did: the schematic PDFs are regenerated, and a few PCB files carry the new net names, as text only.

### ACE CF Adapter

**Rev 1.1** (drawn, not yet made; Rev 1.0 is sold first)

- Annotated properly: `J21` is now `J1`, and `J3` is now `J2`. Rev 1.0 was never annotated, so those two numbers came from another project.
- The CF socket has an LCSC source, [C2962036](https://www.lcsc.com/product-detail/C2962036.html) (HOAUC HYCW01-CF50-395B), and JLCPCB's parts library lists it as an Extended part, with 457 in stock on 2026-11-04. On its datasheet it matches the footprint: 50 pads at 0.635 mm, locating holes 38.78 mm apart against the footprint's 38.74, and hold-down tabs in the same place. It hasn't been fitted to a board yet, so the first Rev 1.1 build will prove it.

**Rev 1.0**

- Initial release, and the board on sale. `Hardware/ACE CF Adapter/Rev 1.0/` and `Production/ACE CF Adapter/Rev 1.0/` match the boards JLCPCB made (order Y89). The Gerbers and drill files in the production zip are byte-for-byte what JLCPCB received. Its CF socket is hand-soldered: `101D-TAAB-R01`, in [BOM.md](BOM.md#ace-cf-adapter).

### ACE RAM Patch

**Rev 1.1**

- Replaces Rev 1.0, and fixes the decode. Tested on 2026-11-03. `Hardware/ACE RAM Patch/Rev 1.1/` and `Production/ACE RAM Patch/Rev 1.1/` match the boards JLCPCB made (order Y99). The Gerbers and drill files in the production zip are byte-for-byte what JLCPCB received.

**Rev 1.0**

- Initial release. Boards were made, and testing showed its decode is wrong, so don't fit one: use Rev 1.1. `Hardware/ACE RAM Patch/Rev 1.0/` and `Production/ACE RAM Patch/Rev 1.0/` match the boards JLCPCB made (order Y94). The Gerbers and drill files in the production zip are byte-for-byte what JLCPCB received.

### ACE Board

**Rev 1.1**

- Fixes the gating of the `LOADL` and `LOADH` latch-enable signals for the 74HC573 latches (`U21`, `U22`) that drive the AS6C4008 banked SRAM. In Rev 1.0 the final two decode gates (`U13C`/`U13D`) were NANDs, which left the latches pulsing while idle and allowed spurious loads on reads, so the latches never reliably held a bank value.
- The fix replaces the final NAND stage with a NOR function: `LOADL = NOR(SEL_L, WB)` and `LOADH = NOR(SEH_L, WB)`, holding each latch enable low out of window and only pulsing on an in-window write. This makes banked RAM work correctly with no firmware change.
- Implemented with one 74HC02 quad NOR beside the 74HC00 `U12`. Rev 1.0's second 74HC00 in this path is gone, and its designator, `U13`, now belongs to the 74HC02. Every gate of both chips is in use — the same eight gates as the ACE RAM Patch Rev 1.1: `U12A` makes `/(A9·A8)`; `U13C` NORs it with `U17`'s `/(A0–A7)` to select the bank register; `U13D` makes IO1 from `IO1B` and `U12D` makes `B18` from `IO2B`; `U12B` and `U12C` combine the select with IO1 and with `B18`; and `U13A` and `U13B` NOR those with `WB` to make `LOADL` and `LOADH`.
- Fixes the bank register's address decode. `U12B` combined `/(A9·A8)` (`U12A`) and `/(A0–A7)` (`U17`) with a NAND, which ORs the two conditions, so each latch also loaded on every write to `$8300`–`$83FE` and `$80FF`, `$81FF`, `$82FF` (and the same in the `$8400` window). `U13C` now combines them with a NOR, so each latch loads only on a write to `$83FF` or `$87FF`.
- `J1`, PHI2 SELECT, picks the CPU clock as on Rev 1.0: 1 MHz on pins 1 and 2, the standard, or 2 MHz on pins 2 and 3, at the builder's risk (tested 2026-11-11). Its middle pin is `PHI2` for the 65C02, the VIA, the ACIA, the SID and both slots, so the SID follows the CPU's clock. On Rev 1.0 the SID stays on U5's 1 MHz output (Q3) whatever `J1` says, and at 2 MHz it answers only every other access. Rev 1.1 was first drawn 1 MHz only, with `J1` removed (2026-09-24); The 2 MHz tests of 2026-11-11 brought it back.
- Adds the ACIA's optional crystal parts, as on the COB Serial Card: `R38` (1M) across XTLI and XTLO through solder jumper `JP1`, and `C32` (22 pF) from XTLI to ground through `JP2`. Both jumpers ship open, for the R6551AP. Close both for a Rockwell R65C51P1 or R65C51P2, whose oscillator won't start on a bare crystal (an R65C51P2 ran clean this way on a Serial Card on 2026-11-11), or for a WDC W65C51.
- U14, the 74HC00 that makes `RB` and `WB` from `PHI2` and `RWB`, is a 74HCT00 (2026-11-11). Its TTL input threshold ends `RB` and `WB` a few nanoseconds later after `PHI2` falls. With an Alliance AS6C62256 at U7, a fast-releasing 74HC00 lot at U14 misread at 2 MHz. A 74HCT00 there, in a Rev 1.0 with the ACE RAM Patch, ran an hour's read-and-write soak at 2 MHz clean, and every other part its `WB` strobes (the banked RAM, the RTC, the CF card) took writes cleanly at 1 MHz. Rev 1.0 keeps its 74HC00; a 74HCT00 fits the same socket.
- Adds `D4` (BAT85) between the video card's `/INT` (U3 pin 16) and `IRQB`, cathode toward U3. The Pico9918 drives `/INT` high as well as low, and without the diode it held `IRQB` high against every other interrupt source.
- Adds `R37`, a 10kΩ pull-up on `RESB`. The AB Controller firmware now only ever pulls `RESB` low, so the DS1511Y and cards on `CART` and `BUS` can reset the machine too.
- Adds `D5` (1N5819) in series between the barrel jack (`J16`) and the power switch (`SW68`), anode at the jack, so a reversed supply can't reach VCC. It drops about 0.3–0.4 V, so VCC sits near 4.6 V, above the 4.5 V floor of the 5 V parts. Measure VCC under full load on the first board built.
- `Tests/check-schematics.mjs` checks the address decoding of Rev 1.1, and of Rev 1.0 with the ACE RAM Patch Rev 1.1 fitted, in every bus state. See [Checking the schematics](README.md#checking-the-schematics).
- Some pull-up resistors changed from 1kΩ to 10kΩ: `R2`–`R5` and `R27` are now 10kΩ.
- Removes Rev 1.0's `R1`, the `SOB` pull-up. `SOB` is tied straight to VCC.
- Added `C31` (10µF electrolytic) at the power input for bulk decoupling capacitance.
- Keeps Rev 1.0's designators, so the two revisions can be compared part for part (owner, 2026-11-11: a part keeps its number from one revision to the next). Parts new in Rev 1.1 take numbers Rev 1.0 never used: `D4` (BAT85), `D5` (1N5819), `R37` (the `RESB` pull-up) and `C31` (the bulk capacitor). The 74HC02 takes `U13`, the number of the Rev 1.0 74HC00 it replaces. A removed part's number is left unused. Rev 1.1 was re-annotated from 1 on 2026-09-24, and put back on 2026-11-11.
- The silkscreen says `SERIAL (DTE)` at `J12`, `MAX238CNG+` at `U10`, `ATmega1284` at `U6`, `ARMSID` at `U9`, `16 MHz` at `X1` and `1.8432 MHz` at `Y1`. Rev 1.0's say `DB9 MALE (DTE)`, `MAX238xNG+`, `ATmega1284-P`, `6581`, `16MHz` and `1.8432 Mhz`.
- Removes Rev 1.0's `J5`, the `VDD` header for a real SID's 12 V supply, which the standard build never provided and which was never tested. `U9` pin 28 is left unconnected: the ARMSID needs nothing there. Its number, `J5`, is left unused.

**Rev 1.0**

- Initial release, ordered from JLCPCB on 2026-05-13.
- `Hardware/ACE Board/Rev 1.0/` and `Production/ACE Board/Rev 1.0/` match that order, so their designators are the ones on the silkscreen. The Gerbers and drill files in the production zip are byte-for-byte what JLCPCB received.
