import {chromium} from 'playwright';
import {mkdir,writeFile} from 'node:fs/promises';

const tests=[
 {name:'main-local-baseline',url:'http://127.0.0.1:8766/'},
 {name:'pr-local-preview',url:'http://127.0.0.1:8765/'},
];
await mkdir('hero-review-output',{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const results=[];
try{
 for(const test of tests){
  for(let trial=1;trial<=3;trial++){
   const context=await browser.newContext({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true,reducedMotion:'no-preference'});
   const page=await context.newPage();
   const errors=[];
   page.on('pageerror',e=>errors.push(String(e).slice(0,350)));
   await page.addInitScript(()=>{
    window.__heroReviewTasks=[];
    try{new PerformanceObserver(list=>{for(const e of list.getEntries())window.__heroReviewTasks.push(Math.round(e.duration));}).observe({type:'longtask',buffered:true});}catch{}
   });
   try{
    const response=await page.goto(test.url,{waitUntil:'domcontentloaded',timeout:45000});
    await page.waitForTimeout(8000);
    if(trial===1)await page.screenshot({path:`hero-review-output/${test.name}-mobile.png`,fullPage:false});
    const report=await page.evaluate(()=>{
      const arr=window.__heroReviewTasks||[];
      const canvas=document.getElementById('beeCanvas');
      return {
        longTaskTotalMs:arr.reduce((sum,n)=>sum+n,0),
        longTaskCount:arr.length,
        heroCanvasPresent:!!canvas,
        heroCanvasSize:canvas?{width:canvas.width,height:canvas.height}:null,
        horizontalOverflow:document.documentElement.scrollWidth>innerWidth,
        title:document.title
      };
    });
    results.push({test:test.name,trial,status:response?.status(),errors,...report});
   }catch(e){results.push({test:test.name,trial,error:String(e),errors});}
   await context.close();
  }
 }
}finally{await browser.close();}
const median=values=>{const s=[...values].sort((a,b)=>a-b);return s.length?s[Math.floor(s.length/2)]:null;};
const summary=Object.fromEntries(tests.map(t=>{const rows=results.filter(x=>x.test===t.name&&!x.error);return [t.name,{successful:rows.length,medianLongTaskTotalMs:median(rows.map(r=>r.longTaskTotalMs)),pageErrorCount:rows.reduce((n,r)=>n+r.errors.length,0),heroCanvasPresent:rows.every(r=>r.heroCanvasPresent),horizontalOverflow:rows.some(r=>r.horizontalOverflow)}];}));
const caveats=['Both variants are served locally from main and the PR branch; external Google Fonts and Three.js may still vary due to network and cache.','PerformanceObserver long-task duration is NOT Lighthouse TBT and does not establish Core Web Vitals gains.','Inspect screenshots manually for hero visual regressions. This script never sends forms or clicks outbound links.'];
await writeFile('hero-review-output/results.json',JSON.stringify({created:new Date().toISOString(),summary,results,caveats},null,2));
console.log(JSON.stringify(summary,null,2));
if(results.some(r=>r.error||r.status!==200||r.errors.length))process.exitCode=1;
