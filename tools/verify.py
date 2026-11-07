import json,re,collections
E=json.load(open('entries_final.json')); R=json.load(open('match_res.json')); D=json.load(open('dcs.json'))
def parse(on):
    on=re.sub(r'[（(][^）)]*[）)]','',on).replace('/','／')
    a,_,b=on.partition('／')
    ons=[t for t in re.split(r'[・\s]',a) if t and re.fullmatch(r'[ァ-ヶー]+',t)]
    kuns=[t for t in re.split(r'[・\s]',b) if t and re.fullmatch(r'[ぁ-ん]+',t)]
    return ons,kuns
def vscore(c,ons,kuns):
    t=D.get(c)
    if not t: return None
    head=t.split('【')[0]
    body=t[:900]
    v=0
    for o in ons:
        if re.search(re.escape(o)+r'[「（\(]',body) or re.search(r'(?<![ァ-ヶ])'+re.escape(o)+r'(?![ァ-ヶ])',body): v+=2
    for k in kuns:
        if len(k)>=2 and (k in head or ('「'+k) in body or k in body[:200]): v+=1
    return v
out=[];chg=[];unk=0
for e,r in zip(E,R):
    ons,kuns=parse(e['on'])
    cand=[(r['ocr'],r['ocr_s'])]+[(c,s) for c,s in r['top'] if c!=r['ocr']]
    sc=[]
    for c,s in cand:
        v=vscore(c,ons,kuns)
        sc.append((c,s,v))
    e['_sc']=sc
    ocr=sc[0]
    best=max(sc,key=lambda x:((x[2] if x[2] is not None else -1),x[1]))
    e['vs_ocr']=ocr[2]
    if ocr[2] is None: unk+=1
    if best[0]!=ocr[0] and (best[2] or 0)>(ocr[2] if ocr[2] is not None else -1) and best[1]>=0.55:
        chg.append((e['page']-16,e['row'],ocr[0],ocr[2],best[0],best[2],round(best[1],2),e['on'][:14]))
print('ocr unknown to dict',unk,'would change',len(chg))
for c in chg[:70]: print(c)
json.dump(chg,open('chg.json','w'),ensure_ascii=False)
