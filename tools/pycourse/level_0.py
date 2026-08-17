"""Level 0: Base Camp.

Six lessons before a single line of Python, for people who have never
programmed. If you have programmed before, skim these and move on: you
will not miss anything you do not already know.
"""

from __future__ import annotations

from .kit import callout, code, exercise, link, out, repl, table, term, voice

LESSONS = []


def _add(**kw):
    LESSONS.append(kw)


# ---------------------------------------------------------------- F1
_add(
    level=0,
    num="1",
    card="CPU, memory, storage and binary, explained as a very fast and very literal kitchen.",
    slug="f1-machine",
    id="py-f1-machine",
    title="What a Computer Actually Is",
    emoji="🧠",
    desc="CPU, memory, storage and binary explained with no jargon: what is really happening when you run a program.",
    lede="""Before you tell a machine what to do, it helps to know what the machine is.
    Good news: it is much dumber than you think, and that is exactly why it works.""",
    body=f"""
    <h2>The world's fastest, dumbest kitchen</h2>
    <p>
      Picture a kitchen with one cook. The cook is unbelievably fast: billions of
      actions per second. The cook is also completely literal and has no imagination
      whatsoever. If your recipe says "add salt" without saying how much, the cook
      does not guess. The cook stops and files a complaint.
    </p>
    <p>That kitchen is your computer. The parts:</p>
    {table(
        ["The part", "In the kitchen", "What it really does"],
        [
            ["<strong>CPU</strong>", "The cook", "Follows instructions, one at a time, absurdly fast"],
            ["<strong>RAM</strong> (memory)", "The counter top", "Holds what you are working on right now. Wiped when the power goes"],
            ["<strong>Disk</strong> (storage)", "The pantry", "Keeps things after you switch off. Slower to reach"],
            ["<strong>Input</strong>", "Someone shouting an order", "Keyboard, mouse, microphone, network"],
            ["<strong>Output</strong>", "The plate leaving the window", "Screen, speakers, files, network"],
        ],
    )}
    <p>
      That is it. That is the whole machine. Every app you have ever used, every game,
      every video call, is that loop: get input, move things around on the counter,
      produce output. Repeat several billion times a second until someone pulls the plug.
    </p>

    {voice("ENCYCLOPEDIA", "Easy: Success",
           "The pattern has a name: the stored-program computer, sketched out by John von "
           "Neumann and colleagues in 1945. The radical idea was that instructions and data "
           "could live in the same memory. Before that, you rewired the machine to change "
           "the program. Literally. With cables.")}

    <h2>Why everything is numbers</h2>
    <p>
      A computer stores everything using switches that are either off or on. One switch is
      a <strong>bit</strong>. Eight of them make a <strong>byte</strong>, which gives 256
      possible combinations, which is enough for one letter in the old days or a fragment
      of a character today.
    </p>
    <p>
      Counting with two symbols instead of ten is <strong>binary</strong>. You already know
      how this works, you just do it with ten fingers instead of two:
    </p>
    {table(
        ["Binary", "Meaning", "In decimal"],
        [
            ["<code>0001</code>", "one 1", "1"],
            ["<code>0010</code>", "one 2", "2"],
            ["<code>0011</code>", "one 2 and one 1", "3"],
            ["<code>1010</code>", "one 8 and one 2", "10"],
            ["<code>11111111</code>", "128+64+32+16+8+4+2+1", "255"],
        ],
    )}
    <p>
      Text is numbers too. There is a giant agreed-upon table called
      {link("Unicode", "https://home.unicode.org")} that says "the number 65 means capital A"
      and "the number 128013 means 🐍". Images are numbers for colours. Sound is numbers for
      air pressure. Your holiday photos, your bank balance and the entire internet are, at
      the bottom, extremely long numbers being pushed around by a very fast idiot.
    </p>

    {callout("tip", "🎮 Game metaphor",
             "<p>Think of a game's <em>tick</em>: 60 times a second the console reads your "
             "controller, updates every position, and draws a frame. That is input, process, "
             "output, sixty times a second. Your program will do the same thing, just slower "
             "and with fewer explosions.</p>")}

    <h2>What "running a program" means</h2>
    <p>
      A program is a file full of instructions. Running it means: copy the instructions from
      the pantry (disk) onto the counter (memory), then let the cook (CPU) work through
      them. When the cook reaches the end, the program stops and the counter is cleared.
    </p>
    <p>
      The CPU does not understand English, or Python, or anything you would recognise as
      language. It understands a few hundred numeric instructions with names like "add these
      two numbers" and "jump back four instructions". Everything else, every language you
      have ever heard of, exists to spare you from writing that by hand.
    </p>

    {voice("PERCEPTION", "Medium: Success",
           "Look closer at the phrase 'jump back four instructions'. That is a loop. That is "
           "the whole idea of a loop, at the bottom of the machine, and you will meet it "
           "again in Lesson 8 wearing a nicer coat.")}

    <h2>Fast, but not magic</h2>
    <p>
      A modern CPU runs at a few billion cycles per second. Some scale, so the numbers stop
      being abstract:
    </p>
    {table(
        ["Operation", "Roughly how long", "If one CPU cycle were one second"],
        [
            ["Add two numbers", "under a nanosecond", "1 second"],
            ["Read from memory (RAM)", "about 100 nanoseconds", "about 2 minutes"],
            ["Read from a fast SSD", "about 100 microseconds", "about 1 day"],
            ["Fetch a web page", "about 100 milliseconds", "about 3 years"],
        ],
    )}
    <p>
      This table explains most performance advice you will ever hear. Touching the network is
      millions of times slower than doing arithmetic, which is why programs that feel slow are
      almost never "doing too much maths" and almost always "waiting for something".
    </p>

    {exercise(1, "Name the parts",
              "<p>Without looking back up the page: which part of the computer forgets "
              "everything when you turn the power off, and which part remembers?</p>",
              "<p>RAM (memory) forgets. Disk (storage) remembers. That is why an app asks "
              "you to save: saving means copying from the counter to the pantry.</p>"
              "<p>This is also why 'have you tried turning it off and on again' works so "
              "often. It wipes the counter and starts clean.</p>")}

    {exercise(2, "Count like a computer",
              "<p>What is <code>0110</code> in ordinary decimal numbers? "
              "The columns, from right to left, are worth 1, 2, 4, 8.</p>",
              "<p><strong>6</strong>. There is a 4 and a 2 switched on: 4 + 2 = 6.</p>")}

    {callout("info", "📚 Want the deeper version?",
             "<p>The Rusty School's Level 0 covers the same ground from a systems angle, and "
             "goes further into how memory is laid out: "
             "<a href='../../learn/f1-computers.html'>How a Computer Thinks</a>. Two "
             "explanations of the same thing from different angles is one of the best "
             "learning tricks there is.</p>")}
""",
)

