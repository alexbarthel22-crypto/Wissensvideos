// 3D-Flug mit dem bestehenden Modell (videos/muscheltal-3d/insel3d.html): Hauptinsel + Kokos-Küste
// node aufnahme_modell.cjs <timings.json> <out> <dauer> [zeiten]   (Server auf :8077 mit videos/ + muscheltal/site)
// Gebäude: harte Schnitte + langsame Fahrt auf das Gebäude zu (keine schnellen Schwenks). Aufnahme in 810x1440, wird hochskaliert.
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;const dur=+durS;const VW=810,VH=1440;
const w=(id,s)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}-]/gu,'').startsWith(s.toLowerCase()));return x?x.start:L[id].start;};
const br=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const pg=[];for(const ins of [0,1]){const p=await br.newPage({viewport:{width:VW,height:VH}});p.setDefaultTimeout(900000);p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto(`http://localhost:8077/videos/muscheltal-3d/insel3d.html?insel=${ins}&w=${VW}&h=${VH}&still=1&t=0`);await p.waitForFunction(()=>window.BEREIT===true);pg.push(p);}
const NO=Object.assign({},await pg[0].evaluate(()=>window.NEUORTE||{}),await pg[1].evaluate(()=>window.NEUORTE||{}));
const B={doener:[-150,108],baeck:[250,180],tier:[-50,180],club:[1503,606],game:[903,966],kino:NO.kino||[1153,930]};
// Gebäude-Einstellung: von weiter weg langsam heranfahren
const shot=(k,t0,t1,y=62,dz=88)=>{const [x,z]=B[k];return [[t0,[x,y+14,z+dz+30],[x,8,z-16]],[t1,[x,y,z+dz],[x,8,z-16]]];};
const strand=(t0,t1)=>[[t0,[408,66,36+135],[408,6,36]],[t1,[408,55,36+107],[408,6,36]]];
const cuts=[];const C=(...segs)=>{const o=[];for(const s of segs){cuts.push(s[0][0]);o.push(...s);}return o;};
const KM=[[0,[0,1150,1250],[0,0,40]],[L.L1.end+.3,[0,330,520],[0,10,40]],[L.L2.start+.3,[150,95,230],[0,18,40]],[L.L2.end+.2,[-150,95,230],[0,18,40]],
 [L.L2b.start-.1,[-370,46,-150],[-250,0,-150]],[L.L2c.start-.4,[-250,46,-150],[-130,0,-150]],
 [L.L2c.start-.1,[-340,80,-70],[-340,0,-160]],[L.L3.start-.1,[-240,80,-70],[-240,0,-160]],
 ...C(shot('doener',L.L3.start,w('L3','Bäckerei')-.2),shot('baeck',w('L3','Bäckerei')-.15,L.L3s.start-.25),strand(L.L3s.start-.2,w('L3s','Tierheim')-.3),shot('tier',w('L3s','Tierheim')-.25,L.L3k.start-.35)),
 ...C([[L.L4.start-.3,[0,700,900],[0,0,0]],[L.L5f.start-.2,[300,600,820],[0,0,0]]]),
 ...C([[L.L5f.start-.15,[-120,40,-150],[-240,0,-150]],[L.L5k.start-.2,[-250,40,-150],[-370,0,-150]]]),
 ...C([[L.L5k.start-.15,[-650,480,520],[0,0,0]],[L.L5.start-.2,[-350,480,800],[0,0,0]]]),
 [L.L5.start-.15,[-350,480,800],[0,0,0]],[dur,[300,560,780],[0,0,0]]];
const K1=[...C([[L.L3k.start-.35,[1153,620,1650],[1153,0,930]],[w('L3k','Kokos-Club')-.35,[1153,330,1350],[1153,0,900]]]),
 ...C(shot('club',w('L3k','Kokos-Club')-.3,L.L3g.start-.2),shot('game',L.L3g.start-.15,L.L3c.start-.2),shot('kino',L.L3c.start-.15,L.L4.start-.35,70,100))];
const kokos=t=>t>=L.L3k.start-.35&&t<L.L4.start-.3;cuts.push(L.L3k.start-.35,L.L4.start-.3);
const cam=(K,t)=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],b=K[Math.min(j+1,K.length-1)];let k=b[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(b[0]-a[0]))):1;k=k*k*(3-2*k);
 const ln=(p,q)=>p.map((v,i)=>v+(q[i]-v)*k);return {p:ln(a[1],b[1]),l:ln(a[2],b[2])};};
fs.mkdirSync(out,{recursive:true});fs.writeFileSync(out+'/../cuts.json',JSON.stringify(cuts.sort((a,b)=>a-b)));
const ts=test?test.split(',').map(Number):[...Array(Math.round(dur*30)).keys()].map(i=>i/30);
for(const [i,t] of ts.entries()){const ko=kokos(t),p=pg[ko?1:0],c=cam(ko?K1:KM,t);
 await p.evaluate(([c,t])=>{window.KAM_SET(c.p,c.l,50);window.BEREIT=false;window.ZEIT(t);},[c,t]);await p.waitForFunction(()=>window.BEREIT===true);
 await p.screenshot({path:`${out}/t${t}.jpg`,type:'jpeg',quality:92});}
await br.close();console.log('ok',ts.length,JSON.stringify(NO));})();
