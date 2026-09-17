# Drop-in and build

Markdown is the source. HTML is generated. Do not hand-edit `index.html` or `plan/*.html`.

Other Grok: this page is the naming law for fast Master drop-ins. Put files in `C:\Users\MichaelThomson\Downloads\edits`, then:

```
cd books/seven-year-king
python scripts/drop_in.py --build
```

`--list` prints the mapping and writes nothing.

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

Windows copies (`04-joss (1).txt`, `outline (1).txt`) are fine. Newest file wins if two hit the same destination.

`.txt` or `.md`. Case does not matter. Hyphens and underscores are the same.

**Do not drop `WORDCOUNT.md`.** The build generates it.

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
| `python scripts/drop_in.py --list` | Show where each file would go |
| `python scripts/drop_in.py --build` | Install, then rebuild the desk |
| `python scripts/build.py` | md → html, skip unchanged |
| `python scripts/build.py --force` | Rewrite every generated file |

Default folder: `C:\Users\MichaelThomson\Downloads\edits`

---

## Paste this at another Grok

> Drop-ins live in `C:\Users\MichaelThomson\Downloads\edits`. Run `python scripts/drop_in.py --build` from `books/seven-year-king/`.
>
> **Chapters:** `ch-04-joss.txt` or `04-joss.txt` → `chapters/**/ch-04-*.md`. YAML card kept; body replaced.
> **Plan:** `plan-outline.txt` or `outline.txt` or `09-protagonist.txt` → `docs/OUTLINE.md` / `docs/09-protagonist.md`. Whole file replaced.
> Exact docs stem wins over chapter number, so `09-protagonist.txt` is the plan page, not chapter 9. Use `ch-09-…` for chapter 9.
> Newest `(1)` copy wins. Do not drop WORDCOUNT. Law: `docs/SCRIPTS.md` on the plan hub.
