// Liest die echte Karte (muscheltal/site/index.html, lokal gebaut) und schreibt welt.json für die 3D-Ansicht.
// Nur für Videos – liegt NICHT im veröffentlichten Ordner.
// node werkzeug/welt_holen.cjs
const {chromium}=require('playwright');const fs=require('fs');const path=require('path');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+path.resolve(__dirname,'../../../muscheltal/site/index.html')+'?zeit=tag');await p.waitForTimeout(2500);
const w=await p.evaluate(()=>{const v=MAIN;canWalk(0,0);
 const umriss=[];for(let i=0;i<240;i++){const a=i/240*TAU,r=coastAt(v,a);umriss.push([+(v.x+Math.cos(a)*r).toFixed(1),+(v.y+Math.sin(a)*r*.92).toFixed(1)]);}
 const huetten=v.people.filter(q=>q.p).map(q=>({n:q.name,x:+q.p.x.toFixed(1),y:+q.p.y.toFixed(1),rund:!!q.round,wand:q.wall,dach:['#e8c25a','#dcb04a','#f0cd6a'][q.nr%3],tuer:q.roof,fenster:!!q.win}));
 const geb=GEB.map(g=>({typ:g.typ,name:g.name,cx:g.cx,cy:g.cy,x0:g.x0,x1:g.x1,y0:g.y0,y1:g.y1,dir:g.dir||1,sea:g.sea}));
 const bau=BAU.map(b=>({name:b.name,steg:!!b.steg,x0:b.x0,x1:b.x1,y0:b.y0,y1:b.y1,cx:b.cx,cy:b.cy,ox:b.ox,oy:b.oy,ang:b.ang,len:b.len,w:b.w}));
 const palmen=v.palms.map(t=>[+t.x.toFixed(1),+t.y.toFixed(1),+t.s.toFixed(2)]),buesche=v.bush.map(b=>[+b.x.toFixed(1),+b.y.toFixed(1),+b.r.toFixed(1)]),laternen=v.lamps.map(([x,y])=>[+x.toFixed(1),+y.toFixed(1)]),baenke=v.benches.map(([x,y])=>[+x.toFixed(1),+y.toFixed(1)]),steine=v.rocks.map(r=>[+r.x.toFixed(1),+r.y.toFixed(1),+r.r.toFixed(1)]);
 // Weg: vom Döner-Tresen durch den Eingang zur nächstgelegenen Küste (über die Wege)
 const d=GEB.find(g=>g.typ==='doener'),H=(d.y1-d.y0)/2,CY=4*S*.9,CX=5*S;const rowY=v.y+Math.ceil((d.y1-v.y)/CY)*CY;const start=[d.cx-3,d.cy+21],tor=[d.cx,d.y1+1];
 const ende=(x,y,dx,dy)=>{let t=0;while(inside(v,x+dx*t,y+dy*t,-2))t+=1;return[x+dx*(t-2),y+dy*(t-2),t];};
 const cand=[];for(const [dx,dy] of[[-1,0],[1,0]]){const e=ende(d.cx,rowY,dx,dy);cand.push({p:[start,tor,[d.cx,rowY],[e[0],e[1]]],len:e[2],blick:[dx,dy]});}
 for(const k of[Math.floor((d.cx-v.x)/CX),Math.ceil((d.cx-v.x)/CX)]){const cx=v.x+k*CX;for(const dy of[1,-1]){const e=ende(cx,rowY,0,dy);cand.push({p:[start,tor,[d.cx,rowY],[cx,rowY],[e[0],e[1]]],len:Math.abs(cx-d.cx)+e[2],blick:[0,dy]});}}
 cand.sort((a,b)=>a.len-b.len);const route=cand[0];
 return{S,mitte:[v.x,v.y],R:v.R,plaza:v.plaza,palS:PAL_S,umriss,huetten,geb,bau,palmen,buesche,laternen,baenke,steine,route,pier:[PIER0,PIER1]};});
fs.writeFileSync(path.resolve(__dirname,'../welt.json'),JSON.stringify(w));console.log('Hütten',w.huetten.length,'Route',JSON.stringify(w.route));await b.close();})();
