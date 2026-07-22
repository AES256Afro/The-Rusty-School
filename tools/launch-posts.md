# Launch posts

Copy-paste drafts for sharing The Rusty School, one per venue. Edit freely:
these should sound like you, and a post in your own voice beats a polished one
that isn't.

---

## Two honesty decisions to make first

Both communities below are allergic to spin, and both will find out anyway.
Deciding deliberately beats getting caught.

**1. AI assistance.** This site was built with heavy AI help. r/rust and Hacker
News both react badly to undisclosed AI-generated content, and well to people
who are upfront. Options:

- *Disclose plainly* (recommended): a single line like "I built this with a lot
  of AI assistance, and I checked every code example compiles." Honest, defuses
  the objection, and the verification detail is the part that earns trust.
- *Don't mention it*: fine if nobody asks, bad if someone spots it and you look
  evasive.

Whichever you pick, **never claim you hand-wrote it all.** The drafts below
include the disclosure line; delete it if you decide otherwise.

**2. The playground uses play.rust-lang.org's API.** The Run buttons proxy to
the official Rust Playground, which is community-funded infrastructure. Saying
so is both accurate and courteous, and the r/rust crowd will respect it far more
than discovering it themselves. It is one clause; leave it in.

---

## r/learnrust (post this one first)

**Title:** I built a free Rust course for people who have never programmed at
all, and I would like it torn apart

**Body:**

I have been learning Rust, and I kept hitting the same wall: almost every
resource assumes you already program in something else. The Rust Book is
excellent but assumes a lot. Rustlings assumes you can already read Rust.

So I built the thing I wanted when I started: https://rustyschool.com

What is different about it:

- **A Level 0 for people who have genuinely never programmed.** Before any Rust,
  five short lessons on what a CPU and memory actually are, how to use a
  terminal, what git is, naming conventions, and the debugging mindset. No code
  at all in that level.
- **28 lessons** from Hello World through ownership and lifetimes to async,
  unsafe, and performance.
- **Run buttons on the examples.** Most code samples execute right in the page
  (it proxies to the official Rust Playground API, so thanks to the Rust infra
  team for that).
- **A project workshop.** Three projects so far where you get a spec instead of
  a tutorial, plus a hint ladder that goes from a gentle nudge to full code, so
  you choose how much help you take.
- Quizzes, a 100+ term glossary linked back to lessons, and printable cheat sheets.

Free, no ads, no tracking, no account required (sign-in only exists to sync
progress across devices, and it does not even ask your provider for your email).

I built this with a lot of AI assistance. Every reference solution was compiled
and run before publishing, which is how I caught that `rand` renamed
`thread_rng`/`gen_range`, so the guessing game project teaches checking docs.rs
when tutorials go stale.

**What I actually want:** if you are a beginner, tell me where you got stuck or
confused. If you are experienced, tell me what I taught wrong. I would rather
fix it than be told it is nice.

---

## r/rust (shorter, different angle, post a day or two later)

**Title:** The Rusty School: a beginner course whose website is served by a
202-line dependency-free Rust web server that students rebuild as the capstone

**Body:**

https://rustyschool.com

I wanted a Rust course that assumes zero programming background, so I built one.
The part this crowd might find fun: the site is served by a web server written
in std-only Rust, no dependencies, and the final workshop project is rebuilding
that server from a spec. The source is commented as a teaching artifact and
mapped to the lessons that cover each concept.

Also included: a Level 0 for people who have never programmed, in-page runnable
examples (via the official Playground API), a project workshop with staged hints,
and a glossary.

Source: https://github.com/AES256Afro/The-Rusty-School

Built with substantial AI assistance; all reference code was compiled and run
before publishing. Corrections very welcome, especially anywhere I have taught
something subtly wrong.

---

## Show HN

**Title:** Show HN: A Rust course served by a Rust web server students rebuild

**Body:**

https://rustyschool.com

I wanted to learn Rust and found that most material assumes you already program.
This starts from "what is a CPU," goes through ownership and lifetimes to
threads, and ends with a project where you rebuild the site's own web server.

That server is 202 lines of std-only Rust with zero dependencies, commented as a
teaching artifact. Code examples run in the page via the official Rust Playground
API. Everything is static and hosted free on Cloudflare Pages, so it costs
nothing to run.

No ads, no tracking, no account needed. Sign-in exists only to sync progress and
deliberately does not request your email address.

Built with heavy AI assistance; every reference solution was compiled and run
before publishing. Feedback and corrections welcome.

---

## Short versions

**Discord / Slack (Rust communities):**

> I built a free Rust course aimed at people who have never programmed:
> https://rustyschool.com. Level 0 covers computers, terminals, and git before any
> code, then 28 lessons through to async and unsafe, plus runnable examples and a
> project workshop. Would genuinely appreciate corrections.

**LinkedIn:**

> I built The Rusty School, a free course that teaches Rust from absolute zero:
> no prior programming assumed. 28 lessons, in-browser runnable examples, and a
> project workshop where you build real programs from a spec.
>
> The part I enjoyed most: the site is served by a web server written in Rust,
> and the final project has students rebuild it. Free, no ads, no tracking.
>
> https://rustyschool.com

**X / Bluesky:**

> Built a free Rust course for people who have never programmed. Starts at "what
> is a CPU," ends at fearless concurrency. Runnable examples, real projects, no
> ads or tracking. The site is served by a Rust server students rebuild as the
> capstone. 🦀 https://rustyschool.com

---

## GitHub repo settings

**Description:**

> A free, beginner-first Rust course. 28 lessons from zero programming
> experience to async and unsafe, with runnable examples, quizzes, and a project
> workshop. Served by a dependency-free Rust web server.

**Website:** https://rustyschool.com

**Topics:** `rust` `learning` `education` `tutorial` `beginner-friendly`
`course` `rust-lang` `teaching` `curriculum` `learn-to-code`

---

## Posting notes

- **Order matters.** r/learnrust first: it is the friendliest audience and the
  best source of the beginner feedback you actually need. Fix whatever they find
  before posting to r/rust or HN.
- **Timing.** Weekday mornings US Eastern get the most traffic on both Reddit
  and HN. Avoid Friday evenings.
- **Reply to everyone** for the first few hours, especially critics. On HN the
  early comments set the tone, and a thoughtful reply to a harsh comment reads
  better than the harsh comment.
- **Expect the first real bug report within an hour.** That is the point. Keep a
  list; do not fix things live while the thread is active unless it is broken
  badly.
- **The counter on the homepage is honest.** It will tick up as real people
  finish lessons, and that number is worth watching more than upvotes.
