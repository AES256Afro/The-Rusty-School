"""The Python School's standalone pages: home, curriculum, setup lab,
playground and achievements."""

from __future__ import annotations

import json

from .kit import SCHOOL, SITE, callout, code, esc, link, page, repl, table, term, voice

NL = chr(10)


# ------------------------------------------------------------------ home
def home(lessons: list[dict]) -> str:
    lesson_count = len(lessons)
    body = f"""
  <section class="hero">
    <div class="container hero-grid">
      <div>
        <span class="kicker">A free course for people who have never written code</span>
        <h1>Learn <span class="grad">Python</span> like it's an adventure game.</h1>
        <p class="lede">
          Python runs the science, the automation and the AI. It is also the friendliest
          language ever put in front of a beginner. This school teaches it from absolute
          zero: {lesson_count} lessons, a workshop full of real projects, puzzles, XP,
          achievements, and a python named Monty who is mildly skeptical of your code.
        </p>
        <div class="cta-row">
          <a class="btn btn-primary" href="learn/index.html">Start from zero 🐍</a>
          <a class="btn btn-ghost" href="playground.html">Run Python right now ⚡</a>
          <a class="btn btn-ghost" href="learn/f4-why-python.html">Why Python?</a>
        </div>
        <div class="pill-stat">
          <div class="stat"><span class="n">{lesson_count}</span><span class="l">lessons</span></div>
          <div class="stat"><span class="n">7</span><span class="l">levels</span></div>
          <div class="stat"><span class="n">12</span><span class="l">build-it projects</span></div>
          <div class="stat"><span class="n">100%</span><span class="l">free &amp; open</span></div>
        </div>
        <p class="impact-banner">
          🔒 No account needed. No ads, no tracking, no data harvesting, ever.
          <a href="../privacy.html">Our privacy promise</a> is one page long.
        </p>
        <p class="impact-banner">
          🧪 Every example runs <strong>in your browser</strong>, on real Python 3.14.
          Nothing you type is ever sent anywhere.
        </p>
      </div>
      <div class="hero-art">
        <img src="assets/monty.svg" alt="Monty, a friendly coiled python">
      </div>
    </div>
  </section>

  <!-- Hidden for first-time visitors. py.js unhides it and fills in the
       next step once there is any progress to pick up from. -->
  <section class="section" id="continue" hidden>
    <div class="container">
      <div class="section-head">
        <span class="kicker">Welcome back</span>
        <h2>Pick up where you left off</h2>
      </div>
      <div class="continue-body"></div>
    </div>
  </section>

  <section class="section" id="try">
    <div class="container">
      <div class="section-head">
        <span class="kicker">No installing, no signing up</span>
        <h2>Your first program is thirty seconds away</h2>
        <p>Press ▶ run. Then change a word and press it again. You cannot break anything.</p>
      </div>
      {code('''name = "you"
print("Hello, world!")
print(f"Welcome to the school, {name}.")

for stage in ["curious", "confused", "dangerous"]:
    print(f"Today you are {stage}.")''',
            expect="""Hello, world!
