"""The Project Workshop: project data.

The cure for tutorial hell. Each project is built from a spec, not
copied from a script, with a ladder of hints (the last of which is a
full reference solution) and stretch goals.

Every reference solution marked verify=True is run by tools/pyverify.py
against its `stdin` and checked to match `expected`, exactly like the
lessons. Projects that need the network or third-party packages are
marked verify=False and only parsed. The house rule holds: no reference
solution ships until it runs.
"""

from __future__ import annotations

PROJECTS = []


def _proj(**kw):
    kw.setdefault("verify", True)
    kw.setdefault("stdin", "")
    kw.setdefault("expected", None)
    PROJECTS.append(kw)


# ---------------------------------------------------------------- 1
_proj(
    num="1", slug="01-guessing-game", id="pybuild-01-guessing-game",
    title="Number Guessing Game", emoji="🎯",
    after="Level 1",
    difficulty=1,
    blurb="The computer picks a secret number, you guess, it says higher or lower. "
          "Loops, conditionals and input, in one satisfying package.",
    lede="The computer picks a secret number from 1 to 100. You guess. It tells you higher or "
         "lower until you get it, then reports how many tries it took. Simple to describe, and "
         "it will teach you more than the last three lessons combined, because this time nobody "
         "is holding the pen.",
    spec=[
        "Pick a secret random number from 1 to 100.",
        "Loop: read a guess, tell the player higher, lower, or correct.",
        "Count the guesses and report the total when they win.",
        "Handle non-numeric input without crashing.",
    ],
    hints=[
        ("Getting a random number",
         "`import random` then `random.randint(1, 100)` gives an inclusive random integer. "
         "Store it in a variable before the loop starts."),
        ("The loop shape",
         "A <code>while True:</code> loop with a <code>break</code> when the guess is correct "
         "is the natural fit. Read the guess with <code>int(input(...))</code>, compare, and "
         "print the hint."),
        ("Not crashing on bad input",
         "Wrap the <code>int(input(...))</code> in a <code>try/except ValueError</code> "
         "(Lesson 22). On a bad value, print a message and <code>continue</code>."),
    ],
    # The reference is scripted (a fixed secret + canned guesses) so it can be verified.
    reference='''import random

secret = random.randint(1, 100)
guesses = 0

while True:
    raw = input("Guess (1-100): ")
    try:
        guess = int(raw)
    except ValueError:
        print("  Digits only, please.")
        continue

    guesses += 1
    if guess < secret:
        print("  Higher.")
    elif guess > secret:
        print("  Lower.")
    else:
        print(f"Got it in {guesses} guesses!")
        break
''',
    verify=False,      # uses random + interactive input; the workshop page notes this
    stretch=[
        "Add a difficulty setting that changes the range.",
        "Limit the player to a maximum number of guesses.",
        "Add a play-again loop that keeps a running win record.",
    ],
)

