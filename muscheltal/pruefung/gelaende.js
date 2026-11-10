// Aufruf: python3 muscheltal/bau.py && node muscheltal/pruefung/gelaende.js  – "taschen" sollte je Laden nahe 0 sein (nur schmale Randspalten)
// Prüft je Laden-Gelände: welche begehbaren Flächen vom Eingang aus mit Körperbreite erreichbar sind (Sackgassen/Taschen)
const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));await p.goto('file://'+require('path').resolve(__dirname,'../site/index.html')+'?zeit=tag');await p.waitForTimeout(2500);
const r=await p.evaluate(()=>{canWalk(0,0);const out=[];
 for(const g of GEB){if(!g.typ||g.typ==='huette')continue;const W=(g.x1-g.x0)/2,H=(g.y1-g.y0)/2,st=1,M=8,x0=g.x0-M,y0=g.y0-M,nx=Math.ceil((2*W+2*M)/st),ny=Math.ceil((2*H+2*M)/st);
  const A=new Uint8Array(nx*ny);for(let i=0;i<nx;i++)for(let j=0;j<ny;j++)A[i*ny+j]=canWalk(x0+i*st,y0+j*st)?1:0;
  const R=1;const C=new Uint8Array(nx*ny);for(let i=R;i<nx-R;i++)for(let j=R;j<ny-R;j++){let ok=1;for(let a=-R;a<=R&&ok;a++)for(let c2=-R;c2<=R;c2++)if(!A[(i+a)*ny+j+c2]){ok=0;break;}C[i*ny+j]=ok;}
  const fl=(M2)=>{const S2=new Uint8Array(nx*ny),q=[];for(let i=0;i<nx;i++)for(let j=0;j<ny;j++){const x=x0+i*st,y=y0+j*st,inside=x>g.x0&&x<g.x1&&y>g.y0&&y<g.y1;if(!inside&&M2[i*ny+j]){S2[i*ny+j]=1;q.push(i*ny+j);}}
   while(q.length){const c=q.pop(),i=(c/ny)|0,j=c%ny;for(const [di,dj] of[[1,0],[-1,0],[0,1],[0,-1]]){const a=i+di,b2=j+dj;if(a<0||b2<0||a>=nx||b2>=ny)continue;const k=a*ny+b2;if(M2[k]&&!S2[k]){S2[k]=1;q.push(k);}}}return S2;};
  const RC=fl(C);// mit Körperbreite erreichbar; ein Rohpunkt gilt als erreichbar, wenn ein erreichbarer Körpermittelpunkt in Reichweite R liegt
  let tot=0,walk=0,reach=0;const lost=[];for(let i=0;i<nx;i++)for(let j=0;j<ny;j++){const x=x0+i*st,y=y0+j*st;if(!(x>g.x0+1&&x<g.x1-1&&y>g.y0+1&&y<g.y1-1))continue;tot++;if(!A[i*ny+j])continue;walk++;let ok=0;for(let a=-R;a<=R&&!ok;a++)for(let c2=-R;c2<=R;c2++){const ii=i+a,jj=j+c2;if(ii>=0&&jj>=0&&ii<nx&&jj<ny&&RC[ii*ny+jj]){ok=1;break;}}if(ok)reach++;else lost.push([Math.round(x-g.cx),Math.round(y-g.cy)]);}
  out.push({typ:g.typ,name:g.name,dir:g.dir||1,begehbar:Math.round(100*walk/tot)+'%',erreichbar:Math.round(100*reach/tot)+'%',taschen:lost.length,bsp:lost.filter((_,i)=>i%6==0).slice(0,25)});}
 return out;});
for(const o of r)console.log(JSON.stringify(o));console.log(errs);await b.close();})();
