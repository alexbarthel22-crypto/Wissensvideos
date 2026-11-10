// Story-Aufnahme (10.11.): zwei Nachbar-Hütten (@anton.van11 + @laura.ngynn), langsamer Zoom
// node aufnahme.cjs <site/index.html> <out> <dauer> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,out,durS,test]=process.argv.slice(2);const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-10T16:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-10T16:11:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});await p.evaluate(()=>cancelAnimationFrame(fly));
const G=await p.evaluate(()=>{const f=n=>PEOPLE.find(q=>q.name.replace('@','')===n).p;const a=f('anton.van11'),l=f('laura.ngynn');return{x:(a.x+l.x)/2,y:(a.y+l.y)/2};});
const K=[[0,G.x,G.y-20,2.6],[dur*.55,G.x+4,G.y-8,4.2],[dur,G.x+4,G.y-8,4.8]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)];};
const shot=async(t,f)=>{const c=cam(t);await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
