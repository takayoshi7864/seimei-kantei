import sys,os,json
sys.path.insert(0,'tools')
from grid import grid
from PIL import Image
def cells(pn,outdir,cols=('oya','kan','gyo')):
    im,c,r=grid(f'pages/p{pn}.png')
    if len(c)!=10: return None
    img=Image.open(f'pages/p{pn}.png').convert('L')
    idx={'oya':1,'kan':3,'gyo':6,'suu':5}
    n=0
    for i in range(len(r)-1):
        for col in cols:
            x0,x1=c[idx[col]]+6,c[idx[col]+1]-5
            y0,y1=r[i]+6,r[i+1]-5
            cr=img.crop((x0,y0,x1,y1))
            # fit into 160x160 white canvas keeping aspect
            s=min(130/cr.width,130/cr.height)
            cr=cr.resize((max(1,int(cr.width*s)),max(1,int(cr.height*s))),Image.LANCZOS)
            cv=Image.new('L',(200,200),255); cv.paste(cr,((200-cr.width)//2,(200-cr.height)//2))
            cv.save(f'{outdir}/p{pn}_r{i}_{col}.png'); n+=1
    return n
if __name__=='__main__':
    os.makedirs(sys.argv[2],exist_ok=True); print(cells(int(sys.argv[1]),sys.argv[2]))
