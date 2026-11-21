// Golden Pearl bei Nacht (21.11.): langsamer Flug von der Kokos-Küste zum beleuchteten Golden Pearl
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> <t0> <t1> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,t0S,t1S,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-21T22:30:00+01:00')});await p.goto('file://'+site+'?zeit=nacht&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-21T22:31:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}'});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));
const G=await p.evaluate(()=>({x:GP.X,y:GP.Y,sx:GP.sx,sy:GP.sy,W:GP.W}));
const K=[[0,G.x-40,G.y-20,1.25],[L.L1.end,G.x,G.y-35,1.6],[L.L2.end,G.x+30,G.y-50,2.1],[L.L3.end,G.x-30,G.y-50,2.1],[dur,G.x,G.y-40,1.4]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)];};
let last=0;const shot=async(t,f)=>{const c=cam(t);const ms=Math.round((t-last)*1000);if(ms>0)await p.clock.runFor(ms);last=t;await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else{const i0=Math.round(+t0S*30),i1=Math.min(N,Math.round(+t1S*30));for(let i=i0;i<i1;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);}
await b.close();console.log('ok',N);})();
