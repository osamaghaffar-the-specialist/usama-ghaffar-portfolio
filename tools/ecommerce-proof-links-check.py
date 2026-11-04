"""Review-only check for contextual ecommerce links, proof integrity and important URLs."""
from html.parser import HTMLParser
from pathlib import Path

class Page(HTMLParser):
 def __init__(self):
  super().__init__()
  self.links=[]
  self.ids=set()
  self.canonical=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if "id" in a:self.ids.add(a["id"])
  if tag=="a" and "href" in a:self.links.append(a["href"])
  if tag=="link" and a.get("rel")=="canonical":self.canonical.append(a.get("href"))

def parse(name):
 p=Page();p.feed(Path(name).read_text(encoding="utf-8"));return p
service=parse("ecommerce-agency-pakistan.html")
proof=parse("performance-marketing.html")
assert "performance-marketing.html#case-01" in service.links,"Ecommerce service needs direct case proof link"
assert "ecommerce-agency-pakistan.html" in proof.links,"Portfolio needs ecommerce service contextual link"
assert "case-01" in proof.ids,"Case study anchor missing"
assert "contact.html?service=ecommerce#project-brief" in service.links,"Consultation CTA missing"
assert service.canonical==["https://beemarketingagency.work/ecommerce-agency-pakistan.html"],"Service canonical changed"
assert proof.canonical==["https://beemarketingagency.work/performance-marketing.html"],"Portfolio canonical changed"
print("PASS: contextual reciprocal navigation, case-study anchor, consultation CTA and canonical URLs")
