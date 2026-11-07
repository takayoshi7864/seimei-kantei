import json,collections,statistics
E=json.load(open('entries_v3.json'))
F={(21,5):'回',(4,6):'之',(5,8):'万',(8,5):'匂',(9,11):'廿',(14,11):'旦',(11,9):'乏',(23,7):'亙',(13,7):'乎',(30,1):'尽',(27,10):'弛',(25,1):'冲',(26,0):'吏',(37,2):'妥',(43,11):'身',(64,13):'阜',(42,1):'伺',(71,0):'軍',(44,10):'束',(48,12):'学',(55,12):'宕',(65,11):'寶',(92,2):'骨',(175,6):'鼠',(57,2):'盂',(67,6):'孟',(72,12):'皇',(86,12):'昧',(124,0):'唯',(186,4):'竪',(151,5):'晶',(138,10):'圈',(78,7):'宥',(116,3):'皐',(131,7):'畢',(205,9):'學',(93,3):'畜',(155,1):'尊',(126,2):'寂',(188,4):'噌',(107,2):'栢',(89,1):'挙',(91,10):'高',(116,4):'髙',(96,1):'莱',(97,0):'凉',(132,9):'菩',(106,0):'莊',(136,0):'嵜',(115,11):'崗',(117,3):'雫',(128,2):'逍',(131,13):'貧',(132,2):'冨',(157,0):'富',(133,0):'萌',(160,0):'寛',(138,5):'軽',(141,4):'遅',(215,2):'舊',(194,8):'撃',(209,9):'隣',(155,0):'巽',(178,7):'箇',(187,6):'翠',(195,2):'榉',(200,9):'箱',(220,7):'瞥',(215,6):'薰',(210,7):'薗',(213,9):'壁',(225,4):'璧'}
n=0
for e in E:
    k=(e['page']-16,e['row'])
    if k in F: e['alt']=e['oya']; e['oya']=F[k]; n+=1
print('fixed',n)
# suu truncated '1' fix
bypage=collections.defaultdict(list)
for i,e in enumerate(E): bypage[e['page']].append(i)
fx=0
for p,ids in bypage.items():
    for j,i in enumerate(ids):
        e=E[i]
        if e['suu']==1 and p>18:
            prev=next((E[x]['suu'] for x in reversed(ids[:j]) if E[x]['suu'] and E[x]['suu']>=5),None)
            nxt=next((E[x]['suu'] for x in ids[j+1:] if E[x]['suu'] and E[x]['suu']>=5),None)
            v=prev if prev is not None else nxt
            if v is not None: e['suu']=v; e['suu_guess']=True; fx+=1
print('suu=1 fixed',fx)
json.dump(E,open('entries_v4.json','w'),ensure_ascii=False)
c=collections.Counter(e['oya'] for e in E); print('dups',sum(1 for v in c.values() if v>1),'distinct',len(c))
print('missing suu',sum(e['suu'] is None for e in E))