Welcome to the school, you.
Today you are curious.
Today you are confused.
Today you are dangerous.""")}
      <p class="muted small">
        That is real CPython, compiled to WebAssembly, running inside this page. The first
        run downloads the interpreter (about 12 MB, once) and after that it is instant.
      </p>
    </div>
  </section>

  <section class="section" id="why">
    <div class="container">
      <div class="section-head">
        <span class="kicker">Why Python?</span>
        <h2>The language that ate the world quietly</h2>
        <p>Not hype. Here is what it is actually good at, with the receipts in the lessons.</p>
      </div>
      <div class="grid cols-3">
        <div class="card"><span class="emoji">📖</span>
          <h3>It reads like English</h3>
          <p>No semicolons, no curly braces, no ceremony. Code you write in week one is
          still readable in year three, which is more than most languages manage.</p>
        </div>
        <div class="card"><span class="emoji">🔬</span>
          <h3>It owns science and AI</h3>
          <p>The first image of a black hole, LIGO's gravitational waves, and essentially
          all modern machine learning were assembled with Python.</p>
        </div>
        <div class="card"><span class="emoji">🔌</span>
          <h3>Batteries genuinely included</h3>
          <p>Dates, files, zip, JSON, databases, HTTP, testing: all built in. Then half a
          million more packages on PyPI for everything else.</p>
        </div>
        <div class="card"><span class="emoji">🤖</span>
          <h3>It is how you talk to AI</h3>
          <p>Every major model provider ships a Python library first. Level 6 of this
          course builds you a private assistant with one.</p>
        </div>
        <div class="card"><span class="emoji">🧹</span>
          <h3>It automates the boring</h3>
          <p>Rename 4,000 files, tidy a spreadsheet, back up a folder, scrape a page,
          post to an API. Fifty lines and an afternoon of your life back.</p>
        </div>
        <div class="card"><span class="emoji">💼</span>
          <h3>It is everywhere jobs are</h3>
          <p>Instagram, Netflix, Spotify, Dropbox and NASA all run production Python. It
          sits at or near the top of every language ranking published.</p>
        </div>
      </div>
      <div class="callout warn">
        <span class="co-title">⚖️ And the honest downsides</span>
        Python is slow compared to compiled languages, its threading has a famous asterisk,
        and shipping a program to a stranger is fiddlier than it should be. We cover all
        three properly in <a href="learn/f4-why-python.html">Base Camp 4</a> rather than
        pretending they do not exist. A course that only sells you the upside is an advert.
      </div>
    </div>
  </section>

  <section class="section" id="path">
    <div class="container">
      <div class="section-head">
        <span class="kicker">Your journey</span>
        <h2>Seven levels, from "what is a variable" to "I built my own AI assistant"</h2>
        <p>Short lessons, heavy handholding, a lot of small wins. Progress saves in your browser.</p>
      </div>
      <div class="grid cols-4">
        <a class="card" href="learn/index.html#level-0">
          <span class="badge l0">Level 0 · Base Camp</span>
          <h3>🏕️ Before any code</h3>
          <p>What a computer is, what programming is, what Python is, and a terminal
          survival guide. Code-free and jargon-slaying.</p>
        </a>
        <a class="card" href="learn/index.html#level-1">
          <span class="badge l1">Level 1 · First Words</span>
          <h3>🌱 The whole language, small</h3>
          <p>Printing, variables, numbers, text, questions, decisions, loops, and how to
          read an error message without fear.</p>
        </a>
        <a class="card" href="learn/index.html#level-2">
          <span class="badge l2">Level 2 · The Toolbox</span>
          <h3>🧰 Data and functions</h3>
          <p>Lists, dictionaries, sets, comprehensions, and writing your own functions.
          This is where it starts to feel like power.</p>
        </a>
        <a class="card" href="learn/index.html#level-3">
          <span class="badge l3">Level 3 · Real Programs</span>
          <h3>🏗️ Software, not scripts</h3>
          <p>Files, exceptions, JSON, dates, regex, virtual environments, command-line
          tools, debugging and testing.</p>
        </a>
        <a class="card" href="learn/index.html#level-4">
          <span class="badge l4">Level 4 · Pythonic</span>
          <h3>🎩 The good stuff</h3>
          <p>Classes, dataclasses, generators, decorators, context managers, type hints,
          and concurrency explained honestly.</p>
        </a>
        <a class="card" href="learn/index.html#level-5">
          <span class="badge l5">Level 5 · In the Wild</span>
          <h3>🌍 What people build</h3>
          <p>Automation, APIs, scraping, web apps, databases, data analysis, charts,
          games, packaging, performance and security.</p>
        </a>
        <a class="card" href="learn/index.html#level-6">
          <span class="badge l6">Level 6 · Jarvis</span>
          <h3>🤖 Your own AI assistant</h3>
          <p>How models actually work, your first API call, memory, streaming, tools,
          your own documents, voice, and running it all locally.</p>
        </a>
        <a class="card" href="build/index.html">
          <span class="badge build">The Workshop</span>
          <h3>🔨 Twelve real projects</h3>
          <p>Built from a spec, not a script: a dice game, a password vault, a Markdown
          blog engine, a Discord-style bot, and more.</p>
        </a>
      </div>
    </div>
  </section>

  <section class="section" id="game">
    <div class="container">
      <div class="section-head">
        <span class="kicker">Gamified, but not gimmicky</span>
        <h2>Earn XP for things that actually make you better</h2>
      </div>
      <div class="quest-map">
        <div class="quest"><span class="q-icon">📚</span><div>
          <h3>Lessons: 100 XP</h3>
          <p>Read it, run the examples, do the exercises, mark it complete. Twelve ranks,
          from Stowaway to Harbourmaster of the Interpreter.</p></div></div>
        <div class="quest"><span class="q-icon">🐍</span><div>
          <h3>The Snake Pit: 60 XP a puzzle</h3>
          <p>Predict the output, find the bug, fix the code. Six tiers from Egg to
          Basilisk. <a href="pit.html">Enter the pit →</a></p></div></div>
        <div class="quest"><span class="q-icon">⚔️</span><div>
          <h3>The Insult Compiler</h3>
          <p>Swordfighting where the insults are real Python error messages and the
          comebacks are the fixes. Error literacy is the most underrated beginner skill
          there is. <a href="insults.html">Draw your sword →</a></p></div></div>
        <div class="quest"><span class="q-icon">🏅</span><div>
          <h3>Achievements</h3>
          <p>Twenty-one of them, including one for finishing lessons at both schools on
          this campus. <a href="achievements.html">See the trophy cabinet →</a></p></div></div>
        <div class="quest"><span class="q-icon">🔨</span><div>
          <h3>Projects: 250 XP</h3>
          <p>The cure for tutorial hell. A spec, a ladder of hints, a reference solution
          you only see if you want it. <a href="build/index.html">Open the workshop →</a></p></div></div>
      </div>
    </div>
  </section>

  <section class="section" id="campus">
    <div class="container">
      <div class="callout info">
        <span class="co-title">🦀 There is a sister school next door</span>
        <p>The Python School shares its campus, design and accounts with
        <a href="../index.html"><strong>The Rusty School</strong></a>, which teaches Rust
        from the same starting point. Python and Rust are the two most useful languages you
        can know at once: one for speed of thought, one for speed of machine. Sign in at
        either and your progress follows you to both.</p>
      </div>
    </div>
  </section>
"""
    return page(
        path="index.html",
        title=f"{SCHOOL} - Learn Python from Zero",
        description=(
            "A free, beginner-first Python course: run real Python in your browser, "
            f"{lesson_count} lessons from absolute zero to building your own AI assistant, "
            "with projects, puzzles, quizzes and XP."
        ),
        body=body,
        canonical=SITE + "/python/",
    )


