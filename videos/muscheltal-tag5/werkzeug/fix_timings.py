"""Korrigiert geschätzte Wortzeiten im Hook L1 (nach tts_de.py erneut ausführen)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Was':0.0,'wäre,':.3,'wenn':.8,'deine':.93,'Follower':1.2,'eine':1.6,'Insel':1.88,'besiedeln?!':2.1}
ws=L['L1']['words']
for w in ws: w['start']=fix.get(w['display'],w['start'])
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
