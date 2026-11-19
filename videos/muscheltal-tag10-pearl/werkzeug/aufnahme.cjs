// Tag 10 „Golden Pearl“ (19.11.): Homepage-Karte, 3 Seiten: A Tag (Wal), B Tag (Schildkröten), C Nacht (Kino, Club)
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> <t0> <t1> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,t0S,t1S,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}_-]/gu,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const CSS='body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}';
const mk=async(time,q)=>{const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});await p.clock.install({time:new Date(time)});await p.goto('file://'+site+q);await p.clock.runFor(7000);return p;};
const fin=async p=>{await p.addStyleTag({content:CSS});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));};
// A: Wal springt bei L3 ("WAL" ~ Sprung 9,5 s nach Start)
const A=await mk('2026-11-19T14:10:00+01:00','?zeit=tag&wetter=sonne');
const WS=await A.evaluate(()=>{const v=ISL[0],n=TNOW(),h=Math.floor(n/3600);const L=[...walPlan(v,h),...walPlan(v,h+1)].filter(w=>w.start>n+60).sort((a,b)=>a.start-b.start);const w=L[0];return {w:{x:w.x,y:w.y,start:w.start},ep:TEPOCH};});
await A.clock.pauseAt(new Date(WS.ep+(WS.w.start+9.5-at('L3','WAL'))*1000));await fin(A);
// B: Babyschildkröten – bei L4-Start schon 30 % unterwegs
const B=await mk('2026-11-19T15:10:00+01:00','?zeit=tag&wetter=sonne');
const SK=await B.evaluate(()=>{const v=ISL[0],n=TNOW(),h=Math.floor(n/3600);const L=[...skPlan(v,h),...skPlan(v,h+1)].filter(w=>w.start>n+60).sort((a,b)=>a.start-b.start);const w=L[0],P=[];for(const u of[.3,.75]){const d=w.r0+u*(BEX+16);P.push(polar(w.v,w.a,d));}return {start:w.start,P,ep:TEPOCH};});
await B.clock.pauseAt(new Date(SK.ep+(SK.start+.3*60-L.L4.start+.3)*1000));await fin(B);
// C: Freitagabend, Kino läuft
const C=await mk('2026-11-20T20:35:00+01:00','?zeit=nacht&wetter=sonne&termin=kino');await C.clock.pauseAt(new Date('2026-11-20T20:36:00+01:00'));await fin(C);
const G=await A.evaluate(()=>{const a=fitAll(),m=fitMain(),k=ISL[1];return{a,m,cl:{x:KCLUB.cx,y:KCLUB.cy},ki:{x:KKINO.cx,y:KKINO.cy},ko:{x:k.x,y:k.y,R:k.R}};});
const m=G.m,Z=m.z,w=WS.w,[s0,s1]=SK.P,kz=1.25*540/(G.ko.R*2.6667);
// [t, seite, x, y, z]  (gleiche Zeit zweimal = harter Schnitt)
const K=[[0,'A',m.x,m.y,Z*.95],[L.L1b.end+.3,'A',m.x,m.y,Z*1.25],
 [L.L2.start-.05,'A',-90,100,2.9],[L.L2b.end+.3,'A',90,110,3.3],
 [L.L3.start-.05,'A',w.x+14,w.y+12,4.4],[L.L3b.end+.3,'A',w.x+14,w.y+12,5.4],
 [L.L4.start-.05,'B',s0[0],s0[1]+4,7.5],[L.L4.end+.4,'B',s1[0],s1[1]+4,8.2],
 [L.L5.start-.05,'C',G.ki.x,G.ki.y-6,3.3],[L.L5.end+.3,'C',G.ki.x,G.ki.y-6,3.8],
 [L.L6.start-.05,'C',G.ko.x,G.ko.y,kz],[L.L6b.end+.3,'C',G.ko.x,G.ko.y+30,kz*1.5],
 [L.L7.start-.05,'C',G.cl.x,G.cl.y+30,3.2],[L.L7d.end+.3,'C',G.cl.x,G.cl.y+30,3.8],
 [L.L8.start-.05,'A',G.a.x,G.a.y,G.a.z*.95],[L.L8c.end+.3,'A',G.a.x,G.a.y,G.a.z*1.15],
 [L.L9.start-.05,'A',m.x,m.y,Z*1.3],[dur,'A',m.x,m.y,Z*.95]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];if(c[1]!==a[1])return [a[1],a[2],a[3],a[4]];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1],a[2]+(c[2]-a[2])*k,a[3]+(c[3]-a[3])*k,Math.exp(Math.log(a[4])+(Math.log(c[4])-Math.log(a[4]))*k)*(1+.012*Math.sin(t*.8))];};
const PG={A,B,C},last={A:0,B:0,C:0};
const shot=async(t,f)=>{const c=cam(t),p=PG[c[0]];const ms=Math.round((t-last[c[0]])*1000);if(ms>0)await p.clock.runFor(ms);last[c[0]]=Math.max(last[c[0]],t);
 await p.evaluate(c=>{cam.x=c[1];cam.y=c[2];cam.z=c[3];draw();},c);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else{const i0=Math.round(+t0S*30),i1=Math.min(N,Math.round(+t1S*30));for(let i=i0;i<i1;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);}
await b.close();console.log('ok',N);})();