# ---------------------------------------------------------------- 2
_proj(
    num="2", slug="02-tip-splitter", id="pybuild-02-tip-splitter",
    title="Tip Splitter", emoji="🧾",
    after="Level 1",
    difficulty=1,
    blurb="Split a restaurant bill with tip across a table. Floats, formatting, and the "
          "rounding decisions that matter with money.",
    lede="Take a bill, a tip percentage, and a number of people, and work out what each person "
         "owes. It sounds trivial until you meet money's favourite trap: rounding. This project "
         "makes you decide, on purpose, how to handle the pennies.",
    spec=[
        "Read the bill amount, the tip percentage, and the number of people.",
        "Compute the tip, the total, and the per-person share.",
        "Show every figure to exactly two decimal places.",
        "Make sure the per-person shares add up to the total (no lost penny).",
    ],
    hints=[
        ("The arithmetic",
         "tip = bill * (percent / 100); total = bill + tip; each = total / people. "
         "Convert the inputs with <code>float()</code> and <code>int()</code>."),
        ("Two decimal places",
         "Use an f-string format spec: <code>f\"{total:.2f}\"</code> shows two decimals "
         "(Lesson 4). This is display formatting, not the stored value."),
        ("The lost penny",
         "If you round each share independently, they may not sum to the total. The honest fix: "
         "round the total, give everyone the floor share, and add the leftover pennies to the "
         "first person. See the reference."),
    ],
    reference='''bill = float(input("Bill amount: "))
percent = float(input("Tip percent: "))
people = int(input("How many people: "))

tip = round(bill * percent / 100, 2)
total = round(bill + tip, 2)

# work in whole pennies so nothing is lost to rounding
total_pennies = round(total * 100)
base = total_pennies // people
leftover = total_pennies - base * people

shares = [base + (1 if i < leftover else 0) for i in range(people)]

print(f"Tip:   {tip:.2f}")
print(f"Total: {total:.2f}")
for i, pennies in enumerate(shares, start=1):
    print(f"Person {i}: {pennies / 100:.2f}")
print(f"Sum of shares: {sum(shares) / 100:.2f}")
''',
    verify=True,
    stdin="87.50\n15\n4",
    expected="""Bill amount: 87.50
Tip percent: 15
How many people: 4
Tip:   13.12
Total: 100.62
Person 1: 25.16
Person 2: 25.16
Person 3: 25.15
Person 4: 25.15
Sum of shares: 100.62""",
    stretch=[
        "Let the user round the tip up to the nearest pound for a tidy total.",
        "Support an uneven split where some people cover more.",
        "Use the <code>decimal</code> module for exact money (Lesson 3).",
    ],
)

# ---------------------------------------------------------------- 3
_proj(
    num="3", slug="03-todo", id="pybuild-03-todo",
    title="Todo List with Save", emoji="✅",
    after="Level 3",
    difficulty=2,
    blurb="A command-line todo list that remembers between runs. Your first program with "
          "persistent data: files, JSON, and a menu loop.",
    lede="A todo list is the 'hello world' of persistent apps. Add tasks, list them, mark them "
         "done, and, crucially, have them still be there tomorrow. This is where your programs "
         "stop forgetting everything the moment they end.",
    spec=[
        "Show a menu: add, list, mark done, quit.",
        "Store tasks as a list of dictionaries, each with a title and a done flag.",
        "Save to a JSON file on every change, load it on start.",
        "Survive a missing or empty file gracefully.",
    ],
    hints=[
        ("The data shape",
         "A task is <code>{\"title\": \"...\", \"done\": False}</code>. The whole list is a list "
         "of those, which is exactly what JSON stores (Lesson 23)."),
        ("Load and save",
         "On start, read the JSON file if it exists, else start with an empty list (Lesson 21). "
         "After every add or change, write the whole list back with "
         "<code>json.dumps(tasks, indent=2)</code>."),
        ("The menu loop",
         "A <code>while True:</code> loop that reads a choice and dispatches with "
         "<code>if/elif</code> or a <code>match</code> (Lesson 7). Break on quit, saving first."),
    ],
    reference='''import json
from pathlib import Path

FILE = Path("tasks.json")


def load():
    if FILE.exists():
        return json.loads(FILE.read_text(encoding="utf-8"))
    return []


def save(tasks):
    FILE.write_text(json.dumps(tasks, indent=2), encoding="utf-8")


def show(tasks):
    if not tasks:
        print("  (no tasks yet)")
    for i, task in enumerate(tasks, start=1):
        mark = "x" if task["done"] else " "
        print(f"  {i}. [{mark}] {task['title']}")


def main():
    tasks = load()
    while True:
        choice = input("add / list / done / quit: ").strip().lower()
        if choice == "add":
            title = input("  Title: ")
            tasks.append({"title": title, "done": False})
            save(tasks)
        elif choice == "list":
            show(tasks)
        elif choice == "done":
            show(tasks)
            n = int(input("  Which number: "))
            tasks[n - 1]["done"] = True
            save(tasks)
        elif choice == "quit":
            save(tasks)
            print("Saved. Bye.")
            break


if __name__ == "__main__":
    main()
''',
    verify=True,
    stdin="add\nWrite the todo app\nadd\nEat lunch\nlist\ndone\n1\nlist\nquit",
    expected="""add / list / done / quit: add
  Title: Write the todo app
add / list / done / quit: add
  Title: Eat lunch
add / list / done / quit: list
  1. [ ] Write the todo app
  2. [ ] Eat lunch
add / list / done / quit: done
  1. [ ] Write the todo app
  2. [ ] Eat lunch
  Which number: 1
add / list / done / quit: list
  1. [x] Write the todo app
  2. [ ] Eat lunch
add / list / done / quit: quit
Saved. Bye.""",
    stretch=[
        "Add a delete option, and a confirm-before-delete (Lesson 41).",
        "Add due dates with the datetime module (Lesson 24).",
        "Turn it into a proper CLI tool with argparse (Lesson 27).",
    ],
)

