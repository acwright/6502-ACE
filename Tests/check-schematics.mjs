#!/usr/bin/env node
// check-schematics — evaluate the ACE's address decoding from the schematics themselves.
//
// The RAM bank latches have been wrong twice, and both times the logic looked right on
// paper. So this does not trust anyone's reading of the gates. It asks KiCad for each
// board's netlist, builds the glue logic from the parts it finds there, and then drives
// every address, as a read and as a write, with PHI2 high and low and with a cartridge in
// and out — 524,288 bus states — and compares every select, strobe and latch enable with
// the memory map below. Nets nobody drives come out as unknown, so a missing wire fails
// too.
//
// A patch board is fitted the way it is on the bench: each of its DIP-14 headers names the
// socket it plugs into in its value, "74HC00 (U13)", the chip in that socket comes out,
// and the header's pins join the socket's nets.
//
// Usage:  node Tests/check-schematics.mjs
// Needs kicad-cli: on the PATH, at the macOS default, or named by KICAD_CLI.

import { execFileSync } from 'node:child_process'
import { existsSync, mkdtempSync, readFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..')
const HW = join(ROOT, 'Hardware')

// ---- The boards, as built -------------------------------------------------------------

const CONFIGS = [
  {
    name: 'ACE Board Rev 1.1',
    board: 'ACE Board/Rev 1.1/ACE Board.kicad_sch',
    rules: ['decode', 'clock', 'shared-lines']
  },
  {
    // Rev 1.0's schematic is the board that was made, so it keeps the PHI2 SELECT jumper
    // and has no /INT diode or RESB pull-up drawn; those are fitted by hand. The jumper is
    // on its 1 MHz pins (1-2), the only setting the ACE supports.
    name: 'ACE Board Rev 1.0 + ACE RAM Patch Rev 1.1',
    board: 'ACE Board/Rev 1.0/ACE Board.kicad_sch',
    patch: 'ACE RAM Patch/Rev 1.1/ACE RAM Patch.kicad_sch',
    jumpers: { J1: [1, 2] },
    rules: ['decode', 'clock']
  }
]

// ---- The memory map -------------------------------------------------------------------
//
// a = address, r = 1 for a read, p = PHI2, h = HRDB (0 while a cartridge claims $C000-$FFFF).
// Each check names a pin on the part that receives the signal, because net names change
// from revision to revision and the pin is what matters.

const io = (a, k) => a >= 0x8000 + k * 0x400 && a < 0x8400 + k * 0x400   // IO slot k+1
const RB = (a, r, p) => r && p ? 0 : 1                                     // read strobe, low
const WB = (a, r, p) => !r && p ? 0 : 1                                    // write strobe, low
const low = (cond) => cond ? 0 : 1

const PINS = [
  // 32 KB RAM, $0000-$7FFF
  ['U7', 20, 'RAM /CE', (a) => low(a < 0x8000)],
  ['U7', 22, 'RAM /OE', RB],
  ['U7', 27, 'RAM /WE', WB],
  // ROM: $A000-$FFFF, or $A000-$BFFF with a cartridge in
  ['U8', 20, 'ROM /CE', (a, r, p, h) => low(a >= 0xA000 && (a < 0xC000 || h))],
  ['U8', 22, 'ROM /OE', RB],
  // Banked RAM through IO 1 ($8000) and IO 2 ($8400); bank latches at $83FF and $87FF
  ['U15', 22, 'banked RAM /CE', (a) => low(io(a, 0) || io(a, 1))],
  ['U15', 24, 'banked RAM /OE', RB],
  ['U15', 29, 'banked RAM /WE', WB],
  ['U15', 1, 'banked RAM A18', (a) => io(a, 1) ? 1 : io(a, 0) ? 0 : '-'],
  ['U21', 1, 'low bank latch /OE', (a) => low(io(a, 0))],
  ['U22', 1, 'high bank latch /OE', (a) => low(io(a, 1))],
  ['U21', 11, 'LOADL (low bank latch LE)', (a, r, p) => a === 0x83FF && !r && p ? 1 : 0],
  ['U22', 11, 'LOADH (high bank latch LE)', (a, r, p) => a === 0x87FF && !r && p ? 1 : 0],
  // IO 3-8
  ['U18', 20, 'RTC /CE', (a) => low(io(a, 2))],
  ['U18', 22, 'RTC /OE', RB],
  ['U18', 27, 'RTC /WE', WB],
  ['J22', 12, 'CF /CS0', (a) => low(io(a, 3))],
  ['J22', 8, 'CF /IORD', RB],
  ['J22', 10, 'CF /IOWR', WB],
  ['U4', 3, 'ACIA CS1B', (a) => low(io(a, 4))],
  ['U4', 2, 'ACIA CS0', () => 1],
  ['U2', 23, 'VIA CS2B', (a) => low(io(a, 5))],
  ['U2', 24, 'VIA CS1', () => 1],
  ['U9', 8, 'SID /CS', (a) => low(io(a, 6))],
  ['U3', 15, 'VDP /CSR', (a, r, p) => low(io(a, 7) && r && p)],
  ['U3', 14, 'VDP /CSW', (a, r, p) => low(io(a, 7) && !r && p)]
]

// What drives the data bus on a read, and what takes it on a write. Exactly one of each,
// except that nothing on the board answers $C000-$FFFF while a cartridge does, and nothing
// answers while PHI2 is low. (A write to $83FF or $87FF also stores the byte in the banked
// RAM; BIOS.inc leaves that byte to the latch.)
const READERS = [
  ['RAM', v => v('U7', 20) === 0 && v('U7', 22) === 0],
  ['ROM', v => v('U8', 20) === 0 && v('U8', 22) === 0],
  ['banked RAM', v => v('U15', 22) === 0 && v('U15', 24) === 0],
  ['RTC', v => v('U18', 20) === 0 && v('U18', 22) === 0],
  ['CF', v => v('J22', 12) === 0 && v('J22', 8) === 0],
  ['ACIA', (v, a, r, p) => v('U4', 3) === 0 && v('U4', 2) === 1 && r && p],
  ['VIA', (v, a, r, p) => v('U2', 23) === 0 && v('U2', 24) === 1 && r && p],
  ['SID', (v, a, r, p) => v('U9', 8) === 0 && r && p],
  ['VDP', v => v('U3', 15) === 0]
]
const WRITERS = [
  ['RAM', v => v('U7', 20) === 0 && v('U7', 27) === 0],
  ['banked RAM', v => v('U15', 22) === 0 && v('U15', 29) === 0],
  ['RTC', v => v('U18', 20) === 0 && v('U18', 27) === 0],
  ['CF', v => v('J22', 12) === 0 && v('J22', 10) === 0],
  ['ACIA', (v, a, r, p) => v('U4', 3) === 0 && v('U4', 2) === 1 && !r && p],
  ['VIA', (v, a, r, p) => v('U2', 23) === 0 && v('U2', 24) === 1 && !r && p],
  ['SID', (v, a, r, p) => v('U9', 8) === 0 && !r && p],
  ['VDP', v => v('U3', 14) === 0]
]
const expectedReaders = (a, r, p, h) => !r || !p ? 0 : a >= 0xC000 && !h ? 0 : 1
const expectedWriters = (a, r, p) => r || !p ? 0 : a < 0xA000 ? 1 : 0

// ---- Netlists -------------------------------------------------------------------------

function kicadCli() {
  const candidates = [process.env.KICAD_CLI, '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli', 'kicad-cli']
  for (const c of candidates.filter(Boolean)) {
    try { execFileSync(c, ['version'], { stdio: 'ignore' }); return c } catch {}
  }
  throw new Error('kicad-cli not found; set KICAD_CLI')
}

function sexpr(text) {
  const stack = [[]]
  const re = /\s*(?:(\()|(\))|"((?:[^"\\]|\\.)*)"|([^\s()"]+))/gy
  let m
  while ((m = re.exec(text)) && m[0].length) {
    if (m[1]) stack.push([])
    else if (m[2]) { const x = stack.pop(); stack[stack.length - 1].push(x) }
    else stack[stack.length - 1].push(m[3] !== undefined ? m[3].replace(/\\(.)/g, '$1') : m[4])
  }
  return stack[0][0]
}
const kids = (node, key) => node.filter(c => Array.isArray(c) && c[0] === key)
const kid = (node, key) => kids(node, key)[0]