# ------------------------------------------------------------------ curriculum
def curriculum(lessons: list[dict], levels: dict) -> str:
    sections = []
    for level, (label, cls, noun, blurb) in levels.items():
        mine = [l for l in lessons if l["level"] == level]
        if not mine:
            continue
        cards = []
        for l in mine:
            cards.append(
                f'      <a class="card lesson-card" data-lesson="{l["id"]}" href="{l["slug"]}.html">'
                f'<span class="num">{"B" if level == 0 else ""}{l["num"]}</span>'
                f'<div><h3>{l["title"]}</h3><p>{l["card"]}</p></div></a>'
            )
        short = label.split("·")[-1].strip()
        sections.append(f"""  <section class="section" id="level-{level}">
    <h2><span class="badge {cls}">Level {level}</span> &nbsp;{short}
      <span class="muted small">- {blurb}</span></h2>
    <div class="grid cols-2">
{NL.join(cards)}
    </div>
  </section>""")

    lesson_index = json.dumps(
        [{"id": l["id"], "level": l["level"]} for l in lessons], separators=(",", ":")
    )

    body = f"""  <section class="lesson-header">
    <span class="kicker">The curriculum</span>
    <h1>Your <span class="grad">learning path</span> 🗺️</h1>
    <p class="lede muted">
      {len(lessons)} lessons across seven levels, starting before code and ending with a
      private AI assistant you built yourself. Every lesson has plain-English explanations,
      examples that run in the page, and exercises with hidden solutions.
    </p>

    <div class="xp-wrap" id="xp-wrap">
      <div class="xp-top">
        <span class="rank-chip"><span class="rank-num">1</span><span class="rank-name">Stowaway</span></span>
        <span class="xp-nums">0 XP</span>
      </div>
      <div class="xp-bar"><div class="xp-fill" id="xp-fill"></div></div>
      <p class="xp-note">Lessons are 100 XP. Puzzles are 60. Projects are 250. Quiz answers
      are 20 each. <a href="../achievements.html">Achievements</a> pay bonuses.</p>
    </div>

    <div class="progress-wrap">
      <div class="progress-bar"><div class="progress-fill" id="progress-fill"></div></div>
      <div class="progress-label" id="progress-label"></div>
    </div>
  </section>

  <div class="callout tip">
    <span class="co-title">🍵 A good rhythm</span>
    One lesson per sitting. Type the examples out yourself rather than pasting them; fingers
    remember what eyes skim. Do the exercises before revealing the answers, take the level
    quiz when you finish a level, and build the matching workshop project before moving on.
    Nothing here expires, and nobody is timing you.
  </div>

{NL.join(sections)}

  <section class="section">
    <div class="callout info">
      <span class="co-title">🔨 Lessons teach the language. Projects teach programming.</span>
      When a level is done, go and build something from the
      <a href="../build/index.html">Project Workshop</a> before starting the next one. The
      gap between "I understood that lesson" and "I can write that from a blank file" is
      the entire job, and the only way across it is a blank file.
    </div>
  </section>

<script>window.PY_LESSONS = {lesson_index};</script>
"""
    return page(
        path="learn/index.html",
        title=f"Curriculum - {SCHOOL}",
        description=(
            f"The full {len(lessons)}-lesson Python curriculum, from what a computer is "
            "through to building your own AI assistant."
        ),
        body=body,
        canonical=SITE + "/python/learn/",
    )


