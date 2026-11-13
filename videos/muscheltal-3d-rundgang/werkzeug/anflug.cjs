// Anflug auf die Haupt-Insel: schräg von oben (gekippte echte Karte mit Horizont), vom offenen Meer bis über den Muschelplatz.
// node werkzeug/anflug.cjs <site/index.html> <ausgabe.mp4> [dauer=14] [vorschau]
const {chromium}=require('playwright');const path=require('path'),fs=require('fs'),{execSync}=require('child_process');
const SITE=process.argv[2],OUT=process.argv[3],DAU=+(process.argv[4]||14),VOR=process.argv[5]==='vorschau';
(async()=>{const F=path.join(path.dirname(OUT),'frames_anflug');fs.rmSync(F,{recursive:true,force:true});fs.mkdirSync(F,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.clock.install({time:new Date('2026-11-13T14:10:00+01:00')});
await p.goto('file://'+SITE+'?zeit=tag&wetter=sonne');await p.clock.runFor(4000);await p.clock.pauseAt(new Date('2026-11-13T14:11:00+01:00'));
await p.evaluate(()=>{cancelAnimationFrame(fly);onScreen=false;
 const st=document.createElement('style');st.textContent='body>*{display:none!important}html,body{margin:0;height:100%;overflow:hidden;background:linear-gradient(#3aa7e0 0%,#9fdcf3 26%,#e8f8fd 31.5%,#7cc9d6 31.8%,#2a8fb0 36%,#0d6a8f 50%,#0a6488 100%)}#mapwrap{display:block!important;position:fixed;left:50%;top:'+(2400-7400)+'px;width:6400px;height:7400px;margin-left:-3200px;transform:rotateX(var(--tilt,58deg));transform-origin:50% 100%;-webkit-mask:linear-gradient(90deg,transparent 0,#000 6%,#000 94%,transparent 100%),linear-gradient(180deg,transparent 0,#000 10%,#000 100%);-webkit-mask-composite:source-in;mask-composite:intersect}#persp{display:block!important;position:fixed;inset:0;perspective:900px;perspective-origin:50% 50%}#mapwrap canvas{display:block;width:100%;height:100%}#dunst{display:block!important;position:fixed;left:0;right:0;top:0;height:47%;background:linear-gradient(rgba(232,248,253,0) 50%,rgba(232,248,253,.95) 67%,rgba(200,236,245,.55) 84%,rgba(200,236,245,0) 100%);pointer-events:none}';document.head.appendChild(st);
 const pe=document.createElement('div');pe.id='persp';const wrap=document.createElement('div');wrap.id='mapwrap';wrap.appendChild(cv);pe.appendChild(wrap);document.body.appendChild(pe);const du=document.createElement('div');du.id='dunst';document.body.appendChild(du);
 DPR=1;W=6400;H=7400;cv.width=base.width=fgc.width=W;cv.height=base.height=fgc.height=H;baseKey='';});
const n=VOR?6:Math.round(DAU*30);
for(let i=0;i<n;i++){const t=VOR?i*DAU/(n-1):i/30;
 await p.evaluate(([t,D])=>{const u=Math.min(1,t/D),e=u<.5?4*u*u*u:1-Math.pow(-2*u+2,3)/2;
  const v=MAIN,tx=v.x,ty0=v.y+v.R*3.2,ty1=v.y+8,ty=ty0+(ty1-ty0)*e,z=Math.exp(Math.log(.55)+(Math.log(4.2)-Math.log(.55))*e);
  const tilt=64-10*e;document.getElementById('mapwrap').style.setProperty('--tilt',tilt+'deg');
  const ang=tilt*Math.PI/180,pp=900,by=2400,scr=yl=>{const sz=pp/(pp+yl*Math.sin(ang));return 960+(by-yl*Math.cos(ang)-960)*sz;};let lo=0,hi=H;for(let k=0;k<40;k++){const m=(lo+hi)/2;if(scr(m)>1250)lo=m;else hi=m;}const yl=(lo+hi)/2;
  cam.z=z;cam.x=tx+Math.sin(u*3)*v.R*.05*(1-e);cam.y=ty-(H/2-yl)/z;T=1000+t;draw();},[t,DAU]);
 await p.clock.runFor(33.333);
 await p.screenshot({path:path.join(F,`f${String(i).padStart(5,'0')}.jpg`),type:'jpeg',quality:92});}
await b.close();
if(VOR){console.log('Vorschau in',F,errs.slice(0,3));return;}
execSync(`ffmpeg -loglevel error -y -framerate 30 -i ${F}/f%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 19 ${OUT}`);fs.rmSync(F,{recursive:true,force:true});console.log('fertig',errs.slice(0,3));})();
