// Story-Aufnahme: Tiermassen auf dem Muschelplatz, am Ende Baustelle Tierheim Pfotenkuss; Basis Tag 3: Streuner, Tierheim, Açaí, Werkstatt, Pool, Villa, Kokos-Tiere
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> [test-zeiten,komma]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));
const L={};for(const l of T.lines)L[l.id]=l;const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^a-z0-9äöüß-]/g,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const mk=async zeit=>{const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
 await p.clock.install({time:new Date('2026-11-10T13:10:00+01:00')});await p.goto('file://'+site+'?zeit='+zeit+'&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-10T13:11:00+01:00'));
 await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});await p.evaluate(()=>cancelAnimationFrame(fly));
 // Hunderte Streuner auf dem Muschelplatz vor dem Palast + Schlange zum Tierheim
 await p.evaluate(()=>{let sd=7;const R=()=>(sd=(sd*16807)%2147483647)/2147483647;const base=PETS.list.slice(),C=[];
  for(let r=0;r<1600;r++){const a=Object.assign({},base[r%base.length]);let x,y;if(r<310){const ang=R()*6.283,d=Math.sqrt(R());x=Math.cos(ang)*d*62;y=78+Math.sin(ang)*d*17;}else if(r<380){x=(R()-.5)*10;y=98+R()*60;}else if(r<640){const sd2=R()<.5?-1:1;x=sd2*(52+R()*58);y=50+R()*70;}else if(r<1100){const sd2=R()<.5?-1:1;x=sd2*(10+R()*95);y=86+R()*44;}else if(r<1220){x=(R()-.5)*56;y=38+R()*18;}else if(r<1340){x=-35+R()*85;y=90+R()*9;}else if(r<1420){x=(R()-.5)*8;y=98+R()*42;}else{x=6+R()*44;y=100+R()*40;}
   a.x=x;a.y=y;a.pause=1e9;a.wp=null;a.sit=R()<.4?1:0;a.dir=R()<.5?-1:1;a.view=['side','front','side','back'][(R()*4)|0];a.vert=a.view!=='side';a.i=1000+r;C.push(a);}
  C.sort((a,b)=>a.y-b.y);PETS.list.push(...C);});
 return p;};
const day=await mk('tag');
const G=await day.evaluate(()=>{const a=fitAll(),m=fitMain();const g=n=>{const x=GEB.find(q=>q.typ===n);return{x:x.cx,y:x.cy}};const lu=PEOPLE.find(q=>q.name.replace('@','')==='luisedbr.11');
 const P=PETS.list.filter(q=>q.v.i===0);let best=null,bn=0;for(const c of P){const n=P.filter(q=>Math.hypot(q.x-c.x,q.y-c.y)<55).length;if(n>bn){bn=n;best=c;}}
 const PK=PETS.list.filter(q=>q.v.i===1);let bk=null,bkn=0;for(const c of PK){const n=PK.filter(q=>Math.hypot(q.x-c.x,q.y-c.y)<60).length;if(n>bkn){bkn=n;bk=c;}}
 return{a,m,pt:{x:best.x,y:best.y},pk:{x:bk.x,y:bk.y},th:{x:BAU[2].cx,y:BAU[2].cy},ac:g('acai'),wk:g('werkstatt'),v:g('villa'),lu:{x:lu.p.x,y:lu.p.y},po:(()=>{const q=poolSpot(lu);return q?{x:q[0],y:q[1]}:{x:lu.p.x+12,y:lu.p.y}})()};});
console.error(JSON.stringify(G));
const PO=G.po,PZ=6.4,POY=PO.y+200/(PZ*2.6667);
const K=[[0,0,80,2.8],[5,0,78,4.4],[9.0,-4,80,5.5],[11.0,-40,160,3.4],[dur,-40,168,4.2]];





const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],b2=K[Math.min(j+1,K.length-1)];let k=b2[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(b2[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(b2[1]-a[1])*k,a[2]+(b2[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(b2[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
const shot=async(t,f)=>{const p=day,c=cam(t);await p.evaluate(c=>{cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},c);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}
else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