# ------------------------------------------------------------------ setup lab
def setup() -> str:
    body = f"""
  <section class="lesson-header">
    <span class="kicker">The Setup Lab</span>
    <h1>Set up your <span class="grad">Python lab</span> 🔧</h1>
    <p class="lede muted">
      Ten minutes, once. Pick your operating system below. Every step says what to type,
      what you should see, and what to do when you see something else instead.
    </p>
  </section>

  <div class="callout tip">
    <span class="co-title">🧪 You do not need any of this to start</span>
    Every example in Levels 1 and 2 runs in your browser, and the
    <a href="playground.html">Playground</a> is a complete editor with nothing installed.
    Come back here when you want to work with real files on your own machine, which is
    around Lesson 21.
  </div>

  <div class="tabs">
    <button class="tab-btn active" data-tab="windows">🪟 Windows</button>
    <button class="tab-btn" data-tab="macos">🍎 macOS</button>
    <button class="tab-btn" data-tab="linux">🐧 Linux</button>
    <button class="tab-btn" data-tab="editor">✏️ Editor</button>
    <button class="tab-btn" data-tab="trouble">🚑 When it breaks</button>
  </div>

  <div class="tab-panel active" id="tab-windows">
    <h2>Windows</h2>
    <ol class="steps">
      <li><strong>Download the installer.</strong> Go to
        {link("python.org/downloads", "https://www.python.org/downloads/")} and press the big
        yellow button. It detects Windows automatically.</li>
      <li><strong>Tick the box. This is the whole lesson.</strong> On the first installer
        screen there is a checkbox at the bottom: <strong>"Add python.exe to PATH"</strong>.
        Tick it. If you miss it, the terminal will not find Python and you will spend an hour
        confused. Then press "Install Now".
        <div class="callout danger" style="margin-top:8px">
          <span class="co-title">🪤 Ninety percent of Windows setup pain</span>
          is that unticked box. If you already installed without it, re-run the installer,
          choose "Modify", and add it.
        </div></li>
      <li><strong>Open PowerShell.</strong> Press Start, type <code>powershell</code>, press
        Enter.</li>
      <li><strong>Check it worked.</strong>
        {term("PS C:\\Users\\you> python --version" + NL + "Python 3.13.5")}
        Any 3.11 or newer is fine.</li>
      <li><strong>Check pip too.</strong> pip installs other people's code and comes with
        Python.
        {term("PS C:\\Users\\you> pip --version" + NL + "pip 25.0 from C:\\... (python 3.13)")}</li>
    </ol>
    {callout("warn", "🏪 A note on the Microsoft Store version",
             "<p>Typing <code>python</code> on a fresh Windows sometimes opens the Store. That "
             "is a placeholder, not Python. Install from python.org instead: the Store build "
             "sandboxes file access in ways that will confuse you later.</p>")}
  </div>

  <div class="tab-panel" id="tab-macos">
    <h2>macOS</h2>
    <ol class="steps">
      <li><strong>Do not use the Python that is already there.</strong> macOS ships an old
        Python for its own use. Leave it alone.</li>
      <li><strong>Install a real one.</strong> Either download from
        {link("python.org/downloads", "https://www.python.org/downloads/")} and run the
        <code>.pkg</code>, or if you use Homebrew:
        {term("brew install python@3.13")}</li>
      <li><strong>Open Terminal.</strong> Cmd+Space, type <code>terminal</code>, Enter.</li>
      <li><strong>Check it.</strong>
        {term("$ python3 --version" + NL + "Python 3.13.5")}
        Always <code>python3</code> with the 3, on macOS.</li>
      <li><strong>Check pip.</strong>
        {term("$ python3 -m pip --version" + NL + "pip 25.0 from /opt/homebrew/... (python 3.13)")}
        Using <code>python3 -m pip</code> rather than bare <code>pip</code> guarantees you are
        installing into the same Python you are running. Make it a habit.</li>
    </ol>
  </div>

  <div class="tab-panel" id="tab-linux">
    <h2>Linux</h2>
    <p>It is already installed. Check which version:</p>
    {term("$ python3 --version" + NL + "Python 3.12.3")}
    <p>If it is older than 3.11, or <code>pip</code> and <code>venv</code> are missing:</p>
    {term("""# Debian, Ubuntu, Mint
