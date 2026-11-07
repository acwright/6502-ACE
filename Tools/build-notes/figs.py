# The figures for the ACE Board Rev 1.0 build notes. Coordinates are read from the KiCad files.
import re,os
HERE=os.path.dirname(os.path.abspath(__file__))
def vb(f):
    t=open(f"{HERE}/svg/{f}.svg").read(); m=re.search(r'viewBox="([\d. ]+)"',t); return list(map(float,m.group(1).split()))[2:]
# The patch's holes land on the ACE's at this offset between the two PCB files.
DX,DY=212.43,117.30
J1=[(106.57+DX+2.54*i,94.82+DY) for i in range(7)]+[(121.81+DX-2.54*i,87.2+DY) for i in range(7)]
J2=[(x+23,y) for x,y in J1]
U1=[(98.81+DX-2.54*i,94.82+DY) for i in range(7)]+[(83.57+DX+2.54*i,87.2+DY) for i in range(7)]
U2=[(167.81+DX-2.54*i,94.82+DY) for i in range(7)]+[(152.57+DX+2.54*i,87.2+DY) for i in range(7)]
PATCH=(291.88,201.75,384.48,214.85)
C26=[(314.23,204.6),(314.23,207.1)]; C27=[(362.12,204.55),(364.62,204.55)]
RED="#c8102e"
def lab(x,y,t,a="middle",s=1.7,w=700,c="#000"):
    return f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{a}" font-size="{s}" font-weight="{w}" fill="{c}" stroke="#fff" stroke-width="{s*.28:.2f}" paint-order="stroke" stroke-linejoin="round">{t}</text>'
def wlab(x,y,t,s=1.05):
    return f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="middle" font-size="{s}" font-weight="700" fill="#fff" stroke="#222" stroke-width="{s*.3:.2f}" paint-order="stroke" stroke-linejoin="round">{t}</text>'
def line(x1,y1,x2,y2,c="#000",w=.22,arrow=False):
    a=' marker-end="url(#arr)"' if arrow else ''
    return f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{c}" stroke-width="{w}"{a}/>'
DEFS='<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker></defs>'
def rect(x1,y1,x2,y2,fill="none",stroke="#000",w=.3,dash=None,op=1):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{min(x1,x2):.2f}" y="{min(y1,y2):.2f}" width="{abs(x2-x1):.2f}" height="{abs(y2-y1):.2f}" fill="{fill}" fill-opacity="{op}" stroke="{stroke}" stroke-width="{w}"{d}/>'
def circ(x,y,r,fill="none",stroke=RED,w=.3): return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>'
def board(name,cx,cy):
    w,h=vb(name)
    return f'<image href="svg/{name}.svg" x="{cx-w/2:.3f}" y="{cy-h/2:.3f}" width="{w}" height="{h}" preserveAspectRatio="none"/>'
def svg(x,y,w,h,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x} {y} {w} {h}" style="width:100%;display:block">{DEFS}{body}</svg>'
def mask(x,w,y1,y2): return f'<rect x="{x}" y="{y1}" width="{w}" height="{y2-y1}" fill="#fff"/>'
CX,CY=267.5,200
def mx(x): return 2*CX-x
TOP=lambda:board("ace-F",CX,CY)
BOT=lambda:board("ace-B",CX,CY)

def badge(x,y,n,r=6.2):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{RED}"/><text x="{x}" y="{y+r*.46:.2f}" text-anchor="middle" font-size="{r*1.32:.2f}" font-weight="700" fill="#fff">{n}</text>'
def fig_map():
    b=TOP()
    b+=rect(*PATCH,fill="#ffd400",stroke=RED,w=.9,op=.55)
    for x1,y1,x2,y2 in ((189.5,112.5,196.5,122),(139,162,151,175),(380,178,392,190),(160,120,183,160),(215,118,222,129),(137,102,146,110),(228,113,250,167),(345,113,366,167),(160.5,125,167,133)):
        b+=rect(x1,y1,x2,y2,fill="#ffd400",stroke=RED,w=.9,op=.45)
    b+=badge(145,183,1)+badge(392,170,1)+badge(193,104,1)
    b+=badge(171,140,'2')+badge(219,110,3)+badge(153,101,4)
    b+=badge(355.5,140,5)+badge(152,129,5)+badge(239,140,6)+badge(338,193,7)
    b+=lab(CX,337.5,"Keyboard edge: toward you",s=7.5,w=600)
    return svg(95,70,345,272,b)
