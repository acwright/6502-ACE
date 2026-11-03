.setcpu "65C02"

; check-ram: test the ACE's banked RAM from the machine itself. Tests/check-ram.mjs
; loads this over XMODEM, runs it, and reads the report it sends to the serial port.
; It needs BIOS 2.x, and it overwrites everything in the banked RAM.
;
;   SEED    Every bank of both windows takes a marker through its latch: the bank
;           number at offset 0, and its complement at offset 1.
;   SWEEP   With bank B latched, write X (never equal to B) to every data address of
;           the window, then read every address, the register included. After each
;           access the markers must still say B: a latch that loaded would now hold
;           X and read X's markers. Then two controls. The other window's latch has
;           not moved, and a write to the register itself does move the bank to X,
;           so a stuck latch can't pass.
;   PASS    All 1023 data bytes of all 256 banks of both windows are written, and
;           only then read back, with three patterns. PASS 1 and PASS 2 are
;           complements, so every bit is seen both ways. No two banks share a
;           pattern in both PASS 1 and PASS 3, so banks that alias each other fail.
;
; Failed accesses print a line each, up to MAX_SHOWN per section, and every section
; prints how many it counted. The last lines are TOTAL and DONE.

SerialChrout := $A051

YS     = $DF
PTR    = $E0    ; 2
BASE   = $E2    ; 2
LATCH  = $E4    ; 2
OBASE  = $E6    ; 2
OLATCH = $E8    ; 2
SPTR   = $EA    ; 2
W      = $EC
BANK   = $ED
BV     = $EE
XV     = $EF
OV     = $F0
FAILS  = $F1    ; 3
PAGE   = $F4
LIMIT  = $F5
KEYL   = $F6
KEYH   = $F7
INV    = $F8
MIX    = $F9
GOT    = $FA
EXPECT = $FB
SHOWN  = $FC
GRAND  = $FD    ; 3

MAX_SHOWN = 16

.macro say str
  jsr say_inline
  .byte str, 0
.endmacro

.segment "CODE"
  .byte $0A, $08, $0A, $00, $A5, "2060", $00, $00, $00   ; 10 SYS 2060

start:
  sei
  cld
  stz GRAND
  stz GRAND+1
  stz GRAND+2
  jsr clear_fails
  say "CHECK-RAM"
  jsr crlf

  jsr seed
  say "SEED FAILS "
  jsr end_section

  lda #0
  jsr sweeps
  lda #1
  jsr sweeps

  ; PASS 1: L key $00, H key $A5
  lda #$00
  sta KEYL
  lda #$A5
  sta KEYH
  stz INV
  jsr pass
  say "PASS 1 FAILS "
  jsr end_section

  ; PASS 2: the complement of PASS 1
  lda #$FF
  sta INV
  jsr pass
  say "PASS 2 FAILS "
  jsr end_section

  ; PASS 3: other keys, so no bank in one window matches any in the other in
  ; both this pass and PASS 1
  lda #$3C
  sta KEYL
  lda #$5B
  sta KEYH
  stz INV
  jsr pass
  say "PASS 3 FAILS "
  jsr end_section

  say "TOTAL "
  lda GRAND+2
  jsr prhex
  lda GRAND+1
  jsr prhex
  lda GRAND
  jsr prhex
  jsr crlf
  say "DONE"
  jsr crlf
  stz $83FF
  stz $87FF
  cli
  rts

; ---- window selection --------------------------------------------------------

setwin:                 ; A = 0 for $8000/$83FF, 1 for $8400/$87FF
  sta W
  stz BASE
  stz OBASE
  lda #$FF
  sta LATCH
  sta OLATCH
  lda W
  beq @low
  lda #$84
  sta BASE+1
  lda #$80
  sta OBASE+1
  lda #$87
  sta LATCH+1
  lda #$83
  sta OLATCH+1
  rts
@low:
  lda #$80
  sta BASE+1
  lda #$84
  sta OBASE+1
  lda #$83
  sta LATCH+1
  lda #$87
  sta OLATCH+1
  rts

; ---- markers: offset 0 holds the bank, offset 1 its complement ----------------

