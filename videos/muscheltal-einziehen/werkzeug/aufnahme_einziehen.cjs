// Hintergrund „Einziehen“-Video: Einwohnerliste (scrollend) + Karte (Zoom aus einer Hütte, Inseln)
// node aufnahme_einziehen.cjs <site-ordner> <timings.json> <out> <dauer>
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const A=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await A.clock.install({time:new Date('2026-11-17T14:10:00+01:00')});await A.goto('file://'+site+'/index.html?zeit=tag&wetter=sonne');await A.clock.runFor(7000);await A.clock.pauseAt(new Date('2026-11-17T14:11:00+01:00'));
await A.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}'});await A.evaluate(()=>resize());await A.evaluate(()=>cancelAnimationFrame(fly));
const G=await A.evaluate(()=>{const q=PEOPLE.find(x=>x.name==='@sophia_e065');const k=fitIsl(KOKV);return{h:{x:q.p.x,y:q.p.y},m:fitMain(),a:fitAll(),k}});console.error(JSON.stringify(G));
const B=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});await B.goto('file://'+site+'/einwohner.html');await B.waitForTimeout(1500);
const H=await B.evaluate(()=>document.body.scrollHeight);
const e=k=>k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2,lerp=(a,b,k)=>a+(b-a)*k,lz=(a,b,k)=>Math.exp(lerp(Math.log(a),Math.log(b),k));
const s2=L.L2.start-.2,s3=L.L3.start-.4,s4=L.L4.start-.2,s5=dur;
fs.mkdirSync(out,{recursive:true});
for(let i=0;i<N;i++){const t=i/30,f=`${out}/f${String(i).padStart(5,'0')}.jpg`;
 if(t<s2){const k=t/s2;await B.evaluate(y=>window.scrollTo(0,y),Math.round(300+(H*.55)*(k*k)));await B.screenshot({path:f,type:'jpeg',quality:90});continue;}
 if(t>=s3&&t<s4){const k=(t-s3)/(s4-s3);await B.evaluate(y=>window.scrollTo(0,y),Math.round(H-720-1500+1500*k));await B.screenshot({path:f,type:'jpeg',quality:90});continue;}
 let c;if(t<s3){const k=e(Math.min(1,(t-s2)/(s3-s2-.3)));c={x:lerp(G.h.x,G.m.x,k),y:lerp(G.h.y,G.m.y,k),z:lz(8,G.m.z*1.05,k)};}
 else if(t<s5){const k=e(Math.min(1,(t-s4)/(s5-s4)));c={x:lerp(G.m.x,G.a.x,k),y:lerp(G.m.y,G.a.y,k),z:lz(G.m.z,G.a.z*1.1,k)};}
 else{const k=e(Math.min(1,(t-s5)/(dur-s5)));c={x:lerp(G.a.x,G.k.x,k),y:lerp(G.a.y,G.k.y,k),z:lz(G.a.z*1.1,G.k.z*1.15,k)};}
 await A.evaluate(c=>{cam.x=c.x;cam.y=c.y;cam.z=c.z;draw();},c);await A.clock.runFor(33.333);await A.screenshot({path:f,type:'jpeg',quality:90});}
await b.close();console.log('ok',N);})();
