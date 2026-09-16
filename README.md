# Grimoire — smut

A shelf of books. This repo is the **smut** imprint of [grimoire-books](https://github.com/grimoire-books). One volume now; more later.

**Live:** not yet. Preview locally. GitHub Pages is off until Master switches it on.

## On the shelf

| Book | Status | Open |
|------|--------|------|
| [*The Seven-Year King*](books/seven-year-king/) | draft · Book 1 in progress | [reader](books/seven-year-king/index.html) |

## Layout

```
smut/
  README.md              this file
  books.json             the catalogue — add a line when a new book starts
  index.html             the shelf (generated)
  shelf.css
  scripts/build_shelf.py
  books/
    seven-year-king/     first volume (own reader, own chapters, own docs)
    <slug>/              next volume, same shape
```

Each book is a self-contained desk:

```
books/<slug>/
  book.json
  chapters/
  docs/
  scripts/build.py       markdown + desk cards → index.html
  reader.css
  reader.js
  index.html
```

## Preview

```powershell
cd C:\Users\MichaelThomson\source\smut
python scripts/build_shelf.py
cd books\seven-year-king
python scripts/build.py
cd ..\..
python -m http.server 8080
```

Shelf: http://localhost:8080  
King: http://localhost:8080/books/seven-year-king/

## Start another book

1. Copy the shape of `books/seven-year-king/` (or an empty desk: `book.json`, `chapters/`, `docs/`, `scripts/build.py`, reader files).
2. Add an entry to `books.json`.
3. `python scripts/build_shelf.py`

Do not write two books in one folder. The shelf is the only shared page.

## GitHub

https://github.com/grimoire-books/smut

Public repo. Readers are `noindex` until we say otherwise. Pages stays off until Master wants it on the internet, not just in git.
