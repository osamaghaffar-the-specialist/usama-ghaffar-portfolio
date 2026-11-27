import { chromium } from 'playwright';

const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const page=await browser.newPage({viewport:{width:390,height:844}});
try {
  await page.route('https://www.googletagmanager.com/**', route=>route.abort());
  const events=async ()=>page.evaluate(()=>(window.dataLayer||[])
    .filter(item=>item && item[0]==='event')
    .map(item=>({name:item[1],details:item[2]||{}})));
  const count=(rows,name)=>rows.filter(row=>row.name===name).length;
  async function fill(){
    await page.locator('#fullName').fill('Example Tester');
    await page.locator('#workEmail').fill('test@example.invalid');
    await page.locator('#projectType').selectOption({label:'SEO / organic growth'});
    await page.locator('#projectBrief').fill('Mock project for automated offline browser checks.');
  }
  // Intercept all contact form requests: never transmit a real lead.
  await page.route('https://api.web3forms.com/submit',route=>route.fulfill({
    status:200,contentType:'application/json',body:JSON.stringify({success:true})
  }));
  await page.goto('http://127.0.0.1:8765/contact.html?service=seo#project-brief',{waitUntil:'domcontentloaded'});
  await page.locator('#fullName').focus();
  await page.locator('#fullName').blur();
  let rows=await events();
  if(count(rows,'project_brief_start')!==1)throw Error('Expected one focus start event');
  await page.locator('#contactForm button[type=submit]').click();
  rows=await events();
  if(count(rows,'project_brief_validation_error')!==1)throw Error('Expected invalid submission event');
  if(count(rows,'generate_lead')!==0)throw Error('Invalid form counted as lead');
  await fill();
  await page.locator('#contactForm button[type=submit]').click();
  await page.locator('#formMessage.success').waitFor();
  rows=await events();
  if(count(rows,'generate_lead')!==1)throw Error('Confirmed response must count exactly one lead');
  if(count(rows,'project_brief_submission_error')!==0)throw Error('Success counted as delivery error');
  if(rows.some(e=>JSON.stringify(e.details).includes('test@example.invalid')||
                  JSON.stringify(e.details).includes('Mock project')))throw Error('PII leaked into analytics');
  await page.unroute('https://api.web3forms.com/submit');
  await page.route('https://api.web3forms.com/submit',route=>route.fulfill({
    status:503,contentType:'application/json',body:JSON.stringify({success:false,message:'Offline test failure'})
  }));
  await page.reload({waitUntil:'domcontentloaded'});
  await fill();
  await page.locator('#contactForm button[type=submit]').click();
  await page.locator('#formMessage.error').waitFor();
  rows=await events();
  if(count(rows,'project_brief_submission_error')!==1)throw Error('Failed delivery not captured');
  if(count(rows,'generate_lead')!==0)throw Error('Failed delivery counted as lead');
  console.log('PASS: form start, invalid, confirmed success, simulated delivery error; no PII in events.');
}finally{await browser.close();}
