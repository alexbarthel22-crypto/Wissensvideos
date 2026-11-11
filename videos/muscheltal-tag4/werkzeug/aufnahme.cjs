// Homepage-Aufnahme Tag 4 (11.11.): erste Hütte → ganze Inselwelt, Gebäude-Montage, Bäckerei (Verlosung), Tierheim, Villa, Anlegestelle (Yacht), Muschelplatz, Nachbarn
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}_-]/gu,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-11T14:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-11T14:11:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important}'});await p.evaluate(()=>cancelAnimationFrame(fly));
await p.evaluate(()=>{petsStep();let sd=11;const R=()=>(sd=(sd*16807)%2147483647)/2147483647;
 for(const a of PETS.list){const opts=[[1,0],[-1,0],[0,1],[0,-1]].filter(([dk,dm])=>rValid(a.v,a.k+dk,a.m+dm));if(!opts.length)continue;const [dk,dm]=opts[(R()*opts.length)|0];
  const [x0,y0]=rNode(a.v,a.k,a.m),[x1,y1]=rNode(a.v,a.k+dk,a.m+dm),t=R();a.x=x0+(x1-x0)*t;a.y=y0+(y1-y0)*t;a.pause=R()*3;}});
const G=await p.evaluate(()=>{const a=fitAll(),m=fitMain();const g=n=>{const x=GEB.find(q=>q.typ===n);return{x:x.cx,y:x.cy}};const f=n=>{const q=PEOPLE.find(q=>q.name.replace('@','')===n);return{x:q.p.x,y:q.p.y}};
 const an=f('anton.van11'),la=f('laura.ngynn');const last=PEOPLE.filter(q=>q.p&&q.isl===ISL[1]).sort((a,b)=>b.nr-a.nr)[0];window.__LAST=last;
 const geb=GEB.filter(g=>g.v===MAIN),bau=BAU.filter(b=>b.v===MAIN),st=.26/Math.max(1,geb.length+bau.length+1);geb.forEach((g,i)=>g.at=.73+st*(i+1));bau.forEach((b,i)=>b.at=.73+st*(geb.length+i+1));
 return{N,a,m,last:{x:last.p.x,y:last.p.y,nr:last.nr},h1:f('sophia_e065'),d:g('doener'),s:g('strandbar'),ac:g('acai'),w:g('werkstatt'),v:g('villa'),b:g('baeckerei'),th:{x:BAU[2].cx,y:BAU[2].cy},an:{x:BAU[1].cx,y:BAU[1].cy},nb:{x:(an.x+la.x)/2,y:(an.y+la.y)/2}};});
const hop=(w,o,z)=>{const t=at('L3',w);return [[t-.25,o.x,o.y+8,z],[t+.6,o.x,o.y+8,z*1.04]];};
const JE=at('L1','jetzt'),GE=JE+1.7,KE=GE+1.2,HZ=6.2,HY=G.last.y+140/(HZ*2.6667);
const K=[[0,G.h1.x,G.h1.y-14,3.4],[JE-.1,G.h1.x,G.h1.y-14,3.0],[GE,G.m.x,G.m.y,G.m.z*1.05],[KE+.3,G.a.x,G.a.y,G.a.z*1.15],
 [L.L2.end,G.a.x,G.a.y,G.a.z*1.2],[L.L2b.start,G.last.x,HY,HZ],[L.L2b.end+.2,G.last.x,HY,HZ],
 ...hop('Dönerbude',G.d,3.6),...hop('Strandbar',G.s,3.2),...hop('Açaí-Stand',G.ac,3.6),...hop('Moped-Werkstatt',G.w,3.6),...hop('Strandvilla',G.v,3.4),[L.L3.end+.2,G.v.x,G.v.y+8,3.0],
 [L.L4.start+.3,G.b.x,G.b.y-10,4.2],[L.L7.end,G.b.x,G.b.y-10,4.6],
 [L.L8.start,G.th.x,G.th.y,3.0],[at('L8','Tierheim')-.4,G.th.x,G.th.y,3.4],[at('L8','Emilia')-.4,G.v.x,G.v.y-6,3.6],[L.L8.end,G.v.x,G.v.y-6,3.9],
 [L.L9.start+.3,G.v.x-120,G.v.y-30,2.6],[L.L9.end,G.v.x-130,G.v.y-30,2.8],
 [L.L10.start+.3,0,40,2.2],[L.L10.end,30,20,2.6],
 [L.L11.start+.2,G.nb.x+4,G.nb.y+22,4.4],[L.L11.end+.3,G.nb.x+4,G.nb.y+22,4.6],[dur,G.a.x,G.a.y,G.a.z*1.1]];
console.error(JSON.stringify({last:G.last,HZ:6.2}));
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
const ST=t=>{const e=(x)=>x<0?0:x>1?1:x;let gk=null,gv=0,lim=G.N,flt=0,nm=0;
 if(t<JE){gk=0;gv=1;lim=1;flt=1;}else if(t<GE){const k=e((t-JE)/(GE-JE));gk=k;gv=1;lim=1+Math.round(499*Math.min(1,k/.72)**2);flt=1-e(k*3);}
 else if(t<KE){const k=e((t-GE)/(KE-GE));lim=500+Math.round((G.N-500)*k*k);}
 if(t>=L.L2b.start-.5&&t<L.L2b.end+.5){lim=t<at('L2b','Folg')+.15?G.last.nr-1:G.last.nr;nm=1;}return [gk,gv,lim,flt,nm];};
const shot=async(t,f)=>{const c=cam(t),z=ST(t);await p.evaluate(([c,z])=>{const [gk,gv,lim,flt,nm]=z;GROWK=gk;GROWV=gv?MAIN:null;growing=gk!=null;limit=lim;
 const H1=PEOPLE.find(q=>q.nr===1);if(H1){H1.orig=H1.orig||H1.name;H1.name=lim===1?'\u200b':H1.orig;}window.__LAST.name=nm?'@dein_name':(window.__LAST.orig||(window.__LAST.orig=window.__LAST.name));if(!nm&&window.__LAST.orig)window.__LAST.name=window.__LAST.orig;
 document.getElementById('map').style.filter=flt?`grayscale(${.85*flt}) brightness(${1-.25*flt}) contrast(${1-.1*flt})`:'';cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},[c,z]);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