# ---------------------------------------------------------------- F2
_add(
    level=0,
    num="2",
    card="Algorithms, the three moves every program is made of, and why languages exist.",
    slug="f2-programming",
    id="py-f2-programming",
    title="What Programming Actually Is",
    emoji="📜",
    desc="Algorithms, instructions, and why programming languages exist. Plus the three things every program does.",
    lede="""Programming is writing instructions for something that cannot infer, assume,
    or use common sense. It is less like maths and more like writing very careful stage
    directions for an actor who takes everything literally.""",
    body=f"""
    <h2>The peanut butter sandwich problem</h2>
    <p>
      There is a classic classroom exercise. Children write instructions for making a peanut
      butter sandwich, and the teacher follows them exactly. "Put the peanut butter on the
      bread" gets the teacher pressing an unopened jar onto an unopened loaf. The room
      dissolves. A lesson is learned.
    </p>
    <p>
      That teacher is the computer. Programming is the skill of writing instructions so
      complete and so unambiguous that a determined literalist cannot get them wrong. It is
      not about being clever. It is about being <em>precise</em>, which is a different and
      much more learnable skill.
    </p>

    {voice("DRAMA", "Easy: Success",
           "Ah, but the machine is not merely literal, is it? It is hostile in its literalism. "
           "It will find the one interpretation you did not intend and commit to it entirely, "
           "the way a bad actor finds the one reading of a line that ruins the scene.")}

    <h2>An algorithm is just a plan</h2>
    <p>
      The word sounds like a magic spell. It means "a list of steps that finishes". You use
      them constantly:
    </p>
    <ul>
      <li>A recipe is an algorithm.</li>
      <li>Looking up "Threepwood" in a phone book by opening the middle and halving your way
      down is an algorithm. Computer scientists call it binary search and are very proud of it.</li>
      <li>Your morning routine is an algorithm, complete with a conditional
      ("if it is raining, take the coat").</li>
    </ul>
    <p>
      Programming is: work out the steps (the hard part, done in your head or on paper), then
      write them in a language the machine accepts (the easy part, which is what this course
      teaches).
    </p>

    {callout("tip", "🎮 You have already done this",
             "<p>If you have ever set up a crafting queue in a game, written a macro, built a "
             "redstone contraption, or configured a spreadsheet formula, you have programmed. "
             "You just did not have to fight anyone about semicolons.</p>")}

    <h2>The three moves</h2>
    <p>
      Nearly every program ever written is built from three moves, and Level 1 of this course
      is basically a tour of them:
    </p>
    {table(
        ["Move", "What it means", "In English"],
        [
            ["<strong>Sequence</strong>", "Do this, then this, then this", "\"Open the door, walk in, close the door\""],
            ["<strong>Selection</strong>", "Choose between paths", "\"If it is locked, use the key\""],
            ["<strong>Repetition</strong>", "Do it again", "\"Keep knocking until someone answers\""],
        ],
    )}
    <p>
      That is the entire toolkit. Add a way to store values (variables) and a way to bundle
      steps under a name (functions) and you can, in principle, write anything: a game, a
      browser, a bank, a chatbot. Everything else is convenience, speed and taste.
    </p>

    <h2>Why languages exist</h2>
    <p>
      The CPU wants numbers. Humans want words. A <strong>programming language</strong> is the
      negotiated settlement. Here is the same idea at three altitudes:
    </p>
    {table(
        ["Level", "Looks like", "Who writes this"],
        [
            ["Machine code", "<code>10110000 01100001</code>", "Nobody, on purpose, since about 1955"],
            ["Assembly", "<code>mov al, 0x61</code>", "Compiler authors, chip people, demoscene heroes"],
            ["Python", "<code>letter = \"a\"</code>", "You, in about ten minutes"],
        ],
    )}
    <p>
      Two ways exist to get from the top row to the bottom row:
    </p>
    <ul>
      <li><strong>Compiled</strong> languages (C, Rust, Go) translate your whole program into
      machine code ahead of time. You get a standalone file that runs blisteringly fast. You
      pay by waiting for the compile and by having to satisfy the compiler first.</li>
      <li><strong>Interpreted</strong> languages (Python, JavaScript, Ruby) keep a translator
      running alongside your program, working through it line by line. You get instant
      feedback and enormous flexibility. You pay in speed.</li>
    </ul>
    <p>
      Python is interpreted, which is why you will be running real code inside a web page
      thirty seconds from now, with nothing installed. It is also why our sister school's
      language, Rust, will run circles around it in a benchmark. Both facts are fine. They
      are the same trade seen from two sides.
    </p>

    {voice("LOGIC", "Medium: Success",
           "Note the honest framing: not 'Python is slow' but 'Python trades machine time for "
           "your time'. Your time costs more than the computer's, right up until the moment it "
           "does not, and knowing where that line sits is most of what senior engineers are paid for.")}

    <h2>What programmers actually do all day</h2>
    <p>
      Not typing. Typing is maybe fifteen minutes of it. The real job:
    </p>
    <ul>
      <li><strong>Reading.</strong> Understanding code you did not write, including your own
      from three months ago, who was a stranger.</li>
      <li><strong>Naming.</strong> Deciding what to call things so the next person understands.
      Famously one of the two hard problems in computer science.</li>
      <li><strong>Debugging.</strong> Finding out why the thing you were certain about is
      false. This is the actual craft, and Lesson 10 starts teaching it properly.</li>
      <li><strong>Deleting.</strong> The best code is the code you did not have to write.</li>
    </ul>

    {exercise(1, "Be the computer",
              "<p>Here are instructions for brushing your teeth. Follow them with maximum "
              "literal-mindedness and find at least three ways they go wrong:</p>"
              "<ol><li>Pick up the toothbrush.</li><li>Put toothpaste on it.</li>"
              "<li>Brush your teeth for two minutes.</li><li>Rinse.</li></ol>",
              "<p>A few of the many: the toothpaste tube is closed, and nothing said to open "
              "it. 'Put toothpaste on it' does not say how much, so you use the whole tube. "
              "'Brush your teeth' does not say to put the brush in your mouth. 'Rinse' does not "
              "say rinse <em>what</em>, so you rinse the cat.</p>"
              "<p>Every one of those is a bug you will genuinely write this year. The mistake "
              "is never stupidity. It is assuming shared context with something that has none.</p>")}

    {exercise(2, "Spot the three moves",
              "<p>Describe how a vending machine works in five or six steps. Then label each "
              "step as sequence, selection or repetition.</p>",
              "<p>One reasonable answer:</p>"
              "<ol><li>Wait for a coin. <em>(repetition: keep waiting)</em></li>"
              "<li>Add the coin's value to the total. <em>(sequence)</em></li>"
              "<li>If the total is less than the price, go back to step 1. <em>(selection, "
              "then repetition)</em></li>"
              "<li>Wait for a button press. <em>(repetition)</em></li>"
              "<li>If that slot is empty, refund and stop. Otherwise drop the item. <em>(selection)</em></li>"
              "<li>Return the change. <em>(sequence)</em></li></ol>"
              "<p>You have just designed a program. The rest of this course is notation.</p>")}
""",
)

