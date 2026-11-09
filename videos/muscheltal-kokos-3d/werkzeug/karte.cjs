// Homepage-Aufnahme fürs Ende (Echtzeit): Hotel-Baustelle -> Anlegestelle -> alle Inseln.
// node karte.cjs <site/index.html> <timings.json> <out> <startzeit> <endzeit>
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,t0s,t1s]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const t0=+t0s,t1=+t1s,N=Math.round((t1-t0)*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-09T13:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-09T13:11:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});
const G=await p.evaluate(()=>{cancelAnimationFrame(fly);const a=fitAll();return{a,bau:BAU.map(q=>({x:q.cx,y:q.cy}))};});
const K=[[t0,G.bau[0].x,G.bau[0].y,2.9],[at('L5','Hotel'),G.bau[0].x,G.bau[0].y,3.5],[at('L5','Anlegestelle')-.5,G.bau[0].x+8,G.bau[0].y,3.7],[at('L5','Anlegestelle')+.2,G.bau[1].x,G.bau[1].y,2.9],[L.L5.end+.3,G.bau[1].x,G.bau[1].y,3.2],
 [L.L6.start+.3,G.bau[1].x,G.bau[1].y,1.6],[L.L6.end,G.a.x,G.a.y,G.a.z*1.15],[t1,G.a.x,G.a.y,G.a.z*1.1]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],b2=K[Math.min(j+1,K.length-1)];let k=b2[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(b2[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(b2[1]-a[1])*k,a[2]+(b2[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(b2[3])-Math.log(a[3]))*k)];};
fs.mkdirSync(out,{recursive:true});
for(let i=0;i<N;i++){const c=cam(t0+i/30);await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);await p.clock.runFor(33.333);await p.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();console.log('ok',N);})();
