// ---------- Grundlagen ----------
const P=new URLSearchParams(location.search),BW=+(P.get('w')||1080),BH=+(P.get('h')||1920),TAU=Math.PI*2;
const hash=(i,s)=>{let x=Math.sin(i*127.1+s*311.7)*43758.5453;return x-Math.floor(x);};
const cv=document.getElementById('cv'),R=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true,preserveDrawingBuffer:true});R.setPixelRatio(1);R.setSize(BW,BH,false);
R.shadowMap.enabled=true;R.shadowMap.type=THREE.PCFSoftShadowMap;
const S=new THREE.Scene();S.fog=new THREE.Fog(0xcfeefa,120,520);
const cam=new THREE.PerspectiveCamera(74,BW/BH,.3,1500);
S.add(new THREE.HemisphereLight(0xfff8ea,0x9aa878,1.45));
const sun=new THREE.DirectionalLight(0xfff0d8,1.5);sun.castShadow=true;sun.shadow.mapSize.set(2048,2048);const sc=sun.shadow.camera;sc.left=-90;sc.right=90;sc.top=90;sc.bottom=-90;sc.near=1;sc.far=400;sun.shadow.bias=-.0006;S.add(sun);S.add(sun.target);
const M=(c,o={})=>new THREE.MeshLambertMaterial(Object.assign({color:c},o));
const add=(geo,mat,x,y,z,sh=true)=>{const m=new THREE.Mesh(geo,mat);m.position.set(x,y,z);m.castShadow=sh;m.receiveShadow=true;S.add(m);return m;};
const W=WELT,[MX,MY]=W.mitte;
// Polygon-Test für den Inselumriss
const inPoly=(x,y,pl)=>{let c=false;for(let i=0,j=pl.length-1;i<pl.length;j=i++){const [xi,yi]=pl[i],[xj,yj]=pl[j];if(((yi>y)!==(yj>y))&&(x<(xj-xi)*(y-yi)/(yj-yi)+xi))c=!c;}return c;};
const schrumpf=(pl,d)=>pl.map(([x,y])=>{const dx=x-MX,dy=y-MY,l=Math.hypot(dx,dy);return[MX+dx*(l-d)/l,MY+dy*(l-d)/l];});
const flaeche=(pl,col,y)=>{const sh=new THREE.Shape(pl.map(([x,z])=>new THREE.Vector2(x,-z)));const m=add(new THREE.ShapeGeometry(sh,2),M(col),0,y,0,false);m.rotation.x=-Math.PI/2;return m;};
// Texte als Textur (Namen, Schilder)
const texCache={};
function textTex(t,{fg='#2a1b12',bg='rgba(255,255,255,.95)',fs=46,pad=18,round=true,font='900'}={}){const k=[t,fg,bg,fs].join('|');if(texCache[k])return texCache[k];const c=document.createElement('canvas'),x=c.getContext('2d');x.font=font+' '+fs+'px Arial, sans-serif';const w=Math.ceil(x.measureText(t).width)+pad*2,h=Math.ceil(fs*1.45);c.width=w;c.height=h;
 x.font=font+' '+fs+'px Arial, sans-serif';x.fillStyle=bg;x.beginPath();if(round&&x.roundRect)x.roundRect(0,0,w,h,h/2);else x.rect(0,0,w,h);x.fill();x.fillStyle=fg;x.textAlign='center';x.textBaseline='middle';x.fillText(t,w/2,h/2+2);const tx=new THREE.CanvasTexture(c);tx.anisotropy=8;return texCache[k]={tx,w,h};}
function label(t,x,y,z,hgt,opt){const {tx,w,h}=textTex(t,opt);const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:tx,depthWrite:false}));sp.scale.set(hgt*w/h,hgt,1);sp.position.set(x,y,z);S.add(sp);return sp;}
function schild(t,x,y,z,breite,opt,rotY=0){const {tx,w,h}=textTex(t,opt);const m=new THREE.Mesh(new THREE.PlaneGeometry(breite,breite*h/w),new THREE.MeshBasicMaterial({map:tx,transparent:true}));m.position.set(x,y,z);m.rotation.y=rotY;S.add(m);return m;}

