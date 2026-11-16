#!/usr/bin/env python3
"""Read-only regression scan for Bee Marketing's static GitHub Pages source.

Validates the sitemap inventory, canonical and metadata consistency, and internal
links. It does not submit indexing requests, change production, or claim that
Google has indexed a page. Run: python3 tools/sitewide-seo-check.py
"""
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
HOST = "beemarketingagency.work"
BASE = f"https://{HOST}/"

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._title = False
        self.h1 = 0
        self.description = []
        self.canonicals = []
        self.links = []
        self.ids = set()
        self.duplicate_ids = set()

    def handle_starttag(self, tag, attributes):
        a = dict(attributes)
        if tag == "title":
            self._title = True
        elif tag == "h1":
            self.h1 += 1
        elif tag == "meta" and a.get("name", "").lower() == "description":
            self.description.append(a.get("content", "").strip())
        elif tag == "link" and "canonical" in a.get("rel", "").lower().split():
            self.canonicals.append(a.get("href", ""))
        elif tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if a.get("id"):
            if a["id"] in self.ids:
                self.duplicate_ids.add(a["id"])
            self.ids.add(a["id"])

    def handle_endtag(self, tag):
        if tag == "title":
            self._title = False

    def handle_data(self, value):
        if self._title:
            self.title += value

def main():
    errors, warnings = [], []
    xml = ET.parse(ROOT / "sitemap.xml")
    sitemap_urls = [
        (node.text or "").strip()
        for node in xml.findall(".//{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    ]
    if len(set(sitemap_urls)) != len(sitemap_urls):
        errors.append("Sitemap includes duplicate URLs")

    sitemap_paths = set()
    for u in sitemap_urls:
        p = urlsplit(u)
        if p.scheme != "https" or p.netloc != HOST or p.query or p.fragment:
            errors.append(f"Noncanonical sitemap URL: {u}")
            continue
        relative = unquote(p.path.lstrip("/")) or "index.html"
        sitemap_paths.add(relative)
        if not (ROOT / relative).is_file():
            errors.append(f"Sitemap URL has no matching file: {relative}")

    root_pages = {p.name for p in ROOT.glob("*.html")
                  if p.name != "404.html"
                  and not re.fullmatch(r"google[0-9a-f]{16}\\.html", p.name)}
    for p in sorted(root_pages - sitemap_paths):
        errors.append(f"Content page missing from sitemap: {p}")
    for p in sorted(sitemap_paths - root_pages):
        errors.append(f"Sitemap points to missing root content page: {p}")

    titles = defaultdict(list)
    descriptions = defaultdict(list)
    parsed = {}
    for path in sorted(root_pages):
        page = Page()
        page.feed((ROOT / path).read_text(encoding="utf-8"))
        parsed[path] = page
        if not page.title.strip():
            errors.append(f"{path}: missing title")
        else:
            titles[page.title.strip()].append(path)
        if len(page.description) != 1 or not page.description[0]:
            errors.append(f"{path}: expected one nonempty meta description")
        else:
            descriptions[page.description[0]].append(path)
        expected = BASE if path == "index.html" else BASE + path
        if page.canonicals != [expected]:
            errors.append(f"{path}: canonical {page.canonicals!r}, expected {expected}")
        if page.h1 != 1:
            errors.append(f"{path}: expected one H1, found {page.h1}")
        if page.duplicate_ids:
            warnings.append(f"{path}: duplicate IDs {sorted(page.duplicate_ids)[:8]}")

    for value, paths in titles.items():
        if len(paths) > 1:
            errors.append(f"Duplicate title on {paths}: {value}")
    for value, paths in descriptions.items():
        if len(paths) > 1:
            errors.append(f"Duplicate meta description on {paths}")

    for path, page in parsed.items():
        for href in page.links:
            link = urlsplit(href)
            if link.scheme and link.scheme not in ("http", "https"):
                continue
            if link.netloc and link.netloc not in (HOST, "www." + HOST):
                continue
            # Resolve links on root-level pages; ignore links inside scripts.
            target = unquote(link.path.lstrip("/")) if link.path.startswith("/") else unquote(link.path)
            target = target or path
            target = target.rstrip("/") or "index.html"
            if target == ".":
                target = "index.html"
            target_path = ROOT / target
            if target_path.is_dir():
                target_path = target_path / "index.html"
            if not target_path.is_file():
                errors.append(f"{path}: broken internal link {href}")
            elif link.fragment and target_path.suffix.lower() in (".html", ".htm"):
                dest = parsed.get(target_path.name)
                if dest is not None and link.fragment not in dest.ids:
                    warnings.append(f"{path}: fragment not found in {target}: #{link.fragment}")

    report = {"sitemap_urls": len(sitemap_urls), "html_pages": len(root_pages),
              "errors": errors, "warnings": warnings,
              "note": "Static-source checks only; not live HTTP, Google indexing, or Core Web Vitals."}
    print(json.dumps(report, indent=2))
    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())
