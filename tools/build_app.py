import json,sys,os
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src=open(os.path.join(root,'src','app.src.html'),encoding='utf-8').read()
d=open(os.path.join(root,'data','dict.json'),encoding='utf-8').read()
k=open(os.path.join(root,'data','kakusu.json'),encoding='utf-8').read()
open(os.path.join(root,'index.html'),'w',encoding='utf-8').write(src.replace('__DICT__',d).replace('__KAKU__',k).replace('__GPAIR__',open(os.path.join(root,'data','gogyo_pair.json'),encoding='utf-8').read()))
print('built',os.path.getsize(os.path.join(root,'index.html')),'bytes')
