# Writes notes.html: the ACE Board Rev 1.0 build notes. make.sh prints it to the repo's PDF.
import os,sys
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from figs import *
CSS='''
@page{size:Letter;margin:0}
*{box-sizing:border-box}
html,body{margin:0;padding:0;font-family:-apple-system,"Helvetica Neue",Helvetica,Arial,sans-serif;color:#000;font-size:10.2pt;line-height:1.3;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:8.5in;height:11in;padding:.45in .5in .55in;position:relative;page-break-after:always;overflow:hidden}
.page:last-child{page-break-after:auto}
h1{font-size:19pt;margin:0 0 3pt;line-height:1.15}
.sub{font-size:10pt;color:#222;margin:0 0 7pt}
h2{font-size:12.5pt;margin:10pt 0 4pt;border-bottom:1.4pt solid #000;padding-bottom:1.5pt;display:flex;align-items:center;gap:6pt}
h2:first-child{margin-top:0}
h2 .n{display:inline-flex;width:17pt;height:17pt;border-radius:50%;background:#c8102e;color:#fff;font-size:10pt;align-items:center;justify-content:center;flex:none}
h3{font-size:10.6pt;margin:7pt 0 2pt}
p{margin:0 0 4pt}
ul{margin:0 0 4pt;padding-left:0;list-style:none}
ul li{padding-left:16pt;text-indent:-16pt;margin-bottom:2pt}
.step{display:grid;grid-template-columns:27pt 1fr;column-gap:5pt;margin:7pt 0 0}
.step>div{min-width:0}
.num{width:23pt;height:23pt;border:1.4pt solid #000;border-radius:3pt;font-size:12pt;font-weight:700;display:flex;align-items:center;justify-content:center}
.step h3{margin:0 0 2pt;font-size:10.8pt}
.fig{margin:4pt 0 2pt}
.cap{font-size:8.7pt;color:#222;margin:1pt 0 4pt}
.cap b{color:#000}
.warn{border:1.4pt solid #c8102e;border-radius:3pt;padding:3.5pt 7pt;margin:4pt 0}
.warn b:first-child{color:#c8102e}
.info{border:1pt solid #444;border-radius:3pt;padding:3.5pt 7pt;margin:4pt 0;background:#f3f3f3}
.foot{position:absolute;left:.5in;right:.5in;bottom:.28in;font-size:8pt;color:#333;display:flex;justify-content:space-between;border-top:.5pt solid #666;padding-top:2pt}
.box{display:inline-block;width:10pt;height:10pt;border:1.1pt solid #000;margin-right:6pt;vertical-align:-1.2pt;text-indent:0}
table{border-collapse:collapse;width:100%}
td,th{border:.7pt solid #000;padding:2.4pt 4.5pt;font-size:9.1pt;text-align:left;vertical-align:top;line-height:1.22}
th{background:#e8e8e8}
.c{text-align:center;font-weight:700;color:#c8102e}
.w{width:40pt}
.two{display:grid;grid-template-columns:1fr 1fr;column-gap:.2in}
.side{display:grid;column-gap:.2in;align-items:start}
code,pre{font-family:Menlo,Consolas,monospace;font-size:8.8pt}
pre{margin:3pt 0;padding:4pt 7pt;border:.7pt solid #666;border-radius:3pt;line-height:1.28;background:#fafafa}
'''
def box(t): return f'<li><span class="box"></span>{t}</li>'
def boxes(*a): return "<ul>"+"".join(box(x) for x in a)+"</ul>"
def step(n,title,body): return f'<div class="step"><div class="num">{n}</div><div><h3>{title}</h3>{body}</div></div>'
def fig(s,cap,style=""): return f'<div class="fig" style="{style}">{s}<div class="cap">{cap}</div></div>'
def h2(n,t): return f'<h2><span class="n">{n}</span>{t}</h2>'
CENTER="width:4.8in;margin-left:auto;margin-right:auto"
pages=[]

