# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this project is

Backend **API** for an app that presents the characters of Ferdowsi's
**Shahname (شاهنامه)** as a full family/relationship tree. There is a separate
frontend app (not in this repo) that consumes this API and renders the tree.

Each node in the tree is a *character* (called a **myth**). The product goal is
that when a user selects a character, they read **the part of the story that
concerns that character** — not the whole poem. So every character needs its own
story text.

## Tech stack

- **Flask 3** + **Flask-SQLAlchemy 2.0** + **Flask-Migrate** (Alembic).
- **PostgreSQL** via `psycopg2`. DB name: `IranianMythDb`.
- Python virtualenv lives in `venv/` (Windows: `venv/Scripts/python.exe`).
- Content is **Persian (Farsi), right-to-left, UTF-8**. Always read/write files
  as UTF-8; stdout on Windows is cp1252 and will choke on Persian — write to a
  file or set encoding explicitly instead of printing it.

## Running / common commands

```bash
# from the API project root, venv active
venv/Scripts/python.exe app.py        # run the dev server (creates DB + seeds if empty)
# DB URL comes from .env -> DATABASE_URL (postgresql://postgres:a@localhost/IranianMythDb)
```

`app/__init__.py` auto-creates the database if missing, runs `db.create_all()`,
and seeds reference data via `app/static/seed_data.py` when the `eras` table is
empty. Config is chosen by `FLASK_CONFIG` (`development` / `production`) from
`.env` / `.flaskenv`.

## Data model (`app/models/`)

- **`myths`** (`Myth`) — the characters / tree nodes. PK `id` is a **String(10)**
  short slug (e.g. `zal`, `jmshd`, `zhk1`). Key columns: `name`, `nickname`,
  `gender`, `importance`, `pos`, `shape`, `khvarenah`, image fields, and
  **`description` (Text)** — the character's story (see below). FKs:
  `era_id` → `eras`, `family_id` → `families`, `category_id` → `categories`.
- **`eras`** (`Era`) — historical/mythical periods (پیشدادیان، کیانیان، …).
- **`families`** (`Family`) — lineages (ایرانیان، تورانیان، تازیان، …).
- **`categories`** (`Category`) — role types (پادشاه، پهلوان، دیو، …).
- **`relationships`** (`Relationship`) — non-parent edges between two myths
  (marriage, affair, …) with drawing metadata (`points`, `from_spot`, `to_spot`).
- **`parent_child`** (`ParentChild`) — parent→child edges for the tree.
- **`myth_photos`**, **`relation_types`** — supporting tables.

> Note: `app/routes/myth_routes.py` declares routes as `/<int:id>` even though
> `myths.id` is a string slug — a pre-existing mismatch; don't "fix" it unless asked.

## The character stories — `stories/` (the current focus)

Only a few myths currently have text in `myths.description`. We extract each
such description into its own **HTML file** under [stories/](stories/) so the
stories are **version-controlled and editable by hand**, then synced back to the
database **manually** (the user does the DB update after reviewing — do **not**
write to the DB unless explicitly asked).

### File layout

- `stories/template.html` — the **single shared wrapper** (HTML shell, all the
  CSS, and a small loader script). Hand-maintained, committed; the generator
  never overwrites it. It loads a character fragment by `?id=` (see Viewing).
- `stories/<myth-id>.html` — one **bare `<article>` fragment** per character
  that has a description, named by the myth's `id` (e.g. `stories/zal.html`).
  No `<head>`, no CSS — only the `<article>` element.
- `stories/index.html` — generated table linking to every story (derived file).

### Fragment anatomy

Each `stories/<id>.html` is exactly one `<article>` element:

- The opening tag carries the metadata as **`data-*` attributes**
  (`data-myth-id`, `data-name`, `data-nickname`, `data-era`, `data-family`,
  `data-category`). The wrapper reads these to rebuild the header. **These
  attributes are NOT part of the database content.**
