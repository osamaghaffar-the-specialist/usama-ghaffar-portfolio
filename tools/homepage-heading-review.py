#!/usr/bin/env python3
"""Regression check for Lighthouse homepage heading hierarchy and known card styles."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]

class Headings(HTMLParser):
    def __init__(self):
        super().__init__()
        self.levels=[]
    def handle_starttag(self,tag,attrs):
        if tag in {"h1","h2","h3","h4","h5","h6"}:
            self.levels.append(int(tag[1]))

class HomepageSemantics(unittest.TestCase):
    def test_heading_progression_and_style(self):
        source=(ROOT/"index.html").read_text(encoding="utf-8")
        p=Headings()
        p.feed(source)
        self.assertEqual(p.levels.count(1),1)
        self.assertEqual(p.levels[0],1)
        for previous,current in zip(p.levels,p.levels[1:]):
            self.assertLessEqual(current,previous+1)
        self.assertEqual(source.count('<h3 class="case-headline">'),5)
        self.assertEqual(source.count('<h3>Services</h3>'),1)
        self.assertIn('.why-item h3{font-size:clamp(18px,2vw,20px) !important',source)
        self.assertIn('.footer-col h3{font-family:var(--font-primary)',source)
        self.assertIn('class="case-headline"',source)
if __name__=="__main__":
    unittest.main()