pages.append(f'''
<h1>ACE Board Rev 1.0: Build Notes</h1>
<p class="sub">The work an ACE Board Rev 1.0 needs beyond its bill of materials, for a new build or for upgrading a built board. Rev 1.1 makes these fixes on the PCB. On Rev 1.0 you make them by hand. Changes 1–8 are done and tested on the owner's Rev 1.0. Changes 9 and 10 are optional and haven't been done on a board yet; change 10's circuit is tested.</p>
<div class="side" style="grid-template-columns:1fr 2.55in">
<div>
<table>
<tr><th style="width:17pt"></th><th>Change</th><th>Who needs it</th></tr>
<tr><td class="c">1</td><td>Fit 10 kΩ at R1–R5 and R27, not 1 kΩ</td><td>Every board</td></tr>
<tr><td class="c">2</td><td>Fit an R6551AP at U4</td><td>Every board</td></tr>
<tr><td class="c">3</td><td>Keep J1 on its 1 MHz pins</td><td>Every board</td></tr>
<tr><td class="c">4</td><td>Add a 10 µF supply capacitor on the underside</td><td>Every board</td></tr>
<tr><td class="c">5</td><td>Program the AB Controller firmware, and add a 10 kΩ pull-up on RESB</td><td>Firmware: every board. Pull-up: recommended</td></tr>
<tr><td class="c">6</td><td>Stack a socket on U3 and fit a diode for /INT</td><td>Any pico9918 video card</td></tr>
<tr><td class="c">7</td><td>Fit the ACE RAM Patch Rev 1.1 in place of U12 and U13</td><td>Any board with the banked RAM (U15, U21, U22)</td></tr>
<tr><td class="c">8</td><td>Optional: put the SID on J1's clock, with one cut and one wire</td><td>Only a board run at 2 MHz, at the builder's risk</td></tr>
<tr><td class="c">9</td><td>Optional: turn the RCA jacks' wiring the right way round</td><td>A board whose J11 and J14 feed an amplifier</td></tr>
<tr><td class="c">10</td><td>Optional: U7's output enable from the inverted RWB</td><td>A board under a heavy load, or above 5.0 V</td></tr>
</table>
</div>
<div>{fig(fig_map(),"<b>Figure 1. Top of the ACE.</b> Where each change is. Change 5 is in two places: the ATmega, U6, and its pull-up under U4.")}</div>
</div>
<div class="warn"><b>Audio:</b> J11 and J14, the RCA jacks, are wired the wrong way round on Rev 1.0: the signal is on the sleeve and ground on the tip. Sound plays, but if the amplifier shares a ground with the ACE through another lead, expect hum. Change 9 rewires them, or use J15, the AUDIO header, which is wired right, with a jack on the case. Rev 1.1 fixes the jacks.</div>
<div class="warn"><b>Power:</b> use a center-positive 5 V supply only. Neither revision has protection against a reversed one.</div>
<h3>These notes use Rev 1.0's part numbers</h3>
<p>Rev 1.0's designators are the ones printed on your board. Build from the ACE Board Rev 1.0 table in <code>BOM.md</code>, or from <code>Production/ACE Board/Rev 1.0/bom.csv</code>, which both use these numbers. Rev 1.1 keeps them, except that its U13 is a 74HC02, not a 74HC00; its new parts take numbers Rev 1.0 never used.</p>
<h3>Changes to the parts you buy</h3>
<table>
<tr><th>Part</th><th style="width:44pt">Qty</th><th>For</th></tr>
<tr><td>10 kΩ resistor, 1/8 W</td><td>7</td><td>Change 1 (R1–R5, R27) and change 5 (RESB). Rev 1.0's BOM lists 34 × 1 kΩ: buy 28 instead</td></tr>
<tr><td>R6551AP</td><td>1</td><td>Change 2. Already at U4 in the BOM, where the value reads 65C51</td></tr>
<tr><td>10 µF electrolytic, 16 V</td><td>1</td><td>Change 4</td></tr>
<tr><td>Machined-pin DIP-40 socket, BAT85 diode</td><td>1 each</td><td>Change 6</td></tr>
<tr><td>ACE RAM Patch Rev 1.1 board, 74HC02</td><td>1 each</td><td>Change 7</td></tr>
<tr><td>74HC00</td><td>4, not 5</td><td>Change 7 uses one on the patch, in place of U12 and U13 on the ACE</td></tr>
<tr><td>DIP-14 sockets</td><td>2 fewer</td><td>Change 7 leaves U12 and U13 without sockets</td></tr>
<tr><td>Pin header, 2.54 mm, 4 strips of 7</td><td>1 set</td><td>Change 7</td></tr>
</table>
<p style="margin-top:6pt"><b>Building a new board?</b> Fit the patch and the underside parts before the keyswitches, sockets and tall parts, while the board still lies flat on its face.</p>
''')

