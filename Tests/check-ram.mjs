#!/usr/bin/env node
// check-ram: test the ACE's banked RAM on a real machine, over its serial port.
//
// check-schematics.mjs proves the drawn logic. This proves the built board: the chips, the
// joints, and on a Rev 1.0 the ACE RAM Patch. It restarts the machine several times, reading
// HW_PRESENT after each boot, then loads check-ram.asm over XMODEM and runs it. See that file
// for what the program checks.
//
// Usage:  node Tests/check-ram.mjs [--port PATH] [--runs N] [--restarts N] [--expect HEX]
//
//   --port      The serial port. Default: ACE_PORT, or the first /dev/cu.usbserial-*
//   --runs      How many times to run the program. Default: 3, about 65 seconds each
//   --restarts  How many restarts to read HW_PRESENT after. Default: 10
//   --expect    The exact HW_PRESENT to require, such as FF with every card fitted. Without
//               it, only the two RAM bits have to be set
//
// The machine has to be at BASIC's prompt on BIOS 2.x, with the serial port at 19200. This
// erases the BASIC program in memory and everything in the banked RAM. Needs cc65 and stty,
// so it runs on macOS and Linux. Exits non-zero on a failure.

import { execFileSync } from 'node:child_process'
import { constants, mkdtempSync, openSync, readFileSync, readdirSync, rmSync, writeSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { dirname, join } from 'node:path'
import { ReadStream } from 'node:tty'
import { fileURLToPath } from 'node:url'
import { parseArgs } from 'node:util'

const HERE = dirname(fileURLToPath(import.meta.url))

const BAUD = 19200
const IO_MODE = 774 // $0306: set to 1 for a line, so PRINT reaches the serial port with a video card fitted
const HW_PRESENT = 781 // $030D
const RESET_VECTOR = 65532
const CARDS = ['RAM-L', 'RAM-H', 'RTC', 'CF', 'SER', 'VIA', 'SID', 'VDP'] // HW_PRESENT's bit order
const RAM_BITS = 0x03

const TYPE_PACE_MS = 12 // BASIC echoes each typed character to the screen
const BOOT_MS = 4000 // With a video card fitted nothing on the wire says that the boot has finished
const RUN_TIMEOUT_MS = 300000

const SOH = 0x01
const EOT = 0x04
const ACK = 0x06
const NAK = 0x15
const SUB = 0x1a

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms))
const hex = (n) => `$${n.toString(16).toUpperCase().padStart(2, '0')}`
const cardNames = (hw) => CARDS.filter((_, bit) => hw & (1 << bit)).join(' ')

// ---- The serial port -------------------------------------------------------------------

// The port is opened non-blocking, set raw with stty, and read through Node's tty stream.
// The serialport package receives nothing from a USB serial port on current macOS.
class Port {
  constructor(path) {
    this.fd = openSync(path, constants.O_RDWR | constants.O_NOCTTY | constants.O_NONBLOCK)
    const device = process.platform === 'linux' ? '-F' : '-f'
    execFileSync('stty', [device, path, String(BAUD), 'raw', '-echo', '-crtscts', 'clocal', 'cs8', '-cstopb', '-parenb'])
    this.rx = Buffer.alloc(0)
    this.waiters = new Set()
    this.stream = new ReadStream(this.fd)
    this.stream.on('data', (chunk) => {
      this.rx = Buffer.concat([this.rx, chunk])
      for (const wake of this.waiters) wake()
    })
    this.stream.on('error', () => {})
  }

  close() {
    this.stream.destroy()
  }

  drain() {
    this.rx = Buffer.alloc(0)
  }

  text() {
    return this.rx.toString('latin1')
  }

  write(bytes) {
    const data = Buffer.from(bytes)
    for (let at = 0; at < data.length; ) {
      try {
        at += writeSync(this.fd, data, at, data.length - at)
      } catch (error) {
        if (error.code !== 'EAGAIN') throw error
      }
    }
  }