// ---------- Meer, Strand, Wiese ----------
const sea=new THREE.Mesh(new THREE.PlaneGeometry(3000,3000,1,1),new THREE.MeshPhongMaterial({color:0x17b3c6,shininess:90,specular:0x99ddee}));sea.rotation.x=-Math.PI/2;sea.position.y=-.6;sea.receiveShadow=true;S.add(sea);
flaeche(schrumpf(W.umriss,-26),0x3fd0d4,-.5);flaeche(schrumpf(W.umriss,-10),0x7fe0dc,-.45);
flaeche(W.umriss,0xf3dcac,-.3);flaeche(schrumpf(W.umriss,10),0x8fd065,-.2);
// Gischt (wird animiert)
const foam=[];for(let k=0;k<3;k++){const pts=schrumpf(W.umriss,-4-k*7).map(([x,z])=>new THREE.Vector3(x,-.35,z));pts.push(pts[0].clone());const l=new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),new THREE.LineBasicMaterial({color:0xffffff,transparent:true,opacity:.6}));S.add(l);foam.push(l);}
// ---------- Wege (Raster wie auf der Karte, nur auf der Insel) ----------
{const CX=5*W.S,CY=4*W.S*.9,g=Math.ceil(W.R/W.S)+1,inner=schrumpf(W.umriss,6),mat=M(0xf3dcac),edge=M(0xe3c48a);
 const strip=(x0,z0,x1,z1,b,mt,yy)=>{const L=Math.hypot(x1-x0,z1-z0);const m=add(new THREE.PlaneGeometry(L,b),mt,(x0+x1)/2,yy,(z0+z1)/2,false);m.rotation.x=-Math.PI/2;m.rotation.z=-Math.atan2(z1-z0,x1-x0);};
 const seg=(fx,vert,c)=>{let run=null;for(let t=-W.R;t<=W.R;t+=2){const x=vert?c:MX+t,z=vert?MY+t:c,ok=inPoly(x,z,inner);if(ok&&!run)run=t;if((!ok||t+2>W.R)&&run!=null){const a=run,b=ok?t:t-2;if(b>a){if(vert){strip(c,MY+a,c,MY+b,8,edge,-.15);strip(c,MY+a,c,MY+b,5.6,mat,-.12);}else{strip(MX+a,c,MX+b,c,8,edge,-.15);strip(MX+a,c,MX+b,c,5.6,mat,-.12);}}run=null;}}};
 for(let gx=-g;gx<=g;gx++){if(((gx%5)+5)%5)continue;seg(0,true,MX+gx*W.S);}for(let gy=-g;gy<=g;gy++){if(((gy%4)+4)%4)continue;seg(0,false,MY+gy*W.S*.9);}
 // Sandkörnchen auf den Wegen
 const gg=new THREE.BufferGeometry(),pos=[],col=[];for(let i=0;i<9000;i++){const vert=hash(i,1)<.5,k=Math.round((hash(i,2)*2-1)*g/(vert?5:4))*(vert?5:4),t=(hash(i,3)*2-1)*W.R,x=vert?MX+k*W.S+(hash(i,4)-.5)*5:MX+t,z=vert?MY+t:MY+k*W.S*.9+(hash(i,4)-.5)*5;if(!inPoly(x,z,inner))continue;pos.push(x,-.08,z);const c=hash(i,5)<.6?[.67,.53,.33]:[1,.98,.92];col.push(...c);}
 gg.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));gg.setAttribute('color',new THREE.Float32BufferAttribute(col,3));S.add(new THREE.Points(gg,new THREE.PointsMaterial({size:.35,vertexColors:true})));}
