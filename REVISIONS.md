# Revisions

Every revision of every board in this repository, and what is known about each. The audit date is at the end.

**Status** says what has happened to a revision:

- **Made, checked:** JLCPCB's own copy of the order is byte-identical to the production zip here. The revision's files match that board.
- **Made, not checked:** the board exists, but its files haven't been compared with an order.
- **Ordered:** placed, and not yet arrived.
- **Drawn:** the files are complete, and the board hasn't been ordered.
- **Never made**, or **To confirm** where nothing on record says either way.

**Holes** is how far the corner mounting holes sit from the board's edges. The standard is 6 mm, and 5 mm on the ACE Board, the CF Adapter and the Keyboard Helper. A dash means a card or cart, which has no corner holes.

| Board | Rev | Status | Order | Ordered | Made from | Tindie stock | Size (mm) | Holes | Top panel | Enclosure | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ACE Board | 1.0 | Made, checked | Y91 | 2026-05-13 | `6502-ACE 83b1b1a` | — | 335×250 | 5 mm | yes | — |  |
| ACE Board | 1.1 | Drawn |  |  |  | — | 335×250 | 5 mm | yes | — |  |
| ACE CF Adapter | 1.0 | Made, checked | Y89 | 2026-05-10 | `6502-ACE ef6370e` | — | 75×50 | 5 mm | yes | — |  |
| ACE RAM Patch | 1.0 | To confirm |  |  |  | — | 46×22 | — | — | — |  |
| ACE RAM Patch | 1.1 | Made, not checked |  |  |  | — | 92.5×13 | — | — | — | fitted and tested 2026-11-03 |

The audit last ran on 2026-11-04. Each production zip marked *Made, checked* was compared byte for byte with JLCPCB's copy, and its PCB regenerated to the same copper, mask, outline and holes. Tindie stock is from the listings as saved on 2026-10-23.