# ---------------------------------------------------------------- F3
_add(
    level=0,
    num="3",
    card="A Christmas project named after a comedy troupe that ended up running the world.",
    slug="f3-python",
    id="py-f3-python",
    title="What Python Is, and Where It Came From",
    emoji="🐍",
    desc="Python's history, its name, versions, the Zen of Python, and what an interpreter really does.",
    lede="""It is named after a comedy troupe, it was a Christmas project, and it now runs a
    frightening share of the modern world. Meet your language.""",
    body=f"""
    <h2>A Christmas holiday project</h2>
    <p>
      In December 1989, a Dutch programmer named Guido van Rossum had a quiet holiday and a
      mild irritation. The languages available to him were either fast and hostile or friendly
      and useless. So he started building a language that read almost like English, punished
      you for writing messy layout, and let you get something working before your coffee went
      cold. He released it publicly in 1991.
    </p>
    <p>
      He named it after {link("Monty Python's Flying Circus", "https://en.wikipedia.org/wiki/Monty_Python%27s_Flying_Circus")},
      not the snake. This is why the official docs are full of spam, eggs and dead parrots,
      and why the traditional placeholder names in Python examples are
      <code>spam</code>, <code>eggs</code> and <code>ham</code> rather than the boring
      <code>foo</code> and <code>bar</code> the rest of the industry uses.
    </p>

    {voice("ENCYCLOPEDIA", "Trivial: Success",
           "Guido carried the informal title 'Benevolent Dictator For Life' for decades, "
           "stepped down in 2018 after a bruising argument about a new syntax feature, and "
           "the language is now governed by an elected Steering Council. A language outliving "
           "its founder's involvement is a sign of health, not decline.")}

    <h2>What actually happens when you run Python</h2>
    <p>
      You write a file, say <code>hello.py</code>. You run it. Behind the scenes:
    </p>
    <ol class="steps">
      <li><strong>Your text is parsed.</strong> The interpreter reads your file and checks the
      grammar. If you forgot a bracket, this is where it complains, before anything runs.</li>
      <li><strong>It is compiled to bytecode.</strong> Yes, compiled: Python turns your code
      into a compact set of instructions for a pretend machine. You will sometimes see these
      cached in a <code>__pycache__</code> folder. That folder is not garbage, and not a virus.</li>
      <li><strong>A virtual machine runs the bytecode.</strong> This is the part that is
      genuinely "interpreted": a loop inside CPython reads one bytecode instruction at a time
      and does it.</li>
    </ol>
    <p>
      "CPython" is the standard Python, written in C, the one you will install. There are
      others: {link("PyPy", "https://pypy.org")} (much faster for long-running number crunching),
      {link("MicroPython", "https://micropython.org")} (runs on a chip that costs less than a
      sandwich), and Pyodide, which is CPython compiled to WebAssembly. That last one is why
      the ▶ run buttons in this course work with no server involved. Your code never leaves
      your laptop.
    </p>

    {callout("tip", "🧪 Try it right now",
             "<p>Every code block in this school with a ▶ run button executes real Python 3.14 "
             "in your browser. Press it. Change the text. Press it again. Nothing you can type "
             "will break anything.</p>")}
    {code('print("Hello from a real Python interpreter, running inside a web page.")',
          expect="Hello from a real Python interpreter, running inside a web page.")}

    <h2>Python 2 versus Python 3, and why you can ignore it</h2>
    <p>
      For about a decade Python had a painful split. Python 3 arrived in 2008 with sensible
      but incompatible changes, and the world took twelve years to move. Python 2 was finally
      retired on 1 January 2020.
    </p>
    <p>
      Why you care: old tutorials and old Stack Overflow answers are still out there. The
      instant tell is <code>print</code>. If you see this:
    </p>
    {code('print "hello"   # Python 2. Ancient. Move on.', run=False, verify="skip")}
    <p>
      then the page is at least six years out of date and probably wrong in other ways too.
      Modern Python always uses <code>print("hello")</code> with brackets. This course teaches
      Python 3.13 and 3.14 conventions throughout.
    </p>

    <h2>The Zen of Python</h2>
    <p>
      Python ships with a hidden poem. Type <code>import this</code> into a Python prompt and
      it prints nineteen aphorisms by Tim Peters about how Python code should feel. The
      opening lines:
    </p>
    {out("""Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.""")}
    <p>
      This is not decoration. It explains real design decisions you are about to meet: why
      Python forces you to indent, why there is usually one obvious way to do a thing, and
      why the community reacts to clever one-liners the way a librarian reacts to shouting.
    </p>

    {voice("RHETORIC", "Medium: Success",
           "'Readability counts' is doing a lot of work in that list. Code is read far more "
           "often than it is written. Optimising for the reader is not politeness, it is "
           "self-interest with a delay built in.")}

    <h2>Where Python sits today</h2>
    <p>
      It is consistently at or near the top of every measure of language popularity: the
      {link("TIOBE index", "https://www.tiobe.com/tiobe-index/")}, the
      {link("Stack Overflow Developer Survey", "https://survey.stackoverflow.co")}, and
      GitHub's {link("Octoverse report", "https://octoverse.github.com")}, which in 2024
      recorded Python overtaking JavaScript as the most-used language on GitHub, driven
      largely by data science and machine learning work.
    </p>
    <p>
      More useful than the rankings: Python is the default language of scientific computing,
      the default language of machine learning, one of the two default languages of
      automation and DevOps, and a first-class option for web backends. Next lesson looks at
      exactly why, with receipts.
    </p>

    {exercise(1, "Read the poem",
              "<p>Run this block and read all nineteen lines. Pick the one you disagree with "
              "most, and keep it in mind. In six months, see whether you still disagree.</p>"
              + code("import this", expect="""The Zen of Python, by Tim Peters

Beautiful is better than ugly.
Explicit is better than implicit.
Simple is better than complex.
Complex is better than complicated.
Flat is better than nested.
Sparse is better than dense.
Readability counts.
Special cases aren't special enough to break the rules.
Although practicality beats purity.
Errors should never pass silently.
Unless explicitly silenced.
In the face of ambiguity, refuse the temptation to guess.
There should be one-- and preferably only one --obvious way to do it.
Although that way may not be obvious at first unless you're Dutch.
Now is better than never.
Although never is often better than *right* now.
If the implementation is hard to explain, it's a bad idea.
If the implementation is easy to explain, it may be a good idea.
Namespaces are one honking great idea -- let's do more of those!"""),
              "<p>There is no wrong answer. Most beginners bristle at 'explicit is better than "
              "implicit' because explicit code is longer. Most people come around after their "
              "first week maintaining someone else's clever implicit code.</p>"
              "<p>(If you noticed the poem is a little odd in places, well spotted. It is a "
              "joke as much as a manifesto, and 'unless you're Dutch' is aimed squarely at "
              "Guido.)</p>")}

    {exercise(2, "Date the tutorial",
              "<p>You find a tutorial online containing this line. Should you trust the rest "
              "of the page?</p>"
              + code('print "Total:", total', run=False, verify="skip"),
              "<p>No. That is Python 2 syntax, dead since January 2020. It will not even run "
              "on a modern Python: you will get a <code>SyntaxError</code>. The rest of the "
              "page is likely to be similarly stale.</p>"
              "<p>Habit worth forming now: check the date on anything you find, and prefer "
              "the official docs at docs.python.org, which are versioned and current.</p>")}
