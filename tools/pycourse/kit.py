"""The authoring kit for The Python School.

Every lesson in this school is written as plain HTML plus calls to the
little helpers below. The helpers exist for two reasons:

  1. no lesson file should ever have to think about HTML escaping
  2. every code block carries the metadata `tools/pyverify.py` needs to
     actually run it and prove the output we printed is the output you
     get

That second point is the important one. The Rusty School's house rule is
"compile every example before publishing". This is the same rule, with a
build step that enforces it.
"""

from __future__ import annotations

import html

SITE = "https://rustyschool.com"
SCHOOL = "The Python School"
OG_IMAGE = SITE + "/python/assets/og-image.png"
OG_ALT = "The Python School: learn Python from zero, with Monty the python mascot"
THEME_COLOR = "#4584b6"

NAV = [
    ("setup.html", "Setup Lab"),
    ("learn/index.html", "Learn"),
    ("build/index.html", "Build"),
    ("pit.html", "Snake Pit"),
    ("playground.html", "Playground"),
    ("quiz.html", "Quizzes"),
]

FOOTER_LINKS = [
    ("learn/index.html", "Curriculum"),
    ("setup.html", "Set up your lab"),
    ("quiz.html", "Quizzes"),
    ("cheatsheets.html", "Cheat sheets"),
    ("glossary.html", "Glossary"),
    ("achievements.html", "Achievements"),
    ("insults.html", "Insult Compiler"),
]

OFFICIAL_LINKS = [
    ("https://www.python.org", "python.org"),
    ("https://docs.python.org/3/tutorial/", "The official tutorial"),
    ("https://docs.python.org/3/library/", "Standard library docs"),
    ("https://peps.python.org/pep-0008/", "PEP 8 style guide"),
    ("https://pypi.org", "PyPI, the package index"),
]

NL = chr(10)


# ------------------------------------------------------------------ escaping
def esc(text: str) -> str:
    return html.escape(text, quote=True)


# ------------------------------------------------------------------ blocks
def code(
    src: str,
    *,
    run: bool = True,
    expect: str | None = None,
    stdin: str | None = None,
    verify: str | None = None,
) -> str:
    """A Python code block.

    run=True    gives the block a working run button (real CPython, in
                the reader's browser, via Pyodide)
    expect=...  prints the exact expected output under it AND tells the
                verifier to prove it
    stdin=...   canned answers for input(), one per line
    verify=     "run" | "compile" | "skip"
    """
    src = src.strip(NL)
    mode = verify or ("run" if run else "compile")
    attrs = ' class="run"' if run else ""
    attrs += f' data-verify="{mode}"'
    if stdin:
        # newlines become entities so the attribute stays on one line;
        # both the browser and the verifier decode them back
        attrs += f' data-stdin="{esc(stdin).replace(NL, "&#10;")}"'
    block = f"<pre{attrs}><code>{esc(src)}</code></pre>"
    if expect is not None:
        block += f'{NL}<pre class="out"><code class="nohl">{esc(expect.strip(NL))}</code></pre>'
    return block


def term(src: str) -> str:
    return f'<pre class="term"><code class="nohl">{esc(src.strip(NL))}</code></pre>'


def repl(src: str) -> str:
    return f'<pre class="repl"><code class="nohl">{esc(src.strip(NL))}</code></pre>'


def tb(src: str) -> str:
    return f'<pre class="traceback"><code class="nohl">{esc(src.strip(NL))}</code></pre>'


def out(src: str) -> str:
    return f'<pre class="out"><code class="nohl">{esc(src.strip(NL))}</code></pre>'


def voice(skill: str, check: str, *paragraphs: str) -> str:
    """One of the voices in your head, weighing in.

    Borrowed, with affection, from a certain detective RPG: the same
    fact lands differently depending on which part of you is speaking.
    """
    slug = skill.lower().replace(" ", "-")
    low = check.lower()
    tone = " success" if low.endswith("success") else (" failure" if low.endswith("failure") else "")
    body = NL.join(f"<p>{p.strip()}</p>" for p in paragraphs)
    return (
        f'<div class="voice" data-skill="{slug}">'
        f'<div class="v-head"><span class="v-name">{esc(skill)}</span>'
        f'<span class="v-check{tone}">[{esc(check)}]</span></div>{body}</div>'
    )


def callout(kind: str, title: str, body: str) -> str:
    return f'<div class="callout {kind}"><span class="co-title">{title}</span>{body}</div>'


def exercise(n, title: str, prompt: str, solution: str, *, label: str = "Exercise") -> str:
    return (
        f'<div class="exercise"><span class="ex-label">{label} {n}</span>'
        f"<h3>{title}</h3>{prompt}"
        f'<details class="solution"><summary>Reveal solution</summary>{solution}</details></div>'
    )


