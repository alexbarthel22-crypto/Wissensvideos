"""Korrigiert geschätzte Wortzeiten im Hook L1 (nach tts_de.py erneut ausführen; Werte aus Energie-Analyse)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Stell':0.03,'dir':.17,'vor,':.29,'deine':.62,'Follower':.82,'würden':1.08,'eine':1.43,'Insel':1.6,'besiedeln!':2.18}
ws=L['L1']['words']
for w in ws: w['start']=fix.get(w['display'],w['start'])
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
