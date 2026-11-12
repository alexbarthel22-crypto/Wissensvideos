"""Korrigiert geschätzte Wortzeiten im Hook L1 (nach tts_de.py erneut ausführen; Werte aus Energie-Analyse)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Stell':0.08,'dir':.3,'vor,':.5,'deine':1.03,'Follower':1.3,'würden':1.68,'eine':1.95,'Insel':2.3,'besiedeln!':2.55}
ws=L['L1']['words']
for w in ws: w['start']=fix.get(w['display'],w['start'])
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
