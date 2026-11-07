# Copy a .kicad_pcb without its 3D model references, so a plot shows only the bare board.
import sys
src,dst=sys.argv[1],sys.argv[2]
t=open(src,encoding='utf8').read()
out=[];i=0
while True:
    j=t.find('(model ',i)
    if j<0: out.append(t[i:]);break
    out.append(t[i:j]); d=0;k=j;s=False
    while True:
        c=t[k]
        if c=='"' and t[k-1]!='\\': s=not s
        elif not s:
            if c=='(':d+=1
            elif c==')':
                d-=1
                if d==0:break
        k+=1
    i=k+1
open(dst,'w',encoding='utf8').write(''.join(out))