def fig_pull():
    b=TOP()
    for y,t in ((164.59,"R2"),(167.13,"R5"),(169.67,"R3"),(172.21,"R4")):
        b+=rect(140.8,y-1,148.8,y+1,fill="#ffd400",stroke=RED,w=.22,op=.4)
        b+=lab(137.8,y+.5,t,s=1.5,c=RED,a="end")
    return svg(127,161,28,14.5,mask(127,28,161,163)+b)
def fig_r25():
    b=TOP()
    b+=rect(382.4,179.5,385.2,187.4,fill="#ffd400",stroke=RED,w=.22,op=.4)
    b+=mask(371,28,172,177.3)
    b+=lab(383.79,176.6,"R27",s=1.7,c=RED)
    return svg(371,174.8,28,15,b)
def fig_j1():
    b=TOP()
    b+=rect(216.8,119.6,220.2,125,fill="#ffd400",stroke=RED,w=.25,op=.5)
    b+=lab(222,121.5,"pin 1",s=1.4,a="start")+lab(222,124.1,"pin 2",s=1.4,a="start")+lab(222,126.7,"pin 3",s=1.4,a="start",w=500)
    return svg(206,116.5,28,14.5,b)
def fig_cap():
    b=BOT()
    L=mx(160)
    b+=mask(L,60,90,99.5)+mask(L,60,110.2,120)
    px=mx(141.5)
    b+=rect(px-8.3,104.2,px-1.3,108.3,fill="#e9c46a",stroke="#000",w=.2)
    b+=rect(px-8.3,106.9,px-1.3,108.3,fill="#555",stroke="#000",w=.15)
    b+=line(px-1.3,105.0,px,105.0,w=.45)+line(px-1.3,107.54,px,107.54,w=.45)
    b+=lab(px-4.8,106.1,"10 µF",s=1.2)
    b+=lab(px+.1,97.6,"J19 pin 1 (square pad): VCC. Capacitor's + leg",s=1.35,c=RED)
    b+=line(px,98.2,px,103.9,c=RED,w=.2,arrow=True)
    b+=lab(px+.1,112.9,"J19 pin 2: GND. Capacitor's striped leg",s=1.35,c=RED)
    b+=line(px,111.9,px,108.9,c=RED,w=.2,arrow=True)
    b+=lab(mx(149.79)-1.1,106.8,"C12",s=1.3,w=500,a="end")
    b+=lab(mx(134),110,"J20",s=1.3,w=500)
    b+=lab(422.6,108.3,"Power switch",s=1.3,w=500,a="end")
    return svg(L+1,96,47,18,b)
def fig_resb():
    b=BOT()
    x=mx(163.75)
    b+=mask(x+1.5,20,118,140)
    b+=rect(x-1.05,127.2,x+1.05,131,fill="#e9c46a",stroke="#000",w=.18)
    b+=line(x,126.54,x,127.2,w=.42)+line(x,131,x,131.62,w=.42)
    b+=lab(x,129.5,"10k",s=.95)
    b+=lab(x+2.6,127,"pin 2: VCC",s=1.3,a="start",c=RED)
    b+=lab(x+2.6,132.1,"pin 4: RESB",s=1.3,a="start",c=RED)
    b+=lab(x+2.6,124.4,"U4 pin 1",s=1.2,a="start",w=500)
    return svg(x-4,121.5,17,14,b)
def fig_u3():
    b=TOP()
    for n,y in (("20",164.26),("19",161.72),("18",159.18),("17",156.64),("16",154.1)):
        b+=lab(229.2,y+.45,n,s=1.3,a="end",c=RED if n=="16" else "#000",w=700)
    b+=circ(231.15,154.1,1.75,w=.32)
    b+=lab(239,152,"U3",s=2)
    b+=lab(239,155.5,"pin 16 is IRQB",s=1.35,c=RED)
    b+=mask(222.5,28,168,175)
    b+=lab(239,171.3,"Keyboard edge",s=1.3,w=500)
    return svg(222.5,146,28,27,b)
