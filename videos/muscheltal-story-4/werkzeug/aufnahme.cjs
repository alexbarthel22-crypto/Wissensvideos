// Story 4: Ich-Perspektive – vom Wasser auf die Kokos-Küste, über den Holzsteg an den ersten Kokosnuss-Hütten vorbei
// zum Lagerfeuer, dann Blick über die ganze (noch fast leere) Insel. Kamera passend zu den Wortzeiten (timings.json).
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));
const L={};for(const l of T.lines)L[l.id]=l;
const dur=+process.argv[5]||T.duration+1.6,N=Math.round(dur*30);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-08T13:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag');await p.clock.runFor(7000);
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});
const G=await p.evaluate(()=>{cancelAnimationFrame(fly);const v=ISL[1];let y=v.y;while(inside(v,v.x,y,-6))y+=4;
 const near=v.people.filter(q=>q.p&&Math.abs(q.p.x-v.x)<90&&q.p.y>v.y);const ring=(near.length?Math.max(...near.map(q=>q.p.y)):v.y+v.plaza+60)-v.y;return{x:v.x,y:v.y,coast:y,ring,R:v.R,plaza:v.plaza};});
const zAll=405/(2*(G.R+40));
// Schlüsselbilder [zeit, x, y, z]: Blick nach vorn = Kamera wandert nach Norden (Bild läuft nach unten weg)
const K=[[0,G.x,G.coast+120,1.7],[L.L1.end-.4,G.x,G.coast-40,2.5],
 [L.L2.start+.3,G.x,G.y+G.ring+10,3.6],[L.L2.end,G.x,G.y+G.ring-25,4.1],
 [L.L3.start+.2,G.x,G.y+20,3.0],[L.L3.start+2.2,G.x,G.y+20,zAll*1.25],[L.L4.end,G.x,G.y+20,zAll*1.05],[dur,G.x,G.y+20,zAll*1.0]];
fs.mkdirSync(out,{recursive:true});
for(let i=0;i<N;i++){const t=i/30;
 await p.evaluate(([t,K,e2])=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],b2=K[Math.min(j+1,K.length-1)];let k=b2[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(b2[0]-a[0]))):1;k=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
  const walk=t<e2?1:Math.max(0,1-(t-e2)/.8);// Schritte (leichtes Wippen), solange man geht
  cam.z=Math.exp(Math.log(a[3])+(Math.log(b2[3])-Math.log(a[3]))*k)*(1+.012*walk*Math.sin(t*11.3));
  cam.x=a[1]+(b2[1]-a[1])*k+walk*Math.sin(t*5.65)*2.2/cam.z;cam.y=a[2]+(b2[2]-a[2])*k+walk*Math.abs(Math.sin(t*5.65))*3/cam.z;draw();},[t,K,L.L2.end]);
 await p.clock.runFor(33.333);await p.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();console.log('frames',N);})();
