"""Korrigiert geschätzte Wortzeiten im Hook L1 (nach tts_de.py erneut ausführen)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Was':0.0,'wäre,':.25,'wenn':.45,'deine':.62,'Follower':1.1,'eine':1.5,'ganze':1.8,'Insel':2.05,'besiedeln?!':2.45}
ws=L['L1']['words']
for w in ws: w['start']=fix.get(w['display'],w['start'])
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
