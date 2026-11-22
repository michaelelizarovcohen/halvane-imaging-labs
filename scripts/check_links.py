#!/usr/bin/env python3
"""Check every internal href/src in docs/*.html resolves to a file; report external links separately.

Usage: python3 scripts/check_links.py [--external]   (--external also HEAD-requests external URLs)
"""
import os, re, sys, urllib.parse, urllib.request
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(ROOT, "docs")


class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.ids, self.base = [], set(), None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "base":
            self.base = a.get("href")
        if "id" in a:
            self.ids.add(a["id"])
        for k in ("href", "src"):
            if tag != "base" and k in a and a[k]:
                self.links.append(a[k])


def main():
    broken, external, pages, anchors = [], set(), 0, {}
    parsed = {}
    for dp, _, fs in os.walk(DOCS):
        for f in fs:
            if f.endswith(".html"):
                p = os.path.join(dp, f)
                pr = P()
                pr.feed(open(p, encoding="utf-8").read())
                parsed[p] = pr
                anchors[os.path.normpath(p)] = pr.ids
    for p, pr in parsed.items():
        pages += 1
        for link in pr.links:
            if link.startswith(("http://", "https://")):
                external.add(link)
                continue
            if link.startswith(("mailto:", "tel:", "data:", "#")):
                if link.startswith("#") and link[1:] and link[1:] not in pr.ids:
                    broken.append((p, link))
                continue
            path, _, frag = link.partition("#")
            if pr.base:  # 404.html uses <base href="/<repo>/">, i.e. the docs root
                target = os.path.normpath(os.path.join(DOCS, urllib.parse.unquote(path)))
            else:
                target = os.path.normpath(os.path.join(os.path.dirname(p), urllib.parse.unquote(path)))
            if os.path.isdir(target):
                target = os.path.join(target, "index.html")
            if not os.path.exists(target):
                broken.append((p, link))
            elif frag and target.endswith(".html") and frag not in anchors.get(os.path.normpath(target), set()):
                broken.append((p, link))
    print(f"pages: {pages}, broken internal links: {len(broken)}, external URLs: {len(external)}")
    for p, l in broken[:50]:
        print("  BROKEN", os.path.relpath(p, DOCS), "->", l)
    bad_ext = []
    if "--external" in sys.argv:
        for u in sorted(external):
            try:
                req = urllib.request.Request(u, method="HEAD", headers={"User-Agent": "halvane-linkcheck/1.0"})
                code = urllib.request.urlopen(req, timeout=20).status
            except Exception as e:
                code = getattr(e, "code", str(e)[:60])
            if code not in (200, 301, 302, 403, 405):
                bad_ext.append((u, code))
            print(f"  {code} {u}")
    sys.exit(1 if broken or bad_ext else 0)


if __name__ == "__main__":
    main()
