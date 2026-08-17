# 🖖 The Bridge

**A starship simulator for people learning to code.**

A story-driven, auto-graded campaign that runs across both schools. You are
posted to a mid-tier exploration vessel whose software is held together by
optimism, and every mission is a real coding problem wearing a uniform.

The name is doing two jobs. It is the ship's bridge, where the crew works. It
is also the bridge between the two schools: every mission exists in Python and
in Rust, and the story has opinions about which one you brought.

---

## Why this, and why now

The campus has 73 puzzles already, 36 in the Rust Dojo and 37 in the Snake Pit.
They are good, they are verified, and they share one honest weakness:

> **Nobody checks your answer.** You read the puzzle, you think, you press
> "Mark solved". The site takes your word for it.

That is fine for drill. It is not a challenge. A challenge requires the machine
to look at what you wrote and tell you whether it works, and that is the thing
The Bridge adds. Both schools already have the hard part built:

| School | How learner code runs today | Cost |
| --- | --- | --- |
| Python | Pyodide, real CPython in the browser | free, client-side, no server |
| Rust | `/api/run`, a proxy to the official playground | free, but it is somebody else's compiler farm |

So the engine is a smaller job than it looks. What is missing is a harness that
appends hidden tests to what the learner wrote, runs it, and reports which
objectives passed.

Everything else here is content, humour and progression on top of that one
capability.

---

## The setting

Genre furniture only. Bridge stations, warp cores, away teams, red alerts, a
literal-minded alien officer and a sardonic ship's computer are stock science
fiction, older than any one franchise and free for anybody to use. The names,
characters and jokes below are original to this school, because the properties
that popularised this furniture are very much owned by other people. The tone we
are aiming at is the workplace comedy one: competent adults, in a utopian
future, having mundane and undignified problems.

### The ship

The **UES Magnanimous**, an exploration vessel of the **United Expeditionary
Service**. Nobody calls her that. She is "the Maggie", she is nineteen years
old, and three of her decks have a smell that Engineering has stopped
apologising for.

You are the newly-posted **Systems Officer**. This is a real job that nobody
wanted, because the previous Systems Officer left in a hurry and their code is
still running.

### The crew

Written as recurring characters with small, human problems. They brief the
missions, they interrupt, and they have opinions about your variable names.

| Who | Role | The joke |
| --- | --- | --- |
| **Capt. Yves Dubois-Okonkwo** | Commanding officer | Genuinely excellent in a crisis. Cannot chair a meeting. Has strong, publicly stated views about the coffee replicator. |
| **Cmdr. Priya Raghunathan** | Chief Engineer | Exhausted genius. Communicates in sighs and precise numbers. Has not taken shore leave since the incident with the plasma manifold. |
| **Lt. Skree** | Science officer, of the Vell | Aggressively literal. Does not understand metaphor, idiom, or why you named a variable `temp2`. Delivers devastating criticism entirely by accident. |
| **Ens. Bo Tannenbaum** | Junior systems | Enthusiastic and dangerously confident. Writes most of the broken code you will be asked to fix. Everybody likes Bo. This is the problem. |
| **Chief T'Kala** | Security | Enormously strong, extremely gentle. Keeps a plant on the bridge. The plant has a name and a duty roster. |
| **ARCHIE** | The ship's computer | Your grader. Deadpan, faintly disappointed, technically helpful. Reports test results in character and never lies about whether your code worked. |

**ARCHIE is the most important design decision here.** He is the auto-grader
given a personality, which turns "3 of 5 tests failed" into a line of dialogue
without ever obscuring the actual result. He is never sarcastic about a genuine
mistake, because a grader that mocks you is a grader you stop using. He is
extremely sarcastic about the Captain.

---

## How a mission works

Every mission is one page with the same six parts.

1. **Briefing.** The story: what broke, who is annoyed, why it matters. Three or
   four sentences. This is where the comedy lives.