def fig_stack():
    # Side view of three pins in U3's left row: not to scale, to show the signal path.
    o=''
    o+=rect(4,42,96,46,fill="#cfd8c8",stroke="#000",w=.3)+lab(93,45,"ACE",s=2.2,a="end")
    o+=rect(10,31.5,90,42,fill="#444",stroke="#000",w=.2)
    o+=rect(10,20,90,28.5,fill="#6b6b6b",stroke="#000",w=.2)
    o+=rect(4,4,96,8,fill="#cfd8c8",stroke="#000",w=.3)+lab(93,7,"pico9918",s=2.2,a="end")
    for x,n in ((25,"15"),(50,"16"),(75,"17")):
        # card pin
        o+=rect(x-.8,8,x+.8,24,fill="#c9a227",stroke="#000",w=.12)
        # riser cup
        o+=rect(x-1.9,20,x+1.9,28.5,fill="#c9a227",stroke="#000",w=.12)
        # lower socket contact
        o+=rect(x-1.9,31.5,x+1.9,42,fill="#c9a227",stroke="#000",w=.12)
        o+=rect(x-.9,31.5,x+.9,36.5,fill="#222",stroke="#000",w=.05)
        if n!="16":
            o+=rect(x-.8,28.5,x+.8,36,fill="#c9a227",stroke="#000",w=.12)
        else:
            o+=rect(x-.8,28.5,x+.8,29.8,fill="#c9a227",stroke="#000",w=.12)
        o+=lab(x,2.6,f"pin {n}",s=2,w=600)
    # snipped gap and diode
    o+=f'<path d="M50.8 29.2 C57 29.2 59 30 59 31" fill="none" stroke="{RED}" stroke-width=".55"/>'
    o+=rect(57.2,31,60.8,36.8,fill="#e9c46a",stroke="#000",w=.2)+rect(57.2,31,60.8,32.2,fill="#111",stroke="#000",w=.1)
    o+=f'<path d="M59 36.8 C59 38.6 54 38.6 50.4 36.2" fill="none" stroke="{RED}" stroke-width=".55"/>'
    o+=lab(4,16,"Riser",s=2.1,a="start",w=600)+line(10,17,15,21,w=.25,arrow=True)
    o+=lab(1.5,30.3,"U3's socket",s=2.1,a="start",w=600)+line(9,31,14,33.5,w=.25,arrow=True)
    o+=lab(62,27,"",s=0)
    o+=lab(50,50,"Band (cathode) to the riser's pin 16. Other leg (anode) into U3's socket at pin 16, which is IRQB.",s=2,c=RED)
    return svg(0,0,100,52,o)
def fig_top():
    XA,XB,YA,YB=287,390,194.2,221.4
    b=TOP()
    b+=mask(XA,XB-XA,YA,200.7)+mask(XA,XB-XA,216.7,YB)
    b+=rect(*PATCH,stroke="#000",w=.35,dash="1.4 .9")
    for ps in (J1,J2):
        xs=[p[0] for p in ps]; ys=[p[1] for p in ps]
        b+=rect(min(xs)-1.5,min(ys)-1.8,max(xs)+1.5,max(ys)+1.8,fill="#ffd400",stroke=RED,w=.45,op=.4)
    for ps in (J1,J2):
        for i,(x,y) in enumerate(ps):
            b+=lab(x,(y-1.75) if y>208 else (y+2.6),str(i+1),s=1.25,w=600)
    for x,t,sub in ((326.62,"U12's 14 holes","J1 goes in here"),(349.62,"U13's 14 holes","J2 goes in here")):
        b+=lab(x,196.2,t,s=2,c=RED); b+=lab(x,198.6,sub,s=1.65,w=500)
        b+=line(x,199.2,x,202.5,c=RED,w=.3,arrow=True)
    for x,t in ((303,"U1 is below here"),(372.62,"U2 is below here")):
        b+=lab(x,208.8,t,s=1.6,w=500)
    b+=lab(291,198.6,"Dashed: the patch's outline",s=1.6,w=500,a="start")
    b+=line(300,199.2,300,201.5,w=.22,arrow=True)
    b+=circ(314.23,205.85,2.9,w=.32)+lab(314.23,198.6,"C26",s=1.9,c=RED)+line(314.23,199.2,314.23,202.8,c=RED,w=.25,arrow=True)
    b+=circ(363.37,204.55,3,w=.32)+lab(363.37,198.6,"C27",s=1.9,c=RED)+line(363.37,199.2,363.37,201.4,c=RED,w=.25,arrow=True)
    b+=lab(293,219.3,"J22, the keyboard header. Its row runs just past the patch's edge.",s=1.6,w=500,a="start")
    return svg(XA,YA,XB-XA,YB-YA,b)
