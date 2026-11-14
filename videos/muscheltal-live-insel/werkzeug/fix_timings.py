"""Wortzeiten im Hook L1 (Energie-Analyse)."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
fix={'Wir':0.05,'bauen':.22,'gerade':.48,'live':.8,'eure':1.08,'neue':1.42,'Welt!':1.62}
ws=L['L1']['words']
for w in ws: w['start']=fix.get(w['display'],w['start'])
for a,b in zip(ws,ws[1:]): a['end']=b['start']
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok')
