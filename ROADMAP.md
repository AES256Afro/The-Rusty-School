# 🗺️ The Rusty School: Roadmap

A campus of two schools, live at [rustyschool.com](https://rustyschool.com):

| | The Rusty School 🦀 | The Python School 🐍 |
|---|---|---|
| Lessons | 28, five levels | 68, seven levels |
| Workshop projects | 9, capstone included | 10, capstone included |
| Flagship build | (none yet) | **The Jarvis Build**, 12 guided chapters |
| Puzzles | 36 (the Dojo, six belts) | 37 (the Snake Pit, six tiers) |
| Quizzes | 5 | 7 |
| Runs code in the page | via the official Rust Playground | real CPython, in your browser (Pyodide) |
| Extras | glossary, cheat sheets, lab setup | glossary (80 terms), 18 cheat sheets, the Insult Compiler, XP and 21 achievements |

Shared across both: one account, one progress set, one search index, one
design system, one deploy pipeline. 139 pages, all static, served free.

This roadmap has two halves. **Milestones** are committed, ordered, and
sized: each one ships on its own and has a test for "done". **Suggestions**
are ideas worth doing that nobody has committed to yet. Keeping those two
lists separate is the whole point; a roadmap where everything is equally
urgent is a wish list.

---

## The next three things

1. **M10: The Bridge mission engine.** Auto-grading is the campus's biggest
   missing capability: 73 puzzles exist and not one of them checks your
   answer. See [BRIDGE.md](BRIDGE.md) for the full design.
2. **M11: The Bridge, Season 1.** The vertical slice that proves the format
   and settles the voice.
3. **M6: Instructor guides**, still the cheapest route to teaching others,
   and unblocked whenever there is an evening for it.

M1 (search), M2 (accounts), M3 (certificate), M4 (per-lesson quizzes)
and M5 (accessibility) have all shipped. See Shipped, below.

---

## Milestones

Sized in evenings, honestly. "1 evening" means one sitting; "1 week" means
a focused week of evenings, not a work week.

### M6 · Instructor guides 👩‍🏫
**Ship test:** somebody who has never taught can run a study group from one
page per level: common misconceptions, a live-demo script, discussion
prompts, a printable worksheet.
**Size:** 1 week.
This is the cheapest possible route to the stated goal of teaching others,
and it needs no backend at all. It also makes M7 worth building.

### M7 · Classroom mode 🏫
**Ship test:** a teacher makes a class code, three students join, the
teacher sees their lesson progress and quiz scores on one page.
**Size:** 1 to 2 weeks. Needs D1 (free tier).
Accounts are live, so this is unblocked. It is the feature that makes the campus usable for
meetups, families and workplaces rather than only for solo learners.

### M8 · Self-hosted Rust playground ⚙️
**Ship test:** Run buttons keep working when the official playground is
slow, rate-limited, or unhappy about our traffic.
**Size:** 1 week. First thing on this list with a monthly bill (a small
VPS, roughly five to ten dollars a month), so it waits until traffic
actually justifies it.
Python already runs client-side via Pyodide and costs nothing, which is
exactly why Rust's dependence on somebody else's compiler farm stands out.
Until then, keep the usage polite and the credit visible.

### M9 · The third school 🖥️
**Ship test:** Level 1 of a new school is as good as Python's Level 1.
**Size:** 4 to 6 weeks.
Candidate order below in Suggestions. The campus rule holds: a new school
launches only when its first level is genuinely excellent. Better two deep
schools than five shallow ones.

---

### M10 · The Bridge: mission engine and auto-grading ⚙️
**Ship test:** a learner opens a mission, writes a function in the console,
presses Run Diagnostics, and gets a per-objective pass or fail with the
failing input shown, in both schools.
**Size:** 1 week.
The enabling capability for [The Bridge](BRIDGE.md), and the only genuinely
new technology in that plan: a harness that appends hidden tests to learner
code, runs it (Pyodide for Python, the /api/run proxy for Rust) and reports
per-objective results. This closes the campus's most honest gap: the 73
existing Dojo and Snake Pit puzzles are self-marked, so nobody checks the
answer. Ships with one mission per language, because the engine is the
deliverable. Note it couples M8 to this work: every Rust diagnostic run is a
compile on somebody else's playground.

### M11 · The Bridge, Season 1: Shakedown Cruise 🚀
**Ship test:** eight missions in both languages, Cadet through Ensign,
playable start to finish, every reference solution verified.
**Size:** 1 to 2 weeks.
The vertical slice, and it must be excellent before anything else starts. The
campus rule about new schools applies: better one season people finish than
six they abandon. This is where the voice is settled for everything after.

### M12 · The Bridge: the campaign layer 🎖️
**Ship test:** ranks, insignia, the crew roster, ARCHIE's in-character
reports, and a ship's status page reflecting real progress.
**Size:** 1 week.
What turns eight exercises into a campaign. Deliberately after Season 1,
because ceremony wrapped around content that is not yet good is just noise.

### M13 · The Bridge, Seasons 2 and 3 📡
**Ship test:** 16 more missions across Ops, Science and Tactical, both
languages, all verified.
**Size:** 2 to 3 weeks.
Loops, collections, functions, structured data and files: the bulk of the
everyday-competence content.

### M14 · The Bridge, Seasons 4 and 5, and Red Alert 🔥
**Ship test:** 16 missions on classes and traits, errors, iterators,
concurrency and performance, plus the optional timed mode.
**Size:** 3 weeks.
The hardest content to write well, especially Engineering, where the point is
that the two languages genuinely disagree. Treat M8 as a hard dependency by
now.

### M15 · The Bridge, Season 6: Terminus 🌌
**Ship test:** four long multi-part capstones and a finale that acknowledges
what the learner built.
**Size:** 2 weeks.
Away missions that leave the browser for a real editor, and an ending.

---

## Suggestions

Not committed. Roughly ordered by value per evening, so the good cheap
ideas float to the top.

### Cheap and high value
- **Streaks and a weekly nudge.** The Python school already tracks daily
  activity for the Caffeinated achievement. Surfacing a gentle streak (and
  never punishing a broken one) is nearly free.
- **"Explain this error" page.** A searchable list of the fifty most common
  compiler errors and tracebacks in both languages, in plain English. This
  is what beginners actually paste into search engines.
- **Lesson feedback button.** One click at the foot of each lesson: "this
  bit confused me". Route it to a GitHub issue. The cheapest possible
  source of truth about which paragraph to rewrite.
- **Printable one-page syllabus** per school, for people who like paper.
- **A "start here" quiz** that recommends Rust or Python based on what the
  visitor wants to build. The home page asks them to choose with no help.

### Worth real effort
- **Translations.** The file-per-lesson structure makes locale folders
  straightforward. Spanish and Portuguese first, on audience size.
- **Video companions.** Five minutes per lesson, embedded, with the text
  staying canonical.
- **The Rusty Blog.** Short posts for returning-student momentum, doubling
  as an RSS feed.
- **Quiz analytics.** Which questions are most-missed, feeding lesson
  revisions. Needs M2 and a tolerance for the privacy question.
- **A yearly cohort.** Eight weeks, shared deadlines, using classroom mode.
  Cohorts finish courses at several times the rate of solo learners.

### The signature assignments (Rust)
Things no other beginner course asks of you:
- **Publish a crate.** Every graduate publishes one small real crate. Being
  a published open-source author is a rite of passage and a resume line.
- **First PR week.** A guided assignment to land one real pull request,
  teaching forks, branches, review culture, and courage.
- **The performance lab.** Port a provided slow Python script to Rust and
  benchmark honestly. Students publish their own speedup number, and learn
  profiling on the way. Doubles as the best possible cross-school lesson.
- **The security lab.** Demonstrate a buffer overflow in C in a sandbox,
  then watch the same code refuse to compile in Rust. Follow with
  RustCrypto exercises. Memory safety stops being abstract.
- **Crab Jam.** A recurring 48-hour game jam with a theme, a gallery, and
  no prizes except glory and a custom badge.
- **Advent of Rust.** A December companion guide to Advent of Code.

### Specialist tracks (after the core)
Each 6 to 10 lessons, each ending in something deployable.
- **Rust for the Web:** WebAssembly, then a browser game; an axum API; a
  Tauri desktop app. Ends with the student deploying to their own
  Cloudflare Pages, exactly like this site.
- **Game Dev with Bevy:** capstone is a finished, distributable 2D game.
- **Async Rust:** beyond Lesson 21, into a concurrent scraper and a chat
  server.
- **Embedded:** Rust on a six-dollar Pico or micro:bit. Physical results
  are rocket fuel for motivation.
- **The Interpreter Track:** build a calculator, then a tiny language. The
  classic path to deep mastery.
- **Python, further:** async, typing in earnest, packaging for PyPI, and a
  data track that stays honest about charts.

### Future schools
The engine (lesson template, quiz engine, progress tracking, deploy
pipeline) is subject-agnostic. Each new subject is a school on the same
campus: same design system, own accent colour, own mascot, shared accounts.
Roughly in order of audience overlap:

- **The Terminal School** (Linux and shell): from `cd` to scripting, ssh,
  cron, and a home server. The single most transferable skill in tech, and
  the strongest M9 candidate.
- **The Web School** (HTML, CSS, JavaScript): students inspect and rebuild
  pages of this very site, ending with a personal site on their own
  Cloudflare Pages.
- **The Data School** (SQL and spreadsheets): queries, joins, honest charts.
- **The C School** (short, advanced): manual memory management, so students
  viscerally understand what Rust automated. Best taken after Level 3, like
  visiting a museum of beautiful, dangerous machinery.
- **The Network School:** DNS, HTTP, TLS, routing. Lab: trace this site's
  own path from git push to Cloudflare edge to browser. Students already
  own every piece of the demo.
- **The Security School:** threat modelling for humans, password managers,
  2FA, phishing, encryption literacy, then hashing and certificates.
- **The Ops School:** containers, pipelines, and deploying things that stay
  up, using this repo's own auto-deploy as lesson one.
- **The AI School** (literacy, not hype): how models work, prompting well,
  when to distrust output, running a local model, and using AI to learn
  rather than to avoid learning.

---

## Shipped

### M4 · Per-lesson mini-quizzes ✅
Two or three recall questions at the foot of **every lesson in both
schools**: 74 questions across 28 Rust lessons, 144 across 68 Python
lessons, 218 in total. Spaced retrieval is the least glamorous,
best-evidenced thing available for retention.

The questions live in one data file per school
(`docs/assets/lesson-quizzes.js`, `docs/python/assets/lesson-quizzes.js`),
loaded only on lesson pages and injected above the complete button, so
none of the hand-written Rust lessons or generated Python lessons had to
change. A new lesson gains a quiz by adding one entry.

Scores reuse the existing `rusty-quiz-best` map under a `lesson-` key, so
they sync to accounts and feed XP like every other score. Every code
snippet in a question is checked by `tools/verify-quiz-code.py`: Rust
compiled with rustc (including two that must NOT compile), Python
executed and its real output compared against the answer the question
claims.

Kept short, because a changelog is not a roadmap. Newest first.

- **The Jarvis Build.** The school's flagship project: twelve guided chapters
  that take a beginner from an empty folder to a personal AI assistant with
  memory, streaming, tools, retrieval over their own notes, an installed
  command and a hard spending cap. Every step explained rather than
  specified. Level 6 teaches the ideas; this builds the thing.
- **Accessibility pass (M5).** Every badge and kicker on both schools now
  clears WCAG AA in both themes. The Level 0 badge had been sitting at
  1.78:1 in light mode, because its colour is a syntax-highlighting token
  meant for the dark code panel and was never re-themed. Toasts and code
  output are announced to screen readers instead of only appearing.
- **The completion certificate (M3).** Finish a school and print your name
  on something, drawn in the browser from your own progress.
- **Campus search (M1).** One overlay across both schools, opened with `/`
  or Cmd/Ctrl-K or the nav button. The index is built from the shipped HTML
  by `tools/build-search-index.py`, so it can never drift from what is
  actually live, and it is fetched only when somebody opens search.
  Client-side, no backend, nothing leaves the browser.
- **Accounts, switched on (M2).** GitHub and Google sign-in are live, and
  both schools have their own account page: signing in from Python returns
  to Python. Fixed a latent data-loss bug on the way, where synced progress
  was capped at 200 items and a learner finishing both schools has 188.
- **Milestones and next-step suggestions**, both schools. A twelve-stop
  spine for Python, eleven for Rust, plus an engine that names one concrete
  next action with a reason. Fixed a real bug on the way: the Python level
  achievements only evaluated correctly on the curriculum page.
- **The Python School:** 68 lessons, 10 projects, 37 verified puzzles, the
  Insult Compiler, XP and achievements, real CPython in the browser.
- **Both schools on the front door:** the campus band, "Why learn Python?",
  and cross-school nav.
- **The Project Workshop** (Rust): nine projects, capstone included.
- **The Rust Dojo:** 36 verified puzzles in six belts.
- **The impact counter:** anonymous, DNT-respecting, auditable from the
  public Worker source.
- **Accounts and progress sync:** code shipped, awaiting M2.

---

## Guiding principles

Do not lose these while growing.

1. **Beginner-first, always.** Every new page passes the test: would
   day-one Chris understand this sentence?
2. **Static-first, dependency-light.** A backend may augment the content;
   it may never gate it. Anything with a monthly bill gets flagged before
   it ships, not after.
3. **Nothing ships unverified.** Rust examples compile before publishing;
   Python examples are executed and their real output checked against the
   promised output. That rule is the school's whole credibility.
4. **Everything is a teaching artifact.** The server, the build scripts,
   the deploy pipeline, this repo's history: students should be able to
   study how the school itself is made.
5. **Finish beats perfect.** Ship each milestone small and real, exactly
   like the projects the school preaches.
6. **No em dashes.** House style.