// ---------- Hütten ----------
const route=W.route.p,nahRoute=(x,z,d)=>{for(let i=1;i<route.length;i++){const [ax,az]=route[i-1],[bx,bz]=route[i],L2=(bx-ax)**2+(bz-az)**2;let t=L2?((x-ax)*(bx-ax)+(z-az)*(bz-az))/L2:0;t=Math.max(0,Math.min(1,t));if(Math.hypot(x-(ax+t*(bx-ax)),z-(az+t*(bz-az)))<d)return true;}return false;};
const stilt=new THREE.CylinderGeometry(.45,.45,2.6,6),body=new THREE.BoxGeometry(12,7,9),roofP=new THREE.ConeGeometry(10.6,9.5,4,1),roofR=new THREE.ConeGeometry(10.2,10,14,1),stiltM=M(0x7a4a24),doorM=M(0x5a3418),winM=M(0x4a2c16);
const strohM={};const stroh=c=>strohM[c]||(strohM[c]=M(c));const wandM={};const wand=c=>wandM[c]||(wandM[c]=M(c));
for(const h of W.huetten){const x=h.x,z=h.y+3;
 for(const [dx,dz] of[[-4.5,-3],[4.5,-3],[-4.5,3],[4.5,3]])add(stilt,stiltM,x+dx,1.3,z+dz);
 add(body,wand(h.wand),x,2.6+3.5,z);const r=h.rund?add(roofR,stroh(h.dach),x,9.6+5,z):add(roofP,stroh(h.dach),x,9.6+4.75,z);if(!h.rund)r.rotation.y=Math.PI/4;r.scale.z=.9;
 add(new THREE.BoxGeometry(2.6,4.6,.3),doorM,x,2.6+2.3,z+4.55,false);if(h.fenster)add(new THREE.BoxGeometry(2.2,2.2,.3),winM,x+3.6,2.6+4.2,z+4.55,false);
 if(nahRoute(x,z,150))label(h.n,x,10.6,z+5.4,2.6);}
// ---------- Natur & Deko ----------
const trunkM=M(0x8a5a2b),leafM=M(0x3f9b45),leafM2=M(0x57b85a);
for(const [x,z,s] of W.palmen){const h=16*s,tr=add(new THREE.CylinderGeometry(.5*s,.8*s,h,7),trunkM,x,h/2,z+3);tr.rotation.z=(hash(x,z)-.5)*.25;
 for(let k=0;k<7;k++){const a=k/7*TAU+hash(z,x),lf=add(new THREE.ConeGeometry(1.4*s,8*s,4),k%2?leafM:leafM2,x+Math.cos(a)*3*s,h+.4,z+3+Math.sin(a)*3*s);lf.rotation.z=Math.cos(a)*1.25;lf.rotation.x=-Math.sin(a)*1.25;lf.scale.z=.35;}}
for(const [x,z,r] of W.buesche)add(new THREE.SphereGeometry(r*.9,9,7),leafM,x,r*.6,z);
const rockM=M(0x9aa0a6);for(const [x,z,r] of W.steine)add(new THREE.DodecahedronGeometry(r*.8,0),rockM,x,r*.3,z);
const lampM=M(0x33333f),lampG=new THREE.MeshBasicMaterial({color:0xfff3c4});for(const [x,z] of W.laternen){add(new THREE.CylinderGeometry(.3,.35,11,6),lampM,x,5.5,z);add(new THREE.BoxGeometry(1.6,1.6,1.6),lampG,x,11.4,z,false);}
const benchM=M(0xa8743c);for(const [x,z] of W.baenke){add(new THREE.BoxGeometry(9,.6,2.6),benchM,x,2,z);add(new THREE.BoxGeometry(9,2.6,.5),benchM,x,3.4,z-1.2);}
// Menschen (einfach): Körper, Kopf, Haare
function mensch(x,z,shirt,hair,rot=0){const g=new THREE.Group();const b=new THREE.Mesh(new THREE.CylinderGeometry(1.5,1.7,4.6,10),M(shirt));b.position.y=6.2;const l1=new THREE.Mesh(new THREE.CylinderGeometry(.55,.55,4.2,6),M(0x2a3a5a));l1.position.set(-.7,2.1,0);const l2=l1.clone();l2.position.x=.7;
 const k=new THREE.Mesh(new THREE.SphereGeometry(1.5,12,10),M(0xf3c9a0));k.position.y=9.7;const hh=new THREE.Mesh(new THREE.SphereGeometry(1.58,12,10,0,TAU,0,Math.PI*.55),M(hair));hh.position.y=9.8;[b,l1,l2,k,hh].forEach(m=>{m.castShadow=true;g.add(m);});g.position.set(x,0,z);g.rotation.y=rot;S.add(g);return g;}
