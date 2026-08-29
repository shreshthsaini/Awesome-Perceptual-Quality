#!/usr/bin/env python3
"""Render README.md from README.template.md and the CSV files in data/.

Every table in the README is generated. Edit the CSVs, not the README.
Run:  python3 scripts/generate_readme.py
"""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TEMPLATE = ROOT / "README.template.md"
README = ROOT / "README.md"

METHOD_CATEGORIES = ["mllm", "hdr", "vqa", "nr-iqa", "fr-iqa"]
DATASET_CATEGORIES = ["aigc", "hdr", "video", "image"]

# Primary tags render as coloured shields badges; modifiers as code spans.
TAG_COLORS = {
    "HDR": "bf3989",
    "UGC": "1a7f37",
    "VQA": "8250df",
    "IQA": "1f6feb",
}
TAG_ORDER = ["HDR", "UGC", "VQA", "IQA"]


def read(name):
    path = DATA / f"{name}.csv"
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return [row for row in csv.DictReader(handle) if any(v.strip() for v in row.values())]


def tag_cell(tags):
    """Primary tags first as coloured badges, then modifiers as code spans."""
    have = (tags or "").split()
    primary = [
        f"![{t}](https://img.shields.io/badge/{t}-{TAG_COLORS[t]}?style=flat-square&labelColor={TAG_COLORS[t]})"
        for t in TAG_ORDER if t in have
    ]
    rest = [f"`{t}`" for t in have if t not in TAG_COLORS]
    return " ".join(primary + rest)


def stars_cell(url):
    """A live star badge when the link is a GitHub repo, a plain link otherwise."""
    url = (url or "").strip()
    if not url:
        return ""
    if url.startswith("https://github.com/"):
        slug = "/".join(url.rstrip("/").removeprefix("https://github.com/").split("/")[:2])
        if slug.count("/") == 1:
            return (
                f"[![Stars](https://img.shields.io/github/stars/{slug}"
                f"?style=flat-square&label=%E2%98%85&color=57606a)]({url})"
            )
    return f"[link]({url})"


DASH = "-"


def link(text, url):
    url = (url or "").strip()
    return f"[{text}]({url})" if url else ""


def or_dash(cell):
    return cell if (cell or "").strip() else DASH


def sort_key(row):
    """Newest first; unknown years last."""
    try:
        return (-int(row.get("year") or 0), row.get("name", "").lower())
    except ValueError:
        return (0, row.get("name", "").lower())


def methods_table(rows):
    head = (
        "| Method | Paper | Venue | Tags | Code |\n"
        "| :--- | :--- | :---: | :--- | :---: |\n"
    )
    body = []
    for r in sorted(rows, key=sort_key):
        venue = " ".join(x for x in [r.get("venue", ""), r.get("year", "")] if x)
        title = r.get("title", "")
        note = r.get("note", "").strip()
        paper = link(title, r.get("paper_url"))
        if note:
            paper = f"{paper}<br /><sub>{note}</sub>" if paper else f"<sub>{note}</sub>"
        body.append(
            f"| **{r.get('name','')}** | {paper} | {venue} | "
            f"{tag_cell(r.get('tags'))} | {or_dash(stars_cell(r.get('code_url')))} |"
        )
    return head + "\n".join(body) if body else head + "| | *no entries yet* | | | |"


def datasets_table(rows):
    head = (
        "| Dataset | Content | Annotations | Venue | Tags | Links |\n"
        "| :--- | :--- | :--- | :---: | :--- | :---: |\n"
    )
    body = []
    for r in sorted(rows, key=sort_key):
        venue = " ".join(x for x in [r.get("venue", ""), r.get("year", "")] if x)
        data_url = (r.get("data_url") or "").strip()
        data_cell = stars_cell(data_url) if data_url.startswith("https://github.com/") else link("data", data_url)
        links = " ".join(x for x in [link("paper", r.get("paper_url")), data_cell] if x)
        note = r.get("note", "").strip()
        name = f"**{r.get('name','')}**"
        if note:
            name = f"{name}<br /><sub>{note}</sub>"
        body.append(
            f"| {name} | {or_dash(r.get('content'))} | {or_dash(r.get('annotations'))} | {venue} | "
            f"{tag_cell(r.get('tags'))} | {or_dash(links)} |"
        )
    return head + "\n".join(body) if body else head + "| | *no entries yet* | | | | |"


