"""Render The Bridge: the mission board, mission pages, and mission data."""

from __future__ import annotations

import json

from .kit import NL, SITE, esc, page
from .mission_data import MISSIONS

STATIONS = {
    "helm": ("🧭", "Helm", "Control flow, loops and keeping the ship pointed somewhere"),
    "ops": ("📦", "Ops", "Collections, manifests and resources that must add up"),
    "engineering": ("⚙️", "Engineering", "Concurrency, performance and memory"),
    "science": ("🔬", "Science", "Algorithms, parsing and making sense of signals"),
    "tactical": ("🛡️", "Tactical", "Errors, validation and refusing bad input"),
    "sickbay": ("🩺", "Sickbay", "Debugging, testing and diagnosing the ship"),
}

SEASONS = {
    1: ("Shakedown Cruise", "Output, variables, types and decisions", "Cadet"),
    2: ("Routine Patrol", "Loops, collections and iteration", "Cadet"),
    3: ("First Contact", "Functions, structured data and parsing", "Ensign"),
    4: ("The Anomaly", "Objects, traits, errors and iterators", "Lieutenant JG"),
    5: ("Deep Space", "Concurrency, async and performance", "Lieutenant"),
    6: ("Terminus", "Four long systems, and an ending", "Commander"),
}

LANGS = [("py", "🐍", "Python"), ("rs", "🦀", "Rust")]


def _mission_page(m: dict, prev: dict | None, nxt: dict | None) -> str:
    icon, station_name, _ = STATIONS[m["station"]]
    season_name = SEASONS[m["season"]][0]
    n_obj = len(m["objectives"])
    words = {3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight",
             9: "nine", 10: "ten"}.get(n_obj, str(n_obj))

    objectives = NL.join(
        f'        <li data-obj="{i}"><span class="obj-state">•</span>'
        f'<span class="obj-label">{esc(label)}</span>'
        f'<span class="obj-detail"></span></li>'
        for i, label in enumerate(m["objectives"])
    )

    panels = []
    tabs = []
    for key, emoji, label in LANGS:
        tabs.append(
            f'      <button type="button" class="lang-tab" data-lang="{key}">'
            f'{emoji} {label}</button>'
        )
        panels.append(f"""    <div class="lang-panel" data-lang="{key}" hidden>
      <div class="objective-spec">
        <h3>Objective</h3>
{m[key + "_spec"]}
      </div>

      <div class="console" data-lang="{key}">
        <div class="console-head">
          <span class="console-title">{emoji} {label} console</span>
          <span class="console-status" data-role="status"></span>
        </div>
        <textarea class="console-editor" spellcheck="false"
          aria-label="{label} code editor for this mission"></textarea>
        <div class="console-actions">
          <button type="button" class="btn btn-primary btn-small" data-role="run">
            Run Diagnostics
          </button>
          <button type="button" class="btn btn-ghost btn-small" data-role="reset">
            Reset console
          </button>
          <span class="console-hint muted small">Ctrl/Cmd + Enter also runs</span>
        </div>
      </div>

      <div class="archie" data-role="archie" aria-live="polite">
        <div class="archie-head"><span class="archie-name">ARCHIE</span>
          <span class="archie-sub muted small">ship's computer, standing by</span></div>
        <div class="archie-body">
          <p class="muted">Press <strong>Run Diagnostics</strong> and I will tell you
          which objectives you actually met.</p>
        </div>
      </div>
    </div>""")

    def _link(other, cls, label):
        return (f'<a class="{cls}" href="../s{other["season"]}/{other["slug"]}.html">'
                f'<span class="dir">{label}</span>{esc(other["title"])}</a>')
    nav_prev = (_link(prev, "", "← Previous") if prev
                else '<a href="../index.html"><span class="dir">← Back</span>Mission board</a>')
    nav_next = (_link(nxt, "next", "Next →") if nxt
                else '<a class="next" href="../index.html"><span class="dir">Next →</span>Mission board</a>')

    body = f"""  <section class="lesson-header">
    <nav class="breadcrumb"><a href="../index.html">← Mission board</a> ·
      Season {m["season"]}, {esc(season_name)}</nav>
    <span class="badge station station-{m["station"]}">{icon} {esc(station_name)}</span>
    <h1>{esc(m["title"])}</h1>
    <p class="stardate muted small">{esc(m["stardate"])} · UES Magnanimous</p>
  </section>

  <div class="mission-body">
    <section class="briefing">
      <h2>Briefing</h2>
{m["briefing"]}
    </section>

    <section class="objectives-panel">
      <h2>Mission objectives</h2>
      <p class="muted small">ARCHIE checks all {words} every time you run diagnostics.</p>
      <ul class="objectives" data-role="objectives">
{objectives}
      </ul>
    </section>

    <div class="lang-tabs" role="tablist" aria-label="Choose a language">
{NL.join(tabs)}
    </div>

{NL.join(panels)}

    <details class="hint">
      <summary>Ask Commander Raghunathan for a hint</summary>
      <div class="hint-body"><p>{m["hint"]}</p></div>
    </details>

    <section class="debrief" data-role="debrief" hidden>
      <h2>Debrief</h2>
{m["debrief"]}
    </section>

    <div class="lesson-nav">
      {nav_prev}
      {nav_next}
    </div>
  </div>

<script>window.BRIDGE_MISSION = {json.dumps(m["id"])};</script>
"""
    return page(
        path=f"bridge/s{m['season']}/{m['slug']}.html",
        title=f"{m['title']} - The Bridge",
        description=esc(m["blurb"]),
        body=body,
        canonical=f"{SITE}/bridge/s{m['season']}/{m['slug']}",
        main_class="container narrow",
    )


