const { chromium } = require('playwright');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1080, height: 1080 } });
  await p.goto('file://' + __dirname + '/index.html'); await p.waitForTimeout(500);
  await p.screenshot({ path: __dirname + '/profilbild.png' }); await b.close(); })();
