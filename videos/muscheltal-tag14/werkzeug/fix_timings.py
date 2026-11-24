"""Korrigiert geschätzte Wortzeiten im Hook L1 (Werte bei speed 1.15 gemessen, skaliert auf speed 0.95)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Ihr':0.02,'habt':.3,'im':.45,'LIVE':.55,'eine':.85,'ganze':1.15,'Insel':1.45,'gebaut!':1.85}
ws=L['L1']['words']
for w in ws: w['start']=fix[w['display']] if w['display'] in fix else w['start']
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
