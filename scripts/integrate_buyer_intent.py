from pathlib import Path

blocks = {
    'index.html': '''
<section id="buyer-intent-digital" aria-labelledby="buyer-intent-digital-title" style="padding:72px 24px;background:#f7f8fa;border-top:1px solid rgba(11,14,20,.08)">
  <div style="max-width:1080px;margin:0 auto">
    <p style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 12px;color:#5b4fe8;font-weight:700">Pakistan Growth Partner</p>
    <h2 id="buyer-intent-digital-title" style="font-size:clamp(30px,4vw,48px);line-height:1.08;margin:0 0 18px">Digital marketing services built to turn search demand into leads and sales</h2>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0 0 16px">Bee Marketing works as a <strong>digital marketing agency in Pakistan</strong> for ecommerce and service businesses that need measurable acquisition, better conversion rates and clearer revenue tracking. Businesses comparing a <strong>digital marketing company in Pakistan</strong> or <strong>digital marketing services in Pakistan</strong> can use our specialist service pages to match the right channel to the right growth problem.</p>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0">For Lahore and nationwide brands, start with our <a href="ecommerce-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">ecommerce growth strategy</a>, <a href="facebook-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Meta and Facebook Ads service</a>, or <a href="google-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Google Ads and PPC service</a>.</p>
  </div>
</section>
''',
    'ecommerce-agency-pakistan.html': '''
<section id="buyer-intent-ecommerce" aria-labelledby="buyer-intent-ecommerce-title" style="padding:72px 24px;background:#f7f8fa;border-top:1px solid rgba(11,14,20,.08)">
  <div style="max-width:1080px;margin:0 auto">
    <p style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 12px;color:#5b4fe8;font-weight:700">Ecommerce Growth</p>
    <h2 id="buyer-intent-ecommerce-title" style="font-size:clamp(30px,4vw,48px);line-height:1.08;margin:0 0 18px">Ecommerce marketing for Shopify and D2C brands in Pakistan</h2>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0 0 16px">If you are looking for an <strong>ecommerce marketing agency in Pakistan</strong> or an <strong>ecommerce growth agency in Pakistan</strong>, the goal should be profitable customer acquisition rather than traffic alone. Bee Marketing combines paid media, CRO, creative testing, analytics and landing-page improvements around one commercial growth plan.</p>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0">We also support brands searching for a <strong>Shopify marketing agency in Pakistan</strong> or a <strong>D2C marketing agency in Pakistan</strong>. Paid acquisition is connected directly to our <a href="facebook-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Meta Ads for ecommerce</a> and <a href="google-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Google Ads for ecommerce</a> services.</p>
  </div>
</section>
''',
    'facebook-ads-agency-pakistan.html': '''
<section id="buyer-intent-meta" aria-labelledby="buyer-intent-meta-title" style="padding:72px 24px;background:#f7f8fa;border-top:1px solid rgba(11,14,20,.08)">
  <div style="max-width:1080px;margin:0 auto">
    <p style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 12px;color:#5b4fe8;font-weight:700">Meta Acquisition</p>
    <h2 id="buyer-intent-meta-title" style="font-size:clamp(30px,4vw,48px);line-height:1.08;margin:0 0 18px">Meta and Facebook Ads management for ecommerce growth</h2>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0 0 16px">Bee Marketing is positioned as a <strong>Meta Ads agency for ecommerce</strong> brands that need more than campaign setup. We connect audience testing, creative testing, offer strategy, tracking and conversion improvements so ad spend can be judged against qualified leads and profitable sales.</p>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0">For businesses comparing a <strong>Facebook Ads agency for ecommerce</strong>, <strong>Facebook Ads management in Pakistan</strong> or <strong>Meta Ads management in Pakistan</strong>, our approach is built around measurable acquisition. Ecommerce brands can also pair this with our <a href="ecommerce-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">ecommerce growth service</a> and <a href="google-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Google Ads service</a>.</p>
  </div>
</section>
''',
    'google-ads-agency-pakistan.html': '''
<section id="buyer-intent-google" aria-labelledby="buyer-intent-google-title" style="padding:72px 24px;background:#f7f8fa;border-top:1px solid rgba(11,14,20,.08)">
  <div style="max-width:1080px;margin:0 auto">
    <p style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 12px;color:#5b4fe8;font-weight:700">High-Intent Search</p>
    <h2 id="buyer-intent-google-title" style="font-size:clamp(30px,4vw,48px);line-height:1.08;margin:0 0 18px">Google Ads and PPC management for high-intent demand</h2>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0 0 16px">For brands that need a <strong>Google Ads agency for ecommerce</strong> or <strong>Google Ads management in Pakistan</strong>, we focus on search intent, keyword economics, negative-keyword control, landing-page relevance and accurate conversion tracking instead of optimizing only for clicks.</p>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0">Our <strong>PPC management services in Pakistan</strong> can cover Search, Shopping and remarketing, including businesses evaluating a <strong>Google Shopping Ads agency in Pakistan</strong>. For full-funnel growth, combine paid search with our <a href="facebook-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Meta Ads service</a> and <a href="performance-marketing-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">performance marketing strategy</a>.</p>
  </div>
</section>
''',
    'performance-marketing-agency-pakistan.html': '''
<section id="buyer-intent-performance" aria-labelledby="buyer-intent-performance-title" style="padding:72px 24px;background:#f7f8fa;border-top:1px solid rgba(11,14,20,.08)">
  <div style="max-width:1080px;margin:0 auto">
    <p style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 12px;color:#5b4fe8;font-weight:700">Profitable Scale</p>
    <h2 id="buyer-intent-performance-title" style="font-size:clamp(30px,4vw,48px);line-height:1.08;margin:0 0 18px">Performance marketing for brands that need measurable growth</h2>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0 0 16px">As an <strong>ecommerce performance marketing agency in Pakistan</strong>, Bee Marketing connects paid media, CRO, creative testing and analytics to business outcomes. Brands comparing a <strong>performance marketing company in Pakistan</strong> should be able to see where spend goes, what converts and what should be scaled next.</p>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0">Our model also fits companies searching for a <strong>paid media agency in Pakistan</strong> or a <strong>growth marketing agency in Pakistan</strong>. Channel execution is supported by our <a href="facebook-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Meta Ads</a>, <a href="google-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Google Ads</a> and <a href="ecommerce-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">ecommerce growth</a> services.</p>
  </div>
</section>
''',
    'seo-agency-pakistan.html': '''
<section id="buyer-intent-seo" aria-labelledby="buyer-intent-seo-title" style="padding:72px 24px;background:#f7f8fa;border-top:1px solid rgba(11,14,20,.08)">
  <div style="max-width:1080px;margin:0 auto">
    <p style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 12px;color:#5b4fe8;font-weight:700">Commercial SEO</p>
    <h2 id="buyer-intent-seo-title" style="font-size:clamp(30px,4vw,48px);line-height:1.08;margin:0 0 18px">SEO for ecommerce and Shopify brands that want qualified organic demand</h2>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0 0 16px">Bee Marketing supports businesses searching for an <strong>ecommerce SEO agency in Pakistan</strong>, an <strong>SEO agency for ecommerce</strong> or a <strong>Shopify SEO agency in Pakistan</strong>. The strategy prioritizes commercial keyword clusters, technical health, category and service-page relevance, internal linking, content authority and trusted backlinks.</p>
    <h3 style="font-size:24px;line-height:1.25;margin:28px 0 10px">How should you choose the best SEO agency in Pakistan?</h3>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0">Look for clear keyword-to-page mapping, transparent reporting, technical competence and a plan tied to qualified leads rather than vanity traffic. For broader acquisition, SEO can work alongside our <a href="ecommerce-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">ecommerce marketing</a> and <a href="google-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Google Ads</a> services.</p>
  </div>
</section>
''',
    'web-development-agency-pakistan.html': '''
<section id="buyer-intent-webdev" aria-labelledby="buyer-intent-webdev-title" style="padding:72px 24px;background:#f7f8fa;border-top:1px solid rgba(11,14,20,.08)">
  <div style="max-width:1080px;margin:0 auto">
    <p style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;margin:0 0 12px;color:#5b4fe8;font-weight:700">Conversion-Focused Development</p>
    <h2 id="buyer-intent-webdev-title" style="font-size:clamp(30px,4vw,48px);line-height:1.08;margin:0 0 18px">Website development for ecommerce and growth-focused businesses</h2>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0 0 16px">Businesses looking for an <strong>ecommerce web development agency in Pakistan</strong> or a <strong>website development agency in Pakistan</strong> need more than a good-looking site. We build around speed, SEO structure, conversion paths, analytics and marketing integrations so the website can support acquisition from day one.</p>
    <p style="font-size:18px;line-height:1.75;color:#4b5160;margin:0">We also support brands evaluating a <strong>Shopify development agency in Pakistan</strong> or an <strong>ecommerce website development company in Pakistan</strong>. Once the site is ready, growth can connect directly to our <a href="ecommerce-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">ecommerce marketing</a>, <a href="facebook-ads-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">Meta Ads</a> and <a href="seo-agency-pakistan.html" style="color:#5b4fe8;text-decoration:underline">SEO</a> services.</p>
  </div>
</section>
'''
}

for file_name, block in blocks.items():
    path = Path(file_name)
    text = path.read_text(encoding='utf-8')
    marker_id = block.split('id="', 1)[1].split('"', 1)[0]
    if f'id="{marker_id}"' in text:
        print(f'{file_name}: already present')
        continue
    lower = text.lower()
    insert_at = lower.find('<footer')
    if insert_at == -1:
        insert_at = lower.rfind('</body>')
    if insert_at == -1:
        raise RuntimeError(f'No safe insertion point found in {file_name}')
    path.write_text(text[:insert_at] + block + '\n' + text[insert_at:], encoding='utf-8')
    print(f'{file_name}: integrated')
