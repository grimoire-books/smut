"""Build the local book reader from chapters/*.md + book.json.

Markdown in, HTML out. Desk cards from YAML. Plan pages from docs/.

Writes a file only when its bytes change. No wall-clock in the HTML, so a
rebuild does not dirty thirty plan pages for a timestamp.

  python scripts/build.py
  python scripts/build.py --force
"""
from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
DOCS = ROOT / "docs"
OUT = ROOT / "index.html"
PLAN_DIR = ROOT / "plan"
META = ROOT / "book.json"

# Plan pages: slug, source markdown, nav label, hub blurb
PLAN_GROUPS: list[tuple[str, list[tuple[str, str, str, str]]]] = [
    (
        "Desk",
        [
            ("outline", "OUTLINE.md", "Trilogy outline", "Lock object — all three books, sequence + cards. No prose"),
            ("freeze", "FREEZE.md", "Freeze law", "AXIOM / HINGE / ELEMENT / CARD / EXAMPLE. Clay is magic"),
            ("conflicts", "CONFLICTS.md", "Conflicts", "Vale belief, sex map, superseded spines"),
            ("objective", "OBJECTIVE.md", "Objective", "North star — premise, thesis, tone, key locks"),
            ("tracker", "TRACKER.md", "Tracker", "UNLOCKED. Next is Master locks the outline"),
            ("length", "LENGTH.md", "Length", "Centre lines, bands, floors. Do not write toward the number"),
            ("wordcount", "WORDCOUNT.md", "Wordcount", "Live counts from the last build"),
            ("draft-choices", "DRAFT-CHOICES.md", "Draft choices", "Provisionals so the page can happen"),
            ("book1-remaining", "BOOK1-REMAINING.md", "Book 1 remaining", "SUPERSEDED. Living jobs live in the outline"),
            ("scripts", "SCRIPTS.md", "Drop-in / scripts", "How to name files. Chapters vs plan. Other Grok reads this"),
        ],
    ),
    (
        "Bible · Draft 07",
        [
            ("bible", "PLANNING-BIBLE.md", "Full bible", "Draft 07 in one file"),
            ("01-premise", "01-premise.md", "1. Premise", "One-page premise"),
            ("02-about", "02-about.md", "2. About", "What the book is actually about"),
            ("03-influences", "03-influences.md", "3. Influences", "Steal / discard"),
            ("04-cosmology", "04-cosmology.md", "4. Cosmology", "Two realms, clay / the between, the valve"),
            ("05-magic", "05-magic.md", "5. Magic", "Clay: physics, belief, pipe, five verbs, gun rule"),
            ("06-factions", "06-factions.md", "6. Factions", "Houses, Vale belief, witches, packs"),
            ("07-morrigan", "07-morrigan.md", "7. Morrígan", "She never pretends the leash is love"),
            ("08-geis", "08-geis.md", "8. Geis", "Horned God, two clocks"),
            ("09-protagonist", "09-protagonist.md", "9. Protagonist", "Unnamed man, control ladder"),
            ("10-cast", "10-cast.md", "10. Cast", "Names and fates"),
            ("11-prologue", "11-prologue.md", "11. Prologue", "Beat sheet"),
            ("12-structure", "12-structure.md", "12. Structure", "Trilogy spine"),
            ("13-sex-and-violence", "13-sex-and-violence.md", "13. Sex and violence", "Design"),
            ("14-style", "14-style.md", "14. Style", "Tense, POV, register"),
            ("15-setting", "15-setting.md", "15. Setting", "Modern Britain and Ireland"),
            ("16-themes", "16-themes.md", "16. Themes", "Themes"),
            ("17-rules", "17-rules.md", "17. Rules", "Hard rules for the draft"),
            ("18-titles", "18-titles.md", "18. Titles", "Working titles"),
            ("19-open", "19-open.md", "19. Open", "Graveyard. Leftovers only"),
            ("20-next", "20-next.md", "20. Next", "Current next. Master locks the outline"),
        ],
    ),
]

FILE_TO_SLUG: dict[str, str] = {}
for _g, pages in PLAN_GROUPS:
    for slug, src, _label, _blurb in pages:
        FILE_TO_SLUG[src] = f"{slug}.html"
