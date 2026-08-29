#!/usr/bin/env python3
"""Check every URL in the catalog and report the ones that fail.

Link rot is the usual reason a list stops being useful, so this is meant to be
run periodically (or in CI) rather than once.

Run:  python3 scripts/check_links.py [--timeout 20] [--workers 8]
"""
import argparse
import csv
import sys
import ssl
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
URL_FIELDS = ("paper_url", "code_url", "data_url", "repo_url", "url")
UA = "awesome-perceptual-quality link checker (+https://github.com/)"


def collect():
    seen = {}
    for path in sorted(DATA.glob("*.csv")):
        with path.open(encoding="utf-8", newline="") as fh:
            for row in csv.DictReader(fh):
                label = row.get("name") or row.get("title") or "?"
                for field in URL_FIELDS:
                    url = (row.get(field) or "").strip()
                    if url:
                        seen.setdefault(url, f"{path.name}:{label}")
    return sorted(seen.items())


def _context():
    """Several university hosts present chains that the system store rejects.
    Use certifi when it is available so those do not look like dead links."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except Exception:
        return ssl.create_default_context()


CTX = _context()


def check(item, timeout):
    url, where = item
    req = urllib.request.Request(url, headers={"User-Agent": UA}, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            return url, where, resp.status
    except urllib.error.HTTPError as e:
        # 403 usually means a publisher bot-wall, not a dead link
        return url, where, e.code
    except Exception as e:
        # Transport-level failure. Often a TLS or user-agent quirk on an academic
        # host rather than link rot, so it is reported as UNVERIFIED, not broken.
        return url, where, f"UNVERIFIED:{type(e).__name__}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--timeout", type=int, default=20)
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    items = collect()
    print(f"checking {len(items)} unique URLs...")
    bad, unverified = [], []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for url, where, status in pool.map(lambda i: check(i, args.timeout), items):
            if isinstance(status, int) and status < 400:
                continue
            if status == 403:
                print(f"  SKIP 403 (bot-wall) {where}  {url}")
                continue
            if isinstance(status, str) and status.startswith("UNVERIFIED"):
                unverified.append((status, where, url))
                continue
            bad.append((status, where, url))

    if unverified:
        print(f"\n{len(unverified)} link(s) could not be verified from Python "
              f"(usually a TLS or user-agent quirk; try curl before removing):")
        for status, where, url in unverified:
            print(f"  {status}  {where}\n      {url}")

    if bad:
        print(f"\n{len(bad)} link(s) look broken:")
        for status, where, url in sorted(bad, key=lambda x: str(x[0])):
            print(f"  {status}  {where}\n      {url}")
        sys.exit(1)
    print("all links OK")


if __name__ == "__main__":
    main()
