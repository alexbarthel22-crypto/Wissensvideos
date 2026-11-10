// Homepage-Aufnahme Tag 3 (10.11.): Streuner, Tierheim, Açaí, Werkstatt, Pool, Villa, Kokos-Tiere
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> [test-zeiten,komma]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));
const L={};for(const l of T.lines)L[l.id]=l;const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^a-z0-9äöüß-]/g,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const mk=async zeit=>{const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
 await p.clock.install({time:new Date('2026-11-10T13:10:00+01:00')});await p.goto('file://'+site+'?zeit='+zeit+'&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-10T13:11:00+01:00'));
 await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});await p.evaluate(()=>cancelAnimationFrame(fly));return p;};
const day=await mk('tag');
const G=await day.evaluate(()=>{const a=fitAll(),m=fitMain();const g=n=>{const x=GEB.find(q=>q.typ===n);return{x:x.cx,y:x.cy}};const lu=PEOPLE.find(q=>q.name.replace('@','')==='luisedbr.11');
 const P=PETS.list.filter(q=>q.v.i===0);let best=null,bn=0;for(const c of P){const n=P.filter(q=>Math.hypot(q.x-c.x,q.y-c.y)<55).length;if(n>bn){bn=n;best=c;}}
 const PK=PETS.list.filter(q=>q.v.i===1);let bk=null,bkn=0;for(const c of PK){const n=PK.filter(q=>Math.hypot(q.x-c.x,q.y-c.y)<60).length;if(n>bkn){bkn=n;bk=c;}}
 return{a,m,pt:{x:best.x,y:best.y},pk:{x:bk.x,y:bk.y},th:{x:BAU[2].cx,y:BAU[2].cy},ac:g('acai'),wk:g('werkstatt'),v:g('villa'),lu:{x:lu.p.x,y:lu.p.y}};});
console.error(JSON.stringify(G));
const K=[[0,G.pt.x,G.pt.y,5.2],[L.L1.end,G.pt.x+10,G.pt.y+4,4.6],
 [L.L2.start+.3,G.th.x,G.th.y+8,3.6],[L.L2.end,G.th.x,G.th.y+8,4.0],
 [L.L3.start+.4,G.m.x,G.m.y+20,G.m.z*1.15],[at('L3','sonst'),G.pt.x,G.pt.y,3.4],[L.L3.end,G.pt.x,G.pt.y,4.2],
 [L.L4.start+.3,G.ac.x,G.ac.y-12,4.4],[L.L4.end,G.ac.x,G.ac.y-12,5.0],
 [L.L5.start+.3,G.wk.x,G.wk.y-12,4.4],[L.L5.end,G.wk.x,G.wk.y-12,5.0],
 [L.L6.start+.4,G.lu.x+10,G.lu.y-14,6.8],[L.L6.end,G.lu.x+10,G.lu.y-14,7.4],
 [L.L7.start+.4,G.v.x+30,G.v.y-6,4.4],[L.L8.end,G.v.x+30,G.v.y-6,4.9],
 [L.L9.start+.4,G.th.x-60,G.th.y-40,2.8],[L.L9.end,G.th.x+40,G.th.y-20,3.0],
 [L.L10.start+.4,G.pk.x,G.pk.y,4.0],[at('L10','Folgt'),G.pk.x,G.pk.y,3.4],[dur,G.a.x,G.a.y,G.a.z*1.1]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],b2=K[Math.min(j+1,K.length-1)];let k=b2[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(b2[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(b2[1]-a[1])*k,a[2]+(b2[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(b2[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
const shot=async(t,f)=>{const p=day,c=cam(t);await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}
else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
