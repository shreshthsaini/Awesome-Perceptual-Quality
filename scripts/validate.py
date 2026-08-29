#!/usr/bin/env python3
"""Validate the CSV catalogs before they are rendered into the README.

Checks column names, required fields, tag vocabulary, category vocabulary,
year sanity, URL scheme, and duplicate entries.

Run:  python3 scripts/validate.py
"""
import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

METHOD_FIELDS = ["name", "title", "year", "venue", "paper_url", "code_url", "tags", "note", "category"]
DATASET_FIELDS = ["name", "year", "venue", "paper_url", "data_url", "content", "annotations", "tags", "note", "category"]

VALID_TAGS = {
    "IQA", "VQA", "UGC", "HDR",
    "FR", "NR", "RR", "PU",
    "CLASSICAL", "DEEP", "CLIP", "TRANSFORMER",
    "MLLM", "RL", "REASONING", "BENCHMARK",
    "SYNTHETIC", "AUTHENTIC", "AIGC", "AESTHETIC",
    "STREAMING", "GAMING", "COMPRESSION",
}
METHOD_CATEGORIES = {"fr-iqa", "nr-iqa", "vqa", "hdr", "mllm"}
DATASET_CATEGORIES = {"aigc", "hdr", "video", "image"}

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def load(name, fields):
    path = DATA / f"{name}.csv"
    if not path.exists():
        err(f"{name}.csv: missing")
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != fields:
            err(f"{name}.csv: columns are {reader.fieldnames}, expected {fields}")
            return []
        return [r for r in reader if any(v.strip() for v in r.values())]


def check_common(rows, name, categories):
    this_year = date.today().year
    seen_names, seen_papers = set(), set()
    for i, row in enumerate(rows, 2):
        where = f"{name}.csv line {i}"
        if not row["name"].strip():
            err(f"{where}: empty name")
        year = row.get("year", "").strip()
        if not re.fullmatch(r"(19|20)\d{2}", year):
            err(f"{where}: bad year {year!r}")
        elif not 1990 <= int(year) <= this_year + 1:
            err(f"{where}: year {year} out of range")
        for field in ("paper_url", "code_url", "data_url"):
            url = (row.get(field) or "").strip()
            if url and not url.startswith("https://"):
                err(f"{where}: {field} must be https, got {url!r}")
        tags = (row.get("tags") or "").split()
        if not tags:
            err(f"{where}: no tags")
        for tag in tags:
            if tag not in VALID_TAGS:
                err(f"{where}: unknown tag {tag!r}")
        cat = (row.get("category") or "").strip()
        if cat not in categories:
            err(f"{where}: category {cat!r} not in {sorted(categories)}")
        key = row["name"].strip().casefold()
        if key in seen_names:
            err(f"{where}: duplicate name {row['name']!r}")
        seen_names.add(key)
        paper = (row.get("paper_url") or "").strip()
        if paper:
            if paper in seen_papers:
                # Companion releases (KADID-10k / KADIS-700k) share one paper, so this
                # is a smell rather than an error.
                warnings.append(f"{where}: shares paper_url with an earlier row ({paper})")
            seen_papers.add(paper)
        if "|" in "".join(row.values()):
            err(f"{where}: contains a pipe character, which breaks table rendering")


methods = load("methods", METHOD_FIELDS)
datasets = load("datasets", DATASET_FIELDS)
check_common(methods, "methods", METHOD_CATEGORIES)
check_common(datasets, "datasets", DATASET_CATEGORIES)

for row in methods:
    if not row.get("title", "").strip():
        err(f"methods.csv: {row.get('name')!r} has no title")

for w in warnings:
    print(f"WARN:  {w}")

if errors:
    for e in errors:
        print(f"ERROR: {e}", file=sys.stderr)
    raise SystemExit(1)

print(f"OK: {len(methods)} methods and {len(datasets)} datasets validated.")
