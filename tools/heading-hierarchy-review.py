#!/usr/bin/env python3
"""Targeted SiteOne heading-hierarchy regression for two verified pages."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]

class Headings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.levels = []
    def handle_starttag(self,tag,attrs):
        if tag in {"h1","h2","h3","h4","h5","h6"}:
            self.levels.append(int(tag[1]))

class HierarchyReview(unittest.TestCase):
    def test_reported_heading_skips_corrected(self):
        for file in ["seo-agency-pakistan.html","sales-growth-framework.html"]:
            with self.subTest(file=file):
                source = (ROOT/file).read_text(encoding="utf-8")
                parser=Headings()
                parser.feed(source)
                self.assertEqual(parser.levels.count(1), 1)
                self.assertTrue(parser.levels[0] == 1)
                for previous,current in zip(parser.levels, parser.levels[1:]):
                    self.assertLessEqual(current, previous + 1, f"{file}: heading jumped {previous} to {current}")
        seo=(ROOT/"seo-agency-pakistan.html").read_text(encoding="utf-8")
        self.assertIn("<h2>Organic Growth Map</h2>",seo)
        self.assertIn(".rank-card h2{font-size:15px",seo)
        sales=(ROOT/"sales-growth-framework.html").read_text(encoding="utf-8")
        self.assertIn("<h2>Want me to look at your business?</h2>",sales)
        self.assertIn(".consultbox h2{",sales)
        self.assertIn(".callout h3{",sales)
        self.assertEqual(sales.count("<h4>"),0)
if __name__=="__main__":
    unittest.main()
