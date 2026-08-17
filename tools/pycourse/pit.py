"""The Snake Pit page: renders the verified puzzles from pit_data.py."""

from __future__ import annotations

import json

from .kit import SCHOOL, SITE, page
from .pit_data import PUZZLES

NL = chr(10)


def build() -> str:
    data = json.dumps(PUZZLES, separators=(",", ":"))

    body = f"""  <section class="lesson-header">
    <span class="kicker">The Snake Pit</span>
    <h1>The <span class="grad">Snake Pit</span> 🐍</h1>
    <p class="lede muted">
      {len(PUZZLES)} puzzles across six tiers, from Egg to Basilisk. Predict the output, find
      the bug, fix the code. Every "it prints" here was checked by actually running the code,
      so if you and the pit disagree, the pit is right and there is something delicious to
      learn.
    </p>

    <div class="xp-wrap" id="xp-wrap">
      <div class="xp-top">
        <span class="rank-chip"><span class="rank-num">1</span><span class="rank-name">Stowaway</span></span>
        <span class="xp-nums">0 XP</span>
      </div>
      <div class="xp-bar"><div class="xp-fill" id="xp-fill"></div></div>
      <p class="xp-note">Each solved puzzle is 60 XP. Solving stays private to you: the public
      counter only tracks lessons.</p>
    </div>

    <div class="progress-wrap">
      <div class="progress-bar"><div class="progress-fill" id="pit-fill"></div></div>
      <div class="progress-label" id="pit-label"></div>
    </div>
  </section>

  <div class="callout tip">
    <span class="co-title">🥋 How to train</span>
    Read the code and commit to a prediction <em>before</em> you reveal anything. For fix and
    bug puzzles, open the code in the <a href="playground.html">Playground</a>, break it,
    repair it, run it. Getting it wrong is how the belt is earned; guessing and revealing is
    not.
  </div>

  <div id="pit-root"></div>

  <div class="callout info" style="margin-top:26px">
    <span class="co-title">🏆 Basilisk Slayer</span>
    Solve every puzzle in the pit and you unlock an achievement. The Basilisk tier is genuinely
    hard: late-binding closures, identity versus equality, shallow copies, exhausted
    generators. These are the bugs that catch professionals, so meeting them here, safely, in a
    puzzle, is a real head start.
  </div>

<script>window.PY_PIT = {data};</script>
"""
    return page(
        path="pit.html",
        title=f"The Snake Pit - {SCHOOL}",
        description=f"{len(PUZZLES)} verified Python puzzles in six tiers: predict the output, "
                    "find the bug, fix the code.",
        body=body,
        canonical=SITE + "/python/pit",
        main_class="container",
        body_attrs=' data-noun="puzzles"',
    )
