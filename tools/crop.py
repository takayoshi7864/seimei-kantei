import sys,os,json
sys.path.insert(0,'tools')
from grid import grid
from PIL import Image
def crops(pn, outdir):
    p=f'pages/p{pn}.png'
    im,c,r=grid(p)
    if len(c)!=10 or len(r)<3: return None
    img=Image.open(p).convert('L')
    top,bot=r[0],r[-1]
    names=['num','oya','m1','kan','m2','suu','gyo','on','nano']
    meta={'rows':[int(x) for x in r],'top':int(top),'bot':int(bot)}
    for i,n in enumerate(names):
        x0,x1=c[i]+4,c[i+1]-3
        cr=img.crop((x0,top-8,x1,bot+8)); 
        W=cr.width; 
        fn=f'{outdir}/p{pn}_{n}.png'
        # white margin so edge rows are not clipped
        cr.save(fn)
    return meta
if __name__=='__main__':
    os.makedirs(sys.argv[2],exist_ok=True)
    print(json.dumps(crops(int(sys.argv[1]),sys.argv[2])))
