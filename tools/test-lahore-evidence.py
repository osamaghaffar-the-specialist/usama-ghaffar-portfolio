"""Regression checks: contextual evidence must be transparent and buyer paths valid."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.ids=set()
        self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):self.ids.add(a["id"])
        if tag=="a" and a.get("href"):self.links.append(a["href"])
        if tag=="h1":self.h1+=1

class LahoreEvidence(unittest.TestCase):
    def test_field_note_has_real_anchor(self):
        p=Links();p.feed((ROOT/"blog.html").read_text(encoding="utf-8"))
        self.assertIn("bee-indexing-field-notes",p.ids)

    def test_commercial_pages_link_to_evidence_and_live_forms(self):
        for filename,service in [("seo-agency-lahore.html","seo"),("google-ads-agency-lahore.html","google_ads")]:
            with self.subTest(page=filename):
                s=(ROOT/filename).read_text(encoding="utf-8")
                p=Links();p.feed(s)
                self.assertEqual(p.h1,1)
                self.assertIn("contact.html?service="+service+"#project-brief",p.links)
                self.assertIn("about.html",p.links)
                self.assertNotIn("Guaranteed #1",s)
        seo=(ROOT/"seo-agency-lahore.html").read_text(encoding="utf-8")
        self.assertIn('href="blog.html#bee-indexing-field-notes"',seo)
        self.assertIn("our own website",seo)

    def test_lahore_hub_links_to_first_party_evidence(self):
        s=(ROOT/"digital-marketing-agency-lahore.html").read_text(encoding="utf-8")
        self.assertIn('href="blog.html#bee-indexing-field-notes"',s)
        self.assertIn('href="seo-agency-lahore.html"',s)
        self.assertIn('href="google-ads-agency-lahore.html"',s)

if __name__=="__main__":
    unittest.main()
