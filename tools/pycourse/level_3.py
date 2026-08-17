"""Level 3: Real Programs.

Files, errors, data formats, environments, command lines, debugging and
testing. This is the level where the thing you write stops being a
script that works on your machine and starts being software.
"""

from __future__ import annotations

from .kit import callout, code, exercise, link, out, repl, table, tb, term, voice

LESSONS = []


def _add(**kw):
    LESSONS.append(kw)


# ---------------------------------------------------------------- 21
_add(
    level=3,
    num="21",
    slug="21-files",
    id="py-21-files",
    card="Reading and writing real files, the with statement, and pathlib instead of string surgery.",
    title="Files: Making Things Last",
    emoji="💾",
    desc="Reading and writing text files, the with statement, encodings, and pathlib for handling paths properly.",
    lede="""Everything your programs have done so far vanished the moment they ended. Files are
    how a program remembers something tomorrow.""",
    body=f"""
    <h2>Writing a file</h2>
    {code('''with open("crew.txt", "w") as f:
    f.write("Guybrush\\n")
    f.write("Elaine\\n")
    f.write("Otis\\n")

print("Written.")''',
          expect="Written.")}
    <p>Three things to notice:</p>
    <ul>
      <li><code>"w"</code> means write, and it <strong>destroys whatever was there</strong>
      without asking. Use <code>"a"</code> to append instead.</li>
      <li><code>\\n</code> is the newline. <code>f.write</code> does not add one for you, unlike
      <code>print</code>.</li>
      <li><code>with</code> is doing something important, which is the next section.</li>
    </ul>
    {table(
        ["Mode", "Means", "If the file exists", "If it does not"],
        [['<code>"r"</code>', "read (the default)", "reads it", "FileNotFoundError"],
         ['<code>"w"</code>', "write", "<strong>empties it first</strong>", "creates it"],
         ['<code>"a"</code>', "append", "adds at the end", "creates it"],
         ['<code>"x"</code>', "exclusive create", "FileExistsError", "creates it"],
         ['<code>"rb"</code> / <code>"wb"</code>', "binary", "for images, zips, anything not text", ""]],
    )}

    <h2>Why with, and not just open</h2>
    {code('''# The way you should never write it
f = open("notes.txt", "w")
f.write("something")
f.close()          # if anything above raises, this never runs

# The way everyone writes it
with open("notes.txt", "w") as f:
    f.write("something")
# closed automatically, even if an error was raised inside

print("done")''',
          expect="done")}
    <p>
      An open file holds an operating system resource, and on many systems the data you wrote
      is not actually on disk until it is closed. <code>with</code> guarantees the close
      happens no matter what, including when an exception fires halfway through. It is called
      a <strong>context manager</strong>, you meet the machinery in Lesson 36, and until then
      the rule is simply: always use <code>with</code> for files.
    </p>

    <h2>Reading it back, three ways</h2>
    {code('''with open("crew.txt", "w") as f:
    f.write("Guybrush\\nElaine\\nOtis\\n")

# 1. the whole thing as one string
with open("crew.txt") as f:
    print(repr(f.read()))

# 2. a list of lines
with open("crew.txt") as f:
    print(f.readlines())

# 3. one line at a time, which is the one you want
with open("crew.txt") as f:
    for line in f:
        print(f"  {line.strip()}")''',
          expect="""'Guybrush\\nElaine\\nOtis\\n'
['Guybrush\\n', 'Elaine\\n', 'Otis\\n']
  Guybrush
  Elaine
  Otis""")}

    {voice("INTERFACING", "Medium: Success",
           "Option three never holds more than one line in memory. Options one and two load "
           "the entire file. For a shopping list that is irrelevant. For an eight gigabyte log "
           "file it is the difference between a program that works and a machine that starts "
           "swapping and has to be rebooted.",
           "Loop over the file object. It is shorter to type as well.")}

    <p>
      Note <code>.strip()</code> on every line: the newline character comes along with the
      text, and forgetting it produces bugs where <code>"Otis\\n" != "Otis"</code> and nobody
      can see why.
    </p>

    <h2>Encodings: always say utf-8</h2>
    {code('''with open("names.txt", "w", encoding="utf-8") as f:
    f.write("Guybrush\\nElaine\\nMonkey 🐒\\nZoë\\n")

with open("names.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())''',
          expect="""Guybrush
Elaine
Monkey 🐒
Zoë""")}
    {callout("danger", "🌍 Always pass encoding='utf-8'",
             "<p>Without it, Python uses your operating system's default, which is UTF-8 on "
             "Mac and Linux and, historically, something else on Windows. That is why files "
             "written on one machine sometimes arrive as <code>Zoë</code> on another. Passing "
             "<code>encoding=\"utf-8\"</code> every single time removes an entire genre of bug, "
             "and Python 3.15 is making it the default precisely because of how much pain it "
             "has caused.</p>")}

    <h2>pathlib: stop gluing strings together</h2>
    {code('''from pathlib import Path

# the old way, which breaks on Windows
old = "data" + "/" + "crew.txt"

# the way that works everywhere
p = Path("data") / "crew.txt"

print(old)
print(p)
print(p.name, p.stem, p.suffix)
print(p.parent)''',
          expect="""data/crew.txt
data/crew.txt
crew.txt crew .txt
data""")}
    <p>
      The <code>/</code> operator on a <code>Path</code> joins path parts with the right
      separator for the machine it runs on. <code>pathlib</code> also folds most of the file
      operations you need into one object:
    </p>
    {code('''from pathlib import Path

notes = Path("notes.txt")

notes.write_text("Remember the rubber chicken.\\n", encoding="utf-8")
print(notes.read_text(encoding="utf-8").strip())

print(notes.exists())
print(notes.stat().st_size, "bytes")

notes.unlink()               # delete
print(notes.exists())''',
          expect="""Remember the rubber chicken.
True
29 bytes
False""")}

    <h2>Checking before you leap</h2>
    {code('''from pathlib import Path

wanted = Path("does-not-exist.txt")

if wanted.exists():
    print(wanted.read_text())
else:
    print("No such file, using defaults instead.")

# The more Pythonic version: try it and handle failure
try:
    print(wanted.read_text())
except FileNotFoundError:
    print("Still not there.")''',
          expect="""No such file, using defaults instead.
Still not there.""")}
    <p>
      Both are fine. The second is generally preferred in Python, and there is even a slogan
      for it: "easier to ask forgiveness than permission". The reason is not style, it is that
      between your <code>exists()</code> check and your <code>read</code>, another program
      could delete the file. Handling the error covers both cases. Lesson 22 is entirely about
      this.
    </p>

    <h2>Walking a folder</h2>
    {code('''from pathlib import Path

# make a small tree to explore
Path("ship/cargo").mkdir(parents=True, exist_ok=True)
Path("ship/log.txt").write_text("day one\\n", encoding="utf-8")
Path("ship/cargo/grog.txt").write_text("47 barrels\\n", encoding="utf-8")
Path("ship/cargo/map.txt").write_text("x marks it\\n", encoding="utf-8")

print("Top level only:")
for item in sorted(Path("ship").iterdir()):
    kind = "dir " if item.is_dir() else "file"
    print(f"  {kind} {item}")

print("Every .txt, all the way down:")
for item in sorted(Path("ship").rglob("*.txt")):
    print(f"  {item} ({item.stat().st_size} bytes)")''',
          expect="""Top level only:
  dir  ship/cargo
  file ship/log.txt
Every .txt, all the way down:
  ship/cargo/grog.txt (11 bytes)
  ship/cargo/map.txt (11 bytes)
  ship/log.txt (8 bytes)""")}
    <p>
      <code>glob("*.txt")</code> looks in one folder, <code>rglob</code> recurses into every
      subfolder. Those two lines replace a startling amount of the shell scripting people
      write, and this is the foundation of the file-organiser project in the workshop.
    </p>

    {callout("warn", "🧹 A note about these examples",
             "<p>These blocks create real files when you run them. In the browser they land in "
             "a sandbox that vanishes when you reload, so nothing on your computer is touched. "
             "On your own machine they appear in whichever folder you ran Python from, which "
             "is a good reason to keep a scratch folder for experiments.</p>")}

    <h2>A real one: a note-taking script</h2>
    {code('''from pathlib import Path
from datetime import datetime

NOTES = Path("captains_log.txt")


def add_note(text):
    """Append a timestamped line to the log."""
    stamp = datetime(1990, 10, 15, 9, 30).strftime("%Y-%m-%d %H:%M")
    with open(NOTES, "a", encoding="utf-8") as f:
        f.write(f"[{stamp}] {text}\\n")


def show_notes():
    """Print the log, or say so if it is empty."""
    if not NOTES.exists():
        print("No log yet.")
        return
    for i, line in enumerate(NOTES.read_text(encoding="utf-8").splitlines(), start=1):
        print(f"{i}. {line}")


add_note("Became a mighty pirate.")
add_note("Lost the ship. Again.")
show_notes()''',
          expect="""1. [1990-10-15 09:30] Became a mighty pirate.
2. [1990-10-15 09:30] Lost the ship. Again.""")}

    {exercise(1, "Word count on a file",
              "<p>Write a file with several lines, then report the number of lines, words and "
              "characters, in the style of the Unix <code>wc</code> command.</p>",
              code('''from pathlib import Path

text = """It is a rubber chicken.
It has a pulley in the middle.
Do not ask why.
"""
Path("chicken.txt").write_text(text, encoding="utf-8")

content = Path("chicken.txt").read_text(encoding="utf-8")

lines = content.splitlines()
words = content.split()

print(f"{len(lines):4} lines")
print(f"{len(words):4} words")
print(f"{len(content):4} characters")''',
                   expect="""   3 lines
  16 words
  71 characters"""))}

    {exercise(2, "Filter a file into another file",
              "<p>Read a log file and write a second file containing only the ERROR lines, "
              "then report how many were found.</p>",
              code('''from pathlib import Path

Path("server.log").write_text("""INFO  started
ERROR disk full
INFO  retrying
ERROR still full
INFO  gave up
""", encoding="utf-8")

errors = []
with open("server.log", encoding="utf-8") as source:
    for line in source:
        if line.startswith("ERROR"):
            errors.append(line)

with open("errors.log", "w", encoding="utf-8") as target:
    target.writelines(errors)

print(f"{len(errors)} errors extracted")
print(Path("errors.log").read_text(encoding="utf-8").strip())''',
                   expect="""2 errors extracted
ERROR disk full
ERROR still full"""))}

    {exercise(3, "Safe overwrite",
              "<p>Write a function that saves text to a file but refuses to destroy an "
              "existing one unless told it may. Prove both branches.</p>",
              code('''from pathlib import Path


def save(path, text, overwrite=False):
    """Write text to path. Refuses to clobber unless overwrite is True."""
    target = Path(path)
    if target.exists() and not overwrite:
        return f"refused: {target} already exists"
    target.write_text(text, encoding="utf-8")
    return f"wrote {len(text)} characters to {target}"


print(save("treasure.txt", "x marks the spot"))
print(save("treasure.txt", "no it does not"))
print(save("treasure.txt", "fine, it does not", overwrite=True))
print(Path("treasure.txt").read_text(encoding="utf-8"))''',
                   expect="""wrote 16 characters to treasure.txt
refused: treasure.txt already exists
wrote 17 characters to treasure.txt
fine, it does not""")
              + "<p>Defaulting to refuse is the right instinct for anything destructive. "
              "Python's <code>\"x\"</code> mode does the same job at the operating system "
              "level, which is even safer because there is no gap between the check and the "
              "write.</p>")}
""",
)

