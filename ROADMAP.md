# 🗺️ The Rusty School: Roadmap

A campus of two schools, live at [rustyschool.com](https://rustyschool.com):

| | The Rusty School 🦀 | The Python School 🐍 |
|---|---|---|
| Lessons | 28, five levels | 68, seven levels |
| Workshop projects | 9, capstone included | 10, capstone included |
| Puzzles | 36 (the Dojo, six belts) | 37 (the Snake Pit, six tiers) |
| Quizzes | 5 | 7 |
| Runs code in the page | via the official Rust Playground | real CPython, in your browser (Pyodide) |
| Extras | glossary, cheat sheets, lab setup | glossary (80 terms), 18 cheat sheets, the Insult Compiler, XP and 21 achievements |

Shared across both: one account, one progress set, one design system, one
deploy pipeline. 138 pages, all static, served free.

This roadmap has two halves. **Milestones** are committed, ordered, and
sized: each one ships on its own and has a test for "done". **Suggestions**
are ideas worth doing that nobody has committed to yet. Keeping those two
lists separate is the whole point; a roadmap where everything is equally
urgent is a wish list.

---

## The next three things

1. **M1: Site search.** The curriculum is now 96 lessons across two schools
   and there is no way to look anything up. This is the biggest gap.
2. **M2: Switch accounts on.** The code shipped months ago and sits idle
   behind two unregistered OAuth apps. An afternoon of dashboard work turns
   progress sync from "written" into "working".
3. **M3: The certificate.** Finishing 68 lessons currently earns a green
   progress bar. It should earn something you can print and show somebody.

---

## Milestones

Sized in evenings, honestly. "1 evening" means one sitting; "1 week" means
a focused week of evenings, not a work week.

### M1 · Site search 🔍
**Ship test:** typing "borrow checker" or "list comprehension" from any page
jumps to the right lesson section, offline, with no backend.
**Size:** 2 to 3 evenings.
Build a JSON index at deploy time (the Python school already generates its
own pages, so it can emit its half for free; the Rust half needs a small
script over `docs/learn/*.html`). Ship a keyboard-first overlay on `/`.
Client-side only, so it costs nothing and works on both schools at once.

### M2 · Accounts, actually on 🔑
**Ship test:** sign in with GitHub on a phone, see progress made on a
laptop.
**Size:** 1 evening, mostly dashboard clicks.
`functions/api/auth/` is written, deployed, and returns "not configured"
because no GitHub or Google OAuth app exists yet. Register both, set the
secrets, verify the round trip, then confirm the privacy page still tells
the truth about what is stored.

### M3 · The completion certificate 🎓
**Ship test:** finishing a school renders a printable certificate with your
name, the school, and the date, drawn on a canvas in the browser.
**Size:** 2 evenings.
Silly, motivating, shareable, and zero infrastructure. Ferris on the Rust
seal, Monty on the Python one. Also the natural reward for the Graduate
milestone that both schools now track.

### M4 · Per-lesson mini-quizzes for Rust 📝
**Ship test:** every Rust lesson ends with two or three questions, the way
the level quizzes already work.
**Size:** 1 week (28 lessons of writing).
The quiz engine already supports it. Python's per-level quizzes are good;
per-lesson recall is better, and the research on spaced retrieval is not
subtle. Do Rust first, then backport to Python.

### M5 · Accessibility and Lighthouse pass ♿
**Ship test:** Lighthouse 100 on accessibility across a sampled page of
each type, full keyboard navigation through quizzes, the dojo, the pit and
the playground, and a reduced-motion audit that includes the new toasts.
**Size:** 2 to 3 evenings.
Overdue. A school that turns people away at the door is not a school.

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
Depends on M2. This is the feature that makes the campus usable for
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

Kept short, because a changelog is not a roadmap. Newest first.

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
