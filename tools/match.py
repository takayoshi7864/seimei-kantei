import json,sys,numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'tools')
from grid import grid
FONT='/System/Library/Fonts/ヒラギノ明朝 ProN.ttc'
f=None
for idx in range(0,8):
    try:
        ft=ImageFont.truetype(FONT,80,index=idx); f=ft; print('font idx',idx,ft.getname()); 
        if 'W6' in ft.getname()[1] or 'Bold' in ft.getname()[1]: break
    except Exception as e: break
font=f
# candidate pool: JIS X 0213 kanji
pool=[]
import codecs
for hi in range(0x21,0x7f):
    for lo in range(0x21,0x7f):
        try:
            ch=bytes([hi|0x80,lo|0x80]).decode('euc_jisx0213')
        except Exception: continue
        if len(ch)==1 and ('一'<=ch<='鿿' or '㐀'<=ch<='䶿' or '豈'<=ch<='﫿'): pool.append(ch)
pool=sorted(set(pool)); print('pool',len(pool))
N=40
def norm(im):
    a=np.array(im.convert('L'))<140
    ys,xs=np.where(a)
    if len(ys)==0: return None
    c=im.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    c=c.resize((N,N),Image.LANCZOS)
    v=(255-np.array(c,dtype=np.float32))/255.0
    v=v-v.mean(); n=np.linalg.norm(v); 
    return (v/n).ravel() if n>0 else None
def render(ch):
    im=Image.new('L',(110,110),255); d=ImageDraw.Draw(im); d.text((10,5),ch,font=font,fill=0)
    return norm(im)
T=[];keep=[]
for ch in pool:
    v=render(ch)
    if v is not None: T.append(v); keep.append(ch)
T=np.array(T); print(T.shape)
np.save('T.npy',T); json.dump(keep,open('Tchars.json','w'),ensure_ascii=False)
