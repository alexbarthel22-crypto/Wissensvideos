// Nimmt die Kamerafahrt Bild für Bild auf (1080x1920, 30 fps) und baut renders/rundgang-doener-meer.mp4
// node werkzeug/aufnahme.cjs
const {chromium}=require('playwright');const path=require('path'),fs=require('fs'),{execSync}=require('child_process');
(async()=>{const D=path.resolve(__dirname,'..'),F=path.join(D,'renders','frames');fs.rmSync(F,{recursive:true,force:true});fs.mkdirSync(F,{recursive:true});
const b=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader']});const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+path.join(D,'rundgang.html'));await p.waitForTimeout(2000);const dauer=await p.evaluate(()=>window.DAUER),n=Math.ceil(dauer*30);
for(let i=0;i<n;i++){await p.evaluate(t=>setT(t),i/30);await p.screenshot({path:path.join(F,`f${String(i).padStart(5,'0')}.jpg`),type:'jpeg',quality:92});if(i%60===0)console.log(i,'/',n);}
await b.close();execSync(`ffmpeg -loglevel error -y -framerate 30 -i ${F}/f%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 18 ${path.join(D,'renders','rundgang-doener-meer.mp4')}`);fs.rmSync(F,{recursive:true,force:true});console.log('fertig',dauer.toFixed(1),'s');})();