function netlist(cli, sch, dir) {
  const out = join(dir, `${Math.random().toString(36).slice(2)}.net`)
  execFileSync(cli, ['sch', 'export', 'netlist', '--format', 'kicadsexpr', '-o', out, join(HW, sch)], { stdio: 'ignore' })
  const root = sexpr(readFileSync(out, 'utf8'))
  const comps = new Map()
  for (const c of kids(kid(root, 'components'), 'comp')) comps.set(kid(c, 'ref')[1], kid(c, 'value')[1])
  const nets = []
  for (const n of kids(kid(root, 'nets'), 'net')) {
    nets.push({ name: kid(n, 'name')[1], nodes: kids(n, 'node').map(x => [kid(x, 'ref')[1], Number(kid(x, 'pin')[1])]) })
  }
  return { comps, nets }
}

// Joins nets: switches closed, jumpers fitted, a patch's headers in their sockets.
class Board {
  constructor() { this.parent = new Map(); this.pinNet = new Map(); this.comps = new Map(); this.names = new Map() }
  find(x) { while (this.parent.get(x) !== x) { const p = this.parent.get(this.parent.get(x)); this.parent.set(x, p); x = p } return x }
  union(a, b) { a = this.find(a); b = this.find(b); if (a !== b) this.parent.set(b, a) }
  add({ comps, nets }, prefix = '', skip = new Set()) {
    for (const [ref, value] of comps) if (!skip.has(ref)) this.comps.set(prefix + ref, value)
    for (const n of nets) {
      const id = prefix + n.name
      this.parent.set(id, id)
      this.names.set(id, n.name)
      for (const [ref, pin] of n.nodes) if (!skip.has(ref)) this.pinNet.set(`${prefix}${ref}.${pin}`, id)
    }
  }
  net(ref, pin) { const n = this.pinNet.get(`${ref}.${pin}`); return n === undefined ? undefined : this.find(n) }
  join(refA, pinA, refB, pinB) {
    const a = this.pinNet.get(`${refA}.${pinA}`), b = this.pinNet.get(`${refB}.${pinB}`)
    if (a === undefined || b === undefined) throw new Error(`cannot join ${refA}.${pinA} and ${refB}.${pinB}`)
    this.union(a, b)
  }
  netNamed(name) { for (const [id, n] of this.names) if (n === name) return this.find(id) }
}