  async type(text) {
    for (const ch of text) {
      this.write(Buffer.from(ch, 'latin1'))
      await sleep(TYPE_PACE_MS)
    }
  }

  // Wait until `test` (a function of the bytes received) returns something other than null or
  // undefined, and return that. Returns null on a timeout.
  waitFor(test, timeoutMs) {
    const found = test(this.rx)
    if (found !== null && found !== undefined) return Promise.resolve(found)
    return new Promise((resolve) => {
      const timer = setTimeout(() => {
        this.waiters.delete(wake)
        resolve(null)
      }, timeoutMs)
      const wake = () => {
        const result = test(this.rx)
        if (result !== null && result !== undefined) {
          clearTimeout(timer)
          this.waiters.delete(wake)
          resolve(result)
        }
      }
      this.waiters.add(wake)
    })
  }
}

// ---- BASIC -----------------------------------------------------------------------------

// One BASIC expression's value. The value goes to the serial port whether or not a video card
// is fitted, and the angle brackets tell it from the echo of the typed line, which has no
// digits straight after the first bracket. A typed character can be lost, so it tries again.
async function value(port, expression) {
  for (let attempt = 0; attempt < 3; attempt++) {
    port.write(Buffer.from('\r', 'latin1'))
    await sleep(200)
    port.drain()
    await port.type(`POKE ${IO_MODE},1:PRINT "<";${expression};">":POKE ${IO_MODE},0\r`)
    const number = await port.waitFor((buf) => {
      const m = /<\s*(\d+)\s*>/.exec(buf.toString('latin1'))
      return m ? Number(m[1]) : null
    }, 3000)
    if (number !== null) return number
  }
  throw new Error(`the machine did not answer ${expression}. Is it at BASIC's prompt? Last heard: ${JSON.stringify(port.text().slice(-80))}`)
}

// BASIC's bare LOAD: the machine sends NAK and takes a checksum XMODEM stream into $0800.
async function load(port, program) {
  for (let attempt = 0; ; attempt++) {
    port.drain()
    await port.type('NEW\r')
    await sleep(400)
    port.drain()
    await port.type('LOAD\r')
    if (await port.waitFor((buf) => (buf.includes(NAK) ? true : null), 15000)) break
    if (attempt === 2) throw new Error('LOAD never asked for the program')
  }
  const blocks = Math.ceil(program.length / 128)
  const reply = () => port.waitFor((buf) => buf.find((b) => b === ACK || b === NAK) ?? null, 5000)
  for (let n = 0; n < blocks; n++) {
    const block = Buffer.alloc(132, SUB)
    block[0] = SOH
    block[1] = (n + 1) & 0xff
    block[2] = 0xff - block[1]
    program.subarray(n * 128, n * 128 + 128).copy(block, 3)
    let sum = 0
    for (let i = 3; i < 131; i++) sum = (sum + block[i]) & 0xff
    block[131] = sum
    for (let attempt = 0; ; attempt++) {
      if (attempt === 10) throw new Error(`XMODEM block ${n + 1} was refused ten times`)
      port.drain()
      port.write(block)
      if ((await reply()) === ACK) break
    }
  }
  for (let attempt = 0; ; attempt++) {
    if (attempt === 10) throw new Error('XMODEM: the machine never acknowledged the end of the transfer')
    port.drain()
    port.write([EOT])
    if ((await reply()) === ACK) break
  }
  await sleep(1500)
  port.drain()
}

// ---- The checks ------------------------------------------------------------------------

function build() {
  const dir = mkdtempSync(join(tmpdir(), 'check-ram-'))
  try {
    const object = join(dir, 'check-ram.o')
    const image = join(dir, 'check-ram.prg')
    execFileSync('ca65', ['-o', object, join(HERE, 'check-ram.asm')], { stdio: 'inherit' })
    execFileSync('ld65', ['-C', join(HERE, 'check-ram.cfg'), '-o', image, object], { stdio: 'inherit' })
    return readFileSync(image)
  } finally {
    rmSync(dir, { recursive: true, force: true })
  }
}

