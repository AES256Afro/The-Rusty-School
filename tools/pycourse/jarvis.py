"""The Jarvis Build: index and chapter pages.

The workshop hands you a spec and gets out of the way. This is the
opposite: a guided build where every step is explained, because "make
your own AI assistant" is the thing beginners most want to do and least
know how to start.
"""

from __future__ import annotations

from .jarvis_data import CHAPTERS, MODEL
from .kit import SCHOOL, SITE, esc, page

NL = chr(10)

PARTS = [
    ("Get it talking", "1 to 4",
     "An assistant that answers you and remembers the conversation.", ["1", "2", "3", "4"]),
    ("Make it feel real", "5 to 7",
     "Streaming, a character of its own, and memory that survives a restart.", ["5", "6", "7"]),
    ("Give it hands", "8 to 10",
     "Tools it can call, tools you wrote safely, and your own notes.", ["8", "9", "10"]),
    ("Make it yours", "11 to 12",
     "A real installed command, a spending cap, and where to go next.", ["11", "12"]),
]


def _part_of(num: str) -> tuple[int, str]:
    for i, (name, _rng, _blurb, nums) in enumerate(PARTS, start=1):
        if num in nums:
            return i, name
    return 0, ""


def _chapter_page(ch: dict, prev: dict | None, nxt: dict | None) -> str:
    part_num, part_name = _part_of(ch["num"])

    nav_prev = (
        f'<a href="{prev["slug"]}.html"><span class="dir">← Previous</span>'
        f'{esc(prev["title"])}</a>'
        if prev else
        '<a href="index.html"><span class="dir">← Back</span>The Jarvis Build</a>'
    )
    nav_next = (
        f'<a class="next" href="{nxt["slug"]}.html"><span class="dir">Next →</span>'
        f'{esc(nxt["title"])}</a>'
        if nxt else
        '<a class="next" href="../build/index.html"><span class="dir">Next →</span>'
        'The Project Workshop</a>'
    )

    body = f"""  <section class="lesson-header">
    <nav class="breadcrumb"><a href="index.html">← The Jarvis Build</a> ·
      Chapter {ch["num"]} of {len(CHAPTERS)} · Part {part_num}, {esc(part_name)}</nav>
    <span class="badge l6">Jarvis · Chapter {ch["num"]}</span>
    <h1>{esc(ch["title"])} {ch["emoji"]}</h1>
    <p class="lede muted">{ch["lede"]}</p>
    <div class="jarvis-goal">
      <span class="jg-label">Goal</span>
      <p>{esc(ch["goal"])}</p>
      <span class="jg-time">about {ch["minutes"]} minutes</span>
    </div>
  </section>

  <div class="lesson-body">
{ch["body"]}

    <div class="jarvis-checkpoint">
      <span class="jc-label">✅ Checkpoint</span>
      <p>{ch["checkpoint"]}</p>
    </div>

    <button class="complete-btn" data-lesson="{ch["id"]}"
      data-label="Mark chapter complete"
      data-done-label="✓ Chapter done. Onwards.">Mark chapter complete</button>
    <span class="xp-gain">+150 XP</span>

    <div class="lesson-nav">
      {nav_prev}
      {nav_next}
    </div>
  </div>
"""
    return page(
        path=f"jarvis/{ch['slug']}.html",
        title=f"Jarvis {ch['num']}: {ch['title']} - {SCHOOL}",
        description=esc(ch["goal"]),
        body=body,
        canonical=f"{SITE}/python/jarvis/{ch['slug']}",
        main_class="container narrow",
    )


