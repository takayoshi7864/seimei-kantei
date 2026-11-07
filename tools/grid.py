from PIL import Image
import numpy as np
TPL=[173,250,365,437,555,628,708,785,1075,1510]
def groups(a):
    if len(a)==0: return []
    g=[];s=a[0];p=a[0]
    for x in a[1:]:
        if x>p+4: g.append((s+p)//2);s=x
        p=x
    g.append((s+p)//2);return g
def grid(path,rowthr=0.5):
    im=np.array(Image.open(path).convert('L'))<130
    h,w=im.shape
    cs=im.sum(axis=0); rs=im.sum(axis=1)
    cols=groups(np.where(cs>cs.max()*0.5)[0]); rows=groups(np.where(rs>rs.max()*rowthr)[0])
    # choose shift dx so template lines coincide with detected lines
    best=(-1,0)
    for dx in range(-60,81):
        sc=sum(1 for t in TPL if any(abs(c-(t+dx))<=5 for c in cols))
        if sc>best[0]: best=(sc,dx)
    dx=best[1]
    snapped=[]
    for t in TPL:
        cand=[c for c in cols if abs(c-(t+dx))<=6]
        snapped.append(min(cand,key=lambda c:abs(c-(t+dx))) if cand else t+dx)
    x0,x1=snapped[0]+8,snapped[-1]-8
    rs2=im[:,x0:x1].sum(axis=1)
    rows=groups(np.where(rs2>(x1-x0)*0.55)[0])
    return im,snapped,rows
if __name__=='__main__':
    import sys
    im,c,r=grid(sys.argv[1]); print([int(x) for x in c]);print([int(x) for x in r])