""",
)

# ---------------------------------------------------------------- F4
_add(
    level=0,
    num="4",
    card="What Python is genuinely great at, where it loses, and when to pick something else.",
    slug="f4-why-python",
    id="py-f4-why-python",
    title="Why Python? An Honest Accounting",
    emoji="⚖️",
    desc="What Python is genuinely great at, what it is bad at, who uses it in production, and when to pick something else.",
    lede="""Every language brochure claims the same six virtues. This lesson gives you the
    real ones, with sources, and then tells you where Python loses.""",
    body=f"""
    <h2>The case for Python</h2>

    <h3>1. It is the shortest distance between an idea and a working thing</h3>
    <p>
      Counting a file's words takes one line in Python and a small ceremony in most compiled
      languages. That difference compounds. When an experiment costs you five minutes instead
      of an hour, you run twenty times more experiments, and running more experiments is
      most of what learning and research actually are.
    </p>

    <h3>2. It reads like English, which matters more than it sounds</h3>
    {code('''crew = ["Guybrush", "Elaine", "Otis"]

if "Otis" in crew:
    print("Otis is aboard.")

for member in crew:
    print(f"{member} reports for duty.")''',
          expect="""Otis is aboard.
Guybrush reports for duty.
Elaine reports for duty.
Otis reports for duty.""")}
    <p>
      You could read that aloud to a non-programmer and they would broadly follow it. Very few
      languages can say that. It matters because, as the Zen says, code is read far more than
      it is written.
    </p>

    <h3>3. The batteries are genuinely included</h3>
    <p>
      Python ships with a standard library that handles dates, files, zip archives, JSON, CSV,
      SQLite databases, HTTP, email, threading, random numbers, maths, testing, logging and
      unit conversion, all without installing anything. Then there is
      {link("PyPI", "https://pypi.org")}, the public package index, which passed
      <strong>half a million</strong> published packages. Whatever you want to do, someone has
      probably done the boring 80% of it already.
    </p>

    <h3>4. It owns science and machine learning outright</h3>
    <p>
      This is not marketing, it is where the field actually happens.
      {link("NumPy", "https://numpy.org")} and {link("pandas", "https://pandas.pydata.org")}
      are the standard tools for numerical work.
      {link("PyTorch", "https://pytorch.org")} is what most AI research is written in.
      The {link("Event Horizon Telescope", "https://github.com/achael/eht-imaging")} team used
      Python to assemble the first image of a black hole, and
      {link("LIGO", "https://gwosc.org/tutorials/")} publishes its gravitational wave analysis
      as Python notebooks. When you learn Python you are learning the language the tools of
      modern science are written in.
    </p>

    <h3>5. It is the glue language</h3>
    <p>
      Python is unusually good at telling other programs what to do: shell commands, web APIs,
      spreadsheets, databases, browsers, your operating system. A huge share of real-world
      Python is fifty lines that make four other systems talk to each other. Unglamorous,
      enormously useful, and the fastest route to your first genuinely handy tool.
    </p>

    {voice("INTERFACING", "Medium: Success",
           "This is the part nobody puts on the brochure. Most working software is not a "
           "cathedral. It is a hundred small pipes connecting things that were never designed "
           "to meet. Python is the best pipe-fitting language ever made, and there is no shame "
           "in that at all.")}

    <h2>Who actually runs it</h2>
    {table(
        ["Who", "What they do with it", "Source"],
        [
            ["Instagram", "One of the largest Django deployments on earth, serving billions of requests",
             link("Instagram engineering", "https://instagram-engineering.com/tagged/python")],
            ["NASA / JPL", "Mission planning, data pipelines and analysis",
             link("JPL open source", "https://github.com/nasa-jpl")],
            ["Netflix", "Almost all of its operational tooling and data platform",
             link("Netflix tech blog", "https://netflixtechblog.com/python-at-netflix-bba45dae649e")],
            ["Spotify", "Data pipelines and backend services",
             link("Spotify engineering", "https://engineering.atspotify.com")],
            ["Dropbox", "Was built on Python; Guido himself worked there for years",
             link("Dropbox tech blog", "https://dropbox.tech/application")],
            ["CERN, LIGO, EHT", "The analysis behind actual physics results",
             link("gravitational wave tutorials", "https://gwosc.org/tutorials/")],
            ["Basically every ML team", "Model training, evaluation and serving",
             link("PyTorch", "https://pytorch.org")],
        ],
    )}

    <h2>The case against Python</h2>
    <p>
      A course that only sells you the upside is an advert. Here is where Python genuinely loses.
    </p>

    <h3>It is slow, and the reason is structural</h3>
    <p>
      Interpreted, dynamically typed code does far more work per operation than compiled code.
      A tight numeric loop in pure Python can be tens to hundreds of times slower than the same
      loop in C or Rust. In practice this rarely matters, because the heavy lifting is done
      inside libraries that are themselves written in C, Rust or Fortran. NumPy is fast because
      NumPy is not really Python. But if <em>your</em> hot loop is pure Python, you will feel it.
    </p>

    <h3>It lets you make mistakes that a compiler would catch</h3>
    <p>
      Python will happily run a program containing a typo in a branch you have not tested yet,
      then fail at 3am. Static languages catch that class of error before the program starts.
      Type hints and tools like {link("mypy", "https://mypy-lang.org")} claw a lot of this back
      (Lesson 38), but it is opt-in, and opt-in safety is weaker than enforced safety.
    </p>

    <h3>Shipping it to other people is awkward</h3>
    <p>
      A Rust program compiles to a single file you can email to someone. A Python program is
      code plus an interpreter plus a set of dependencies, and getting all three onto a
      stranger's machine has spawned an entire industry of workarounds. It is much better
      than it was, and Lesson 50 covers the modern answers, but it is still Python's softest spot.
    </p>

    <h3>Threads do not do what you expect</h3>
    <p>
      For most of its life CPython has had a Global Interpreter Lock, which means ordinary
      threads do not give you more CPU. There are good workarounds (processes, async, native
      libraries), Python 3.13 introduced an experimental build without the lock, and Lesson 39
      explains the whole situation honestly. But "just add threads" is not the answer here that
      it is elsewhere.
    </p>

    {voice("VOLITION", "Medium: Success",
           "None of that is a reason to stop. It is a reason to know your tool. A chef is not "
           "embarrassed that a bread knife cuts bread badly when used as a screwdriver.")}

    <h2>So when should you not pick Python?</h2>
    {table(
        ["If you need...", "Consider", "Why"],
        [
            ["A game engine, an operating system, a browser core", "Rust, C++",
             "You need predictable speed and control over memory"],
            ["A tiny single-file tool for strangers to download", "Rust, Go",
             "One compiled binary, no runtime to install"],
            ["Code running in a web browser", "JavaScript, TypeScript",
             "It is the browser's native language"],
            ["An iPhone or Android app", "Swift, Kotlin",
             "First-class platform support and tooling"],
            ["Squeezing the last 30% out of a hot loop", "Rust, C, or NumPy",
             "Or write that one function in Rust and call it from Python. People do this constantly"],
        ],
    )}
    {callout("info", "🦀 The sister school",
             "<p>That last row is not a joke. Tools like "
             "<a href='https://pyo3.rs' target='_blank' rel='noopener'>PyO3</a> let you write "
             "the slow 5% of a Python program in Rust and call it as if it were Python. "
             "<a href='https://github.com/astral-sh/ruff' target='_blank' rel='noopener'>ruff</a>, "
             "<a href='https://github.com/astral-sh/uv' target='_blank' rel='noopener'>uv</a> and "
             "<a href='https://pola.rs' target='_blank' rel='noopener'>Polars</a> are all Python "
             "tools written in Rust, and they are 10 to 100 times faster than what they replaced. "
             "If that sounds appealing, the <a href='../../learn/index.html'>Rusty School</a> is "
             "next door, and Lesson 51 here shows you the bridge.</p>")}

    <h2>The honest summary</h2>
    <p>
      Python is the best first language available, and remains a genuinely excellent tenth
      language. It optimises for the scarcest resource in any project, which is human attention.
      You will outgrow it in specific directions, and that is a good outcome: knowing exactly
      why you are reaching for another tool is what makes you an engineer rather than a fan.
    </p>

    {exercise(1, "Pick the tool",
              "<p>For each job, would you reach for Python? Answer before revealing.</p>"
              "<ol><li>Rename 4,000 holiday photos by the date they were taken.</li>"
              "<li>Write the firmware for a pacemaker.</li>"
              "<li>Analyse a 200MB spreadsheet of sales data and chart the trend.</li>"
              "<li>Build a competitive first-person shooter.</li>"
              "<li>Glue a weather API to a smart light so the bulb turns blue when rain is forecast.</li></ol>",
              "<ol><li><strong>Yes.</strong> Textbook Python. Twenty lines, ten minutes.</li>"
              "<li><strong>No.</strong> Safety-critical, real-time, memory-constrained. That is C, "
              "Ada or Rust territory with certification requirements Python cannot meet.</li>"
              "<li><strong>Yes.</strong> pandas plus matplotlib is exactly this job.</li>"
              "<li><strong>Mostly no.</strong> The engine wants C++ or Rust. Python is often used "
              "for the scripting layer inside such engines, though.</li>"
              "<li><strong>Yes.</strong> Two APIs and a bit of logic: peak glue language.</li></ol>")}
