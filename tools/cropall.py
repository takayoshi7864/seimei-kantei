import sys,json
sys.path.insert(0,'tools')
from crop import crops
meta={}
for pn in range(17,319):
    try:
        m=crops(pn,'cr')
    except Exception as e:
        m=None
    if m: meta[pn]=m
json.dump(meta,open('meta.json','w'))
print(len(meta),'pages with grid')
