"""Validate focused Lahore money-page SEO edits without a new monitoring system."""
from html.parser import HTMLParser
from pathlib import Path

class Check(HTMLParser):
 def __init__(self):
  super().__init__();self.links=[];self.canonical=[];self.h1=[];self._in_h1=False
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  if tag=="a":self.links.append(attrs.get("href",""))
  if tag=="link" and attrs.get("rel")=="canonical":self.canonical.append(attrs.get("href",""))
  if tag=="h1":self._in_h1=True;self.h1.append("")
 def handle_endtag(self,tag):
  if tag=="h1":self._in_h1=False
 def handle_data(self,text):
  if self._in_h1:self.h1[-1]+=text
pages={
 "seo-agency-lahore.html":("SEO Agency in Lahore",["seo-cost-lahore.html","contact.html?service=seo#project-brief"]),
 "google-ads-agency-lahore.html":("Google Ads Agency in Lahore",["google-ads-cost-lahore.html","contact.html?service=google_ads#project-brief"]),
 "digital-marketing-agency-lahore.html":("Digital Marketing Agency in Lahore",["seo-agency-lahore.html","google-ads-agency-lahore.html","performance-marketing.html#case-01"])
}
for path,(target,expected) in pages.items():
 p=Check();p.feed(Path(path).read_text(encoding="utf-8"))
 assert len(p.h1)==1,(path,"one H1 required",p.h1)
 assert target.lower() in p.h1[0].lower(),(path,"commercial intent H1 mismatch")
 assert p.canonical==["https://beemarketingagency.work/"+path],(path,"canonical altered",p.canonical)
 for href in expected:
  assert href in p.links,(path,"missing expected route",href)
  if href.endswith(".html") or ".html#" in href:
   assert Path(href.split("#")[0]).is_file(),(path,"missing local target",href)
 print("PASS",path,"H1, canonical, commercial links")
