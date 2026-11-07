import sys,os,json
sys.path.insert(0,'tools')
import cells2
meta=json.load(open('meta.json'))
reps,size,outdir=int(sys.argv[1]),int(sys.argv[2]),sys.argv[3]
os.makedirs(outdir,exist_ok=True)
for pn in sorted(map(int,meta)):
    cells2.make(pn,outdir,reps,size)