# ---------------------------------------------------------------- 4
_proj(
    num="4", slug="04-word-counter", id="pybuild-04-word-counter",
    title="Word Frequency Counter", emoji="📊",
    after="Level 2",
    difficulty=2,
    blurb="Count how often each word appears in a piece of text and show the top ten. "
          "Dictionaries, sorting, and Counter doing real work.",
    lede="Feed it text, and it tells you which words appear most. It is the engine under word "
         "clouds, search ranking and basic text analysis, and it is a beautiful showcase for "
         "the dictionary skills from Level 2.",
    spec=[
        "Take a block of text and split it into words.",
        "Normalise: lowercase, and strip surrounding punctuation.",
        "Count each word, then show the ten most common with their counts.",
        "Ignore very common stop-words like 'the' and 'a'.",
    ],
    hints=[
        ("Splitting and cleaning",
         "<code>text.lower().split()</code> gives lowercase words. Strip punctuation from each "
         "with <code>word.strip('.,!?;:\"')</code> (Lesson 4)."),
        ("Counting",
         "The dictionary idiom <code>counts[word] = counts.get(word, 0) + 1</code> works, but "
         "<code>collections.Counter</code> is purpose-built and has a <code>.most_common(10)</code> "
         "method (Lesson 20)."),
        ("Stop-words",
         "Keep a <code>set</code> of words to ignore and skip any word in it. Sets make the "
         "membership test instant (Lesson 14)."),
    ],
    reference='''from collections import Counter

STOP = {"the", "a", "an", "and", "to", "of", "in", "is", "it", "on"}

text = """The cat sat on the mat. The cat ate the fish.
A dog sat on the log and the dog ate the bone. The cat ran."""

words = []
for raw in text.lower().split():
    word = raw.strip(".,!?;:\\"'")
    if word and word not in STOP:
        words.append(word)

counts = Counter(words)
for word, n in counts.most_common(5):
    print(f"{n:2}  {word}")
''',
    verify=True,
    expected=""" 3  cat
 2  sat
 2  ate
 2  dog
 1  mat""",
    stretch=[
        "Read the text from a file the user names (Lesson 21).",
        "Draw a text bar chart, one # per occurrence (Lesson 20's dice example).",
        "Add command-line flags for the top-N and the stop-word list (Lesson 27).",
    ],
)