""",
)

# ---------------------------------------------------------------- F5
_add(
    level=0,
    num="5",
    card="The black window with the cursor: ten commands, and what a path really is.",
    slug="f5-terminal",
    id="py-f5-terminal",
    title="The Terminal, Files and Paths",
    emoji="⌨️",
    desc="A survival guide to the command line on macOS, Windows and Linux: the ten commands you need and what a path really is.",
    lede="""The black window with the blinking cursor is not a hacker thing. It is a text
    conversation with your computer, and it is about to become the room you live in.""",
    body=f"""
    <h2>Why bother, when you have a mouse</h2>
    <p>
      Clicking is great for one file. It is terrible for four thousand. The terminal is how
      you say "rename every photo in this folder" in one sentence instead of four thousand
      drags. It is also the only sane way to run Python programs, install packages, and use
      almost every professional development tool ever built.
    </p>
    <p>
      More importantly: it is a text interface, which means every instruction in every tutorial
      you will ever read is a line you can copy. Nobody can screenshot a mouse gesture.
    </p>

    {voice("HALF LIGHT", "Easy: Failure",
           "It looks like the interface from a film where someone says 'I'm in'. You are going "
           "to type something wrong and destroy the machine.",
           "You are not. You would have to go well out of your way. The commands in this lesson "
           "look at things and move you around; not one of them deletes anything.")}

    <h2>Opening it</h2>
    {table(
        ["System", "How", "What you get"],
        [
            ["macOS", "Cmd+Space, type 'Terminal', Enter", "zsh, a Unix shell"],
            ["Windows", "Start menu, type 'PowerShell', Enter", "PowerShell"],
            ["Linux", "Ctrl+Alt+T, usually", "bash or zsh"],
        ],
    )}
    <p>
      You will see a <strong>prompt</strong>: some text, then a cursor. It is telling you where
      you are and waiting. You type a command, press Enter, it does the thing, and gives the
      prompt back.
    </p>

    <h2>Where am I? The idea of a path</h2>
    <p>
      Your files live in a tree. A <strong>path</strong> is the route from somewhere to a
      specific file, written as folder names joined by slashes:
    </p>
    {out("""/Users/you/Documents/python/hello.py     macOS and Linux
C:\\Users\\you\\Documents\\python\\hello.py     Windows (backslashes)""")}
    <p>Two kinds of path, and the difference causes more beginner pain than any other topic:</p>
    <ul>
      <li>An <strong>absolute path</strong> starts at the very top (<code>/</code> or
      <code>C:\\</code>) and works everywhere. Like full postal address.</li>
      <li>A <strong>relative path</strong> starts from wherever you currently are.
      <code>hello.py</code> means "in this folder". Like saying "two doors down".</li>
    </ul>
    <p>Two special names you will use constantly:</p>
    {table(
        ["Written", "Means"],
        [["<code>.</code>", "the folder I am in right now"],
         ["<code>..</code>", "the folder one level up"],
         ["<code>~</code>", "my home folder (macOS/Linux, and PowerShell understands it too)"]],
    )}

    {callout("danger", "🪤 The number one beginner error",
             "<p><code>python hello.py</code> failing with "
             "<code>can't open file 'hello.py': No such file or directory</code> almost never "
             "means the file is missing. It means <em>you are not standing in the folder that "
             "contains it</em>. Run <code>ls</code> (or <code>dir</code> on Windows) and look. "
             "If the file is not in that list, you need to <code>cd</code> somewhere else first.</p>")}

    <h2>The ten commands that cover almost everything</h2>
    {table(
        ["macOS / Linux", "Windows PowerShell", "What it does"],
        [
            ["<code>pwd</code>", "<code>pwd</code>", "Print working directory: where am I?"],
            ["<code>ls</code>", "<code>ls</code> or <code>dir</code>", "List what is in this folder"],
            ["<code>ls -la</code>", "<code>ls -Force</code>", "List everything, including hidden files"],
            ["<code>cd folder</code>", "<code>cd folder</code>", "Go into a folder"],
            ["<code>cd ..</code>", "<code>cd ..</code>", "Go up one level"],
            ["<code>cd ~</code>", "<code>cd ~</code>", "Go home"],
            ["<code>mkdir name</code>", "<code>mkdir name</code>", "Make a folder"],
            ["<code>cat file</code>", "<code>cat file</code>", "Print a file to the screen"],
            ["<code>python3 file.py</code>", "<code>python file.py</code>", "Run a Python program"],
            ["<code>clear</code>", "<code>cls</code>", "Wipe the screen (nothing is deleted)"],
        ],
    )}

    <h2>A first session, annotated</h2>
    {term("""~ $ pwd
/Users/you

~ $ mkdir python-school
~ $ cd python-school
~/python-school $ pwd
/Users/you/python-school

~/python-school $ ls
(nothing here yet, which is correct)

~/python-school $ cd ..
~ $ """)}
    <p>
      That is the whole loop: look around, move, make something, look again. You now know
      enough terminal to finish this entire course.
    </p>

    <h2>Three tricks that will save you hours</h2>
    <ul>
      <li><strong>Tab completion.</strong> Type the first few letters of a folder or file and
      press Tab. The shell finishes it. This prevents typos and is the single biggest speedup
      available to you. Use it constantly.</li>
      <li><strong>Up arrow.</strong> Recalls your previous commands. You will re-run the same
      <code>python hello.py</code> three hundred times today. Do not retype it.</li>
      <li><strong>Ctrl+C.</strong> Stops whatever is running. If a program is stuck in a loop
      and will not stop, this is the escape hatch. Memorise it now, you will need it in
      Lesson 8.</li>
    </ul>

    {voice("SAVOIR FAIRE", "Medium: Success",
           "Watch an experienced developer's hands sometime. They barely type full paths. "
           "It is all Tab, up arrow, Ctrl+R, muscle memory built over years. None of it is "
           "talent. It is just the same six keys, ten thousand times.")}

    <h2>Dragging beats typing</h2>
    <p>
      Nobody types long paths. On macOS and Linux, type <code>cd </code> (with the space) and
      then <strong>drag the folder from your file manager onto the terminal window</strong>.
      The path appears. Press Enter. On Windows, hold Shift, right-click a folder, and choose
      "Copy as path", then paste.
    </p>

    {exercise(1, "Find your feet",
              "<p>Open a terminal and run these, in order. Read each result before typing the "
              "next one.</p>"
              + term("""pwd
ls
cd ~
mkdir python-school
cd python-school
pwd"""),
              "<p>You should end with a path ending in <code>/python-school</code> (or "
              "<code>\\python-school</code> on Windows). That folder is where everything in "
              "this course will live.</p>"
              "<p>If <code>mkdir</code> said the folder already exists, no harm done: you have "
              "run it twice, which is exactly as damaging as it sounds.</p>")}

    {exercise(2, "Read a path",
              "<p>You are in <code>/Users/you/python-school</code>. Where do these point?</p>"
              "<ol><li><code>notes.txt</code></li><li><code>../Downloads/data.csv</code></li>"
              "<li><code>/etc/hosts</code></li></ol>",
              "<ol><li><code>/Users/you/python-school/notes.txt</code>, in the folder you are "
              "standing in.</li>"
              "<li><code>/Users/you/Downloads/data.csv</code>: up one level, then down into "
              "Downloads.</li>"
              "<li><code>/etc/hosts</code> exactly, because it starts with a slash. Absolute "
              "paths ignore where you are standing.</li></ol>")}
