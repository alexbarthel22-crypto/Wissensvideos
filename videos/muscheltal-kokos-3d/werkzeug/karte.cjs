// Muschel-Tal-Karte (Homepage) für das Ende: Kokos-Küste -> alle Inseln, Echtzeit. node karte.cjs <site/index.html> <out> <sekunden>
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,out,durS]=process.argv.slice(2);const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-09T13:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-09T13:11:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});
const G=await p.evaluate(()=>{cancelAnimationFrame(fly);const a=fitAll(),k=ISL[1];return{a,k:{x:k.x,y:k.y}};});
fs.mkdirSync(out,{recursive:true});
for(let i=0;i<N;i++){const t=i/30,k0=Math.min(1,t/dur),k=k0<.5?2*k0*k0:1-Math.pow(-2*k0+2,2)/2;
 await p.evaluate(([G,k])=>{cam.x=G.k.x+(G.a.x-G.k.x)*k;cam.y=G.k.y+(G.a.y-G.k.y)*k;cam.z=Math.exp(Math.log(1.6)+(Math.log(G.a.z*1.12)-Math.log(1.6))*k);draw();},[G,k]);
 await p.clock.runFor(33.333);await p.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();console.log('ok',N);})();
