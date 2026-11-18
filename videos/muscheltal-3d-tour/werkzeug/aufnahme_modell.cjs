// 3D-Inseltour mit dem Modell (videos/muscheltal-3d/insel3d.html): Hauptinsel (Seite 0) + Kokos-Küste (Seite 1)
// node aufnahme_modell.cjs <timings.json> <out> <dauer> [zeiten|@stride:offset]   (Server auf :8077 mit videos/ + muscheltal/site)
// Jede Einstellung = eine weiche Catmull-Rom-Fahrt (kein Anhalten an Zwischenpunkten), Schnitte zwischen Einstellungen.
// Volle 30 fps, kein Überblenden. Je Einstellung ein Neben-Event (Wal, Delfine, Flieger, Ballon, Jetski).
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [timf,out,durS,sel]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;const dur=+durS;const VW=810,VH=1440;
const w=(id,s)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}-]/gu,'').startsWith(s.toLowerCase()));return x?x.start:L[id].start;};
// ---- Einstellungen: [t0, t1, insel, [[pos,look],...], fov] ----
const S=[];const sh=(t1,ins,keys,fov=50)=>{const t0=S.length?S[S.length-1].t1:0;S.push({t0,t1,ins,keys,fov});};
sh(L.L1.end+.25,0,[[[0,1150,1250],[0,0,40]],[[0,620,860],[0,5,40]],[[0,330,520],[0,10,40]]]);
sh(L.L2b.start-.15,0,[[[-95,34,150],[0,22,10]],[[0,26,128],[0,22,10]],[[95,34,150],[0,22,10]]]);
sh(L.L2c.start-.15,0,[[[-200,32,45],[-200,6,-130]],[[-200,30,-10],[-200,6,-170]],[[-200,30,-60],[-200,6,-220]]]);
sh(L.L3.start-.1,0,[[[-230,175,40],[-230,0,-50]],[[-150,165,20],[-150,0,-70]]]);
sh(w('L3','Bäckerei')-.2,0,[[[-78,42,195],[-150,6,100]],[[-95,34,175],[-150,6,100]]]);
sh(L.L3s.start-.2,0,[[[190,42,262],[250,6,170]],[[205,32,238],[250,6,170]]]);
sh(L.L3t.start-.2,0,[[[408,66,171],[408,6,36]],[[412,58,150],[420,6,40]],[[440,40,118],[520,4,50]],[[472,26,88],[600,4,42]],[[478,24,80],[600,4,42]]]);
sh(L.L3k.start-.35,0,[[[8,42,258],[-50,6,170]],[[-8,36,245],[-50,6,170]],[[-25,32,236],[-50,6,170]]]);
sh(w('L3g','Kokos-Club')-.25,1,[[[1153,560,1580],[1153,0,930]],[[1175,200,1150],[1153,0,930]],[[1095,80,1000],[1153,6,930]],[[1105,46,972],[1153,6,930]]]);
sh(w('L3g','Game')-.2,1,[[[1555,46,700],[1503,8,600]],[[1545,40,685],[1503,8,600]]]);
sh(L.L3c.start-.2,1,[[[955,46,1060],[903,8,966]],[[945,40,1045],[903,8,966]]]);
sh(L.L4.start-.3,1,'kino');
sh(L.L5f.start-.2,0,[[[0,700,900],[0,0,0]],[[300,600,820],[0,0,0]]]);
sh(L.L5k.start-.15,0,[[[-120,40,-150],[-240,0,-150]],[[-250,40,-150],[-370,0,-150]]]);
sh(L.L5.start-.2,0,[[[-650,480,520],[0,0,0]],[[-350,480,800],[0,0,0]]]);
sh(dur,0,[[[-350,480,800],[0,0,0]],[[300,560,780],[0,0,0]]]);
const br=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const pg=[];for(const ins of [0,1]){const p=await br.newPage({viewport:{width:VW,height:VH}});p.setDefaultTimeout(900000);p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto(`http://localhost:8077/videos/muscheltal-3d/insel3d.html?insel=${ins}&w=${VW}&h=${VH}&still=1&t=0`,{timeout:900000});await p.waitForFunction(()=>window.BEREIT===true);pg.push(p);}
const NO=Object.assign({},await pg[0].evaluate(()=>window.NEUORTE||{}),await pg[1].evaluate(()=>window.NEUORTE||{}));
const [kx,kz]=NO.kino||[1403,1038];for(const s of S)if(s.keys==='kino')s.keys=[[[kx,46,kz+118],[kx,15,kz-25]],[[kx,32,kz+80],[kx,16,kz-25]]];
const ix=k=>S.findIndex(s=>s.t1>k);const at=(i,d=0)=>S[i].t0+d;
// ---- Neben-Events (absolute Zeiten je Insel-Seite) ----
const E0=[{typ:'ballon',x:-170,z:420,h:330,t0:0,dur:3,s:3},{typ:'flieger',x:0,z:-230,h:105,dir:Math.PI/2,t0:at(1,-.3),dur:5,len:360},
 {typ:'delfine',x:-200,z:-470,dir:Math.PI/2,t0:at(2),dur:5},{typ:'jetski',x:-270,z:-470,r:30,t0:at(3),dur:4},
 {typ:'ballon',x:-60,z:-120,h:110,t0:at(4),dur:4},{typ:'ballon',x:330,z:60,h:95,t0:at(5),dur:4},
 {typ:'walsprung',x:588,z:58,dir:Math.PI,t0:L.L3s.end+.85,dur:3.2},
 {typ:'ballon',x:-40,z:40,h:85,t0:at(7),dur:5},
 {typ:'flieger',x:150,z:500,h:420,dir:Math.PI/2,t0:at(12),dur:5,len:700,s:4},{typ:'ballon',x:-300,z:-200,h:70,t0:at(13),dur:4},
 {typ:'wal',x:-460,z:330,dir:Math.PI*.75,t0:at(14,-.4),dur:4},{typ:'flieger',x:-30,z:520,h:400,dir:Math.PI/2,t0:at(15),dur:4.5,len:650,s:4}];
