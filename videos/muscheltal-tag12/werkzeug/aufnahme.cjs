// Tag 12 (22.11.): Tag 1 (Bild) → Tag 12 Karte, Gebäude-Blitzschnitte, Tierheim nah, Übersicht
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> <t0> <t1> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,t0S,t1S,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}_-]/gu,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const CSS='body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}';
const mk=async(t0,t1,q)=>{const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});await p.clock.install({time:new Date(t0)});await p.goto('file://'+site+q);await p.clock.runFor(7000);await p.clock.pauseAt(new Date(t1));
 await p.addStyleTag({content:CSS});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));return p;};
const A=await mk('2026-11-22T14:10:00+01:00','2026-11-22T14:11:00+01:00','?zeit=tag&wetter=sonne');
const C=await mk('2026-11-21T22:30:00+01:00','2026-11-21T22:31:00+01:00','?zeit=nacht&wetter=sonne');
const G=await A.evaluate(()=>{const g=t=>{const q=GEB.find(q=>q.typ===t);return q?[q.cx,q.cy]:[0,0]};return{m:fitMain(),th:g('tierheim'),gp:[GP.X,GP.Y],cl:[KCLUB.cx,KCLUB.cy],ki:[KKINO.cx,KKINO.cy]}});const m=G.m;
const t1b=L.L1b.start;
const K=[[0,'A',m.x,m.y,m.z*1.05],[t1b+1.2,'A',m.x,m.y,m.z*1.15],
 [at('L2','Palast')-.05,'A',0,10,2.6],[at('L2','Club')-.06,'A',0,10,2.9],
 [at('L2','Club')-.05,'C',G.cl[0],G.cl[1]-4,3.6],[at('L2','Kino')-.06,'C',G.cl[0],G.cl[1]-4,4.0],
 [at('L2','Kino')-.05,'C',G.ki[0],G.ki[1]-14,3.0],[at('L2','Golden')-.06,'C',G.ki[0],G.ki[1]-14,3.3],
 [at('L2','Golden')-.05,'C',G.gp[0],G.gp[1]-30,1.6],[L.L2b.end+.2,'C',G.gp[0],G.gp[1]-40,1.9],
 [L.L3.start-.05,'A',G.th[0],G.th[1]+8,4.0],[L.L4b.end+.3,'A',G.th[0],G.th[1]+8,5.4],[L.L6.start-.05,'C',G.gp[0],G.gp[1]-40,1.7],[L.L6.end+.2,'C',G.gp[0],G.gp[1]-50,2.1],[L.L6b.start-.05,'C',m.x,m.y,m.z*2.6],[L.L6b.end+.2,'C',m.x,m.y,m.z*2.9],[L.L7.start-.05,'A',-150,100,3.0],[L.L7b.end+.2,'A',150,100,3.0],[L.L8.start-.05,'A',m.x,m.y,m.z*.9],[L.L8b.end+.2,'A',m.x,m.y,m.z*1.1],
 [L.L5.start-.05,'A',m.x,m.y,m.z*1.3],[dur,'A',m.x,m.y,m.z]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];if(c[1]!==a[1])return [a[1],a[2],a[3],a[4]];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
 return [a[1],a[2]+(c[2]-a[2])*k,a[3]+(c[3]-a[3])*k,Math.exp(Math.log(a[4])+(Math.log(c[4])-Math.log(a[4]))*k)];};
const PG={A,C},last={A:0,C:0};
const shot=async(t,f)=>{const c=cam(t),p=PG[c[0]];const ms=Math.round((t-last[c[0]])*1000);if(ms>0)await p.clock.runFor(ms);last[c[0]]=Math.max(last[c[0]],t);
 await p.evaluate(c=>{cam.x=c[1];cam.y=c[2];cam.z=c[3];draw();},c);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else{const i0=Math.round(+t0S*30),i1=Math.min(N,Math.round(+t1S*30));for(let i=i0;i<i1;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);}
await b.close();console.log('ok',N);})();
