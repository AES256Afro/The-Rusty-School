# 🗺️ The Rusty School: Roadmap

The Rusty School today: a 28-lesson curriculum (Foundations through the Level 4
Deep Cuts: strings, patterns, error design, async, unsafe, and performance),
quizzes, cheat sheets, lab setup guides, progress tracking, and a
zero-dependency Rust web server, live at [rustyschool.com](https://rustyschool.com).

This roadmap is the broad, ambitious version of what it can become: a place where
someone goes from "never touched a terminal" to shipping real Rust software, and
then turns around and teaches the next person. Phases are ordered by
value-per-effort; each phase is shippable on its own.

---

## Phase 1: Deepen the core (near term, no backend needed)

Small additions that multiply the value of what already exists.

- **Run code in the page: "The Rusty Playground."** A playground page with our
  editor and theme, plus Run buttons on lesson examples, executing via the
  official Rust Playground's public API (the same backend mdBook's run buttons
  use, with credit given). Compiling untrusted code needs real sandboxed
  servers, which Workers cannot do, so borrowing the official backend is the
  honest first step. If traffic ever outgrows polite use of their API, stage
  two is self-hosting the open-source playground backend (github.com/rust-lang/
  rust-playground) on a small VPS. This is the single highest-impact upgrade:
  it turns every lesson into a lab.
- **Per-lesson mini-quizzes.** Two or three questions at the end of each lesson
  (the quiz engine already supports it), plus a Foundations quiz.
- **Glossary.** An A-to-Z page of every term the course defines, each entry
  linking back to the lesson that teaches it. Beginners revisit vocabulary
  constantly; give them one place to do it.
- **Site search.** A client-side index (build a small JSON at deploy time) so
  "borrow checker" jumps straight to the right lesson section.
- **Completion certificate.** When all lessons are checked, generate a printable
  "Certified Rustacean, The Rusty School" certificate on a canvas, with Rusty on
  the seal. Silly, motivating, shareable.
- **More cheat sheets.** Traits and generics, lifetimes, concurrency decision
  chart ("which pointer/lock do I need?"), and a printable "borrow checker
  flowchart" poster.
- **Accessibility and polish pass.** Keyboard navigation for quizzes, focus
  states, alt text audit, reduced-motion audit, Lighthouse 100s across the board.

## Phase 2: The Project Workshop (course 2)

The cure for tutorial hell: a second track where every module builds a complete,
ownable program, applying the curriculum with progressively less hand-holding.

1. **Number Guessing Game** (Level 1 skills): input, loops, match ✅ shipped
2. **Tip Splitter CLI** (functions, floats, args) ✅ shipped
3. **Todo List** (structs, Vec, files): first persistent data ✅ shipped
4. **Flashcard Quizzer** (structs, files, retry rounds) ✅ shipped
5. **Text Adventure** (enums, HashMap, pattern matching) ✅ shipped
6. **Word Counter Pro** (iterators, HashMap, sorting, tests) ✅ shipped
7. **Markdown Converter** (string mastery, a real parser) ✅ shipped
8. **rustle, a mini grep** (lifetimes for real, flags, stderr) ✅ shipped
9. **Build Your Own Web Server** (capstone): recreate this site's own
   `src/main.rs` from a spec ✅ shipped. Still open: the extension ideas
   (logging, thread pool, a JSON endpoint) live on as stretch goals, and the
   **Multi-threaded Password Cracker Demo** (concurrency: educational
   brute-force of a toy hash, showing cores scale) is queued for a future batch.

Each project ships with: a spec ("build this"), staged hints (collapsed, like
exercise solutions), a reference implementation, and "stretch goals" for the bold.

### Ambitious Rust assignments (the signature stuff)

Assignments no other beginner course has, leaning into what makes this school
unique:

- **Publish a crate.** Every graduate publishes one small, real crate to
  crates.io (a word generator, a unit converter, anything). Being a published
  open-source author is a rite of passage and a resume line.