function assemble(cli, cfg, dir) {
  const board = new Board()
  const main = netlist(cli, cfg.board, dir)
  let sockets = new Map()
  let patch
  if (cfg.patch) {
    patch = netlist(cli, cfg.patch, dir)
    for (const [ref, value] of patch.comps) {
      const m = /\((U\d+)\)/.exec(value)
      if (m) sockets.set(ref, m[1])
    }
    if (!sockets.size) throw new Error(`${cfg.patch}: no header names a socket, e.g. "74HC00 (U13)"`)
  }
  // The chip in each socket a patch plugs into comes out; its pins stay as the socket's.
  const pulled = new Set(sockets.values())
  board.add({ comps: new Map([...main.comps].filter(([r]) => !pulled.has(r))), nets: main.nets })
  if (patch) {
    board.add(patch, 'P:')
    for (const [header, socket] of sockets) {
      for (let pin = 1; pin <= 14; pin++) {
        if (board.pinNet.has(`P:${header}.${pin}`) && board.pinNet.has(`${socket}.${pin}`)) board.join(`P:${header}`, pin, socket, pin)
      }
    }
    for (const name of ['VCC', 'GND']) board.union(board.netNamed(name), `P:${name}`)
  }
  // IO ENABLE switches closed: pin k to pin 17-k.
  for (let k = 1; k <= 8; k++) board.join('SW70', k, 'SW70', 17 - k)
  for (const [ref, [a, b]] of Object.entries(cfg.jumpers ?? {})) board.join(ref, a, ref, b)
  return board
}

// ---- The logic ------------------------------------------------------------------------

const X = 'X'
const nand = ins => ins.includes(0) ? 1 : ins.every(v => v === 1) ? 0 : X
const nor = ins => ins.includes(1) ? 0 : ins.every(v => v === 0) ? 1 : X

const GATES = {
  '74HC00': { fn: nand, units: [[[1, 2], 3], [[4, 5], 6], [[9, 10], 8], [[12, 13], 11]] },
  '74HC02': { fn: nor, units: [[[2, 3], 1], [[5, 6], 4], [[8, 9], 10], [[11, 12], 13]] },
  '74HC30': { fn: nand, units: [[[1, 2, 3, 4, 5, 6, 11, 12], 8]] }
}
const Y138 = [15, 14, 13, 12, 11, 10, 9, 7]