chk:                    ; carry set if this window's markers don't say BV
  lda (BASE)
  cmp BV
  bne @bad
  ldy #1
  lda (BASE),y
  eor #$FF
  cmp BV
  bne @bad
  clc
  rts
@bad:
  sta GOT
  sec
  rts

chk_other:              ; carry set if the other window's markers don't say OV
  lda (OBASE)
  cmp OV
  bne @bad
  ldy #1
  lda (OBASE),y
  eor #$FF
  cmp OV
  bne @bad
  clc
  rts
@bad:
  sta GOT
  sec
  rts

seed:
  lda #0
  jsr seed_write
  lda #1
  jsr seed_write
  lda #0
  jsr seed_check
  lda #1
  ; fall through
seed_check:
  jsr setwin
  stz BANK
@loop:
  lda BANK
  sta BV
  sta (LATCH)
  jsr chk
  bcc @ok
  lda #'S'
  jsr note_bank
@ok:
  inc BANK
  bne @loop
  rts

seed_write:
  jsr setwin
  stz BANK
@loop:
  lda BANK
  sta (LATCH)
  sta (BASE)
  eor #$FF
  ldy #1
  sta (BASE),y
  inc BANK
  bne @loop
  rts

; ---- SWEEP -------------------------------------------------------------------

sweeps:                 ; A = window
  jsr setwin
  lda #$55
  ldx #$AA
  jsr sweep_one
  lda #$AA
  ldx #$55
  jsr sweep_one
  lda #$00
  ldx #$FF
  jsr sweep_one
  lda #$FF
  ldx #$00
  ; fall through
sweep_one:              ; A = bank B, X = the value X written
  sta BV
  stx XV
  eor #$3C
  sta OV
  sta (OLATCH)
  lda BV
  sta (LATCH)

  ; writes to every data address
  lda BASE+1
  sta PTR+1
  stz PTR
  stz PAGE
  ldy #0
@wloop:
  lda PAGE
  cmp #3
  bne @wgo
  cpy #$FF
  beq @reads            ; $83FF/$87FF is the register, not a data address
@wgo:
  lda XV
  sta (PTR),y
  lda PAGE
  bne @wchk
  cpy #2
  bcs @wchk
  lda BV                ; that write hit a marker: put it back
  cpy #0
  beq @wfix
  eor #$FF
@wfix:
  sta (PTR),y
@wchk:
  phy
  jsr chk
  ply
  bcc @wok
  lda #'W'
  jsr note_addr
@wok:
  iny
  bne @wloop
  inc PTR+1
  inc PAGE
  bra @wloop

  ; reads of every address, the register included. Bank B is now full of X, so
  ; a read that loaded the latch would load X
@reads:
  lda BASE+1
  sta PTR+1
  stz PAGE
  ldy #0
@rloop:
  lda (PTR),y
  phy
  jsr chk
  ply
  bcc @rok
  lda #'R'
  jsr note_addr
@rok:
  iny
  bne @rloop
  inc PTR+1
  inc PAGE
  lda PAGE
  cmp #4
  bne @rloop

  ; control: the other window's latch never moved
  jsr chk_other
  bcc @oth1
  lda #'O'
  jsr note_bank
@oth1:

  ; control: the register itself does move the bank
  lda BV
  pha
  lda XV
  sta (LATCH)
  sta BV
  jsr chk
  bcc @ctl
  lda #'C'
  jsr note_bank
@ctl:
  pla
  sta BV

  ; and that write left the other window alone too
  jsr chk_other
  bcc @oth2
  lda #'O'
  jsr note_bank
@oth2:

  say "SWEEP W"
  lda W
  jsr prhex
  say " B"
  lda BV
  jsr prhex
  say " X"
  lda XV
  jsr prhex
  say " FAILS "
  jmp end_section

; ---- PASS --------------------------------------------------------------------

mixtab: .byte $00, $35, $6A, $9F

setmix:                 ; the page's starting value, and where its loop stops
  ldx PAGE
  lda BANK
  eor mixtab,x
  ldx W
  bne @high
  eor KEYL
  bra @both
@high:
  eor KEYH
