# 🦀 The Rusty School

**Learn Rust from absolute zero: no coding experience required.**

The Rusty School is a self-contained, beginner-first Rust curriculum packaged as a
website. It takes you from "what is a terminal?" to traits, lifetimes, and fearless
concurrency, with interactive quizzes, hands-on exercises, cheat sheets, and lab
setup guides for every operating system.

And yes, **the website is served by a web server written in Rust** (see
[`src/main.rs`](src/main.rs)). The server has zero dependencies, is heavily
commented, and doubles as the final reading exercise of the course.

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

## What's inside

| Where | What |
|---|---|
| `docs/index.html` | Home: why Rust, who uses it, games & apps built with Rust |
| `docs/setup.html` | Build your lab: macOS, Windows, Linux, or zero-install in the browser |
| `docs/learn/` | The 22-lesson curriculum, from "what is a computer?" to concurrency |
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

See [ROADMAP.md](ROADMAP.md) for the expansion plan: runnable in-page examples,
a project workshop track, specialist courses (web, games, async, embedded), and
a classroom mode for teaching groups.

## Project goals

- Teach Rust to people with *very little* coding experience, without dumbing it down.
- Explain **why** Rust is worth adopting, not just how to write it.
- Be fun: mascots, analogies, quizzes, small wins everywhere.
- Stay dependency-free and hackable: the whole site is readable source code.
