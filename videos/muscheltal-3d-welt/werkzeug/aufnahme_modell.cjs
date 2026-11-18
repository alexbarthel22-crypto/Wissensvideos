// 3D-Flug mit dem bestehenden Modell (videos/muscheltal-3d/insel3d.html): Hauptinsel + Kokos-Küste
// node aufnahme_modell.cjs <timings.json> <out> <dauer> [test-zeiten]   (Server auf :8077 mit videos/ + muscheltal/site)
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;const dur=+durS;
const w=(id,s)=>{const x=L[id].words.find(q=>q.display.toLowerCase().replace(/[^\p{L}\p{N}-]/gu,'').startsWith(s.toLowerCase()));return x?x.start:L[id].start;};
const B={doener:[-150,108],baeck:[250,180],strand:[408,36],tier:[-50,180],club:[1503,606],game:[903,966]};
const at=(k,y=62,dz=88)=>[[B[k][0],y,B[k][1]+dz],[B[k][0],8,B[k][1]-16]];
const KM=[[0,[0,1150,1250],[0,0,40]],[L.L1.end-.3,[0,330,520],[0,10,40]],[L.L2.start+.2,[150,95,230],[0,18,40]],[L.L2.end,[-150,95,230],[0,18,40]],
 [L.L2b.start+.3,[-370,46,-150],[-250,0,-150]],[L.L2b.end+.3,[-230,46,-150],[-110,0,-150]],
 [w('L3','Dönerbude')-.05,...at('doener')],[w('L3','Bäckerei')-.45,...at('doener')],[w('L3','Bäckerei')-.05,...at('baeck')],[w('L3','Strandbar')-.45,...at('baeck')],
 [w('L3','Strandbar')-.05,...at('strand')],[w('L3','Tierheim')-.5,...at('strand')],[w('L3','Tierheim')-.05,...at('tier')],[L.L3.end+.3,...at('tier')],
 [L.L4.start-.15,[0,700,900],[0,0,0]],[dur,[500,520,700],[0,0,0]]];
const K1=[[L.L3k.start-.15,[1153,520,1550],[1153,0,930]],[w('L3k','Kokos-Club')-.1,...at('club')],[w('L3k','Game')-.45,...at('club')],[w('L3k','Game')-.05,...at('game')],[L.L3k.end-.2,...at('game')],[L.L4.start-.15,[1153,420,1500],[1153,0,900]]];
const kokos=t=>t>=L.L3k.start-.15&&t<L.L4.start-.15;
const cam=(K,t)=>{let j=0;while(j<K.length-1&&K[j+1][0]<=t)j++;const a=K[j],b=K[Math.min(j+1,K.length-1)];let k=b[0]>a[0]?Math.max(0,Math.min(1,(t-a[0])/(b[0]-a[0]))):1;k=k*k*(3-2*k);
 const ln=(p,q)=>p.map((v,i)=>v+(q[i]-v)*k);return {p:ln(a[1],b[1]),l:ln(a[2],b[2])};};
const br=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});
const pg=[];for(const ins of [0,1]){const p=await br.newPage({viewport:{width:1080,height:1920}});p.setDefaultTimeout(900000);p.on('pageerror',e=>console.log('ERR',e.message));
 await p.goto(`http://localhost:8077/videos/muscheltal-3d/insel3d.html?insel=${ins}&w=1080&h=1920&still=1&t=0`,{timeout:600000});await p.waitForFunction(()=>window.BEREIT===true,null,{timeout:300000});pg.push(p);}
fs.mkdirSync(out,{recursive:true});
const ts=test?test.split(',').map(Number):[...Array(Math.round(dur*30)).keys()].map(i=>i/30);
for(const [i,t] of ts.entries()){const ko=kokos(t),p=pg[ko?1:0],c=cam(ko?K1:KM,t);
 await p.evaluate(([c,t])=>{window.KAM_SET(c.p,c.l,50);window.BEREIT=false;window.ZEIT(t);},[c,t]);await p.waitForFunction(()=>window.BEREIT===true);
 await p.screenshot({path:`${out}/${test?'t'+t:'f'+String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:90});}
await br.close();console.log('ok',ts.length);})();
