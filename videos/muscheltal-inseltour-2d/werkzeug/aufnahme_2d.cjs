// 2D-Inseltour (19.11.): Homepage-Karte als Hintergrund, Wal-Sprung der Homepage, gleiche Stimme wie die 3D-Tour
// node aufnahme_2d.cjs <site/index.html> <timings.json> <out> <dauer> <t0> <t1> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,t0S,t1S,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}_-]/gu,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-19T14:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);
// Wal der Haupt-Insel suchen, der in der Zukunft startet; Uhr so stellen, dass er bei L0b springt (Sprung ca. 9,5 s nach Start)
const WS=await p.evaluate(()=>{const v=ISL[0],n=TNOW(),h=Math.floor(n/3600);const L=[...walPlan(v,h),...walPlan(v,h+1)].filter(w=>w.start>n+5).sort((a,b)=>a.start-b.start);const w=L[0];return {w:{x:w.x,y:w.y,start:w.start,dir:w.dir},ep:TEPOCH};});
const WSTART=WS.w.start+9.5-L.L0b.start;// TNOW bei Video-t=0
await p.clock.pauseAt(new Date(WS.ep+WSTART*1000));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}'});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));
const G=await p.evaluate(()=>{const a=fitAll(),m=fitMain(),g=t=>{const q=GEB.find(q=>q.typ===t);return q?{x:q.cx,y:q.cy}:{x:0,y:0};};
 const k=ISL[1];
 return{a,m,ti:g('tierheim'),dn:g('doener'),bk:g('baeckerei'),sb:g('strandbar'),cl:{x:KCLUB.cx,y:KCLUB.cy},gl:{x:KGAME.cx,y:KGAME.cy},ki:{x:KKINO.cx,y:KKINO.cy},ko:{x:k.x,y:k.y,R:k.R}};});
G.w=WS.w;console.error(JSON.stringify(G));
const m=G.m,Z=m.z,w=G.w;
const K=[[0,m.x,m.y,Z*.92],[L.L1.end,m.x,m.y,Z*1.12],
 [L.L1b.start,m.x,m.y,Z*1.12],[L.L0b.start-.05,w.x,w.y,2.4],
 [L.L0b.start,w.x+14,w.y+12,5.0],[L.L0c.end+.3,w.x+14,w.y+12,5.6],
 [L.L1t.start-.1,m.x,m.y,Z*1.6],[L.L1t.end+.3,m.x,m.y,Z*1.05],
 [L.L2.start,0,24,2.9],[L.L2.end+.3,0,24,3.3],
 [L.L2b.start,-70,110,3.0],[L.L2c.end+.2,70,110,3.2],
 [L.L3.start,G.dn.x,G.dn.y+30,3.8],[at('L3','und')-.05,G.dn.x,G.dn.y+30,4.0],[at('L3','und'),G.bk.x,G.bk.y+30,3.8],[L.L3.end+.3,G.bk.x,G.bk.y+30,4.0],
 [L.L3s.start,G.sb.x,G.sb.y+30,3.6],[L.L3s.end+.3,G.sb.x,G.sb.y+30,3.9],
 [L.L3t.start,G.ti.x,G.ti.y+30,3.6],[L.L3t.end+.3,G.ti.x,G.ti.y+30,3.9],
 [L.L3k.start,G.ko.x,G.ko.y,1.25*540/(G.ko.R*2.6667)],[L.L3k.end+.2,G.ko.x,G.ko.y+20,3.0],
 [L.L3g.start,G.cl.x,G.cl.y+30,3.6],[at('L3g','Game')-.05,G.cl.x,G.cl.y+30,3.8],[at('L3g','Game'),G.gl.x,G.gl.y+30,3.6],[L.L3g.end+.3,G.gl.x,G.gl.y+30,3.8],
 [L.L3c.start,G.ki.x,G.ki.y+30,3.6],[L.L3c.end+.3,G.ki.x,G.ki.y+30,3.9],
 [L.L4.start,m.x,m.y,Z*1.3],[L.L4.end+.3,m.x,m.y,Z*1.0],
 [L.L5f.start,G.a.x,G.a.y,G.a.z],[L.L5f.end+.3,G.a.x,G.a.y,G.a.z*1.08],
 [L.L5k.start,G.ko.x,G.ko.y,1.3*540/(G.ko.R*2.6667)],[L.L5k.end+.3,G.ko.x,G.ko.y,1.45*540/(G.ko.R*2.6667)],
 [L.L5.start,m.x,m.y,Z*1.25],[dur,m.x,m.y,Z*.95]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
let last=0;const shot=async(t,f)=>{const c=cam(t);const ms=Math.round((t-last)*1000);if(ms>0)await p.clock.runFor(ms);last=t;
 await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else{const i0=Math.round(+t0S*30),i1=Math.min(N,Math.round(+t1S*30));for(let i=i0;i<i1;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);}
await b.close();console.log('ok',N);})();
