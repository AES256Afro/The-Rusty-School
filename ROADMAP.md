# 🗺️ The Rusty School: Roadmap

The Rusty School today: a 22-lesson curriculum (Foundations through Fearless
Concurrency), quizzes, cheat sheets, lab setup guides, progress tracking, and a
zero-dependency Rust web server, live at [cybercard.net](https://cybercard.net).

This roadmap is the broad, ambitious version of what it can become: a place where
someone goes from "never touched a terminal" to shipping real Rust software, and
then turns around and teaches the next person. Phases are ordered by
value-per-effort; each phase is shippable on its own.

---

## Phase 1: Deepen the core (near term, no backend needed)

Small additions that multiply the value of what already exists.

- **Run code in the page.** Wire the "copy" buttons to the Rust Playground's
  execute API so examples and exercises run inside the lesson, output and all.
  This is the single highest-impact upgrade: it turns every lesson into a lab.
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

1. **Number Guessing Game** (Level 1 skills): input, loops, match
2. **Tip Splitter CLI** (functions, floats, args): the Lesson 17 capstone, expanded
3. **Todo List** (structs, Vec, files): first persistent data
4. **Flashcard Quizzer** (HashMap, Result): reads its own card files; students
   make decks for other subjects they study
5. **Text Adventure** (enums, ownership): rooms, items, and a tiny game loop
6. **Word Counter Pro** (iterators, closures): real text analytics with sorting
7. **Multi-threaded Password Cracker Demo** (concurrency): educational brute-force
   of a toy hash, showing cores scale
8. **Build Your Own Web Server** (capstone): recreate this site's own
   `src/main.rs` from scratch, then extend it (logging, caching, a JSON endpoint)

Each project ships with: a spec ("build this"), staged hints (collapsed, like
exercise solutions), a reference implementation, and "stretch goals" for the bold.

## Phase 3: Specialist tracks (courses 3 to 6)

Parallel mini-courses after the core, each 6 to 10 lessons, each ending in a
deployable artifact.

- **Rust for the Web:** WebAssembly basics, then a browser game compiled from
  Rust; an API server with axum; a desktop app with Tauri. Ends with the student
  deploying to their own Cloudflare Pages, exactly like this site.
- **Game Dev with Bevy:** entities and components, sprites, input, collisions,
  sound; capstone is a finished, distributable 2D game (crab platformer,
  obviously).
- **Async Rust:** what async actually is (the restaurant pager analogy), tokio,
  channels revisited, a concurrent web scraper, a chat server.
- **Embedded & Hardware:** Rust on a $6 Raspberry Pi Pico or micro:bit: blink an
  LED, read a sensor, build a tiny gadget. Physical results are rocket fuel for
  motivation.
- **The Interpreter Track (advanced):** build a calculator, then a tiny scripting
  language, in Rust. The classic path to deep mastery.

## Phase 4: The teaching platform (needs a light backend)

Chris's stated goal is to teach others. This phase turns the site from a course
into a school. Cloudflare Workers + KV/D1 (already in the account, free tier)
can power all of it without abandoning the static site.

- **Accounts & synced progress:** optional sign-in; progress and quiz scores
  follow the student across devices. LocalStorage remains the no-account default.
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
