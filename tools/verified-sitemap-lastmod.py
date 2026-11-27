#!/usr/bin/env python3
"""Validate genuine lastmod values only for known materially updated Lahore pages."""
from pathlib import Path
from datetime import date
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
EXPECTED={
  "https://beemarketingagency.work/digital-marketing-agency-lahore.html":"2026-11-16",
  "https://beemarketingagency.work/seo-agency-lahore.html":"2026-11-16",
  "https://beemarketingagency.work/google-ads-agency-lahore.html":"2026-11-16",
  "https://beemarketingagency.work/ecommerce-agency-pakistan.html":"2026-11-04",
  "https://beemarketingagency.work/seo-agency-pakistan.html":"2026-11-06",
  "https://beemarketingagency.work/google-ads-agency-pakistan.html":"2026-11-06",
  "https://beemarketingagency.work/digital-marketing-agency-gulberg-lahore.html":"2026-11-06",
  "https://beemarketingagency.work/digital-marketing-agency-lake-city-lahore.html":"2026-11-06",
}
NS={"sm":"http://www.sitemaps.org/schemas/sitemap/0.9"}
def main():
    root=ET.parse(ROOT/"sitemap.xml").getroot()
    seen={}
    for node in root.findall("sm:url",NS):
        loc=node.findtext("sm:loc",default="",namespaces=NS)
        assert loc.startswith("https://beemarketingagency.work/"),f"Unexpected sitemap hostname: {loc}"
        assert loc not in seen,f"Duplicate URL: {loc}"
        lastmod=node.findtext("sm:lastmod",default="",namespaces=NS)
        if lastmod:
            assert loc in EXPECTED,f"Unverified modification date attached: {loc}"
            assert lastmod==EXPECTED[loc],f"Unsupported lastmod for {loc}"
            assert date.fromisoformat(lastmod)<=date.today(),f"Future-dated sitemap change: {loc}"
        seen[loc]=lastmod
    assert len(seen)==103,f"Unexpected sitemap URL count: {len(seen)}"
    for url,stamp in EXPECTED.items():
        assert seen.get(url)==stamp, f"Missing verified lastmod: {url}"
        path=urlsplit(url).path.lstrip("/")
        assert (ROOT/path).is_file(),f"Missing corresponding source page: {url}"
    print(f"PASS {len(seen)} canonical sitemap URLs; {len(EXPECTED)} verified Git-based content modification dates")
if __name__=="__main__":
    main()
