"""The Project Workshop: index and per-project pages."""

from __future__ import annotations

from .kit import SCHOOL, SITE, callout, code, esc, hint_ladder, page
from .workshop_data import PROJECTS

NL = chr(10)


def _difficulty(n: int) -> str:
    filled = "🐍" * n
    empty = '<span class="off">🐍</span>' * (5 - n)
    return f'<span class="difficulty">{filled}{empty}</span>'


def _project_page(project: dict, prev: dict | None, nxt: dict | None) -> str:
    spec_items = NL.join(f"      <li>{esc(s)}</li>" for s in project["spec"])
    ladder = hint_ladder(project["hints"])

    stretch_items = NL.join(f"      <li>{s}</li>" for s in project["stretch"])

    if project["reference"]:
        note = ""
        if not project["verify"]:
            note = ('<p class="muted small">This one needs the network or a live secret, so it '
                    'has no run button. Build it on your own machine.</p>')
        reference_block = (
            '<details class="solution"><summary>Reveal the reference solution</summary>'
            + (code(project["reference"], run=project["verify"],
                    expect=project["expected"] if project["verify"] else None,
                    stdin=project["stdin"] or None,
                    verify="run" if project["verify"] else "compile")
               if project["reference"] else "")
            + note
            + "</details>"
        )
    else:
        reference_block = callout(
            "info", "🏗️ The reference lives in the lessons",
            "<p>This capstone's reference is the full four-file build in "
            "<a href='../learn/61-assemble-jarvis.html'>Lesson 61</a>, extended with your own "
            "tools and the safety net from "
            "<a href='../learn/62-ethics-cost.html'>Lesson 62</a>. Build it, then make it "
            "yours.</p>")

    nav_prev = (f'<a href="{prev["slug"]}.html"><span class="dir">← Previous</span>'
                f'Project {prev["num"]}: {prev["title"]}</a>'
                if prev else '<a href="index.html"><span class="dir">← Back</span>The Workshop</a>')
    nav_next = (f'<a class="next" href="{nxt["slug"]}.html"><span class="dir">Next →</span>'
                f'Project {nxt["num"]}: {nxt["title"]}</a>'
                if nxt else '<a class="next" href="../pit.html"><span class="dir">Next →</span>'
                            'The Snake Pit</a>')

    body = f"""  <section class="lesson-header">
    <nav class="breadcrumb"><a href="index.html">← Workshop</a> · Project {project["num"]} of {len(PROJECTS)}</nav>
    <span class="badge build">Project · after {project["after"]}</span>
    <h1>{project["title"]} {project["emoji"]}</h1>
    <p class="lede muted">{project["lede"]}</p>
    <p class="meta muted small">Difficulty {_difficulty(project["difficulty"])}</p>
  </section>

  <div class="lesson-body">
    <div class="spec">
      <h3>📋 Build this</h3>
      <ul>
{spec_items}
      </ul>
    </div>

    <h2>Hints, if you want them</h2>
    <p class="muted">Try the spec cold first. Open a hint only when you are properly stuck; the
    struggle is where the learning is.</p>
    {ladder}

    <h2>The reference solution</h2>
    <p class="muted">Yours does not need to match this. There are many good ways to build any of
    these. Compare only after you have your own working.</p>
    {reference_block}

    <h2>Stretch goals</h2>
    <ul>
{stretch_items}
    </ul>

    <button class="complete-btn" data-lesson="{project["id"]}"
      data-label="Mark project complete" data-done-label="✓ Built it. Nicely done.">Mark project complete</button>
    <span class="xp-gain">+250 XP</span>

    <div class="lesson-nav">
      {nav_prev}
      {nav_next}
    </div>
  </div>
"""
    return page(
        path=f"build/{project['slug']}.html",
        title=f"Project {project['num']}: {project['title']} - {SCHOOL}",
        description=esc(project["blurb"]),
        body=body,
        canonical=f"{SITE}/python/build/{project['slug']}",
        main_class="container narrow",
    )


def _index() -> str:
    cards = []
    for p in PROJECTS:
        cards.append(
            f'      <a class="card lesson-card project-card" data-lesson="{p["id"]}" '
            f'href="{p["slug"]}.html">'
            f'<span class="num">{p["num"]}</span>'
            f'<div><h3>{p["title"]} {p["emoji"]}</h3><p>{esc(p["blurb"])}</p>'
            f'<div class="meta">after {p["after"]} · {_difficulty(p["difficulty"])}</div></div></a>'
        )

    body = f"""  <section class="lesson-header">
    <span class="kicker">The Project Workshop</span>
    <h1>The <span class="grad">Workshop</span> 🔨</h1>
    <p class="lede muted">
      Lessons teach the language. Projects teach programming. Here are {len(PROJECTS)} things to
      build from a spec, not a script, with a ladder of hints and a reference solution you only
      see if you want it. Every reference that can run has been run and checked, exactly like
      the lessons.
    </p>

    <div class="xp-wrap" id="xp-wrap">
      <div class="xp-top">
        <span class="rank-chip"><span class="rank-num">1</span><span class="rank-name">Stowaway</span></span>
        <span class="xp-nums">0 XP</span>
      </div>
      <div class="xp-bar"><div class="xp-fill" id="xp-fill"></div></div>
      <p class="xp-note">Each finished project is 250 XP, the biggest single reward in the
      school. Finishing them all unlocks the Shipped It achievement.</p>
    </div>

    <div class="progress-wrap">
      <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
      <div class="progress-label" id="progress-label"></div>
    </div>
  </section>

  <div class="callout tip">
    <span class="co-title">🧗 The right way to use this</span>
    Read the spec, then close the page and open a blank file. Wrestle with it. Reach for a hint
    only when genuinely stuck, and the reference only when you have something working of your
    own to compare it to. The gap between "I understood that lesson" and "I built that from
    nothing" is the whole job, and the only way across is a blank file.
  </div>

  <section class="section">
    <div class="grid cols-2">
{NL.join(cards)}
    </div>
  </section>

<script>window.PY_BUILD_TOTAL = {len(PROJECTS)};</script>
"""
    return page(
        path="build/index.html",
        title=f"The Project Workshop - {SCHOOL}",
        description=f"{len(PROJECTS)} build-it-yourself Python projects with hint ladders and "
                    "verified reference solutions.",
        body=body,
        canonical=SITE + "/python/build/",
        body_attrs=' data-noun="projects"',
    )


def build() -> list[tuple[str, str]]:
    out = [("build/index.html", _index())]
    for i, project in enumerate(PROJECTS):
        prev = PROJECTS[i - 1] if i > 0 else None
        nxt = PROJECTS[i + 1] if i + 1 < len(PROJECTS) else None
        out.append((f"build/{project['slug']}.html", _project_page(project, prev, nxt)))
    return out