sudo apt update && sudo apt install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip""")}
    {callout("warn", "🐧 Do not fight your system Python",
             "<p>On Linux the system Python belongs to your package manager, and installing "
             "things into it with <code>sudo pip</code> can break system tools. Newer distros "
             "block it outright with an <code>externally-managed-environment</code> error. "
             "That error is protecting you. Use a virtual environment (Lesson 26); it is two "
             "commands and it makes the problem disappear forever.</p>")}
  </div>

  <div class="tab-panel" id="tab-editor">
    <h2>An editor that helps you</h2>
    <p>
      Take {link("VS Code", "https://code.visualstudio.com")} unless you have a reason not to.
      It is free, runs everywhere, and every tutorial on earth assumes it.
    </p>
    <ol class="steps">
      <li><strong>Install VS Code</strong> from the link above.</li>
      <li><strong>Install the Python extension.</strong> Open the Extensions panel (the
        blocks icon in the sidebar), search "Python", install the one published by Microsoft.
        You get colouring, error squiggles, autocomplete and a Run button.</li>
      <li><strong>Open a folder, not a file.</strong> File, Open Folder, choose your
        <code>python-school</code> folder. This one habit prevents a surprising amount of
        confusion later.</li>
      <li><strong>Pick your interpreter.</strong> Press Ctrl+Shift+P (Cmd+Shift+P on Mac),
        type "Python: Select Interpreter", choose the 3.13 you just installed.</li>
      <li><strong>Turn on format-on-save</strong> once you reach Lesson 30. Settings, search
        "format on save", tick it. Never argue about spacing again.</li>
    </ol>
    {callout("tip", "⌨️ The four shortcuts worth memorising",
             "<p><code>Ctrl+S</code> save. <code>Ctrl+/</code> comment out the selected lines. "
             "<code>Ctrl+Shift+P</code> the command palette, which can do everything. "
             "<code>Ctrl+`</code> opens a terminal inside the editor, already standing in your "
             "project folder. On a Mac, Cmd instead of Ctrl.</p>")}
  </div>

  <div class="tab-panel" id="tab-trouble">
    <h2>When it breaks</h2>
    {table(
        ["What you see", "What it means", "What to do"],
        [
            ["<code>command not found: python3</code><br><code>'python' is not recognized</code>",
             "The shell cannot find Python",
             "Windows: reinstall with 'Add to PATH' ticked. All: close and reopen the terminal after installing"],
            ["<code>can't open file 'hello.py'</code>",
             "You are not in the folder that holds the file",
             "Run <code>ls</code> (or <code>dir</code>) and look. <code>cd</code> to the right folder"],
            ["<code>SyntaxError: invalid syntax</code>",
             "A typo. Very often a missing bracket or quote on the line ABOVE the one named",
             "Read the line number, then look one line up. Lesson 10 covers this properly"],
            ["<code>IndentationError</code>",
             "Your spacing is inconsistent",
             "Use four spaces per level, never tabs. In VS Code: 'Convert Indentation to Spaces'"],
            ["<code>ModuleNotFoundError: No module named 'x'</code>",
             "That package is not installed in the Python you are running",
             "<code>python3 -m pip install x</code>, and see Lesson 26 on virtual environments"],
            ["<code>externally-managed-environment</code>",
             "Linux is protecting its system Python",
             "Make a virtual environment: <code>python3 -m venv .venv</code> then activate it"],
            ["Two Pythons, wrong one runs",
             "PATH order",
             "<code>which python3</code> (macOS/Linux) or <code>where python</code> (Windows) shows which one wins"],
        ],
    )}
    <h3>The universal check</h3>
    <p>When anything is confusing, ask Python itself which Python is talking:</p>
    {code('''import sys
print(sys.version)
print(sys.executable)''', run=False, verify="compile")}
    <p>
      That prints the exact version and the exact file being run. Nine times out of ten,
      "it works in my editor but not my terminal" is those two lines disagreeing.
    </p>
  </div>

  <section class="section">
    <h2>Prove the lab works</h2>
    <p>Make a file called <code>hello.py</code>, put this in it, and run
    <code>python3 hello.py</code>:</p>
    {code('''import sys

print("Python is installed and working.")
print(f"Version: {sys.version.split()[0]}")
print("Lab status: operational. Go and learn something.")''', run=False, verify="compile")}
    <p>
      Three lines of output means you are done. Go to
      <a href="learn/index.html">Level 1</a>.
    </p>
  </section>
"""
    return page(
        path="setup.html",
        title=f"Setup Lab - {SCHOOL}",
        description="Install Python and an editor on Windows, macOS or Linux, with a troubleshooting table for every common error.",
        body=body,
        canonical=SITE + "/python/setup",
        main_class="container narrow",
    )