- **First PR week.** A guided assignment to land one real pull request on an
  open-source Rust project (rustlings and this school itself both welcome
  first-timers). Teaches forks, branches, review culture, and courage.
- **Borrow-checker dojo.** A page of "broken on purpose" programs ranked like
  chess puzzles (10 kyu to black belt). Fix each until it compiles. Timed mode
  for the competitive.
- **The performance lab.** Take a slow Python script (provided), port it to
  Rust, and benchmark honestly. Students publish their own speedup number and
  learn profiling along the way.
- **The security lab.** Demonstrate a buffer overflow in C in a sandbox, then
  show the same code refusing to compile in Rust. Follow with hands-on
  RustCrypto exercises: hash passwords properly, encrypt a file, verify a
  signature. Memory safety stops being abstract.
- **Crab Jam.** A recurring 48-hour game jam (Macroquad or Bevy) with a theme,
  a gallery of entries, and zero prizes except glory and a custom Ferris badge.
- **Advent of Rust.** Each December, a curated companion guide to Advent of
  Code with Rust-flavored hints, run as a community event.
- **The capstone of capstones.** Rebuild this school's own web server from a
  spec, extend it (logging, caching, JSON API), and submit it as a PR to a
  dedicated showcase repo. The school literally teaches students to rebuild
  itself.

## Phase 3: Specialist tracks (courses 3 to 6)

Parallel mini-courses after the core, each 6 to 10 lessons, each ending in a
deployable artifact.

- **Rust for the Web:** WebAssembly basics, then a browser game compiled from
  Rust; an API server with axum; a desktop app with Tauri. Ends with the student
  deploying to their own Cloudflare Pages, exactly like this site.
- **Game Dev with Bevy:** entities and components, sprites, input, collisions,
  sound; capstone is a finished, distributable 2D game (crab platformer,
  obviously).
- **Async Rust:** the fundamentals shipped as Lesson 21 (Deep Cuts); this track
  goes further: channels revisited, a concurrent web scraper, a chat server.
- **Embedded & Hardware:** Rust on a $6 Raspberry Pi Pico or micro:bit: blink an
  LED, read a sensor, build a tiny gadget. Physical results are rocket fuel for
  motivation.
- **The Interpreter Track (advanced):** build a calculator, then a tiny scripting
  language, in Rust. The classic path to deep mastery.

## Phase 4: The teaching platform (needs a light backend)

Chris's stated goal is to teach others. This phase turns the site from a course
into a school. Cloudflare Workers + KV/D1 (already in the account, free tier)
can power all of it without abandoning the static site.

- **Accounts & synced progress (GitHub + Google SSO)** *(code shipped; goes
  live once the OAuth apps are registered)*: optional sign-in via
  OAuth so progress, quiz scores, and certificates follow the student across
  devices. LocalStorage remains the no-account default; signing in merges local
  progress into the profile. Implementation sketch: a Cloudflare Worker handles
  the OAuth dance, stores only the provider id, display name, avatar, and a
  progress JSON in D1, and sets a signed session cookie. No passwords ever
  stored, no email marketing, a plain-English privacy page, and one-click
  export/delete of your data. Scope check: this is roughly a focused week of
  work, not a moonshot, and it is the right architecture (the static site stays
  static; the Worker only augments it).
- **The impact counter** *(shipped)*: a "students helped" banner on the home page backed by
  real numbers. Phase A needs no accounts at all: the site pings a Worker on
  each lesson completion (an anonymous counter increment, no personal data,
  respecting Do Not Track), and the home page shows "N lessons completed
  worldwide." Once accounts exist, add "N students, N courses finished, N
  countries." Honest counters only: numbers a student could audit from the
  public repo's Worker code.
- **Classroom mode:** a teacher creates a class code; students join; the teacher
  sees a dashboard of everyone's lesson progress and quiz scores, and can set
  "due by Friday" checkpoints. This is the feature that makes the school usable
  for meetups, family, and workplaces.
