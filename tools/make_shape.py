"""字の構造（縦に割れるか・横に割れるか）の表 data/shape.json を作る。
元データ：CJKVI IDS（CHISE IDS 由来・GPLv2）https://github.com/cjkvi/cjkvi-ids
  ※元データ（ids.txt）はリポジトリに含めない。このスクリプトが、実行時に取得して、結果だけを保存する。
規則（講義レジュメの図解に合わせた近似）：
  縦に割れる(V)：左右（⿰・⿲）・しんにょう等（⿺）の構造、上下に重なる部品がすべて縦に割れるもの、
                 または、草冠（艹）の字（艹は十十で左右に分かれた部品なので、下の部品にかかわらず縦に割れる）
  横に割れる(H)：上下（⿱・⿳）の構造、または、左右の部品がすべて横に割れるもの
                 垂れ（⿸・⿹）は、まだれ（广）・がんだれ（厂）で、中が独立した字のものだけ（例：麻＝广＋林）
                 やまいだれ（疒）・しかばね（尸）などの他の垂れは横に割れない
  ただし、正は横分離の例外として、Hから外す。（安は、レジュメの横分離の例「安藤 麻希」に合わせて、Hに含める）
  中の字が独立しているかの判定は、中の部品が1字で、かつ辞書にある字かで行い、講義・資料で個別に示された字は TARE_H・TARE_NOT で上書きする。
"""
import json, os, sys, urllib.request
root=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cache=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.environ.get('TMPDIR','/tmp'),'cjkvi_ids.txt')
if not os.path.exists(cache):
    # 例：curl -sL -o /tmp/cjkvi_ids.txt https://raw.githubusercontent.com/cjkvi/cjkvi-ids/master/ids.txt
    sys.exit('ids.txt がありません。次で取得してください：curl -sL -o '+cache+' https://raw.githubusercontent.com/cjkvi/cjkvi-ids/master/ids.txt')
ids={}
for l in open(cache,encoding='utf-8'):
    if l.startswith('#') or not l.strip(): continue
    p=l.rstrip('\n').split('\t')
    if len(p)>=3 and p[1] not in ids: ids[p[1]]=p[2]       # 先頭の読み（地域指定のない・または最初のもの）を使う
dic=json.load(open(os.path.join(root,'data','dict.json'),encoding='utf-8'))
chars=sorted({e['c'] for e in dic}|{e['k'] for e in dic if e.get('k')})
DICT_CHARS=set(c for c in chars if len(c)==1)
import re
ARITY={'⿰':2,'⿱':2,'⿲':3,'⿳':3,'⿴':2,'⿵':2,'⿶':2,'⿷':2,'⿸':2,'⿹':2,'⿺':2,'⿻':2}
def clean(s): return re.sub(r'\[[A-Z]+\]$','',s)
def parse(s,i=0):
    c=s[i]
    if c in ARITY:
        kids=[]; j=i+1
        for _ in range(ARITY[c]):
            k,j=parse(s,j); kids.append(k)
        return (c,kids),j
    return c,i+1
def tree(ch):
    s=ids.get(ch)
    if not s: return ch
    s=clean(s)
    if s==ch: return ch
    try: t,_=parse(s); return t
    except Exception: return ch
KUSA={'艹','⺾','⺿'}
def top_kusa(n,d=0):
    # 一番上の部品が草冠か（莫→慕 のように重なっていても上をたどる）
    if d>6: return False
    if isinstance(n,tuple):
        op,kids=n
        return op in '⿱⿳' and top_kusa(kids[0],d+1)
    if n in KUSA: return True
    t=tree(n)
    return top_kusa(t,d+1) if t!=n else False
def V(n,d=0):
    if d>6: return False
    if isinstance(n,tuple):
        op,kids=n
        if op in '⿰⿲⿺': return True
        if op in '⿱⿳': return top_kusa(kids[0]) or all(V(k,d+1) for k in kids)
        return False
    if n=='艹': return True                     # 艹は屮屮（左右に割れる）
    t=tree(n)
    return V(t,d+1) if t!=n else False
def H(n,d=0):
    if d>6: return False
    if isinstance(n,tuple):
        op,kids=n
        if op in '⿱⿳': return True
        if op in '⿸⿹': return tare_h(kids[0],kids[1])
        if op in '⿰⿲': return all(H(k,d+1) for k in kids)
        return False
    t=tree(n)
    return H(t,d+1) if t!=n else False
TARE_OUT={'广','厂','麻'}           # まだれ・がんだれ（麻は广＋林で、摩・磨などの上に乗る）
TARE_H={'原','厚','麿'}              # 資料で横に割れるとされた字（原＝厂＋泉、厚）と、麿（麻＋呂。IDSでは呂が異体の吕）
TARE_NOT={'広','庄'}                 # 資料で割れないとされた字
def tare_h(outer,inner):
    return (not isinstance(outer,tuple)) and outer in TARE_OUT and (not isinstance(inner,tuple)) and inner in DICT_CHARS
NORM={'亻':'人','氵':'水','扌':'手','忄':'心','礻':'示','⺼':'月','𧾷':'足','⻌':'辶','⻏':'阝','⻖':'阝','衤':'衣','⺾':'艹','⺿':'艹','灬':'火','⺌':'小','罒':'网','犭':'犬','饣':'食'}
def comp(n):
    if isinstance(n,tuple): return None
    return NORM.get(n,n)
def parts(ch):
    t=tree(ch)
    if not isinstance(t,tuple): return None
    op,kids=t
    if op in '⿰⿲': a,b=comp(kids[0]),comp(kids[-1]); return ('h',a,b) if a and b else None
    if op in '⿱⿳': a,b=comp(kids[0]),comp(kids[-1]); return ('v',a,b) if a and b else None
    return None
v=''.join(c for c in chars if len(c)==1 and V(tree(c)))
h=''.join(c for c in chars if len(c)==1 and ((H(tree(c)) and c not in TARE_NOT) or c in TARE_H) and c not in '正')
pp={}
for c in chars:
    if len(c)==1:
        r=parts(c)
        if r: pp[c]=r[0]+r[1]+r[2]
json.dump({'v':v,'h':h,'p':pp},open(os.path.join(root,'data','shape.json'),'w',encoding='utf-8'),ensure_ascii=False)
print('parts',len(pp))
print('chars',len(chars),'V',len(v),'H',len(h))
# 講義レジュメの例で確認
chk=lambda s,f:[c for c in s if c not in (v if f=='v' else h)]
for name,f in [('野村佳代','v'),('加藤明','v'),('渡部透','v'),('服部礼次郎','v'),('芳賀実','h'),('芝章宏','h'),('安藤麻希','h')]:
    print(name,f,'全字が該当' if not chk(name,f) else '外れた字:'+''.join(chk(name,f)))
print('川 V/H:',('川' in v),('川' in h))
print('朝 V/H:',('朝' in v),('朝' in h))
