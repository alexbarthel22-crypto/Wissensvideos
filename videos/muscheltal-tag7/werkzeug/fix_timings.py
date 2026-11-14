"""Korrigiert geschätzte Wortzeiten im Hook L1 (Werte bei speed 1.15 gemessen, skaliert auf speed 0.95)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Diese':0.05,'Insel':.35,'wächst':.58,'durch':.84,'Follower,':1.13,'die':1.76,'einziehen!':1.96}
ws=L['L1']['words']
for w in ws: w['start']=fix[w['display']] if w['display'] in fix else w['start']
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
