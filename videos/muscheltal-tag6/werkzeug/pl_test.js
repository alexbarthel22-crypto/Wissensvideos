const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-09T13:10:00+01:00')});await p.goto('file://'+process.argv[2]+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});await p.evaluate(()=>cancelAnimationFrame(fly));
for(const [z,f] of [[6,'a'],[4,'b']]){await p.evaluate(z=>{cam.x=6;cam.y=36*PAL_S+4;cam.z=z;draw();},z);await p.clock.runFor(100);await p.evaluate(z=>{cam.x=6;cam.y=36*PAL_S+4;cam.z=z;draw();},z);await p.screenshot({path:process.argv[3]+f+'.jpg'});}
await b.close();})();
