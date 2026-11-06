#!/usr/bin/env python3
"""Check that every local href/src in a site's HTML resolves.
Usage: check_links.py <dir>                  # files exist on disk (run before deploy)
       check_links.py <dir> --base-url URL   # also GET each one over HTTP (run after deploy)
Exit code 1 if anything is missing."""
import re, sys, os, urllib.request, urllib.error
from urllib.parse import urlparse, unquote
root = os.path.abspath(sys.argv[1]); base = sys.argv[sys.argv.index("--base-url")+1].rstrip("/") if "--base-url" in sys.argv else None
pat = re.compile(r'''(?:href|src)\s*=\s*["']([^"']+)["']''', re.I)
bad, seen = [], set()
for dp, _, fs in os.walk(root):
    for f in fs:
        if not f.endswith(".html"): continue
        page = os.path.join(dp, f)
        for ref in pat.findall(open(page, encoding="utf-8", errors="ignore").read()):
            u = urlparse(ref)
            if u.scheme or ref.startswith(("#", "//", "data:", "mailto:", "javascript:")) or not u.path: continue
            target = os.path.normpath(os.path.join(root, u.path.lstrip("/")) if u.path.startswith("/") else os.path.join(dp, unquote(u.path)))
            if target.endswith(os.sep) or os.path.isdir(target): target = os.path.join(target, "index.html")
            rel = os.path.relpath(target, root)
            if rel in seen: continue
            seen.add(rel)
            if not os.path.isfile(target): bad.append(f"MISSING on disk: {rel} (referenced from {os.path.relpath(page, root)})"); continue
            if base:
                try: code = urllib.request.urlopen(f"{base}/{rel}", timeout=60).status
                except urllib.error.HTTPError as e: code = e.code
                except Exception as e: code = str(e)
                if code != 200: bad.append(f"HTTP {code}: {base}/{rel}")
print(f"checked {len(seen)} local references" + (f" against {base}" if base else ""))
for b in bad: print(b)
sys.exit(1 if bad else 0)