function compile(board) {
  const gates = []   // { ins: [net], out: net, fn }
  const netOf = (ref, pin) => board.net(ref, pin)
  const refs = [...board.comps.keys()]
  for (const ref of refs) {
    const value = board.comps.get(ref)
    const g = GATES[value]
    if (g) {
      for (const [ins, out] of g.units) {
        const o = netOf(ref, out)
        if (o === undefined) continue
        gates.push({ ins: ins.map(p => netOf(ref, p)), out: o, fn: g.fn, what: `${ref}.${out}` })
      }
    } else if (value === '74HC138') {
      const [A, B, C, E1, E2, E3] = [1, 2, 3, 4, 5, 6].map(p => netOf(ref, p))
      Y138.forEach((pin, k) => {
        const o = netOf(ref, pin)
        if (o === undefined) return
        gates.push({
          ins: [A, B, C, E1, E2, E3], out: o, what: `${ref}.${pin}`,
          fn: ([a, b, c, e1, e2, e3]) => {
            if (e1 === 1 || e2 === 1 || e3 === 0) return 1
            if ([a, b, c, e1, e2, e3].includes(X) || [a, b, c, e1, e2, e3].includes(undefined)) return X
            return (a | b << 1 | c << 2) === k ? 0 : 1
          }
        })
      })
    }
  }
  // Pull-ups to VCC, and Schottky diodes pulling a pulled-up net low (the wired AND on
  // the banked RAM's /CE).
  const vcc = board.netNamed('VCC'), gnd = board.netNamed('GND')
  const pullups = new Set(), diodes = []
  for (const ref of refs) {
    if (/^(P:)?R\d+$/.test(ref)) {
      const a = netOf(ref, 1), b = netOf(ref, 2)
      if (a === vcc && b !== undefined) pullups.add(b)
      if (b === vcc && a !== undefined) pullups.add(a)
    }
    if (/^(P:)?D\d+$/.test(ref) && /BAT|Schottky|1N/i.test(board.comps.get(ref))) {
      diodes.push({ k: netOf(ref, 1), a: netOf(ref, 2) })
    }
  }
  const driven = new Set(gates.map(g => g.out))
  for (const n of driven) {
    const count = gates.filter(g => g.out === n).length
    if (count > 1) throw new Error(`net ${board.names.get(n)} has ${count} gate outputs driving it`)
  }
  return { gates, pullups, diodes, vcc, gnd, driven }
}

function evaluate(board, logic, inputs) {
  const val = new Map(inputs)
  val.set(logic.vcc, 1); val.set(logic.gnd, 0)
  for (let pass = 0; pass < 32; pass++) {
    let changed = false
    for (const g of logic.gates) {
      const v = g.fn(g.ins.map(n => n === undefined ? X : val.has(n) ? val.get(n) : X))
      if (val.get(g.out) !== v) { val.set(g.out, v); changed = true }
    }
    for (const n of logic.pullups) {
      if (logic.driven.has(n) || inputs.has(n)) continue
      const ks = logic.diodes.filter(d => d.a === n).map(d => val.has(d.k) ? val.get(d.k) : X)
      const v = ks.includes(0) ? 0 : ks.includes(X) ? X : 1
      if (val.get(n) !== v) { val.set(n, v); changed = true }
    }
    if (!changed) return val
  }
  throw new Error('the logic did not settle: is there a loop?')
}

// ---- Rules ----------------------------------------------------------------------------

