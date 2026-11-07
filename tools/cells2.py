import sys,os
sys.path.insert(0,'tools')
from grid import grid
from PIL import Image
def glyph(img,box,size):
    cr=img.crop(box)
    # trim to ink bbox
    bb=Image.eval(cr,lambda v:255-v).getbbox()
    if bb: cr=cr.crop(bb)
    s=size/max(cr.width,cr.height)
    return cr.resize((max(1,int(cr.width*s)),max(1,int(cr.height*s))),Image.LANCZOS)
def make(pn,outdir,reps=3,size=70):
    im,c,r=grid(f'pages/p{pn}.png')
    img=Image.open(f'pages/p{pn}.png').convert('L')
    idx={k:v for k,v in {'oya':1,'kan':3,'gyo':6,'suu':5}.items() if k in os.environ.get('COLS','oya,kan,gyo').split(',')}
    for i in range(len(r)-1):
        for col,ci in idx.items():
            box=(c[ci]+6,r[i]+6,c[ci+1]-5,r[i+1]-5)
            g=glyph(img,box,size)
            if Image.eval(img.crop(box),lambda v:255-v).getbbox() is None: continue
            gap=size//2
            W=reps*g.width+(reps+1)*gap
            cv=Image.new('L',(W,size+2*gap),255)
            for k in range(reps): cv.paste(g,(gap+k*(g.width+gap),gap+(size-g.height)//2))
            cv.save(f'{outdir}/p{pn}_r{i}_{col}.png')
if __name__=='__main__':
    os.makedirs(sys.argv[2],exist_ok=True); make(int(sys.argv[1]),sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