def fig_under():
    XA,XB,YA,YB=287,390,194.2,221.4
    b=BOT()
    b+=mask(mx(XB),XB-XA,YA,200.7)+mask(mx(XB),XB-XA,216.7,YB)
    b+=rect(mx(PATCH[2]),PATCH[1],mx(PATCH[0]),PATCH[3],stroke="#000",w=.35,dash="1.4 .9")
    for ps,n in ((J1,"U12"),(J2,"U13")):
        xs=[mx(p[0]) for p in ps]; ys=[p[1] for p in ps]
        b+=rect(min(xs)-1.5,min(ys)-1.8,max(xs)+1.5,max(ys)+1.8,fill="#ffd400",stroke=RED,w=.45,op=.4)
        b+=lab(sum(xs)/14,209,n+" holes",s=2,c=RED)
    for ps,n,t in ((U1,"U1","74HC00"),(U2,"U2","74HC02")):
        xs=[mx(p[0]) for p in ps]
        for (x,y) in ps:
            b+=circ(mx(x),y,.8,fill="#fff",stroke="#444",w=.22)
        for i,(x,y) in enumerate(ps):
            hot=(n=="U2" and i==7)
            b+=lab(mx(x)-(1.05 if hot else 0),(y+2.25) if y>208 else (y-1.2),str(i+1),s=1.3 if hot else 1.15,w=700 if hot else 600,c=RED if hot else "#000")
        b+=lab(sum(xs)/14,208.9,f"{n} ({t}) pins below",s=1.45,w=600,c="#222")
    for (x,y) in C26+C27:
        b+=circ(mx(x),y,.85,fill=RED,w=0)
    X=mx(C26[0][0]); b+=lab(X-1,197.9,"C26 VCC leg",s=1.6,c=RED); b+=line(X-1,198.4,X,203.6,c=RED,w=.22,arrow=True)
    X=mx(C26[1][0]); b+=lab(X+.8,219,"C26 GND leg",s=1.6,c=RED,a="end"); b+=line(X,217.6,X,208.1,c=RED,w=.22,arrow=True)
    X=mx(C27[0][0]); b+=lab(X+2,197.9,"C27 VCC leg",s=1.6,c=RED,a="start"); b+=line(X+3,198.4,X+.2,203.5,c=RED,w=.22,arrow=True)
    X=mx(C27[1][0]); b+=lab(170.2,197.9,"C27 GND leg, over U2 pin 8",s=1.75,c=RED,a="end"); b+=line(X-.5,198.4,X,203.5,c=RED,w=.3,arrow=True)
    b+=lab(223.5,219,"J22 runs just past the patch's edge",s=1.3,w=500,a="start")
    return svg(mx(XB),YA,XB-XA,YB-YA,b)
PCX,PCY=125.75,91.0
def fig_patch_back():
    def m(x): return 2*PCX-x
    b=board("patch-B",PCX,PCY)
    for ps,n,v in (((83.57,98.81),"U1","74HC00"),((152.57,167.81),"U2","74HC02")):
        a,c=m(ps[1]),m(ps[0])
        b+=rect(a-1.2,88.4,c+1.2,93.6,fill="#ffd400",stroke=RED,w=.35,op=.35)
        b+=lab((a+c)/2,90.5,f"{n}: {v}",s=1.8,c=RED); b+=lab((a+c)/2,92.6,"chip goes here",s=1.25,w=500)
        b+=lab(a-.4,99.7,"pin 1",s=1.4,c=RED); b+=line(a-.2,98.5,a,96.3,c=RED,w=.25,arrow=True)
    b+=lab(PCX,99.7,"Square pads: pin 1 of J2 and J1, on the keyboard side",s=1.3,w=500)
    b+=lab(m(137.19),83.2,"J2: solder the short tails here",s=1.3,w=500)
    b+=lab(m(114.19),83.2,"J1: solder the short tails here",s=1.3,w=500)
    return svg(78,81.4,95.5,19.2,b)
def fig_patch_front():
    b=board("patch-F",PCX,PCY)
    for a,c,n,sub in ((106.57,121.81,"J1","into U12"),(129.57,144.81,"J2","into U13")):
        b+=rect(a-1.2,85.7,c+1.2,96.3,fill="#9ad0ff",stroke="#0a5aa0",w=.3,op=.25)
        b+=lab((a+c)/2,83.2,f"{n} {sub}: header strips, no chip",s=1.3,c="#0a5aa0")
    b+=lab(91.19,91.4,"U1's legs: clip flush",s=1.3,w=500)
    b+=lab(160.19,91.4,"U2's legs: clip flush",s=1.3,w=500)
    b+=lab(106.57,99.7,"J1 pin 1",s=1.3,w=500); b+=lab(129.57,99.7,"J2 pin 1",s=1.3,w=500)
    return svg(78,81.4,95.5,19.2,b)
