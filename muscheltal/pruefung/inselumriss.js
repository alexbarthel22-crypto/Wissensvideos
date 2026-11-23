// Aufruf: python3 muscheltal/bau.py && node muscheltal/pruefung/inselumriss.js && python3 muscheltal/bau.py
// Schreibt die Küstenlinien aller Inseln (im Raster der Statistik-Heatmap, 1 Einheit = 60 px) nach daten/inselumriss.json –
// die Statistikseite zeichnet damit die Insel-Umrisse unter die Heatmap. Nur nötig, wenn sich Inseln ändern.
const {chromium}=require('playwright'),path=require('path'),fs=require('fs');(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.join(__dirname,'..','site','index.html')+'?zeit=tag');await p.waitForTimeout(2500);
const r=await p.evaluate(()=>ISL.map(v=>{const pts=[];for(let a=0;a<Math.PI*2;a+=.08){const [x,y]=polar(v,a,coastAt(v,a));pts.push([Math.round(x/60*10)/10,Math.round(y/60*10)/10]);}return{i:v.i,pts};}));
const ins=JSON.parse(fs.readFileSync(path.join(__dirname,'..','daten','insel.json'),'utf8')).inseln;r.forEach(o=>o.name=ins[o.i]?ins[o.i].name:'Insel '+(o.i+1));
fs.writeFileSync(path.join(__dirname,'..','daten','inselumriss.json'),JSON.stringify(r));console.log(r.map(o=>o.name+': '+o.pts.length+' Punkte').join('\n'));await b.close();})();
