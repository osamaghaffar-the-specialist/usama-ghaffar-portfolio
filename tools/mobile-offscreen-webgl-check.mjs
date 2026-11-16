import {chromium} from 'playwright';
import {mkdir} from 'node:fs/promises';

await mkdir('hero-review-output',{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
const errors=[];
page.on('pageerror',err=>errors.push(String(err)));
try{
  const response=await page.goto('http://127.0.0.1:8765/',{waitUntil:'domcontentloaded',timeout:45000});
  if(response?.status()!==200)throw new Error('Homepage did not load');

  const service=page.locator('canvas.miniBee').first();
  if(await service.count()===0)throw new Error('Service bee canvas missing');
  const initial=await service.evaluate(el=>({width:el.width,height:el.height}));
  await service.scrollIntoViewIfNeeded();
  await page.waitForTimeout(1300);
  const serviceSize=await service.evaluate(el=>({width:el.width,height:el.height,clientWidth:el.clientWidth,clientHeight:el.clientHeight}));
  if(serviceSize.clientWidth>0 && (serviceSize.width===initial.width && serviceSize.height===initial.height)){
    throw new Error('Service bee renderer did not initialize after scrolling into view');
  }
  await page.screenshot({path:'hero-review-output/service-bee-after-scroll.png'});

  const section=page.locator('#featured-work');
  if(await section.count()===0)throw new Error('Featured work section missing');
  const roam=page.locator('#roamBee canvas');
  if(await roam.count()===0)throw new Error('Featured roaming bee canvas missing');
  const roamingInitial=await roam.evaluate(el=>({width:el.width,height:el.height}));
  await section.scrollIntoViewIfNeeded();
  await page.waitForTimeout(1300);
  const roamingSize=await roam.evaluate(el=>({width:el.width,height:el.height,clientWidth:el.clientWidth,clientHeight:el.clientHeight}));
  if(roamingSize.clientWidth>0 && (roamingSize.width===roamingInitial.width && roamingSize.height===roamingInitial.height)){
    throw new Error('Featured bee renderer did not initialize after scrolling into view');
  }
  await page.screenshot({path:'hero-review-output/featured-bee-after-scroll.png'});
  if(errors.length)throw new Error('Browser errors: '+errors.join('; '));
  console.log('PASS: mobile below-fold bee scenes initialize after scrolling',JSON.stringify({serviceSize,roamingSize}));
} finally{
  await browser.close();
}