pages.append(f'''
{h2(1,"Pull-ups: R1–R5 and R27 are 10 kΩ")}
<p>Rev 1.0's BOM lists 1 kΩ at these six places. Rev 1.1 makes five of them 10 kΩ and removes R1. R2, R5, R3 and R4 pull up shared lines: BE, RDY, NMIB and IRQB. A 1 kΩ pull-up draws 5 mA, more than the 3.2 mA the 65C22's IRQ output is rated to sink. R27 pulls up the banked RAM's chip enable (U15 pin 22). R1, beside U1's top left corner, holds SOB (U1 pin 38) high. Nothing else holds that pin, so don't leave R1 out. Every other 1 kΩ on the board stays 1 kΩ, including R6, which is the ATmega's reset pull-up.</p>
<div class="two">{fig(fig_pull(),"<b>Figure 2.</b> R2–R5, beside the CART connector. Note the order: R2, R5, R3, R4.")}{fig(fig_r25(),"<b>Figure 3.</b> R27, between U17 and U21.")}</div>
{boxes("R1, R2, R3, R4, R5: 10 kΩ.","R27: 10 kΩ.")}
{h2(2,"U4: fit an R6551AP")}
<p>The silkscreen and Rev 1.0's BOM say 65C51. The R6551AP is the part the AC6502 machines are tested with. Don't substitute a W65C51N: its transmit-empty status bit does not work.</p>
{boxes("U4 is an R6551AP.")}
<div class="side" style="grid-template-columns:1fr 2.4in">
<div>
{h2(3,"J1: keep the shunt on pins 1 and 2")}
<p>J1, PHI2 SELECT, offers 1 MHz or 2 MHz. Use 1 MHz, the AC6502's standard clock. On Rev 1.0 the SID's clock is always U5's 1 MHz output, whatever J1 says, so at 2 MHz the SID answers only every other CPU cycle. Rev 1.1 keeps J1 and puts the SID on J1's clock, so 2 MHz is an option there, at the builder's risk. Change 8 makes a Rev 1.0 the same.</p>
{boxes("Shunt on J1 pins 1 and 2.")}
</div>
<div style="padding-top:10pt">{fig(fig_j1(),"<b>Figure 4.</b> J1: the shunt covers the highlighted pair.")}</div>
</div>
''')
pages.append(f'''
{h2(4,"Add the 10 µF supply capacitor")}
<p>Rev 1.1 adds a 10 µF electrolytic across VCC and GND beside the power input, as bulk capacitance for the whole board. Rev 1.0 has no holes for it, so it goes on the underside, across the pads of J19, the VCC header. J19's pads are close to the power switch and 2.54 mm apart, and J19 can still be fitted. Rev 1.0's own C20 is a 100 nF capacitor elsewhere on the board: leave it alone.</p>
{fig(fig_cap(),"<b>Figure 5.</b> The capacitor across J19's pads, lying flat. Underside of the ACE, keyboard edge toward you.","width:5.2in;margin-left:auto;margin-right:auto")}
{boxes("Bend the legs to 2.54 mm. Positive leg to J19 pin 1 (VCC), striped leg to J19 pin 2 (GND).","Lay the body flat on the board, so it stays clear of the plate. Its insulated sleeve can rest on C12's joints. Solder the legs to the pads, or to J19's tails if J19 is fitted, and clip them.")}
''')