def _index() -> str:
    sections = []
    for i, (name, rng, blurb, nums) in enumerate(PARTS, start=1):
        cards = []
        for ch in CHAPTERS:
            if ch["num"] not in nums:
                continue
            cards.append(
                f'      <a class="card lesson-card" data-lesson="{ch["id"]}" '
                f'href="{ch["slug"]}.html">'
                f'<span class="num">{ch["num"]}</span>'
                f'<div><h3>{esc(ch["title"])} {ch["emoji"]}</h3>'
                f'<p>{esc(ch["goal"])}</p>'
                f'<div class="meta">about {ch["minutes"]} minutes</div></div></a>'
            )
        sections.append(f"""  <section class="section" id="part-{i}">
    <h2><span class="jarvis-part">Part {i}</span> {esc(name)}
      <span class="muted small">chapters {rng}</span></h2>
    <p class="muted">{esc(blurb)}</p>
    <div class="grid cols-2">
{NL.join(cards)}
    </div>
  </section>""")

    total_minutes = sum(c["minutes"] for c in CHAPTERS)

    body = f"""  <section class="lesson-header">
    <span class="kicker">The flagship project</span>
    <h1>The <span class="grad">Jarvis</span> Build 🤖</h1>
    <p class="lede muted">
      Build your own AI assistant from an empty folder, in {len(CHAPTERS)} chapters, with
      every step explained. It will remember your conversations, run code you wrote, read
      your own notes, and refuse to spend more than you allow. About {total_minutes // 60}
      hours of work, and less than the price of a coffee in API costs.
    </p>

    <div class="xp-wrap" id="xp-wrap">
      <div class="xp-top">
        <span class="rank-chip"><span class="rank-num">1</span><span class="rank-name">Stowaway</span></span>
        <span class="xp-nums">0 XP</span>
      </div>
      <div class="xp-bar"><div class="xp-fill" id="xp-fill"></div></div>
      <p class="xp-note">Each chapter is 150 XP. Finishing all {len(CHAPTERS)} unlocks the
      It's Alive achievement and the Jarvis milestone.</p>
    </div>

    <div class="progress-wrap">
      <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
      <div class="progress-label" id="progress-label"></div>
    </div>
  </section>

  <div class="callout tip">
    <span class="co-title">🧭 This is a build, not a lesson</span>
    Every chapter ends with a program that runs, so you are never left holding half a
    thing. Type the code rather than pasting it, and do not move on while something is
    broken: chapter N+1 assumes chapter N works. Every chapter finishes with the three
    things that actually go wrong.
  </div>

  <div class="callout info">
    <span class="co-title">🎒 What you need first</span>
    Roughly Lessons 1 to 30: functions, loops, dictionaries and files. Python 3.10+, a
    terminal, and an Anthropic account with a few dollars of credit. Chapter 2 walks
    through the setup properly, including how to keep your API key out of your code.
    <a href="../learn/index.html#level-6">Level 6</a> explains the ideas underneath in more
    depth, and is a good companion, but you do not need it first.
  </div>

  <div class="callout warn">
    <span class="co-title">💸 What it costs, honestly</span>
    This build defaults to <code>{MODEL}</code>, the cheapest current model, at $1 per
    million tokens in and $5 out. A hundred back-and-forth messages costs about twenty
    cents. Chapter 12 adds a hard daily cap so it cannot quietly become more. Prices and
    model names change; the chapters say so rather than pretending otherwise.
  </div>

{NL.join(sections)}

  <section class="section">
    <div class="callout">
      <span class="co-title">🧱 What you will have built</span>
      <p>Not "an AI app". A while loop, a list, a dictionary of functions, a search, and a
      spending cap. Every AI agent you meet from now on, however impressive the marketing,
      is made of those parts. That is the actual point of this project: after it, none of
      this is mysterious.</p>
    </div>
  </section>

<script>window.PY_JARVIS_TOTAL = {len(CHAPTERS)};</script>
"""
    return page(
        path="jarvis/index.html",
        title=f"The Jarvis Build - {SCHOOL}",
        description=(
            f"Build your own AI assistant from scratch in {len(CHAPTERS)} guided chapters: "
            "memory, streaming, tools, your own notes, and a hard spending cap. Every step "
            "explained, for beginners."
        ),
        body=body,
        canonical=SITE + "/python/jarvis/",
        body_attrs=' data-noun="chapters"',
    )


def build() -> list[tuple[str, str]]:
    out = [("jarvis/index.html", _index())]
    for i, ch in enumerate(CHAPTERS):
        prev = CHAPTERS[i - 1] if i > 0 else None
        nxt = CHAPTERS[i + 1] if i + 1 < len(CHAPTERS) else None
        out.append((f"jarvis/{ch['slug']}.html", _chapter_page(ch, prev, nxt)))
    return out