function checkDecode(board) {
  const logic = compile(board)
  const cpu = pin => board.net('U1', pin)
  const addr = [9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 24, 25].map(cpu)  // A0-A15
  const rwb = cpu(34), phi2 = cpu(37), hrdb = board.net('J18', 4)
  const failures = new Map()
  const fail = (what, a, r, p, h, got, want) => {
    const f = failures.get(what) ?? { count: 0, examples: [] }
    f.count++
    if (f.examples.length < 6) f.examples.push(`$${a.toString(16).toUpperCase().padStart(4, '0')} ${r ? 'read ' : 'write'} PHI2=${p}${h ? '' : ' cart'}: got ${got}, want ${want}`)
    failures.set(what, f)
  }
  const pinNets = PINS.map(([ref, pin, what, want]) => {
    const n = board.net(ref, pin)
    if (n === undefined) throw new Error(`${ref} pin ${pin} (${what}) is not in the netlist`)
    return [n, what, want]
  })
  for (let h = 0; h <= 1; h++) for (let p = 0; p <= 1; p++) for (let r = 0; r <= 1; r++) {
    for (let a = 0; a < 0x10000; a++) {
      const inputs = new Map()
      addr.forEach((n, i) => inputs.set(n, a >> i & 1))
      inputs.set(rwb, r); inputs.set(phi2, p); inputs.set(hrdb, h)
      const val = evaluate(board, logic, inputs)
      const v = (ref, pin) => { const n = board.net(ref, pin); return val.has(n) ? val.get(n) : X }
      for (const [n, what, want] of pinNets) {
        const w = want(a, r, p, h)
        const got = val.has(n) ? val.get(n) : X
        if (w !== '-' && got !== w) fail(what, a, r, p, h, got, w)
      }
      const readers = READERS.filter(([, f]) => f(v, a, r, p)).map(([n]) => n)
      if (readers.length !== expectedReaders(a, r, p, h)) fail('devices driving the data bus', a, r, p, h, readers.join('+') || 'none', expectedReaders(a, r, p, h))
      const writers = WRITERS.filter(([, f]) => f(v, a, r, p)).map(([n]) => n)
      if (writers.length !== expectedWriters(a, r, p)) fail('devices taking a write', a, r, p, h, writers.join('+') || 'none', expectedWriters(a, r, p))
    }
  }
  return [...failures].map(([what, f]) => `${what}: wrong in ${f.count} bus states, e.g.\n        ${f.examples.join('\n        ')}`)
}

// The CPU, VIA, ACIA and SID all run from U5's 1 MHz output. At 2 MHz the SID, whose clock
// was always the 1 MHz tap, answers only every other CPU cycle (TODO.md, "The ACE runs at
// 1 MHz only").
function checkClock(board) {
  const errs = []
  const q3 = board.net('U5', 11)
  for (const [ref, pin, what] of [['U1', 37, 'CPU PHI2'], ['U2', 25, 'VIA PHI2'], ['U4', 27, 'ACIA PHI2'], ['U9', 6, 'SID φ2']]) {
    if (board.net(ref, pin) !== q3) errs.push(`${what} (${ref}.${pin}) is not on U5's 1 MHz output (Q3, pin 11)`)
  }
  return errs
}

// IRQB and RESB are shared, so nothing may drive them high (TODO.md items 1 and 2).
function checkSharedLines(board) {
  const errs = []
  const irqb = board.net('U1', 4), resb = board.net('U1', 40), vcc = board.netNamed('VCC')
  const intb = board.net('U3', 16)
  if (intb === irqb) errs.push('the video card\'s push-pull /INT (U3.16) is wired straight to IRQB')
  else {
    const ok = [...board.comps.keys()].some(ref => /^D\d+$/.test(ref) && board.net(ref, 1) === intb && board.net(ref, 2) === irqb)
    if (!ok) errs.push('U3.16 (/INT) does not reach IRQB through a diode, cathode toward U3')
  }
  const pull = [...board.comps.keys()].some(ref => /^R\d+$/.test(ref) &&
    ((board.net(ref, 1) === resb && board.net(ref, 2) === vcc) || (board.net(ref, 2) === resb && board.net(ref, 1) === vcc)))
  if (!pull) errs.push('RESB has no pull-up resistor to VCC')
  return errs
}

// ---- Main -----------------------------------------------------------------------------

const cli = kicadCli()
const dir = mkdtempSync(join(tmpdir(), 'ace-check-'))
let failed = 0
try {
  for (const cfg of CONFIGS) {
    const board = assemble(cli, cfg, dir)
    const results = []
    if (cfg.rules.includes('decode')) results.push(['address decoding (524,288 bus states)', checkDecode(board)])
    if (cfg.rules.includes('clock')) results.push(['clock', checkClock(board)])
    if (cfg.rules.includes('shared-lines')) results.push(['IRQB and RESB', checkSharedLines(board)])
    console.log(cfg.name)
    for (const [what, errs] of results) {
      console.log(`  ${errs.length ? 'FAIL' : 'ok  '}  ${what}`)
      for (const e of errs) console.log(`      ${e}`)
      failed += errs.length
    }
  }
} finally {
  rmSync(dir, { recursive: true, force: true })
}
process.exit(failed ? 1 : 0)