def table(headers, rows) -> str:
    head = "".join(f"<th>{h}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return (
        f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead>'
        f"<tbody>{body}</tbody></table></div>"
    )


def link(text: str, url: str) -> str:
    return f'<a href="{url}" target="_blank" rel="noopener">{text}</a>'


def hint_ladder(hints) -> str:
    """Staged hints for workshop projects, last one being the full answer."""
    parts = ['<div class="hint-ladder">']
    for i, (summary, body) in enumerate(hints, start=1):
        parts.append(
            f'<details class="hint"><summary>Hint {i}: {summary}</summary>'
            f'<div class="hint-body">{body}</div></details>'
        )
    parts.append("</div>")
    return "".join(parts)


# ------------------------------------------------------------------ shell
def page(
    *,
    path: str,
    title: str,
    description: str,
    body: str,
    canonical: str,
    main_class: str = "container",
    body_attrs: str = "",
) -> str:
    depth = path.count("/")
    up = "../" * depth
    campus = "../" * (depth + 1)

    nav_items = NL.join(f'      <a href="{up + href}">{label}</a>' for href, label in NAV)
    foot_items = NL.join(
        f'        <li><a href="{up + href}">{label}</a></li>' for href, label in FOOTER_LINKS
    )
    official = NL.join(
        f'        <li><a href="{href}" target="_blank" rel="noopener">{label}</a></li>'
        for href, label in OFFICIAL_LINKS
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SCHOOL}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{OG_ALT}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<meta name="theme-color" content="{THEME_COLOR}">
<link rel="icon" type="image/svg+xml" href="{up}assets/monty.svg">
<link rel="stylesheet" href="{campus}assets/style.css">
<link rel="stylesheet" href="{up}assets/py.css">
<script>try{{var t=localStorage.getItem("rusty-theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<script defer src="{up}assets/course.js"></script>
<script defer src="{up}assets/py.js"></script>
</head>
<body{body_attrs}>

<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container">
    <a class="logo" href="{up}index.html"><img src="{up}assets/monty.svg" alt="Monty the python">The Python <span class="crate">School</span></a>
    <button class="nav-burger" aria-label="Open menu">☰</button>
    <nav class="main-nav">
{nav_items}
      <button class="theme-toggle" aria-label="Toggle light/dark theme">☀️</button>
    </nav>
  </div>
</header>

<main id="main" tabindex="-1" class="{main_class}">
{body}
</main>

<footer class="site-footer">
  <div class="container cols">
    <div>
      <h2>🐍 {SCHOOL}</h2>
      <p>Learn Python from absolute zero.<br>This site is itself built by a Python
      script you will be able to read by Level 3.</p>
      <p class="campus-switch">Same campus as <a href="{campus}index.html">🦀 The Rusty School</a></p>
    </div>
    <div>
      <h2>School</h2>
      <ul>
{foot_items}
      </ul>
    </div>
    <div>
      <h2>Official Python resources</h2>
      <ul>
{official}
      </ul>
    </div>
  </div>
</footer>

</body>
</html>
"""


def lesson_page(lesson: dict, prev: dict | None, nxt: dict | None) -> str:
    if prev:
        prev_html = (
            f'<a href="{prev["slug"]}.html"><span class="dir">← Previous</span>'
            f'{prev["nav_label"]}</a>'
        )
    else:
        prev_html = '<a href="index.html"><span class="dir">← Back</span>The curriculum</a>'
    if nxt:
        next_html = (
            f'<a class="next" href="{nxt["slug"]}.html"><span class="dir">Next →</span>'
            f'{nxt["nav_label"]}</a>'
        )
    else:
        next_html = (
            '<a class="next" href="../build/index.html"><span class="dir">Next →</span>'
            "The Project Workshop</a>"
        )

    body = f"""  <section class="lesson-header">
    <nav class="breadcrumb"><a href="index.html">← Curriculum</a> · {lesson["counter"]}</nav>
    <span class="badge {lesson["level_class"]}">{lesson["level_label"]}</span>
    <h1>{lesson["title"]} {lesson["emoji"]}</h1>
    <p class="lede muted">{lesson["lede"]}</p>
  </section>

  <div class="lesson-body">
{lesson["body"]}

    <button class="complete-btn" data-lesson="{lesson["id"]}">Mark lesson complete</button>
    <span class="xp-gain">+100 XP</span>

    <div class="lesson-nav">
      {prev_html}
      {next_html}
    </div>
  </div>
"""
    return page(
        path=f"learn/{lesson['slug']}.html",
        title=f"{lesson['nav_label']} - {SCHOOL}",
        description=lesson["desc"],
        body=body,
        canonical=f"{SITE}/python/learn/{lesson['slug']}",
        main_class="container narrow",
    )