# ------------------------------------------------------------------ playground
def playground() -> str:
    body = """
  <section class="lesson-header">
    <span class="kicker">The Playground</span>
    <h1>Write Python <span class="grad">right here</span> ⚡</h1>
    <p class="lede muted">
      A real Python 3.14 interpreter, running inside this page. Nothing is installed and
      nothing is uploaded: your code never leaves your machine, because there is no server
      to send it to.
    </p>
  </section>

  <div class="pg-toolbar">
    <button class="btn btn-primary" id="pg-run">▶ Run (Ctrl+Enter)</button>
    <select class="pg-select" id="pg-example" aria-label="Load an example">
      <option value="hello">Hello, world</option>
      <option value="variables">Variables and f-strings</option>
      <option value="fizzbuzz">FizzBuzz (loops and conditions)</option>
      <option value="lists">Lists and looping</option>
      <option value="dicts">Dictionaries</option>
      <option value="input">Asking for input</option>
      <option value="classes">Classes and objects</option>
      <option value="errors">Broken on purpose</option>
    </select>
    <span class="pg-status" id="pg-status">starting up…</span>
  </div>

  <div class="pg-grid">
    <textarea class="pg-editor" id="pg-editor" spellcheck="false"
      aria-label="Python code editor"></textarea>
    <div class="pg-output-wrap">
      <p class="pg-output-label muted">Output</p>
      <pre class="pg-output" id="pg-output"><span class="run-warn">Press run, or Ctrl+Enter.</span></pre>
    </div>
  </div>

  <p class="stdin-note">
    💬 <code>input()</code> works: when your program asks a question, your browser pops up a
    box. Your draft is saved in this browser automatically.
  </p>

  <div class="callout tip" style="margin-top:22px">
    <span class="co-title">🧠 How this works, since you will wonder</span>
    <p>
      This is <a href="https://pyodide.org" target="_blank" rel="noopener">Pyodide</a>: the
      actual CPython interpreter compiled to WebAssembly, so it runs at native-ish speed in a
      sandbox your browser already trusts. The whole standard library is here: try
      <code>import json</code>, <code>import random</code>, <code>import datetime</code>.
    </p>
    <p>
      What is <em>not</em> here: the network (no <code>requests</code>), your files, and
      anything that needs an operating system. For those, do
      <a href="setup.html">the ten-minute lab setup</a> and run Python properly on your own
      machine.
    </p>
  </div>

  <div class="callout warn">
    <span class="co-title">♾️ If you write an infinite loop</span>
    The school stops any program that runs longer than 20 seconds and tells you so. This is
    a feature: writing a loop that never ends is a rite of passage, and freezing your own
    browser tab should not be the punishment.
  </div>
"""
    return page(
        path="playground.html",
        title=f"The Playground - {SCHOOL}",
        description="Write and run real Python 3.14 in your browser. No installs, no uploads, no account.",
        body=body,
        canonical=SITE + "/python/playground",
    )


