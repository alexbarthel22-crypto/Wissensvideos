// Einzelbilder zum Prüfen: node werkzeug/vorschau.cjs t1 t2 ...
const {chromium}=require('playwright');const path=require('path');
(async()=>{const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage({viewport:{width:540,height:960}});const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text());});
await p.goto('file://'+path.resolve(__dirname,'../rundgang.html')+'?w=540&h=960');await p.waitForTimeout(1500);
const dauer=await p.evaluate(()=>window.DAUER);
for(const t of process.argv.slice(2).map(Number)){const t0=Date.now();await p.evaluate(t=>setT(t),t);await p.screenshot({path:path.resolve(__dirname,`../renders/vorschau_${t}.png`)});console.log('t',t,(Date.now()-t0)+'ms');}
console.log('Dauer',dauer,errs);await b.close();})();
