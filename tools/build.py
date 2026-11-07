import json,re,collections,bisect
def cjk1(s): return [c for c in s if '一'<=c<='鿿' or '㐀'<=c<='䶿' or '\U00020000'<=c<='\U0002ffff' or c in '々']
def loadcells(fn):
    d=collections.defaultdict(list)
    for line in open(fn,encoding='utf-8'):
        p=line.rstrip('\n').split('\t')
        if len(p)<3: continue
        m=re.match(r'\w+/p(\d+)_r(\d+)_(\w+)\.png',p[0])
        d[(int(m.group(1)),int(m.group(2)),m.group(3))].append(p[2])
    return d
def mode(xs):
    return collections.Counter(xs).most_common(1)[0][0] if xs else ''
def fixnum(s):
    if len(s)%2==0 and len(s)>=2 and s[:len(s)//2]==s[len(s)//2:]: s=s[:len(s)//2]
    return s
def build(metafn,stripfn,f_og,f_b,f_suu,f_kan):
    meta=json.load(open(metafn))
    obs=collections.defaultdict(list)
    for line in open(stripfn,encoding='utf-8'):
        p=line.rstrip('\n').split('\t')
        if len(p)<3: continue
        m=re.match(r'\w+/p(\d+)_(\w+)\.png',p[0]); obs[(int(m.group(1)),m.group(2))].append((float(p[1]),p[2]))
    og,ob,sb,kb=loadcells(f_og),loadcells(f_b),loadcells(f_suu),loadcells(f_kan)
    out=[]
    for pn,m in sorted(meta.items(),key=lambda x:int(x[0])):
        pn=int(pn); r=m['rows']; top=m['top']; bot=m['bot']; H=bot-top+16; nrows=len(r)-1
        cells=[collections.defaultdict(list) for _ in range(nrows)]
        for col in ('m1','suu','on','nano'):
            for fy,t in sorted(obs.get((pn,col),[])):
                i=bisect.bisect_right(r,top-8+fy*H)-1
                if 0<=i<nrows: cells[i][col].append(t)
        for i,c in enumerate(cells):
            d={k:''.join(v) for k,v in c.items()}
            k=(pn,i)
            oya=mode(sum((cjk1(t) for t in og.get(k+('oya',),[])+ob.get(k+('oya',),[])),[]))
            gyo=mode([ch for t in og.get(k+('gyo',),[])+ob.get(k+('gyo',),[]) for ch in t if ch in '木火土金水'])
            kan=mode(sum((cjk1(t) for t in kb.get(k+('kan',),[])),[]))
            a=re.sub(r'\D','',d.get('suu',''))
            tl=[re.sub(r'\D','',t) for t in sb.get(k+('suu',),[])]; tl=[x for x in tl if x]
            s=a if a else (mode(tl) if tl else '')
            s=fixnum(s)
            m1=d.get('m1','')
            mark='常' if '常' in m1 else ('人' if ('人' in m1 or '①' in m1 or 'A' in m1) else '')
            out.append(dict(page=pn,row=i,oya=oya,kan=kan,suu=int(s) if s else None,gyo=gyo,mark=mark,on=d.get('on',''),nano=d.get('nano','')))
    return out
base=build('meta.json','strips.tsv','cells_oya_gyo.tsv','cells_b.tsv','cells_suu.tsv','cells_kan.tsv')
ext=build('meta_x.json','xstrips.tsv','xcells_oya_gyo.tsv','xcells_b.tsv','xcells_suu.tsv','xcells_kan.tsv')
allr=sorted(base+ext,key=lambda e:(e['page'],e['row']))
good=[]
for e in allr:
    if e['oya'] in ('画','親','字','数') and not e['on'].strip('音訓 '): continue
    if not e['on'] and e['suu'] is None and not e['gyo'] and not e['nano']: continue
    if e['on'] in ('音訓','音','訓'): continue
    good.append(e)
json.dump(good,open('entries_g.json','w'),ensure_ascii=False)
print(len(base),len(ext),len(good))
miss=[(e['page'],e['row']) for e in good if not e['oya'] or e['suu'] is None or not e['gyo']]
json.dump(miss,open('miss2.json','w'))
print('missing now',len(miss))
old=set(map(tuple,json.load(open('miss.json'))))
new=[m for m in miss if tuple(m) not in old]
print('new missing (extra pages etc.)',len(new))
json.dump(new,open('miss_new.json','w'))