def toolboxes_table(rows):
    """Stars render as a live shields badge so the table never goes stale.
    The `stars` column is only used to order the rows at generation time."""
    head = "| Toolbox | Stars | Language | What it does |\n| :--- | :---: | :---: | :--- |\n"

    def stars(r):
        try:
            return -int(r.get("stars") or 0)
        except ValueError:
            return 0

    def badge(repo_url):
        slug = (repo_url or "").rstrip("/").removeprefix("https://github.com/")
        if not slug or slug.count("/") != 1:
            return ""
        return (
            f"![Stars](https://img.shields.io/github/stars/{slug}"
            f"?style=flat-square&label=&color=57606a)"
        )

    body = [
        f"| {link('**' + r.get('name','') + '**', r.get('repo_url')) or r.get('name','')} "
        f"| {badge(r.get('repo_url'))} | {r.get('language','')} | {r.get('note','')} |"
        for r in sorted(rows, key=stars)
    ]
    return head + "\n".join(body) if body else head + "| | | | |"


def challenges_table(rows):
    head = "| Challenge | Years | What it covers |\n| :--- | :---: | :--- |\n"
    body = [
        f"| {link('**' + r.get('name','') + '**', r.get('url')) or r.get('name','')} "
        f"| {r.get('years','')} | {r.get('note','')} |"
        for r in rows
    ]
    return head + "\n".join(body) if body else head + "| | | |"


def surveys_table(rows):
    head = "| Survey | Venue | Summary |\n| :--- | :---: | :--- |\n"
    body = []
    for r in sorted(rows, key=lambda x: -int(x.get("year") or 0)):
        venue = " ".join(x for x in [r.get("venue", ""), r.get("year", "")] if x)
        body.append(f"| {link(r.get('title',''), r.get('paper_url'))} | {venue} | {r.get('note','')} |")
    return head + "\n".join(body) if body else head + "| | | |"


def build_blocks():
    methods = read("methods")
    datasets = read("datasets")
    blocks = {}
    for cat in METHOD_CATEGORIES:
        blocks[f"methods:{cat}"] = methods_table([r for r in methods if r.get("category") == cat])
    for cat in DATASET_CATEGORIES:
        blocks[f"datasets:{cat}"] = datasets_table([r for r in datasets if r.get("category") == cat])
    blocks["toolboxes"] = toolboxes_table(read("toolboxes"))
    blocks["challenges"] = challenges_table(read("challenges"))
    blocks["surveys"] = surveys_table(read("surveys"))

    n_hdr = sum(1 for r in methods + datasets if "HDR" in (r.get("tags") or ""))
    n_ugc = sum(1 for r in methods + datasets if "UGC" in (r.get("tags") or ""))
    for cat in METHOD_CATEGORIES:
        blocks[f"count:methods:{cat}"] = str(sum(1 for r in methods if r.get("category") == cat))
    for cat in DATASET_CATEGORIES:
        blocks[f"count:datasets:{cat}"] = str(sum(1 for r in datasets if r.get("category") == cat))
    blocks["count:toolboxes"] = str(len(read("toolboxes")))
    blocks["count:challenges"] = str(len(read("challenges")))
    blocks["count:surveys"] = str(len(read("surveys")))
    blocks["stat:methods"] = str(len(methods))
    blocks["stat:datasets"] = str(len(datasets))
    blocks["stat:hdr"] = str(n_hdr)
    blocks["stat:ugc"] = str(n_ugc)
    blocks["stat:total"] = str(len(methods) + len(datasets))
    return blocks


def main():
    if not TEMPLATE.exists():
        sys.exit(f"missing template: {TEMPLATE}")
    text = TEMPLATE.read_text(encoding="utf-8")
    blocks = build_blocks()

    # Table blocks: <!-- AUTOGEN:key --> ... <!-- /AUTOGEN -->
    def replace_block(match):
        key = match.group(1)
        if key not in blocks:
            sys.exit(f"template references unknown block: {key}")
        return f"<!-- AUTOGEN:{key} -->\n{blocks[key]}\n<!-- /AUTOGEN -->"

    text = re.sub(
        r"<!-- AUTOGEN:([a-z:\-]+) -->.*?<!-- /AUTOGEN -->",
        replace_block,
        text,
        flags=re.S,
    )
    # Inline stats: {{stat:methods}}
    text = re.sub(r"\{\{((?:stat|count):[a-z:\-]+)\}\}", lambda m: blocks[m.group(1)], text)

    README.write_text(text, encoding="utf-8")
    print(
        f"Wrote {README.name}: {blocks['stat:methods']} methods, "
        f"{blocks['stat:datasets']} datasets "
        f"({blocks['stat:hdr']} HDR-tagged, {blocks['stat:ugc']} UGC-tagged)."
    )


if __name__ == "__main__":
    main()
