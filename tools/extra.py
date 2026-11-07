import sys,os,json,re,collections,bisect,subprocess
sys.path.insert(0,'tools')
import crop,cells2,grid
from PIL import Image
EXTRA=[25,29,106,113,120,169,199,221,249,251]
for d in ('xcr','xca','xcb','xcs','xkb'): os.makedirs(d,exist_ok=True)
meta={}
for pn in EXTRA:
    m=crop.crops(pn,'xcr'); meta[pn]=m
json.dump(meta,open('meta_x.json','w'))
os.environ['COLS']='oya,gyo'
for pn in EXTRA:
    cells2.make(pn,'xca',3,70); cells2.make(pn,'xcb',5,60)
os.environ['COLS']='suu'
for pn in EXTRA: cells2.make(pn,'xcs',3,70)
os.environ['COLS']='kan'
for pn in EXTRA: cells2.make(pn,'xkb',1,110)
print({k:len(v['rows'])-1 for k,v in meta.items()})
