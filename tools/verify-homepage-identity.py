#!/usr/bin/env python3
"""Validate public homepage schema identity against the verified GBP public listing.

Source-only test; no claim of Google rich results or ranking impact.
"""
from html.parser import HTMLParser
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]

class JsonLd(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_script = False
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "script" and a.get("type") == "application/ld+json":
            self.in_script = True
            self.scripts.append("")
    def handle_data(self, data):
        if self.in_script:
            self.scripts[-1] += data
    def handle_endtag(self, tag):
        if tag == "script":
            self.in_script = False

def main():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    parser = JsonLd()
    parser.feed(html)
    graphs = []
    for text in parser.scripts:
        data = json.loads(text)
        graphs += data.get("@graph", [data])
    matched = [x for x in graphs if x.get("@id") == "https://beemarketingagency.work/#organization"]
    assert len(matched) == 1, "Expected exactly one canonical Organization graph node"
    org = matched[0]
    assert org["@type"] == "Organization"
    assert org["name"] == "Bee Marketing"
    assert org["alternateName"] == "Bee Marketing Agency"
    assert org["url"] == "https://beemarketingagency.work/"
    assert "https://maps.google.com/maps?cid=8401910023599920054" in org.get("sameAs", [])
    assert org.get("telephone") == "+92-315-4294157"
    assert "address" not in org, "No physical street address was validated for this service business"
    print("PASS: homepage structured-data JSON and verified public business identity")

if __name__ == "__main__":
    main()
