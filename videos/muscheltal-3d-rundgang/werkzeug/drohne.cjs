// Drohnenflug über die ECHTE Karte (muscheltal/site/index.html): dieselbe Zeichnung, alle Details & Animationen,
// schräg gekippt mit Horizont. Nur für Videos.  node werkzeug/drohne.cjs [zeit=tag|nacht|...] [vorschau]
const {chromium}=require('playwright');const path=require('path'),fs=require('fs'),{execSync}=require('child_process');
const ZEIT=process.argv[2]||'tag',VOR=process.argv[3]==='vorschau';
(async()=>{const D=path.resolve(__dirname,'..'),F=path.join(D,'renders','frames_drohne');fs.rmSync(F,{recursive:true,force:true});fs.mkdirSync(F,{recursive:true});
const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+path.resolve(D,'../../muscheltal/site/index.html')+'?zeit='+ZEIT);await p.waitForTimeout(3000);
const info=await p.evaluate(()=>{cancelAnimationFrame(fly);onScreen=false;
 // nur die Karte zeigen, groß und schräg gekippt (Horizont oben), Himmel dahinter
 const st=document.createElement('style');st.textContent='body>*{display:none!important}html,body{margin:0;height:100%;overflow:hidden;background:linear-gradient(#4fb6e8 0%,#a6e0f5 30%,#e4f6fc 34.6%,#3fb7c8 34.9%,#1aa6bf 45%,#139bb7 100%)}#mapwrap{display:block!important;position:fixed;left:50%;top:'+(1950-5000)+'px;width:3600px;height:5000px;margin-left:-1800px;transform:rotateX(58deg);transform-origin:50% 100%}#persp{display:block!important;position:fixed;inset:0;perspective:900px;perspective-origin:50% 50%}#mapwrap canvas{display:block;width:100%;height:100%}#dunst{display:block!important;position:fixed;left:0;right:0;top:0;height:42%;background:linear-gradient(rgba(228,246,252,0) 62%,rgba(228,246,252,.9) 82%,rgba(228,246,252,0) 100%);pointer-events:none}';document.head.appendChild(st);
 const pe=document.createElement('div');pe.id='persp';const wrap=document.createElement('div');wrap.id='mapwrap';wrap.appendChild(cv);pe.appendChild(wrap);document.body.appendChild(pe);const du=document.createElement('div');du.id='dunst';document.body.appendChild(du);
 DPR=1;W=3600;H=5000;cv.width=base.width=fgc.width=W;cv.height=base.height=fgc.height=H;baseKey='';
 // Route: über der Dönerbude starten, durch den Eingang auf den Weg, dann zur nächsten Küste in Blickrichtung Norden/Westen/Osten
 const v=MAIN,d=GEB.find(g=>g.typ==='doener'),CY=4*S*.9,CX=5*S;const rowY=v.y+Math.ceil((d.y1-v.y)/CY)*CY,rowN=v.y+Math.floor((d.y0-v.y)/CY)*CY;
 const ende=(x,y,dx,dy)=>{let t=0;while(inside(v,x+dx*t,y+dy*t,-6))t+=1;return[x+dx*t,y+dy*t,t];};
 const c=[];for(const dx of[-1,1]){const e=ende(d.cx,rowY,dx,0);c.push({name:dx<0?'Westen':'Osten',p:[[d.cx,d.cy+40],[d.cx,rowY],[e[0],e[1]]],len:e[2]});}
 for(const k of[Math.floor((d.cx-v.x)/CX),Math.ceil((d.cx-v.x)/CX)]){const cx=v.x+k*CX,e=ende(cx,rowN,0,-1);c.push({name:'Norden',p:[[d.cx,d.cy+40],[d.cx,rowY],[cx,rowY],[cx,rowN],[e[0],e[1]]],len:Math.abs(cx-d.cx)+e[2]+(rowY-rowN)});}
 c.sort((a,b)=>a.len-b.len);window.ROUTE=c[0];return c.map(x=>x.name+' '+Math.round(x.len));});
console.log('Routen:',info.join(', '));
const dauer=await p.evaluate(()=>{const pts=ROUTE.p,L=[0];for(let i=1;i<pts.length;i++)L.push(L[i-1]+Math.hypot(pts[i][0]-pts[i-1][0],pts[i][1]-pts[i-1][1]));window.RL=L;window.TOT=L[L.length-1];window.DAU=2+TOT/13+4;return DAU;});
const n=VOR?6:Math.ceil(dauer*30);
for(let i=0;i<n;i++){const t=VOR?i*dauer/(n-1):i/30;await p.evaluate(t=>{const pts=ROUTE.p,L=RL,sm=u=>u*u*(3-2*u);let s;if(t<2)s=0;else if(t<DAU-4)s=sm((t-2)/(DAU-6))*TOT;else s=TOT+sm(Math.min(1,(t-(DAU-4))/4))*30;
 let i=1;while(i<L.length-1&&L[i]<s)i++;const a=pts[i-1],b2=pts[i],u=Math.min(1.4,(s-L[i-1])/Math.max(1,L[i]-L[i-1]));const x=a[0]+(b2[0]-a[0])*u,y=a[1]+(b2[1]-a[1])*u;
 const z=7.2,ang=58*Math.PI/180,pp=900,by=1950,scr=yl=>{const sz=pp/(pp+yl*Math.sin(ang));return 960+(by-yl*Math.cos(ang)-960)*sz;};let lo=0,hi=H;for(let k=0;k<40;k++){const m=(lo+hi)/2;if(scr(m)>1420)lo=m;else hi=m;}const yl=(lo+hi)/2;cam.z=z;cam.x=x;cam.y=y-(H/2-yl)/z;T=1000+t;draw();},t);
 await p.screenshot({path:path.join(F,`f${String(i).padStart(5,'0')}.jpg`),type:'jpeg',quality:92});if(!VOR&&i%90===0)console.log(i,'/',n);}
await b.close();
if(VOR){console.log('Vorschau-Bilder in',F,errs);return;}
execSync(`ffmpeg -loglevel error -y -framerate 30 -i ${F}/f%05d.jpg -c:v libx264 -pix_fmt yuv420p -crf 18 ${path.join(D,'renders','drohne-doener-kueste.mp4')}`);fs.rmSync(F,{recursive:true,force:true});console.log('fertig',dauer.toFixed(1),'s',errs);})();
