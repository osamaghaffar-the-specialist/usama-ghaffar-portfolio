import { chromium } from 'playwright';
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
try{
 const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 const response=await page.goto('http://127.0.0.1:8765/ecommerce-agency-pakistan.html',{waitUntil:'domcontentloaded'});
 if(response?.status()!==200)throw Error('Page did not load');
 await page.evaluate(()=>{
  window.__ctaEvents=[];
  window.gtag=(...args)=>window.__ctaEvents.push(args);
  document.addEventListener('click',e=>{if(e.target.closest('a[href="contact.html?service=ecommerce#project-brief"]'))e.preventDefault();},true);
 });
 const ctas=page.locator('a[href="contact.html?service=ecommerce#project-brief"]');
 const count=await ctas.count();
 if(count<1)throw Error('Consultation CTA missing');
 await page.locator('.hero-actions a[href="contact.html?service=ecommerce#project-brief"]').click({noWaitAfter:true});
 const events=await page.evaluate(()=>window.__ctaEvents);
 const matches=events.filter(x=>x[0]==='event'&&x[1]==='contact_cta_click'&&x[2]?.source_page==='ecommerce_agency_pakistan'&&x[2]?.lead_status==='click_intent_only');
 if(matches.length!==1)throw Error('Expected exactly one click-intent event, got '+JSON.stringify(events));
 if(errors.length)throw Error('Page errors: '+errors.join('; '));
 console.log('PASS: consultation CTA sends one anonymous intent-only event; '+count+' project brief links present');
}finally{await browser.close();}
