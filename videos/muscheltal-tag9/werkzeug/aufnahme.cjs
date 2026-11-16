// Homepage-Aufnahme Tag 9 (16.11.): Club KOK(O)S nachts, CocoCare, Porto Pizza, Kokos-Bad, Tierheim – früher Tag 7 (14.11.): Yacht, Bäckerei, Kokos-Läden, LIVE-Insel, Hütte – früher Tag 6: Hook über der Haupt-Insel, Villa-Verlosung (@sklmq3), Rettungsschwimmerin, Porto Pizza, Boba Beach, Kiosk Kunterbunt, Meerkauf, Bäckerei, Tierheim
// node aufnahme.cjs <site/index.html> <timings.json> <out> <dauer> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,timf,out,durS,mode,t0S,t1S,test]=process.argv.slice(2);const NACHT=mode==='nacht';const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;
const at=(id,w)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}_-]/gu,'').startsWith(w.toLowerCase()));return x?x.start:L[id].start;};
const dur=+durS,N=Math.round(dur*30);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:2.6667});
const HH=NACHT?'23':'14';await p.clock.install({time:new Date(`2026-11-16T${HH}:10:00+01:00`)});await p.goto('file://'+site+(NACHT?'?zeit=nacht&wetter=sonne':'?zeit=tag&wetter=sonne'));await p.clock.runFor(7000);await p.clock.pauseAt(new Date(`2026-11-16T${HH}:11:00+01:00`));
await p.addStyleTag({content:'body *{visibility:hidden!important}canvas#map{visibility:visible!important;position:fixed!important;left:0!important;top:0!important;width:100vw!important;height:100vh!important;z-index:9}'});await p.evaluate(()=>resize());await p.evaluate(()=>cancelAnimationFrame(fly));
await p.evaluate(()=>{petsStep();let sd=11;const R=()=>(sd=(sd*16807)%2147483647)/2147483647;
 for(const a of PETS.list){const opts=[[1,0],[-1,0],[0,1],[0,-1]].filter(([dk,dm])=>rValid(a.v,a.k+dk,a.m+dm));if(!opts.length)continue;const [dk,dm]=opts[(R()*opts.length)|0];
  const [x0,y0]=rNode(a.v,a.k,a.m),[x1,y1]=rNode(a.v,a.k+dk,a.m+dm),t=R();a.x=x0+(x1-x0)*t;a.y=y0+(y1-y0)*t;a.pause=R()*3;}});
const G=await p.evaluate(()=>{const a=fitAll(),m=fitMain();
 const ti=BAU.find(b=>/tierheim/i.test(JSON.stringify(b.name||b.n||b.titel||'')))||BAU.find(b=>b.ziel===800);
 return{N,a,m,ti:{x:ti.cx,y:ti.cy},po:{x:KI.x+KI.po,y:KI.cy},cl:{x:KCLUB.cx,y:KCLUB.cy},dr:{x:KDROG.cx,y:KDROG.cy},bd:{x:KBAD.cx,y:KBAD.cy},lv:{x:LV.x,y:LV.y,r:LV.r}};});
console.error(JSON.stringify(G));
const LZ=1080/(2.6667*2.4*G.lv.r);const K=[[0,G.cl.x,G.cl.y+32,4.0],[L.L1.end+.2,G.cl.x,G.cl.y+32,3.7],
 [L.L1b.start+.1,G.m.x,G.m.y-10,G.m.z*1.5],[L.L1b.end,G.m.x,G.m.y,G.m.z*1.15],
 [L.L2.start,G.cl.x,G.cl.y-22,3.3],[L.L2.end+.2,G.cl.x,G.cl.y-22,4.0],
 [L.L2c.start-.15,G.dr.x,G.dr.y-24,4.0],[L.L2c.end+.3,G.dr.x,G.dr.y-24,4.3],
 [L.L3.start+.2,G.m.x,G.m.y,G.m.z*1.2],[L.L3a.start-.05,G.po.x,G.po.y-9,4.6],[L.L3aw.end+.6,G.po.x,G.po.y-9,5.0],
 [L.L3b.start-.05,G.bd.x,G.bd.y-8,4.0],[L.L3bw.end+.6,G.bd.x,G.bd.y-8,4.4],
 [L.L4.start+.1,G.ti.x-20,G.ti.y-30,3.4],[L.L4b.start,G.ti.x,G.ti.y-14,3.2],[L.L4b.end+.3,G.ti.x,G.ti.y-14,3.6],
 [L.L6.start+.1,0,-55,2.0],[L.L6bw.end+.6,0,-55,2.3],
 [L.L4c.start+.3,G.lv.x,G.lv.y+G.lv.r*.62,LZ*.95],[L.L4c.end+.3,G.lv.x,G.lv.y+G.lv.r*.62,LZ],
 [L.L5.start+.3,G.cl.x,G.cl.y-34,3.0],[dur,G.cl.x,G.cl.y-34,3.2]];

const cam=t=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],c=K[Math.min(j+1,K.length-1)];let k=c[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(c[0]-a[0]))):1;k=k<.5?4*k*k*k:1-Math.pow(-2*k+2,3)/2;
 return [a[1]+(c[1]-a[1])*k,a[2]+(c[2]-a[2])*k,Math.exp(Math.log(a[3])+(Math.log(c[3])-Math.log(a[3]))*k)*(1+.012*Math.sin(t*.8))];};
const ST=t=>[null,0,G.N,0,0,0];
const shot=async(t,f)=>{const c=cam(t),z=ST(t);if(!globalThis.CROWD){globalThis.CROWD=1;await p.evaluate(([tx,ty])=>{let sd=7;const R=()=>(sd=(sd*16807)%2147483647)/2147483647;const base=PETS.list.slice(),C=[];
 for(let r=0;r<700;r++){const a=Object.assign({},base[r%base.length]);const ang=R()*6.283,d=.45+Math.sqrt(R())*.65;const x=tx+Math.cos(ang)*d*80,y=ty+Math.sin(ang)*d*58;
  a.x=x;a.y=y;a.pause=1e9;a.wp=null;a.sit=R()<.4?1:0;a.dir=R()<.5?-1:1;a.view=['side','front','side','back'][(R()*4)|0];a.vert=a.view!=='side';a.i=5000+r;C.push(a);}
 C.sort((a,b)=>a.y-b.y);PETS.list.push(...C);},[G.ti.x,G.ti.y]);}await p.evaluate(([c,z])=>{const [gk,gv,lim,flt,nm]=z;GROWK=gk;GROWV=gv?MAIN:null;growing=gk!=null;limit=lim;
 document.getElementById('map').style.filter=flt?`grayscale(${.85*flt}) brightness(${1-.25*flt}) contrast(${1-.1*flt})`:'';window.NOLAB=z[5];cam.x=c[0];cam.y=c[1];cam.z=c[2];draw();},[c,z.concat([0,0])]);await p.clock.runFor(33.333);await p.screenshot({path:f,type:'jpeg',quality:92});};
fs.mkdirSync(out,{recursive:true});
if(test){for(const t of test.split(',').map(Number))await shot(t,`${out}/t${t}.jpg`);}else{const i0=Math.round(+t0S*30),i1=Math.min(N,Math.round(+t1S*30));for(let i=i0;i<i1;i++)await shot(i/30,`${out}/f${String(i).padStart(5,'0')}.jpg`);}
await b.close();console.log('ok',N);})();