FILE_TO_SLUG["README.md"] = "index.html"
FILE_TO_SLUG["PLANNING-BIBLE.md"] = "bible.html"

_FORCE = False
_written = 0
_skipped = 0


def write_if_changed(path: Path, text: str) -> bool:
    """Write UTF-8 LF only if content differs. Skip timestamp-only churn."""
    global _written, _skipped
    if not text.endswith("\n"):
        text += "\n"
    new = text.replace("\r\n", "\n").encode("utf-8")
    if not _FORCE and path.exists():
        old = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if old == new:
            _skipped += 1
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(new)
    _written += 1
    return True


def volume_of(path: Path) -> tuple[int, str]:
    parts = {p.lower() for p in path.parts}
    if "book-1-shadow" in parts or "book-1" in parts:
        return 1, "Shadow"
    if "book-2-green" in parts or "book-2" in parts:
        return 2, "Green"
    if "book-3-crow" in parts or "book-3" in parts:
        return 3, "Crow"
    return 1, "Shadow"


def parse_front_matter(raw: str) -> tuple[dict, str]:
    desk = {
        "status": "draft",
        "room": "",
        "job": "",
        "happens": [],
        "notes": "",
    }
    if not raw.startswith("---"):
        return desk, raw
    rest = raw[3:].lstrip("\n")
    end = rest.find("\n---")
    if end < 0:
        return desk, raw
    block = rest[:end]
    body = rest[end + 4 :].lstrip("\n")

    key = None
    notes: list[str] = []
    for line in block.splitlines():
        if line.startswith("status:"):
            key = "status"
            desk["status"] = line.split(":", 1)[1].strip()
        elif line.startswith("room:"):
            key = "room"
            desk["room"] = line.split(":", 1)[1].strip()
        elif line.startswith("job:"):
            key = "job"
            desk["job"] = line.split(":", 1)[1].strip()
        elif line.startswith("happens:"):
            key = "happens"
        elif line.startswith("notes:"):
            key = "notes"
            tail = line.split(":", 1)[1].strip()
            if tail and tail not in ("|", ">"):
                notes.append(tail)
        elif key == "happens" and line.strip().startswith("- "):
            desk["happens"].append(line.strip()[2:].strip())
        elif key == "job" and (line.startswith("  ") or line.startswith(" ")):
            desk["job"] = (desk["job"] + " " + line.strip()).strip()
        elif key == "notes":
            notes.append(line[2:] if line.startswith("  ") else line)
    desk["notes"] = "\n".join(notes).strip()
    return desk, body


