#!/usr/bin/env python3
"""Review Bee Marketing homepage primary marketing-agency intent without fake SEO promises."""
from html.parser import HTMLParser
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
HOME="https://beemarketingagency.work/"

class Extract(HTMLParser):
    def __init__(self):
        super().__init__();self.h1=[];self.title=[];self.in_h1=False;self.in_title=False;self.links=[];self.meta={};self.canonicals=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="h1":self.in_h1=True
        if tag=="title":self.in_title=True
        if tag=="a":self.links.append(a.get("href",""))
        if tag=="meta":
            self.meta[a.get("name") or a.get("property")]=a.get("content","")
        if tag=="link" and a.get("rel")=="canonical":self.canonicals.append(a.get("href"))
    def handle_endtag(self,tag):
        if tag=="h1":self.in_h1=False
        if tag=="title":self.in_title=False
    def handle_data(self,data):
        if self.in_h1:self.h1.append(data)
        if self.in_title:self.title.append(data)

def main():
    src=(ROOT/"index.html").read_text(encoding="utf-8")
    p=Extract();p.feed(src)
    title=" ".join(p.title).strip()
    heading=" ".join(p.h1)
    assert title=="Marketing Agency in Lahore, Pakistan | Bee Marketing",title
    assert src.count("<h1>")==1,"Homepage should have a single H1"
    assert "Marketing Agency in Lahore, Pakistan" in heading,heading
    assert p.canonicals==[HOME],p.canonicals
    assert p.meta["description"].startswith("Bee Marketing is a Lahore-based marketing agency")
    assert p.meta["og:title"]==title
    assert "Bahria Town, Lahore" in src
    for target in ("seo-agency-lahore.html","google-ads-agency-lahore.html",
                   "facebook-ads-agency-pakistan.html","ecommerce-agency-pakistan.html",
                   "contact.html#project-brief"):
        assert target in p.links,f"Missing user-facing path {target}"
    assert "guaranteed #1" not in src.lower()
    print("PASS one marketing agency homepage target; honest Lahore positioning, service pathways, unchanged canonical")

if __name__=="__main__":
    main()
