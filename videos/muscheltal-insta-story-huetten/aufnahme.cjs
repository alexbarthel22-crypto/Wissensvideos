const {chromium}=require('playwright');const path=require('path');const fs=require('fs');
(async()=>{const b=await chromium.launch();const E='file://'+path.resolve('site2')+'/index.html';
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-08T13:10:00+01:00')});await p.goto(E+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);
await p.addStyleTag({content:'body *{visibility:hidden!important} canvas#map{visibility:visible!important}'});
await p.evaluate(()=>cancelAnimationFrame(fly));
const K=[[0,0,-30,2.7],[3.5,-60,-130,3.6],[10,-170,-210,4.1]];const out='ig7/frames';fs.rmSync(out,{recursive:true,force:true});fs.mkdirSync(out);
for(let i=0;i<300;i++){const t=i/30;
 await p.evaluate(([t,K])=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],b2=K[Math.min(j+1,K.length-1)];let k=b2[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(b2[0]-a[0]))):1;k=k<.5?2*k*k:1-Math.pow(-2*k+2,2)/2;
  cam.x=a[1]+(b2[1]-a[1])*k;cam.y=a[2]+(b2[2]-a[2])*k;cam.z=Math.exp(Math.log(a[3])+(Math.log(b2[3])-Math.log(a[3]))*k);draw();},[t,K]);
 await p.clock.runFor(33.333);await p.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();})();
