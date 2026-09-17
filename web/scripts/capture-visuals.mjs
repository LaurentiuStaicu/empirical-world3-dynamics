import { chromium } from 'playwright';
import { spawn } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';

const out=resolve('visual-artifacts');
await mkdir(out,{recursive:true});
const server=spawn(process.platform==='win32'?'npm.cmd':'npm',['run','preview','--','--host','127.0.0.1','--port','4173'],{stdio:'inherit'});
async function ready(){for(let i=0;i<60;i++){try{const r=await fetch('http://127.0.0.1:4173');if(r.ok)return;}catch{}await new Promise(r=>setTimeout(r,500));}throw new Error('Preview server did not start.');}
const specs=[
  {name:'desktop-1920x1080',width:1920,height:1080},
  {name:'desktop-1600x900',width:1600,height:900},
  {name:'desktop-1440x900',width:1440,height:900},
  {name:'laptop-1366x768',width:1366,height:768},
  {name:'tablet-820x1180',width:820,height:1180},
  {name:'mobile-390x844',width:390,height:844},
];
const results=[];
function insideViewport(box,width,tolerance=2){return box.x>=-tolerance&&box.x+box.width<=width+tolerance;}
try{
  await ready();
  const browser=await chromium.launch({headless:true});
  for(const spec of specs){
    const page=await browser.newPage({viewport:{width:spec.width,height:spec.height}});
    await page.goto('http://127.0.0.1:4173',{waitUntil:'networkidle'});
    await page.locator('.trajectory-chart').waitFor();
    const overflow=await page.evaluate(()=>Math.max(document.documentElement.scrollWidth,document.body.scrollWidth)-window.innerWidth);
    if(overflow>2)throw new Error(`${spec.name}: horizontal document overflow ${overflow}px`);

    const selectors=['.product-header','.question-band','.trajectory-stage','.chart-product','.control-rail','.outlook-section','.analysis-section','.learn-strip'];
    for(const selector of selectors){
      const count=await page.locator(selector).count();
      for(let i=0;i<count;i++){
        const box=await page.locator(selector).nth(i).boundingBox();
        if(!box||!insideViewport(box,spec.width))throw new Error(`${spec.name}: ${selector}[${i}] leaves viewport`);
      }
    }
    const cards=page.locator('.timing-card');
    const cardCount=await cards.count();
    if(cardCount<7)throw new Error(`${spec.name}: expected at least 7 timing cards, got ${cardCount}`);
    for(let i=0;i<cardCount;i++){
      const box=await cards.nth(i).boundingBox();
      if(!box||!insideViewport(box,spec.width))throw new Error(`${spec.name}: timing card ${i} leaves viewport`);
    }

    const stage=await page.locator('.trajectory-stage').boundingBox(),chart=await page.locator('.chart-product').boundingBox(),rail=await page.locator('.control-rail').boundingBox();
    if(!stage||!chart||!rail)throw new Error(`${spec.name}: trajectory layout missing`);
    const ratio=chart.width/stage.width;
    if(spec.width>=1000&&(ratio<0.70||ratio>0.80))throw new Error(`${spec.name}: chart share ${ratio.toFixed(3)} outside 70–80% gate`);
    if(spec.width>=1000&&chart.x+chart.width>rail.x+2)throw new Error(`${spec.name}: chart and control rail overlap`);
    if(await page.locator('.trajectory-stage + .outlook-section').count()!==1)throw new Error(`${spec.name}: System Outlook is not directly below trajectory stage`);

    const sensitivityLabel=await page.locator('label.toggle').filter({hasText:'model sensitivity range'}).count();
    if(!sensitivityLabel)throw new Error(`${spec.name}: user-facing sensitivity label missing`);
    await page.locator('.sensitivity-control summary').click();
    const sensitivityText=await page.locator('.sensitivity-help').innerText();
    if(!sensitivityText.includes('80%')||!sensitivityText.includes('does not change')||!sensitivityText.includes('12 accepted'))throw new Error(`${spec.name}: sensitivity explanation incomplete`);

    await page.selectOption('#indicator','industry_per_capita');
    await page.waitForTimeout(50);
    const markerCount=await page.locator('.event-marker').count();
    if(markerCount<2)throw new Error(`${spec.name}: turning-point markers are not visible for industrial output per capita`);
    const chartBox=await page.locator('#chart-wrap').boundingBox();
    if(!chartBox)throw new Error(`${spec.name}: chart box missing`);
    for(const x of [chartBox.x+12,chartBox.x+chartBox.width-12]){
      await page.mouse.move(x,chartBox.y+Math.min(chartBox.height/2,180));
      await page.waitForTimeout(30);
      const tip=page.locator('.chart-tooltip:not([hidden])');
      if(await tip.count()){
        const box=await tip.boundingBox();
        if(!box||!insideViewport(box,spec.width))throw new Error(`${spec.name}: chart tooltip leaves viewport`);
      }
    }
    await page.mouse.move(0,0);

    const outlookText=await page.locator('.outlook-section').innerText();
    for(const required of ['System Outlook','Industrial','Food','Population'])if(!outlookText.includes(required))throw new Error(`${spec.name}: System Outlook missing ${required}`);
    const mainText=await page.locator('main').innerText();
    if(/S1–S10|candidate interfaces|structural contract|source-hashes/i.test(mainText))throw new Error(`${spec.name}: internal technical metadata leaked onto normal product surface`);

    await page.locator('#open-theory').click();
    await page.locator('#theory-dialog[open]').waitFor();
    const chapters=await page.locator('.manual-reader>section:not(.manual-home)').count();
    if(chapters<21)throw new Error(`${spec.name}: manual only has ${chapters} chapters`);
    const theoryText=await page.locator('.manual-reader').innerText();
    for(const required of ['Club of Rome','BAU Hybrid 2026','Nebel','corrigendum','Scenario'])if(!theoryText.includes(required))throw new Error(`${spec.name}: manual missing ${required}`);
    await page.locator('[data-close="theory"]').click();

    await page.locator('#open-evidence').click();
    await page.locator('#evidence-dialog[open]').waitFor();
    const evidenceText=await page.locator('#evidence-view').innerText();
    for(const required of ['Latin Hypercube','128','12','P10','RETAIN AS DIAGNOSTIC'])if(!evidenceText.includes(required))throw new Error(`${spec.name}: evidence audit missing ${required}`);
    await page.locator('[data-close="evidence"]').click();

    const bauToggle=page.locator('[data-scenario="original_bau"]');
    await bauToggle.uncheck();
    if(await page.locator('.series-bau').count())throw new Error(`${spec.name}: BAU toggle did not hide trajectory`);
    await bauToggle.check();

    await page.screenshot({path:resolve(out,`${spec.name}.png`),fullPage:true});
    results.push({viewport:spec,document_overflow_px:overflow,chart_share:Number(ratio.toFixed(3)),timing_cards:cardCount,event_markers:markerCount,manual_chapters:chapters,pass:true});
    await page.close();
  }
  await browser.close();
  await writeFile(resolve(out,'visual-audit.json'),JSON.stringify({gate:'PASS',requirements:['all six viewports','no horizontal overflow','no primary-panel overlap','tooltips inside viewport','chart 70–80% on desktop/laptop','System Outlook immediately follows graph','timing cards visible','full theory/evidence semantics'],results},null,2));
  console.log(JSON.stringify(results,null,2));
}finally{server.kill('SIGTERM');}