pages[-1]+=(f'''
{h2(5,"Reset: the AB Controller firmware and the RESB pull-up")}
<p>Rev 1.0 has no pull-up on RESB, and older AB Controller firmware drives the line high as well as low, so nothing else can reset the machine. The firmware in the 6502-ACE repository only ever pulls RESB low. That lets the DS1511Y and any card on CART or BUS reset the machine too.</p>
<div class="side" style="grid-template-columns:1fr 2.5in">
<div>
<h3>Program the ATmega</h3>
<p>Program U6 out of its socket in a TL866-class programmer, using <code>minipro</code> and PlatformIO. In <code>Firmware/AB Controller/</code>, for an ATmega1284:</p>
<pre>pio run -e atmega1284 -t upload</pre>
<p>Use <code>-e atmega1284p</code> for a 1284P. The command also writes the fuses. The firmware's README has the details.</p>
{boxes("U6 programmed, and back in its socket.")}
<h3>Fit the pull-up</h3>
<p>The ATmega's internal pull-up raises RESB on its own, but a 10 kΩ is stiffer on a line that runs out to CART and BUS. Rev 1.1 has one. On Rev 1.0, U4's pins 2 and 4 are VCC and RESB, 5.08 mm apart, the same pitch as a resistor footprint.</p>
{boxes("10 kΩ across U4 pin 2 and U4 pin 4, on the underside. Pin 3 is between them: keep the legs off its joint.")}
</div>
<div style="padding-top:6pt">{fig(fig_resb(),"<b>Figure 6.</b> The RESB pull-up on the underside, keyboard edge toward you. U4's pin 1 is nearest the connectors.")}</div>
</div>
''')
pages.append(f'''
{h2(6,"The /INT diode, on a socket stack at U3")}
<p>U3 pin 16 is the video chip's /INT, and Rev 1.0 wires it straight to IRQB. A TMS9918A's /INT is open-drain, but every pico9918 drives it high as well as low, and holds IRQB at about 3.8 V while the VIA tries to pull it low. Keyboard and serial input are then dead. This affects the PRO and the v1.3 alike: a v1.3 can appear to work, but only by luck. Rev 1.1 has a diode on the PCB. Rev 1.0's PCB has no place for one, so it goes in a socket stack: a second socket between U3's socket and the card, with pin 16 routed through the diode.</p>
<div class="side" style="grid-template-columns:2.2in 1fr">
<div>{fig(fig_u3(),"<b>Figure 7.</b> Find pin 16: the fifth pin up from the keyboard end of U3's left row.")}</div>
<div>{fig(fig_stack(),"<b>Figure 8. The stack, seen from inside the left row.</b> Not to scale. The riser's pin 16 stops short of the socket below, so the only path from the card's pin 16 to IRQB is through the diode.")}</div>
</div>
{boxes("Take a machined-pin DIP-40 socket: this is the riser. The pico9918's pins are solid and can't be bent or cut, so the change is made here.",
"Count to pin 16 on the riser, with its notch the same way as U3's. Cut off pin 16's tail below the plastic, so it can't reach U3's socket.",
"Solder the BAT85's band end (cathode) to what is left of the riser's pin 16.",
"Put the other leg (anode) into U3's socket at pin 16, and press the riser into U3's socket. Keep the diode under the card or on the board beside U3's left row, with its legs clear of the other pins.",
"Check with the meter's diode test, with the card out: red on IRQB (R4's left leg, Figure 2), black in the riser's pin 16. About 0.3 V this way, and open the other way.",
"Fit the card into the riser, with its pin 1 at the connector end. It now sits one socket higher: check that it clears any top panel.")}
''')

pages.append(f'''
{h2(7,"The ACE RAM Patch Rev 1.1")}
<p>Rev 1.0's latches for the banked RAM load at the wrong times, so the RAM doesn't hold a bank. The patch is a small board that replaces U12 and U13. It mounts under the ACE on pin headers, with the same logic as Rev 1.1.</p>
<div class="info"><b>Status:</b> the patch's logic passes <code>Tests/check-schematics.mjs</code> in every bus state. Its fit and these steps come from the PCB files, and have not yet been confirmed on a real board. The 6502-ACE README's "ACE RAM Patch" section has the current status.</div>
<h3>Before you start</h3>
{boxes("U12 and U13 are empty: no chips and no sockets. On a built board, take them off. Take off an older Rev 1.0 patch or any other rework on this part of the logic.","All 28 holes of U12 and U13 are open and clear of solder.")}
{fig(fig_top(),"<b>Figure 9. Top of the ACE, keyboard toward you.</b> The patch's four parts run in one row: U1, J1, J2, U2. J1 goes in U12's holes and J2 goes in U13's. Pin numbers are marked on both sockets.")}
{fig(fig_under(),"<b>Figure 10. Underside of the ACE, keyboard toward you.</b> Left and right swap, so U13 is left of U12. Red dots are the legs of C26 and C27. Numbered white circles show where the patch's U1 and U2 pins land, 2.54 mm below the ACE.")}
<div class="warn"><b>Watch C27:</b> its GND leg sits 0.38 mm off the center of U2 pin 8, with only the 2.54 mm header gap between them. U2 pin 8 carries the signal from U1 pin 8. If the leg touches the joint, that signal is shorted to ground. Step 2 deals with this.</div>
{step(1,"Try the header pins in the holes",
"<p>Do this before soldering anything. Both boards have 0.8 mm holes at these pins. A standard 0.64 mm square pin measures about 0.9 mm across its corners, so it may be tight. Push one strip through J1's row on the patch and through U12's row on the ACE, by hand, then take it out.</p>"
+boxes("The pins go in with finger pressure: use the strips.","They need force: stop, and use round machined-pin header instead. Forcing a pin can damage the plated hole. Check that the chips still clear the plate (Figure 13)."))}
''')
pages.append(f'''
{step(2,"Clear the underside of the ACE",
boxes("<b>C27 and C26:</b> clip all four legs to no more than 1 mm below the ACE. C27's GND leg matters most.",
"The whole strip inside the dashed outline in Figure 10 is free of wires and parts.",
"<b>J22:</b> its tails stand just past the patch's long edge, about 0.3 mm clear. Keep them straight."))}
''')

