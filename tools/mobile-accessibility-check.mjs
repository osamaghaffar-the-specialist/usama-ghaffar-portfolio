import {chromium} from 'playwright';
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const errors=[];
try{
 const page=await browser.newPage({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 page.on('pageerror',e=>errors.push(String(e)));
 const response=await page.goto('http://127.0.0.1:8765/',{waitUntil:'domcontentloaded',timeout:45000});
 if(response?.status()!==200)throw Error('Homepage HTTP status '+response?.status());
 const menu=page.locator('#mobileMenu'),toggle=page.locator('#menuToggle');
 if(await menu.getAttribute('aria-hidden')!=='true'||!await menu.evaluate(n=>n.inert))throw Error('Closed menu must be aria-hidden and inert');
 await toggle.click();
 if(await menu.getAttribute('aria-hidden')!=='false'||await menu.evaluate(n=>n.inert))throw Error('Open menu must be accessible');
 if(await toggle.getAttribute('aria-expanded')!=='true')throw Error('Toggle aria-expanded should be true');
 await page.keyboard.press('Escape');
 if(await menu.getAttribute('aria-hidden')!=='true'||!await menu.evaluate(n=>n.inert))throw Error('Escape must close and inert the menu');
 if(await toggle.getAttribute('aria-expanded')!=='false')throw Error('Toggle aria-expanded should be false');
 const accessible=await page.evaluate(()=>{
  const links=[...document.querySelectorAll('p.lead a[aria-label]')];
  return links.every(a=>a.getAttribute('aria-label').trim()===a.textContent.trim());
 });
 if(!accessible)throw Error('Inline hero link labels must equal visible text');
 if(errors.length)throw Error('Browser errors: '+errors.join('; '));
 console.log('PASS: mobile menu inert/ARIA state, Escape, inline labels, no browser errors');
}finally{await browser.close();}
