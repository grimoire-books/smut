# Scripts

Markdown is the source. HTML is generated. Do not hand-edit `index.html` or `plan/*.html`.

From `books/seven-year-king/`:

| Command | What it does |
|---------|----------------|
| `python scripts/build.py` | `chapters/*.md` + `docs/*.md` → `index.html` + `plan/`. **Writes a file only if the bytes changed.** |
| `python scripts/build.py --force` | Rewrite every generated file even if unchanged. |
| `python scripts/drop_in.py` | Replace chapter **bodies** from `~/Downloads/edits` (`04-joss.txt` → `ch-04-joss.md`). Keeps YAML desk cards. Newest file wins if two hit the same number. |
| `python scripts/drop_in.py --build` | Drop-in, then build. |

`desk_stamp.py` and `split_planning_bible.py` are one-shot. Do not re-run them on living files.

The clock is not stamped into HTML. A rebuild after a chapter drop-in should dirty `index.html` and maybe `docs/WORDCOUNT.md`, not thirty plan pages.
