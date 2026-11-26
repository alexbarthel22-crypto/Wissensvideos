// Tag 14: Innenansicht Sunken Pearl (Tiefsee-Suite) + Muschel-Möwe als Bildfolge aus dem Homepage-Code
// node extras.cjs <site/index.html> <out-dir>
const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const [site,out]=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:405,height:720},deviceScaleFactor:3});await p.clock.install({time:new Date('2026-11-24T14:10:00+01:00')});
await p.goto('file://'+site+'?zeit=tag&wetter=sonne');await p.clock.runFor(7000);
await p.evaluate(()=>{const q=PEOPLE.find(x=>x.p&&x.isl===MAIN);const f=Object.assign({},q,{isl:SPV,name:'Sunken Pearl',L:null});huetteRein(f);});
await p.clock.runFor(1500);await p.addStyleTag({content:'*{visibility:hidden!important} #hinnen,#hinnen *{visibility:visible!important}'});await p.clock.runFor(300);
await p.locator('#hicv').screenshot({path:out+'/innen.png'});
const fr=await p.evaluate(()=>{const R=[];for(let i=0;i<8;i++){const c=document.createElement('canvas');c.width=520;c.height=300;const x=c.getContext('2d');x.scale(10,10);mwVogel(x,26,15,1,i/8*(Math.PI*2/9),true,1);R.push(c.toDataURL('image/png'));}return R;});
fr.forEach((u,i)=>fs.writeFileSync(out+'/moewe/m'+i+'.png',Buffer.from(u.split(',')[1],'base64')));
await b.close();console.log('ok');})();
