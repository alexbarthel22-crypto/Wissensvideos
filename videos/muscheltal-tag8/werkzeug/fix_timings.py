"""Korrigiert geschätzte Wortzeiten im Hook L1 (Werte bei speed 1.15 gemessen, skaliert auf speed 0.95)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Ich':0.0,'war':.18,'zum':.33,'ersten':.38,'Mal':.62,'LIVE':.72,'ihr':1.33,'habt':1.48,'eine':1.6,'ganze':1.88,'Insel':2.18,'gebaut!':2.45}
ws=L['L1']['words']
for w in ws: w['start']=fix[w['display']] if w['display'] in fix else w['start']
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