- The story body sits between two markers inside the article:
  ```html
  <article class="story" data-myth-id="zal" ...>
    <!-- ... DB:START ... -->
    ...the exact text that belongs in myths.description...
    <!-- ... DB:END ... -->
  </article>
  ```
  **Everything between `DB:START` and `DB:END` is the canonical
  `description` value.** That is the only part to copy back into the database.

### Formatting (important)

All files are formatted with **Prettier 3, default settings + CRLF line
endings** (`npx prettier@3 --end-of-line crlf --write stories/`).
`stories/simk.html` is the reference style. Prettier only reflows insignificant
whitespace (indentation, soft-wrapping long `<p>` text); it never changes the
Persian text. Keep running it so every fragment stays consistent with `simk`.

### Two content formats (both appear in the DB)

1. **Rich HTML** (e.g. جمشید, ضحاک) — `<h2>` section titles, `<p>` prose,
   centered `<p>` blocks for Shahname couplets (each verse in its own `<span>`,
   one verse per line, joined by `<br />`), and
   `<span class="hidden-in-read">…</span>` for verse lines the **frontend hides
   in read-mode** (shown but greyed by the wrapper). Copied **verbatim** (then
   prettier-reflowed).
2. **Plain text** (e.g. فرانک, کاوه) — newline-separated paragraphs, converted
   to escaped `<p>…</p>` paragraphs (an intentional upgrade toward HTML).

The generator decides per-myth by detecting whether the description contains
HTML tags.

### Viewing

The fragments have no styling on their own; open them through the wrapper:
`stories/template.html?id=<myth-id>`. The wrapper uses `fetch()`, which browsers
block over `file://`, so serve the folder first:

```bash
cd stories && python -m http.server   # then open http://localhost:8000/template.html?id=zal
```

`index.html` links each character to `template.html?id=<id>`.

### Regenerating

`scripts/generate_stories.py` reads `DATABASE_URL` from `.env`, queries every
myth with a non-empty `description`, writes the `<article>` fragments, rewrites
`index.html`, and finally runs Prettier on `stories/` (if `npx` is available).

```bash
venv/Scripts/python.exe scripts/generate_stories.py            # create only MISSING fragments (safe)
venv/Scripts/python.exe scripts/generate_stories.py --force     # overwrite ALL from the DB
```

**Safety:** by default it **skips fragments that already exist**, so re-running
it after adding new descriptions to the DB creates only the new characters'
fragments and never clobbers your hand-edits. `index.html` is always rewritten;
`template.html` is never touched. Use `--force` only when you intentionally want
to discard local edits and re-pull from the database.

### Workflow & conventions

- Source of truth going forward: the `stories/*.html` files in git. The DB is
  updated **manually** from the `DB:START`/`DB:END` region after review.
- When **adding** a character's story: add the fragment (or add the description
  to the DB and run the generator), keeping the same `<article>` + `data-*` +
  marker structure, then run Prettier.
- The longer-term goal is to **split** a poem's combined narrative so each
  character's file contains only the portion relevant to that character. Some
  current files (e.g. `zhk1.html` / ضحاک) still hold a long multi-section
  narrative covering several characters; splitting those is expected future work.
- Preserve Persian text exactly; keep the `hidden-in-read` spans and the
  centered-couplet structure intact when editing rich-HTML stories.

## The راوی (narrator) skill — turning couplets into story prose

The character stories above need modern, readable prose. That prose is produced
with a **Claude Code skill** that lives in this repo:
[.claude/skills/shahnameh-ravi/SKILL.md](.claude/skills/shahnameh-ravi/SKILL.md).

- **What it does:** re-tells (bازآفرینی) a passage of Ferdowsi's Shahname as
  flowing, modern, plain Persian prose and then quotes the **verses verbatim**,
  following the fixed pattern **prose → verse block → prose → verse block → …**.
  It is a *narrator*, not a line-by-line translator.
