import json,sys,numpy as np
from PIL import Image
sys.path.insert(0,'tools')
from grid import grid
N=40
T=np.load('T.npy'); chars=json.load(open('Tchars.json'))
cidx={c:i for i,c in enumerate(chars)}
def norm_arr(a):
    ys,xs=np.where(a)
    if len(ys)==0: return None
    return ys.min(),ys.max()+1,xs.min(),xs.max()+1
def cellvec(img,box):
    cr=img.crop(box); a=np.array(cr.convert('L'))<140
    H,W=a.shape
    rows=a.sum(axis=1)>0
    # split into vertical segments by blank gaps >=5
    segs=[];s=None;gap=0
    for y in range(H):
        if rows[y]:
            if s is None: s=y
            gap=0; e=y
        else:
            if s is not None:
                gap+=1
                if gap>=5: segs.append((s,e+1)); s=None
    if s is not None: segs.append((s,e+1))
    if not segs: return None
    if len(segs)>1:
        tot=a.sum()
        s0,e0=segs[0]
        sub=a[s0:e0]; xs0=np.where(sub.any(axis=0))[0]
        if (e0-s0)<0.25*H and (xs0.max()-xs0.min())<0.3*W and sub.sum()<0.12*tot:
            a=a[segs[1][0]:]
    ys,xs=np.where(a)
    if len(ys)==0: return None
    c=Image.fromarray(((~a[ys.min():ys.max()+1,xs.min():xs.max()+1])*255).astype(np.uint8)).resize((N,N),Image.LANCZOS)
    v=(255-np.array(c,dtype=np.float32))/255.0; v=v-v.mean(); n=np.linalg.norm(v)
    return (v/n).ravel() if n>0 else None
E=json.load(open('entries_final.json'))
meta={**json.load(open('meta.json')),**json.load(open('meta_x.json'))}
vecs=[];ids=[]
cache={}
for i,e in enumerate(E):
    pn=e['page']
    if pn not in cache:
        _,c,r=grid(f'pages/p{pn}.png'); cache[pn]=(c,Image.open(f'pages/p{pn}.png').convert('L'))
    c,img=cache[pn]; r=meta[str(pn)]['rows']
    row=e['row']
    v=cellvec(img,(c[1]+6,r[row]+6,c[2]-5,r[row+1]-5))
    vecs.append(v); ids.append(i)
res=[]
V=np.array([v if v is not None else np.zeros(N*N,dtype=np.float32) for v in vecs])
S=V@T.T  # (n, pool)
best=S.argmax(axis=1); bs=S.max(axis=1)
for i,e in enumerate(E):
    oi=cidx.get(e['oya']); os_=float(S[i,oi]) if oi is not None else -1
    top=np.argsort(-S[i])[:6]
    res.append(dict(i=i,ocr=e['oya'],ocr_s=round(os_,3),best=chars[best[i]],best_s=round(float(bs[i]),3),top=[(chars[j],round(float(S[i,j]),3)) for j in top]))
json.dump(res,open('match_res.json','w'),ensure_ascii=False)
dis=[r for r in res if r['best']!=r['ocr']]
print('total',len(res),'disagree',len(dis))
import collections
print('ocr score quantiles',np.percentile([r['ocr_s'] for r in res],[1,5,25,50]))
big=[r for r in dis if r['best_s']-r['ocr_s']>0.05]
print('disagree with margin>0.05:',len(big))
for r in big[:40]: print(E[r['i']]['page'],E[r['i']]['row'],r)
