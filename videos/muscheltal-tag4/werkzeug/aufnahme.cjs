// Homepage-Aufnahme Tag 4 (11.11.): erste Hütte → ganze Inselwelt, Gebäude-Montage, Bäckerei (Verlosung), Tierheim, Villa, Anlegestelle (Yacht), Muschelplatz, Nachbarn
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}_-]/gu,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-11T14:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-11T14:11:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});await p.evaluate(()=>cancelAnimationFrame(fly));
const G=await p.evaluate(()=>{const a=fitAll(),m=fitMain();const g=n=>{const x=GEB.find(q=>q.typ===n);return{x:x.cx,y:x.cy}};const f=n=>{const q=PEOPLE.find(q=>q.name.replace('@','')===n);return{x:q.p.x,y:q.p.y}};
 const an=f('anton.van11'),la=f('laura.ngynn');return{a,m,h1:f('sophia_e065'),d:g('doener'),s:g('strandbar'),ac:g('acai'),w:g('werkstatt'),v:g('villa'),b:g('baeckerei'),th:{x:BAU[2].cx,y:BAU[2].cy},an:{x:BAU[1].cx,y:BAU[1].cy},nb:{x:(an.x+la.x)/2,y:(an.y+la.y)/2}};});
const hop=(w,o,z)=>{const t=at('L3',w);return [[t-.25,o.x,o.y+8,z],[t+.4,o.x,o.y+8,z*1.03]];};
const K=[[0,G.h1.x,G.h1.y-4,9],[at('L1','jetzt')-.1,G.h1.x,G.h1.y-4,7.5],[L.L1.end+.2,G.a.x,G.a.y,G.a.z*1.15],
 [L.L2.start+.3,G.m.x,G.m.y,G.m.z*1.05],[L.L2.end,G.m.x,G.m.y,G.m.z*1.25],
 ...hop('Dönerbude',G.d,3.6),...hop('Strandbar',G.s,3.2),...hop('Açaí-Stand',G.ac,3.6),...hop('Moped-Werkstatt',G.w,3.6),...hop('Strandvilla',G.v,3.4),[L.L3.end+.2,G.v.x,G.v.y+8,3.0],
 [L.L4.start+.3,G.b.x,G.b.y-10,4.2],[L.L7.end,G.b.x,G.b.y-10,4.6],
 [L.L8.start+.3,G.m.x,G.m.y,G.m.z*1.2],[at('L8','Tierheim')-.4,G.th.x,G.th.y,3.4],[at('L8','Emilia')-.4,G.v.x,G.v.y-6,3.6],[L.L8.end,G.v.x,G.v.y-6,3.9],
 [L.L9.start+.3,G.an.x,G.an.y-20,2.6],[L.L9.end,G.an.x,G.an.y-10,3.0],
 [L.L10.start+.3,0,40,2.2],[L.L10.end,30,20,2.6],
 [L.L11.start+.2,G.nb.x+4,G.nb.y+22,4.4],[L.L11.end+.3,G.nb.x+4,G.nb.y+22,4.6],[dur,G.a.x,G.a.y,G.a.z*1.1]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
const shot=async(t,f)=>{const c=cam(t);await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