""",
)

# ---------------------------------------------------------------- F6
_add(
    level=0,
    num="6",
    card="Install Python and an editor, then run your first real program from a real file.",
    slug="f6-lab",
    id="py-f6-lab",
    title="Setting Up Your Lab",
    emoji="🔧",
    desc="Install Python and an editor, run your first script from the terminal, and understand what you just installed.",
    lede="""Ten minutes of setup buys you the real thing: Python on your own machine, an
    editor that helps you, and a folder that is yours.""",
    body=f"""
    <h2>You can skip this. For now.</h2>
    <p>
      Every example in Levels 1 and 2 runs in your browser with the ▶ button, and the
      <a href="../playground.html">Playground</a> is a full editor with nothing to install. If
      you want to start learning in the next thirty seconds, go, and come back here when a
      lesson needs real files.
    </p>
    <p>
      But do come back. Programming on your own machine, with your own files, is the moment
      this stops being a course and starts being a craft.
    </p>

    <h2>Step 1: get Python</h2>
    <p>
      The full walkthrough for each operating system, with screenshots' worth of detail, lives
      on the <a href="../setup.html">Setup Lab</a> page. The short version:
    </p>
    {table(
        ["System", "Do this", "Then check"],
        [
            ["Windows", "Install from " + link("python.org/downloads", "https://www.python.org/downloads/") +
             " and <strong>tick 'Add python.exe to PATH'</strong> on the first screen",
             "<code>python --version</code>"],
            ["macOS", "Install from " + link("python.org/downloads", "https://www.python.org/downloads/") +
             " (the version Apple ships is old and not for your projects)",
             "<code>python3 --version</code>"],
            ["Linux", "It is almost certainly already there", "<code>python3 --version</code>"],
        ],
    )}
    <p>You are looking for something like this:</p>
    {term("""$ python3 --version
Python 3.13.5""")}
    <p>
      Anything 3.11 or newer is fine for this course. If you get "command not found", the
      Setup Lab has a section for exactly that, and it is nearly always the PATH checkbox on
      Windows.
    </p>

    {callout("warn", "⚠️ python versus python3",
             "<p>On macOS and Linux, type <code>python3</code>. Plain <code>python</code> may "
             "not exist, or may point at something ancient. On Windows, plain "
             "<code>python</code> is correct. This course writes <code>python3</code> and you "
             "should mentally drop the 3 if you are on Windows.</p>")}

    <h2>Step 2: get an editor</h2>
    <p>
      You can write Python in Notepad. You should not. A real editor gives you syntax
      colouring, tells you about mistakes as you type, and lets you run code without leaving
      the window.
    </p>
    <ul>
      <li>{link("VS Code", "https://code.visualstudio.com")} plus the official Python
      extension. The default choice, free, works everywhere, and every tutorial assumes it.</li>
      <li>{link("PyCharm Community", "https://www.jetbrains.com/pycharm/")}: heavier, free,
      more opinionated, excellent refactoring.</li>
      <li>{link("Zed", "https://zed.dev")}: very fast, newer, and (fun fact for the sister
      school) written in Rust.</li>
    </ul>
    <p>Take VS Code if you have no opinion. You can change later; nobody will mind.</p>

    <h2>Step 3: your first real program</h2>
    <ol class="steps">
      <li><strong>Make a folder.</strong> In your terminal:
        {term("cd ~\nmkdir python-school\ncd python-school")}</li>
      <li><strong>Open it in your editor.</strong> In VS Code: File, Open Folder, pick
        <code>python-school</code>. Working with a <em>folder</em> open rather than a lone
        file is the habit that makes everything else work later.</li>
      <li><strong>Make a file</strong> called <code>hello.py</code> and type this into it.
        Type it, do not paste it. Your fingers learn things your eyes do not.
        {code('''name = "Guybrush Threepwood"
print("Hello, world!")
print(f"My name is {name} and I am a mighty programmer.")''',
              expect="""Hello, world!
My name is Guybrush Threepwood and I am a mighty programmer.""")}</li>
      <li><strong>Save it.</strong> Ctrl+S, or Cmd+S on a Mac. An unsaved file is why your
        change "did nothing".</li>
      <li><strong>Run it</strong> from the terminal, standing in that folder:
        {term("$ python3 hello.py\nHello, world!\nMy name is Guybrush Threepwood and I am a mighty programmer.")}</li>
    </ol>

    {voice("VOLITION", "Formidable: Success",
           "That was it. That was the wall. Almost everyone who quits programming quits "
           "somewhere in the last five minutes: the install, the PATH, the folder, the "
           "'command not found'. You are past it. Everything after this is just learning "
           "what to type.")}

    <h2>What you actually installed</h2>
    <p>Three things arrived on your machine, and knowing which is which will save you later:</p>
    {table(
        ["Thing", "What it is", "You use it by"],
        [
            ["<code>python3</code>", "The interpreter: the program that runs your programs",
             "<code>python3 myfile.py</code>"],
            ["<code>pip</code>", "The package installer: fetches other people's code from PyPI",
             "<code>pip install requests</code> (Lesson 26)"],
            ["The REPL", "An interactive prompt for trying things one line at a time",
             "typing <code>python3</code> with no filename"]
        ],
    )}
    <p>Try the third one now. Type <code>python3</code> on its own:</p>
    {repl(""">>> 2 + 2
4
>>> "Guybrush" * 3
'GuybrushGuybrushGuybrush'
>>> len("How appropriate. You fight like a cow.")
38
>>> exit()""")}
    <p>
      That is the REPL: Read, Evaluate, Print, Loop. It is a calculator that speaks Python and
      it is the single best tool for answering "wait, what does this do?". Professionals keep
      one open all day. <code>exit()</code> leaves.
    </p>

    {callout("tip", "📁 One folder per project, always",
             "<p>Do not pile everything into Documents. Make a folder per project, keep its "
             "code in it, and open that folder in your editor. When Lesson 26 introduces "
             "virtual environments, this habit is what makes them painless instead of "
             "mysterious.</p>")}

    <h2>If something went wrong</h2>
    {table(
        ["Message", "What it means", "Fix"],
        [
            ["<code>command not found: python3</code>", "The shell cannot find Python",
             "Reinstall, ticking 'Add to PATH'. Close and reopen the terminal afterwards"],
            ["<code>No such file or directory: 'hello.py'</code>", "You are in the wrong folder",
             "<code>ls</code> to look, <code>cd</code> to move. See Base Camp 5"],
            ["<code>SyntaxError</code>", "A typo in your code",
             "Read the line number it gives you, then the line above it. Lesson 10 makes this easy"],
            ["<code>IndentationError</code>", "Stray spaces at the start of a line",
             "Line up your code at the left margin unless it is inside a block"],
        ],
    )}
    <p>
      The full troubleshooting list, per operating system, is on the
      <a href="../setup.html">Setup Lab</a> page. Nothing you can hit here is unusual, and
      nothing is your fault.
    </p>

    {exercise(1, "Make it yours",
              "<p>Change <code>hello.py</code> so it prints your own name, and add a third "
              "line that prints how many years you have wanted to learn this. Run it again.</p>",
              code('''name = "your name here"
years = 4
print("Hello, world!")
print(f"My name is {name}.")
print(f"I have wanted to do this for {years} years, which ends today.")''',
                   expect="""Hello, world!
My name is your name here.
I have wanted to do this for 4 years, which ends today.""")
              + "<p>If it ran, you have a working lab. Level 1 starts now.</p>")}

    {exercise(2, "Live in the REPL for two minutes",
              "<p>Open <code>python3</code> with no filename and work out, by experiment, what "
              "each of these does. Guess first, then run it.</p>"
              + code("""17 // 5
17 % 5
2 ** 10
"ho" * 3
len("Monkey Island")""", run=False, verify="compile"),
              "<p><code>17 // 5</code> is <strong>3</strong> (division, throwing away the "
              "remainder). <code>17 % 5</code> is <strong>2</strong> (just the remainder). "
              "<code>2 ** 10</code> is <strong>1024</strong> (2 to the power of 10). "
              "<code>\"ho\" * 3</code> is <strong>'hohoho'</strong> (yes, multiplying text "
              "works). <code>len(\"Monkey Island\")</code> is <strong>13</strong>, counting "
              "the space.</p>"
              "<p>You just learned five things by asking the machine instead of asking a "
              "person. That is the most valuable habit in this entire course.</p>")}
""",
)
