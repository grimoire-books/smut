# Scripts

Canonical naming law (on the site): [docs/SCRIPTS.md](../docs/SCRIPTS.md) → `plan/scripts.html`.

Markdown is the source. HTML is generated. Do not hand-edit `index.html` or `plan/*.html`.

From `books/seven-year-king/`:

| Command | What it does |
|---------|----------------|
| `python scripts/drop_in.py --list` | Map `~/Downloads/edits` files to chapters or `docs/` — write nothing |
| `python scripts/drop_in.py --build` | Install drop-ins, then build |
| `python scripts/build.py` | `chapters/*.md` + `docs/*.md` → `index.html` + `plan/`. **Writes only if bytes changed.** |
| `python scripts/build.py --force` | Rewrite every generated file even if unchanged |

**Chapters:** `ch-04-joss.txt` (YAML kept). **Plan:** `plan-outline.txt` or `09-protagonist.txt` (whole file). Exact docs stem beats chapter number.

`desk_stamp.py` and `split_planning_bible.py` are one-shot. Do not re-run them on living files.
