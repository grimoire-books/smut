"""Drop Master text into chapters or plan pages. Keep chapter YAML desk cards.

  python scripts/drop_in.py
  python scripts/drop_in.py "C:\\Users\\MichaelThomson\\Downloads\\edits"
  python scripts/drop_in.py --build
  python scripts/drop_in.py --list

Naming law (canonical on the site): docs/SCRIPTS.md

Chapters:  ch-04-joss.txt  or  04-joss.txt
Plan:      plan-outline.txt  or  outline.txt  or  09-protagonist.txt
           (exact docs stem wins over chapter number)

If two files hit the same destination (04-joss.txt then 04-joss (1).txt),
they are applied in LastWriteTime order: oldest first, newest last.
Do not drop WORDCOUNT.md — it is generated.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ROOT / "chapters"
DOCS = ROOT / "docs"
DEFAULT_IN = Path.home() / "Downloads" / "edits"

QUOTE_MAP = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201d": '"',
        "\u201c": '"',
        "\u2013": "—",
        "\u00a0": " ",
    }
)

COPY_RE = re.compile(r"\s*\(\d+\)\s*$")
CH_PREFIX_RE = re.compile(r"^ch-(\d{1,2})(?:[-_.]|$)", re.I)
PLAN_PREFIX_RE = re.compile(r"^(?:plan|doc|docs)[-_]", re.I)
NUM_RE = re.compile(r"^(\d{1,2})([-_.]|$)")
HEADING_RE = re.compile(r"^\d{1,2}\s*[·.\-–—]\s+\S")
PAREN_NOTE_RE = re.compile(r"^\([^)]+\)\s*$")
SKIP_DOCS = {"wordcount.md"}
SKIP_STEM = re.compile(r"readme|how-to|card-patches|this-pack", re.I)


def write_if_changed(path: Path, text: str) -> bool:
    if not text.endswith("\n"):
        text += "\n"
    new = text.replace("\r\n", "\n").encode("utf-8")
    if path.exists():
        old = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        if old == new:
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(new)
    return True


def stem_key(name: str) -> str:
    stem = Path(name).stem
    stem = COPY_RE.sub("", stem).strip()
    return stem


def docs_index() -> dict[str, Path]:
    idx: dict[str, Path] = {}
    for p in DOCS.glob("*.md"):
        idx[p.name.lower()] = p
        idx[p.stem.lower()] = p
        idx[p.stem.lower().replace("_", "-")] = p
    return idx


def match_doc(stem: str, idx: dict[str, Path]) -> Path | None:
    raw = PLAN_PREFIX_RE.sub("", stem).strip("-_ ")
    key = raw.lower().replace("_", "-")
    if key + ".md" in idx:
        return idx[key + ".md"]
    if key in idx:
        return idx[key]
    hits = [
        p
        for k, p in idx.items()
        if not k.endswith(".md") and (k == key or k.endswith("-" + key) or k.endswith("_" + key))
    ]
    uniq = {p.resolve(): p for p in hits}
    if len(uniq) == 1:
        return next(iter(uniq.values()))
    return None


def chapter_for(num: int) -> Path | None:
    hits = sorted(CHAPTERS.rglob(f"ch-{num:02d}-*.md"))
    if not hits:
        hits = sorted(CHAPTERS.rglob(f"ch-{num}-*.md"))
    return hits[0] if hits else None


def classify(path: Path, idx: dict[str, Path]) -> tuple[str, Path] | None:
    """Return ('chapter'|'plan', dest) or None."""
    rel_parts = {p.lower() for p in path.parts}
    stem = stem_key(path.name)
    parent = path.parent.name.lower()

    if parent in {"chapters", "chapter"} or "chapters" in rel_parts:
        m = CH_PREFIX_RE.match(stem) or NUM_RE.match(stem)
        if not m:
            return None
        dest = chapter_for(int(m.group(1)))
        return ("chapter", dest) if dest else None

    if parent in {"docs", "plan", "planning"}:
        dest = match_doc(stem, idx)
        return ("plan", dest) if dest else None

    if CH_PREFIX_RE.match(stem):
        dest = chapter_for(int(CH_PREFIX_RE.match(stem).group(1)))
        return ("chapter", dest) if dest else None

    if PLAN_PREFIX_RE.match(stem):
        dest = match_doc(stem, idx)
        return ("plan", dest) if dest else None

    dest = match_doc(stem, idx)
    if dest is not None:
        return ("plan", dest)

    m = NUM_RE.match(stem)
    if m:
        dest = chapter_for(int(m.group(1)))
        return ("chapter", dest) if dest else None
    return None


def iter_dropins(folder: Path) -> list[Path]:
    files: list[Path] = []
    for p in folder.rglob("*"):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".txt", ".md"}:
            continue
        if p.name.startswith("."):
            continue
        files.append(p)
    return files


def pick_jobs(folder: Path) -> dict[Path, list[tuple[str, Path]]]:
    """dest -> [(kind, src), ...] oldest LastWriteTime first, newest last."""
    idx = docs_index()
    buckets: dict[Path, list[tuple[str, Path, float]]] = {}
    for src in iter_dropins(folder):
        if SKIP_STEM.search(stem_key(src.name)):
            continue
        hit = classify(src, idx)
        if hit is None:
            continue
        kind, dest = hit
        if dest.name.lower() in SKIP_DOCS:
            continue
        buckets.setdefault(dest, []).append((kind, src, src.stat().st_mtime))
    out: dict[Path, list[tuple[str, Path]]] = {}
    for dest, items in buckets.items():
        items.sort(key=lambda t: (t[2], t[1].name))
        out[dest] = [(k, s) for k, s, _ in items]
    return out


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


def clean_chapter(text: str) -> str:
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


def clean_plan(text: str, dest_name: str) -> str:
    text = text.translate(QUOTE_MAP).replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines()
    if lines:
        first = lines[0].strip().strip("`").replace("\\", "/")
        if first.lower() in {
            dest_name.lower(),
            "docs/" + dest_name.lower(),
            dest_name.lower().replace(".md", ".txt"),
        }:
            lines = lines[1:]
            while lines and not lines[0].strip():
                lines = lines[1:]
    return "\n".join(lines).strip() + "\n"


def stamp_notes(yaml: str, src_name: str) -> str:
    line = f"  Drop-in: {src_name} ({datetime.now().strftime('%Y-%m-%d')})."
    if "Drop-in:" in yaml:
        return re.sub(r"  Drop-in:.*", line, yaml, count=1)
    if re.search(r"^notes:\s*\|", yaml, re.M) or re.search(r"^notes:", yaml, re.M):
        return yaml.rstrip() + "\n" + line + "\n"
    return yaml.rstrip() + "\nnotes: |\n" + line + "\n"


def install_chapter(src: Path, dest: Path) -> str:
    yaml, old_body = split_front_matter(dest.read_text(encoding="utf-8"))
    kicker, title, _old = split_headings(old_body)
    prose = clean_chapter(src.read_text(encoding="utf-8"))
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
    new = "".join(parts)
    changed = write_if_changed(dest, new)
    words = len(prose.split())
    tag = "OK " if changed else "same"
    return f"{tag} {src.name} → {dest.relative_to(ROOT)} ({words} words)"


def install_plan(src: Path, dest: Path) -> str:
    body = clean_plan(src.read_text(encoding="utf-8"), dest.name)
    changed = write_if_changed(dest, body)
    words = len(body.split())
    tag = "OK " if changed else "same"
    return f"{tag} {src.name} → {dest.relative_to(ROOT)} ({words} words)"


def install(folder: Path, dry: bool = False) -> list[str]:
    jobs = pick_jobs(folder)
    if not jobs:
        names = [p.name for p in iter_dropins(folder)]
        hint = f" saw: {', '.join(names)}" if names else " folder empty of .txt/.md"
        raise SystemExit(f"No drop-ins matched a chapter or plan page.{hint}")
    report: list[str] = []
    for dest in sorted(jobs, key=lambda p: str(p).lower()):
        chain = jobs[dest]
        for i, (kind, src) in enumerate(chain):
            last = i == len(chain) - 1
            note = "" if last else "  (then newer copy)"
            if dry:
                report.append(
                    f"DRY {kind:7} {src.name} → {dest.relative_to(ROOT)}{note}"
                )
                continue
            if kind == "chapter":
                line = install_chapter(src, dest)
            else:
                line = install_plan(src, dest)
            report.append(line + note)
    return report


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "folder",
        nargs="?",
        default=str(DEFAULT_IN),
        help="Folder of drop-ins (default: ~/Downloads/edits)",
    )
    p.add_argument("--build", action="store_true", help="Run scripts/build.py after")
    p.add_argument("--list", action="store_true", help="Show mapping, do not write")
    args = p.parse_args()
    folder = Path(args.folder)
    if not folder.is_dir():
        raise SystemExit(f"Not a folder: {folder}")
    for line in install(folder, dry=args.list):
        print(line)
    if args.build and not args.list:
        import subprocess

        subprocess.check_call([sys.executable, str(ROOT / "scripts" / "build.py")], cwd=ROOT)


if __name__ == "__main__":
    main()
