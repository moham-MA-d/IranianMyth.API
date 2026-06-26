# -*- coding: utf-8 -*-
"""
Generate one HTML "story" fragment per Shahname character that has a non-empty
`description` in the `myths` table, into the top-level `stories/` folder.

STRUCTURE: each `stories/<id>.html` is a bare `<article>` fragment (no <head>,
no CSS). The shared chrome lives once in `stories/template.html`, which loads a
fragment by `?id=` and rebuilds the header from the article's data-* attributes.

WHY: the per-character story is the source of truth we want to version in git
and edit by hand. The text between the DB:START / DB:END markers inside the
article is exactly what belongs in `myths.description`. After editing, copy that
text back into the database yourself (this script never writes to the DB).

SAFETY: by default this only creates files that do NOT already exist, so
re-running it after adding new descriptions never clobbers your hand-edits.
Pass --force to regenerate every fragment from the current database content.
`index.html` is always rewritten (it is derived, not hand-edited).
`template.html` is a committed static file and is never touched here.

FORMATTING: after writing, the script runs Prettier (defaults + CRLF) on the
folder if Node/npx is available, so output matches `simk.html` (the reference
style). If Prettier is unavailable it leaves valid—but unformatted—HTML.

Usage (from the API project root, with the venv active):
    python scripts/generate_stories.py            # create only missing fragments
    python scripts/generate_stories.py --force     # overwrite all from DB
"""
import os
import re
import sys
import html
import shutil
import subprocess

import psycopg2
from dotenv import load_dotenv

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_DIR = os.path.join(ROOT, "stories")

load_dotenv(os.path.join(ROOT, ".env"))
DB_URL = os.getenv("DATABASE_URL")
if not DB_URL:
    sys.exit("DATABASE_URL is not set (expected in .env).")

FORCE = "--force" in sys.argv[1:]


def esc(v):
    return html.escape(v or "", quote=True)


def looks_like_html(text: str) -> bool:
    return bool(re.search(r"<[a-zA-Z/!][^>]*>", text))


def plain_to_html(text: str) -> str:
    """Convert newline-separated plain text into escaped <p> paragraphs."""
    return "\n".join(
        "    <p>" + html.escape(line.strip()) + "</p>"
        for line in text.splitlines()
        if line.strip()
    )


# A bare <article> fragment. Metadata rides on data-* attributes so the shared
# template can rebuild the header without the fragment carrying any chrome.
ARTICLE = (
    '<article class="story" data-myth-id="{id}" data-name="{name}" '
    'data-nickname="{nick}" data-era="{era}" data-family="{family}" '
    'data-category="{category}">\n'
    "  <!-- ===================== DB:START — copy everything between START and END into myths.description ===================== -->\n"
    "{content}\n"
    "  <!-- ===================== DB:END ===================== -->\n"
    "</article>\n"
)

INDEX = """<!doctype html>
<html lang="fa" dir="rtl">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>داستان شخصیت‌های شاهنامه</title>
    <style>
      body {{
        font-family: "Vazirmatn", "Segoe UI", Tahoma, sans-serif;
        max-width: 900px;
        margin: 0 auto;
        padding: 24px;
        color: #1f2328;
      }}
      h1 {{ font-size: 1.6rem; }}
      p.sub {{ color: #6b7280; }}
      table {{ width: 100%; border-collapse: collapse; font-size: 0.95rem; }}
      th, td {{ border-bottom: 1px solid #e5e7eb; padding: 8px 10px; text-align: right; }}
      th {{ background: #f8fafc; }}
      a {{ color: #7c3f00; text-decoration: none; }}
      a:hover {{ text-decoration: underline; }}
    </style>
  </head>
  <body>
    <h1>داستان شخصیت‌های شاهنامه</h1>
    <p class="sub">
      {count} شخصیت دارای متن در ستون <code>description</code>. هر پیوند، آن
      شخصیت را در قالب <code>template.html</code> باز می‌کند.
    </p>
    <table>
      <thead>
        <tr>
          <th>شناسه</th><th>نام</th><th>لقب</th><th>دوران</th>
          <th>دسته</th><th>قالب</th><th>طول</th>
        </tr>
      </thead>
      <tbody>
{rows}
      </tbody>
    </table>
  </body>
</html>
"""


def run_prettier():
    npx = shutil.which("npx")
    if not npx:
        print("Prettier skipped (npx not found). Output is valid but unformatted.")
        print("Tip: install Node, then run: npx prettier@3 --end-of-line crlf --write stories/")
        return
    try:
        subprocess.run(
            [npx, "--yes", "prettier@3", "--end-of-line", "crlf", "--write", "stories/"],
            cwd=ROOT, check=True,
        )
        print("Formatted stories/ with Prettier (defaults + CRLF).")
    except subprocess.CalledProcessError as e:
        print(f"Prettier run failed ({e}); output left unformatted.")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    conn = psycopg2.connect(DB_URL)
    cur = conn.cursor()

    cur.execute("SELECT id, name FROM eras")
    eras = {r[0]: r[1] for r in cur.fetchall()}
    cur.execute("SELECT id, title FROM families")
    families = {r[0]: r[1] for r in cur.fetchall()}
    cur.execute("SELECT id, title FROM categories")
    categories = {r[0]: r[1] for r in cur.fetchall()}

    cur.execute(
        """
        SELECT id, name, nickname, era_id, family_id, category_id, description
        FROM myths
        WHERE description IS NOT NULL AND btrim(description) <> ''
        ORDER BY name
        """
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()

    created, skipped, index_items = 0, 0, []
    for (mid, name, nick, era_id, fam_id, cat_id, desc) in rows:
        is_html = looks_like_html(desc)
        era = eras.get(era_id, era_id or "—")
        category = categories.get(cat_id, cat_id or "—")
        index_items.append((mid, name, nick, era, category,
                            "html" if is_html else "text", len(desc)))

        path = os.path.join(OUT_DIR, f"{mid}.html")
        if os.path.exists(path) and not FORCE:
            skipped += 1
            continue

        fragment = ARTICLE.format(
            id=esc(mid), name=esc(name), nick=esc(nick), era=esc(era),
            family=esc(families.get(fam_id, fam_id or "—")), category=esc(category),
            content=(desc if is_html else plain_to_html(desc)),
        )
        with open(path, "w", encoding="utf-8") as f:
            f.write(fragment)
        created += 1

    rows_html = "\n".join(
        f'        <tr><td><a href="template.html?id={esc(mid)}">{esc(mid)}</a></td>'
        f'<td>{esc(name)}</td><td>{esc(nick)}</td>'
        f'<td>{esc(era)}</td><td>{esc(cat)}</td>'
        f'<td>{fmt}</td><td>{ln:,}</td></tr>'
        for (mid, name, nick, era, cat, fmt, ln) in index_items
    )
    with open(os.path.join(OUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(INDEX.format(count=len(index_items), rows=rows_html))

    if not os.path.exists(os.path.join(OUT_DIR, "template.html")):
        print("WARNING: stories/template.html is missing — fragments need it to render.")

    print(f"Characters with description: {len(index_items)}")
    print(f"Fragments created: {created} | skipped (already existed): {skipped}")
    if skipped and not FORCE:
        print("Tip: pass --force to overwrite existing fragments from the database.")
    run_prettier()


if __name__ == "__main__":
    main()
