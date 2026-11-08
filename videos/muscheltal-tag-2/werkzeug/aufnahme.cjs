// Homepage-Aufnahme für Muschel-Tal Tag 2: Kamerafahrt passend zu den Wortzeiten (timings.json)
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));
const L={};for(const l of T.lines)L[l.id]=l;const W=id=>(id2,w)=>{const x=L[id2].words.find(q=>q.display.toLowerCase().replace(/[^a-z0-9äöüß]/g,'').startsWith(w.toLowerCase()));return x?x.start:L[id2].start;};const at=W();
const dur=+process.argv[5]||T.duration+1.6,N=Math.round(dur*30);
const b=await chromium.launch();const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-08T13:10:00+01:00')});await p.goto('file://'+site);await p.clock.runFor(7000);
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});
const G=await p.evaluate(()=>{cancelAnimationFrame(fly);const m=fitMain(),a=fitAll(),k=ISL[1];const RV=(window.RESVS||[[[1,0],[-2,-1]]])[0];const [bk,bm]=RV[0];const pp=k.people.filter(q=>q.p).map(q=>q.p);pp.sort((u,v)=>u.x-v.x);const ka=pp[Math.floor(pp.length*.15)]||k,kb=pp[Math.floor(pp.length*.85)]||k;const MR=ISL[0].R;return{MR,m,a,k:{x:k.x,y:k.y,R:k.R},ka:{x:ka.x,y:ka.y},kb:{x:kb.x,y:kb.y},bp:{x:(5*bk+2.5)*S,y:(4*bm+2)*S*.9},bp2:{x:(5*RV[1][0]+2.5)*S,y:(4*RV[1][1]+2)*S*.9}};});
const zk=405/(2*(G.k.R+60));
// Schlüsselbilder [zeit, x, y, z]
const K=[[0,G.m.x,G.m.y,G.m.z*.82],[L.L2.end,G.m.x,G.m.y,G.m.z*1.08],
 [L.L3.start+.1,-G.MR*.6,-G.MR*.5,2.8],[L.L5.start-.2,G.MR*.6,-G.MR*.35,2.8],
 [at('L5','nächste')-.1,G.m.x,G.m.y,G.m.z*1.05],[at('L5','Kokos'),G.k.x,G.k.y,zk],[L.L6.start-.3,G.ka.x,G.ka.y,4.4],[L.L6.end+.4,G.kb.x,G.kb.y,4.6],
 [L.L7.start-.1,(G.k.x+G.m.x)/2,(G.k.y+G.m.y)/2,G.a.z*1.5],[L.L7.start+1.1,-G.MR*.6,G.MR*.45,2.7],[L.L7.end+.3,G.MR*.55,G.MR*.55,2.7],[at('L8','zwei'),G.bp.x,G.bp.y,2.6],[L.L9.start,G.bp.x+20,G.bp.y,2.8],[L.L10.end,G.bp2.x,G.bp2.y,2.6],
 [L.L11.start+.3,0,10,3.4],[L.L12b.end,0,0,4.0],
 [L.L13.start+.4,G.a.x,G.a.y,G.a.z*1.15],[dur,G.a.x,G.a.y,G.a.z*1.05]];
fs.mkdirSync(out,{recursive:true});
for(let i=0;i<N;i++){const t=i/30;
 await p.evaluate(([t,K])=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],b2=K[Math.min(j+1,K.length-1)];let k=b2[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(b2[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
  cam.x=a[1]+(b2[1]-a[1])*k;cam.y=a[2]+(b2[2]-a[2])*k;cam.z=Math.exp(Math.log(a[3])+(Math.log(b2[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8));draw();},[t,K]);
 await p.clock.runFor(33.333);await p.screenshot({path:`${out}/f${String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});}
await b.close();console.log('frames',N);})();