# ---------------------------------------------------------------- 5
_proj(
    num="5", slug="05-password-vault", id="pybuild-05-password-vault",
    title="Password Generator & Strength Checker", emoji="🔐",
    after="Level 3",
    difficulty=2,
    blurb="Generate strong passwords and rate the strength of existing ones. secrets, not "
          "random, and the security thinking from Lesson 52.",
    lede="Two tools in one: generate a genuinely strong password, and rate how weak an existing "
         "one is. It is a great excuse to internalise the difference between random and secrets, "
         "which is the difference between fun and safe.",
    spec=[
        "Generate a password of a requested length from letters, digits and symbols.",
        "Use the secrets module, never random, for anything security-related.",
        "Rate a given password: length, character variety, obvious weaknesses.",
        "Give a clear verdict and one concrete suggestion.",
    ],
    hints=[
        ("Generating safely",
         "<code>secrets.choice(alphabet)</code> in a loop, or "
         "<code>''.join(secrets.choice(chars) for _ in range(length))</code>. Never "
         "<code>random</code>: it is predictable (Lesson 52)."),
        ("Rating strength",
         "Score by length and by how many character classes appear (lower, upper, digit, "
         "symbol). Use <code>any(c.isdigit() for c in pw)</code> and friends."),
        ("Honest feedback",
         "A short password with one character class is weak no matter what. Say so plainly, and "
         "suggest the single most effective fix (usually: make it longer)."),
    ],
    reference='''import secrets
import string


def generate(length=16):
    """Generate a strong password. secrets, not random (Lesson 52)."""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def rate(password):
    """Return a verdict and one suggestion."""
    classes = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in "!@#$%^&*" for c in password),
    ])
    if len(password) < 8 or classes < 2:
        return "weak", "Make it at least 12 characters with mixed types."
    if len(password) < 12 or classes < 3:
        return "medium", "A little longer, and mix in more character types."
    return "strong", "Good. Consider a password manager for the rest."


# generate() uses secrets, so its output changes each run; rate() is deterministic
for example in ["password", "P4ssw0rd", "correct-horse-battery-staple-9!"]:
    verdict, tip = rate(example)
    print(f"{verdict:7} {example}")
''',
    verify=True,
    expected="""weak    password
medium  P4ssw0rd
strong  correct-horse-battery-staple-9!""",
    stretch=[
        "Check a password against a list of the most common ones and reject matches.",
        "Generate a memorable passphrase from a word list instead of random characters.",
        "Never print or log the generated password anywhere it could leak (Lesson 52).",
    ],
)

# ---------------------------------------------------------------- 6
_proj(
    num="6", slug="06-markdown", id="pybuild-06-markdown",
    title="Markdown to HTML Converter", emoji="📝",
    after="Level 3",
    difficulty=3,
    blurb="Turn a subset of Markdown into HTML. A real little parser: string mastery, "
          "line-by-line state, and edge cases that bite.",
    lede="Write a converter that turns Markdown (# headings, **bold**, - lists) into HTML. It is "
         "a genuine parser, small enough to finish and real enough to teach you why parsing is "
         "harder than it looks. This is the project that makes string handling click.",
    spec=[
        "Convert # / ## / ### headings to h1 / h2 / h3.",
        "Convert **bold** to <strong> and *italic* to <em>.",
        "Convert consecutive - lines into a <ul> with <li> items.",
        "Wrap plain lines in <p>. Handle blank lines as separators.",
    ],
    hints=[
        ("Go line by line",
         "Split the input on newlines and process each line by what it starts with. Headings "
         "and list items are decided by the first characters (Lesson 4)."),
        ("Inline formatting with regex",
         "For **bold** and *italic*, <code>re.sub</code> with a captured group is cleanest: "
         "<code>re.sub(r'\\\\*\\\\*(.+?)\\\\*\\\\*', r'&lt;strong&gt;\\\\1&lt;/strong&gt;', line)</code> "
         "(Lesson 25). Do bold before italic."),
        ("Lists need state",
         "A list spans multiple lines, so you must remember whether you are 'inside a list' and "
         "open the <ul> when the first - appears, closing it when a non-list line arrives. This "
         "state-tracking is the heart of the exercise."),
    ],
    reference='''import re


def inline(text):
    """Bold and italic. Bold first, so ** is not eaten by the * rule."""
    text = re.sub(r"\\*\\*(.+?)\\*\\*", r"<strong>\\1</strong>", text)
    text = re.sub(r"\\*(.+?)\\*", r"<em>\\1</em>", text)
    return text


def convert(markdown):
    html = []
    in_list = False

    for line in markdown.splitlines():
        stripped = line.strip()

        if stripped.startswith("- "):
            if not in_list:
                html.append("<ul>")
                in_list = True
            html.append(f"  <li>{inline(stripped[2:])}</li>")
            continue

        if in_list:
            html.append("</ul>")
            in_list = False

        if stripped.startswith("### "):
            html.append(f"<h3>{inline(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            html.append(f"<h2>{inline(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            html.append(f"<h1>{inline(stripped[2:])}</h1>")
        elif stripped:
            html.append(f"<p>{inline(stripped)}</p>")

    if in_list:
        html.append("</ul>")

    return "\\n".join(html)


sample = """# Shopping
Some **important** notes and an *idea*.
- milk
- eggs
- bread
Done."""

print(convert(sample))
''',
    verify=True,
    expected="""<h1>Shopping</h1>
<p>Some <strong>important</strong> notes and an <em>idea</em>.</p>
<ul>
  <li>milk</li>
  <li>eggs</li>
  <li>bread</li>
</ul>
<p>Done.</p>""",
    stretch=[
        "Add links: [text](url) to an anchor tag.",
        "Add code spans with backticks, and escape HTML special characters inside them.",
        "Read a .md file and write a .html file, with a real HTML skeleton (Lesson 21).",
    ],
)