function checkPresent(label, hw, expect) {
  const problems = []
  if ((hw & RAM_BITS) !== RAM_BITS) problems.push('the BIOS did not find both RAM windows')
  if (expect !== undefined && hw !== expect) problems.push(`expected ${hex(expect)}`)
  console.log(`${problems.length ? 'FAIL' : 'ok  '} ${label}: HW_PRESENT ${hex(hw)} (${cardNames(hw)})${problems.length ? `: ${problems.join(', ')}` : ''}`)
  return problems.length === 0
}

async function runProgram(port, program, run) {
  await load(port, program)
  const started = Date.now()
  await port.type('RUN\r')
  let shown = 0
  const show = () => {
    const text = port.text()
    if (text.length > shown) process.stdout.write(text.slice(shown))
    shown = text.length
  }
  const ticker = setInterval(show, 1000)
  const report = await port.waitFor((buf) => {
    const text = buf.toString('latin1')
    return text.includes('DONE\r\n') ? text : null
  }, RUN_TIMEOUT_MS)
  clearInterval(ticker)
  show()
  if (report === null) {
    console.log(`FAIL run ${run}: the program did not finish within ${RUN_TIMEOUT_MS / 1000} seconds`)
    return false
  }
  // Every section has to have reported, with no failures, as well as the total being zero.
  const counts = [...report.matchAll(/FAILS ([0-9A-F]{6})/g)].map((m) => parseInt(m[1], 16))
  const total = /TOTAL ([0-9A-F]{6})/.exec(report)
  const SECTIONS = 12 // SEED, 8 SWEEPs, 3 PASSes
  const ok = counts.length === SECTIONS && counts.every((n) => n === 0) && total !== null && parseInt(total[1], 16) === 0
  console.log(`${ok ? 'ok  ' : 'FAIL'} run ${run}: ${counts.length} of ${SECTIONS} sections reported, ${total ? parseInt(total[1], 16) : '?'} failures, ${((Date.now() - started) / 1000).toFixed(0)} seconds`)
  await sleep(1000)
  return ok
}

const { values: args } = parseArgs({
  options: {
    port: { type: 'string' },
    runs: { type: 'string', default: '3' },
    restarts: { type: 'string', default: '10' },
    expect: { type: 'string' },
  },
})
const expect = args.expect === undefined ? undefined : parseInt(args.expect.replace(/^\$/, ''), 16)
const path = args.port ?? process.env.ACE_PORT ?? readdirSync('/dev').filter((name) => name.startsWith('cu.usbserial')).sort().map((name) => `/dev/${name}`)[0]
if (!path) {
  console.error('check-ram: no serial port found. Name one with --port or ACE_PORT.')
  process.exit(2)
}

const program = build()
const port = new Port(path)
console.log(`check-ram on ${path}`)
let ok = true
try {
  ok = checkPresent('now', await value(port, `PEEK(${HW_PRESENT})`), expect) && ok
  const vector = await value(port, `PEEK(${RESET_VECTOR})+256*PEEK(${RESET_VECTOR + 1})`)
  for (let i = 1; i <= Number(args.restarts); i++) {
    await port.type(`SYS ${vector}\r`)
    await sleep(BOOT_MS)
    ok = checkPresent(`restart ${i}`, await value(port, `PEEK(${HW_PRESENT})`), expect) && ok
  }
  for (let run = 1; run <= Number(args.runs); run++) {
    ok = (await runProgram(port, program, run)) && ok
    ok = checkPresent(`after run ${run}`, await value(port, `PEEK(${HW_PRESENT})`), expect) && ok
  }
} catch (error) {
  console.log(`FAIL ${error.message}`)
  ok = false
}
console.log(ok ? 'check-ram: PASS' : 'check-ram: FAIL')
port.close()
process.exit(ok ? 0 : 1)
