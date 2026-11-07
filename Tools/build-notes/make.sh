#!/bin/zsh
# Builds the ACE Board Rev 1.0 build notes into this repository (6502-ACE). Reads both boards' PCB files,
# so a figure can't drift from the board it shows. Needs KiCad, Python 3 and Chrome.
ACE=${ACE:-${0:A:h:h:h}}   # this repository: make.sh is in Tools/build-notes/
cd "$(dirname "$0")" || exit 1
OUT="$ACE/Docs/ACE Board/Rev 1.0/ACE Board Build Notes.pdf"
KC=/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p svg "$(dirname "$OUT")" "$TMP/p" "$TMP/a"
python3 strip_models.py "$ACE/Hardware/ACE RAM Patch/Rev 1.1/ACE RAM Patch.kicad_pcb" "$TMP/p/p.kicad_pcb" || exit 1
python3 strip_models.py "$ACE/Hardware/ACE Board/Rev 1.0/ACE Board.kicad_pcb" "$TMP/a/a.kicad_pcb" || exit 1
for s in F B; do
  M=(); [ $s = B ] && M=(--mirror)
  $KC pcb export svg --mode-single --black-and-white --exclude-drawing-sheet --page-size-mode 2 $M --layers "$s.Silkscreen,$s.Mask,Edge.Cuts" -o svg/patch-$s.svg "$TMP/p/p.kicad_pcb" >/dev/null || exit 1
  $KC pcb export svg --mode-single --black-and-white --exclude-drawing-sheet --page-size-mode 2 $M --layers "$s.Silkscreen,$s.Mask,Edge.Cuts" -o svg/ace-$s.svg "$TMP/a/a.kicad_pcb" >/dev/null || exit 1
done
python3 build.py || exit 1
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --allow-file-access-from-files --user-data-dir="$TMP/chrome" --print-to-pdf="$OUT" --virtual-time-budget=8000 "file://$PWD/notes.html" >/dev/null 2>&1
ls -la "$OUT"