pages[-1]+=(f'''
{step(3,"Solder U1 and U2 to the patch",
"<p>Hold the patch with its text side toward you and the text upright. This is the back. The chips go on this side.</p>"
+fig(fig_patch_back(),"<b>Figure 11a. The patch's back: text upright.</b> U2 (74HC02) is on the left and U1 (74HC00) on the right. Both have pin 1 at lower left, so both notches point left.")
+boxes("U2, the <b>74HC02</b>, on the left. U1, the <b>74HC00</b>, on the right. Check the markings: the two chips look alike.",
"Notches to the left. Chips seated flat on the board. <b>No sockets:</b> a socket adds about 3 mm and the chip would hit the plate.",
"Solder all 28 legs on the front. Clip them flush now: this side faces the ACE and you can't reach it later.")
+fig(fig_patch_front(),"<b>Figure 11b. The patch's front.</b> The silkscreen on J1 and J2 looks like two chip outlines. Those are headers. No chip goes on this side."))}
{step(4,"Stand the header strips in the ACE",
boxes("Turn the ACE face down, keyboard edge toward you. Hold it up on blocks at the board's edges, so nothing rests on any keycaps or chips and the pins have room below.",
"Push four 7-pin strips into U12's and U13's holes from the underside: <b>long ends down, through the ACE.</b> The plastic sits flat on the ACE, with the short tails pointing up at you."))}
''')
pages.append(f'''
{step(5,"Lower the patch onto the strips, and check which way round it is",
boxes("Patch with chips up, so the front faces the ACE. The short tails come up through J1 and J2. The patch rests on the plastic.")
+'<div class="warn"><b>The patch also fits turned 180°, and that is wrong.</b> Every pin finds a hole, but VCC lands on GND (J1 pin 14 goes in U13 pin 7). Check all of these before any solder:</div>'
+boxes("Keyboard edge toward you, and the text on the patch reads <b>upright</b>.",
"U2 (74HC02) on your left and U1 (74HC00) on your right.",
"The patch's square J1 and J2 pads are on the keyboard side, under the ACE's square U12 and U13 pads.",
"C27's and C26's legs don't touch the patch. Look through the gap with a light."))}
{fig(fig_flip(),"<b>Figure 12. Steps 4 to 6: the ACE face down, seen from the keyboard edge</b> (one row of pins, to scale). U2 is on the left in this view.",CENTER)}
''')

meter=[("J19 pin 1","J19 pin 2","VCC and GND not shorted","<b>No steady beep.</b> A short chirp is fine"),
("U1 pin 14","C26 VCC leg","Patch has power; not turned 180°","Beep"),
("U1 pin 7","C26 GND leg","U1 has ground","Beep"),
("U2 pin 14","C27 VCC leg","U2 has power","Beep"),
("U2 pin 7","C27 GND leg","U2 has ground","Beep"),
("U2 pin 8","C27 GND leg","C27's leg not touching U2 pin 8","<b>No beep</b>"),
("U2 pin 10","U13 pin 8, ACE top","LOADL reaches the ACE","Beep"),
("U2 pin 13","U13 pin 11, ACE top","LOADH reaches the ACE","Beep"),
("U12 pin 1, ACE top","U12 pin 2, ACE top","A9 and A8 not bridged","<b>No beep</b>")]
mt="".join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a,b,c,d in meter)
pages[-1]+=(f'''
{step(6,"Solder the short tails on the patch's back",
boxes("On each of the four strips, tack the two end pins only.",
"Check that the patch lies flat on all the plastic, and the plastic flat on the ACE. Reheat a tack to correct it.",
"Solder the rest: 28 joints in all, including the pins that show no track. They hold the patch on."))}
{step(7,"Solder the long pins on top of the ACE",
boxes("Turn the ACE face up. Hold it on blocks or its standoffs, so the patch hangs free. It hangs about 8.5 mm.",
"Push the patch up, so the plastic is against the ACE's underside. Tack the end pins of each strip and check again.",
"Solder the rest: 28 joints in U12's and U13's pads. Clip the pins to about 1 mm above the joint."))}
{fig(fig_final(),"<b>Figure 13. The finished stack, ACE on top, seen from the keyboard edge</b> (one row of pins, to scale).",CENTER)}
''')
pages.append(f'''
<h2>Check the board with the meter, with no power on</h2>
<p>Use the continuity beep. Figure 10 numbers the U1 and U2 pins, and Figure 9 numbers the U12 and U13 holes. Touch U1 and U2 at the chips' legs, from under the ACE. Inspect every joint first: 28 on the patch's back, 28 on top of the ACE, and U1's and U2's on the patch's front, seen through the gap with a light.</p>
<table><tr><th>From</th><th>To</th><th>What this checks</th><th>Expect</th></tr>{mt}</table>
<div class="warn" style="margin-top:6pt"><b>Any row wrong:</b> do not power the ACE. A beep from U1 pin 14 to C26's GND leg means the patch is turned 180°.</div>
''')

