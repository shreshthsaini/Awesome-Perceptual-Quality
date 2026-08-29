#!/usr/bin/env python3
"""Render assets/landscape.svg from the catalog.

One lane per primary tag. Each entry is a dot at its year, so the picture shows
when each strand of the field started producing work and how dense it is now.
Colours are chosen to stay readable on both the light and dark GitHub themes,
and the background is transparent for the same reason.

Run:  python3 scripts/generate_figure.py
"""
import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "assets" / "landscape.svg"

LANES = [
    ("IQA", "Image quality", "#1f6feb"),
    ("VQA", "Video quality", "#8250df"),
    ("UGC", "User-generated", "#1a7f37"),
    ("HDR", "High dynamic range", "#bf3989"),
]
MUTED = "#8b949e"          # readable on light and dark
GRID = "#8b949e"

W, H = 1180, 430
LEFT, RIGHT, TOP = 168, 40, 78
LANE_H = 74
DOT_R = 5.0


def load():
    rows = []
    for name in ("methods", "datasets"):
        path = DATA / f"{name}.csv"
        if not path.exists():
            continue
        with path.open(encoding="utf-8", newline="") as fh:
            for r in csv.DictReader(fh):
                year = (r.get("year") or "").strip()
                tags = (r.get("tags") or "").split()
                if year.isdigit() and tags:
                    rows.append((int(year), tags, name))
    return rows


def main():
    rows = load()
    if not rows:
        raise SystemExit("no data: populate data/*.csv first")

    years = [y for y, _, _ in rows]
    y0, y1 = min(years), max(years)
    # round outward to a tidy axis
    y0 = (y0 // 5) * 5          # round the start down to a tidy tick
    # leave the end at the real maximum so the axis does not claim future years
    span = max(y1 - y0, 1)
    plot_w = W - LEFT - RIGHT

    def x_of(year):
        return LEFT + (year - y0) / span * plot_w

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">'
    )
    parts.append(
        f'<text x="{LEFT}" y="34" font-size="20" font-weight="600" fill="{MUTED}">'
        f'The perceptual quality landscape</text>'
    )
    parts.append(
        f'<text x="{LEFT}" y="55" font-size="13" fill="{MUTED}" opacity="0.85">'
        f'Every catalogued method and dataset, placed at its year. '
        f'Authentic-distortion and HDR work starts late and stays thin.</text>'
    )

    # vertical year gridlines
    step = 5 if span > 12 else 2
    year = y0
    while year <= y1:
        gx = x_of(year)
        parts.append(
            f'<line x1="{gx:.1f}" y1="{TOP - 12}" x2="{gx:.1f}" y2="{TOP + len(LANES) * LANE_H - 18}" '
            f'stroke="{GRID}" stroke-width="1" opacity="0.18"/>'
        )
        parts.append(
            f'<text x="{gx:.1f}" y="{TOP + len(LANES) * LANE_H + 2}" font-size="12" '
            f'fill="{MUTED}" text-anchor="middle" opacity="0.8">{year}</text>'
        )
        year += step

    for i, (tag, label, color) in enumerate(LANES):
        base = TOP + i * LANE_H
        parts.append(
            f'<text x="{LEFT - 16}" y="{base + 4}" font-size="13" font-weight="600" '
            f'fill="{color}" text-anchor="end">{label}</text>'
        )
        lane_rows = [(y, src) for y, tags, src in rows if tag in tags]
        parts.append(
            f'<text x="{LEFT - 16}" y="{base + 21}" font-size="11" fill="{MUTED}" '
            f'text-anchor="end" opacity="0.75">{len(lane_rows)} entries</text>'
        )
        parts.append(
            f'<line x1="{LEFT}" y1="{base}" x2="{W - RIGHT}" y2="{base}" '
            f'stroke="{color}" stroke-width="1" opacity="0.22"/>'
        )

        # stack dots that share a year so density is visible
        by_year = defaultdict(list)
        for y, src in lane_rows:
            by_year[y].append(src)
        for y, srcs in sorted(by_year.items()):
            cx = x_of(y)
            n = len(srcs)
            # Spread the year's entries across the lane height. Spacing shrinks as a
            # year gets busier so a dense year reads as dense instead of collapsing
            # into a single dot.
            usable = LANE_H - 18
            gap = min(DOT_R * 1.7, usable / max(n, 1))
            for k, src in enumerate(srcs):
                offset = (k - (n - 1) / 2) * gap
                cy = base + offset
                if src == "datasets":
                    # Diamond. A rounded square read almost identically to the
                    # circles at this size; a rotated silhouette does not.
                    d = DOT_R * 1.25
                    pts = f"{cx:.1f},{cy - d:.1f} {cx + d:.1f},{cy:.1f} {cx:.1f},{cy + d:.1f} {cx - d:.1f},{cy:.1f}"
                    parts.append(f'<polygon points="{pts}" fill="{color}" opacity="0.95"/>')
                else:
                    parts.append(
                        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{DOT_R:.1f}" '
                        f'fill="{color}" opacity="0.55"/>'
                    )

    # legend
    ly = TOP + len(LANES) * LANE_H + 34
    parts.append(f'<circle cx="{LEFT + 6}" cy="{ly - 4}" r="{DOT_R}" fill="{MUTED}" opacity="0.55"/>')
    parts.append(f'<text x="{LEFT + 20}" y="{ly}" font-size="12" fill="{MUTED}">method</text>')
    lx, lcy, d = LEFT + 90, ly - 4, DOT_R * 1.25
    parts.append(
        f'<polygon points="{lx},{lcy - d:.1f} {lx + d:.1f},{lcy} {lx},{lcy + d:.1f} {lx - d:.1f},{lcy}" '
        f'fill="{MUTED}" opacity="0.95"/>'
    )
    parts.append(f'<text x="{LEFT + 104}" y="{ly}" font-size="12" fill="{MUTED}">dataset</text>')
    parts.append(
        f'<text x="{W - RIGHT}" y="{ly}" font-size="11" fill="{MUTED}" text-anchor="end" opacity="0.7">'
        f'entries carry multiple tags, so lanes overlap</text>'
    )
    parts.append("</svg>")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts), encoding="utf-8")
    counts = {tag: sum(1 for _, tags, _ in rows if tag in tags) for tag, _, _ in LANES}
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(rows)} entries, {y0}-{y1}, {counts}")


if __name__ == "__main__":
    main()
