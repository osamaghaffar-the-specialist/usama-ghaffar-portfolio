#!/usr/bin/env python3
"""Read-only production smoke check for Bee Marketing GitHub Pages.

Checks HTTP availability and served canonical tags. A live response does not
establish search-engine indexing, ranking, real-user performance or lead delivery.
"""
import sys
from html.parser import HTMLParser
from urllib.request import Request, urlopen, build_opener, HTTPRedirectHandler
from urllib.error import URLError, HTTPError

HOST = "beemarketingagency.work"
BASE = f"https://{HOST}"
PATHS = (
    "/",
    "/robots.txt",
    "/sitemap.xml",
    "/contact.html",
    "/seo-agency-lahore.html",
    "/google-ads-agency-lahore.html",
    "/digital-marketing-agency-lahore.html",
)

class Canonical(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = []
    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "link" and "canonical" in attrs.get("rel", "").split():
            self.values.append(attrs.get("href"))

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None

def request(url, follow=True):
    headers = {"User-Agent": "BeeMarketing-Monitor/1.0 (+read-only)","Accept": "text/html,application/xml,text/plain"}
    opener = None if follow else build_opener(NoRedirect)
    req = Request(url, headers=headers, method="GET")
    if opener:
        with opener.open(req, timeout=20) as res:
            return res.status, res.url, res.read(400000).decode("utf-8", "replace")
    with urlopen(req, timeout=20) as res:
        return res.status, res.url, res.read(400000).decode("utf-8", "replace")

def main():
    errors = []
    for path in PATHS:
        url = BASE + path
        try:
            status, final, body = request(url)
            if status != 200 or final != url:
                errors.append(f"{url}: returned {status} at {final}")
                continue
            if path.endswith(".html") or path == "/":
                p = Canonical()
                p.feed(body)
                if p.values != [url]:
                    errors.append(f"{url}: served canonical {p.values!r}")
            elif path == "/robots.txt" and "Sitemap: https://beemarketingagency.work/sitemap.xml" not in body:
                errors.append("robots.txt: missing expected sitemap declaration")
            elif path == "/sitemap.xml" and "<urlset" not in body:
                errors.append("sitemap.xml: invalid or missing URL set")
            print(f"OK {status} {url}")
        except Exception as exc:
            errors.append(f"{url}: {type(exc).__name__}: {exc}")

    # GitHub Pages should upgrade HTTP to the custom HTTPS domain.
    try:
        status, final, _ = request("http://" + HOST + "/", follow=True)
        if final != BASE + "/" or status != 200:
            errors.append(f"HTTP upgrade ended at {final}, status {status}")
        else:
            print("OK HTTP to HTTPS upgrade")
    except Exception as exc:
        errors.append(f"HTTP upgrade: {type(exc).__name__}: {exc}")

    # Official 27 Nov full-sitemap URL Inspection still names the historical
    # github.io copy as Google-selected for two national money pages. Google
    # last crawled those pages Oct 20/27; verify CURRENT redirect, not Google freshness.
    legacy_root = "https://osamaghaffar-the-specialist.github.io/usama-ghaffar-portfolio/"
    from urllib.parse import urljoin
    for page in ("google-ads-agency-pakistan.html", "performance-marketing-agency-pakistan.html"):
        legacy = legacy_root + page
        target = BASE + "/" + page
        try:
            try:
                status, final, _ = request(legacy, follow=False)
            except HTTPError as exc:
                status = exc.code
                final = exc.headers.get("Location", "")
            if status not in (301, 308):
                errors.append(f"{page}: old GitHub Pages URL did not redirect permanently (HTTP {status})")
                continue
            redirect_to = urljoin(legacy, final)
            if redirect_to != target:
                errors.append(f"{page}: old GitHub Pages redirects to unexpected URL: {redirect_to}")
                continue
            end_status, end_url, html = request(legacy, follow=True)
            if end_status != 200 or end_url != target:
                errors.append(f"{page}: redirect chain ended at {end_url} with HTTP {end_status}")
                continue
            p = Canonical()
            p.feed(html)
            if p.values != [target]:
                errors.append(f"{page}: redirected destination canonical mismatch {p.values!r}")
            else:
                print(f"OK historical GitHub Pages {page} permanently redirects to its canonical")
        except Exception as exc:
            errors.append(f"Legacy {page} redirect check: {type(exc).__name__}: {exc}")

    if errors:
        print("FAILED checks:")
        for err in errors:
            print(" -", err)
        return 1
    print("PASS production smoke check; this is not a GSC index or Lighthouse validation.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
