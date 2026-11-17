// Zwei Nachbar-Hütten mit „@du“ und „@deine_bestie“ (Homepage-Aufnahme)
const {chromium}=require('playwright');(async()=>{const [site,out]=process.argv.slice(2);const b=await chromium.launch();const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-17T16:20:00+01:00')});await p.goto('file://'+site+'?zeit=untergang&p=.55&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-17T16:21:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}'});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));
const c=await p.evaluate(()=>{const a=PEOPLE.find(x=>x.name==='@sophia_e065'),b=PEOPLE.find(x=>x.name==='@lxnn9xm');a.name='@deine_bestie';b.name='@du';return {x:(a.p.x+b.p.x)/2,y:(a.p.y+b.p.y)/2};});
const f=async()=>p.evaluate(c=>{cam.x=c.x;cam.y=c.y+8;cam.z=6.0;JOG.list=[];if(typeof WALKERS!=='undefined')WALKERS.length=0;;draw();},c);await f();await p.clock.runFor(200);await f();
await p.screenshot({path:out,type:'png'});await b.close();})();
