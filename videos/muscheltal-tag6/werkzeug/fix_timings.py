"""Korrigiert geschätzte Wortzeiten im Hook L1 (Werte bei speed 1.15 gemessen, skaliert auf speed 0.95)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Auf':0.03,'dieser':.28,'Insel':.55,'wird':.78,'nur':.95,'gebaut,':1.12,'was':1.58,'ihr':1.83,'wollt!':2.2}
ws=L['L1']['words']
for w in ws: w['start']=fix[w['display']] if w['display'] in fix else w['start']
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
