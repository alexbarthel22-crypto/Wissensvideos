const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:405,height:720},deviceScaleFactor:2.6667,isMobile:true,hasTouch:true});
const p=await ctx.newPage();await p.clock.install({time:new Date('2026-11-07T13:10:00+01:00')});
await p.goto('file:///home/user/TikTok-/muscheltal/site/index.html');await p.clock.runFor(7000);
await p.addStyleTag({content:'.ctrl,.quick,.down,#hint{display:none!important}'});
const N=300, out=process.argv[2];
await p.evaluate(()=>{window.__A=fitMain();const f=fitAll();window.__B={x:f.x,y:f.y,z:f.z*.9};cancelAnimationFrame(fly);});
for(let i=0;i<N;i++){const t=i/30;
  await p.evaluate((t)=>{const A=__A,B=__B,k=Math.max(0,Math.min(1,(t-1.2)/4.6)),e=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
    cam.x=A.x+(B.x-A.x)*e;cam.y=A.y+(B.y-A.y)*e+Math.sin(t*.5)*6/cam.z;cam.z=Math.exp(Math.log(A.z)+(Math.log(B.z)-Math.log(A.z))*e)*(1+.015*Math.sin(t*.7));draw();},t);
  await p.clock.runFor(33);await p.screenshot({path:`${out}/f${String(i).padStart(4,'0')}.png`});}
await b.close();})()