pages[-1]+=(f'''
<h2>First power-on</h2>
{boxes("SW69, IO ENABLE: all eight switches on. Each switch is one I/O window, IO1 to IO8, and the first two are the banked RAM.",
"A center-positive 5 V supply. Switch on.")}
<p>With a pico9918 running 6502-PICOVDP and BIOS 2.x, the screen shows the AC6502 logo, then <code>AC6502 BIOS v2.1</code>, <code>BASIC v2.0 30718 BYTES FREE</code> and the cards the BIOS found: <code>RAM RTC CF SER VIA SID VDP</code>. The 6502-ACE README's "Video card" section covers setting up the card and the ROM.</p>
<h3>Which cards did the BIOS find?</h3>
<p>Type this at BASIC:</p>
<pre>PRINT PEEK(781)</pre>
<p>With everything fitted it prints <b>255</b>. Each card the BIOS doesn't find takes its own value off that total:</p>
<table style="width:auto"><tr><th>RAM, $8000</th><th>RAM, $8400</th><th>RTC</th><th>CF</th><th>Serial</th><th>VIA</th><th>SID</th><th>Video</th></tr>
<tr><td>1</td><td>2</td><td>4</td><td>8</td><td>16</td><td>32</td><td>64</td><td>128</td></tr></table>
<p style="margin-top:5pt">Without the patch, the BIOS doesn't find the $8400 window, so a full Rev 1.0 prints 253. BIOS 2.0.x could miss an ARMSID on about one boot in a dozen; BIOS 2.1.0 finds it every time, so use 2.1.0 or later.</p>
''')
pages.append(f'''
<h3 style="margin-top:0">Does the banked RAM work?</h3>
<p>Type this short program. It writes each bank of both windows and reads it back. Then it writes to the addresses that wrongly loaded the bank register on an unpatched board, and checks that the bank didn't move. It takes about a minute at most.</p>
<pre>NEW
10 E=0
20 FOR W=0 TO 1
30 D=32768+1024*W:R=D+1023
40 FOR B=0 TO 255:POKE R,B:POKE D,B:NEXT
50 FOR B=0 TO 255:POKE R,B:IF PEEK(D)&lt;&gt;B THEN E=E+1
60 NEXT
70 POKE R,7:POKE D,165:POKE R,8:POKE D,90:POKE R,7
80 FOR A=255 TO 767 STEP 256:POKE D+A,0:NEXT
90 POKE D+768,0:POKE D+1022,0
100 IF PEEK(D)&lt;&gt;165 THEN E=E+1000
110 NEXT W
120 IF PEEK(32768)&lt;&gt;165 THEN E=E+1000
130 PRINT "ERRORS:";E
RUN</pre>
<p>It should print <b>ERRORS: 0</b>. A count under 1000 means banks that don't hold their data. A count of 1000 or more means a write moved the bank: look again at the patch's joints and at the meter table.</p>
<h3>Keyboard, serial and reset</h3>
{boxes("The keyboard types at BASIC. A dead keyboard with a pico9918 fitted points to change 6, the /INT diode.",
"The reset button, SW70, restarts the machine to the same boot screen.",
"Serial works at 19200 baud over a null-modem DB-9 cable. The ACE's port is wired as DTE. J2 (CTS EN) and J4 (DCD EN) both stay on ground unless you need the handshake.")}
''')
pages.append(f'''
{h2(8,"Optional: the SID on J1's clock, for 2 MHz")}
<p>Only for a board you mean to run at 2 MHz, which is at the builder's risk on any ACE. On Rev 1.0 the SID, U9, takes its clock from U5's 1 MHz output, whatever J1 says, so at 2 MHz it answers only every other CPU cycle. Rev 1.1 clocks the SID from J1's middle pin, PHI2, the clock the CPU runs on. One cut and one wire do the same on a Rev 1.0. After them the SID follows J1 at either setting, so the change does no harm at 1 MHz. Tested on the owner's Rev 1.0 at 2 MHz (2026-11-21): the BIOS finds the SID, an ARMSID, and it plays. Its notes sound an octave higher than at 1 MHz, since a SID's pitch follows its clock and BASIC's <code>SOUND</code> values assume 1 MHz.</p>
<div class="info"><b>2 MHz needs more than this.</b> The 2 MHz tests of 2026-11-11 ran a Rev 1.0 with a 74HCT00 at U14, which fits its socket. See the 6502-ACE README's notes on 2 MHz.</div>
<div class="side" style="grid-template-columns:2.7in 1fr">
<div>{fig(fig_sid_cut(),"<b>Figure 14. Top of the ACE, beside U9.</b> The SID's clock runs on the top side, 2.4 mm left of U9's pins, between two vias. It is drawn in blue: the track itself is under the solder mask. Cut it level with pin 5, below C7.")}</div>
<div>
{step(1,"Cut the track",boxes("Find the track on the top side, running straight up and down 2.4 mm left of U9's pins 1–6, past C4 and C7.","Cut it level with U9 pin 5, below C7, where no other track runs within 4 mm: two cuts about 1 mm apart, with a sharp blade, and lift the copper between them."))}
{step(2,"Fit the wire",boxes("On the underside, solder an insulated wire from J1 pin 2, the middle pin, to U9 pin 6 (Figure 15). Solder to the joints, and keep the wire flat against the board.","For 2 MHz, move J1's shunt to pins 2 and 3. For 1 MHz, leave it on pins 1 and 2."))}
{step(3,"Check with the meter, power off",boxes("U9 pin 6 to J1 pin 1: no beep. The cut is through.","U9 pin 6 to J1 pin 2: beep. The wire is on.","U9 pin 6 to its neighbours, pins 5 and 7: no beep."))}
</div>
</div>
{fig(fig_sid_wire(),"<b>Figure 15. Underside of the ACE.</b> The wire from J1's middle pin to U9 pin 6. Seen from below the board is mirrored, so J1 is on the right.")}
''')
pages.append(f'''
{h2(9,"Optional: the RCA jacks the right way round")}
<p>J11 (AUDIO L) and J14 (AUDIO R) are wired the wrong way round on Rev 1.0. Each jack's sleeve, its ground, is the centred slot nearest the board edge, and its tip, the signal, is one of the two holes behind it; the other is the tip's shunt, which touches the tip whenever no plug is in. Rev 1.0 puts the SID's signal on the sleeves and ground on the tip and shunt. Sound still plays, since audio has no polarity, but the signal rides on the cable's shield, so an amplifier that shares a ground with the ACE through another lead can hum. This change swaps them, as Rev 1.1 is drawn: the sleeves go to ground, and the tip and shunt holes to the signal. It hasn't been tried on a board yet.</p>
<div class="info"><b>Do it before fitting J11 and J14.</b> Four of the cuts are on the top side, under the jacks. On a built board, take the jacks off first. <b>The simpler way round:</b> leave J11 and J14 as they are, and wire a jack on the case to J15, the AUDIO header, which is wired right: pin 1 the signal, pin 2 ground.</div>
<div class="two">{fig(fig_audio_top(),"<b>Figure 16. Top copper around J14 and J11.</b> Cut the track from J15 to J14's sleeve, and the eight spokes circled, two at the ends of each tip and shunt hole.")}{fig(fig_audio_bot(),"<b>Figure 17. Underside copper, mirrored.</b> Cut the eight spokes circled. Red: the signal wire, from J15 pin 1 (square pad) to all four tip and shunt holes. Blue: J14's sleeve to J15 pin 2, ground.")}</div>
{step(1,"Cut the signal track to the sleeves",boxes("On the top side, the track runs up from J15 pin 1 into J14's sleeve slot. Cut it just below the jack's outline, where it runs straight (Figure 16), with two cuts about 1 mm apart, and lift the copper between them.","Leave the underside track that joins the two sleeves: both go to ground together."))}
{step(2,"Free the tip and shunt holes from the ground pour",boxes("Each of the four holes behind the sleeves is held in the ground pour by two thin spokes, one at each end, on each side of the board: sixteen in all, circled in Figures 16 and 17.","Cut each spoke across its gap with a sharp blade, so no copper joins the hole's ring to the pour."))}
{step(3,"Fit the jacks, then the two wires underneath",boxes("Fit J11 and J14 as usual.","Signal: solder an insulated wire from J15 pin 1 to the tip and shunt holes' joints, all four in a chain (red).","Ground: solder an insulated wire from J14's sleeve joint to J15 pin 2 (blue)."))}
{step(4,"Check with the meter, power off",boxes("Each sleeve joint to J15 pin 2: beep. Each tip and shunt joint to J15 pin 2: no beep.","Each tip and shunt joint to J15 pin 1: beep. Each sleeve joint to J15 pin 1: no beep.","J15 pin 1 to C8's lead nearest J15: beep. The signal still reaches J15."))}
''')

