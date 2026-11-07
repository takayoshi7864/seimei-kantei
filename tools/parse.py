import json,re,collections,bisect
meta=json.load(open('meta.json'))
obs=collections.defaultdict(list)
for line in open('strips.tsv',encoding='utf-8'):
    p=line.rstrip('\n').split('\t')
    if len(p)<3: continue
    m=re.match(r'cr/p(\d+)_(\w+)\.png',p[0])
    obs[(int(m.group(1)),m.group(2))].append((float(p[1]),p[2]))
def cjk(s): return ''.join(c for c in s if '一'<=c<='鿿' or '㐀'<=c<='䶿' or '\U00020000'<=c<='\U0002ffff' or c in '々〆')
rows_out=[]
for pn,m in sorted(meta.items(),key=lambda x:int(x[0])):
    pn=int(pn); r=m['rows']; top=m['top']; bot=m['bot']; H=bot-top+16
    nrows=len(r)-1
    cells=[collections.defaultdict(list) for _ in range(nrows)]
    for col in ('oya','m1','kan','m2','suu','gyo','on','nano'):
        for fy,t in sorted(obs.get((pn,col),[])):
            y=top-8+fy*H
            i=bisect.bisect_right(r,y)-1
            if 0<=i<nrows: cells[i][col].append(t)
    for i,c in enumerate(cells):
        d={k:''.join(v) for k,v in c.items()}
        d['page']=pn; d['row']=i
        rows_out.append(d)
json.dump(rows_out,open('rows.json','w'),ensure_ascii=False)
print(len(rows_out))