# ------------------------------------------------------------------ achievements
def account() -> str:
    """The Python School's account page.

    Deliberately the same flow as the Rusty School's: one campus, one
    session, one database row. Signing in here signs you in there, and
    the OAuth round trip carries a `from=python` marker so you land back
    on this page rather than being dumped at the other school's door.
    """
    body = """
  <section class="lesson-header">
    <span class="kicker">Optional, always</span>
    <h1>Your <span class="grad">account</span> 🎒</h1>
    <p class="lede muted">
      The school works perfectly without one. Your progress lives in this browser and
      signing in is <strong>never required</strong>. Sign in only if you want your lessons,
      puzzles, XP and quiz scores to follow you between devices. Nothing is harvested,
      profiled or sold, we store almost nothing, and you can see, download or erase all of
      it right here. The details are in the
      <a href="../privacy.html">one-page privacy promise</a>.
    </p>
  </section>

  <div id="account-root" class="section" style="padding-top:6px">
    <div class="card"><p class="muted">Checking your session…</p></div>
  </div>

  <!-- Signed-out view -->
  <template id="tpl-signed-out">
    <div class="card" style="max-width:560px">
      <h3 style="margin-top:0">Sign in to sync</h3>
      <p class="muted small">
        We ask your provider for the bare minimum: a display name and a picture.
        No email, no contacts, no posting rights, no permission to read anything of yours.
      </p>
      <div class="cta-row" id="provider-buttons"></div>
      <p class="muted small" id="provider-note" hidden>
        Sign-in is being set up and is not live quite yet. Your progress is safe in this
        browser meanwhile. 🐍
      </p>
      <p class="muted small" id="auth-error" hidden></p>
    </div>
  </template>

  <!-- Signed-in view -->
  <template id="tpl-signed-in">
    <div class="card" style="max-width:560px">
      <div style="display:flex;align-items:center;gap:14px">
        <img id="acct-avatar" alt="" style="width:56px;height:56px;border-radius:50%;background:var(--surface-2)">
        <div>
          <h3 style="margin:0" id="acct-name"></h3>
          <p class="muted small" style="margin:2px 0 0">signed in with <span id="acct-provider"></span></p>
        </div>
      </div>
      <p style="margin-top:16px" id="acct-progress"></p>
      <p class="muted small" id="acct-sync-note"></p>
      <div class="cta-row">
        <a class="btn btn-ghost btn-small" href="learn/index.html">Continue learning →</a>
        <a class="btn btn-ghost btn-small" href="/api/me/export">Download my data</a>
        <button class="btn btn-ghost btn-small" id="btn-signout" type="button">Sign out</button>
      </div>
      <hr class="soft" style="margin:22px 0">
      <p class="muted small">
        Deleting your account erases your name, picture and synced progress from our
        database immediately and permanently. Progress saved in your browsers stays in
        those browsers.
      </p>
      <button class="btn btn-ghost btn-small" id="btn-delete" type="button" style="border-color:var(--red);color:var(--red)">
        Delete my account
      </button>
    </div>
  </template>

  <div class="callout info" style="max-width:560px">
    <span class="co-title">🎓 One account, both schools</span>
    This is the same account as the <a href="../account.html">Rusty School's</a>. Sign in at
    either and your progress follows you to the other: finished lessons, solved puzzles,
    best quiz scores, milestones, XP and achievements. There is even an achievement
    (Bilingual 🦀) for learning at both.
  </div>

  <div class="callout" style="max-width:560px">
    <span class="co-title">📦 What syncing actually includes</span>
    Completed lessons and puzzles, best quiz scores, and which completions were already
    counted toward the public banner, so moving between devices never double-counts.
    That is the entire list. Your playground code never leaves your browser, because the
    Python in this school runs <em>in</em> your browser.
  </div>
"""
    return page(
        path="account.html",
        title=f"Your account - {SCHOOL}",
        description=(
            "Optional sign-in for the Python School: sync your lessons, puzzles and quiz "
            "scores across devices. No email collected, and you can erase everything."
        ),
        body=body,
        canonical=SITE + "/python/account",
        main_class="container narrow",
    )


