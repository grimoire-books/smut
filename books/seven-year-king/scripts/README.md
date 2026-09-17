# Scripts

Canonical naming law (on the site): [docs/SCRIPTS.md](../docs/SCRIPTS.md) → `plan/scripts.html`.

Markdown is the source. HTML is generated. Do not hand-edit `index.html` or `plan/*.html`.

From `books/seven-year-king/`:

| Command | What it does |
|---------|----------------|
| `python scripts/drop_in.py` | **Dump loop.** Audit `~/Downloads/edits`, apply, build, `git commit`, `git push`. |
| `python scripts/drop_in.py PATH` | Same, from that folder **or .zip**. |
| `python scripts/drop_in.py --list` | Audit only. OK / SKIP / ERROR. Writes nothing. |
| `python scripts/drop_in.py --no-push` | Commit locally, do not push. |
| `python scripts/drop_in.py --no-git` | Apply + build, no git. |
| `python scripts/build.py` | md → html, skip unchanged. |

Bad names (`mystery.txt`, `ch-99-…`, `WORDCOUNT.md`, `00-THIS-PASS.txt` mistaken for Last Day) are **ERROR**. The run stops before writing.

`desk_stamp.py` and `split_planning_bible.py` are one-shot. Do not re-run them on living files.
