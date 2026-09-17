# Drop-in and build

Markdown is the source. HTML is generated. Do not hand-edit `index.html` or `plan/*.html`.

Other Grok: this page is the naming law for fast Master drop-ins.

**The loop** (audit → apply → build → `git commit` → `git push`):

```
cd books/seven-year-king
python scripts/drop_in.py
python scripts/drop_in.py "C:\Users\MichaelThomson\Downloads\edits-pass3"
python scripts/drop_in.py "C:\Users\MichaelThomson\Downloads\seven-year-king-ch16-fp.zip"
```

A `.zip` is the same as a folder. Nested `edits-16/` inside the zip is fine. `__MACOSX` is ignored.

`--list` audits only (mapping + errors). Writes nothing. Git is not run.

If a file is named wrong, the script **stops before writing** and prints `ERROR` lines. Fix the names. Do not invent destinations.

If a drop-in is **under half** the words already on disk, that is an ERROR (regression — the other Grok cut the room). Under 80% is a WARN. `--allow-shrink` if Master meant a cut. A four-times swell is a WARN, not a stop.

---

## What goes where

| Filename in `Downloads\edits` | Lands on |
|-------------------------------|----------|
| `ch-04-joss.txt` | chapter **04** body. YAML desk card kept. |
| `04-joss.txt` | same (legacy). Leading digits = chapter **only if** no plan page has that stem. |
| `ch-06-the-candle.txt` | chapter **06** body. Title in the file can be `# Chapter 6` / `## The Candle`. |
| `plan-outline.txt` or `outline.txt` | `docs/OUTLINE.md` — **whole file**. |
| `plan-09-protagonist.txt` or `09-protagonist.txt` | `docs/09-protagonist.md` — **whole file**. Exact docs stem **beats** chapter number. |
| `plan-tracker.txt` / `TRACKER.txt` | `docs/TRACKER.md` |
| `docs\OUTLINE.md` (subfolder) | `docs/OUTLINE.md` |
| `chapters\04-joss.txt` (subfolder) | chapter 04 |

Windows copies (`ch-19-the-graph (1).txt`) are later passes. The script applies **oldest first, newest last**, so the `(1)` body is what stays. Same rule for three copies.

`.txt` or `.md`. Case does not matter. Hyphens and underscores are the same.

**Do not drop `WORDCOUNT.md`.** The build generates it.

**Notes files are not chapters.** `00-README-HOW-TO.txt`, `00-THIS-PASS.txt`, `README-THIS-PACK.md`, `CARD-PATCHES.md` are skipped. A leading `00-` on a note must not overwrite Last Day. Chapter drop-ins should be `ch-NN-…`.

**Do not drop PLANNING-BIBLE unless Master said to replace the snapshot.** Living law is OUTLINE / FREEZE / MAGIC / CONFLICTS.

---

## Chapters vs plan — the collision rule

`09-protagonist.txt` is the **plan page**, not chapter 9.

`09-the-mess.txt` or `ch-09.txt` is **chapter 9**.

`06-the-candle.txt` is **chapter 6** (no docs file with that stem).  
`06-factions.txt` is the **plan page** `docs/06-factions.md`.

When in doubt, prefix:

- chapters: `ch-NN-…`
- plan: `plan-…`

---

## What the script does

**Chapter:** keeps the YAML desk card (`status`, `room`, `job`, `happens`, `notes`). Replaces the prose after `# Chapter` / `## Title`. Strips a first line like `23 · Home` and a parenthetical note. Stamps `Drop-in: filename (date)` into notes.

**Plan:** replaces the whole markdown file. No YAML wrap. No clock stamp. Writes only if bytes changed.

**Build:** `python scripts/build.py` turns `chapters/*.md` + `docs/*.md` into `index.html` + `plan/*.html`. Writes a file **only if the bytes changed**. No wall-clock in the HTML.

---

## Commands

From `books/seven-year-king/`:

| Command | Job |
|---------|-----|
| `python scripts/drop_in.py` | Full loop: audit, apply, build, commit, push |
| `python scripts/drop_in.py PATH` | Same, from that folder **or .zip** |
| `python scripts/drop_in.py --list` | Audit only. Print OK / SKIP / ERROR. Write nothing |
| `python scripts/drop_in.py --no-push` | Commit locally, do not push |
| `python scripts/drop_in.py --no-git` | Apply + build only |
| `python scripts/drop_in.py --allow-shrink` | Permit a cut under half the on-disk words |
| `python scripts/build.py` | md → html, skip unchanged |

Default folder: `C:\Users\MichaelThomson\Downloads\edits`

---

## Paste this at another Grok

> Drop-ins: a folder or a `.zip`. From `books/seven-year-king/` run `python scripts/drop_in.py --list` then `python scripts/drop_in.py [path]`. That audits, applies, builds, commits, and pushes. Wrong names are ERROR and nothing is written.
>
> **Chapters:** `ch-04-joss.txt` or `04-joss.txt` → `chapters/**/ch-04-*.md`. YAML card kept; body replaced.
> **Plan:** `plan-outline.txt` or `outline.txt` or `09-protagonist.txt` → `docs/OUTLINE.md` / `docs/09-protagonist.md`. Whole file replaced.
> Exact docs stem wins over chapter number, so `09-protagonist.txt` is the plan page, not chapter 9. Use `ch-09-…` for chapter 9.
> Doubled files apply oldest first, newest last. Wrong names ERROR the run; nothing is written. README / HOW-TO / THIS-PASS / CARD-PATCHES are SKIP. Do not drop WORDCOUNT. Law: `docs/SCRIPTS.md`.