2. **Objective.** The precise, unambiguous spec. Function name, arguments,
   return value, edge cases. No jokes in here at all. The learner must be able
   to read this alone and know exactly what is wanted.
3. **The console.** An editor with starter code, usually a stub with a
   docstring or doc comment and a `TODO`.
4. **Run Diagnostics.** The button. Runs the learner's code against the hidden
   tests.
5. **ARCHIE's report.** Per-objective pass or fail, with the failing input and
   what came back. Never just "wrong".
6. **Commendation.** On a full pass: XP, rank progress, and a closing beat of
   story. Missions can be replayed; the score is the best run.

### The rule that keeps it honest

The tests run in the learner's own browser (Python) or through the playground
proxy (Rust). That means a determined person can read them. **This is fine, and
we will say so out loud rather than pretending otherwise.** It is a learning
tool, not an examination. Nobody is awarded a degree at the end, and the only
person a cheat would be cheating is themselves. Building elaborate tamper
resistance would cost real effort, break the offline-friendly design, and
protect nothing worth protecting.

---

## The stations

Six bridge stations, each mapping to a genuine area of computing. This is the
spine that stops the campaign being a random bag of exercises: every mission is
posted to a station, and a learner can see which station they keep failing at.

| Station | What it teaches | Python's turn to shine | Rust's turn to shine |
| --- | --- | --- | --- |
| 🧭 **Helm** | Control flow, loops, state machines | Readable simulation loops | `match` exhaustiveness on course states |
| 📦 **Ops** | Collections, data wrangling, resource tracking | Dicts and comprehensions | Ownership makes the manifest impossible to double-book |
| ⚙️ **Engineering** | Performance, concurrency, memory | `asyncio` for many slow sensors | Threads without data races; this is the flagship contrast |
| 🔬 **Science** | Algorithms, parsing, analysis | Batteries included, the obvious winner | Zero-cost iterators over a big signal |
| 🛡️ **Tactical** | Errors, validation, security | `try`/`except` and input hygiene | `Result` and the type system refusing bad states |
| 🩺 **Sickbay** | Debugging, testing, diagnostics | `pytest` and reading a traceback | The compiler as the first test suite |

The two-language design is the point rather than a bonus. The same briefing in
both languages, with the story noting the difference, is the campus's existing
"here is when to pick which" argument made playable. Engineering missions are
where a Rust learner feels smug. Science missions are where a Python learner
finishes in four lines and goes to lunch.

---

## Progression

### Ranks

XP already exists campus-wide; ranks here are a second, narrative track earned
by missions specifically.

| Rank | Missions cleared | Unlocks |
| --- | --- | --- |
| **Cadet** | 0 | Season 1, Helm and Ops only |
| **Ensign** | 6 | Science station, the crew quarters page |
| **Lieutenant JG** | 14 | Tactical station, Red Alert mode |
| **Lieutenant** | 24 | Engineering station, away missions |
| **Lt. Commander** | 34 | Sickbay, the holodeck sandbox |
| **Commander** | 44 | Season 6, the command chair |
| **Captain** | all | The finale, and the ship's dedication plaque with your name on it |

Ranks gate *stations*, not difficulty, so the campaign opens up rather than
merely getting harder. A Cadet has two places to fail; a Commander has six.

### Seasons

Episodic, like a television season, because that shape gives natural resting
points and a reason to come back.

| Season | Title | Teaches | Missions |
| --- | --- | --- | --- |
| 1 | **Shakedown Cruise** | Output, variables, types, input, conditionals | 8 |
| 2 | **Routine Patrol** | Loops, collections, iteration | 8 |
| 3 | **First Contact** | Functions, structured data, files | 8 |
| 4 | **The Anomaly** | Classes and traits, errors, iterators | 8 |
| 5 | **Deep Space** | Concurrency, async, performance | 8 |
| 6 | **Terminus** | Multi-part capstone systems | 4 (long) |