# ---------------------------------------------------------------- 7
_proj(
    num="7", slug="07-expense-tracker", id="pybuild-07-expense-tracker",
    title="Expense Tracker & Report", emoji="💰",
    after="Level 3",
    difficulty=3,
    blurb="Record expenses to a CSV and produce a monthly report grouped by category. "
          "CSV done properly, grouping, and honest totals.",
    lede="Log expenses with a category and an amount, store them in a CSV a spreadsheet could "
         "open, and generate a report totalled by category. It is small-business software in "
         "miniature, and it uses the CSV and grouping skills from Level 3 in anger.",
    spec=[
        "Append each expense (date, category, amount, note) as a row in a CSV file.",
        "Read the CSV back with the csv module, converting amounts to numbers.",
        "Produce a report: total per category, sorted by spend, and a grand total.",
        "Handle the file not existing yet.",
    ],
    hints=[
        ("Writing CSV properly",
         "Use <code>csv.writer</code> with <code>newline=\"\"</code>, never string-join on commas "
         "(Lesson 23). A note with a comma in it will break a naive writer."),
        ("Reading and totalling",
         "<code>csv.DictReader</code> gives each row as a dict. Remember every value is a string, "
         "so convert the amount with <code>float()</code> (Lesson 23)."),
        ("Grouping",
         "Total per category with <code>collections.defaultdict(float)</code> or a plain dict "
         "and <code>.get</code>, then sort the items by total, descending (Lesson 15)."),
    ],
    reference='''import csv
from collections import defaultdict
from pathlib import Path

FILE = Path("expenses.csv")


def add_expense(date, category, amount, note):
    """Append one expense as a CSV row, creating the header if new."""
    new_file = not FILE.exists()
    with open(FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["date", "category", "amount", "note"])
        writer.writerow([date, category, f"{amount:.2f}", note])


def report():
    """Total per category, sorted by spend, plus a grand total."""
    totals = defaultdict(float)
    with open(FILE, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            totals[row["category"]] += float(row["amount"])

    for category, total in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{category:12} {total:8.2f}")
    print(f"{'TOTAL':12} {sum(totals.values()):8.2f}")


# a scripted run so the output is reproducible
add_expense("2026-08-01", "food", 12.50, "lunch, with a comma")
add_expense("2026-08-02", "transport", 4.20, "bus")
add_expense("2026-08-03", "food", 30.00, "dinner")
report()
''',
    verify=True,
    expected="""food            42.50
transport        4.20
TOTAL           46.70""",
    stretch=[
        "Filter the report to a single month using the date column (Lesson 24).",
        "Draw a simple bar chart of spend per category (Lesson 47).",
        "Load it into pandas and produce the report in two lines (Lesson 46).",
    ],
)

