"""Korrigiert geschätzte Wortzeiten (nach tts_de.py erneut ausführen): L3-Aufzählung, L10-Gruppen."""
import json
p='assets/voice/timings.json';t=json.load(open(p));L={x['id']:x for x in t['lines']}
ws=L['L3']['words'];st=ws[0]['start'];r=1.1/0.92
fix=[('eine',14.3),('Strandbar,',14.55),('einen',15.05),('Açaí-Stand',15.25),('eine',15.95),('Moped-Werkstatt',16.15),('und',16.85),('eine',17.0),('Strandvilla',17.25)];j=0
for i,w in enumerate(ws):
  if i>=4 and j<len(fix) and w['display']==fix[j][0]: w['start']=round(st+(fix[j][1]-12.84)*r,3); j+=1
for a,b in zip(ws,ws[1:]): a['end']=b['start']
ws=L['L10']['words'];sh=ws[0]['start']-55.27
win={0:(55.3,55.95),1:(56.2,57.05),2:(57.25,58.35),3:(58.45,59.7),4:(59.95,61.6),5:(61.75,62.75)}
for g,(a,b) in win.items():
  a+=sh;b+=sh;gw=[w for w in ws if w['group']==g];tot=sum(max(1,len(w['display'])) for w in gw);x=a
  for w in gw:
    d=(b-a)*max(1,len(w['display']))/tot;w['start']=round(x,3);w['end']=round(x+d,3);x+=d
json.dump(t,open(p,'w'),ensure_ascii=False,indent=1);print('ok',j)