- **Instructor guides:** per-lesson teaching notes (common misconceptions, live
  demo scripts, discussion prompts, printable worksheets) so anyone can run a
  study group without preparing from scratch.
- **Discussion:** per-lesson threads, or simply an embedded link flow into a
  community Discord to start.
- **Quiz analytics:** which questions are most-missed, feeding lesson revisions.

## Phase 5: Community & scale

- **Open-source the pedagogy:** CONTRIBUTING.md, issue templates ("report a
  confusing paragraph" as a first-class issue type), and a "lesson RFC" process
  so other Rustaceans can propose content. The em-dash-free style guide included.
- **Translations:** the file-per-lesson structure makes locale folders
  (`docs/es/`, `docs/pt/`...) straightforward; recruit the community.
- **The Rusty Blog:** short posts ("this week in your Rust journey") for
  returning-student momentum, doubling as an RSS feed and newsletter source.
- **Video companions:** 5-minute screencasts per lesson, embedded; the lesson
  text remains canonical.
- **A yearly "Crab Cohort":** a scheduled 8-week community run-through of the
  curriculum with shared deadlines, using classroom mode. Cohorts finish courses
  at 5 to 10 times the rate of solo learners.

---

## The bigger campus: beyond Rust

The engine under this school (lesson template, quiz engine, progress tracking,
cheat sheets, the deploy pipeline) is subject-agnostic. Each new subject is a
"school" in the same campus: same design system, own color accent, own mascot,
shared accounts and certificates. Candidate schools, roughly in order of
audience overlap:

### Programming schools

- **The Terminal School (Linux & shell):** from `cd` to shell scripting, ssh,
  cron, and building a home server. The single most transferable tech skill.
- **The Web School (HTML, CSS, JavaScript):** students inspect and rebuild
  pages of this very site as the running example, ending with each student
  shipping a personal site on their own Cloudflare Pages.
- **The Python School:** the friendly generalist language, taught as a contrast
  ("here is the same program in Rust and Python; here is when to pick which"),
  covering scripting, automation, and data basics.
- **The Data School (SQL & spreadsheets):** queries, joins, and honest charts.
  Pairs naturally with a future D1-backed classroom dashboard.
- **The C School (short, advanced):** a guided tour of manual memory management
  so students viscerally understand what Rust automated. Best taken after
  Level 3, like visiting a museum of beautiful, dangerous machinery.

### Non-programming tech schools

- **The Network School:** how the internet actually works: DNS, HTTP, TLS,
  routing. Lab: trace this site's own path from GitHub push to Cloudflare edge
  to browser. Students already own every piece of the demo.
- **The Security School:** threat modeling for humans, password managers,
  2FA, phishing recognition, encryption literacy, then hands-on basics
  (hashing, certificates). A natural sibling to the Rust security lab.
- **The Hardware School:** build a PC, understand specs honestly, set up a
  Raspberry Pi homelab, and meet microcontrollers (bridging to the embedded
  Rust track).
- **The Ops School (Docker, CI/CD, cloud):** containers, pipelines, and
  deploying things that stay up, using this repo's own auto-deploy as lesson
  one.
- **The AI School (literacy, not hype):** how models work at a high level,
  prompting well, when to trust output, running a local model, and using AI as
  a learning tool without letting it do your homework.

Rule for the campus: a new school launches only when its Level 1 is genuinely
excellent. Better one deep school than five shallow ones.

---

## Guiding principles (do not lose these while growing)

1. **Beginner-first, always.** Every new page passes the test: "would day-one
   Chris understand this sentence?"
2. **The site stays fast and dependency-light.** Static-first; a backend only
   ever augments, never gates, the content.
3. **Everything is a teaching artifact.** The server, the deploy pipeline, the
   repo history: students should be able to study how the school itself is built.
4. **Finish beats perfect.** Ship each phase small and real, like the projects
   the school preaches.
5. **No em dashes.** House style.
