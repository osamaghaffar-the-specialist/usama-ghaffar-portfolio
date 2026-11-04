import { chromium } from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';
const variants=[['main','http://127.0.0.1:8766/'],['optional','http://127.0.0.1:8765/']];
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const runs=[];
try {
 for(const [variant,url] of variants){
  for(let trial=1;trial<=3;trial++){
   const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
   const page=await context.newPage();const errors=[];page.on('pageerror',x=>errors.push(String(x)));
   await page.addInitScript(()=>{
    window.__clsEntries=[];
    try{new PerformanceObserver(list=>{
      for(const e of list.getEntries()) if(!e.hadRecentInput) window.__clsEntries.push({value:e.value,startTime:e.startTime,sources:(e.sources||[]).map(s=>({node:s.node?.tagName,previousRect:s.previousRect,currentRect:s.currentRect}))});
    }).observe({type:'layout-shift',buffered:true});}catch{}
   });
   try{
    const response=await page.goto(url,{waitUntil:'domcontentloaded',timeout:45000});
    await page.waitForTimeout(5500);
    if(trial===1) await page.screenshot({path:`font-cls-output/${variant}.png`});
    const metrics=await page.evaluate(()=>{
      const events=window.__clsEntries||[];
      return {clsTotal:events.reduce((sum,x)=>sum+x.value,0),events:events.slice(0,30),fontStatus:document.fonts.status,spaceGroteskReady:document.fonts.check('600 24px "Space Grotesk"'),h1Text:document.querySelector('h1')?.textContent.trim(),overflow:document.documentElement.scrollWidth>innerWidth};
    });
    runs.push({variant,trial,status:response?.status(),errors,...metrics});
   }catch(e){runs.push({variant,trial,error:String(e),errors});}
   await context.close();
  }
 }
}finally{await browser.close();}
const med=x=>{const s=x.slice().sort((a,b)=>a-b);return s.length?s[Math.floor(s.length/2)]:null};
const summary=Object.fromEntries(variants.map(([variant])=>{const x=runs.filter(r=>r.variant===variant&&!r.error);return [variant,{valid:x.length,medianCls:med(x.map(y=>y.clsTotal)),errors:x.reduce((sum,z)=>sum+z.errors.length,0),fontReady:x.map(z=>z.spaceGroteskReady),overflow:x.some(z=>z.overflow)}]}));
await writeFile('font-cls-output/report.json',JSON.stringify({summary,runs,caveats:['Browser-only CLS observation, not Chrome UX Report field CWV','font-display optional can retain fallback font on slow networks; typography appearance may differ','A/B variants serve the same main and PR content on separate localhost ports; third-party fonts and browser cache may vary']},null,2));
console.log(JSON.stringify(summary,null,2));
if(runs.some(r=>r.error||r.status!==200||r.errors.length)) process.exitCode=1;
