"""Build the imprint shelf from books.json."""
from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAT = json.loads((ROOT / "books.json").read_text(encoding="utf-8"))
OUT = ROOT / "index.html"


def main() -> None:
    cards = []
    for b in CAT.get("books") or []:
        title = html.escape(b.get("title") or b["slug"])
        sub = html.escape(b.get("subtitle") or "")
        status = html.escape(b.get("status") or "draft")
        href = html.escape(b.get("path") or f"books/{b['slug']}/")
        epi = html.escape(b.get("epigraph") or "")
        epi_h = f"<p>{epi}</p>" if epi else ""
        cards.append(
            f'<a class="card" href="{href}">'
            f'<div class="kicker">{status}</div>'
            f"<h2>{title}</h2>"
            f"<p>{sub}</p>"
            f"{epi_h}"
            "</a>"
        )
    imprint = html.escape(CAT.get("imprint") or "Grimoire")
    shelf = html.escape(CAT.get("shelf") or "smut")
    robots = html.escape(CAT.get("robots") or "noindex, nofollow")
    page = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{imprint} — {shelf}</title>
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#12110f">
  <link rel="stylesheet" href="shelf.css">
</head>
<body>
  <main class="wrap">
    <div class="brand">{imprint} · {shelf}</div>
    <h1>On the shelf</h1>
    <p class="lede">One imprint. Each book is its own desk. More volumes later.</p>
    {"".join(cards)}
    <p class="foot">Not published. Local preview only. GitHub Pages is off.</p>
  </main>
</body>
</html>
"""
    OUT.write_text(page, encoding="utf-8")
    print(f"Wrote {OUT} ({len(CAT.get('books') or [])} books)")


if __name__ == "__main__":
    main()
