"""Wortzeiten im Hook L1 (Energie-Analyse)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Ich':0.0,'bin':.14,'gerade':.25,'LIVE':.58,'wir':1.05,'bauen':1.2,'eure':1.44,'neue':1.72,'Welt!':1.98,'Kommt':2.42,'rein!':2.85}
ws=L['L1']['words']
for w in ws: w['start']=fix.get(w['display'],w['start'])
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
