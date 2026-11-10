// Homepage-Aufnahme „Eure verrückteste Idee“ (10.11.): Muschelplatz (Red-Bull-Regen, Matcha-Brunnen), Dönerbude, Muschelplatz, Rauszoom
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^a-z0-9äöüß_-]/g,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-10T14:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-10T14:11:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});await p.evaluate(()=>cancelAnimationFrame(fly));
const G=await p.evaluate(()=>{const a=fitAll(),m=fitMain();const lu=PEOPLE.find(q=>q.name.replace('@','')==='luisedbr.11');const q=poolSpot(lu);return{a,m,po:q?{x:q[0],y:q[1]}:{x:lu.p.x+12,y:lu.p.y}};});
const PZ=6.4,POY=G.po.y+200/(PZ*2.6667);
const K=[[0,0,40,2.2],[L.L1.end,0,30,3.0],
 [L.L2.start-.3,0,45,3.3],[L.L2.end+.3,0,45,3.3],
 [L.L3.start+.2,-150,100,2.6],[L.L3.end,-60,140,3.0],
 [L.L4.start+.3,0,40,2.2],[L.L4.end,30,20,2.6],
 [L.L5.start+.3,G.m.x,G.m.y,G.m.z*1.3],[dur,G.a.x,G.a.y,G.a.z*1.1]];



const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
const shot=async(t,f)=>{const c=cam(t);await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
