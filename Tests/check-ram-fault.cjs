// check-ram-fault: show that check-ram can fail, by running it on an emulated machine with a
// known fault in its banked RAM. This changes the 6502-EMULATOR checkout's compiled RAMBank in
// memory only, as Node loads it, and leaves the files alone. The faults:
//
//   FAULT=oldbug  the decode the first RAM Patch had: the latch also loads on $x3xx and $xxFF
//   FAULT=bit7    bit 7 of the latch is stuck low, so the upper 128 banks alias the lower
//   FAULT=stuck   the latch never loads
//
// From a built 6502-EMULATOR checkout, with check-ram.prg built by hand from check-ram.asm:
//
//   printf 'RUN\r' | FAULT=oldbug node -r /path/to/check-ram-fault.cjs bin/6502 run --headless \
//     --vdp picovdp --empty video,storage --input-after OK --exit-on DONE check-ram.prg
//
// Every fault has to make the report's TOTAL non-zero.

const Module = require('node:module')

const compile = Module.prototype._compile
Module.prototype._compile = function (source, file) {
  if (!file.endsWith('out/core/IO/RAMBank.js')) return compile.call(this, source, file)
  const load = /if \(address === RAMBank\.BANK_CONTROL_REGISTER\) \{\s*this\.currentBank = data & (0xFF|255);/
  if (!load.test(source)) throw new Error('check-ram-fault: the emulator\'s RAMBank has changed')
  const faults = {
    oldbug: 'if ((address & 0x300) === 0x300 || (address & 0xFF) === 0xFF) { this.currentBank = data & 255;',
    bit7: 'if (address === RAMBank.BANK_CONTROL_REGISTER) { this.currentBank = data & 127;',
    stuck: 'if (false) { this.currentBank = data & 255;',
  }
  const fault = faults[process.env.FAULT]
  if (!fault) throw new Error(`check-ram-fault: FAULT must be one of ${Object.keys(faults).join(', ')}`)
  return compile.call(this, source.replace(load, fault), file)
}
