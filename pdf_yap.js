// Kullanım: node pdf_yap.js girdi.html cikti.pdf [A4|A3|slayt]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [, , girdi, cikti, bicim = 'A4'] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage();
  await p.goto('file://' + path.resolve(girdi), { waitUntil: 'load' });
  await p.waitForTimeout(400);
  const ayar = bicim === 'slayt'
    ? { width: '1280px', height: '720px', printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 } }
    : { format: bicim, printBackground: true, preferCSSPageSize: true };
  await p.pdf({ path: cikti, ...ayar });
  await b.close();
  console.log(cikti, 'yazıldı');
})();