def section(flip=False,trim=True,plate=True):
    XL,XR=338,384
    def X(x): return (XL+XR-x) if flip else x
    def Z(z): return z if flip else -z
    def R(x1,z1,x2,z2,**k): return rect(X(x1),Z(z1),X(x2),Z(z2),**k)
    def L(x1,z1,x2,z2,**k): return line(X(x1),Z(z1),X(x2),Z(z2),**k)
    b=""
    pt,pb=-2.54,-4.14
    b+=R(XL,0,XR,1.6,fill="#cfd8c8",stroke="#000",w=.12)
    b+=R(XL+1.7,pt,XR,pb,fill="#cfd8c8",stroke="#000",w=.12)
    J=[342+2.54*i for i in range(7)]; U=[365+2.54*i for i in range(7)]
    b+=R(J[0]-1.27,0,J[-1]+1.27,pt,fill="#333",stroke="#000",w=.08)
    def blob(x,z,ry=.42): return f'<ellipse cx="{X(x):.2f}" cy="{Z(z):.2f}" rx=".85" ry="{ry}" fill="#999" stroke="#000" stroke-width=".06"/>'
    for x in J:
        b+=R(x-.32,2.6 if trim else 6.0,x+.32,-5.54,fill="#c9a227",stroke="#000",w=.06)
        b+=blob(x,pb)
        if trim: b+=blob(x,1.6)
    b+=R(U[0]-1.2,pb-.5,U[-1]+1.2,-8.5,fill="#555",stroke="#000",w=.1)
    for x in U:
        b+=R(x-.2,pt+.02,x+.2,pb-.6,fill="#c9a227",stroke="#000",w=.05)
        b+=blob(x,pt,.32)
    for x in (362.12,364.62):
        b+=L(x,3.2,x,-.9,c="#000",w=.32)
        b+=blob(x,.05,.36)
    b+=R(360.9,3,365.85,7.6,fill="#e9c46a",stroke="#000",w=.1)
    if plate: b+=R(XL,-10,XR,-12.5,fill="#e8eef5",stroke="#000",w=.1)
    return b,X
def fig_flip():
    b,X=section(flip=True,trim=False,plate=False)
    Jc=X(349.6); Uc=X(372.6)
    b+=lab(Jc,-8.6,"Solder the 28 short tails first",s=1.2,c=RED); b+=line(Jc,-8,Jc,-5.9,c=RED,w=.16,arrow=True)
    b+=wlab(Uc,-5.9,"U2: already soldered",s=1.1)
    b+=lab(339,1.2,"ACE, face down",s=1.05,a="start")
    b+=lab(360.5,-2.95,"Patch",s=1.05)
    b+=lab(384.6,8.6,"Long pins stand out below the ACE: keep them off the bench",s=1.1,w=500,a="end")
    b+=lab(X(363.38),5.7,"C27",s=1.15)
    return svg(337,-10.2,48,20,b)
def fig_final():
    b,X=section()
    b+=lab(383.6,-.42,"ACE, top side up",s=1.1,a="end")
    b+=lab(360.5,3.75,"Patch",s=1.05)
    b+=lab(363.38,-5,"C27",s=1.15)
    b+=lab(349.6,-8.8,"Long pins clipped to about 1 mm",s=1.15,w=500); b+=line(349.6,-8.2,349.6,-3,w=.13,arrow=True)
    b+=wlab(349.6,1.65,"Plastic: 2.54 mm gap")
    b+=lab(349.6,7.6,"Short tails soldered on the patch's back",s=1.15,w=500); b+=line(349.6,6.8,349.6,5.8,w=.13,arrow=True)
    b+=wlab(372.6,6.9,"U2: 74HC02, no socket",s=1.15)
    b+=lab(373.5,1.35,"U2's legs clipped flush",s=1.05,w=500)
    b+=lab(372.6,9.7,"Chips clear the plate by about 1.5 mm",s=1.05,w=600)
    b+=lab(345,11.7,"Base plate",s=1.1,w=500)
    b+=lab(383.6,11.7,"10 mm below the ACE",s=1.1,w=500,a="end")
    b+=line(383,0,383,10,w=.12,arrow=True)+line(383,10,383,0,w=.12,arrow=True)
    b+=circ(364.62,1,1.15,w=.18)
    b+=lab(383.8,-9.9,"C27's GND leg: under 1 mm below the ACE",s=1.15,c=RED,a="end")
    b+=lab(383.8,-8.4,"U2 pin 8 is right under it",s=1.15,c=RED,a="end",w=500)
    b+=line(369.5,-7.9,365.3,.1,c=RED,w=.16,arrow=True)
    return svg(337,-11.2,48,24,b)