pages.append(f'''
{h2(10,"Optional: the RAM's output enable, for a heavy load")}
<p>U7, the main RAM, is an Alliance AS6C62256. On Rev 1.0 its output enable, pin 22, is RB, which rises as PHI2 falls, so the RAM lets go of the data bus before the CPU has finished reading it. Under a heavy load, such as the 1 MB Flash Cart, or at 2 MHz, the CPU can then read a 0 bit as 1, and programs crash or misbehave. The supply voltage decides how often: in tests, 5.0 V at the board read clean and 5.1 V or more failed. Rev 1.1 takes U7's output enable from the inverted RWB, which U14 already makes, so the RAM holds the byte until the address changes. Two cuts and two wires do the same on a Rev 1.0, and do no harm on a board that doesn't need them.</p>
<div class="info"><b>Status:</b> the circuit is tested on the owner's Rev 1.0 (2026-11-21 to 2026-11-23), with U7's pin 22 bent out of its socket and wired to U14 pin 6: the reads that failed thousands of times a run read 0, from 4.5 V to 5.24 V, at 1 MHz and 2 MHz, and none of 20 million writes to the cart, the CF card, the video chip and the bank latches was lost. These cuts and wires make that circuit permanent; they haven't been done on a board yet. A Hitachi HM62256LP-70 at U7, no longer made, doesn't need the change.</div>
{fig(fig_ram_cuts(),"<b>Figure 18. Underside copper around U7, mirrored.</b> RB in blue: from U18 pin 22 into U7 pin 22, and on toward U8. The two cuts in red.")}
{step(1,"Cut the track on both sides of U7 pin 22",boxes("On the underside, find U7 pin 22. RB comes into it from U18 and leaves toward U8, the ROM (Figure 18).","<b>Cut 1:</b> on the straight run between U7's two rows of pins, about 11 mm from pin 22.","<b>Cut 2:</b> on the straight run out of pin 22 the other way, about 7 mm from the pin, before the track bends.","At each, make two cuts about 1 mm apart with a sharp blade, and lift the copper between them. No other track runs within 1.2 mm of either cut."))}
''')
pages.append(f'''
{fig(fig_ram_wires(),"<b>Figure 19. Underside of the ACE, mirrored.</b> Blue: the bridge, from U18 pin 22 to U8 pin 22. Red: the signal wire, from U7 pin 22 to U14 pin 6. The red bars are the two cuts. The lines show which joints to join, not the path: route each wire flat along the board.")}
{step(2,"Fit the two wires",boxes("<b>Bridge:</b> an insulated wire from U18 pin 22 to U8 pin 22, about 11 cm. The cuts leave the ROM, the banked RAM and the CF card off RB; this joins them back to it, with the RTC.","<b>Signal:</b> an insulated wire from U7 pin 22 to U14 pin 6, the inverted RWB, about 9 cm.","Solder to the joints on the underside, keep both wires flat against the board, and keep them clear of the standoffs."))}
{step(3,"Check with the meter, power off",boxes("U7 pin 22 to U14 pin 6: beep. The signal wire is on.","U7 pin 22 to U14 pin 8: <b>no beep</b>. Both cuts are through: a beep means one isn't.","U14 pin 8 to U8 pin 22, and to U15 pin 24: beep. The bridge is on.","U7 pin 22 to its neighbours, pins 21 and 23: <b>no beep</b>."))}
''')

N=len(pages)
FT="ACE Board Rev 1.0 build notes · github.com/acwright/6502-ACE"
html="".join(f'<div class="page">{p}<div class="foot"><span>{FT}</span><span>© 2026 A.C. Wright Design</span><span>Page {i+1} of {N}</span></div></div>' for i,p in enumerate(pages))
open(f"{HERE}/notes.html","w",encoding="utf8").write(f'<!DOCTYPE html><html><head><meta charset="utf-8"><title>ACE Board Rev 1.0: Build Notes</title><style>{CSS}</style></head><body>{html}</body></html>')
print("pages",N)
