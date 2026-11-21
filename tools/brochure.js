// Renders tools/brochure.html to assets/frisson-writing-profile.pdf (needs Playwright)
const {chromium}=require('playwright'); const path=require('path');
(async()=>{const root=path.resolve(__dirname,'..');const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://'+root+'/tools/brochure.html');await p.waitForTimeout(800);
await p.pdf({path:root+'/assets/frisson-writing-profile.pdf',format:'A4',printBackground:true,pageRanges:'1'});
await b.close()})();
