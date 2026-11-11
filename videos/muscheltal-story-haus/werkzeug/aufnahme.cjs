// Story-Aufnahme (11.11.): Fabiennes Bäckerei, langsamer Zoom, viele Tiere
// node aufnahme.cjs <site/index.html> <out> <dauer> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,out,durS,test]=process.argv.slice(2);const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-11T15:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-11T15:11:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}'});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));
const G=await p.evaluate(()=>{const g=GEB.find(q=>q.typ==='baeckerei');petsStep();let sd=11;const R=()=>(sd=(sd*16807)%2147483647)/2147483647;
 for(const a of PETS.list){const o=[[1,0],[-1,0],[0,1],[0,-1]].filter(([dk,dm])=>rValid(a.v,a.k+dk,a.m+dm));if(!o.length)continue;const [dk,dm]=o[(R()*o.length)|0];const [x0,y0]=rNode(a.v,a.k,a.m),[x1,y1]=rNode(a.v,a.k+dk,a.m+dm),t=R();a.x=x0+(x1-x0)*t;a.y=y0+(y1-y0)*t;a.pause=R()*3;}
 return{x:g.cx,y:g.cy};});
const K=[[0,G.x,G.y-2,3.4],[dur,G.x,G.y-6,4.2]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)];};
const shot=async(t,f)=>{const c=cam(t);await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