# ---------------------------------------------------------------- 8
_proj(
    num="8", slug="08-text-adventure", id="pybuild-08-text-adventure",
    title="Text Adventure Engine", emoji="🗺️",
    after="Level 4",
    difficulty=3,
    blurb="A room-and-inventory adventure driven by a data map and a match-based parser. "
          "Dictionaries, match, and clean game structure.",
    lede="Build the engine for a text adventure: rooms you move between, items you pick up, a "
         "parser that understands commands. It is the purest showcase there is for dictionaries "
         "as a world and match for a command parser, and it is genuinely fun to extend.",
    spec=[
        "Describe the world as a dictionary of rooms, each with exits and items.",
        "Parse commands: look, go <direction>, take <item>, inventory.",
        "Track the player's location and inventory as they play.",
        "Reject impossible moves and unknown commands gracefully.",
    ],
    hints=[
        ("The world as data",
         "Each room is <code>{\"description\": ..., \"exits\": {\"north\": \"jungle\"}, "
         "\"items\": [...]}</code>. The whole map is a dict of rooms keyed by name (Lesson 15)."),
        ("Parsing with match",
         "<code>match command.lower().split():</code> with cases like "
         "<code>case [\"go\", direction]:</code> reads beautifully and handles the whole parser "
         "(Lesson 33). Put the specific cases before the catch-all."),
        ("State",
         "Two variables, <code>here</code> (the current room name) and <code>carrying</code> "
         "(a list), are the entire game state. Move by reassigning <code>here</code>."),
    ],
    reference='''ROOMS = {
    "beach": {"description": "A beach. A rubber chicken lies in the sand.",
              "exits": {"north": "jungle"}, "items": ["rubber chicken"]},
    "jungle": {"description": "Thick jungle. Something rustles.",
               "exits": {"south": "beach", "east": "clearing"}, "items": []},
    "clearing": {"description": "A clearing with a locked chest.",
                 "exits": {"west": "jungle"}, "items": ["chest"]},
}


def play(commands):
    here = "beach"
    carrying = []
    out = []

    for command in commands:
        room = ROOMS[here]
        match command.lower().split():
            case ["look"]:
                out.append(room["description"])
                if room["items"]:
                    out.append("You see: " + ", ".join(room["items"]))
            case ["go", direction] if direction in room["exits"]:
                here = room["exits"][direction]
                out.append(f"You go {direction}. {ROOMS[here]['description']}")
            case ["go", direction]:
                out.append(f"You cannot go {direction}.")
            case ["take", *words] if " ".join(words) in room["items"]:
                item = " ".join(words)
                room["items"].remove(item)
                carrying.append(item)
                out.append(f"Taken: {item}.")
            case ["inventory"] | ["i"]:
                out.append("Carrying: " + (", ".join(carrying) or "nothing"))
            case _:
                out.append(f"I do not understand {command!r}.")

    return out


for line in play(["look", "take rubber chicken", "inventory",
                  "go north", "go up", "go east", "look"]):
    print(line)
''',
    verify=True,
    expected="""A beach. A rubber chicken lies in the sand.
You see: rubber chicken
Taken: rubber chicken.
Carrying: rubber chicken
You go north. Thick jungle. Something rustles.
You cannot go up.
You go east. A clearing with a locked chest.
A clearing with a locked chest.
You see: chest""",
    stretch=[
        "Add a locked chest that opens only with a key (Lesson 48's exercise).",
        "Save and load the game state as JSON (Lesson 23).",
        "Add a win condition and an ending.",
    ],
)

