# The Seven-Year King

Working title. A smut epic fantasy set in modern Britain and Ireland. Book 1 in draft.

One volume on the **Grimoire smut** shelf. Not a Tyneside brand.

```
C:\Users\MichaelThomson\source\smut\books\seven-year-king
```

Repo: [grimoire-books/smut](https://github.com/grimoire-books/smut)

**Thesis:** She never pretends the leash is love.

## Law

The plan is in `docs/`. The manuscript is `chapters/book-1-shadow/`. Notes and dumps go in `material/`.

- [docs/OBJECTIVE.md](docs/OBJECTIVE.md) — north star
- [docs/LENGTH.md](docs/LENGTH.md) — word targets (do not write toward them)
- [docs/TRACKER.md](docs/TRACKER.md) — locked rooms
- [docs/DRAFT-CHOICES.md](docs/DRAFT-CHOICES.md) — provisionals
- [docs/PLANNING-BIBLE.md](docs/PLANNING-BIBLE.md) — Draft 07 in full

## Desk cards (top-down)

Each chapter file may start with YAML front matter. The reader shows it as a **desk card** (job, what happens, notes) plus a **spine** table of the whole book. Toggle Desk / Both / Prose in the sidebar.

```yaml
---
status: locked-room
room: Wake
job: What this chapter is doing in the architecture.
happens:
- Plot beat
- Plot beat
notes: |
  Thought process, locks, provisionals, what is still thin.
---
```

`python scripts/build.py` writes the reader **and** `plan/` (every docs/*.md as an HTML page). Toggle Desk / Both / Prose in the sidebar. Plan hub: `plan/index.html`.

## Preview the reader

```powershell
cd C:\Users\MichaelThomson\source\smut\books\seven-year-king
python scripts/build.py
cd ..\..
python -m http.server 8080
```

http://localhost:8080/books/seven-year-king/

## Layout

```
book.json
chapters/book-1-shadow/   manuscript
docs/LENGTH.md            targets
docs/WORDCOUNT.md          live counts (from build)
docs/              planning bible, split
material/source/   Word original + unwrapped markdown
scripts/build.py   markdown → index.html
```