def parse_chapter(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    desk, raw = parse_front_matter(raw)
    lines = raw.splitlines()
    num = 0
    m = re.search(r"ch-(\d+)", path.name)
    if m:
        num = int(m.group(1))
    title = path.stem
    kicker = f"Chapter {num}"
    i = 0
    if lines and lines[0].startswith("# "):
        kicker = lines[0][2:].strip()
        i = 1
    if i < len(lines) and lines[i].startswith("## "):
        title = lines[i][3:].strip()
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    body = "\n".join(lines[i:]).strip()
    vol, vol_name = volume_of(path)
    return {
        "num": num,
        "title": title,
        "kicker": kicker,
        "body": body,
        "path": path.name,
        "volume": vol,
        "volume_name": vol_name,
        "words": len(body.split()),
        "desk": desk,
    }


def chapter_files() -> list[Path]:
    nested = list(CHAPTERS.rglob("ch-*.md"))
    files = nested if nested else list(CHAPTERS.glob("ch-*.md"))
    return sorted(files, key=lambda p: (volume_of(p)[0], parse_chapter(p)["num"]))


def write_wordcount(book: dict, chapters: list[dict], total_words: int) -> None:
    length = book.get("length") or {}
    books = {b["number"]: b for b in length.get("books", [])}
    by_vol: dict[int, int] = {}
    for c in chapters:
        by_vol[c["volume"]] = by_vol.get(c["volume"], 0) + c["words"]
    lines = [
        "# Wordcount",
        "",
        "Generated by `python scripts/build.py`. Law: [LENGTH.md](LENGTH.md).",
        "",
        "Do not write toward the centre line. Write the locked rooms.",
        "",
        f"Series so far: **{total_words:,}** / 400–450k",
        "",
        "| Book | Words | Centre | Band | Floor |",
        "|------|------:|-------:|------|------:|",
    ]
    for n, name in ((1, "Shadow"), (2, "Green"), (3, "Crow")):
        meta = books.get(n, {})
        w = by_vol.get(n, 0)
        centre = meta.get("centre", 0)
        band = meta.get("band", [0, 0])
        band_s = f"{band[0]//1000}–{band[1]//1000}k" if band[1] else "—"
        centre_s = f"{centre//1000}k" if centre else "—"
        lines.append(
            f"| {n} · {name} | {w:,} | {centre_s} | {band_s} | 110k |"
        )
    lines += [
        "",
        "## Chapters",
        "",
        "| Vol | # | Title | Job | Status | Words |",
        "|-----|---|-------|-----|--------|------:|",
    ]
    for c in chapters:
        job = (c["desk"].get("job") or "").replace("|", "/")
        if len(job) > 80:
            job = job[:77] + "…"
        lines.append(
            f"| {c['volume']} | {c['num']} | {c['title']} | {job} | {c['desk'].get('status', '')} | {c['words']:,} |"
        )
    write_if_changed(ROOT / "docs" / "WORDCOUNT.md", "\n".join(lines) + "\n")


def md_lite_to_html(text: str) -> str:
    fences: list[str] = []

    def save_fence(m: re.Match) -> str:
        fences.append(m.group(1))
        return f"\x00FENCE{len(fences) - 1}\x00"

    text = re.sub(r"```[^\n]*\n(.*?)```", save_fence, text, flags=re.DOTALL)
    parts = re.split(r"\n\s*\n", text)
    out: list[str] = []
    for part in parts:
        p = part.strip()
        if not p:
            continue
        if p.strip() == "---":
            out.append("<hr>")
            continue
        if p.startswith("#"):
            p = re.sub(r"^#+\s*", "", p)
        esc = html.escape(p)
        esc = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", esc)
        esc = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", esc)
        esc = re.sub(r"`([^`]+)`", r"<code>\1</code>", esc)
        esc = esc.replace("\n", "<br>\n")
        for i, code in enumerate(fences):
            esc = esc.replace(
                f"\x00FENCE{i}\x00",
                f"<pre><code>{html.escape(code.rstrip())}</code></pre>",
            )
        if esc.startswith("<pre>"):
            out.append(esc)
        else:
            out.append(f"<p>{esc}</p>")
    return "\n".join(out)


def rewrite_doc_href(href: str) -> str:
    if href.startswith(("http://", "https://", "mailto:", "#")):
        return href
    path, _, frag = href.partition("#")
    name = Path(path).name
    slug = FILE_TO_SLUG.get(name)
    if slug:
        return f"{slug}#{frag}" if frag else slug
    return href


def inline_md(text: str) -> str:
    def esc_fmt(s: str) -> str:
        s = html.escape(s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
        s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
        s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
        s = re.sub(r"\bLOCK\b", r'<span class="lock">LOCK</span>', s)
        s = re.sub(r"\bOPEN\b", r'<span class="open">OPEN</span>', s)
        return s

    parts: list[str] = []
    pos = 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        parts.append(esc_fmt(text[pos : m.start()]))
        label, href = m.group(1), rewrite_doc_href(m.group(2))
        parts.append(f'<a href="{html.escape(href)}">{html.escape(label)}</a>')
        pos = m.end()
    parts.append(esc_fmt(text[pos:]))
    return "".join(parts)


def _is_pipe_table(lines: list[str]) -> bool:
    return len(lines) >= 2 and "|" in lines[0] and re.match(r"^\s*\|?\s*[-:| ]+\s*$", lines[1] or "")


def _is_grid_rule(line: str) -> bool:
    s = line.strip()
    return len(s) >= 8 and set(s) <= set("-+| ") and "-" in s


def _pipe_table(lines: list[str]) -> str:
    rows = []
    for i, line in enumerate(lines):
        if i == 1 and re.match(r"^\s*\|?\s*[-:| ]+\s*$", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        tag = "th" if i == 0 else "td"
        rows.append("<tr>" + "".join(f"<{tag}>{inline_md(c)}</{tag}>" for c in cells) + "</tr>")
    return f'<div class="plan-table"><table>{"".join(rows)}</table></div>'


def md_docs_to_html(text: str) -> str:
    """Richer markdown for planning pages: headings, lists, tables, quotes, tasks."""
    raw_lines = text.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    i = 0
    n = len(raw_lines)

    def take_while(pred) -> list[str]:
        nonlocal i
        block = []
        while i < n and pred(raw_lines[i]):
            block.append(raw_lines[i])
            i += 1
        return block

    while i < n:
        line = raw_lines[i]
        if not line.strip():
            i += 1
            continue
        if line.strip() == "---":
            out.append("<hr>")
            i += 1
            continue
        hm = re.match(r"^(#{1,4})\s+(.*)$", line)
        if hm:
            level = len(hm.group(1))
            out.append(f"<h{level}>{inline_md(hm.group(2).strip())}</h{level}>")
            i += 1
            continue
        if line.lstrip().startswith(">"):
            qs = take_while(lambda L: L.lstrip().startswith(">") or (L.strip() == "" and i + 1 < n and raw_lines[i + 1].lstrip().startswith(">")))
            body = "<br>\n".join(inline_md(re.sub(r"^\s*>\s?", "", q)) for q in qs if q.strip())
            out.append(f"<blockquote>{body}</blockquote>")
            continue
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?\s*[-:| ]+\s*$", raw_lines[i + 1]):
            tbl = take_while(lambda L: "|" in L)
            out.append(_pipe_table(tbl))
            continue
        if _is_grid_rule(line):
            start = i
            i += 1
            while i < n:
                L = raw_lines[i]
                if re.match(r"^#{1,4}\s+", L) or re.match(r"^\s*[-*]\s+", L):
                    break
                if not L.strip():
                    nxt = raw_lines[i + 1] if i + 1 < n else ""
                    if nxt.strip() and not nxt.startswith("  ") and not _is_grid_rule(nxt):
                        break
                i += 1
            grid = raw_lines[start:i]
            while grid and not grid[-1].strip():
                grid.pop()
            out.append('<pre class="plan-grid">' + html.escape("\n".join(grid)) + "</pre>")
            continue
        if re.match(r"^\s*[-*]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < n:
                L = raw_lines[i]
                if re.match(r"^\s*[-*]\s+", L) or re.match(r"^\s*\d+\.\s+", L) or (L.startswith("  ") and L.strip()):
                    items.append(L)
                    i += 1
                    continue
                if not L.strip() and i + 1 < n and (
                    re.match(r"^\s*[-*]\s+", raw_lines[i + 1]) or re.match(r"^\s*\d+\.\s+", raw_lines[i + 1])
                ):
                    i += 1
                    continue
                break
            lis = []
            for it in items:
                m = re.match(r"^\s*[-*]\s+\[([ xX])\]\s+(.*)$", it)
                if m:
                    chk = "checked" if m.group(1).lower() == "x" else ""
                    lis.append(
                        f'<li class="task"><input type="checkbox" disabled {chk}> {inline_md(m.group(2))}</li>'
                    )
                    continue
                m = re.match(r"^\s*[-*]\s+(.*)$", it)
                if m:
                    lis.append(f"<li>{inline_md(m.group(1))}</li>")
                    continue
                m = re.match(r"^\s*\d+\.\s+(.*)$", it)
                if m:
                    lis.append(f"<li>{inline_md(m.group(1))}</li>")
                else:
                    if lis:
                        lis[-1] = lis[-1][:-5] + " " + inline_md(it.strip()) + "</li>"
            ordered = bool(re.match(r"^\s*\d+\.", items[0]))
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>{''.join(lis)}</{tag}>")
            continue
        para = [line]
        i += 1
        while i < n and raw_lines[i].strip() and not re.match(r"^(#{1,4})\s+", raw_lines[i]) and not raw_lines[i].lstrip().startswith((">", "-", "*")) and not _is_grid_rule(raw_lines[i]) and raw_lines[i].strip() != "---":
            if "|" in raw_lines[i] and i + 1 < n and re.match(r"^\s*\|?\s*[-:| ]+\s*$", raw_lines[i + 1]):
                break
            para.append(raw_lines[i])
            i += 1
        out.append("<p>" + "<br>\n".join(inline_md(p) for p in para) + "</p>")
    return "\n".join(out)


def desk_html(c: dict) -> str:
    d = c["desk"]
    if not d.get("job") and not d.get("happens") and not d.get("notes"):
        return (
            '<aside class="desk">'
            "<p class=\"desk-empty\">No desk card yet. Add YAML front matter "
            "(job, happens, notes) at the top of the chapter file.</p>"
            "</aside>"
        )
    happens = "".join(f"<li>{html.escape(h)}</li>" for h in d.get("happens") or [])
    happens_h = (
        f'<h3 class="desk-k">What happens</h3><ul class="desk-happens">{happens}</ul>'
        if happens
        else ""
    )
    notes_h = ""
    if d.get("notes"):
        notes_h = (
            '<h3 class="desk-k">Notes</h3>'
            f'<div class="desk-notes">{md_lite_to_html(d["notes"])}</div>'
        )
    room = html.escape(d["room"]) if d.get("room") else ""
    room_html = f'<span class="desk-room">{room}</span>' if room else ""
    status = html.escape(d.get("status") or "draft")
    return f"""<aside class="desk" aria-label="Desk card">
      <div class="desk-top">
        <span class="desk-status s-{html.escape(d.get('status') or 'draft')}">{status}</span>
        {room_html}
      </div>
      <h3 class="desk-k">Job</h3>
      <p class="desk-job">{html.escape(d.get("job") or "")}</p>
      {happens_h}
      {notes_h}
    </aside>"""


def spine_html(chapters: list[dict]) -> str:
    rows = []
    for c in chapters:
        job = html.escape(c["desk"].get("job") or "—")
        st = html.escape(c["desk"].get("status") or "draft")
        cid = f"ch-{c['num']:02d}"
        rows.append(
            "<tr>"
            f'<td class="sp-n">{c["num"]}</td>'
            f'<td class="sp-t"><a href="#{cid}">{html.escape(c["title"])}</a></td>'
            f'<td class="sp-j">{job}</td>'
            f'<td class="sp-s">{st}</td>'
            f'<td class="sp-w">{c["words"]:,}</td>'
            "</tr>"
        )
    return f"""<section class="spine" id="spine" aria-label="Chapter spine">
      <h2>Spine</h2>
      <p class="spine-lead">Top-down. The job of each chapter without the prose. Click through to the room.</p>
      <div class="spine-wrap">
      <table>
        <thead>
          <tr><th>#</th><th>Title</th><th>Job</th><th>Status</th><th>Words</th></tr>
        </thead>
        <tbody>
          {"".join(rows)}
        </tbody>
      </table>
      </div>
    </section>"""


def plan_nav_html(current: str) -> str:
    bits = []
    for group, pages in PLAN_GROUPS:
        bits.append(f'<p class="nav-group">{html.escape(group)}</p>')
        for slug, _src, label, _blurb in pages:
            href = "index.html" if slug == "hub" else f"{slug}.html"
            on = ' aria-current="page"' if slug == current else ""
            bits.append(
                f'<a class="nav-item" href="{href}"{on}>'
                f'<span class="t">{html.escape(label)}</span></a>'
            )
    return "".join(bits)


def plan_page(
    book: dict,
    slug: str,
    title: str,
    kicker: str,
    body_html: str,
) -> str:
    book_title = html.escape(book.get("title") or "Untitled")
    robots = html.escape(book.get("robots") or "noindex, nofollow, noarchive")
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} — {book_title}</title>
  <meta name="robots" content="{robots}">
  <meta name="theme-color" content="#12110f">
  <link rel="stylesheet" href="../reader.css">
  <script defer src="../reader.js"></script>
</head>
<body class="plan-page">
  <a class="skip" href="#main">Skip to plan</a>
  <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="chapter-side">
    Plan
  </button>
  <div class="nav-backdrop" id="nav-backdrop" hidden></div>
  <aside class="side" id="chapter-side" aria-label="Plan navigation">
    <button type="button" class="nav-close" id="nav-close" aria-label="Close">×</button>
    <div class="side-head">
      <div class="brand"><a href="../../../index.html">grimoire · smut</a></div>
      <h1>{book_title}</h1>
      <p class="sub">Planning desk</p>
      <p class="spine-link"><a href="../index.html">The book →</a></p>
      <p class="spine-link"><a href="index.html">Plan hub</a></p>
    </div>
    <nav class="nav" aria-label="Plan">
      {plan_nav_html(slug)}
    </nav>
  </aside>
  <div class="shell">
    <div class="side-spacer" aria-hidden="true"></div>
    <main class="main plan-main" id="main">
      <header class="hero">
        <div class="badge">{html.escape(kicker)}</div>
        <h1>{html.escape(title)}</h1>
      </header>
      <div class="plan-body">
        {body_html}
      </div>
      <footer class="foot">
        {book_title} · plan · markdown in docs/
      </footer>
    </main>
  </div>
  <a class="top" href="#">Top</a>
</body>
</html>
"""


def build_plan_hub(book: dict) -> str:
    groups_html = []
    for group, pages in PLAN_GROUPS:
        cards = []
        for slug, _src, label, blurb in pages:
            cards.append(
                f'<a class="plan-card" href="{html.escape(slug)}.html">'
                f"<h2>{html.escape(label)}</h2>"
                f"<p>{html.escape(blurb)}</p>"
                "</a>"
            )
        groups_html.append(
            f"<h2 class=\"plan-group-title\">{html.escape(group)}</h2>"
            f'<div class="plan-cards">{"".join(cards)}</div>'
        )
    body = (
        "<p class=\"plan-lead\">Living desk first. Draft 07 is a snapshot. "
        "Chapter summaries stay on the book. Cosmology, geis, sex design, rules, "
        "tracker — to read with the eyes, not only in markdown.</p>"
        + "".join(groups_html)
    )
    return plan_page(book, "hub", "Plan", "desk + bible", body)


def build_plan(book: dict) -> None:
    PLAN_DIR.mkdir(exist_ok=True)
    write_if_changed(PLAN_DIR / "index.html", build_plan_hub(book))
    n = 1
    for _group, pages in PLAN_GROUPS:
        for slug, src, label, _blurb in pages:
            path = DOCS / src
            if not path.exists():
                print(f"missing plan source: {src}")
                continue
            raw = path.read_text(encoding="utf-8")
            html_body = md_docs_to_html(raw)
            html_body = re.sub(r"^<h1>.*?</h1>\s*", "", html_body, count=1)
            write_if_changed(
                PLAN_DIR / f"{slug}.html",
                plan_page(book, slug, label, "planning", html_body),
            )
            n += 1
    print(f"Plan pages considered: {n} in {PLAN_DIR}")


def build() -> Path:
    book = json.loads(META.read_text(encoding="utf-8"))
    files = chapter_files()
    if not files:
        raise SystemExit(f"No chapters in {CHAPTERS}")
    chapters = [parse_chapter(p) for p in files]
    total_words = sum(c["words"] for c in chapters)
    write_wordcount(book, chapters, total_words)
    shadow = sum(c["words"] for c in chapters if c["volume"] == 1)
    target = ((book.get("length") or {}).get("books") or [{}])[0].get("centre", 125000)

    title = book.get("title") or "Untitled"
    author = book.get("author") or ""
    subtitle = book.get("subtitle") or ""
    epigraph = book.get("epigraph") or ""
    badge = book.get("badge") or "draft"
    robots = book.get("robots") or "noindex, nofollow, noarchive"
    status = book.get("status") or "draft"
    hero_line = subtitle or epigraph or author

    nav: list[str] = []
    sections: list[str] = []
    for c in chapters:
        cid = f"ch-{c['num']:02d}"
        nav.append(
            f'<a class="nav-item" href="#{cid}">'
            f'<span class="n">{c["num"]}</span>'
            f'<span class="t">{html.escape(c["title"])}</span></a>'
        )
        body_html = md_lite_to_html(c["body"])
        w = c["words"]
        sections.append(
            f'<article class="chapter" id="{cid}">'
            f'<header class="ch-head">'
            f'<p class="kicker">{html.escape(c["kicker"])}</p>'
            f'<h2>{html.escape(c["title"])}</h2>'
            f'<p class="meta">{w:,} words · {html.escape(c["desk"].get("status") or "draft")}</p>'
            f"</header>"
            f"{desk_html(c)}"
            f'<div class="body">{body_html}</div>'
            f"</article>"
        )

    epigraph_html = ""
    if epigraph:
        epigraph_html = f'<div class="epigraph">{html.escape(epigraph)}</div>'

    sub_html = html.escape(author)
    if subtitle:
        sub_html = html.escape(subtitle)

    page = f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <meta name="description" content="{html.escape(title)}{(' — ' + author) if author else ''}">
  <meta name="robots" content="{html.escape(robots)}">
  <meta name="theme-color" content="#12110f">
  <link rel="stylesheet" href="reader.css">
  <script defer src="reader.js"></script>
</head>
<body data-mode="both">
  <a class="skip" href="#main">Skip to reading</a>
  <button type="button" class="nav-toggle" id="nav-toggle" aria-expanded="false" aria-controls="chapter-side">
    Chapters
  </button>
  <div class="nav-backdrop" id="nav-backdrop" hidden></div>
  <aside class="side" id="chapter-side" aria-label="Chapter navigation">
    <button type="button" class="nav-close" id="nav-close" aria-label="Close chapters">×</button>
    <div class="side-head">
      <div class="brand"><a href="../../index.html">grimoire · smut</a></div>
      <h1>{html.escape(title)}</h1>
      <p class="sub">{sub_html}</p>
      {epigraph_html}
      <div class="stats">
        <div><strong>{len(chapters)}</strong> chapter{"s" if len(chapters) != 1 else ""}</div>
        <div><strong>{shadow:,}</strong> / {target:,} Book 1</div>
        <div><strong>{total_words:,}</strong> series</div>
      </div>
      <div class="mode" role="group" aria-label="Page mode">
        <button type="button" data-mode="desk">Desk</button>
        <button type="button" data-mode="both" class="on">Both</button>
        <button type="button" data-mode="prose">Prose</button>
      </div>
      <p class="mode-hint">Desk = spine + cards. Prose = the book. Both = how we edit.</p>
      <p class="spine-link"><a href="#spine">Spine ↓</a> · <a href="plan/index.html">Plan →</a></p>
    </div>
    <nav class="nav" aria-label="Chapters">
      {"".join(nav)}
    </nav>
  </aside>
  <div class="shell">
    <div class="side-spacer" aria-hidden="true"></div>
    <main class="main" id="main">
      <header class="hero">
        <div class="badge">{html.escape(badge)}</div>
        <h1>{html.escape(title)}</h1>
        <p>{html.escape(hero_line)}</p>
      </header>
      {spine_html(chapters)}
      {"".join(sections)}
      <footer class="foot">
        {html.escape(title)} · {html.escape(author)} · {html.escape(status)}.
        <a href="plan/index.html">Full plan</a> · desk cards on each chapter.
      </footer>
    </main>
  </div>
  <a class="top" href="#">Top</a>
</body>
</html>
"""
    write_if_changed(OUT, page)
    build_plan(book)
    print(f"Wrote {_written} file(s), skipped {_skipped} unchanged")
    print(f"Chapters: {len(chapters)}")
    print(f"Book 1: {shadow:,} / {target:,}")
    print(f"Series: {total_words:,} / 400–450k")
    return OUT


def main() -> None:
    global _FORCE
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--force",
        action="store_true",
        help="Rewrite every HTML file even if bytes match",
    )
    args = p.parse_args()
    _FORCE = args.force
    build()


if __name__ == "__main__":
    main()
