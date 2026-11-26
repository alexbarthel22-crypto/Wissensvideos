// Story 26.11.: Sunken Pearl im Sonnenuntergang → Fähre Seestern fährt los (Kamera folgt) → Hütten (Nachbarn) → Haupt-Insel
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> <t0> <t1> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,t0S,t1S,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const CSS='body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}';
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});await p.clock.install({time:new Date('2026-11-26T16:10:00+01:00')});
await p.goto('file://'+site+'?zeit=untergang&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-26T16:11:00+01:00'));
await p.addStyleTag({content:CSS});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));
const G=await p.evaluate(()=>({m:fitMain(),sp:[SPL.X,SPL.Y]}));const m=G.m;
const TB=L.L2.start-.45, TE=L.L3.start-.05;
const K=[[0,G.sp[0],G.sp[1]+10,3.4],[L.L1b.end+.2,G.sp[0],G.sp[1]+20,2.2],
 [TE,-60,110,3.0],[L.L3.end+.2,-60,110,3.9],[L.L4.start-.05,m.x,m.y,m.z*1.35],[dur,m.x,m.y,m.z*1.0]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)];};
let last=0,booted=false;
const adv=async t=>{const ms=Math.round((t-last)*1000);if(ms>0)await p.clock.runFor(ms);last=Math.max(last,t);};
const shot=async(t,f)=>{
 if(!booted&&t>=TB){await adv(TB);await p.evaluate(()=>{const g=STEGE.find(x=>x.th==='sunken'),h=STEGE.find(x=>x.th==='haupt');WK.x=stegKopf(g)[0];WK.y=stegKopf(g)[1];bootStart(g,h);});booted=true;}
 await adv(t);
 if(t>=TB&&t<TE){const q=await p.evaluate(()=>{bootSchritt(performance.now());return [BOOT.x,BOOT.y];});const u=Math.min(1,(t-TB)/.6),c0=cam(TB);
   await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},[c0[0]+(q[0]-c0[0])*u,c0[1]+(q[1]-c0[1])*u,2.2+0.4*u]);}
 else{if(booted&&t>=TE)await p.evaluate(()=>{try{bootSchritt(performance.now());}catch(e){}});const c=cam(t);await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);}
 await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else{const i0=Math.round(+t0S*30),i1=Math.min(N,Math.round(+t1S*30));for(let i=i0;i<i1;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);}
await b.close();console.log('ok',N);})();
