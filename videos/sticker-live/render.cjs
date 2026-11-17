const {chromium}=require('playwright');const fs=require('fs');(async()=>{const d=process.argv[2];const b=await chromium.launch();const p=await b.newPage({viewport:{width:600,height:600},deviceScaleFactor:1});
for(const f of fs.readdirSync(d).filter(f=>f.endsWith('.html')).sort()){await p.goto('file://'+d+'/'+f);await p.waitForTimeout(300);await p.screenshot({path:d+'/'+f.replace('.html','.png'),omitBackground:true});}
await b.close();})();
