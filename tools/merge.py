import json,re,collections
rows=json.load(open('rows.json'))
def cjk1(s): return [c for c in s if '一'<=c<='鿿' or '㐀'<=c<='䶿' or '\U00020000'<=c<='\U0002ffff' or c in '々']
def load(fn):
    import re as _re
    d=collections.defaultdict(list)
    for line in open(fn,encoding='utf-8'):
        p=line.rstrip('\n').split('\t')
        if len(p)<3: continue
        m=re.match(r'(?:ca|kb|cs|cb)/p(\d+)_r(\d+)_(\w+)\.png',p[0])
        d[(int(m.group(1)),int(m.group(2)),m.group(3))].append(p[2])
    return d
og=load('cells_oya_gyo.tsv'); kb=load('cells_kan.tsv'); sb=load('cells_suu.tsv'); ob=load('cells_b.tsv')
def mode(chars):
    if not chars: return ''
    return collections.Counter(chars).most_common(1)[0][0]
out=[]
for r in rows:
    k=(r['page'],r['row'])
    oya=mode(sum((cjk1(t) for t in og.get(k+('oya',),[])+ob.get(k+('oya',),[])),[]))
    gyo=mode([c for t in og.get(k+('gyo',),[])+ob.get(k+('gyo',),[]) for c in t if c in '木火土金水'])
    kan=mode(sum((cjk1(t) for t in kb.get(k+('kan',),[])),[]))
    _a=re.sub(r'\D','',r.get('suu',''))
    _t=[re.sub(r'\D','',t) for t in sb.get(k+('suu',),[])]
    _t=[x for x in _t if x]
    suu=_a if _a else (collections.Counter(_t).most_common(1)[0][0] if _t else '')
    m1=r.get('m1','')
    mark='常' if '常' in m1 else ('人' if ('人' in m1 or '①' in m1 or 'A' in m1) else '')
    out.append(dict(page=r['page'],row=r['row'],oya=oya,kan=kan,suu=int(suu) if suu else None,gyo=gyo,mark=mark,on=r.get('on',''),nano=r.get('nano','')))
json.dump(out,open('entries_raw.json','w'),ensure_ascii=False)
n=len(out)
print('rows',n,'no oya',sum(not e['oya'] for e in out),'no suu',sum(e['suu'] is None for e in out),'no gyo',sum(not e['gyo'] for e in out),'no on',sum(not e['on'] for e in out))
# gogyo from first kana of on
GY={}
for ch in 'カキクケコガギグゲゴ': GY[ch]='木'
for ch in 'タチツテトダヂヅデドナニヌネノラリルレロ': GY[ch]='火'
for ch in 'アイウエオヤユヨワ': GY[ch]='土'
for ch in 'サシスセソザジズゼゾ': GY[ch]='金'
for ch in 'ハヒフヘホバビブベボパピプペポマミムメモ': GY[ch]='水'
mis=[]
for e in out:
    on=e['on']
    kana=re.sub(r'[^ァ-ヶぁ-ん]','',on)
    if not kana or not e['gyo']: continue
    c=kana[0]
    c=chr(ord(c)+0x60) if 'ぁ'<=c<='ん' else c
    exp=GY.get(c)
    if exp and exp!=e['gyo']: mis.append((e['page'],e['oya'],e['gyo'],exp,on[:16]))
print('gyo mismatches vs first reading',len(mis))
for m in mis[:25]: print(m)
