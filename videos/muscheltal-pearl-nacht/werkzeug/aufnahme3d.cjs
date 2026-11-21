// 3D-Flug durch Muschel-Tal: node aufnahme3d.cjs <timings.json> <out> <dauer> [test-zeiten]
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [timf,out,durS,test]=process.argv.slice(2);const T=JSON.parse(fs.readFileSync(timf));const L={};for(const l of T.lines)L[l.id]=l;const dur=+durS;
const K=[ // [t, pos, look, label]
 [0,[-240,200,-270],[40,0,15],0],[L.L1.end-.4,[-95,70,-95],[2,4,2],0],[L.L2.start,[-70,32,-52],[0,4,-12],.5],
 [L.L2.start+1.6,[-48,17,-40],[-8,4,-38],1],[L.L2.end+.4,[-6,16,-40],[34,4,-38],1],
 [L.L3.start+1.2,[40,62,-50],[80,0,30],0],[L.L3.end+.2,[135,38,25],[190,2,90],.4],
 [L.L4.start+.6,[155,17,62],[198,4,66],1],[L.L4.end+.6,[200,16,55],[235,4,75],1],
 [L.L5.start+1.2,[190,100,230],[100,0,50],0],[dur,[100,230,350],[95,0,45],0]];
const lerp=(a,b,k)=>a+(b-a)*k,cr=(p0,p1,p2,p3,t)=>{const t2=t*t,t3=t2*t;return .5*((2*p1)+(-p0+p2)*t+(2*p0-5*p1+4*p2-p3)*t2+(-p0+3*p1-3*p2+p3)*t3);};
function cam(t){let j=0;while(j<K.length-2&&K[j+1][0]<=t)j++;const a=K[Math.max(0,j-1)],b=K[j],c=K[j+1],d=K[Math.min(K.length-1,j+2)];
 let k=Math.max(0,Math.min(1,(t-b[0])/(c[0]-b[0])));k=k*k*(3-2*k);
 const v=(i)=>[0,1,2].map(n=>cr(a[i][n],b[i][n],c[i][n],d[i][n],k));return {t,p:v(1),l:v(2),lab:lerp(b[3],c[3],k)};}
const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('http://localhost:8877/welt3d.html');await p.waitForFunction(()=>window.READY,null,{timeout:60000});
fs.mkdirSync(out,{recursive:true});
const ts=test?test.split(',').map(Number):[...Array(Math.round(dur*30)).keys()].map(i=>i/30);
for(const [i,t] of ts.entries()){await p.evaluate(c=>setT(c.t,c),cam(t));await p.screenshot({path:`${out}/${test?'t'+t:'f'+String(i).padStart(5,'0')}.jpg`,type:'jpeg',quality:90});}
await b.close();console.log('ok',ts.length);})();
