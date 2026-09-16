"""Split Draft 07 into docs/*.md. Run from the book root."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "material" / "source" / "PLANNING-BIBLE-DRAFT-07.md"
DOCS = ROOT / "docs"

HEAD = re.compile(r"^\*\*(\d+)\.\s+(.+?)\*\*\s*$", re.M)

FILES = {
    1: "01-premise.md",
    2: "02-about.md",
    3: "03-influences.md",
    4: "04-cosmology.md",
    5: "05-magic.md",
    6: "06-factions.md",
    7: "07-morrigan.md",
    8: "08-geis.md",
    9: "09-protagonist.md",
    10: "10-cast.md",
    11: "11-prologue.md",
    12: "12-structure.md",
    13: "13-sex-and-violence.md",
    14: "14-style.md",
    15: "15-setting.md",
    16: "16-themes.md",
    17: "17-rules.md",
    18: "18-titles.md",
    19: "19-open.md",
    20: "20-next.md",
}


def clean(text: str) -> str:
    text = text.replace("\\'", "'")
    text = text.replace('\\"', '"')
    return text.replace("\r\n", "\n")


def heading(title: str) -> str:
    title = title.replace("\\", "")
    title = title.replace("---", "—")
    return title


def main() -> None:
    raw = clean(SRC.read_text(encoding="utf-8"))
    matches = list(HEAD.finditer(raw))
    if not matches:
        raise SystemExit("no numbered sections found")

    front = raw[: matches[0].start()].strip()
    sections: list[tuple[int, str, str]] = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        num = int(m.group(1))
        title = heading(m.group(2))
        body = raw[m.end() : end].strip()
        # drop trailing "End of Draft 07" from last section
        sections.append((num, title, body))

    DOCS.mkdir(exist_ok=True)

    full_bits = [front, ""]
    for num, title, body in sections:
        full_bits.append(f"## {num}. {title}\n\n{body}\n")
    full = "\n".join(full_bits).rstrip() + "\n"
    (DOCS / "PLANNING-BIBLE.md").write_text(full, encoding="utf-8")
    SRC.write_text(raw, encoding="utf-8")

    note = (
        "From **Planning Bible · Draft 07**. "
        "Canonical whole: [PLANNING-BIBLE.md](PLANNING-BIBLE.md). "
        "Word source: `material/source/Seven_Year_King_Planning_Bible.docx`.\n\n"
        "Locked decisions are marked **LOCK**. Open choices are marked **OPEN**.\n\n"
    )

    for num, title, body in sections:
        name = FILES[num]
        page = f"# {num}. {title}\n\n{note}{body}\n"
        (DOCS / name).write_text(page, encoding="utf-8")
        print(f"wrote docs/{name} ({len(body)} chars)")

    print(f"wrote docs/PLANNING-BIBLE.md ({len(full)} chars)")
    print(f"sections: {len(sections)}")


if __name__ == "__main__":
    main()