// ---------- Dönerbude (nach Karte) ----------
const d=W.geb.find(g=>g.typ==='doener');if(d){const X=x=>d.cx+x,Z=z=>d.cy+z,Wd=(d.x1-d.x0)/2,Hd=(d.y1-d.y0)/2;
 const boden=add(new THREE.PlaneGeometry(2*Wd,2*Hd),M(0xecdcbc),d.cx,-.05,d.cy,false);boden.rotation.x=-Math.PI/2;
 // Mauer mit blauen Fliesen, Eingang unten Mitte
 const mauer=(x0,z0,x1,z1)=>{const L=Math.hypot(x1-x0,z1-z0),m=add(new THREE.BoxGeometry(L,3.2,1.6),M(0xf7f1e6),(x0+x1)/2,1.6,(z0+z1)/2);m.rotation.y=-Math.atan2(z1-z0,x1-x0);const f=add(new THREE.BoxGeometry(L,.6,1.7),M(0x1d5fbf),(x0+x1)/2,2.4,(z0+z1)/2,false);f.rotation.y=m.rotation.y;};
 mauer(X(-Wd+1),Z(-Hd+1),X(Wd-1),Z(-Hd+1));mauer(X(-Wd+1),Z(-Hd+1),X(-Wd+1),Z(Hd-1));mauer(X(Wd-1),Z(-Hd+1),X(Wd-1),Z(Hd-1));mauer(X(-Wd+1),Z(Hd-1),X(-10),Z(Hd-1));mauer(X(10),Z(Hd-1),X(Wd-1),Z(Hd-1));
 for(const ex of[-10,10]){add(new THREE.BoxGeometry(2.4,5,2.4),M(0xf7f1e6),X(ex),2.5,Z(Hd-1));add(new THREE.SphereGeometry(1.4,10,8,0,TAU,0,Math.PI/2),M(0x1d5fbf),X(ex),5,Z(Hd-1));}
 // Haus
 const hx0=-27,hx1=10,hz0=-22,hz1=-6,hh=14;add(new THREE.BoxGeometry(hx1-hx0,hh,hz1-hz0),M(0xfff3e0),X((hx0+hx1)/2),hh/2,Z((hz0+hz1)/2));add(new THREE.BoxGeometry(hx1-hx0+1,1.6,hz1-hz0+1),M(0xc0392b),X((hx0+hx1)/2),hh+.8,Z((hz0+hz1)/2));
 // Fenster mit Drehspieß
 add(new THREE.BoxGeometry(20,9,.4),new THREE.MeshLambertMaterial({color:0x2f4a63}),X(-14),7,Z(hz1)+.1,false);const spiess=add(new THREE.CylinderGeometry(1.4,2.2,6.5,10),M(0x8a4a1e),X(-15),6.8,Z(hz1)-1.4);
 schild('DÖNER',X(-12),hh+5.5,Z(hz1)+.2,22,{fg:'#c0392b',bg:'#ffd23f',fs:80,round:true});
 schild('OFFEN',X(5),hh-3.5,Z(hz1)+.3,7,{fg:'#fff',bg:'#ff3d7f',fs:60});
 // Markise
 for(let k=0;k<8;k++){const m=add(new THREE.BoxGeometry(4.6,.3,4),M(k%2?0xffffff:0xe8433c),X(-24.7+k*4.6),hh-4.5,Z(hz1)+2,false);m.rotation.x=.35;}
 // Theke + Team
 add(new THREE.BoxGeometry(37,4.5,2.4),M(0x8a5a2b),X(-8.5),2.25,Z(hz1)+4);add(new THREE.BoxGeometry(37,.5,2.6),M(0xf4e3c0),X(-8.5),4.6,Z(hz1)+4,false);
 for(const [ox,c] of[[-21.5,0xffffff],[-8.5,0xffffff],[-1.5,0xffffff]])mensch(X(ox),Z(hz1)+1.6,0xe8433c,0x2a1b12,0);
 // Tische mit Schirmen
 for(const [tx,tz,uc] of[[24,-8,0xe8433c],[24,10,0xffd23f],[25,21,0x2fb3a0]]){add(new THREE.CylinderGeometry(2.6,2.6,.4,14),M(0x6b3f1d),X(tx),3.6,Z(tz));add(new THREE.CylinderGeometry(.3,.3,3.6,6),M(0x6b3f1d),X(tx),1.8,Z(tz));add(new THREE.CylinderGeometry(.2,.2,11,6),M(0xdddddd),X(tx),5.5,Z(tz));const sch=add(new THREE.ConeGeometry(6.5,2.4,10,1,true),M(uc,{side:THREE.DoubleSide}),X(tx),11.5,Z(tz));sch.rotation.z=.18;}
 // Roller, Kühlschrank, Pflanzen
 add(new THREE.BoxGeometry(6,3,2.4),M(0xe8433c),X(-24),2.6,Z(19));for(const o of[-2.6,2.6]){const r=add(new THREE.TorusGeometry(1,.4,6,12),M(0x2a2a2a),X(-24+o),1.2,Z(19));}add(new THREE.BoxGeometry(3.4,3,3.4),M(0xffffff),X(-26),5,Z(19));
 add(new THREE.BoxGeometry(4.8,10,4),M(0xf4f6f8),X(-34),5,Z(-8));
 for(const [px,pz] of[[-34,-18],[-34,16],[33,-20]]){add(new THREE.CylinderGeometry(1.6,1.2,2.6,8),M(0xb5651d),X(px),1.3,Z(pz));add(new THREE.SphereGeometry(2.4,9,7),leafM,X(px),3.6,Z(pz));}
 // Gäste
 mensch(X(17.5),Z(-8),0x3fa0e8,0x6b3f1d,Math.PI/2);mensch(X(30.5),Z(10),0x9b6bff,0xe0b860,-Math.PI/2);mensch(X(17.5),Z(10),0x2fb3a0,0x1a1a1a,Math.PI/2);mensch(X(-22),Z(3),0xff8a4c,0x2a1b12,Math.PI);}
