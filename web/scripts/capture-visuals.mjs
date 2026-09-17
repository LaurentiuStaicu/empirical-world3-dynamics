import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const out=resolve('visual-artifacts');
await mkdir(out,{recursive:true});
const server=spawn(process.platform==='win32'?'npm.cmd':'npm',['run','preview','--','--host','127.0.0.1','--port','4173'],{stdio:'inherit'});
const specs=[['desktop-1920x1080',1920,1080],['desktop-1600x900',1600,900],['desktop-1440x900',1440,900],['laptop-1366x768',1366,768],['tablet-820x1180',820,1180],['mobile-390x844',390,844]];
const results=[];
const wait=ms=>new Promise(r=>setTimeout(r,ms));
async function ready(){for(let i=0;i<60;i++){try{if((await fetch('http://127.0.0.1:4173')).ok)return;}catch{}await wait(500);}throw new Error('Preview server did not start');}
const inside=(box,width,tol=2)=>box&&box.x>=-tol&&box.x+box.width<=width+tol;
try{
  await ready();
  const browser=await chromium.launch({headless:true});
  for(const [name,width,height] of specs){
    const page=await browser.newPage({viewport:{width,height}});
    await page.goto('http://127.0.0.1:4173',{waitUntil:'networkidle'});
    await page.locator('.trajectory-chart').waitFor();
    const overflow=await page.evaluate(()=>Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-innerWidth);
    if(overflow>2)throw new Error(`${name}: horizontal overflow ${overflow}px`);
    for(const selector of ['.product-header','.question-band','.trajectory-stage','.chart-product','.control-rail','.outlook-section','.analysis-section','.learn-strip']){
      const loc=page.locator(selector),count=await loc.count();
      for(let i=0;i<count;i++)if(!inside(await loc.nth(i).boundingBox(),width))throw new Error(`${name}: ${selector}[${i}] leaves viewport`);
    }
    const cards=page.locator('.timing-card'),cardCount=await cards.count();
    if(cardCount<7)throw new Error(`${name}: only ${cardCount} timing cards`);
    for(let i=0;i<cardCount;i++)if(!inside(await cards.nth(i).boundingBox(),width))throw new Error(`${name}: timing card ${i} leaves viewport`);
    const stage=await page.locator('.trajectory-stage').boundingBox(),chart=await page.locator('.chart-product').boundingBox(),rail=await page.locator('.control-rail').boundingBox();
    if(!stage||!chart||!rail)throw new Error(`${name}: trajectory layout missing`);
    const ratio=chart.width/stage.width;
    if(width>=1000&&(ratio<.70||ratio>.80))throw new Error(`${name}: chart share ${ratio.toFixed(3)} outside 70–80%`);
    if(width>=1000&&chart.x+chart.width>rail.x+2)throw new Error(`${name}: chart/control overlap`);
    if(await page.locator('.trajectory-stage + .outlook-section').count()!==1)throw new Error(`${name}: System Outlook not directly below chart stage`);

    const sensitivity=page.locator('label.toggle').filter({hasText:'model sensitivity range'});
    if(await sensitivity.count()!==1)throw new Error(`${name}: sensitivity control label missing`);
    await page.locator('.sensitivity-control summary').click();
    const help=await page.locator('.sensitivity-help').innerText();
    for(const token of ['80%','does not change','12 accepted'])if(!help.includes(token))throw new Error(`${name}: sensitivity explanation missing ${token}`);

    await page.selectOption('#indicator','industry_per_capita');await wait(60);
    const markerCount=await page.locator('.event-marker').count();
    if(markerCount<2)throw new Error(`${name}: fewer than two calculated event markers`);
    const chartBox=await page.locator('#chart-wrap').boundingBox();
    if(!chartBox)throw new Error(`${name}: chart box missing`);
    for(const px of [chartBox.x+12,chartBox.x+chartBox.width-12]){
      await page.mouse.move(px,chartBox.y+Math.min(chartBox.height/2,180));await wait(30);
      const tip=page.locator('.chart-tooltip:not([hidden])');
      if(await tip.count()&&!inside(await tip.boundingBox(),width))throw new Error(`${name}: tooltip leaves viewport`);
    }
    await page.mouse.move(0,0);
    const outlookText=await page.locator('.outlook-section').innerText();
    for(const token of ['System Outlook','Industrial','Food','Population'])if(!outlookText.includes(token))throw new Error(`${name}: System Outlook missing ${token}`);
    const normalText=await page.locator('main').innerText();
    if(/S1–S10|candidate interfaces|structural contract|source-hashes/i.test(normalText))throw new Error(`${name}: internal metadata leaked into normal UI`);

    await page.locator('#open-theory').click();await page.locator('#theory-dialog[open]').waitFor();
    const chapters=await page.locator('.manual-reader>section:not(.manual-home)').count();
    if(chapters<21)throw new Error(`${name}: manual only has ${chapters} chapters`);
    const theory=await page.locator('.manual-reader').innerText();
    for(const token of ['Club of Rome','BAU Hybrid 2026','Nebel','corrigendum','Scenario'])if(!theory.includes(token))throw new Error(`${name}: theory missing ${token}`);
    await page.locator('[data-close="theory"]').click();

    await page.locator('#open-evidence').click();await page.locator('#evidence-dialog[open]').waitFor();
    const technical=page.locator('.technical-provenance');
    if(await technical.count()===1&&!await technical.getAttribute('open'))await technical.locator('summary').click();
    const evidence=await page.locator('#evidence-view').innerText();
    for(const token of ['Latin Hypercube','128','12','P10','RETAIN AS DIAGNOSTIC'])if(!evidence.includes(token))throw new Error(`${name}: evidence audit missing ${token}`);
    await page.locator('[data-close="evidence"]').click();

    const bau=page.locator('[data-scenario="original_bau"]');await bau.uncheck();if(await page.locator('.series-bau').count())throw new Error(`${name}: BAU toggle failed`);await bau.check();
    await page.screenshot({path:resolve(out,`${name}.png`),fullPage:true});
    results.push({viewport:{width,height},document_overflow_px:overflow,chart_share:Number(ratio.toFixed(3)),timing_cards:cardCount,event_markers:markerCount,manual_chapters:chapters,pass:true});
    await page.close();
  }
  await browser.close();
  await writeFile(resolve(out,'visual-audit.json'),JSON.stringify({gate:'PASS',results},null,2));
  console.log(JSON.stringify(results,null,2));
}finally{server.kill('SIGTERM');}