44 missions per language, 88 implementations in total. Every one needs a
reference solution that is executed and checked, exactly like the lessons.

### Red Alert

Unlocked at Lieutenant JG. The same mission, on a clock, with ARCHIE narrating
the hull integrity. Optional forever, because timed challenges are motivating
for some people and genuinely unpleasant for others, and this school does not
do unpleasant.

### Away missions

Unlocked at Lieutenant. Longer, multi-file problems that leave the console and
land in the learner's own editor, in the style of the existing Workshop. The
handoff is deliberate: at some point you have to build things on your own
machine, and a browser console should be the thing that teaches you to want a
real one.

---

## Two sample missions, for tone

Written out so the voice is a decision rather than an aspiration.

### Season 1 · Helm · "The Long Cold Cup"

> **Briefing.** The beverage replicator on Deck 4 has produced 340 consecutive
> cups of lukewarm water. The Captain has raised it at three consecutive
> staff meetings and is now raising it again, with feeling. Ensign Tannenbaum
> "already looked at it" and the situation has since become worse.
>
> Commander Raghunathan has traced the fault to a temperature routine. She has
> not fixed it herself, because she says this is "a good first one", which is
> Engineering for "I am extremely tired".
>
> **Objective.** Write `brew_report(celsius)` which returns:
> `"too cold"` below 82, `"acceptable"` from 82 to 96 inclusive, and
> `"the Captain is happy"` above 96.
>
> **ARCHIE, on a failing run.** *"Objective two returned 'too cold' for 82
> degrees. 82 is within the acceptable band. I have re-read the specification
> twice in case I was being unfair. I was not."*
>
> **ARCHIE, on a pass.** *"All objectives met. The Captain has been informed
> and is describing the coffee to people who did not ask."*

That mission teaches inclusive boundary conditions, which is one of the top
three things beginners get wrong, and it teaches it through a joke about an
off-by-one at exactly 82.

### Season 5 · Engineering · "Everyone Wants the Sensors"

> **Briefing.** Six science teams have queued for the long-range array and all
> six have written their own scheduling code. Lt. Skree reports that two teams
> received identical timeslots and that this is "arithmetically impossible,
> and yet". Commander Raghunathan has stopped sighing, which everybody agrees
> is the bad sign.
>
> **Objective.** Allocate timeslots to six concurrent requesters such that no
> slot is issued twice and every requester receives one.
>
> **In Python.** You will reach for a lock, and you will discover why the GIL
> did not save you.
>
> **In Rust.** You will reach for shared state, and the compiler will decline
> to let you have the bug. This is the mission where the borrow checker stops
> being an obstacle and starts being a colleague.

That is the same problem in both languages, with the languages disagreeing
about it, which is the entire thesis of a two-school campus in one exercise.

---

## Where it lives

A campus-level area, not inside either school, because it belongs to both.

```
docs/bridge/
├── index.html            the ship, the crew, your rank
├── crew.html             the roster, unlocked as you meet them
├── s1/ … s6/             seasons, one folder each
└── assets/
    ├── bridge.css        LCARS-adjacent but our own palette
    ├── bridge.js         mission runner, grading, rank display
    └── missions.js       generated mission data, both languages
```

Content is generated the way the Python school is: a `tools/bridge/` package
with one module per season, so a mission is a dict and the pages are built.
Reference solutions run through the existing verifiers. Progress ids are
`bridge-*`, which slots into the campus progress model, the account sync and
the XP system with no new plumbing.

---

## Milestones

Sized in evenings, honestly, and sequenced so that each one is shippable alone.

### M10 · The mission engine and auto-grading ⚙️

**Ship test:** a learner opens one mission, writes a function in the console,
presses Run Diagnostics, and gets a per-objective pass or fail with the failing
input shown, in both schools.

**Size:** 1 week.