// ---------- übrige Gebäude grob (für die Ferne) ----------
for(const g of W.geb){if(g.typ==='doener')continue;const col={strandbar:0xd9a066,villa:0xfffaf2,acai:0x7a3a8c,werkstatt:0xb85c3c}[g.typ]||0xdddddd;add(new THREE.BoxGeometry(30,12,16),M(col),g.cx,6,g.cy-6);}
for(const b of W.bau)if(!b.steg){add(new THREE.BoxGeometry(b.x1-b.x0-30,26,18),M(0xc9c2b5),b.cx,13,b.cy-6);add(new THREE.BoxGeometry(1.4,48,1.4),M(0xf0a500),b.cx+(b.x1-b.x0)*.31,24,b.cy+4);}
// Palast (rosa Muschel) in der Mitte
{const ps=W.palS;add(new THREE.CylinderGeometry(50*ps,52*ps,10,32),M(0xf6e2b8),MX,5,MY-4);const sh=add(new THREE.SphereGeometry(30*ps,24,16,0,TAU,0,Math.PI/2),M(0xf8a4bd),MX,10,MY-12);sh.scale.z=.6;add(new THREE.SphereGeometry(5*ps,14,10),M(0xffffff),MX,10+31*ps,MY-12);}

// ---------- Segelboote auf dem Meer (vor dem Strand am Ende der Route) ----------
const BOOTE=[];{const [ex,ez]=route[route.length-1],[bx0,bz0]=W.route.blick;for(let i=0;i<3;i++){const g=new THREE.Group();const rumpf=new THREE.Mesh(new THREE.BoxGeometry(14,2.6,4.4),M(0xfdfdf8));rumpf.position.y=.6;const streif=new THREE.Mesh(new THREE.BoxGeometry(14.2,.6,4.6),M(0x0a6fb0));streif.position.y=.2;
 const mast=new THREE.Mesh(new THREE.CylinderGeometry(.25,.25,18,6),M(0x6b4a2a));mast.position.y=10;const sg=new THREE.BufferGeometry();sg.setAttribute('position',new THREE.Float32BufferAttribute([0,19,0, 0,2.6,0, -8,2.6,0, 0,17,0, 0,2.6,0, 7,2.6,0],3));sg.computeVertexNormals();const segel=new THREE.Mesh(sg,new THREE.MeshLambertMaterial({color:i===1?0xffd23f:0xfff8ec,side:THREE.DoubleSide}));
 [rumpf,streif,mast,segel].forEach(m=>{m.castShadow=true;g.add(m);});const d2=110+i*70;g.position.set(ex+bx0*d2+(i-1)*70,0,ez+bz0*d2+(i-1)*12);S.add(g);BOOTE.push({g,i,x0:g.position.x});}}
