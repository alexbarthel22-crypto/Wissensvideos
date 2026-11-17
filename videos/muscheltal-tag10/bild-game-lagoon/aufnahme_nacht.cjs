const {chromium}=require('playwright');(async()=>{const [site,out,dy,z]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-17T21:30:00+01:00')});await p.goto('file://'+site+'?zeit=nacht&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-17T21:31:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}'});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));
const f=async()=>p.evaluate(([dy,z])=>{cam.x=KGAME.cx;cam.y=KGAME.cy+(+dy);cam.z=+z;draw();},[dy,z]);await f();await p.clock.runFor(200);await f();
await p.screenshot({path:out,type:'png'});await b.close();})();