def achievements() -> str:
    body = """
  <section class="lesson-header">
    <span class="kicker">The trophy cabinet</span>
    <h1>Achievements 🏅</h1>
    <p class="lede muted">
      Twenty-one of them. Every one is earned by doing something that genuinely makes you a
      better programmer, with the possible exception of the one about staying up too late.
    </p>
    <p class="muted" id="ach-count">counting…</p>

    <div class="xp-wrap" id="xp-wrap">
      <div class="xp-top">
        <span class="rank-chip"><span class="rank-num">1</span><span class="rank-name">Stowaway</span></span>
        <span class="xp-nums">0 XP</span>
      </div>
      <div class="xp-bar"><div class="xp-fill" id="xp-fill"></div></div>
      <p class="xp-note">Achievements pay bonus XP on top of the lessons, puzzles and
      projects that earn them.</p>
    </div>
  </section>

  <div id="ach-root"></div>

  <div class="callout info" style="margin-top:26px">
    <span class="co-title">🔒 Where this is stored</span>
    In your browser, in localStorage, like everything else here. If you
    <a href="account.html">sign in</a> (optional, GitHub or Google, no email collected)
    it follows you between devices and between both schools on this campus. If you never
    sign in, nothing about you is ever sent anywhere.
  </div>
"""
    return page(
        path="achievements.html",
        title=f"Achievements - {SCHOOL}",
        description="The Python School's twenty-one achievements, XP ranks, and how to earn them.",
        body=body,
        canonical=SITE + "/python/achievements",
        main_class="container narrow",
    )
