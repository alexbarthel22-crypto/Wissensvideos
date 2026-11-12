// Homepage-Aufnahme Tag 5 (12.11.): Strandvilla (Opener), freie Hütte → @dein_name, Ocean Nails, Yacht White Pearl, Hotel-Baustelle, Muschelplatz, Nachbarn
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}_-]/gu,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
await p.clock.install({time:new Date('2026-11-12T14:10:00+01:00')});await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);await p.clock.pauseAt(new Date('2026-11-12T14:11:00+01:00'));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}'});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));
await p.evaluate(()=>{petsStep();let sd=11;const R=()=>(sd=(sd*16807)%2147483647)/2147483647;
 for(const a of PETS.list){const opts=[[1,0],[-1,0],[0,1],[0,-1]].filter(([dk,dm])=>rValid(a.v,a.k+dk,a.m+dm));if(!opts.length)continue;const [dk,dm]=opts[(R()*opts.length)|0];
  const [x0,y0]=rNode(a.v,a.k,a.m),[x1,y1]=rNode(a.v,a.k+dk,a.m+dm),t=R();a.x=x0+(x1-x0)*t;a.y=y0+(y1-y0)*t;a.pause=R()*3;}});
const G=await p.evaluate(()=>{const a=fitAll(),m=fitMain();const g=n=>{const x=GEB.find(q=>q.typ===n);return{x:x.cx,y:x.cy}};const f=n=>{const q=PEOPLE.find(q=>q.name.replace('@','')===n);return{x:q.p.x,y:q.p.y}};
 const an=f('melie_js'),la=f('lisann.lmp');const geb=GEB.filter(g=>g.v===MAIN),bau=BAU.filter(b=>b.v===MAIN),st=.26/Math.max(1,geb.length+bau.length+1);geb.forEach((g,i)=>g.at=.73+st*(i+1));bau.forEach((b,i)=>b.at=.73+st*(geb.length+i+1));const last=PEOPLE.filter(q=>q.p&&q.isl===ISL[1]).sort((a,b)=>b.nr-a.nr)[0];window.__LAST=last;const y={x:YACHT.cx,y:YACHT.cy};
 return{N,a,m,last:{x:last.p.x,y:last.p.y,nr:last.nr},v:g('villa'),na:g('nagel'),ya:{x:y.x!=null?y.x:y[0],y:y.y!=null?y.y:y[1]},ho:{x:BAU[0].cx,y:BAU[0].cy},nb:{x:(an.x+la.x)/2,y:(an.y+la.y)/2}};});
console.error(JSON.stringify(G));
const HW=['verschenke','VILLA'].map(w=>at('L2v',w)).concat([L.L2v.start]),AL=L.L2v.end+.2,AS=L.L2v.start-.1,HZ=6.2,HY=G.last.y+140/(HZ*2.6667);
const GS=at('L1','besiedeln')-.1,GE=L.L1b.end+.6;
const K=[[0,G.m.x,G.m.y-10,G.m.z*1.0],[GS,G.m.x,G.m.y-10,G.m.z*1.15],[GE,G.a.x,G.a.y,G.a.z*1.2],
 [L.L2v.start-.15,G.v.x+20,G.v.y-10,4.0],[L.L2v.end,G.v.x+20,G.v.y-10,4.4],[L.L2vb.end,G.v.x+10,G.v.y-14,3.4],
 [L.L3h.start,G.last.x,HY,HZ],[L.L3h.end+.2,G.last.x,HY,HZ],
 [L.L4n.start+.2,G.na.x,G.na.y+10,3.4],[L.L4n.end,G.na.x,G.na.y+8,3.7],
 [L.L5.start+.3,G.ya.x,G.ya.y-10,4.0],[L.L5.end,G.ya.x,G.ya.y-10,4.4],
 [L.L6.start+.3,G.ho.x,G.ho.y-6,3.4],[L.L6.end,G.ho.x,G.ho.y-6,3.7],[L.L7.start+.3,G.m.x,G.m.y,G.m.z*1.2],[L.L7.end,G.m.x,G.m.y,G.m.z*1.3],
 [L.L8.start+.3,0,40,2.2],[L.L8.end,30,20,2.6],
 [L.L9.start+.2,G.nb.x,G.nb.y-2,4.5],[L.L9.end+.3,G.nb.x,G.nb.y-2,4.5],[dur,G.a.x,G.a.y,G.a.z*1.1]];


const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
const ST=t=>{const e=x=>x<0?0:x>1?1:x;let gk=null,gv=0,lim=G.N,flt=0,nm=0;
 if(t<GS){gk=0;gv=1;lim=1;}else if(t<GE){const k=e((t-GS)/(GE-GS));gk=Math.min(1,k*1.3);gv=k<.75?1:0;lim=1+Math.round((G.N-1)*Math.min(1,k/.8)**2);if(!gv)gk=null;}
 if(t>=L.L3h.start-.5&&t<L.L3h.end+.5){lim=t<at('L3h','folgt')+.15?G.last.nr-1:G.last.nr;nm=1;}return [gk,gv,lim,flt,nm];};
const shot=async(t,f)=>{const c=cam(t),z=ST(t);if(t>AS&&t<AL){let b=0;for(const w of HW)b+=Math.exp(-(((t-w-.05)/.09)**2));c[2]*=1+.12*b;const sh=Math.min(1,b);c[0]+=Math.sin(t*90)*6*sh/c[2];c[1]+=Math.cos(t*77)*6*sh/c[2];}await p.evaluate(([c,z])=>{const [gk,gv,lim,flt,nm]=z;GROWK=gk;GROWV=gv?MAIN:null;growing=gk!=null;limit=lim;
 const GB=GEB.find(q=>q.typ==='baeckerei');if(GB){GB.tl0=GB.tl0||GB.tl;GB.tr0=GB.tr0||GB.tr;GB.tl=z[6]?GB.tl0.slice(0,1):GB.tl0;GB.tr=z[6]?[[GB.tr0[0][0]]]:GB.tr0;}const LJ=PEOPLE.find(q=>q.name.replace('@','')==='lona.js');if(LJ){LJ.orig=LJ.orig||LJ.name;LJ.name=z[6]?'\u200b':LJ.orig;}window.__LAST.name=nm?'@dein_name':(window.__LAST.orig||(window.__LAST.orig=window.__LAST.name));if(!nm&&window.__LAST.orig)window.__LAST.name=window.__LAST.orig;
 document.getElementById('map').style.filter=flt?`grayscale(${.85*flt}) brightness(${1-.25*flt}) contrast(${1-.1*flt})`:'';window.NOLAB=z[5];cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},[c,z.concat([0,0])]);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
