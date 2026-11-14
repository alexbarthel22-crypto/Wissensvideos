// Homepage-Aufnahme Tag 7 (14.11.): Yacht, Bäckerei, Kokos-Läden, LIVE-Insel, Hütte – früher Tag 6: Hook über der Haupt-Insel, Villa-Verlosung (@sklmq3), Rettungsschwimmerin, Porto Pizza, Boba Beach, Kiosk Kunterbunt, Meerkauf, Bäckerei, Tierheim
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
const G=await p.evaluate(()=>{const a=fitAll(),m=fitMain();const g=n=>{const x=GEB.find(q=>q.typ===n);return{x:x.cx,y:x.cy}};
 return{N,a,m,ba:g('baeckerei'),ya:{x:YACHT.cx!=null?YACHT.cx:YACHT[0],y:YACHT.cy!=null?YACHT.cy:YACHT[1]},k:{x:KOKV.x,y:KOKV.y,r:KOKV.R||KOKV.r||300},kb:{x:KBAR.cx,y:KBAR.cy},kd:{x:KBAD.cx,y:KBAD.cy},km:{x:KMODE.cx,y:KMODE.cy},lv:{x:LV.x,y:LV.y,r:LV.r},
  last:(()=>{const q=PEOPLE.filter(q=>q.p&&q.isl===ISL[1]&&q.name.length>=12).sort((a,b)=>b.nr-a.nr)[0];window.__LAST=q;q.orig=q.name;return{x:q.p.x,y:q.p.y,nr:q.nr}})()};});
console.error(JSON.stringify(G));
const HZ=6.2,HY=G.last.y+40/(HZ*2.6667),KZ=1080/(2.6667*2.3*G.k.r),LZ=1080/(2.6667*2.4*G.lv.r);
const GS=at('L1','Follower')-.1,GE=L.L1.end+.5;
const K=[[0,G.m.x+40,G.m.y-50,G.m.z*.8],[L.L1.end,G.m.x,G.m.y-10,G.m.z*1.1],[L.L1b.start+.1,G.m.x,G.m.y-10,G.m.z*1.6],[L.L1b.end,G.m.x,G.m.y,G.m.z*1.15],
 [L.L2.start-.1,G.ba.x,G.ba.y-4,4.6],[L.L2w.start-.3,G.ba.x,G.ba.y-4,4.8],[L.L2w.end+.2,G.ba.x,G.ba.y-6,6.2],[L.L2w.end+.8,G.ba.x,G.ba.y-6,6.4],
 [L.L3.start+.2,G.k.x,G.k.y,KZ],[L.L3x.start-.15,G.kb.x,G.kb.y-6,4.0],[L.L3y.start-.4,G.kb.x,G.kb.y-6,4.4],[L.L3y.start-.05,G.kd.x,G.kd.y-6,4.0],[L.L3z.start-.4,G.kd.x,G.kd.y-6,4.4],[L.L3z.start-.05,G.km.x,G.km.y-6,4.0],[L.L4.start-.7,G.km.x,G.km.y-6,4.6],
 [L.L4.start-.1,G.ya.x,G.ya.y+2,4.0],[L.L4b.end+.3,G.ya.x,G.ya.y+2,4.6],
 [L.L5.start,G.lv.x,G.lv.y+G.lv.r*.15,LZ],[L.L5.end+.3,G.lv.x,G.lv.y+G.lv.r*.1,LZ*1.25],
 [L.L6.start,G.last.x,HY,HZ*.8],[at('L6','Hütte'),G.last.x,HY,HZ],[dur,G.last.x,HY,HZ]];
const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
const ST=t=>{const e=x=>x<0?0:x>1?1:x;let gk=null,gv=0,lim=G.N;if(t<GS){gk=0;gv=1;lim=1;}else if(t<GE){const k=e((t-GS)/(GE-GS));gk=Math.min(1,k*1.3);gv=k<.75?1:0;lim=1+Math.round((G.N-1)*Math.min(1,k/.8)**2);if(!gv)gk=null;}const h=t>=L.L6.start-.5;return [gk,gv,lim,0,h?1:0,t<L.L1b.end?1:0];};
const shot=async(t,f)=>{const c=cam(t),z=ST(t);if(t>=L.L2w.start-.3&&!globalThis.JULI){globalThis.JULI=1;await p.evaluate(()=>{const q=PEOPLE.find(q=>q.name==='@julicrzy2000');if(q){q.ort='Bäckerei';q.beruf='Team';}});}await p.evaluate(([c,z])=>{const [gk,gv,lim,flt,nm]=z;GROWK=gk;GROWV=gv?MAIN:null;growing=gk!=null;limit=lim;
 const GB=GEB.find(q=>q.typ==='baeckerei');if(GB){GB.tl0=GB.tl0||GB.tl;GB.tr0=GB.tr0||GB.tr;GB.tl=z[6]?GB.tl0.slice(0,1):GB.tl0;GB.tr=z[6]?[[GB.tr0[0][0]]]:GB.tr0;}const LJ=PEOPLE.find(q=>q.name.replace('@','')==='lona.js');if(LJ){LJ.orig=LJ.orig||LJ.name;LJ.name=z[6]?'\u200b':LJ.orig;}window.__LAST.name=z[4]?'@dein_name':window.__LAST.orig;document.getElementById('map').style.filter=flt?`grayscale(${.85*flt}) brightness(${1-.25*flt}) contrast(${1-.1*flt})`:'';window.NOLAB=z[5];cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},[c,z.concat([0,0])]);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else for(let i=0;i<N;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);
await b.close();console.log('ok',N);})();
