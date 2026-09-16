# VDP assessment: 6502-ACE

> An outline, not a plan. The detailed plan for this repository goes in `VDP-PLAN.md`,
> written in a session of its own. Surveyed 2026-09-16 across the whole workspace.

## The change

The ACE moves from a Pico9918 running stock TMS9918A firmware to the **6502-PICOVDP**
(`6502-PICOVDP/SPEC.md`) on PICO9918 PRO v2.0 hardware, running **BIOS 2.x**. Everything
else stays where it is: COB, DEV, KIM, VCS, PicoCalc, and any ACE whose card cannot be
reflashed (RP2040 pico9918 v1.0–1.3). Those keep the stock firmware and **BIOS 1.x (1.5)**.

- **Legacy** in these documents means TMS9918A + BIOS 1.x. **VDP** means PICOVDP + BIOS 2.x.
- **Compatibility runs one way.** The PICOVDP's legacy submode runs Text and Graphics I
  programs unchanged, so BIOS 1.5 and existing cartridges run on it. Graphics II and
  Multicolor fall back to Graphics I and draw garbage. Register writes above 7 no longer
  alias, so F18A tricks break. Sprites per line are 16 by default, not 4. Nothing written
  for the VDP runs on a TMS9918A.
- **BIOS 2.0 is assumed to be:** BIOS 1.5, plus the NVRAM save slots in
  `6502-BIOS/PLAN.md`, plus the VDP work in `6502-EMULATOR`'s
  `docs/handoff/6502-BIOS.md` (branch `v3-vdp`). Existing jump-table addresses stay put.
  A later BIOS redesign may revise this.

## Decisions already made

- No new repositories.
- **6502-EMULATOR** makes the video card an option (TMS9918A or PICOVDP): one app, one
  site. It also publishes a frozen 2.6.9 web build at a versioned path for the legacy docs.
- **6502-DOCS** is versioned: legacy docs are frozen at `/6502-DOCS/v1/`, and the main
  site is rewritten for the VDP.
- **6502-BIOS** gets a `v1.x` maintenance branch; `main` becomes 2.x.
- **Assembly and C projects** get a VDP include chosen by a build option, not branches.
- **EhBASIC and vc83basic** stay 1.x. **PicoCalc** stays legacy. **The YouTube series**
  teaches the legacy VDP and mentions the new features.

## Order across the workspace

1. **6502-PICOVDP:** firmware proven on the PRO (its Phases 9–11). This gates the
   hardware switch, not the software work.
2. **6502-EMULATOR:** frozen 2.6.9 web build at `/6502-EMULATOR/v2/`.
3. **6502-DOCS:** `v1` branch published at `/6502-DOCS/v1/`, embeds pinned to step 2.
4. **6502-EMULATOR:** `v3-vdp` merged, with the card as an option; tagged 3.x.
5. **6502-BIOS:** `v1.x` cut; 2.0 built on `main`. This can start any time, because the
   `v3-vdp` emulator already runs the PICOVDP.
6. **6502-ASM** sets the VDP include convention. 6502-CRT, 6502-PRG, 6502-BIN and 6502-C
   follow it.
7. The emulator bundles BIOS 2.0. 6502-DOCS `main` is rewritten. 6502-ACE, bastok,
   WIZARDSLAB, 6502-EHBASIC, vc83basic and 6502-ASSEMBLY follow.

---

## This repository's role

The ACE's hardware: KiCad design, BOM, production files, and the AB Controller keyboard
firmware. **It is the only hardware repository affected.** COB, DEV, KIM and VCS stay
legacy.

## Where it stands

- `README.md` specs: "Video: Pico9918 (VGA 640×480)".
- BOM line U3: "Pico9918A, VDP (VGA)", linking the Tindie PICO9918 PRO listing.
- `Firmware/` holds only the AB Controller (unaffected).

## Work outline

**Blocked on 6502-PICOVDP's firmware being proven on the PRO.**

1. **No board change is expected.** The PICOVDP is designed for the PRO v2.0 with "no
   hardware modification required" (SPEC §2). Confirm against the schematic during
   PICOVDP Phases 9–11:
   - Slot 8 already decodes `$9C00`–`$9FFF`.
   - The four ports use A1:A0.
   - /INT routing.
   If anything differs, that becomes a board revision item here.
2. **BOM.** U3 specifically requires a **PICO9918 PRO v2.0** (RP2354A). RP2040 boards
   (v1.0–1.3) cannot run the PICOVDP.
3. **README: specs and firmware.**
   - Video becomes "6502-PICOVDP on PICO9918 PRO v2.0", with the VGA output resolution
     from the SPEC.
   - Add firmware steps: flash the PICOVDP UF2 (release from 6502-PICOVDP) and program
     the EEPROM with BIOS 2.x.
4. **README: existing boards.**
   - An ACE on stock pico9918 firmware (or with an RP2040 board) is a legacy system: BIOS
     1.5, and the `/6502-DOCS/v1/` docs.
   - Reflashing a PRO v2.0 plus a BIOS 2.x EEPROM converts it.
   - BIOS 1.5 also runs on the new card.
5. **Family table.** The README's related-systems table might note which systems are
   legacy. The plan decides whether that belongs here or only in 6502-DOCS.

## Linked repositories

| Repository | Path | Why |
|---|---|---|
| 6502-PICOVDP | `~/Developer/C/6502-PICOVDP` | Firmware release; SPEC §2 hardware requirements; bench confirmation |
| 6502-BIOS | `~/Developer/Assembly/6502-BIOS` | BIOS 2.x EEPROM image |
| 6502-DOCS | `~/Developer/NodeJS/6502-DOCS` | `docs/the-ace.md`, getting-started pages and the ace card follow this README |
