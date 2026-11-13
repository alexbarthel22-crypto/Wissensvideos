"""Korrigiert geschätzte Wortzeiten im Hook L1 (Werte bei speed 1.15 gemessen, skaliert auf speed 0.95)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Ich':0.0,'baue':.08,'ALLES,':.15,'was':.45,'ihr':.55,'in':.65,'die':.8,'Kommentare':.95,'schreibt!':1.58}
ws=L['L1']['words']
for w in ws: w['start']=round(fix[w['display']]*1.15/0.95,3) if w['display'] in fix else w['start']
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
