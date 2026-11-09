// Homepage-Aufnahme Tag 2 (9.11.): Kamerafahrt zu Dönerbude, Strandbar (Tag -> Nacht), Palast, Villa, Baustellen
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> [test-zeiten,komma]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));
const L={};for(const l of T.lines)L[l.id]=l;const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^a-z0-9äöüß-]/g,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const mk=async zeit=>{const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
 await p.clock.install({time:new Date('2026-11-09T13:10:00+01:00')});await p.goto('file://'+site+'?zeit='+zeit+'&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-09T13:11:00+01:00'));
 await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});await p.evaluate(()=>cancelAnimationFrame(fly));return p;};
const day=await mk('tag'),night=await mk('nacht');const SITE3=process.env.SITE3;let dayPL=day;if(SITE3){const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});await p.clock.install({time:new Date('2026-11-09T13:10:00+01:00')});await p.goto('file://'+SITE3+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-09T13:11:00+01:00'));await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});await p.evaluate(()=>cancelAnimationFrame(fly));dayPL=p;}
const G=await day.evaluate(()=>{const m=fitMain(),a=fitAll(),k=ISL[1];const g=n=>{const x=GEB.find(q=>q.typ===n);return{x:x.cx,y:x.cy}};
 const bau=BAU.map(q=>({x:q.cx,y:q.cy}));const so=PEOPLE.find(q=>q.name.replace('@','')==='sophia_e065'),an=PEOPLE.find(q=>q.name.replace('@','')==='anton.van11'),la=PEOPLE.find(q=>q.name.replace('@','')==='laura.ngynn');return{nb:{x:(an.p.x+la.p.x)/2,y:(an.p.y+la.p.y)/2,a:[an.p.x,an.p.y],l:[la.p.x,la.p.y]},so:so&&so.p?{x:so.p.x,y:so.p.y}:{x:0,y:0},m,a,k:{x:k.x,y:k.y,R:k.R},d:g('doener'),s:g('strandbar'),v:g('villa'),mayor:{x:0,y:36*PAL_S+4},bau};});
const MID={x:(G.m.x+G.k.x)/2,y:(G.m.y+G.k.y)/2},nightA=1e9,nightB=1e9,winT=1e9;
const K=[[0,G.d.x,G.d.y,3.2],[at('L1','Dönerbude')+.2,G.d.x,G.d.y,4.4],[at('L1','Strandbar')-.5,G.d.x,G.d.y,4.6],[at('L1','Strandbar')-.1,G.s.x-50,G.s.y,3.4],[L.L1.end+.5,G.s.x-40,G.s.y,3.7],
 [at('L2','Hotel')-.1,G.bau[0].x,G.bau[0].y,3.4],[at('L2','Anlegestelle')-.4,G.bau[0].x+6,G.bau[0].y,3.7],[at('L2','Anlegestelle')+.3,G.bau[1].x,G.bau[1].y,3.0],[L.L2.end+.3,G.bau[1].x,G.bau[1].y,3.2],
 [at('L3','Inseln'),MID.x,MID.y,G.a.z*1.45],[dur,MID.x,MID.y,G.a.z*1.6]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],b2=K[Math.min(j+1,K.length-1)];let k=b2[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(b2[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(b2[1]-a[1])*k,a[2]+(b2[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(b2[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
const shot=async(t,f)=>{const p=(t>=nightA&&t<nightB)?night:(t>=winT?dayPL:day);const c=cam(t);
 for(const q of new Set([day,night,dayPL]))await q.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);
 for(const q of new Set([day,night,dayPL]))await q.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}
else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
