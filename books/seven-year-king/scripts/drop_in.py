"""Replace chapter bodies from a folder of Master drop-ins. Keep YAML desk cards.

  python scripts/drop_in.py
  python scripts/drop_in.py "C:\\Users\\MichaelThomson\\Downloads\\edits"
  python scripts/drop_in.py --build

Filenames: 04-joss.txt, 23-home-watersports.txt, 04-joss (1).txt.
Leading digits map to chapters/**/ch-NN-*.md.
If two files hit the same chapter, the newest wins.
Prose-only files keep the existing # / ## headings.
"""
from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
DEFAULT_IN = Path.home() / "Downloads" / "edits"

QUOTE_MAP = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "—",
        "\u00a0": " ",
    }
)

NUM_RE = re.compile(r"^(\d{1,2})")
HEADING_RE = re.compile(r"^\d{1,2}\s*[·.\-–—]\s+\S")
PAREN_NOTE_RE = re.compile(r"^\([^)]+\)\s*$")


def split_front_matter(raw: str) -> tuple[str, str]:
    if not raw.startswith("---"):
        return "", raw
    rest = raw[3:].lstrip("\n")
    end = rest.find("\n---")
    if end < 0:
        return "", raw
    yaml = rest[:end].rstrip() + "\n"
    body = rest[end + 4 :].lstrip("\n")
    return yaml, body


def split_headings(body: str) -> tuple[str, str, str]:
    lines = body.splitlines()
    kicker = ""
    title = ""
    i = 0
    if i < len(lines) and lines[i].startswith("# "):
        kicker = lines[i]
        i += 1
    if i < len(lines) and lines[i].startswith("## "):
        title = lines[i]
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    return kicker, title, "\n".join(lines[i:]).strip() + "\n"


def clean_drop_in(text: str) -> str:
    text = text.translate(QUOTE_MAP).replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines()
    i = 0
    if i < len(lines) and HEADING_RE.match(lines[i].strip()):
        i += 1
        if i < len(lines) and PAREN_NOTE_RE.match(lines[i].strip()):
            i += 1
        while i < len(lines) and not lines[i].strip():
            i += 1
    return "\n".join(lines[i:]).strip() + "\n"


def chapter_for(num: int) -> Path | None:
    hits = sorted(CHAPTERS.rglob(f"ch-{num:02d}-*.md"))
    if not hits:
        hits = sorted(CHAPTERS.rglob(f"ch-{num}-*.md"))
    return hits[0] if hits else None


def stamp_notes(yaml: str, src_name: str) -> str:
    line = f"  Drop-in: {src_name} ({datetime.now().strftime('%Y-%m-%d')})."
    if "Drop-in:" in yaml:
        yaml = re.sub(r"  Drop-in:.*", line, yaml, count=1)
        return yaml
    if re.search(r"^notes:\s*\|", yaml, re.M):
        return yaml.rstrip() + "\n" + line + "\n"
    if re.search(r"^notes:", yaml, re.M):
        return yaml.rstrip() + "\n" + line + "\n"
    return yaml.rstrip() + "\nnotes: |\n" + line + "\n"


def pick_sources(folder: Path) -> dict[int, Path]:
    chosen: dict[int, Path] = {}
    for path in folder.iterdir():
        if not path.is_file() or path.suffix.lower() != ".txt":
            continue
        m = NUM_RE.match(path.name)
        if not m:
            continue
        num = int(m.group(1))
        prev = chosen.get(num)
        if prev is None or path.stat().st_mtime >= prev.stat().st_mtime:
            chosen[num] = path
    return chosen


def install(folder: Path) -> list[str]:
    report: list[str] = []
    chosen = pick_sources(folder)
    if not chosen:
        raise SystemExit(f"No NN-*.txt drop-ins in {folder}")
    for num in sorted(chosen):
        src = chosen[num]
        dest = chapter_for(num)
        if dest is None:
            report.append(f"SKIP {src.name}: no ch-{num:02d}-*.md")
            continue
        yaml, old_body = split_front_matter(dest.read_text(encoding="utf-8"))
        kicker, title, _old_prose = split_headings(old_body)
        prose = clean_drop_in(src.read_text(encoding="utf-8"))
        dk, dt, rest = split_headings(prose)
        if dk or dt:
            kicker = dk or kicker
            title = dt or title
            prose = rest
        yaml = stamp_notes(yaml, src.name)
        parts = ["---\n", yaml]
        if not yaml.endswith("\n"):
            parts.append("\n")
        parts.append("---\n\n")
        if kicker:
            parts.append(kicker + "\n")
        if title:
            parts.append(title + "\n")
        parts.append("\n")
        parts.append(prose if prose.endswith("\n") else prose + "\n")
        dest.write_text("".join(parts), encoding="utf-8")
        words = len(prose.split())
        report.append(f"OK  {src.name} → {dest.relative_to(ROOT)} ({words} words)")
    return report


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "folder",
        nargs="?",
        default=str(DEFAULT_IN),
        help="Folder of NN-*.txt drop-ins (default: ~/Downloads/edits)",
    )
    p.add_argument("--build", action="store_true", help="Run scripts/build.py after")
    args = p.parse_args()
    folder = Path(args.folder)
    if not folder.is_dir():
        raise SystemExit(f"Not a folder: {folder}")
    for line in install(folder):
        print(line)
    if args.build:
        import subprocess
        import sys

        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "build.py")], cwd=ROOT)


if __name__ == "__main__":
    main()
