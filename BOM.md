# Bill of materials: 6502-ACE

Every part for every board in this repository, by revision, with supplier numbers.

## How to use this

1. **Find your board and revision** in [Which revision do I have?](#which-revision-do-i-have)
2. **Read the [known issues](#known-issues)** for that revision, because they change what you buy or fit.
3. **Order from the table for your revision.** Each revision links to files you can upload to Digi-Key and Mouser. Those files are for one board, so multiply the quantities if you're building more. If a site asks which column is which, the first column is its part number and the third is the quantity. A cart only holds what that supplier sells, so check the table for anything else, such as chips from Jameco.

**Pre-soldered parts.** Some boards on Tindie come with their surface-mount parts already soldered. Parts marked **Yes** under Pre-soldered are the ones soldered on those boards. Check your listing, because others are sold as a bare PCB. Each revision that has such parts also has a `through-hole` cart that leaves them out. To solder a bare board yourself, use the full cart.

**Suppliers.** Every part has one set of numbers, so the same resistor is the same order line on every board. The numbers were read from Digi-Key and Mouser on 2026-11-04, and stock changes. A blank supplier cell means that supplier doesn't sell the part, or only sells it in bulk.

**The `bom.csv` files** under `Production/` are for JLCPCB assembly. They list the same parts. A blank LCSC cell there means JLCPCB doesn't place that part, and JLCPCB's "missing parts" warning about it is expected.

## Which revision do I have?

Look on the board: the silk prints the revision next to the copyright line. [REVISIONS.md](REVISIONS.md) has the facts for each one, and the [README](README.md) lists what changed between them.

| Board | Revision | What the silk says | Status |
|---|---|---|---|
| [ACE Board](#ace-board) | 1.0 | Rev 1.0 | Made, tested |
| [ACE Board](#ace-board) | 1.1 | Rev 1.1 | Drawn, not made yet |
| [ACE CF Adapter](#ace-cf-adapter) | 1.0 | Rev 1.0 | Made, tested |
| [ACE CF Adapter](#ace-cf-adapter) | 1.1 | Rev 1.1 | Drawn, not made yet |
| [ACE RAM Patch](#ace-ram-patch) | 1.0 | Rev 1.0 | Made. Failed: Rev 1.1 replaces it |
| [ACE RAM Patch](#ace-ram-patch) | 1.1 | Rev 1.1 | Made. Yes, 2026-11-03 |

## Known issues

These change what you buy or fit. The boards themselves stay as they were made.

| Board | Revision | Parts | Issue |
|---|---|---|---|
| ACE Board | 1.0 | R1–R5, R27 | Fit 10k, not the 1k in the original files. See the build notes. |
| ACE Board | 1.0 | U4 | The silk says 65C51; fit an R6551AP. |
| ACE Board | 1.0 | J16 | `DCJ200-10-A-K1-K` is obsolete, so stock will run out. A replacement that fits this footprint is still being looked for. Pads 1 and 2 are 6.0 mm apart, and pad 3 is 3 mm along and 4.7 mm to the side. |
| ACE Board | 1.0 | BT1 | `BAT-HLD-001-THM`, on the tested boards, is obsolete. `BAT-HLD-001-THM-TR` is its listed continuation, with no stock today and no board built with it yet. |
| ACE Board | 1.1 | J16 | `DCJ200-10-A-K1-K` is obsolete, so stock will run out. A replacement that fits this footprint is still being looked for. Pads 1 and 2 are 6.0 mm apart, and pad 3 is 3 mm along and 4.7 mm to the side. |
| ACE Board | 1.1 | BT1 | `BAT-HLD-001-THM`, on the tested boards, is obsolete. `BAT-HLD-001-THM-TR` is its listed continuation, with no stock today and no board built with it yet. |
| ACE RAM Patch | 1.0 |  | Boards were made, and testing showed the decode is wrong. Do not fit one: use Rev 1.1. |

### Build notes

These come from the README.

**ACE Board**

**Building a Rev 1.0**

Rev 1.0 is the board on sale. Rev 1.1 fixes each of these on the board; on a Rev 1.0 they're done by hand. The [build notes](Docs/ACE%20Board/Rev%201.0/ACE%20Board%20Build%20Notes.pdf) have each step, with figures and checks.

- **Pull-ups:** fit 10kΩ for `R1`–`R5` and `R27`, not the 1kΩ in Rev 1.0's BOM. Don't leave out `R1`: it is the only thing holding `SOB` (U1 pin 38) high.
- **ACIA:** fit an R6551AP at `U4`, where Rev 1.0's silkscreen and BOM say 65C51.
- **Supply capacitor:** fit a 10µF electrolytic on the underside, across the pads of `J19`, the VCC header. Rev 1.0 has no holes for it.
- **`RESB`:** flash the AB Controller firmware from this repository, which only ever pulls `RESB` low (see [AB Controller](README.md#ab-controller)); older firmware drove it high as well, so nothing else could reset the machine. A 10kΩ pull-up from `RESB` to 5 V, soldered on the underside, is optional: the ATmega's internal pull-up raises the line on its own, but the 10 k is stiffer on a line that runs out to `CART` and `BUS`.
- **Video card `/INT`:** fit a BAT85 between U3 pin 16 and `IRQB`, cathode toward the card, in a socket stack under the card with pin 16 routed through the diode. Without it, a PICO9918 PRO holds `IRQB` at 3.8 V while the VIA asserts it, and the keyboard and serial input are dead. A v1.3 has the same circuit and only works by luck.
- **Clock:** keep the PHI2 SELECT jumper (J1) on its 1 MHz pins, 1 and 2.
- **Banked RAM:** fit the [ACE RAM Patch](README.md#ace-ram-patch) Rev 1.1 in place of U12 and U13.
- **Power:** use a center-positive 5 V supply only. Nothing protects Rev 1.0 from reverse polarity.


## ACE Board

### ACE Board Rev 1.1

Drawn, not made yet.

Cart files: [digikey.csv](BOM/ACE%20Board/Rev%201.1/digikey.csv), [mouser.csv](BOM/ACE%20Board/Rev%201.1/mouser.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other |
|---|---|---|---|---|---|---|
| BT1 | 1 | CR2032 | TE Connectivity Linx BAT-HLD-001-THM-TR | [343-BAT-HLD-001-THM-TRCT-ND](https://www.digikey.com/en/products/filter?keywords=343-BAT-HLD-001-THM-TRCT-ND) |  |  |
| C1, C9–C19, C21–C31 | 23 | 100nF | KYOCERA AVX SR205C104KAR | [478-3187-ND](https://www.digikey.com/en/products/filter?keywords=478-3187-ND) | [581-SR205C104KAR](https://www.mouser.com/ProductDetail/581-SR205C104KAR) |  |
| C2, C3, C5, C6, C8 | 5 | 1uF | KYOCERA AVX SR205E105MAR | [478-7667-ND](https://www.digikey.com/en/products/filter?keywords=478-7667-ND) | [581-SR205E105MAR](https://www.mouser.com/ProductDetail/581-SR205E105MAR) |  |
| C4, C7 | 2 | 2.2nF | KYOCERA AVX SR155C222KAR | [478-11698-ND](https://www.digikey.com/en/products/filter?keywords=478-11698-ND) | [581-SR155C222KAR](https://www.mouser.com/ProductDetail/581-SR155C222KAR) |  |
| C20 | 1 | 10uF | Panasonic EEA-GA1C100 | [P14482-ND](https://www.digikey.com/en/products/filter?keywords=P14482-ND) | [667-EEA-GA1C100](https://www.mouser.com/ProductDetail/667-EEA-GA1C100) |  |
| D1, D3, D4 | 3 | BAT85 | Vishay BAT85S-TR | [BAT85SCT-ND](https://www.digikey.com/en/products/filter?keywords=BAT85SCT-ND) | [78-BAT85S](https://www.mouser.com/ProductDetail/78-BAT85S) |  |
| D2 | 1 | POWER LED | Würth Elektronik 151031VS06000 | [732-5008-ND](https://www.digikey.com/en/products/filter?keywords=732-5008-ND) | [710-151031VS06000](https://www.mouser.com/ProductDetail/710-151031VS06000) |  |
| D5 | 1 | 1N5819 | Vishay 1N5819-E3/54 | [1N5819-E3/54GICT-ND](https://www.digikey.com/en/products/filter?keywords=1N5819-E3%2F54GICT-ND) | [625-1N5819-E3](https://www.mouser.com/ProductDetail/625-1N5819-E3) |  |
| J1 | 1 | CTS EN | Pin header 1×3, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J2 | 1 | RESET SW | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J3 | 1 | DCD EN | Pin header 1×3, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J4 | 1 | VDD | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J5 | 1 | JOYSTICK A | Amphenol D09P33E4GX00LF | [609-1481-ND](https://www.digikey.com/en/products/filter?keywords=609-1481-ND) | [649-D09P33E4GX00LF](https://www.mouser.com/ProductDetail/649-D09P33E4GX00LF) |  |
| J6 | 1 | PADDLES | Pin header 1×4, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J7 | 1 | JOYSTICK B | Amphenol D09P33E4GX00LF | [609-1481-ND](https://www.digikey.com/en/products/filter?keywords=609-1481-ND) | [649-D09P33E4GX00LF](https://www.mouser.com/ProductDetail/649-D09P33E4GX00LF) |  |
| J8 | 1 | PORT B | Adam Tech BHR-12-VUA | [2057-BHR-12-VUA-ND](https://www.digikey.com/en/products/filter?keywords=2057-BHR-12-VUA-ND) | [737-BHR-12-VUA](https://www.mouser.com/ProductDetail/737-BHR-12-VUA) | 2057-BHR-12-VUA-ND |
| J9 | 1 | PORT A | Adam Tech BHR-12-VUA | [2057-BHR-12-VUA-ND](https://www.digikey.com/en/products/filter?keywords=2057-BHR-12-VUA-ND) | [737-BHR-12-VUA](https://www.mouser.com/ProductDetail/737-BHR-12-VUA) | 2057-BHR-12-VUA-ND |
| J10 | 1 | AUDIO L | Switchcraft Inc. PJRAN1X1U02X | [PJRAN1X1U02X-ND](https://www.digikey.com/en/products/filter?keywords=PJRAN1X1U02X-ND) | [502-PJRAN1X1U02X](https://www.mouser.com/ProductDetail/502-PJRAN1X1U02X) |  |
| J11 | 1 | SERIAL (DTE) | Amphenol D09P33E4GX00LF | [609-1481-ND](https://www.digikey.com/en/products/filter?keywords=609-1481-ND) | [649-D09P33E4GX00LF](https://www.mouser.com/ProductDetail/649-D09P33E4GX00LF) |  |
| J12 | 1 | PS/2 | Kycon, Inc. KMDGX-6S-BS | [2092-KMDGX-6S-BS-ND](https://www.digikey.com/en/products/filter?keywords=2092-KMDGX-6S-BS-ND) | [806-KMDGX-6S-BS](https://www.mouser.com/ProductDetail/806-KMDGX-6S-BS) |  |
| J13 | 1 | KEYBOARD | Adam Tech 2PH1-16-UA | [2057-2PH1-16-UA-ND](https://www.digikey.com/en/products/filter?keywords=2057-2PH1-16-UA-ND) | [737-2PH1-16-UA](https://www.mouser.com/ProductDetail/737-2PH1-16-UA) |  |
| J14 | 1 | AUDIO R | Switchcraft Inc. PJRAN1X1U03X | [PJRAN1X1U03X-ND](https://www.digikey.com/en/products/filter?keywords=PJRAN1X1U03X-ND) | [502-PJRAN1X1U03X](https://www.mouser.com/ProductDetail/502-PJRAN1X1U03X) |  |
| J15 | 1 | AUDIO | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J16 | 1 | 5V DC | GCT DCJ200-10-A-K1-K | [2073-DCJ200-10-A-K1-K-ND](https://www.digikey.com/en/products/filter?keywords=2073-DCJ200-10-A-K1-K-ND) | [640-DCJ200-10-A-K1-K](https://www.mouser.com/ProductDetail/640-DCJ200-10-A-K1-K) |  |
| J17 | 1 | CART | TE Connectivity 5-5530843-4 | [A31723-ND](https://www.digikey.com/en/products/filter?keywords=A31723-ND) | [571-5-5530843-4](https://www.mouser.com/ProductDetail/571-5-5530843-4) |  |
| J18 | 1 | BUS | Würth Elektronik 61204021621 | [732-5401-ND](https://www.digikey.com/en/products/filter?keywords=732-5401-ND) | [710-61204021621](https://www.mouser.com/ProductDetail/710-61204021621) |  |
| J19 | 1 | VCC | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J20 | 1 | POWER LED | Pin header 1×2, 2.54 mm, cut from a strip | [S1011EC-40-ND](https://www.digikey.com/en/products/filter?keywords=S1011EC-40-ND) | [200-TSW14007TS](https://www.mouser.com/ProductDetail/200-TSW14007TS) |  |
| J21 | 1 | STORAGE | Sullins PPPC102LJBN-RC | [S5563-ND](https://www.digikey.com/en/products/filter?keywords=S5563-ND) |  |  |
| R1–R5, R26 | 6 | 10k | YAGEO MFR-12FTF52-10K | [13-MFR-12FTF52-10KCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-10KCT-ND) | [603-MFR-12FTF52-10K](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-10K) |  |
| R6–R24, R27–R35 | 28 | 1k | YAGEO MFR-12FTF52-1K | [13-MFR-12FTF52-1KCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-1KCT-ND) | [603-MFR-12FTF52-1K](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-1K) |  |
| R25 | 1 | 330 | YAGEO MFR-12FTF52-330R | [13-MFR-12FTF52-330RCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-330RCT-ND) | [603-MFR-12FTF52-330R](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-330R) |  |
| SW1–SW16, SW18–SW68 | 67 | Keyswitch | Cherry Americas LLC MX2A-E1NA | [1644-MX2A-E1NA-ND](https://www.digikey.com/en/products/filter?keywords=1644-MX2A-E1NA-ND) | [540-MX2A-E1NA](https://www.mouser.com/ProductDetail/540-MX2A-E1NA) |  |
| SW17 | 1 | RESET | Same Sky (Formerly CUI Devices) TS02-66-50-BK-160-LCR-D | [2223-TS02-66-50-BK-160-LCR-D-ND](https://www.digikey.com/en/products/filter?keywords=2223-TS02-66-50-BK-160-LCR-D-ND) | [179-TS026650BK160LCR](https://www.mouser.com/ProductDetail/179-TS026650BK160LCR) |  |
| SW69 | 1 | POWER | E-Switch 400MSP1R6BLKM6QE | [EG4326-ND](https://www.digikey.com/en/products/filter?keywords=EG4326-ND) | [612-400MSP1R6BLKM6QE](https://www.mouser.com/ProductDetail/612-400MSP1R6BLKM6QE) |  |
| SW70 | 1 | IO ENABLE | CTS Electronic Components 206-8 | [CT2068-ND](https://www.digikey.com/en/products/filter?keywords=CT2068-ND) | [774-2068](https://www.mouser.com/ProductDetail/774-2068) |  |
| U1 | 1 | 65C02 | Western Design Center (WDC) W65C02S6TPG-14 |  | [955-W65C02S6TPG-14](https://www.mouser.com/ProductDetail/955-W65C02S6TPG-14) |  |
| U2 | 1 | 65C22 | Western Design Center (WDC) W65C22N6TPG-14 |  | [955-W65C22N6TPG-14](https://www.mouser.com/ProductDetail/955-W65C22N6TPG-14) |  |
| U3 | 1 | Pico9918A | Pico9918A, DIP-40_W15.24mm |  |  | [Tindie](https://www.tindie.com/products/visrealm/pico9918-pro/) |
| U4 | 1 | R6551AP | Rockwell R6551AP |  |  | [Jameco 43318](https://www.jameco.com/z/R6551AP-Rockwell-IC-6551-Asynchronous-Communication-Interface-Adapter-DIP-28-pin_43318.html) |
| U5 | 1 | 74HC163 | Texas Instruments SN74HC163N | [296-8246-5-ND](https://www.digikey.com/en/products/filter?keywords=296-8246-5-ND) | [595-SN74HC163N](https://www.mouser.com/ProductDetail/595-SN74HC163N) |  |
| U6 | 1 | ATmega1284 | Microchip Technology ATMEGA1284-PU | [ATMEGA1284-PU-ND](https://www.digikey.com/en/products/filter?keywords=ATMEGA1284-PU-ND) | [556-ATMEGA1284-PU](https://www.mouser.com/ProductDetail/556-ATMEGA1284-PU) |  |
| U7 | 1 | AS6C62256 | Alliance Memory AS6C62256-55PCN | [1450-1033-ND](https://www.digikey.com/en/products/filter?keywords=1450-1033-ND) | [913-AS6C62256-55PCN](https://www.mouser.com/ProductDetail/913-AS6C62256-55PCN) |  |
| U8 | 1 | AT28C256 | Microchip Technology AT28C256-15PU | [AT28C256-15PU-ND](https://www.digikey.com/en/products/filter?keywords=AT28C256-15PU-ND) | [556-AT28C25615PU](https://www.mouser.com/ProductDetail/556-AT28C25615PU) |  |
| U9 | 1 | 6581 | 6581, DIP-28_W15.24mm |  |  | [Retrocomp](https://retrocomp.cz/produkt?id=2) |
| U10 | 1 | MAX238CNG+ | Maxim MAX238CNG+ | [MAX238CNG+-ND](https://www.digikey.com/en/products/filter?keywords=MAX238CNG%2B-ND) | [700-MAX238CNG](https://www.mouser.com/ProductDetail/700-MAX238CNG) |  |
| U11, U12, U14, U16 | 4 | 74HC00 | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| U13 | 1 | 74HC02 | Texas Instruments SN74HC02N | [296-1564-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1564-5-ND) | [595-SN74HC02N](https://www.mouser.com/ProductDetail/595-SN74HC02N) |  |
| U15 | 1 | AS6C4008 | Alliance Memory AS6C4008-55PCN | [1450-1027-ND](https://www.digikey.com/en/products/filter?keywords=1450-1027-ND) | [913-AS6C4008-55PCN](https://www.mouser.com/ProductDetail/913-AS6C4008-55PCN) |  |
| U17 | 1 | 74HC30 | Texas Instruments CD74HC30E |  | [595-CD74HC30E](https://www.mouser.com/ProductDetail/595-CD74HC30E) |  |
| U18 | 1 | DS1511Y | Maxim DS1511Y+ | [DS1511Y+-ND](https://www.digikey.com/en/products/filter?keywords=DS1511Y%2B-ND) | [700-DS1511Y](https://www.mouser.com/ProductDetail/700-DS1511Y) |  |
| U19, U20 | 2 | 74HC138 | Texas Instruments SN74HC138N | [296-1575-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1575-5-ND) | [595-SN74HC138N](https://www.mouser.com/ProductDetail/595-SN74HC138N) |  |
| U21, U22 | 2 | 74HC573 | Texas Instruments CD74HC573E | [296-12815-5-ND](https://www.digikey.com/en/products/filter?keywords=296-12815-5-ND) | [595-CD74HC573E](https://www.mouser.com/ProductDetail/595-CD74HC573E) |  |
| X1 | 1 | 16MHz | ECS Inc. ECS-100AX-160 | [X947-ND](https://www.digikey.com/en/products/filter?keywords=X947-ND) | [520-TCF1600-X](https://www.mouser.com/ProductDetail/520-TCF1600-X) |  |
| Y1 | 1 | 1.8432 Mhz | Abracon LLC AB-1.8432MHZ-B2 | [535-9009-ND](https://www.digikey.com/en/products/filter?keywords=535-9009-ND) | [815-AB-1.8432-B2](https://www.mouser.com/ProductDetail/815-AB-1.8432-B2) |  |
| U4, U7, U9, U18 | 4 | Socket | IC socket, 28-pin, 0.6 in | [3M5481-ND](https://www.digikey.com/en/products/filter?keywords=3M5481-ND) | [517-4828-6004-CP](https://www.mouser.com/ProductDetail/517-4828-6004-CP) | |
| U8 | 1 | Socket | 28-pin ZIF socket, or an ordinary 28-pin socket | [3M2802-ND](https://www.digikey.com/en/products/filter?keywords=3M2802-ND) | [517-228-1277-00](https://www.mouser.com/ProductDetail/517-228-1277-00) | |
| U21, U22 | 2 | Socket | IC socket, 20-pin, 0.3 in | [3M5477-ND](https://www.digikey.com/en/products/filter?keywords=3M5477-ND) | [517-4820-3004-CP](https://www.mouser.com/ProductDetail/517-4820-3004-CP) | |
| U11–U14, U16, U17 | 6 | Socket | IC socket, 14-pin, 0.3 in | [3M5474-ND](https://www.digikey.com/en/products/filter?keywords=3M5474-ND) | [517-4814-3004-CP](https://www.mouser.com/ProductDetail/517-4814-3004-CP) | |
| U10 | 1 | Socket | IC socket, 24-pin, 0.3 in | [3M5466-ND](https://www.digikey.com/en/products/filter?keywords=3M5466-ND) | [517-4824-3000-CP](https://www.mouser.com/ProductDetail/517-4824-3000-CP) | |
| U1–U3, U6 | 4 | Socket | IC socket, 40-pin, 0.6 in |  |  | |
| U15 | 1 | Socket | IC socket, 32-pin, 0.6 in |  |  | |
| U5, U19, U20 | 3 | Socket | IC socket, 16-pin, 0.3 in | [3M5475-ND](https://www.digikey.com/en/products/filter?keywords=3M5475-ND) | [517-4816-3004-CP](https://www.mouser.com/ProductDetail/517-4816-3004-CP) | |

Pin headers are cut from strips, and the cart files count whole strips.

- **BT1:** Retainer for a CR2032 cell. BAT-HLD-001-THM, on the tested boards, is obsolete; this is its listed continuation. Digi-Key has none in stock today.
- **D2:** Green shown. The colour is the builder's choice.
- **J16:** Obsolete. Replacement open.
- **J18:** Male box header with a keying notch, for a 40-way ribbon cable.
- **J21:** Right-angle socket on the ACE Board; the CF Adapter plugs in here. Digi-Key only.
- **SW1–SW16, SW18–SW68:** Cherry MX2A RGB Blue, clear housing, as on the owner's Amazon kit. MX1A-E1NN (black housing) is the deeper-stocked alternative; Digi-Key CH196-ND, Mouser 540-MX1A-E1NN.
- **U4:** Rockwell R6551AP, out of production. Do not substitute a W65C51.
- **U9:** SID 6581, out of production

### ACE Board Rev 1.0

Made, tested.

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
| J16 | 1 | 5V DC | GCT DCJ200-10-A-K1-K | [2073-DCJ200-10-A-K1-K-ND](https://www.digikey.com/en/products/filter?keywords=2073-DCJ200-10-A-K1-K-ND) | [640-DCJ200-10-A-K1-K](https://www.mouser.com/ProductDetail/640-DCJ200-10-A-K1-K) |  |
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
| U7 | 1 | AS6C62256 | Alliance Memory AS6C62256-55PCN | [1450-1033-ND](https://www.digikey.com/en/products/filter?keywords=1450-1033-ND) | [913-AS6C62256-55PCN](https://www.mouser.com/ProductDetail/913-AS6C62256-55PCN) |  |
| U8 | 1 | AT28C256 | Microchip Technology AT28C256-15PU | [AT28C256-15PU-ND](https://www.digikey.com/en/products/filter?keywords=AT28C256-15PU-ND) | [556-AT28C25615PU](https://www.mouser.com/ProductDetail/556-AT28C25615PU) |  |
| U9 | 1 | 6581 | 6581, DIP-28_W15.24mm |  |  | [Retrocomp](https://retrocomp.cz/produkt?id=2) |
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
| U1–U3, U6 | 4 | Socket | IC socket, 40-pin, 0.6 in |  |  | |
| U15 | 1 | Socket | IC socket, 32-pin, 0.6 in |  |  | |
| U5, U19, U20 | 3 | Socket | IC socket, 16-pin, 0.3 in | [3M5475-ND](https://www.digikey.com/en/products/filter?keywords=3M5475-ND) | [517-4816-3004-CP](https://www.mouser.com/ProductDetail/517-4816-3004-CP) | |
| Added | 1 | | Panasonic EEA-GA1C100, 10 µF, on the underside across J19 | [P14482-ND](https://www.digikey.com/en/products/filter?keywords=P14482-ND) | [667-EEA-GA1C100](https://www.mouser.com/ProductDetail/667-EEA-GA1C100) |  |
| Added | 1 | | Vishay BAT85S-TR, for the video card /INT | [BAT85SCT-ND](https://www.digikey.com/en/products/filter?keywords=BAT85SCT-ND) | [78-BAT85S](https://www.mouser.com/ProductDetail/78-BAT85S) |  |

Pin headers are cut from strips, and the cart files count whole strips.

U12 and U13 are not listed: fit the ACE RAM Patch Rev 1.1 in their sockets. See the build notes.

- **BT1:** Retainer for a CR2032 cell. BAT-HLD-001-THM, on the tested boards, is obsolete; this is its listed continuation. Digi-Key has none in stock today.
- **D1:** Green shown. The colour is the builder's choice.
- **J16:** Obsolete. Replacement open.
- **J18:** Male box header with a keying notch, for a 40-way ribbon cable.
- **J21:** Right-angle socket on the ACE Board; the CF Adapter plugs in here. Digi-Key only.
- **SW1–SW67:** Cherry MX2A RGB Blue, clear housing, as on the owner's Amazon kit. MX1A-E1NN (black housing) is the deeper-stocked alternative; Digi-Key CH196-ND, Mouser 540-MX1A-E1NN.
- **U4:** Rockwell R6551AP, out of production. Do not substitute a W65C51.
- **U9:** SID 6581, out of production


## ACE CF Adapter

### ACE CF Adapter Rev 1.1

Drawn, not made yet.

Cart files: [digikey.csv](BOM/ACE%20CF%20Adapter/Rev%201.1/digikey.csv), [mouser.csv](BOM/ACE%20CF%20Adapter/Rev%201.1/mouser.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other |
|---|---|---|---|---|---|---|
| D1 | 1 | ACT | Würth Elektronik 151031VS06000 | [732-5008-ND](https://www.digikey.com/en/products/filter?keywords=732-5008-ND) | [710-151031VS06000](https://www.mouser.com/ProductDetail/710-151031VS06000) |  |
| J1 | 1 | STORAGE | Amphenol 68021-120HLF | [609-3338-ND](https://www.digikey.com/en/products/filter?keywords=609-3338-ND) | [649-68021-120HLF](https://www.mouser.com/ProductDetail/649-68021-120HLF) |  |
| J2 | 1 | Compact Flash | ATTEND Technology 101D-TAAB-R01 | [4827-101D-TAAB-R01-ND](https://www.digikey.com/en/products/filter?keywords=4827-101D-TAAB-R01-ND) |  | LCSC [C2962036](https://www.lcsc.com/search?q=C2962036) |
| R1–R4 | 4 | 1k | YAGEO MFR-12FTF52-1K | [13-MFR-12FTF52-1KCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-1KCT-ND) | [603-MFR-12FTF52-1K](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-1K) |  |
| R5 | 1 | 330 | YAGEO MFR-12FTF52-330R | [13-MFR-12FTF52-330RCT-ND](https://www.digikey.com/en/products/filter?keywords=13-MFR-12FTF52-330RCT-ND) | [603-MFR-12FTF52-330R](https://www.mouser.com/ProductDetail/603-MFR-12FTF52-330R) |  |

- **D1:** Green shown. The colour is the builder's choice.
- **J1:** Right-angle header on the CF Adapter; plugs into the right-angle socket on the ACE Board.
- **J2:** LCSC C2962036 is a different maker (HOAUC HYCW01-CF50-395B), matched to the footprint by datasheet and not yet built. Digi-Key has none in stock today.

### ACE CF Adapter Rev 1.0

Made, tested.

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
- **J21:** Right-angle header on the CF Adapter; plugs into the right-angle socket on the ACE Board.


## ACE RAM Patch

### ACE RAM Patch Rev 1.1

Made. Yes, 2026-11-03.

Cart files: [digikey.csv](BOM/ACE%20RAM%20Patch/Rev%201.1/digikey.csv), [mouser.csv](BOM/ACE%20RAM%20Patch/Rev%201.1/mouser.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other |
|---|---|---|---|---|---|---|
| J1 | 1 | 74HC00 (U12) | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| J2 | 1 | 74HC00 (U13) | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| U1 | 1 | 74HC00 | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| U2 | 1 | 74HC02 | Texas Instruments SN74HC02N | [296-1564-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1564-5-ND) | [595-SN74HC02N](https://www.mouser.com/ProductDetail/595-SN74HC02N) |  |

### ACE RAM Patch Rev 1.0

Made. Failed: Rev 1.1 replaces it.

Cart files: [digikey.csv](BOM/ACE%20RAM%20Patch/Rev%201.0/digikey.csv), [mouser.csv](BOM/ACE%20RAM%20Patch/Rev%201.0/mouser.csv)

| Reference | Qty | Value | Part | Digi-Key | Mouser | Other |
|---|---|---|---|---|---|---|
| J1 | 1 | 74HC00 (U13) | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| U1 | 1 | 74HC00 | Texas Instruments SN74HC00N | [296-1563-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1563-5-ND) | [595-SN74HC00N](https://www.mouser.com/ProductDetail/595-SN74HC00N) |  |
| U2 | 1 | 74HC02 | Texas Instruments SN74HC02N | [296-1564-5-ND](https://www.digikey.com/en/products/filter?keywords=296-1564-5-ND) | [595-SN74HC02N](https://www.mouser.com/ProductDetail/595-SN74HC02N) |  |