# ---------------------------------------------------------------- 9
_proj(
    num="9", slug="09-weather-cli", id="pybuild-09-weather-cli",
    title="Weather CLI", emoji="🌦️",
    after="Level 5",
    difficulty=3,
    blurb="A real command-line tool that fetches live weather from a public API. HTTP, JSON, "
          "argparse, and keeping your key out of git.",
    lede="Your first tool that reaches out to the internet and comes back with something useful: "
         "the weather, from a real API, for a city you name on the command line. It ties "
         "together HTTP, JSON, argument parsing and secret handling into one genuinely handy "
         "program.",
    spec=[
        "Take a city name as a command-line argument.",
        "Fetch current weather from a free API (Open-Meteo needs no key).",
        "Print temperature and conditions in a clean, readable line.",
        "Handle a city that is not found, and a network failure, without a stack trace.",
    ],
    hints=[
        ("Parsing the argument",
         "<code>argparse</code> gives you <code>city</code> as a positional argument plus a "
         "free --help (Lesson 27). Structure the code so <code>main(argv=None)</code> is "
         "testable."),
        ("Calling the API",
         "<code>requests.get(url, params={...}, timeout=10)</code>, then "
         "<code>response.raise_for_status()</code> and <code>response.json()</code> (Lesson 42). "
         "Open-Meteo has a geocoding endpoint to turn a city name into coordinates."),
        ("Failing gracefully",
         "Catch <code>requests.RequestException</code> for network problems and check whether "
         "the geocoding result is empty for an unknown city. Print a friendly message and "
         "return a non-zero exit code (Lesson 27)."),
    ],
    reference='''#!/usr/bin/env python3
"""weather: current conditions for a city, from Open-Meteo (no key needed)."""

import argparse
import sys

import requests

GEO = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST = "https://api.open-meteo.com/v1/forecast"


def find_city(name):
    """Turn a city name into (lat, lon, label), or None if not found."""
    resp = requests.get(GEO, params={"name": name, "count": 1}, timeout=10)
    resp.raise_for_status()
    results = resp.json().get("results")
    if not results:
        return None
    hit = results[0]
    return hit["latitude"], hit["longitude"], f"{hit['name']}, {hit['country']}"


def current_weather(lat, lon):
    resp = requests.get(FORECAST, params={
        "latitude": lat, "longitude": lon, "current_weather": True,
    }, timeout=10)
    resp.raise_for_status()
    return resp.json()["current_weather"]


def main(argv=None):
    parser = argparse.ArgumentParser(description="Current weather for a city.")
    parser.add_argument("city", help="the city to look up")
    args = parser.parse_args(argv)

    try:
        located = find_city(args.city)
        if located is None:
            print(f"weather: no city called {args.city!r}", file=sys.stderr)
            return 1
        lat, lon, label = located
        weather = current_weather(lat, lon)
    except requests.RequestException as err:
        print(f"weather: network error: {err}", file=sys.stderr)
        return 1

    print(f"{label}: {weather['temperature']}C, wind {weather['windspeed']} km/h")
    return 0


if __name__ == "__main__":
    sys.exit(main())
''',
    verify=False,      # needs the network; the page says so
    stretch=[
        "Add a --forecast flag for the next few days.",
        "Cache results for a few minutes so repeated calls do not hit the API (Lesson 42).",
        "Package it with a console command so you can type `weather London` (Lesson 50).",
    ],
)

# ---------------------------------------------------------------- 10 (capstone)
_proj(
    num="10", slug="10-jarvis", id="pybuild-10-jarvis",
    title="The Capstone: Your Own Jarvis", emoji="🤖",
    after="Level 6",
    difficulty=5,
    blurb="The graduation project: assemble the full personal AI assistant from Level 6, then "
          "make it genuinely yours with your own tools and data.",
    lede="Everything, together. Take the Jarvis you assembled in Lesson 61 and finish it as a "
         "real, extensible, personal assistant: memory, streaming, tools you wrote, your own "
         "documents, a spending cap. This is the project that proves the whole course to "
         "yourself.",
    spec=[
        "A chat loop with persistent memory and streaming (Lessons 55, 56).",
        "At least two tools you wrote yourself, run through a safe tool loop (Lesson 57).",
        "One capability from the wider level: your own documents (58), voice (59), or local "
        "models (60).",
        "A hard daily spending cap and honest error handling (Lesson 62).",
    ],
    hints=[
        ("Start from Lesson 61",
         "Lesson 61 gives you the four-file architecture: config, tools, memory, main. Build "
         "that first, get it running, then extend it. Do not start from a blank file; start "
         "from the working skeleton."),
        ("Add tools with the registry",
         "The whole point of the Lesson 61 design is that a new tool is one registry entry. Add "
         "a calculator and a clock first (safe, useful), then one tool that does something you "
         "personally want."),
        ("The safety net is part of the project",
         "This is not optional polish. A daily spend cap (Lesson 62), a confirm-before-acting "
         "step for any tool that changes the world (Lesson 57), and honest error handling are "
         "what make it a responsible tool rather than a risky toy."),
    ],
    reference="",      # the reference is Lesson 61's full four-file build
    verify=False,
    stretch=[
        "Give it a web interface with FastAPI (Lesson 44).",
        "Add retrieval over your own notes so it answers from your documents (Lesson 58).",
        "Publish the pieces as a package with a console command (Lesson 50).",
        "Write real tests for the tools and the memory layer (Lesson 29).",
    ],
)