# ---------------------------------------------------------------- 22
_add(
    level=3,
    num="22",
    slug="22-exceptions",
    id="py-22-exceptions",
    card="try, except, finally, raising your own, and why bare except is a crime.",
    title="Exceptions: Handling Failure",
    emoji="🧯",
    desc="try/except/else/finally, catching specific exceptions, raising your own, and custom exception classes.",
    lede="""Things go wrong: files vanish, networks drop, users type 'banana' into an age box.
    Exceptions are how Python lets you plan for that without every line becoming a check.""",
    body=f"""
    <h2>try and except</h2>
    {code('''raw = "banana"

try:
    number = int(raw)
    print(f"Got {number}")
except ValueError:
    print(f"'{raw}' is not a number.")

print("The program carries on.")''',
          expect="""'banana' is not a number.
The program carries on.""")}
    <p>
      Python attempts the <code>try</code> block. If an exception of the named type appears,
      it jumps straight to the matching <code>except</code> and carries on afterwards. Without
      that handler, the program would stop dead.
    </p>

    <h2>Catch what you expect, not everything</h2>
    {code('''# Never do this
try:
    result = 10 / 0
except:                     # catches literally everything
    print("something went wrong")

# Do this
try:
    result = 10 / 0
except ZeroDivisionError:
    print("cannot divide by zero")''',
          expect="""something went wrong
cannot divide by zero""")}

    {voice("PARANOIA", "Formidable: Success",
           "A bare except swallows everything. Your typo in a variable name: swallowed. The "
           "user pressing Ctrl+C to quit: swallowed. A genuine out-of-memory condition: "
           "swallowed, and then the program keeps going in a state nobody designed for.",
           "You have not handled the error. You have hidden it, and it will surface somewhere "
           "far away with no clue where it came from.")}

    <p>Catch several, or several at once:</p>
    {code('''def to_number(text):
    try:
        return int(text)
    except ValueError:
        return f"'{text}' has no digits I can use"
    except TypeError:
        return "I need text, not that"


print(to_number("42"))
print(to_number("banana"))
print(to_number(None))


def read_config(value):
    try:
        return 100 / int(value)
    except (ValueError, ZeroDivisionError) as err:
        return f"{type(err).__name__}: {err}"


print(read_config("4"))
print(read_config("0"))
print(read_config("x"))''',
          expect="""42
'banana' has no digits I can use
I need text, not that
25.0
ZeroDivisionError: division by zero
ValueError: invalid literal for int() with base 10: 'x'""")}
    <p>
      <code>as err</code> gives you the exception object itself, which carries the message.
      Printing <code>type(err).__name__</code> and <code>err</code> is how you log something
      useful rather than "an error occurred".
    </p>

    <h2>else and finally</h2>
    {code('''def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("  cannot divide by zero")
        return None
    else:
        print("  no exception, so this ran")
        return result
    finally:
        print("  finally always runs")


print(divide(10, 2))
print(divide(10, 0))''',
          expect="""  no exception, so this ran
  finally always runs
5.0
  cannot divide by zero
  finally always runs
None""")}
    {table(
        ["Block", "Runs when"],
        [["<code>try</code>", "Always. The risky part"],
         ["<code>except</code>", "Only if a matching exception was raised"],
         ["<code>else</code>", "Only if <strong>no</strong> exception was raised"],
         ["<code>finally</code>", "Always, exception or not, even after a return"]],
    )}
    <p>
      <code>finally</code> is for cleanup that must happen regardless: closing a connection,
      releasing a lock, deleting a temporary file. Note in the output above that it ran even
      though the function had already decided to return.
    </p>

    <h2>Keep the try block small</h2>
    {code('''values = ["12", "banana", "7"]

# Too wide: the ValueError might come from anywhere in here
try:
    total = 0
    for v in values:
        total += int(v)
    average = total / len(values)
    print(average)
except ValueError:
    print("something in there was not a number, but which?")

# Better: the try wraps exactly the risky line
total = 0
skipped = []
for v in values:
    try:
        total += int(v)
    except ValueError:
        skipped.append(v)

print(f"total {total}, skipped {skipped}")''',
          expect="""something in there was not a number, but which?
total 19, skipped ['banana']""")}

    <h2>Raising your own</h2>
    {code('''def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"age must be a whole number, got {type(age).__name__}")
    if age < 0:
        raise ValueError(f"age cannot be negative, got {age}")
    return f"age set to {age}"


print(set_age(30))

for bad in [-5, "thirty"]:
    try:
        set_age(bad)
    except (TypeError, ValueError) as err:
        print(f"{type(err).__name__}: {err}")''',
          expect="""age set to 30
ValueError: age cannot be negative, got -5
TypeError: age must be a whole number, got str""")}
    <p>
      Raising early with a clear message is a kindness. The alternative is that the bad value
      travels three functions deep and explodes somewhere that gives no hint about where it
      came from. This is called failing fast, and it is one of the highest-value habits in
      software.
    </p>

    <h2>Your own exception types</h2>
    {code('''class InsufficientGrogError(Exception):
    """Raised when a pirate cannot afford the round."""

    def __init__(self, needed, available):
        self.needed = needed
        self.available = available
        super().__init__(f"need {needed} mugs, only {available} left")


def serve_round(crew_size, barrels):
    if crew_size > barrels:
        raise InsufficientGrogError(crew_size, barrels)
    return f"Served {crew_size} mugs."


print(serve_round(3, 10))

try:
    serve_round(12, 4)
except InsufficientGrogError as err:
    print(f"Caught: {err}")
    print(f"Short by {err.needed - err.available}")''',
          expect="""Served 3 mugs.
Caught: need 12 mugs, only 4 left
Short by 8""")}
    <p>
      A custom exception is a class that inherits from <code>Exception</code> (classes are
      Lesson 31; you can copy this shape until then). It lets callers catch <em>your</em>
      specific problem without catching everything, and it can carry structured data about
      what went wrong, which a plain string cannot.
    </p>

    <h2>Re-raising and chaining</h2>
    {code('''def load_settings(raw):
    try:
        return int(raw)
    except ValueError as err:
        raise ValueError(f"settings file is corrupt: {raw!r}") from err


try:
    load_settings("not-a-number")
except ValueError as err:
    print(err)
    print("caused by:", type(err.__cause__).__name__)''',
          expect="""settings file is corrupt: 'not-a-number'
caused by: ValueError""")}
    <p>
      <code>raise ... from err</code> adds context without losing the original. In a real
      traceback you see both, joined by "The above exception was the direct cause of the
      following exception". It turns a mysterious low-level error into a story.
    </p>

    <h2>When not to use exceptions</h2>
    {code('''crew = {"Guybrush": 8}

# Clumsy
try:
    insults = crew["Elaine"]
except KeyError:
    insults = 0

# Just say what you mean
insults = crew.get("Elaine", 0)
print(insults)''',
          expect="0")}
    <p>
      Exceptions are for the exceptional. If a situation is normal and expected, handle it
      with ordinary logic: <code>.get()</code>, an <code>if</code>, a default. A
      <code>try</code> around every line is as unreadable as no error handling at all.
    </p>

    {exercise(1, "Bulletproof number input",
              "<p>Write <code>ask_number</code> that keeps asking until it gets a valid whole "
              "number between a low and high bound, explaining each rejection.</p>",
              code('''def ask_number(prompt, low, high):
    """Ask until the human gives a whole number within range."""
    while True:
        raw = input(f"{prompt} ({low}-{high}): ")
        try:
            value = int(raw)
        except ValueError:
            print(f"  '{raw}' is not a whole number. Digits only, please.")
            continue
        if not low <= value <= high:
            print(f"  {value} is outside {low} to {high}.")
            continue
        return value


age = ask_number("Your age", 1, 120)
print(f"Thank you, {age}.")''',
                   stdin="banana\n500\n-3\n42",
                   expect="""Your age (1-120): banana
  'banana' is not a whole number. Digits only, please.
Your age (1-120): 500
  500 is outside 1 to 120.
Your age (1-120): -3
  -3 is outside 1 to 120.
Your age (1-120): 42
Thank you, 42.""")
              + "<p>This tiny function is genuinely production-grade: it cannot be crashed by "
              "any input, and it explains every rejection. Steal it.</p>")}

    {exercise(2, "What is wrong with this?",
              "<p>Four separate sins. Name them.</p>"
              + code('''def load(path):
    try:
        f = open(path)
        data = f.read()
        number = int(data)
        return 100 / number
    except:
        pass''', run=False, verify="compile"),
              "<ol><li><strong>Bare except.</strong> It catches typos, Ctrl+C and everything "
              "else.</li>"
              "<li><strong><code>pass</code> as the handler.</strong> The failure is now "
              "completely invisible; the function silently returns None and the caller has no "
              "idea why.</li>"
              "<li><strong>No <code>with</code>.</strong> If <code>int()</code> raises, the "
              "file is never closed.</li>"
              "<li><strong>The try is far too wide.</strong> Three different failures "
              "(missing file, non-numeric contents, division by zero) are treated as one "
              "nameless event.</li></ol>"
              + code('''def load(path):
    """Return 100 divided by the number in path, or None with a reason."""
    try:
        with open(path, encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        print(f"no such file: {path}")
        return None

    try:
        number = int(data.strip())
    except ValueError:
        print(f"{path} does not contain a whole number")
        return None

    if number == 0:
        print(f"{path} contains zero, cannot divide by it")
        return None

    return 100 / number


print(load("nope.txt"))''', expect="""no such file: nope.txt
None"""))}

    {exercise(3, "A custom exception with data",
              "<p>Write a <code>Vault</code> function that raises a custom "
              "<code>WrongCombinationError</code> carrying how many attempts remain, and a "
              "caller that reports it.</p>",
              code('''class WrongCombinationError(Exception):
    """Raised when the vault combination is wrong."""

    def __init__(self, attempts_left):
        self.attempts_left = attempts_left
        super().__init__(f"wrong combination, {attempts_left} attempts left")


def try_combination(guess, correct="1-2-3", attempts_used=0):
    if guess != correct:
        raise WrongCombinationError(3 - attempts_used - 1)
    return "The vault swings open."


for attempt, guess in enumerate(["9-9-9", "1-2-3"]):
    try:
        print(try_combination(guess, attempts_used=attempt))
    except WrongCombinationError as err:
        print(f"Denied. {err.attempts_left} left.")''',
                   expect="""Denied. 2 left.
The vault swings open."""))}
""",
)

# ---------------------------------------------------------------- 23
_add(
    level=3,
    num="23",
    slug="23-data-formats",
    id="py-23-data-formats",
    card="JSON and CSV: the two formats that carry most of the world's data.",
    title="JSON and CSV",
    emoji="🧾",
    desc="Reading and writing JSON and CSV properly, including the quoting traps that break naive parsers.",
    lede="""Two formats account for a staggering share of all the data moving around the
    world. Python handles both in about four lines each, and both have exactly one trap.""",
    body=f"""
    <h2>JSON: how programs talk to each other</h2>
    <p>
      JSON looks like Python's dictionaries and lists, because both borrowed the notation from
      JavaScript. Every web API you will ever call, including the AI models in Level 6, speaks
      it.
    </p>
    {code('''import json

crew = {
    "ship": "Sea Monkey",
    "captain": "Guybrush",
    "crew": ["Otis", "Meathook"],
    "seaworthy": False,
    "cargo_tons": 12.5,
    "insurance": None,
}

text = json.dumps(crew, indent=2)
print(text)''',
          expect="""{
  "ship": "Sea Monkey",
  "captain": "Guybrush",
  "crew": [
    "Otis",
    "Meathook"
  ],
  "seaworthy": false,
  "cargo_tons": 12.5,
  "insurance": null
}""")}
    <p>Note the translations. They matter when you read someone else's JSON:</p>
    {table(
        ["Python", "JSON"],
        [["<code>dict</code>", "object"],
         ["<code>list</code> and <code>tuple</code>", "array (tuples come back as lists)"],
         ["<code>str</code>", "string, always double-quoted"],
         ["<code>True</code> / <code>False</code>", "<code>true</code> / <code>false</code>"],
         ["<code>None</code>", "<code>null</code>"]],
    )}

    <h2>The four functions</h2>
    {code('''import json
from pathlib import Path

data = {"ship": "Sea Monkey", "crew": ["Otis"]}

text = json.dumps(data)          # to a string  ("dump s"tring)
back = json.loads(text)          # from a string
print(text)
print(back["crew"][0])

with open("ship.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)     # to a file

with open("ship.json", encoding="utf-8") as f:
    loaded = json.load(f)            # from a file

print(loaded == data)''',
          expect="""{"ship": "Sea Monkey", "crew": ["Otis"]}
Otis
True""")}
    {callout("tip", "🔤 dumps and loads have an s for string",
             "<p><code>dump</code> and <code>load</code> work with files. "
             "<code>dumps</code> and <code>loads</code> work with strings. The <code>s</code> "
             "is for string, not plural. Everyone mixes them up for the first month.</p>")}

    <h2>The JSON traps</h2>
    {code('''import json

# 1. Not everything can be encoded
from datetime import date
try:
    json.dumps({"when": date(1990, 10, 15)})
except TypeError as err:
    print("TypeError:", err)

# The fix: convert it yourself
print(json.dumps({"when": date(1990, 10, 15).isoformat()}))

# 2. Dictionary keys always come back as strings
original = {1: "one", 2: "two"}
round_tripped = json.loads(json.dumps(original))
print(original)
print(round_tripped)

# 3. Broken input raises, so handle it
try:
    json.loads("{not json at all}")
except json.JSONDecodeError as err:
    print(f"JSONDecodeError at line {err.lineno} column {err.colno}")''',
          expect="""TypeError: Object of type date is not JSON serializable
{"when": "1990-10-15"}
{1: 'one', 2: 'two'}
{'1': 'one', '2': 'two'}
JSONDecodeError at line 1 column 2""")}
    <p>
      That second one bites people constantly: JSON objects can only have string keys, so
      numeric keys are silently converted. If your data is keyed by id, either accept strings
      or store a list of records instead.
    </p>

    <h2>Non-English text</h2>
    {code('''import json

data = {"name": "Zoë", "ship": "Sjøhesten", "emoji": "🐒"}

print(json.dumps(data))
print(json.dumps(data, ensure_ascii=False))''',
          expect='''{"name": "Zo\\u00eb", "ship": "Sj\\u00f8hesten", "emoji": "\\ud83d\\udc12"}
{"name": "Zoë", "ship": "Sjøhesten", "emoji": "🐒"}''')}
    <p>
      Both are valid JSON and both decode to the same thing. Pass
      <code>ensure_ascii=False</code> when a human is going to read the file, and make sure
      you also opened it with <code>encoding="utf-8"</code>.
    </p>

    <h2>CSV: how spreadsheets talk</h2>
    {code('''import csv

rows = [
    ["name", "role", "pay"],
    ["Guybrush", "captain", 100],
    ["Elaine", "governor", 250],
    ["Otis, the prisoner", "lookout", 40],
]

with open("crew.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

print(open("crew.csv", encoding="utf-8").read())''',
          expect='''name,role,pay
Guybrush,captain,100
Elaine,governor,250
"Otis, the prisoner",lookout,40
''')}

    {voice("PARANOIA", "Legendary: Success",
           "Look at the last row. The name contains a comma, so the csv module wrapped it in "
           "quotes. If you had written this file by hand with ','.join(row), that row would "
           "now have four fields instead of three, and everything after it would be silently "
           "misaligned.",
           "This is why you never parse CSV by splitting on commas. Not once. Not for a quick "
           "script. The quoting rules also cover embedded newlines and embedded quotes, and "
           "the module handles all of it.")}

    <h2>Reading CSV properly</h2>
    {code('''import csv

with open("crew.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows([
        ["name", "role", "pay"],
        ["Guybrush", "captain", 100],
        ["Otis, the prisoner", "lookout", 40],
    ])

# As lists
with open("crew.csv", newline="", encoding="utf-8") as f:
    for row in csv.reader(f):
        print(row)

print("---")

# As dictionaries, keyed by the header row. Much better.
with open("crew.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        print(f"{row['name']:20} {row['role']:10} {row['pay']}")''',
          expect="""['name', 'role', 'pay']
['Guybrush', 'captain', '100']
['Otis, the prisoner', 'lookout', '40']
---
Guybrush             captain    100
Otis, the prisoner   lookout    40""")}
    {callout("warn", "🪤 Two CSV gotchas",
             "<p><strong>Everything comes back as a string.</strong> <code>row['pay']</code> "
             "is <code>'100'</code>, not <code>100</code>. Convert what you need.</p>"
             "<p><strong>Always pass <code>newline=\"\"</code></strong> when opening a CSV file "
             "for reading or writing. Without it you get blank rows between every line on "
             "Windows. The csv module handles line endings itself and needs Python to keep out "
             "of the way.</p>")}

    <h2>Writing dictionaries out</h2>
    {code('''import csv

crew = [
    {"name": "Guybrush", "role": "captain", "pay": 100},
    {"name": "Elaine", "role": "governor", "pay": 250},
]

with open("crew.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "role", "pay"])
    writer.writeheader()
    writer.writerows(crew)

print(open("crew.csv", encoding="utf-8").read().strip())''',
          expect="""name,role,pay
Guybrush,captain,100
Elaine,governor,250""")}

    <h2>Which format when?</h2>
    {table(
        ["Use", "When", "Watch out for"],
        [["<strong>JSON</strong>", "Nested structure, APIs, config files",
          "No comments allowed, no dates, keys become strings"],
         ["<strong>CSV</strong>", "Flat tables, spreadsheets, anything a colleague will open in Excel",
          "Everything is text, quoting rules, no nesting"],
         ["<strong>TOML</strong>", "Config a human edits (<code>tomllib</code> is built in since 3.11)",
          "Read-only in the standard library"],
         ["<strong>SQLite</strong>", "More than a few thousand rows, or you need queries",
          "Lesson 45"]],
    )}

    {exercise(1, "Round-trip a structure",
              "<p>Build a nested dictionary describing a game, save it as JSON, read it back, "
              "and prove nothing was lost.</p>",
              code('''import json
from pathlib import Path

game = {
    "title": "The Secret of Monkey Island",
    "year": 1990,
    "characters": [
        {"name": "Guybrush", "hero": True, "insults": 8},
        {"name": "LeChuck", "hero": False, "insults": 3},
    ],
}

Path("game.json").write_text(json.dumps(game, indent=2), encoding="utf-8")
loaded = json.loads(Path("game.json").read_text(encoding="utf-8"))

print(loaded == game)
print(loaded["characters"][0]["name"])
print(sum(c["insults"] for c in loaded["characters"]))''',
                   expect="""True
Guybrush
11"""))}

    {exercise(2, "CSV to a report",
              "<p>Read a CSV of sales and print the total per region, sorted highest first. "
              "Remember that CSV values are text.</p>",
              code('''import csv
from pathlib import Path

Path("sales.csv").write_text("""region,seller,amount
North,Elaine,1200
South,Otis,340
North,Guybrush,890
South,Meathook,1150
East,Stan,4200
""", encoding="utf-8")

totals = {}
with open("sales.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        amount = int(row["amount"])
        totals[row["region"]] = totals.get(row["region"], 0) + amount

for region, total in sorted(totals.items(), key=lambda pair: pair[1], reverse=True):
    print(f"{region:6} {total:6,}")''',
                   expect="""East    4,200
North   2,090
South   1,490"""))}

    {exercise(3, "Convert CSV to JSON",
              "<p>Write a function that turns any CSV file into a JSON file containing a list "
              "of objects, converting any column that looks numeric.</p>",
              code('''import csv, json
from pathlib import Path


def looks_numeric(value):
    """True if this text should become a number."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def csv_to_json(csv_path, json_path):
    """Convert a CSV file to a JSON array of objects."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = []
        for row in csv.DictReader(f):
            clean = {}
            for key, value in row.items():
                if looks_numeric(value):
                    clean[key] = float(value) if "." in value else int(value)
                else:
                    clean[key] = value
            rows.append(clean)

    Path(json_path).write_text(json.dumps(rows, indent=2), encoding="utf-8")
    return len(rows)


Path("crew.csv").write_text("name,pay,rating\\nGuybrush,100,4.5\\nOtis,40,3.0\\n",
                            encoding="utf-8")

count = csv_to_json("crew.csv", "crew.json")
print(f"{count} rows converted")
print(Path("crew.json").read_text(encoding="utf-8"))''',
                   expect="""2 rows converted
[
  {
    "name": "Guybrush",
    "pay": 100,
    "rating": 4.5
  },
  {
    "name": "Otis",
    "pay": 40,
    "rating": 3.0
  }
]""")
              + "<p>Honest caveat, and a good one to notice: this converts a postcode like "
              "<code>90210</code> or a phone number into a number, which is usually wrong. "
              "Real converters take a schema. Guessing types from data is convenient and "
              "always slightly lossy.</p>")}
""",
)