def _season_block(num: int) -> str:
    name, blurb, rank = SEASONS[num]
    mine = [m for m in MISSIONS if m["season"] == num]
    if not mine:
        return f"""  <section class="section season season-locked" id="season-{num}">
    <h2><span class="season-num">Season {num}</span> {esc(name)}
      <span class="badge soon">coming soon</span></h2>
    <p class="muted">{esc(blurb)}.</p>
  </section>"""
    cards = []
    for m in mine:
        icon, station_name, _ = STATIONS[m["station"]]
        cards.append(
            f'      <a class="card mission-card" data-mission="{m["id"]}" '
            f'data-station="{m["station"]}" data-season="{num}" '
            f'href="s{m["season"]}/{m["slug"]}.html">'
            f'<span class="mission-num">{m["num"]:02d}</span>'
            f'<div><span class="badge station station-{m["station"]}">{icon} {esc(station_name)}</span>'
            f'<h3>{esc(m["title"])}</h3><p>{esc(m["blurb"])}</p>'
            f'<div class="meta mission-flags"></div></div></a>'
        )
    return f"""  <section class="section season" id="season-{num}" data-season="{num}">
    <h2><span class="season-num">Season {num}</span> {esc(name)}
      <span class="muted small season-count" data-role="season-count"></span></h2>
    <p class="muted">{esc(blurb)}. Opens at {esc(rank)}.</p>
    <div class="grid cols-2">
{NL.join(cards)}
    </div>
  </section>"""


def _index() -> str:
    seasons_html = NL.join(_season_block(n) for n in sorted(SEASONS))

    station_rows = NL.join(
        f'        <li data-station="{key}"><span class="st-icon">{icon}</span>'
        f'<strong>{esc(name)}</strong> <span class="muted">{esc(desc)}</span>'
        f'<span class="st-lock muted small"></span></li>'
        for key, (icon, name, desc) in STATIONS.items()
    )

    body = f"""  <section class="lesson-header bridge-hero">
    <span class="kicker">United Expeditionary Service</span>
    <h1>The <span class="grad">Bridge</span> 🖖</h1>
    <p class="lede muted">
      You are the new Systems Officer aboard the <strong>UES Magnanimous</strong>: nineteen
      years old, three decks with a smell Engineering has stopped apologising for, and
      software held together by optimism. Every mission is a real coding problem wearing
      a uniform, and the ship's computer checks your work.
    </p>

    <div class="rank-wrap" id="rank-wrap">
      <div class="rank-top">
        <span class="rank-chip"><span class="rank-icon">🎖️</span>
          <span class="rank-name">Cadet</span></span>
        <span class="rank-nums muted small">0 missions cleared</span>
      </div>
      <div class="rank-bar"><div class="rank-fill" id="rank-fill"></div></div>
      <p class="rank-next muted small" id="rank-next"></p>
    </div>
    <p class="crew-link"><a href="crew.html">Meet the crew →</a></p>
  </section>

  <div class="callout info">
    <span class="co-title">🖥️ What makes this different from the puzzles</span>
    The Dojo and the Snake Pit show you a problem and trust you to mark it solved. Here
    <strong>ARCHIE runs your code</strong> against the mission objectives and tells you
    which ones you actually met, with the input that broke it. Every mission exists in
    both Python and Rust, and you can clear it in either. Doing both is how you find out
    where the two languages genuinely disagree.
  </div>

{seasons_html}

  <section class="section">
    <h2>The stations</h2>
    <p class="muted">Every mission is posted to a station, so you can see which kind of
    problem keeps catching you out. Promotions open more of them; they never make the
    missions harder, only wider.</p>
    <ul class="station-list">
{station_rows}
    </ul>
  </section>

  <section class="section">
    <div class="callout">
      <span class="co-title">🔍 About the tests</span>
      <p>The objectives run in your own browser (Python) or through our playground proxy
      (Rust), which means a determined person can read them. That is fine. This is a
      place to learn, not an exam, and nobody is awarded anything at the end. Building
      elaborate tamper resistance would cost real effort and protect nothing worth
      protecting.</p>
    </div>
  </section>
"""
    return page(
        path="bridge/index.html",
        title="The Bridge - The Rusty School",
        description=(
            "A starship simulator for people learning to code. Repair the UES "
            "Magnanimous one mission at a time, in Python or Rust, and the ship's "
            "computer checks your work."
        ),
        body=body,
        canonical=SITE + "/bridge/",
    )


def _missions_js() -> str:
    """The data bridge.js runs: stubs and checkers, per language."""
    payload = {}
    for m in MISSIONS:
        payload[m["id"]] = {
            "title": m["title"],
            "season": m["season"],
            "station": m["station"],
            "crew": m.get("crew", []),
            "objectives": m["objectives"],
            "py": {"stub": m["py_stub"], "checker": m["py_checker"]},
            "rs": {"stub": m["rs_stub"], "checker": m["rs_checker"]},
        }
    return (
        "/* Generated by tools/bridgebuild.py. Do not edit by hand.\n"
        "   Stubs and objective checkers for every mission on The Bridge. */\n"
        "window.BRIDGE_MISSIONS = " + json.dumps(payload, indent=2) + ";\n"
    )


def build() -> list[tuple[str, str]]:
    out = [("bridge/index.html", _index()),
           ("bridge/assets/missions.js", _missions_js())]
    for i, m in enumerate(MISSIONS):
        prev = MISSIONS[i - 1] if i > 0 else None
        nxt = MISSIONS[i + 1] if i + 1 < len(MISSIONS) else None
        out.append((f"bridge/s{m['season']}/{m['slug']}.html", _mission_page(m, prev, nxt)))
    return out
