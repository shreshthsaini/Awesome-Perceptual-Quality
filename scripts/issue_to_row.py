#!/usr/bin/env python3
"""Turn a filled-in GitHub issue form into a catalog row.

This is what lets people contribute without touching git: they fill the form,
a workflow runs this, and the resulting branch is opened as a pull request.

Usage:
  python3 scripts/issue_to_row.py --kind method  --body-file issue.md
  python3 scripts/issue_to_row.py --kind dataset --body-file issue.md
"""
import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

METHOD_FIELDS = ["name", "title", "year", "venue", "paper_url", "code_url", "tags", "note", "category"]
DATASET_FIELDS = ["name", "year", "venue", "paper_url", "data_url", "content", "annotations", "tags", "note", "category"]

# Issue-form label -> CSV column. Labels must match the YAML forms exactly.
LABELS = {
    "short name": "name",
    "paper title": "title",
    "year": "year",
    "venue": "venue",
    "paper link": "paper_url",
    "code link": "code_url",
    "data link": "data_url",
    "size": "content",
    "annotations": "annotations",
    "tags": "tags",
    "one-line description": "note",
    "section": "category",
}

EMPTY = {"_no response_", "none", "n/a", "-", ""}


def parse_body(text):
    """GitHub renders each form field as '### Label' followed by its value."""
    out = {}
    chunks = re.split(r"^###\s+", text, flags=re.M)[1:]
    for chunk in chunks:
        head, _, rest = chunk.partition("\n")
        label = head.strip().casefold()
        value = rest.strip()
        if value.casefold() in EMPTY:
            value = ""
        key = LABELS.get(label)
        if key:
            # collapse newlines: every catalog field is single-line
            out[key] = " ".join(value.split())
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", choices=["method", "dataset"], required=True)
    ap.add_argument("--body-file", required=True)
    args = ap.parse_args()

    fields = METHOD_FIELDS if args.kind == "method" else DATASET_FIELDS
    path = DATA / ("methods.csv" if args.kind == "method" else "datasets.csv")

    body = Path(args.body_file).read_text(encoding="utf-8")
    parsed = parse_body(body)

    row = {f: parsed.get(f, "") for f in fields}
    # The form offers a friendly section label; map it back to the category slug.
    row["category"] = row["category"].split("(")[-1].strip(") ").strip() or row["category"]

    problems = []
    if not row["name"]:
        problems.append("no short name given")
    if not re.fullmatch(r"(19|20)\d{2}", row["year"] or ""):
        problems.append(f"year must be four digits, got {row['year']!r}")
    if not row["tags"]:
        problems.append("no tags given")
    for f in ("paper_url", "code_url", "data_url"):
        v = row.get(f, "")
        if v and not v.startswith("https://"):
            if v.startswith("http://"):
                row[f] = "https://" + v[len("http://"):]
            else:
                problems.append(f"{f} must be a https link, got {v!r}")
    if "|" in "".join(row.values()):
        problems.append("a field contains '|', which breaks table rendering")

    existing = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    if any(r["name"].casefold() == row["name"].casefold() for r in existing):
        problems.append(f"{row['name']} is already in the catalog")

    if problems:
        print("Could not build a row from this issue:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(existing + [row])

    print(f"Added {row['name']} to {path.name} (category {row['category']}).")


if __name__ == "__main__":
    main()