const E1=[{typ:'delfine',x:1153,z:1700,dir:Math.PI/2,t0:at(8),dur:4},{typ:'ballon',x:1450,z:520,h:70,t0:at(9),dur:2},{typ:'jetski',x:1640,z:560,r:30,t0:at(10),dur:3},{typ:'ballon',x:kx+60,z:kz-90,h:75,t0:at(11),dur:3}];
await pg[0].evaluate(e=>{window.EVT=e;},E0);await pg[1].evaluate(e=>{window.EVT=e;},E1);
// ---- Kamera: Catmull-Rom über die Schlüssel, leicht geglättete Geschwindigkeit ----
const cr=(P,u)=>{const n=P.length-1;if(n<1)return P[0];const x=u*n,i=Math.min(n-1,Math.floor(x)),f=x-i,p0=P[Math.max(0,i-1)],p1=P[i],p2=P[i+1],p3=P[Math.min(n,i+2)];
 return p1.map((_,j)=>{const a=p0[j],b=p1[j],c=p2[j],d=p3[j];return .5*((2*b)+(-a+c)*f+(2*a-5*b+4*c-d)*f*f+(-a+3*b-3*c+d)*f*f*f);});};
const cam=t=>{const s=S[Math.max(0,ix(t))]||S[S.length-1];let u=Math.max(0,Math.min(1,(t-s.t0)/(s.t1-s.t0)));u=.6*u+.4*u*u*(3-2*u);return {si:S.indexOf(s),ins:s.ins,fov:s.fov,p:cr(s.keys.map(k=>k[0]),u),l:cr(s.keys.map(k=>k[1]),u)};};
fs.mkdirSync(out,{recursive:true});fs.writeFileSync(out+'/../cuts.json',JSON.stringify(S.map(s=>s.t0).slice(1)));
let ts=[...Array(Math.round(dur*30)).keys()].map(i=>i/30);
if(sel&&sel[0]==='@'){const [st,of]=sel.slice(1).split(':').map(Number);ts=ts.filter((_,i)=>i%st===of);}else if(sel)ts=sel.split(',').map(Number);
for(const t of ts){const c=cam(t),p=pg[c.ins],fn=`${out}/f${String(Math.round(t*30)).padStart(5,'0')}.jpg`;if(fs.existsSync(fn))continue;
 await p.evaluate(([c,t,hn])=>{if(window.HUTNAMEN)window.HUTNAMEN(hn);window.KAM_SET(c.p,c.l,c.fov);window.BEREIT=false;window.ZEIT(t);},[c,t,c.si===3]);await p.waitForFunction(()=>window.BEREIT===true);
 await p.screenshot({path:fn,type:'jpeg',quality:92});}
await br.close();console.log('ok',ts.length,JSON.stringify(NO));})();