@both:
  eor INV
  sta MIX
  stz LIMIT
  lda PAGE
  cmp #3
  bne @done
  lda #$FF
  sta LIMIT
@done:
  lda BASE+1
  clc
  adc PAGE
  sta PTR+1
  rts

pass:
  lda #0
  jsr pass_write
  lda #1
  jsr pass_write
  lda #0
  jsr pass_read
  lda #1
  ; fall through
pass_read:
  jsr setwin
  stz PTR
  stz BANK
@bank:
  lda BANK
  sta (LATCH)
  stz PAGE
@page:
  jsr setmix
  ldy #0
@byte:
  tya
  eor MIX
  cmp (PTR),y
  bne @bad
@next:
  iny
  cpy LIMIT
  bne @byte
  inc PAGE
  lda PAGE
  cmp #4
  bne @page
  inc BANK
  bne @bank
  rts
@bad:
  sta EXPECT
  lda (PTR),y
  sta GOT
  phy
  jsr note_cell
  ply
  bra @next

pass_write:
  jsr setwin
  stz PTR
  stz BANK
@bank:
  lda BANK
  sta (LATCH)
  stz PAGE
@page:
  jsr setmix
  ldy #0
@byte:
  tya
  eor MIX
  sta (PTR),y
  iny
  cpy LIMIT
  bne @byte
  inc PAGE
  lda PAGE
  cmp #4
  bne @page
  inc BANK
  bne @bank
  rts

; ---- reporting ---------------------------------------------------------------

count:
  inc FAILS
  bne :+
  inc FAILS+1
  bne :+
  inc FAILS+2
:
  inc GRAND
  bne :+
  inc GRAND+1
  bne :+
  inc GRAND+2
:
  lda SHOWN
  cmp #MAX_SHOWN        ; carry set: enough printed for this section
  bcs :+
  inc SHOWN
  clc
:
  rts

note_bank:              ; A = kind. BANK/BV say what was expected
  pha
  jsr count
  pla
  bcs @out
  jsr SerialChrout
  say " W"
  lda W
  jsr prhex
  say " want "
  lda BV
  jsr prhex
  say " got "
  lda GOT
  jsr prhex
  jsr crlf
@out:
  rts

note_addr:              ; A = kind, Y and PTR the address. Puts the latch back
  sty YS
  pha
  jsr count
  pla
  bcs @fix
  jsr SerialChrout
  say " W"
  lda W
  jsr prhex
  say " addr "
  lda PTR+1
  jsr prhex
  lda YS
  jsr prhex
  say " want "
  lda BV
  jsr prhex
  say " got "
  lda GOT
  jsr prhex
  jsr crlf
@fix:
  lda BV
  sta (LATCH)
  ldy YS
  rts

note_cell:              ; a PASS byte that read back wrong, Y and PTR the address
  sty YS
  jsr count
  bcs @out
  say "P W"
  lda W
  jsr prhex
  say " bank "
  lda BANK
  jsr prhex
  say " addr "
  lda PTR+1
  jsr prhex
  lda YS
  jsr prhex
  say " want "
  lda EXPECT
  jsr prhex
  say " got "
  lda GOT
  jsr prhex
  jsr crlf
@out:
  ldy YS
  rts

clear_fails:
  stz FAILS
  stz FAILS+1
  stz FAILS+2
  stz SHOWN
  rts

end_section:
  lda FAILS+2
  jsr prhex
  lda FAILS+1
  jsr prhex
  lda FAILS
  jsr prhex
  jsr crlf
  jmp clear_fails

crlf:
  lda #13
  jsr SerialChrout
  lda #10
  jmp SerialChrout

prhex:
  pha
  lsr
  lsr
  lsr
  lsr
  jsr @nib
  pla
@nib:
  and #$0F
  ora #'0'
  cmp #'9'+1
  bcc :+
  adc #6
:
  jmp SerialChrout

say_inline:
  pla
  sta SPTR
  pla
  sta SPTR+1
@loop:
  inc SPTR
  bne :+
  inc SPTR+1
:
  lda (SPTR)
  beq @end
  jsr SerialChrout
  bra @loop
@end:
  lda SPTR+1
  pha
  lda SPTR
  pha
  rts