- **When it fires:** whenever the user sends Shahname couplets (as
  `مصرع اول - مصرع دوم` lines) and asks to "معنی / روایت / بازنویسی / به نثر روان",
  even without saying "skill" or "شاهنامه". Claude Code auto-discovers it from
  `.claude/skills/`; you can also invoke it explicitly.
- **Hard rules (in the skill):** verses are reproduced exactly (no word/order/
  punctuation change, keep even input typos); nothing may be dropped from or
  added to a verse's meaning; verify each prose block against its verses before
  finalizing.

### Skill references (consult before narrating)

- [.claude/skills/shahnameh-ravi/references/glossary.md](.claude/skills/shahnameh-ravi/references/glossary.md)
  — the واژه‌نامه. Top of the file is a small **curated** set of archaic words
  with a *suggested سره rendering* column (use these for prose wording). Below a
  `---` separator is the **full imported dictionary (~5990 entries)** merged from
  the user's own `shahname vajename.txt` — word → meaning only, in original
  order. The file is large (>256 KB); **Grep it** to look a word up rather than
  reading it whole. If a word is in both, the curated table's suggestion wins.
- [.claude/skills/shahnameh-ravi/references/style-decisions.md](.claude/skills/shahnameh-ravi/references/style-decisions.md)
  — fixed, project-wide style choices (e.g. keep «یزدان»/«فرّ», Persian quotes
  «…», نیم‌فاصله). Skim it when starting a new passage; record new agreed choices
  here so later passages stay consistent.

### Source glossary

`shahname vajename.txt` (repo root) is the user's original hand-built glossary
(a JSON array of `{name, value}`). It has been merged into `glossary.md` above
and is kept as the source — **don't delete it**. To re-merge after editing it,
regenerate the full section of `glossary.md` from this JSON (preserve the curated
top section and every imported entry).

### How it connects to `stories/`

The prose the راوی skill produces is the raw material for a character's story
text. Split it per character and place it in the matching `stories/<id>.html`
fragment (between the `DB:START`/`DB:END` markers), keeping the verse blocks and
`hidden-in-read` spans as described above — then sync to the DB manually.

### Reviewing stories & the self-improvement loop

Beyond writing new stories, an ongoing task is **reviewing the existing
`stories/*.html`** for (a) structural conformance to `simk.html` and (b) fidelity
of each prose block to the verses it narrates. This review is also the mechanism
by which the راوی skill gets **better over time**. The user's stated top priority:
Claude's معنی ability must improve after every chat and file review, because
future couplets arrive with no reference meaning. The loop:

1. **Structure check** — every fragment must match `simk.html`: prose `<p>` →
   centered verse block — each verse in its own `<span>`, one per line, joined by
   `<br />` (`<p style="text-align: center"><span>…</span><br /><span>…</span></p>`) →
   `<p>&nbsp;</p>`. Files that put each verse in its own `<p>` (e.g. `zal`,
   `sohrab`, `siavash`, `keyKavous`, `keykhosro`, `frydn`, `mnchr`, `sam`,
   `rostam`) were all regrouped into this span format on 2026-07-02, verified
   character-for-character against `git HEAD`; every `stories/*.html` now uses it.
   Full spec in `style-decisions.md`. **Never alter the Persian verse text** —
   only fix grouping/tags.
2. **Content check** — for each prose block, verify it faithfully narrates the
   verses that follow it (nothing dropped, nothing invented, archaic words and
   the subject of each action read correctly). Fix wrong meanings in place.
3. **Record the lesson** — every mistake found or correction made goes into
   `references/style-decisions.md` → «لاگ اصلاح‌ها», and every new word into
   `references/glossary.md`. This is what makes the next interpretation better.
4. **Learn from the user's edits** — the user reviews Claude's changes and may
   edit them. **Before committing, re-read the user's edits (`git diff`)**, work
   out why each was an improvement, and log it. Human corrections are the
   highest-value signal. Do not commit until this review-and-record step is done.

As always during review, do **not** write to the DB; the user syncs manually.
