# 🦀 The Rusty School

**Learn Rust from absolute zero: no coding experience required.**

The Rusty School is a self-contained, beginner-first Rust curriculum packaged as a
website. It takes you from "what is a terminal?" to traits, lifetimes, and fearless
concurrency, with interactive quizzes, hands-on exercises, cheat sheets, and lab
setup guides for every operating system.

And yes, **the website is served by a web server written in Rust** (see
[`src/main.rs`](src/main.rs)). The server has zero dependencies, is heavily
commented, and doubles as the final reading exercise of the course.


## 🖖 The Bridge

A starship simulator for people learning to code, live at
[rustyschool.com/bridge](https://rustyschool.com/bridge/). Six seasons, 44
missions, each playable in Python and in Rust; the ship's computer runs your
code against the mission objectives and reports which ones you met. Built by
`tools/bridgebuild.py` from `tools/bridge/`, verified by
`tools/verify-bridge.py` (every reference passes, every stub fails, nothing
hangs). Design in [BRIDGE.md](BRIDGE.md).

## Quick start

1. [Install Rust](https://rustup.rs) (the site's *Setup* page walks you through it
   for macOS, Windows, and Linux).
2. Run the school:

   ```sh
   cargo run
   ```

3. Open **http://localhost:7878** in your browser. Class is in session. 🎓

No Rust installed yet? The site is plain HTML/CSS/JS, so you can also just open
`docs/index.html` directly in a browser, or serve the `docs/` folder with any
static file server.

## 🐍 The Python School (sister course)

The same campus now has a second, self-contained course:
[**The Python School**](docs/python/index.html), a 68-lesson beginner-first Python
curriculum living under `docs/python/`. It takes an absolute beginner from "what is
a variable?" all the way to building their own AI assistant, and unlike the Rust
playground (which ships code to a compiler farm), it runs **real CPython in the
browser** via Pyodide, so every example has a working ▶ run button with nothing to
install.

It is generated, not hand-written:

```sh
python3 tools/pybuild.py            # build docs/python/ from tools/pycourse/
python3 tools/pyverify.py           # RUN every code example and prove its output
python3 tools/build-search-index.py # rebuild the campus search index
```

Run the search index builder last, and after editing any hand-written Rust page
too: it reads the shipped HTML in `docs/` rather than the sources, so the index
can never claim something the site does not actually say.

`pyverify.py` is the Python analogue of the Rust school's "compile every example
before publishing" rule: it executes all 621 runnable examples (and all 37 Snake
Pit puzzles, and the workshop reference solutions) and checks each one's real output
against what the lesson promises. Nothing ships until it runs. The generator, the
verifier, and the whole course are themselves the Level-3 reading exercise, exactly
as `src/main.rs` is for Rust.

Highlights: Base Camp (code-free foundations), Levels 1-5 (the language and what
people build with it), Level 6 (Build Your Own Jarvis), the **Snake Pit** (verified
predict/fix/bug puzzles in six tiers), and the **Insult Compiler** (Monkey-Island
error-message swordfighting). Accounts and progress are shared with the Rust school.

### The Jarvis Build

`docs/python/jarvis/` is the school's flagship project: twelve guided chapters that walk
a beginner from an empty folder to a working personal AI assistant, with every step
explained. Content lives in `tools/pycourse/jarvis_data.py`, rendered by
`tools/pycourse/jarvis.py`. Its runnable examples are output-verified like everything
else; the blocks that call the Anthropic API are parse-checked instead, since CI has
neither a network nor a key.

## What's inside

| Where | What |
|---|---|
| `docs/index.html` | Home: why Rust, who uses it, games & apps built with Rust |
| `docs/setup.html` | Build your lab: macOS, Windows, Linux, or zero-install in the browser |
| `docs/learn/` | The 28-lesson curriculum, from "what is a computer?" to async, unsafe, and profiling |
| `docs/build/` | The Project Workshop: build real programs from a spec |
| `docs/playground.html` | Write and run Rust in the browser |
| `docs/glossary.html` | Every term the course defines, A to Z |
| `docs/quiz.html` | Interactive quizzes for each level, with explanations |
| `docs/cheatsheets.html` | Printable cheat sheets: syntax, ownership, collections, Cargo |
| `src/main.rs` | The Rust web server that serves it all (and teaches while doing it) |

### The curriculum

- **Level 0 - Foundations 🌍** (never programmed): how computers think, the
  terminal, git & version control, standards & conventions, the programmer's mindset
- **Level 1 - Sprout 🌱** (total beginner): Hello World & Cargo, variables,
  data types, functions, control flow
- **Level 2 - The Rust Way 🔧**: ownership, borrowing & references, structs,
  enums & pattern matching, collections, error handling
- **Level 3 - Power Tools 🚀**: traits & generics, lifetimes, closures &
  iterators, smart pointers, concurrency, modules/testing/ecosystem

Progress is tracked in your browser (localStorage): lessons you complete get a
checkmark, and the curriculum page shows your overall progress.

## Running the tests

The server ships with unit tests (which are themselves part of Lesson 17):

```sh
cargo test
```

## Deploying the site

Everything under `docs/` is static, so deployment is trivial:

- **GitHub Pages** (easiest): push this repo, then in the repo's
  *Settings → Pages*, choose *Deploy from a branch*, branch `main`, folder
  `/docs`. Done. The site appears at `https://<user>.github.io/<repo>/`.
- **Netlify / Cloudflare Pages / Vercel**: point the publish directory at `docs/`.
- **Any server**: copy `docs/` anywhere that can serve files, or run the Rust
  server on a box of your own.

## Where this is going

[ROADMAP.md](ROADMAP.md) is the working plan: committed milestones (each sized
and with a test for "done") separated from suggestions nobody has committed to
yet. The next three are site search, switching accounts on, and a completion
certificate.

[rustyschool.com/roadmap](https://rustyschool.com/roadmap) is the same thing for
visitors, in plainer language, and deliberately honest about what is missing as
well as what is built.

## License

Two licenses, split the way educational projects usually split them:

- **Code** (the Rust server, API functions, site JS/CSS, tooling, and every
  code example inside the course): dual-licensed under
  [MIT](LICENSE-MIT) OR [Apache-2.0](LICENSE-APACHE), the Rust ecosystem's
  standard. Copy any snippet into any project, commercial or not.
- **Course content** (lesson text, puzzles, quizzes, specs, prose, artwork):
  [CC BY-NC-SA 4.0](LICENSE-CONTENT.md). Share it, translate it, teach with it,
  with credit; no commercial use, and adaptations stay under the same license.

## Project goals

- Teach Rust to people with *very little* coding experience, without dumbing it down.
- Explain **why** Rust is worth adopting, not just how to write it.
- Be fun: mascots, analogies, quizzes, small wins everywhere.
- Stay dependency-free and hackable: the whole site is readable source code.