# ---------------------------------------------------------------- 24
_add(
    level=3,
    num="24",
    slug="24-dates",
    id="py-24-dates",
    card="Dates, times, durations, formatting, and why time zones ruin lives.",
    title="Dates and Times",
    emoji="📅",
    desc="datetime, timedelta, strftime and strptime, ISO format, and the time zone rules that keep software honest.",
    lede="""Time looks simple and is not. This lesson gives you the 90% you need and warns you
    honestly about the 10% that has broken production systems at every company on earth.""",
    body=f"""
    <h2>The three types</h2>
    {code('''from datetime import date, time, datetime

release = date(1990, 10, 15)
opening = time(9, 30)
launch = datetime(1990, 10, 15, 9, 30, 0)

print(release)
print(opening)
print(launch)
print(release.year, release.month, release.day)
print(launch.weekday(), launch.strftime("%A"))''',
          expect="""1990-10-15
09:30:00
1990-10-15 09:30:00
1990 10 15
0 Monday""")}
    <p>
      <code>date</code> is a day, <code>time</code> is a clock reading, <code>datetime</code>
      is both. <code>weekday()</code> counts from 0 for Monday, which is one of those
      arbitrary facts you look up forever.
    </p>

    <h2>Now</h2>
    {code('''from datetime import datetime, date

today = date.today()
now = datetime.now()

print(type(today).__name__, type(now).__name__)
print(now.year >= 2024)''',
          expect="""date datetime
True""")}
    <p>
      This lesson mostly uses fixed dates rather than <code>now()</code>, for the same reason
      the school seeds its random numbers: an example whose output changes every day cannot be
      checked. That is also excellent advice for your own code, and Lesson 29 explains why
      testable code never calls <code>now()</code> deep inside a function.
    </p>

    <h2>Doing arithmetic with timedelta</h2>
    {code('''from datetime import date, timedelta

release = date(1990, 10, 15)
sequel = date(1991, 12, 20)

gap = sequel - release
print(gap)
print(f"{gap.days} days, about {gap.days / 365.25:.1f} years")

print(release + timedelta(days=100))
print(release + timedelta(weeks=52))
print(release - timedelta(days=1))''',
          expect="""431 days, 0:00:00
431 days, about 1.2 years
1991-01-23
1991-10-14
1990-10-14""")}
    <p>
      Subtracting two dates gives a <code>timedelta</code>: a duration. Adding a
      <code>timedelta</code> to a date gives another date, and it handles month lengths and
      leap years for you, which is the entire reason not to do this arithmetic by hand.
    </p>
    {callout("warn", "📆 There is no timedelta(months=1)",
             "<p>Deliberately. How long is a month? Adding one month to 31 January has no "
             "single correct answer, and different businesses want different answers. If you "
             "need calendar months, use the third-party "
             "<code>dateutil.relativedelta</code>, and decide explicitly what your rule "
             "is.</p>")}

    <h2>Formatting: datetime to text</h2>
    {code('''from datetime import datetime

launch = datetime(1990, 10, 15, 9, 5, 30)

print(launch.strftime("%Y-%m-%d"))
print(launch.strftime("%d/%m/%Y"))
print(launch.strftime("%A %d %B %Y"))
print(launch.strftime("%H:%M:%S"))
print(launch.strftime("%I:%M %p"))
print(launch.strftime("Released on %B %d, %Y at %H:%M"))''',
          expect="""1990-10-15
15/10/1990
Monday 15 October 1990
09:05:30
09:05 AM
Released on October 15, 1990 at 09:05""")}
    {table(
        ["Code", "Means", "Example"],
        [["<code>%Y</code> / <code>%y</code>", "year, 4 or 2 digits", "1990 / 90"],
         ["<code>%m</code> / <code>%B</code> / <code>%b</code>", "month number / name / short", "10 / October / Oct"],
         ["<code>%d</code>", "day of month", "15"],
         ["<code>%A</code> / <code>%a</code>", "weekday name / short", "Monday / Mon"],
         ["<code>%H</code> / <code>%I</code>", "hour, 24 or 12", "09 / 09"],
         ["<code>%M</code> / <code>%S</code>", "minute / second", "05 / 30"],
         ["<code>%p</code>", "AM or PM", "AM"]],
    )}

    <h2>Parsing: text to datetime</h2>
    {code('''from datetime import datetime, date

parsed = datetime.strptime("15/10/1990", "%d/%m/%Y")
print(parsed)          # no time in the input, so midnight

# ISO 8601 is the sane interchange format, and has its own shortcut
print(date.fromisoformat("1990-10-15"))
print(datetime.fromisoformat("1990-10-15T09:30:00"))
print(date(1990, 10, 15).isoformat())

try:
    datetime.strptime("banana", "%d/%m/%Y")
except ValueError as err:
    print("ValueError:", err)''',
          expect="""1990-10-15 00:00:00
1990-10-15
1990-10-15 09:30:00
1990-10-15
ValueError: time data 'banana' does not match format '%d/%m/%Y'""")}

    {voice("ENCYCLOPEDIA", "Medium: Success",
           "Always store and exchange dates as ISO 8601: 1990-10-15. It sorts correctly as "
           "plain text, it is unambiguous worldwide, and it is what every database and API "
           "expects.",
           "The format 10/15/1990 versus 15/10/1990 has caused genuine medical and financial "
           "errors. On the third of April, half the world writes 03/04 and the other half "
           "writes 04/03, and neither half is warned.")}

    <h2>Time zones, honestly</h2>
    {code('''from datetime import datetime, timezone, timedelta

naive = datetime(1990, 10, 15, 9, 30)
aware = datetime(1990, 10, 15, 9, 30, tzinfo=timezone.utc)

print(naive, "<- no idea where in the world this is")
print(aware, "<- unambiguous")

melee_time = timezone(timedelta(hours=-5))
print(aware.astimezone(melee_time))

# comparing the two raises, which is Python protecting you
try:
    print(naive < aware)
except TypeError as err:
    print("TypeError:", err)''',
          expect="""1990-10-15 09:30:00 <- no idea where in the world this is
1990-10-15 09:30:00+00:00 <- unambiguous
1990-10-15 04:30:00-05:00
TypeError: can't compare offset-naive and offset-aware datetimes""")}
    <p>Three rules that will save you real pain:</p>
    <ol>
      <li><strong>Store UTC.</strong> Always. Convert to local time only when displaying it to
      a human.</li>
      <li><strong>Use aware datetimes</strong> for anything that crosses a machine boundary.
      Naive ones are fine for a stopwatch and dangerous for a calendar.</li>
      <li><strong>Never write your own offset arithmetic.</strong> Daylight saving means some
      local times happen twice a year and some never happen at all. Python 3.9 added
      <code>zoneinfo</code>, which knows the real rules for every zone.</li>
    </ol>
    {code('''from datetime import datetime
from zoneinfo import ZoneInfo

utc = datetime(2026, 6, 15, 12, 0, tzinfo=ZoneInfo("UTC"))

for zone in ["Europe/London", "America/New_York", "Asia/Tokyo"]:
    local = utc.astimezone(ZoneInfo(zone))
    print(f"{zone:18} {local.strftime('%Y-%m-%d %H:%M %Z')}")''',
          expect="""Europe/London      2026-06-15 13:00 BST
America/New_York   2026-06-15 08:00 EDT
Asia/Tokyo         2026-06-15 21:00 JST""")}

    <h2>Measuring how long something took</h2>
    {code('''import time

start = time.perf_counter()
total = sum(range(1_000_000))
elapsed = time.perf_counter() - start

print(f"summed to {total:,}")
print(f"took less than a second: {elapsed < 1}")''',
          expect="""summed to 499,999,500,000
took less than a second: True""")}
    <p>
      Use <code>time.perf_counter()</code> for measuring durations, not
      <code>datetime.now()</code>: it is monotonic, so it cannot go backwards when the system
      clock is adjusted or the clocks change. Lesson 51 uses it properly with
      <code>timeit</code>.
    </p>

    {exercise(1, "How old is this?",
              "<p>Write a function that takes a release date and a reference date and returns "
              "a friendly age like '35 years, 10 months'. Approximating months as 30.44 days "
              "is fine.</p>",
              code('''from datetime import date


def age_of(released, today):
    """Return a friendly age string between two dates."""
    days = (today - released).days
    years = days // 365
    months = int((days % 365) / 30.44)
    return f"{years} years, {months} months"


print(age_of(date(1990, 10, 15), date(2026, 8, 17)))
print(age_of(date(2024, 1, 1), date(2026, 8, 17)))''',
                   expect="""35 years, 10 months
2 years, 7 months""")
              + "<p>Approximate, and honest about it. If you need exact calendar arithmetic, "
              "that is what <code>dateutil.relativedelta</code> exists for.</p>")}

    {exercise(2, "Working days until",
              "<p>Count the weekdays (Monday to Friday) between two dates, excluding the start "
              "and including the end.</p>",
              code('''from datetime import date, timedelta


def working_days(start, end):
    """Count Mon-Fri days after start, up to and including end."""
    days = 0
    current = start + timedelta(days=1)
    while current <= end:
        if current.weekday() < 5:
            days += 1
        current += timedelta(days=1)
    return days


print(working_days(date(2026, 8, 17), date(2026, 8, 31)))''',
                   expect="10")
              + "<p>A loop over days is perfectly acceptable here: two weeks is fourteen "
              "iterations. If you were doing this across ten years you would want maths "
              "instead of a loop, and that is a good instinct to develop.</p>")}

    {exercise(3, "Parse a messy log",
              "<p>These timestamps arrive in three different formats. Normalise them all to "
              "ISO and sort them chronologically.</p>",
              code('''from datetime import datetime

raw = [
    "15/10/1990 09:30",
    "1991-12-20T14:00:00",
    "Jan 03 1993 18:45",
]

formats = ["%d/%m/%Y %H:%M", "%Y-%m-%dT%H:%M:%S", "%b %d %Y %H:%M"]


def parse_any(text):
    """Try each known format until one works."""
    for fmt in formats:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError(f"no known format matches {text!r}")


parsed = sorted(parse_any(t) for t in raw)
for moment in parsed:
    print(moment.isoformat())''',
                   expect="""1990-10-15T09:30:00
1991-12-20T14:00:00
1993-01-03T18:45:00""")
              + "<p>Try-each-format-until-one-works is the standard approach to messy real "
              "data, and raising a clear error when nothing matches is what stops the mess "
              "spreading silently into your database.</p>")}
""",
)

# ---------------------------------------------------------------- 25
_add(
    level=3,
    num="25",
    slug="25-regex",
    id="py-25-regex",
    card="Pattern matching for text: powerful, ugly, and worth exactly the amount you learn.",
    title="Regular Expressions",
    emoji="🔍",
    desc="A gentle, practical introduction to the re module: patterns, groups, findall, sub, and when not to use regex.",
    lede="""A tiny language for describing shapes of text. It looks like someone sat on a
    keyboard, and it will one day save you four hours in four minutes.""",
    body=f"""
    <h2>Why bother</h2>
    <p>
      You can find a phone number in a document with string methods. It takes forty lines and
      misses cases. With a pattern it is one line. The trade is that the line is unreadable
      until you learn the notation, so this lesson teaches the 20% that does 80% of the work.
    </p>
    {code('''import re

text = "Call Stan on 555-0199 or Elaine on 555-0100 before Friday."

print(re.findall(r"\\d{3}-\\d{4}", text))''',
          expect="['555-0199', '555-0100']")}
    <p>
      <code>\\d{{3}}-\\d{{4}}</code> means "three digits, a hyphen, four digits". That is the
      whole idea: you describe a <em>shape</em>, and Python finds every piece of text with
      that shape.
    </p>

    {callout("tip", "🅁 Always use raw strings",
             "<p>Write patterns as <code>r\"...\"</code>. Regex uses backslashes constantly, "
             "and so do Python strings, so without the <code>r</code> you end up writing "
             "<code>\"\\\\\\\\d\"</code> to mean one <code>\\d</code>. The <code>r</code> prefix "
             "turns that off. Every regex you ever see in real code has it.</p>")}

    <h2>The pieces worth memorising</h2>
    {table(
        ["Pattern", "Matches", "Example"],
        [["<code>.</code>", "any single character except newline", "<code>a.c</code> matches abc, a7c"],
         ["<code>\\d</code>", "a digit", "<code>\\d\\d</code> matches 42"],
         ["<code>\\w</code>", "a letter, digit or underscore", "<code>\\w+</code> matches a word"],
         ["<code>\\s</code>", "any whitespace", "space, tab, newline"],
         ["<code>[abc]</code>", "any one of these", "<code>[aeiou]</code> is a vowel"],
         ["<code>[^abc]</code>", "anything except these", ""],
         ["<code>[a-z]</code>", "a range", "<code>[A-Za-z]</code> is any letter"],
         ["<code>*</code>", "zero or more of the thing before", "<code>ab*</code> matches a, ab, abbb"],
         ["<code>+</code>", "one or more", "<code>\\d+</code> is a number"],
         ["<code>?</code>", "zero or one, so optional", "<code>colou?r</code> matches both spellings"],
         ["<code>{{3}}</code>", "exactly three", "<code>\\d{{3}}</code>"],
         ["<code>{{2,4}}</code>", "between two and four", ""],
         ["<code>^</code> / <code>$</code>", "start / end of the text", "<code>^Dear</code>"],
         ["<code>|</code>", "either", "<code>cat|dog</code>"],
         ["<code>( )</code>", "a group you want to capture", ""]],
    )}

    <h2>The five functions</h2>
    {code('''import re

text = "Guybrush scored 95, Elaine scored 88, Otis scored 42."

print(re.findall(r"\\d+", text))
print(re.search(r"\\d+", text).group())
print(re.match(r"Guybrush", text) is not None)
print(re.sub(r"\\d+", "??", text))
print(re.split(r",\\s*", text))''',
          expect="""['95', '88', '42']
95
True
Guybrush scored ??, Elaine scored ??, Otis scored ??.
['Guybrush scored 95', 'Elaine scored 88', 'Otis scored 42.']""")}
    {table(
        ["Function", "Does", "Returns"],
        [["<code>re.findall</code>", "every match", "a list of strings"],
         ["<code>re.search</code>", "the first match anywhere", "a match object, or None"],
         ["<code>re.match</code>", "a match at the very start only", "a match object, or None"],
         ["<code>re.sub</code>", "find and replace", "a new string"],
         ["<code>re.split</code>", "split on a pattern", "a list"],
         ["<code>re.finditer</code>", "every match, lazily, with positions", "match objects"]],
    )}
    <p>
      <code>search</code> and <code>match</code> return <code>None</code> when there is no
      match, and <code>None.group()</code> raises <code>AttributeError</code>. Always test
      before using the result.
    </p>

    <h2>Groups: pulling pieces out</h2>
    {code('''import re

log = "2026-08-17 09:30:00 ERROR disk full"

pattern = r"(\\d{4})-(\\d{2})-(\\d{2}) (\\d{2}:\\d{2}:\\d{2}) (\\w+) (.+)"
found = re.search(pattern, log)

if found:
    print(found.group(0))
    print(found.group(1), found.group(2), found.group(3))
    print(found.group(5), "->", found.group(6))
    print(found.groups())''',
          expect="""2026-08-17 09:30:00 ERROR disk full
2026 08 17
ERROR -> disk full
('2026', '08', '17', '09:30:00', 'ERROR', 'disk full')""")}
    <p>Numbered groups get unreadable fast. Name them:</p>
    {code('''import re

log = "2026-08-17 09:30:00 ERROR disk full"

pattern = (r"(?P<date>\\d{4}-\\d{2}-\\d{2}) "
           r"(?P<time>\\d{2}:\\d{2}:\\d{2}) "
           r"(?P<level>\\w+) "
           r"(?P<message>.+)")

found = re.search(pattern, log)
if found:
    parts = found.groupdict()
    print(parts["level"], "on", parts["date"])
    print(parts)''',
          expect="""ERROR on 2026-08-17
{'date': '2026-08-17', 'time': '09:30:00', 'level': 'ERROR', 'message': 'disk full'}""")}

    <h2>Greedy versus lazy: the classic surprise</h2>
    {code('''import re

html = "<b>bold</b> and <i>italic</i>"

print(re.findall(r"<.+>", html))
print(re.findall(r"<.+?>", html))''',
          expect="""['<b>bold</b> and <i>italic</i>']
['<b>', '</b>', '<i>', '</i>']""")}

    {voice("LOGIC", "Formidable: Success",
           "<code>+</code> and <code>*</code> are greedy: they take as much as they possibly "
           "can while still allowing a match. The first pattern matched from the very first "
           "&lt; to the very last &gt;, which is technically correct and completely useless.",
           "Adding <code>?</code> after them makes them lazy: take as little as possible. When "
           "a pattern matches far more than you expected, this is nearly always why.")}

    <h2>Substitution with groups</h2>
    {code('''import re

dates = "Due 15/10/1990, meeting 20/12/1991."

iso = re.sub(r"(\\d{2})/(\\d{2})/(\\d{4})", r"\\3-\\2-\\1", dates)
print(iso)

def shout(match):
    return match.group(0).upper()

print(re.sub(r"\\b\\w{4}\\b", shout, "this is a test of four char words"))''',
          expect="""Due 1990-10-15, meeting 1991-12-20.
THIS is a TEST of FOUR CHAR words""")}
    <p>
      <code>\\3-\\2-\\1</code> in the replacement means "group 3, then group 2, then group 1".
      And when the replacement needs logic, pass a <em>function</em>: it receives each match
      and returns the replacement text.
    </p>

    <h2>Useful patterns to steal</h2>
    {code('''import re

text = """Contact elaine@melee.gov or stan@usedships.example.
Visit https://rustyschool.com/python for the course.
Ring 555-0199. Order #A-1042 shipped 2026-08-17."""

print(re.findall(r"[\\w.+-]+@[\\w-]+\\.[\\w.]+", text))
print(re.findall(r"https?://[^\\s]+", text))
print(re.findall(r"\\d{4}-\\d{2}-\\d{2}", text))
print(re.findall(r"#[A-Z]-\\d+", text))''',
          expect="""['elaine@melee.gov', 'stan@usedships.example.']
['https://rustyschool.com/python']
['2026-08-17']
['#A-1042']""")}
    <p>
      Spot the trailing full stop on that second address. The pattern's final
      <code>[\\w.]+</code> includes dots, so it kept going past the domain and took the end of
      the sentence with it. Patterns match text, not meaning, and this is exactly the kind of
      near-miss that survives a quick eyeball and breaks later.
    </p>
    {callout("warn", "📧 On validating email addresses",
             "<p>That email pattern is fine for <em>finding</em> addresses in text. It is not "
             "a validator. The real specification for a valid email address is monstrous, and "
             "the standard regex that implements it is thousands of characters long. The "
             "industry answer is: check there is an @ with something either side, then send a "
             "confirmation message. That is the only real test anyway.</p>")}

    <h2>Compile patterns you reuse</h2>
    {code('''import re

pattern = re.compile(r"\\berror\\b", re.IGNORECASE)

lines = ["Error: disk full", "all fine", "ERROR again", "terrorist"]
for line in lines:
    if pattern.search(line):
        print(f"match: {line}")''',
          expect="""match: Error: disk full
match: ERROR again""")}
    <p>
      <code>re.compile</code> parses the pattern once instead of on every call, and gives you
      somewhere to hang a name and a comment. <code>\\b</code> is a word boundary, which is why
      "terrorist" does not match. Flags like <code>re.IGNORECASE</code> and
      <code>re.MULTILINE</code> go here.
    </p>

    <h2>When not to use regex</h2>
    <ul>
      <li><strong>Parsing HTML or XML.</strong> Use a parser. HTML is not a regular language
      and cannot be correctly matched by a regular expression. This is a mathematical fact,
      not an opinion.</li>
      <li><strong>Parsing CSV.</strong> Use the <code>csv</code> module. Lesson 23 showed you
      why.</li>
      <li><strong>When a string method does it.</strong> <code>"x" in text</code> beats
      <code>re.search</code> for a literal substring, and is faster and clearer.</li>
      <li><strong>When the pattern needs a comment to be readable</strong> and you only use it
      once. A short loop can be kinder to the next reader.</li>
    </ul>

    {exercise(1, "Extract and total",
              "<p>Pull every price out of a receipt and total them.</p>",
              code('''import re

receipt = """Grog        £4.50
Rubber chicken   £12.00
Map        £3.25
Sword      £8.75"""

prices = re.findall(r"£(\\d+\\.\\d{2})", receipt)
print(prices)
print(f"Total: £{sum(float(p) for p in prices):.2f}")''',
                   expect="""['4.50', '12.00', '3.25', '8.75']
Total: £28.50""")
              + "<p>The group around the number means <code>findall</code> returns just the "
              "digits, not the currency symbol. Groups control what you get back, which is "
              "half the reason to use them.</p>")}

    {exercise(2, "Redact sensitive data",
              "<p>Replace every email address and phone number in a message with "
              "<code>[redacted]</code>, keeping everything else intact.</p>",
              code('''import re

message = """From: elaine@melee.gov
Call me on 555-0199 or reach stan@usedships.example.
The meeting is Tuesday."""

redacted = re.sub(r"[\\w.+-]+@[\\w-]+\\.[\\w.]+", "[redacted email]", message)
redacted = re.sub(r"\\d{3}-\\d{4}", "[redacted phone]", redacted)

print(redacted)''',
                   expect="""From: [redacted email]
Call me on [redacted phone] or reach [redacted email]
The meeting is Tuesday.""")
              + "<p>Look closely at the second line: the full stop after "
              "<code>usedships.example</code> has vanished. The pattern ends with "
              "<code>[\\w.]+</code>, which happily includes dots, so it swallowed the "
              "sentence's punctuation along with the domain.</p>"
              "<p>That is greedy matching biting you in a way that is easy to miss, because "
              "the output still looks plausible. Ending the pattern with "
              "<code>[\\w-]+\\.[A-Za-z]{2,}</code> would stop at the top-level domain "
              "instead. Always read what a regex actually matched, not what you meant.</p>")}

    {exercise(3, "Parse a log file",
              "<p>Turn each line of a log into a dictionary, and count how many of each level "
              "there were. Skip any line that does not match.</p>",
              code('''import re
from collections import Counter

log = """2026-08-17 09:30:00 INFO server started
2026-08-17 09:31:12 ERROR disk full
this line is garbage
2026-08-17 09:31:45 WARN retrying
2026-08-17 09:32:00 ERROR still full"""

pattern = re.compile(
    r"(?P<date>\\d{4}-\\d{2}-\\d{2}) (?P<time>[\\d:]+) (?P<level>\\w+) (?P<message>.+)"
)

entries = []
for line in log.splitlines():
    found = pattern.match(line)
    if found:
        entries.append(found.groupdict())

print(f"{len(entries)} parsed, 1 skipped")
for level, count in Counter(e["level"] for e in entries).most_common():
    print(f"  {level:6} {count}")

for entry in entries:
    if entry["level"] == "ERROR":
        print(f"{entry['time']} {entry['message']}")''',
                   expect="""4 parsed, 1 skipped
  ERROR  2
  INFO   1
  WARN   1
09:31:12 disk full
09:32:00 still full""")
              + "<p>Silently skipping unparseable lines is a decision, not a default. In a "
              "real tool you would count them and report the number, because a log format that "
              "quietly changed is exactly the sort of thing you want to hear about.</p>")}
""",
)

# ---------------------------------------------------------------- 26
_add(
    level=3,
    num="26",
    slug="26-venv",
    id="py-26-venv",
    card="Virtual environments and pip: how to install other people's code without wrecking your machine.",
    title="Virtual Environments and pip",
    emoji="🧪",
    desc="Why virtual environments exist, creating and activating them, pip, requirements files, and uv.",
    lede="""Half a million packages are waiting for you on PyPI. Two commands stop them from
    turning your computer into a swamp.""",
    body=f"""
    <h2>The problem, first</h2>
    <p>
      Project A needs version 1 of a library. Project B needs version 2. If both install into
      the same Python, one of them breaks. Multiply by twenty projects and several years and
      you get a machine where nothing works and nobody knows why. This has a name:
      dependency hell.
    </p>
    <p>
      A <strong>virtual environment</strong> is a private Python for one project: its own
      folder, its own installed packages, isolated from everything else. Making one is one
      command, and you should make one for every project, every time, no exceptions.
    </p>

    <h2>The three commands</h2>
    {term("""# 1. create it (once per project)
python3 -m venv .venv

# 2. activate it (every time you open a terminal)
source .venv/bin/activate        # macOS and Linux
.venv\\Scripts\\activate           # Windows PowerShell

# 3. install things (they land inside .venv, not on your system)
pip install requests""")}
    <p>Once activated, your prompt changes to show it:</p>
    {term("""$ source .venv/bin/activate
(.venv) $ which python
/Users/you/python-school/.venv/bin/python

(.venv) $ pip install requests
Successfully installed requests-2.32.3 ...

(.venv) $ deactivate
$ """)}
    {callout("tip", "📁 Call it .venv",
             "<p>The name is a convention, and a strong one: editors like VS Code look for "
             "<code>.venv</code> and offer to use it automatically, and every "
             "<code>.gitignore</code> template already excludes it. The leading dot hides it "
             "from ordinary directory listings.</p>")}

    <h2>Never commit it</h2>
    {code('''# .gitignore
.venv/
__pycache__/
*.pyc
.env''', run=False, verify="skip")}
    <p>
      A virtual environment contains thousands of files, is specific to your operating system,
      and can be rebuilt from a text file in seconds. Committing it to git is a classic
      beginner mistake that makes a repository unusably large.
    </p>

    <h2>Recording what you need</h2>
    {term("""(.venv) $ pip freeze > requirements.txt
(.venv) $ cat requirements.txt
certifi==2025.7.9
charset-normalizer==3.4.2
idna==3.10
requests==2.32.3
urllib3==2.5.0""")}
    <p>
      Anyone (including you, on another machine, in a year) can then recreate the exact
      environment:
    </p>
    {term("""python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt""")}

    {voice("VOLITION", "Medium: Success",
           "This is the moment your code becomes shareable. Before a requirements file, "
           "'it works on my machine' is a true statement and a useless one. After it, someone "
           "else can reproduce your machine in thirty seconds.",
           "Reproducibility is not bureaucracy. It is the difference between a script and "
           "software.")}

    <h2>pip, the essential commands</h2>
    {table(
        ["Command", "Does"],
        [["<code>pip install requests</code>", "Install the latest version"],
         ["<code>pip install requests==2.32.3</code>", "Install exactly that version"],
         ["<code>pip install 'requests&gt;=2.30'</code>", "Install at least that version"],
         ["<code>pip install -r requirements.txt</code>", "Install everything listed in a file"],
         ["<code>pip list</code>", "What is installed here"],
         ["<code>pip show requests</code>", "Details, including what depends on what"],
         ["<code>pip uninstall requests</code>", "Remove it"],
         ["<code>pip install --upgrade requests</code>", "Update it"]],
    )}
    {callout("warn", "🎯 Use python3 -m pip, not bare pip",
             "<p><code>python3 -m pip install x</code> guarantees the package lands in the "
             "same Python you are running. Bare <code>pip</code> can belong to a different "
             "installation, which produces the single most baffling beginner experience there "
             "is: pip says it installed successfully, and Python says "
             "<code>ModuleNotFoundError</code>.</p>")}

    <h2>Using an installed package</h2>
    {code('''# after: pip install requests
import requests

response = requests.get("https://api.github.com/repos/python/cpython")
data = response.json()

print(data["name"], "has", data["stargazers_count"], "stars")''',
          run=False, verify="compile")}
    <p>
      That block has no run button, because the school's in-browser Python has no network
      access and no third-party packages. This is exactly the point at which doing
      <a href="../setup.html">the ten-minute lab setup</a> starts to pay off. Lesson 42 covers
      <code>requests</code> properly.
    </p>

    <h2>The modern alternative: uv</h2>
    <p>
      {link("uv", "https://github.com/astral-sh/uv")} is a drop-in replacement for pip and venv
      that is typically 10 to 100 times faster, because it is written in Rust. It is
      increasingly the default choice in new projects.
    </p>
    {term("""# the same three ideas, one tool
uv venv                       # create .venv
uv pip install requests       # install into it
uv run script.py              # run with the right environment, no activation needed

# or let it manage the whole project
uv init my-project
uv add requests""")}
    {callout("info", "🦀 Wait, a Python tool written in Rust?",
             "<p>Yes, and it is one of the best arguments for learning both languages. uv, "
             "<a href='https://github.com/astral-sh/ruff' target='_blank' rel='noopener'>ruff</a> "
             "(the linter) and <a href='https://pola.rs' target='_blank' rel='noopener'>Polars</a> "
             "(dataframes) are all Rust programs that made the Python ecosystem dramatically "
             "faster. The pattern is: write the workflow in Python, write the hot inner loop "
             "in Rust. Lesson 51 shows you how to do it yourself, and the "
             "<a href='../../learn/index.html'>Rusty School</a> is next door when you are "
             "ready.</p>")}

    <h2>Judging a package before you install it</h2>
    <p>
      Anyone can publish to PyPI. Packages have been published with names one typo away from
      popular ones, containing malware. Before installing something you have not heard of:
    </p>
    <ul>
      <li><strong>Check the name character by character.</strong> <code>requests</code> is
      real. <code>request</code>, <code>requsts</code> and <code>python-requests</code> are the
      kind of thing attackers register. This is called typosquatting.</li>
      <li><strong>Look at the PyPI page.</strong> When was it last released? Does it link to a
      real source repository?</li>
      <li><strong>Look at the repository.</strong> Stars, recent commits, open issues being
      answered.</li>
      <li><strong>Prefer the standard library</strong> when it will do. Zero dependencies is
      zero supply chain risk.</li>
      <li><strong>Pin your versions</strong> in <code>requirements.txt</code> so an update
      cannot change under you without you noticing.</li>
    </ul>

    <h2>Common problems</h2>
    {table(
        ["Symptom", "Cause", "Fix"],
        [["<code>ModuleNotFoundError</code> right after installing",
          "Installed into a different Python",
          "Activate the venv, then <code>python3 -m pip install x</code>"],
         ["<code>externally-managed-environment</code>",
          "You are installing into the system Python on Linux or Homebrew",
          "Make and activate a venv. The error is protecting you"],
         ["<code>command not found: pip</code>", "Not activated, or pip not installed",
          "<code>python3 -m ensurepip</code>, then activate"],
         ["Works in the terminal, not in VS Code", "The editor is using a different interpreter",
          "Ctrl+Shift+P, 'Python: Select Interpreter', pick the <code>.venv</code> one"],
         ["<code>Permission denied</code> while installing", "Trying to write to a system folder",
          "Never use <code>sudo pip</code>. Use a venv"]],
    )}

    {exercise(1, "Set up a real project",
              "<p>On your own machine, do the whole loop: folder, venv, activate, install "
              "<code>requests</code>, freeze, and confirm which Python is in charge.</p>",
              term("""mkdir weather-tool && cd weather-tool
python3 -m venv .venv
source .venv/bin/activate

python -m pip install requests
python -c "import requests; print(requests.__version__)"

pip freeze > requirements.txt
printf '.venv/\\n__pycache__/\\n' > .gitignore

which python
deactivate""")
              + "<p>If <code>which python</code> printed a path ending in "
              "<code>weather-tool/.venv/bin/python</code>, everything is correct. That "
              "sequence is the opening move of every Python project you will ever start.</p>")}

    {exercise(2, "Read a requirements file",
              "<p>What does each line mean, and which one would you object to in a code "
              "review?</p>"
              + code('''requests==2.32.3
rich>=13.0
pandas
numpy~=1.26.0''', run=False, verify="skip"),
              "<ol><li><code>requests==2.32.3</code>: exactly this version. Fully "
              "reproducible.</li>"
              "<li><code>rich&gt;=13.0</code>: this or newer. A future version 14 could break "
              "you.</li>"
              "<li><code>pandas</code>: <strong>any version at all</strong>. This is the one to "
              "object to. Today it installs 2.x; next year it installs 3.x and your program "
              "changes behaviour with no change to your code.</li>"
              "<li><code>numpy~=1.26.0</code>: compatible release, so 1.26.x but not 1.27. A "
              "sensible middle ground.</li></ol>"
              "<p>Rule of thumb: pin exactly for applications you deploy, use ranges for "
              "libraries other people will install alongside things you cannot predict.</p>")}

    {exercise(3, "Explain it to a colleague",
              "<p>A teammate says: 'Virtual environments are pointless, I just install "
              "everything globally and it works fine.' Write the three-sentence reply.</p>",
              "<p>Something like: <em>It works fine until two projects need different versions "
              "of the same library, and then one of them breaks in a way that is genuinely "
              "hard to diagnose. It also means nobody else can reproduce your setup, so 'works "
              "on my machine' becomes the whole support process. A venv costs one command per "
              "project and removes both problems permanently.</em></p>"
              "<p>The persuasive detail is the second sentence. Most people accept isolation "
              "as theory and adopt it for real the first time a colleague cannot run their "
              "code.</p>")}
""",
)

# ---------------------------------------------------------------- 27
_add(
    level=3,
    num="27",
    slug="27-cli",
    id="py-27-cli",
    card="Turn a script into a proper command-line tool with arguments, flags and help text.",
    title="Command-Line Programs",
    emoji="⌨️",
    desc="sys.argv, argparse, flags, subcommands, exit codes, and making a script feel like a real Unix tool.",
    lede="""The difference between a script you edit before every run and a tool you actually
    use is about fifteen lines of argument parsing.""",
    body=f"""
    <h2>The raw way: sys.argv</h2>
    {code('''import sys

# when run as: python3 greet.py Guybrush pirate
print(sys.argv)          # ['greet.py', 'Guybrush', 'pirate']''',
          run=False, verify="compile")}
    <p>
      <code>sys.argv</code> is a list of what was typed, with the script name first. It works,
      and for a two-argument throwaway it is fine. It gives you no help text, no validation, no
      flags, and no type conversion, which is why nobody uses it for anything real.
    </p>

    <h2>argparse: the standard answer</h2>
    {code('''import argparse

parser = argparse.ArgumentParser(description="Greet someone, loudly if required.")
parser.add_argument("name", help="who to greet")
parser.add_argument("--times", type=int, default=1, help="how many times")
parser.add_argument("--shout", action="store_true", help="use capital letters")

# normally: args = parser.parse_args()
# for this lesson we pass the list ourselves so the example can run
args = parser.parse_args(["Guybrush", "--times", "3", "--shout"])

message = f"Hello, {args.name}!"
if args.shout:
    message = message.upper()

for _ in range(args.times):
    print(message)''',
          expect="""HELLO, GUYBRUSH!
HELLO, GUYBRUSH!
HELLO, GUYBRUSH!""")}
    <p>For fifteen lines you get, entirely for free:</p>
    {term("""$ python3 greet.py --help
usage: greet.py [-h] [--times TIMES] [--shout] name

Greet someone, loudly if required.

positional arguments:
  name           who to greet

options:
  -h, --help     show this help message and exit
  --times TIMES  how many times
  --shout        use capital letters

$ python3 greet.py
usage: greet.py [-h] [--times TIMES] [--shout] name
greet.py: error: the following arguments are required: name""")}
    <p>
      Help text, usage lines, error messages, and a non-zero exit code on failure. Writing that
      by hand takes an hour and is worse.
    </p>

    <h2>The argument types you will use</h2>
    {code('''import argparse

parser = argparse.ArgumentParser(prog="crewtool")

parser.add_argument("files", nargs="+", help="one or more files")
parser.add_argument("-o", "--output", default="out.txt", help="where to write")
parser.add_argument("-n", "--limit", type=int, default=10, help="max rows")
parser.add_argument("-v", "--verbose", action="store_true", help="chatty mode")
parser.add_argument("--format", choices=["json", "csv", "text"], default="text")

args = parser.parse_args(["a.csv", "b.csv", "-n", "5", "--format", "json", "-v"])

print(args.files)
print(args.output, args.limit, args.verbose, args.format)''',
          expect="""['a.csv', 'b.csv']
out.txt 5 True json""")}
    {table(
        ["Written as", "Gives you"],
        [["<code>add_argument(\"name\")</code>", "A required positional argument"],
         ["<code>add_argument(\"--flag\")</code>", "An optional named argument"],
         ["<code>action=\"store_true\"</code>", "A yes/no switch, False unless present"],
         ["<code>type=int</code>", "Automatic conversion, with a clear error if it fails"],
         ["<code>default=x</code>", "What to use when it is not given"],
         ["<code>choices=[...]</code>", "Validation against a fixed set"],
         ["<code>nargs=\"+\"</code>", "One or more values, as a list"],
         ["<code>nargs=\"?\"</code>", "Optional positional"],
         ["<code>required=True</code>", "Force an optional argument to be given"]],
    )}

    <h2>Subcommands, like git</h2>
    {code('''import argparse

parser = argparse.ArgumentParser(prog="crew")
subs = parser.add_subparsers(dest="command", required=True)

add = subs.add_parser("add", help="add a crew member")
add.add_argument("name")
add.add_argument("--role", default="deckhand")

remove = subs.add_parser("remove", help="remove someone")
remove.add_argument("name")

subs.add_parser("list", help="show everyone")


def run(argv):
    args = parser.parse_args(argv)
    if args.command == "add":
        return f"Added {args.name} as {args.role}"
    if args.command == "remove":
        return f"Removed {args.name}"
    return "Crew: Guybrush, Elaine, Otis"


print(run(["add", "Meathook", "--role", "lookout"]))
print(run(["remove", "Otis"]))
print(run(["list"]))''',
          expect="""Added Meathook as lookout
Removed Otis
Crew: Guybrush, Elaine, Otis""")}
    <p>
      That is the shape of <code>git commit</code>, <code>docker run</code> and
      <code>pip install</code>. Each subcommand gets its own arguments and its own help.
    </p>

    <h2>Exit codes, and why they matter</h2>
    {code('''import sys


def main():
    """Return 0 for success, non-zero for failure."""
    problem = True
    if problem:
        print("could not read the crew file", file=sys.stderr)
        return 1
    print("all good")
    return 0


# in a real script:
# if __name__ == "__main__":
#     sys.exit(main())

print("would exit with", main())''',
          expect="""could not read the crew file
would exit with 1""")}
    <p>Two conventions that make your tool a good citizen of the command line:</p>
    <ul>
      <li><strong>Exit 0 for success, non-zero for failure.</strong> This is how
      <code>&amp;&amp;</code>, shell scripts and CI systems know whether to continue. A program
      that always exits 0 cannot be automated.</li>
      <li><strong>Errors go to stderr, results go to stdout.</strong> Then someone can write
      <code>mytool data.csv &gt; results.txt</code> and still see the error messages on screen
      rather than mixed into their output file.</li>
    </ul>

    <h2>The complete shape of a real tool</h2>
    {code('''#!/usr/bin/env python3
"""wordcount: count lines, words and characters in files."""

import argparse
import sys
from pathlib import Path


def count(path):
    """Return (lines, words, characters) for one file."""
    text = Path(path).read_text(encoding="utf-8")
    return len(text.splitlines()), len(text.split()), len(text)


def build_parser():
    parser = argparse.ArgumentParser(
        prog="wordcount",
        description="Count lines, words and characters.",
    )
    parser.add_argument("files", nargs="+", help="files to count")
    parser.add_argument("-l", "--lines-only", action="store_true")
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    failures = 0

    for name in args.files:
        try:
            lines, words, chars = count(name)
        except FileNotFoundError:
            print(f"wordcount: {name}: no such file", file=sys.stderr)
            failures += 1
            continue
        if args.lines_only:
            print(f"{lines:6} {name}")
        else:
            print(f"{lines:6} {words:6} {chars:6}  {name}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())''',
          run=False, verify="compile")}
    <p>
      Note the structure: <code>count</code> is a pure function with no argument parsing in
      it, <code>build_parser</code> is separate so tests can inspect it, and <code>main</code>
      takes an optional <code>argv</code> so tests can call it directly without touching the
      real command line. That last trick is what makes a CLI testable, and it costs one
      default argument.
    </p>

    {callout("tip", "🎨 When you want it to look good",
             "<p>The standard library is deliberately plain. Two popular third-party options: "
             "<a href='https://typer.tiangolo.com' target='_blank' rel='noopener'>Typer</a> "
             "builds the whole parser from your function's type hints, and "
             "<a href='https://rich.readthedocs.io' target='_blank' rel='noopener'>rich</a> "
             "gives you colours, tables, progress bars and spinners in about two lines. "
             "Neither is needed to learn the ideas, and both are a joy once you have.</p>")}

    {exercise(1, "Add flags to a converter",
              "<p>Build a parser for a temperature tool that takes a number, a "
              "<code>--to</code> choice of c or f, and an optional <code>--precision</code>. "
              "Show it working for two different calls.</p>",
              code('''import argparse

parser = argparse.ArgumentParser(description="Convert temperatures.")
parser.add_argument("value", type=float, help="the temperature to convert")
parser.add_argument("--to", choices=["c", "f"], required=True, help="target scale")
parser.add_argument("--precision", type=int, default=1, help="decimal places")


def convert(argv):
    args = parser.parse_args(argv)
    if args.to == "f":
        result = args.value * 9 / 5 + 32
    else:
        result = (args.value - 32) * 5 / 9
    return f"{result:.{args.precision}f}°{args.to.upper()}"


print(convert(["100", "--to", "f"]))
print(convert(["212", "--to", "c", "--precision", "3"]))''',
                   expect="""212.0°F
100.000°C""")
              + "<p>Note <code>{{result:.{{args.precision}}f}}</code>: an f-string can compute "
              "its own format spec from a variable. Genuinely useful and not widely known.</p>")}

    {exercise(2, "Design a CLI on paper",
              "<p>You are building a tool that backs up a folder. Write out the "
              "<code>--help</code> output you would want <em>before</em> writing any code. "
              "What arguments does it need?</p>",
              term("""usage: backup [-h] [--dest DEST] [--exclude PATTERN] [--dry-run]
              [--compress] [-v] source

Back up a folder, skipping anything you tell it to.

positional arguments:
  source              the folder to back up

options:
  -h, --help          show this help message and exit
  --dest DEST         where to put the backup (default: ./backups)
  --exclude PATTERN   glob to skip, may be given several times
  --dry-run           show what would happen, change nothing
  --compress          write a .zip instead of a folder
  -v, --verbose       list every file as it is copied""")
              + "<p>Designing the interface first is a real technique, sometimes called "
              "README-driven development. <code>--dry-run</code> in particular is the mark of "
              "a considerate tool: anything that deletes or overwrites should offer a way to "
              "preview it, and you will thank yourself the first time you point it at the "
              "wrong folder.</p>")}

    {exercise(3, "Make it testable",
              "<p>Why does <code>def main(argv=None)</code> matter, and how would you test the "
              "tool without running it from a terminal?</p>",
              code('''import argparse


def build_parser():
    p = argparse.ArgumentParser()
    p.add_argument("name")
    p.add_argument("--times", type=int, default=1)
    return p


def main(argv=None):
    """argv=None means 'read the real command line', but tests can pass a list."""
    args = build_parser().parse_args(argv)
    return [f"Hello, {args.name}!" for _ in range(args.times)]


# a test, with no terminal involved at all
assert main(["Guybrush"]) == ["Hello, Guybrush!"]
assert len(main(["Elaine", "--times", "3"])) == 3
print("both assertions passed")''',
                   expect="both assertions passed")
              + "<p>With <code>argv=None</code>, argparse falls back to "
              "<code>sys.argv[1:]</code> in real use, and your tests hand it a list instead. "
              "Same code path, no subprocess, no fixtures. Lesson 29 turns those "
              "<code>assert</code> lines into a proper test suite.</p>")}
""",
)

# ---------------------------------------------------------------- 28
_add(
    level=3,
    num="28",
    slug="28-debugging",
    id="py-28-debugging",
    card="print, breakpoint, and logging: three tools, and knowing which one you need.",
    title="Debugging and Logging",
    emoji="🔦",
    desc="Systematic debugging, the built-in debugger, and replacing print with the logging module.",
    lede="""Lesson 10 taught you to read an error. This one is about the harder case: the
    program runs perfectly and produces the wrong answer.""",
    body=f"""
    <h2>The method, restated</h2>
    <p>
      A bug is always the same thing: a gap between what you believe and what is true. The
      whole job is finding which belief is wrong, and the fastest route is not to stare
      harder, it is to make beliefs visible and test them one at a time.
    </p>
    <ol class="steps">
      <li><strong>Reproduce it reliably.</strong> A bug you cannot trigger on demand cannot be
      fixed, only guessed at. Get it down to the smallest input that shows the problem.</li>
      <li><strong>State the belief.</strong> "At line 14, <code>total</code> should be 47."</li>
      <li><strong>Check it.</strong> Print it, or stop there with a debugger.</li>
      <li><strong>Halve the search space.</strong> If the belief was right, the bug is
      downstream. If it was wrong, it is upstream. Repeat.</li>
      <li><strong>Fix, then prove.</strong> Write a test that fails before your fix and passes
      after (Lesson 29). Otherwise it will come back.</li>
    </ol>

    <h2>Level 1: better prints</h2>
    {code('''def parse_row(row):
    parts = row.split(",")
    print(f"{row=}")
    print(f"{parts=}")
    print(f"{len(parts)=}")
    return {"name": parts[0], "pay": int(parts[1])}


print(parse_row("Guybrush, 100"))''',
          expect="""row='Guybrush, 100'
parts=['Guybrush', ' 100']
len(parts)=2
{'name': 'Guybrush', 'pay': 100}""")}

    {voice("PERCEPTION", "Formidable: Success",
           "Look at the second field: ' 100', with a space in front of it. int() happens to "
           "tolerate that, so this row parsed fine and you learned nothing.",
           "Now imagine the field were a name and you compared it with ==. ' Otis' is not "
           "'Otis', and the comparison fails for a reason that is completely invisible when "
           "you print the value on its own. This is why the debugging print shows repr, with "
           "the quotes, rather than the bare text.")}

    <p>
      That <code>{{variable=}}</code> form inside an f-string is the fastest debugging tool
      Python has. It prints the name, the value, and (because it uses <code>repr</code>) the
      quotes and escapes that reveal stray whitespace. Three keystrokes, and it has ended more
      mysteries than any debugger.
    </p>
    <p>Two other print upgrades worth knowing:</p>
    {code('''import sys

print("this goes to stderr, so it does not pollute piped output", file=sys.stderr)
print("flushed immediately, useful when a program is about to crash", flush=True)''',
          expect="""this goes to stderr, so it does not pollute piped output
flushed immediately, useful when a program is about to crash""")}

    <h2>Level 2: the built-in debugger</h2>
    {code('''def calculate_total(prices, discount):
    total = sum(prices)
    # breakpoint()          # uncomment and run this in a terminal
    final = total * (1 - discount)
    return round(final, 2)


print(calculate_total([10.00, 24.99, 5.50], 0.1))''',
          expect="36.44")}
    <p>
      Put <code>breakpoint()</code> on a line and run the program in a terminal. Execution
      stops there and hands you a prompt where you can inspect anything:
    </p>
    {repl("""(Pdb) total
40.49
(Pdb) discount
0.1
(Pdb) total * (1 - discount)
36.441
(Pdb) prices
[10.0, 24.99, 5.5]
(Pdb) n          # run the next line
(Pdb) c          # continue to the end
(Pdb) q          # quit""")}
    {table(
        ["Command", "Does"],
        [["<code>n</code> (next)", "Run this line, stay in this function"],
         ["<code>s</code> (step)", "Run this line, step <em>into</em> any function it calls"],
         ["<code>c</code> (continue)", "Run until the next breakpoint or the end"],
         ["<code>l</code> (list)", "Show where you are in the source"],
         ["<code>p x</code>", "Print x"],
         ["<code>pp x</code>", "Pretty-print x"],
         ["<code>w</code> (where)", "Show the call stack"],
         ["<code>q</code> (quit)", "Stop"]],
    )}
    <p>
      <code>breakpoint()</code> has been built in since Python 3.7 and needs no import. Your
      editor has a graphical version of the same thing, and in VS Code it is the F5 key. Both
      beat printing when the state is complicated, because you can ask questions you did not
      think of in advance.
    </p>

    <h2>Level 3: logging, for programs that outlive the terminal</h2>
    {code('''import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(message)s",
)

log = logging.getLogger("crew")

log.debug("this will not appear, the level is INFO")
log.info("loaded 3 crew members")
log.warning("no ship assigned")
log.error("could not open manifest")
log.critical("hull breach")''',
          expect="""INFO     loaded 3 crew members
WARNING  no ship assigned
ERROR    could not open manifest
CRITICAL hull breach""")}
    <p>Why this beats <code>print</code> for anything real:</p>
    <ul>
      <li><strong>Levels.</strong> Turn detail up or down without editing code. Run at DEBUG
      while investigating, WARNING in production.</li>
      <li><strong>Destinations.</strong> The same calls can go to the screen, a file, a rotating
      set of files, or a central log service, decided by configuration.</li>
      <li><strong>Context for free.</strong> Timestamps, module names, line numbers, process
      ids.</li>
      <li><strong>It can be left in.</strong> Debug prints get deleted, then re-added the next
      time. Log lines stay, and are there at 3am when the thing breaks and you cannot
      reproduce it.</li>
    </ul>
    {code('''import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(name)-8s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)

log = logging.getLogger("ship")


def load_crew(names):
    log.debug("loading %d names", len(names))
    for name in names:
        if not name.strip():
            log.warning("skipping an empty name")
            continue
        log.info("added %s", name)
    return [n for n in names if n.strip()]


crew = load_crew(["Guybrush", "", "Elaine"])
log.info("finished with %d crew", len(crew))''',
          run=False, verify="compile")}
    {callout("tip", "🔤 Use %s, not an f-string, in log calls",
             "<p><code>log.info(\"added %s\", name)</code> rather than "
             "<code>log.info(f\"added {{name}}\")</code>. The formatting is then only done if "
             "the message is actually going to be emitted, which matters when a debug line "
             "sits inside a hot loop and the level is set to WARNING.</p>")}

    <h2>Logging exceptions properly</h2>
    {code('''import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
log = logging.getLogger("vault")


def open_vault(combination):
    try:
        return 100 / combination
    except ZeroDivisionError:
        log.exception("could not open the vault")
        return None


print(open_vault(0))''',
          run=False, verify="compile")}
    <p>
      <code>log.exception(...)</code> inside an <code>except</code> block records your message
      <em>and</em> the full traceback. It is the single most useful logging call there is, and
      it is why "an error occurred" appears in so many useless log files: somebody used
      <code>log.error</code> and threw the traceback away.
    </p>

    <h2>Bugs that are not in your code</h2>
    {table(
        ["Symptom", "Very often"],
        [["Works alone, fails in a loop", "Shared mutable state, or a leftover variable from the previous iteration"],
         ["Works on your machine only", "A file path, an environment variable, or a package version"],
         ["Fails only sometimes", "Ordering, timing, or something depending on a set or dictionary you assumed was ordered"],
         ["Broke after an update", "A dependency changed. <code>pip freeze</code> and compare"],
         ["Wrong by exactly one", "An off-by-one: a range end, or counting from 1 instead of 0"],
         ["Changes when you add a print", "Timing or buffering. Usually threads (Lesson 39)"]],
    )}

    {exercise(1, "Find the bug by halving",
              "<p>This should give each pirate an equal share of the treasure, rounded down, "
              "with the remainder going to the captain. It does not. Find out why, without "
              "just reading it: add prints and narrow it down.</p>"
              + code('''def divide_treasure(total, crew):
    share = total // len(crew)
    remainder = total - share * len(crew)
    payouts = {}
    for member in crew:
        payouts[member] = share
    payouts[crew[0]] = remainder
    return payouts


print(divide_treasure(100, ["Guybrush", "Elaine", "Otis"]))''', run=False, verify="compile"),
              "<p>The captain's line <em>replaces</em> their share instead of adding to it, so "
              "Guybrush gets 1 instead of 34.</p>"
              + code('''def divide_treasure(total, crew):
    """Split total evenly, with any remainder going to crew[0]."""
    share = total // len(crew)
    remainder = total - share * len(crew)
    payouts = {member: share for member in crew}
    payouts[crew[0]] += remainder
    return payouts


result = divide_treasure(100, ["Guybrush", "Elaine", "Otis"])
print(result)
print("total paid out:", sum(result.values()))''',
                     expect="""{'Guybrush': 34, 'Elaine': 33, 'Otis': 33}
total paid out: 100""")
              + "<p>Note the second print. Checking that the parts add up to the whole is an "
              "<strong>invariant</strong>, and asserting invariants is how you catch this "
              "class of bug automatically instead of by eye.</p>")}

    {exercise(2, "Replace prints with logging",
              "<p>Convert this debug-print-riddled function into one that uses logging at "
              "sensible levels.</p>"
              + code('''def process(orders):
    print("starting")
    for order in orders:
        print("processing", order)
        if order["total"] < 0:
            print("BAD ORDER!", order)
            continue
        print("ok")
    print("done")''', run=False, verify="compile"),
              code('''import logging

log = logging.getLogger(__name__)


def process(orders):
    """Process each order, skipping any with a negative total."""
    log.info("processing %d orders", len(orders))
    processed = 0

    for order in orders:
        log.debug("order %s", order)
        if order["total"] < 0:
            log.warning("skipping order %s: negative total %s", order["id"], order["total"])
            continue
        processed += 1

    log.info("finished: %d of %d processed", processed, len(orders))
    return processed


logging.basicConfig(level=logging.INFO, format="%(levelname)-8s %(message)s")
process([{"id": 1, "total": 10}, {"id": 2, "total": -5}])''',
                   expect="""INFO     processing 2 orders
WARNING  skipping order 2: negative total -5
INFO     finished: 1 of 2 processed""")
              + "<p>Notice the levels carry meaning now: the per-order detail is DEBUG and "
              "invisible by default, the skipped order is a WARNING you would want to see, and "
              "the summary is INFO. Same information, and you can now choose how much of it "
              "you want without editing the file.</p>")}

    {exercise(3, "Practise with the debugger",
              "<p>On your own machine, save this and run it. Use <code>breakpoint()</code> to "
              "find out why the average is wrong.</p>"
              + code('''def average(numbers):
    total = 0
    for n in numbers:
        total += n
    breakpoint()
    return total / len(numbers) - 1


print(average([10, 20, 30]))''', run=False, verify="compile"),
              "<p>At the prompt, <code>total</code> shows 60 and "
              "<code>total / len(numbers)</code> shows 20.0, which is correct. So the bug is "
              "in the line you have not run yet: a stray <code>- 1</code>.</p>"
              "<p>The lesson is the workflow, not the bug. You confirmed where the value was "
              "still right, which meant the fault had to be downstream of that point. Two "
              "questions, one bug found, no guessing.</p>")}
""",
)

# ---------------------------------------------------------------- 29
_add(
    level=3,
    num="29",
    slug="29-testing",
    id="py-29-testing",
    card="Prove your code works, automatically, forever. The habit that changes everything.",
    title="Testing",
    emoji="🧪",
    desc="assert, unittest, pytest, what makes a good test, and test-driven development in practice.",
    lede="""Testing sounds like homework. It is actually the thing that lets you change code
    without fear, and fear of changing code is what kills projects.""",
    body=f"""
    <h2>You are already testing</h2>
    <p>
      Every time you run your program and look at the output, you are testing. The problem is
      that you do it by hand, only for the thing you just changed, and you stop doing it when
      you are tired. Automated tests are the same checks, written down once, run in a second,
      forever.
    </p>

    <h2>The simplest possible test</h2>
    {code('''def add(a, b):
    return a + b


assert add(2, 3) == 5
assert add(-1, 1) == 0
assert add(0, 0) == 0

print("all assertions passed")''',
          expect="all assertions passed")}
    <p>
      <code>assert</code> does nothing when the condition is true and raises
      <code>AssertionError</code> when it is false. That is genuinely a test suite. It is just
      one that stops at the first failure and tells you very little.
    </p>

    <h2>pytest: the one everybody uses</h2>
    <p>Put this in <code>test_maths.py</code>:</p>
    {code('''def add(a, b):
    return a + b


def test_add_positive():
    assert add(2, 3) == 5


def test_add_negative():
    assert add(-1, -1) == -2


def test_add_zero():
    assert add(5, 0) == 5''',
          run=False, verify="compile")}
    <p>Then run <code>pytest</code>:</p>
    {term("""$ pip install pytest
$ pytest -v

test_maths.py::test_add_positive PASSED                    [ 33%]
test_maths.py::test_add_negative PASSED                    [ 66%]
test_maths.py::test_add_zero PASSED                        [100%]

============= 3 passed in 0.01s =============""")}
    <p>
      The rules are minimal: files named <code>test_*.py</code>, functions named
      <code>test_*</code>, plain <code>assert</code>. No classes, no special methods, no
      boilerplate. That is why pytest won.
    </p>

    <h2>What a failure looks like</h2>
    {term("""$ pytest

    def test_add_positive():
>       assert add(2, 3) == 6
E       assert 5 == 6
E        +  where 5 = add(2, 3)

test_maths.py:6: AssertionError
============= 1 failed, 2 passed in 0.02s =============""")}
    <p>
      pytest rewrites your assertions so the failure shows both sides and what produced them.
      This is the feature that makes it pleasant rather than a chore.
    </p>

    <h2>unittest, which needs no install</h2>
    {code('''import unittest


def add(a, b):
    return a + b


class TestAdd(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_negative(self):
        self.assertEqual(add(-1, -1), -2)

    def test_raises_on_text(self):
        with self.assertRaises(TypeError):
            add(1, "two")


import io

suite = unittest.TestLoader().loadTestsFromTestCase(TestAdd)
runner = unittest.TextTestRunner(stream=io.StringIO())     # keep the report quiet
result = runner.run(suite)

print("tests run:", result.testsRun)
print("failures:", len(result.failures))
print("errors:", len(result.errors))''',
          expect="""tests run: 3
failures: 0
errors: 0""")}
    <p>
      <code>unittest</code> is in the standard library, so it needs nothing installed. It is
      more verbose (classes, <code>self.assertEqual</code> instead of <code>assert</code>) and
      it is what you will find in older codebases. Learn pytest, recognise unittest.
    </p>

    <h2>What to actually test</h2>
    {code('''def apply_discount(price, percent):
    """Reduce price by percent. Percent must be 0-100."""
    if not 0 <= percent <= 100:
        raise ValueError(f"percent must be 0-100, got {percent}")
    return round(price * (1 - percent / 100), 2)


# the normal case
assert apply_discount(100, 10) == 90.0

# the boundaries, where bugs live
assert apply_discount(100, 0) == 100.0
assert apply_discount(100, 100) == 0.0

# the awkward reality
assert apply_discount(0, 50) == 0.0
assert apply_discount(19.99, 33) == 13.39

# and that it refuses bad input
for bad in [-1, 101]:
    try:
        apply_discount(100, bad)
        raise SystemExit("should have raised!")
    except ValueError:
        pass

print("every case passed")''',
          expect="every case passed")}
    <p>
      The pattern to internalise: <strong>normal case, boundaries, and failure</strong>. Most
      bugs live at the edges, at zero, at one, at empty, at the last element, and at the input
      nobody expected. A test that only covers the happy path is a test that will pass while
      your program is broken.
    </p>

    {voice("VOLITION", "Formidable: Success",
           "Here is the argument that actually convinces people, and it is not about "
           "correctness.",
           "Without tests, every change is frightening, so you make small timid changes and "
           "the code slowly rots around the parts you dare not touch. With tests, you can "
           "restructure something at 5pm on a Friday, run one command, and know. Tests do not "
           "buy you correctness so much as they buy you courage.")}

    <h2>Parametrising: many cases, one test</h2>
    {code('''import pytest


def is_even(n):
    return n % 2 == 0


@pytest.mark.parametrize("number,expected", [
    (2, True),
    (3, False),
    (0, True),
    (-4, True),
    (-3, False),
])
def test_is_even(number, expected):
    assert is_even(number) is expected''',
          run=False, verify="compile")}
    <p>
      That is five separate tests, each reported individually, from one function. When one
      fails you are told exactly which input broke it.
    </p>

    <h2>Fixtures: shared setup</h2>
    {code('''import pytest


@pytest.fixture
def crew():
    """A fresh crew list for each test that asks for one."""
    return ["Guybrush", "Elaine", "Otis"]


def test_crew_size(crew):
    assert len(crew) == 3


def test_adding_does_not_leak(crew):
    crew.append("Meathook")
    assert len(crew) == 4


def test_still_three(crew):
    # the fixture ran again, so this list is untouched
    assert len(crew) == 3''',
          run=False, verify="compile")}
    <p>
      A test that depends on another test having run first is a broken test. Fixtures give each
      one a clean slate. pytest also ships <code>tmp_path</code>, which hands you a fresh
      temporary directory, so file-touching code can be tested without leaving a mess.
    </p>

    <h2>Test-driven development, briefly</h2>
    <p>Write the test first, watch it fail, then make it pass. Red, green, refactor.</p>
    {code('''# 1. RED: the test, before any implementation
def test_initials():
    assert initials("guybrush ulysses threepwood") == "G.U.T."


# 2. GREEN: the simplest thing that passes
def initials(full_name):
    return ".".join(part[0].upper() for part in full_name.split()) + "."


test_initials()
print("green")

# 3. REFACTOR: now handle the edge case the test made you think about
def initials(full_name):
    """Return dotted initials, or an empty string for empty input."""
    parts = full_name.split()
    if not parts:
        return ""
    return ".".join(part[0].upper() for part in parts) + "."


assert initials("") == ""
assert initials("elaine marley") == "E.M."
print("still green, and now it survives an empty name")''',
          expect="""green
still green, and now it survives an empty name""")}
    <p>
      The real benefit of writing the test first is not discipline, it is design: you are
      forced to decide what the function is called, what it takes and what it returns before
      you can hide those decisions inside an implementation.
    </p>

    <h2>How much testing is enough?</h2>
    <ul>
      <li><strong>Test the logic, not the language.</strong> You do not need a test proving
      that <code>+</code> adds.</li>
      <li><strong>Test anything you got wrong once.</strong> Every bug you fix deserves a test
      that would have caught it. This is the highest-value test you will ever write.</li>
      <li><strong>Test the edges.</strong> Empty, zero, one, negative, huge, missing, wrong
      type.</li>
      <li><strong>Do not chase 100% coverage.</strong> Coverage tells you what was executed,
      not what was checked. It is a smoke detector, not a safety certificate.</li>
      <li><strong>Fast tests get run.</strong> A suite that takes ten minutes gets skipped, and
      a skipped test protects nothing.</li>
    </ul>

    {exercise(1, "Test a function properly",
              "<p>Here is a function. Write assertions covering the normal case, the "
              "boundaries, and the failure. Find the bug it contains.</p>"
              + code('''def grade(score):
    if score > 90:
        return "A"
    elif score > 80:
        return "B"
    elif score > 70:
        return "C"
    return "F"''', run=False, verify="compile"),
              "<p>The bug is <code>&gt;</code> where it should be <code>&gt;=</code>: exactly "
              "90 gets a B, and exactly 70 gets an F. Boundary tests find this instantly; "
              "testing 85 and 95 never would.</p>"
              + code('''def grade(score):
    """Convert a percentage to a letter grade. Boundaries are inclusive."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    return "F"


# normal
assert grade(95) == "A"
assert grade(85) == "B"
assert grade(50) == "F"

# boundaries: this is where the bug was
assert grade(90) == "A"
assert grade(80) == "B"
assert grade(70) == "C"
assert grade(69) == "F"

# extremes
assert grade(0) == "F"
assert grade(100) == "A"

print("all 9 assertions passed")''', expect="all 9 assertions passed"))}

    {exercise(2, "Write the test first",
              "<p>Do it properly: write tests for a <code>word_frequencies(text)</code> "
              "function <em>before</em> writing it. Decide what it should do about case and "
              "punctuation by writing the assertion.</p>",
              code('''# The tests, written first. These are decisions, not checks.
def check(word_frequencies):
    assert word_frequencies("") == {}
    assert word_frequencies("hi") == {"hi": 1}
    assert word_frequencies("hi hi") == {"hi": 2}
    assert word_frequencies("Hi hi") == {"hi": 2}          # case insensitive
    assert word_frequencies("hi, hi!") == {"hi": 2}        # punctuation ignored
    return "all passed"


# Now the implementation has no choice but to satisfy them.
from collections import Counter


def word_frequencies(text):
    """Count words, ignoring case and surrounding punctuation."""
    words = [w.strip(".,!?;:\\"'") .lower() for w in text.split()]
    return dict(Counter(w for w in words if w))


print(check(word_frequencies))''',
                   expect="all passed")
              + "<p>Notice how the fourth and fifth assertions are design decisions you had to "
              "make consciously. Written after the fact, you would probably have tested "
              "whatever the code happened to do.</p>")}

    {exercise(3, "Why is this test bad?",
              "<p>Three problems.</p>"
              + code('''import datetime


def test_everything():
    result = process_orders(load_orders("/Users/chris/data/orders.csv"))
    assert result
    assert result["date"] == datetime.date.today()''', run=False, verify="compile"),
              "<ol><li><strong>It tests everything at once.</strong> When it fails you know "
              "nothing about which part broke. One test, one behaviour.</li>"
              "<li><strong>It depends on the outside world:</strong> a hard-coded path on one "
              "person's machine. It will fail for everyone else and in CI. Use pytest's "
              "<code>tmp_path</code> and build the input inside the test.</li>"
              "<li><strong><code>assert result</code> asserts almost nothing</strong> (any "
              "non-empty value passes), and comparing to <code>today()</code> makes the test "
              "depend on the clock. It will pass today and fail if it runs at midnight. Pass "
              "the date in as an argument instead: functions that take their dependencies as "
              "arguments are the ones that are easy to test.</li></ol>"
              "<p>That last point is the deepest one in this lesson. Code that is hard to test "
              "is usually badly designed, and the difficulty is the message.</p>")}
""",
)

# ---------------------------------------------------------------- 30
_add(
    level=3,
    num="30",
    slug="30-style",
    id="py-30-style",
    card="PEP 8, ruff, black, and type hints: making code that other people (and tools) can read.",
    title="Style, Linting and Type Hints",
    emoji="🎨",
    desc="PEP 8, automatic formatting with black or ruff, linting, and an introduction to type hints.",
    lede="""Working code is the first goal. Code that a stranger can change without breaking
    it is the real one, and most of the way there is automatic.""",
    body=f"""
    <h2>PEP 8, the shared agreement</h2>
    <p>
      {link("PEP 8", "https://peps.python.org/pep-0008/")} is Python's official style guide,
      written in 2001 and followed almost universally. Its value is not that its choices are
      objectively best; it is that everybody made the same choices, so you can read anyone's
      code without adjusting.
    </p>
    {table(
        ["Rule", "Yes", "No"],
        [["Four spaces per indent, never tabs", "<code>    x = 1</code>", "a tab character"],
         ["snake_case for variables and functions", "<code>total_pay</code>", "<code>totalPay</code>"],
         ["CapWords for classes", "<code>class ShipLog:</code>", "<code>class ship_log:</code>"],
         ["ALL_CAPS for constants", "<code>MAX_CREW = 12</code>", "<code>maxCrew = 12</code>"],
         ["Spaces around operators", "<code>x = a + b</code>", "<code>x=a+b</code>"],
         ["No space inside brackets", "<code>f(a, b)</code>", "<code>f( a, b )</code>"],
         ["Two blank lines between top-level functions", "", ""],
         ["Lines under 88 characters or so", "", "a 200 character line"],
         ["Imports at the top, one per line, grouped", "", "<code>import os, sys</code>"]],
    )}

    <h2>Stop arguing: let a tool do it</h2>
    {code('''# before
def  calc( a,b ):
    result=a+b
    if result>10 :
        return  "big"
    else :
        return "small"

print(calc(5,6))''',
          expect="big")}
    <p>Run a formatter over that and it becomes:</p>
    {code('''def calc(a, b):
    result = a + b
    if result > 10:
        return "big"
    else:
        return "small"


print(calc(5, 6))''',
          expect="big")}
    {term("""# the two options, either is fine
pip install black && black .

pip install ruff && ruff format .""")}
    <p>
      Both reformat your entire project in under a second and have almost no configuration on
      purpose. {link("black", "https://black.readthedocs.io")} calls itself "the uncompromising
      formatter" and its central insight is that the fastest way to end a style argument is to
      remove the choice. {link("ruff", "https://docs.astral.sh/ruff/")} does the same job (and
      linting too) and is written in Rust, which is why it is fast enough to run on every
      keystroke.
    </p>
    {callout("tip", "⚙️ Set format-on-save and never think about it again",
             "<p>VS Code: install the Ruff or Black extension, then Settings, search 'format on "
             "save', tick it. From that moment your code is correctly formatted forever and "
             "you have stopped spending attention on it.</p>")}

    <h2>Linting: the tool that reads your code critically</h2>
    <p>
      A formatter fixes how code looks. A <strong>linter</strong> points out things that look
      like mistakes: unused imports, variables assigned but never used, shadowed built-ins,
      comparisons that are always true.
    </p>
    {term("""$ ruff check .

app.py:1:8: F401 [*] `os` imported but unused
app.py:12:5: F841 Local variable `total` is assigned to but never used
app.py:20:1: E741 Ambiguous variable name: `l`
app.py:34:12: SIM108 Use ternary operator instead of if-else block

Found 4 errors.
[*] 1 fixable with the `--fix` option.""")}
    <p>
      Nearly all of those are real bugs in embryo. An unused import means you deleted the code
      that needed it; an assigned-but-unused variable very often means you typed the name
      slightly differently on the line that uses it.
    </p>

    <h2>Type hints</h2>
    {code('''def greet(name: str, times: int = 1) -> str:
    """Greet someone, possibly repeatedly."""
    return " ".join([f"Hello, {name}!"] * times)


print(greet("Guybrush"))
print(greet("Elaine", 2))
print(greet.__annotations__)''',
          expect="""Hello, Guybrush!
Hello, Elaine! Hello, Elaine!
{'name': <class 'str'>, 'times': <class 'int'>, 'return': <class 'str'>}""")}

    {callout("warn", "🎭 Python does not enforce them",
             "<p><code>greet(42)</code> runs perfectly happily and returns "
             "<code>'Hello, 42!'</code>. Type hints are documentation that tools can read, not "
             "a runtime check. This surprises people coming from Java or Rust, where the "
             "compiler refuses.</p>")}

    <p>So why bother? Three excellent reasons:</p>
    <ul>
      <li><strong>Your editor gets smarter.</strong> Autocomplete knows what methods exist, and
      it underlines <code>name.uppr()</code> before you run anything.</li>
      <li><strong>A checker can prove things.</strong>
      {link("mypy", "https://mypy-lang.org")} reads your whole project and finds type errors
      without running it. On a large codebase this catches real bugs in code paths nobody has
      exercised yet.</li>
      <li><strong>They are the best documentation there is,</strong> because they cannot drift
      out of date silently the way a comment can.</li>
    </ul>

    <h2>The notation you need</h2>
    {code('''def process(
    names: list[str],
    scores: dict[str, int],
    limit: int | None = None,
    tags: tuple[str, ...] = (),
) -> list[tuple[str, int]]:
    """Pair names with scores, optionally limited."""
    pairs = [(n, scores.get(n, 0)) for n in names]
    return pairs[:limit] if limit else pairs


print(process(["Guybrush", "Elaine"], {"Guybrush": 95}, limit=1))''',
          expect="[('Guybrush', 95)]")}
    {table(
        ["Hint", "Means"],
        [["<code>str</code>, <code>int</code>, <code>float</code>, <code>bool</code>", "The obvious ones"],
         ["<code>list[str]</code>", "A list of strings"],
         ["<code>dict[str, int]</code>", "String keys, integer values"],
         ["<code>tuple[str, int]</code>", "Exactly two items, in that order"],
         ["<code>tuple[str, ...]</code>", "Any number of strings"],
         ["<code>int | None</code>", "Either an int or None (the modern way, 3.10+)"],
         ["<code>-&gt; None</code>", "Returns nothing"],
         ["<code>Any</code>", "Give up (from <code>typing</code>). Use sparingly"]],
    )}

    <h2>What mypy catches</h2>
    {code('''def total_price(items: list[float]) -> float:
    return sum(items)


# mypy reports: Argument 1 has incompatible type "list[str]";
#               expected "list[float]"
result = total_price(["12.50", "3.99"])''',
          run=False, verify="skip")}
    {term("""$ mypy shop.py
shop.py:7: error: Argument 1 to "total_price" has incompatible type
    "list[str]"; expected "list[float]"  [arg-type]
Found 1 error in 1 file (checked 1 source file)""")}
    <p>
      That program runs without hints and produces <code>'12.503.99'</code>, a string, which
      then breaks something else three functions away. mypy found it in a second without
      running anything.
    </p>

    <h2>How much of this to adopt</h2>
    {table(
        ["Situation", "Advice"],
        [["A twenty-line script for yourself", "A formatter. That is all"],
         ["A project you will still be using next year", "Formatter, linter, and hints on the public functions"],
         ["Anything with other people in it", "All of the above, running automatically in CI"],
         ["A library other people import", "All of the above plus hints everywhere, since they are your documentation"]],
    )}

    {voice("RHETORIC", "Medium: Success",
           "There is a failure mode at both ends. One is the codebase with no conventions, "
           "where every file is a different dialect and reading it is exhausting.",
           "The other is the team that spends three weeks configuring linters and arguing "
           "about line length instead of shipping. Turn on the defaults, accept them, and go "
           "back to work. The defaults are fine. That is the entire point of defaults.")}

    <h2>One config file</h2>
    {code('''# pyproject.toml
[project]
name = "crew-manager"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["requests>=2.31"]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.mypy]
python_version = "3.13"
warn_unused_ignores = true

[tool.pytest.ini_options]
testpaths = ["tests"]''',
          run=False, verify="skip")}
    <p>
      <code>pyproject.toml</code> is the modern single home for project configuration:
      packaging, formatting, linting, type checking and testing all in one file. Lesson 50
      uses it to publish a package.
    </p>

    {exercise(1, "Clean it up",
              "<p>Fix everything PEP 8 would complain about, and name each problem.</p>"
              + code('''import os, sys
def CalcTotal( Items ):
    Total=0
    for i in Items :
        Total=Total+i
    if Total>100 :
        return Total*0.9
    else :
        return Total
print(CalcTotal([50,60]))''', run=False, verify="compile"),
              "<p>Problems: two imports on one line and both unused; CapWords function name; "
              "CapWords variable names; no spaces around operators; spaces inside brackets; "
              "space before the colon; no blank lines around the function; the "
              "<code>else</code> after a <code>return</code> is redundant.</p>"
              + code('''def calculate_total(items: list[float]) -> float:
    """Sum the items, applying a 10 percent discount over 100."""
    total = sum(items)
    if total > 100:
        return total * 0.9
    return total


print(calculate_total([50, 60]))''', expect="99.0"))}

    {exercise(2, "Add type hints",
              "<p>Annotate this fully, including the return type.</p>"
              + code('''def find_best(scores, minimum=0):
    best_name = None
    best_score = minimum
    for name, score in scores.items():
        if score > best_score:
            best_name, best_score = name, score
    return best_name, best_score''', run=False, verify="compile"),
              code('''def find_best(
    scores: dict[str, int],
    minimum: int = 0,
) -> tuple[str | None, int]:
    """Return the highest scorer above minimum, or (None, minimum)."""
    best_name: str | None = None
    best_score = minimum
    for name, score in scores.items():
        if score > best_score:
            best_name, best_score = name, score
    return best_name, best_score


print(find_best({"Guybrush": 95, "Otis": 42}))
print(find_best({"Otis": 42}, minimum=50))''',
                   expect="""('Guybrush', 95)
(None, 50)""")
              + "<p>The interesting part is <code>str | None</code> in the return type. Writing "
              "it forces you to notice that this function can return None, which is exactly "
              "the sort of thing callers forget to handle.</p>")}

    {exercise(3, "Set up a real project",
              "<p>On your own machine, in a project folder, install and run the whole toolchain "
              "once. Look at what each tool says.</p>",
              term("""python3 -m venv .venv && source .venv/bin/activate
pip install ruff mypy pytest

ruff format .          # reformat everything
ruff check . --fix     # fix what can be fixed automatically
mypy .                 # type check
pytest                 # run the tests

# and the one command that does all of it before you commit
ruff format . && ruff check . && mypy . && pytest""")
              + "<p>That last line is what a continuous integration pipeline runs. When it "
              "passes locally, it passes in CI, and you stop discovering problems after "
              "pushing. Lesson 50 wires it into GitHub Actions so it runs automatically.</p>")}

    {callout("info", "🎉 That is Level 3",
             "<p>Files, exceptions, JSON and CSV, dates, regular expressions, virtual "
             "environments, command-line tools, debugging and testing, and the tooling that "
             "keeps it all readable. You can now write software rather than scripts. Take the "
             "<a href='../quiz.html'>Level 3 quiz</a>, then build something substantial in the "
             "<a href='../build/index.html'>workshop</a> before Level 4 shows you how Python "
             "programmers actually write Python.</p>")}
""",
)