// ---------- Passanten, die auf den Wegen laufen ----------
const LEUTE=[];{const farben=[[0xff6fa3,0x2a1b12],[0x3fa0e8,0xe0b860],[0xffd23f,0x6b3f1d],[0x2fb3a0,0x1a1a1a],[0x9b6bff,0xc8742a],[0xff8a4c,0x2a1b12],[0xe8433c,0x8a5a2b]];
 for(let i=0;i<7;i++){const [sh,ha]=farben[i];const g=mensch(0,0,sh,ha,0);LEUTE.push({g,seg:1+(i%(route.length-2)),u:hash(i,9),dir:i%2?1:-1,sp:5+hash(i,8)*2,off:(i%2?1:-1)*(2.2+hash(i,7)*.6)});}}
function leute(t){for(const L of LEUTE){const i=Math.min(route.length-1,L.seg+1),[ax,az]=route[L.seg],[bx2,bz2]=route[i],len=Math.hypot(bx2-ax,bz2-az)||1;let u=((L.u+L.dir*t*L.sp/len)%1+1)%1;const x=ax+(bx2-ax)*u,z=az+(bz2-az)*u,nx=-(bz2-az)/len,nz=(bx2-ax)/len;
  L.g.position.set(x+nx*L.off,Math.abs(Math.sin(t*6+L.u*9))*.25,z+nz*L.off);L.g.visible=Math.hypot(L.g.position.x-cam.position.x,L.g.position.z-cam.position.z)>9;L.g.rotation.y=Math.atan2((bx2-ax)*L.dir,(bz2-az)*L.dir);const legs=L.g.children;legs[1].rotation.x=Math.sin(t*6+L.u*9)*.5;legs[2].rotation.x=-Math.sin(t*6+L.u*9)*.5;}}
// ---------- Kamerafahrt in Augenhöhe ----------
const EYE=9.2,SPEED=+(P.get('tempo')||15);
// Route mit weichen Kurven
const pts=route.map(([x,z])=>new THREE.Vector3(x,EYE,z));const curve=new THREE.CatmullRomCurve3(pts,false,'centripetal',.2);const LEN=curve.getLength();
const T_START=2.2,T_GEHEN=LEN/SPEED,T_ENDE=4.5,DAUER=T_START+T_GEHEN+T_ENDE;window.DAUER=DAUER;
const [bx,bz]=W.route.blick;
function setT(t){leute(t);BOOTE.forEach(b=>{b.g.position.x=b.x0+Math.sin(t*.05+b.i)*20+t*(b.i%2?1.2:-1);b.g.rotation.z=Math.sin(t*1.3+b.i)*.04;b.g.position.y=Math.sin(t*1.1+b.i)*.3;});// Gischt + Wellen
 foam.forEach((l,k)=>{const ph=((t*.25+k/3)%1);l.material.opacity=.65*(1-ph);l.scale.setScalar(1+ph*.012);l.position.set(-MX*ph*.012,0,-MY*ph*.012);});
 let p,look;if(t<T_START){p=curve.getPointAt(0);const front=new THREE.Vector3(d.cx-8,EYE+1.5,d.cy-12);const go=curve.getTangentAt(.02);const k=Math.max(0,(t-T_START+1.2)/1.2),e=k*k*(3-2*k);look=front.lerp(new THREE.Vector3(p.x+go.x*20,EYE-1,p.z+go.z*20),e);}
 else if(t<T_START+T_GEHEN){const u=(t-T_START)/T_GEHEN,ue=u<.06?u*u/.12:u>.94?1-(1-u)*(1-u)/.12:u;const uu=Math.min(1,Math.max(0,ue));p=curve.getPointAt(uu);const tg=curve.getTangentAt(Math.min(.999,uu+.01));look=new THREE.Vector3(p.x+tg.x*25,EYE-1.2,p.z+tg.z*25);p.y=EYE+Math.abs(Math.sin(t*5.2))*.25;}
 else{p=curve.getPointAt(1);const k=Math.min(1,(t-T_START-T_GEHEN)/2),e=k*k*(3-2*k);const tg=curve.getTangentAt(.999);const a=new THREE.Vector3(p.x+tg.x*25,EYE-1.2,p.z+tg.z*25),b=new THREE.Vector3(p.x+bx*60,EYE-2.2,p.z+bz*60);look=a.lerp(b,e);}
 cam.position.copy(p);cam.lookAt(look);sun.position.set(p.x-60,140,p.z+80);sun.target.position.set(p.x,0,p.z-20);
 R.render(S,cam);}
window.setT=setT;setT(+(P.get('t')||0));