The enabling capability, and the only genuinely new technology in the whole
plan. A harness that appends hidden tests to learner code, runs it (Pyodide for
Python, the `/api/run` proxy for Rust), and reports per-objective results.
Ships with exactly one mission in each language, because the engine is the
deliverable and the content is the proof it works.

Watch: Rust grading multiplies traffic to the official playground, since every
Run Diagnostics is a compile. That makes **M8 (self-hosted playground)** a
genuine dependency rather than a nice-to-have, and it should be re-read the
moment this ships.

### M11 · Season 1: Shakedown Cruise 🚀

**Ship test:** eight missions in both languages, Cadet through Ensign, playable
start to finish, every reference solution verified.

**Size:** 1 to 2 weeks.

The vertical slice, and it must be genuinely excellent before anything else
starts. The campus rule about new schools applies here too: better one season
that people finish than six they abandon. This is also where the voice gets
settled, so the writing standard for every later season is set by this one.

### M12 · The campaign layer 🎖️

**Ship test:** ranks, insignia, the crew roster, ARCHIE's in-character reports,
and a ship's status page that reflects real progress.

**Size:** 1 week.

The part that turns eight exercises into a campaign. Rank progression, station
unlocks, the crew page filling in as you meet people, and the dedication plaque.
Deliberately after Season 1, because ceremony wrapped around content that is not
yet good is just noise.

### M13 · Seasons 2 and 3 📡

**Ship test:** 16 more missions across Ops, Science and Tactical, both
languages, all verified.

**Size:** 2 to 3 weeks.

Loops, collections, functions, structured data and files. The bulk of the
everyday-competence content, and the point at which the campaign is long enough
to be worth telling people about.

### M14 · Seasons 4 and 5, and Red Alert 🔥

**Ship test:** 16 missions covering classes and traits, errors, iterators,
concurrency and performance, plus optional timed mode.

**Size:** 3 weeks.

The hardest content to write well, especially Engineering, where the whole
point is that the two languages genuinely disagree. Red Alert lands here
because by this stage there is enough material to make a timer meaningful.

### M15 · Season 6: Terminus 🌌

**Ship test:** four long multi-part capstones and a finale that acknowledges
what the learner built.

**Size:** 2 weeks.

Away missions that leave the browser for a real editor, and an ending. Sincerity
is allowed in the last one; the whole comedy register only works if the show is
willing to mean it occasionally.

---

## What could go wrong

Named up front, because a plan without failure modes is a wish.

- **The writing is the hard part, not the code.** 88 mission briefings that are
  actually funny is a comedy-writing project with a compiler attached. Season 1
  is the honest test of whether the voice sustains. If it does not, the right
  answer is fewer, better missions rather than more.
- **Auto-grading raises the bar on specs.** The moment a machine checks the
  answer, an ambiguous objective becomes a bug report. Every spec needs to be
  readable in isolation, which is why the Objective section bans jokes.
- **Rust grading has a real dependency.** Every diagnostic run is a compile on
  somebody else's infrastructure. Keep the volume polite, cache aggressively,
  and treat M8 as coupled to M14 at the latest.
- **Gating can demotivate.** Rank gates unlock stations, never difficulty, and
  nothing in the main campaign is ever locked behind a timed mode. If a gate
  ever feels like a wall, remove it.
- **Franchise gravity.** The genre furniture is free; the specific names and
  characters are not. Everything here stays original, and any contributor
  content gets read with that in mind.

---

## The thing this is really for

A learner who has finished Level 3 knows the syntax and cannot yet tell whether
they can *do* anything with it. The gap between "I understood that lesson" and
"I solved that on my own" is the whole job, and the only way across it is
problems that push back.

The Bridge is 88 problems that push back, wrapped in a reason to come back
tomorrow, in a campus that already teaches both languages and has spent this
entire project arguing that knowing two is better than knowing one.

Also the coffee replicator joke is genuinely good and it would be a waste not
to use it.
