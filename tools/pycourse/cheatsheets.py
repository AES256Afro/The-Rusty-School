"""Printable cheat sheets: the syntax you look up most, on one page."""

from __future__ import annotations

from .kit import SCHOOL, SITE, esc, page

NL = chr(10)


def _sheet(title: str, snippet: str) -> str:
    return (f'<div class="card"><h3>{title}</h3>'
            f'<pre><code>{esc(snippet.strip(chr(10)))}</code></pre></div>')


CARDS = [
    ("Print and f-strings", '''print("hello")
print("a", "b", sep="-")   # a-b
name, n = "Sam", 5
print(f"{name} has {n}")
print(f"{3.14159:.2f}")    # 3.14
print(f"{1000000:,}")      # 1,000,000
print(f"{n=}")             # n=5  (debug)'''),

    ("Numbers", '''7 / 2     # 3.5   float divide
7 // 2    # 3     floor divide
7 % 2     # 1     remainder
2 ** 10   # 1024  power
int("42") # 42    text to int
round(3.14159, 2)  # 3.14
abs(-5)   # 5'''),

    ("Strings", '''s = "Monkey Island"
s.upper()  s.lower()  s.strip()
s.replace("Monkey", "Rubber")
s.split()          # list of words
"-".join(["a", "b"])   # "a-b"
s[0]   s[-1]   s[0:6]   s[::-1]
len(s)   "Monkey" in s'''),

    ("Lists", '''nums = [3, 1, 2]
nums.append(4)     nums.insert(0, 9)
nums.remove(3)     nums.pop()
nums.sort()        sorted(nums)
nums[0]  nums[-1]  nums[1:3]
len(nums)  sum(nums)  max(nums)
copy = nums.copy()   # not = nums!'''),

    ("Dictionaries", '''d = {"a": 1, "b": 2}
d["c"] = 3         # add
d.get("z", 0)      # 0 if missing
"a" in d           # True
for k, v in d.items(): ...
d.keys()  d.values()
from collections import Counter'''),

    ("Sets", '''s = {1, 2, 3}
s.add(4)   s.discard(2)
"x" in s           # instant
a | b   union
a & b   intersection
a - b   difference
list(set(items))   # dedupe'''),

    ("If / elif / else", '''if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "F"

x = "adult" if age >= 18 else "minor"'''),

    ("Loops", '''for item in things:
    print(item)

for i, x in enumerate(things, start=1):
    print(i, x)

for a, b in zip(names, ages):
    ...

for n in range(1, 6):   # 1..5
    ...

while condition:
    ...
    break     continue'''),

    ("Functions", '''def greet(name, greeting="Hi"):
    """Say hello."""
    return f"{greeting}, {name}"

def total(*nums):        # any count
    return sum(nums)

def config(**options):   # named
    ...

greet("Sam", greeting="Yo")'''),

    ("Comprehensions", '''[n*n for n in range(5)]
[n for n in nums if n > 0]
{w: len(w) for w in words}
{c for c in text}
(n*n for n in nums)   # generator
any(x > 0 for x in nums)
all(x > 0 for x in nums)'''),

    ("Files", '''from pathlib import Path

Path("f.txt").write_text(s, encoding="utf-8")
text = Path("f.txt").read_text(encoding="utf-8")

with open("f.txt", encoding="utf-8") as f:
    for line in f:
        print(line.strip())

Path("dir").mkdir(exist_ok=True)
Path(".").rglob("*.py")'''),

    ("Exceptions", '''try:
    n = int(raw)
except ValueError:
    print("not a number")
except (TypeError, KeyError) as err:
    print(err)
else:
    print("no error")
finally:
    print("always runs")

raise ValueError("message")'''),

    ("JSON", '''import json

text = json.dumps(data, indent=2)
data = json.loads(text)

with open("f.json") as f:
    data = json.load(f)
with open("f.json", "w") as f:
    json.dump(data, f)'''),

    ("Classes", '''from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

class Dog:
    def __init__(self, name):
        self.name = name
    def speak(self):
        return f"{self.name}: woof"
    def __repr__(self):
        return f"Dog({self.name!r})"'''),

    ("Type hints", '''def f(name: str, n: int = 1) -> str:
    ...

x: list[str] = []
y: dict[str, int] = {}
z: int | None = None

# checked by mypy, not at runtime'''),

    ("The venv + pip ritual", '''python3 -m venv .venv
source .venv/bin/activate   # mac/linux
.venv\\Scripts\\activate      # windows

pip install requests
pip freeze > requirements.txt
pip install -r requirements.txt
deactivate'''),

    ("Calling a model (Level 6)", '''import anthropic
client = anthropic.Anthropic()   # key from env

r = client.messages.create(
    model="claude-sonnet-5",
    max_tokens=1024,
    system="You are Jarvis.",
    messages=[{"role": "user",
               "content": "Hello"}],
)
print(r.content[0].text)'''),

    ("Common dunder methods", '''__init__     build the object
__repr__     for programmers (debug)
__str__      for humans (print)
__len__      len(x)
__eq__       x == y
__getitem__  x[i]  and iteration
__enter__/__exit__   with x:'''),
]


def build() -> str:
    cards = NL.join("      " + _sheet(t, s) for t, s in CARDS)
    body = f"""  <section class="lesson-header">
    <span class="kicker">Cheat sheets</span>
    <h1>Python at a <span class="grad">glance</span> 📄</h1>
    <p class="lede muted">
      The syntax you look up most, on one page. Print it (it is styled for paper) and keep it by
      your keyboard for the first few weeks. Muscle memory does the rest.
    </p>
  </section>

  <div class="sheet">
    <div class="sheet-grid">
{cards}
    </div>
  </div>

  <div class="callout tip no-print" style="margin-top:24px">
    <span class="co-title">🖨️ Made for printing</span>
    Use your browser's print to PDF. The header, footer and this note vanish; you get clean
    reference cards on white.
  </div>
"""
    return page(
        path="cheatsheets.html",
        title=f"Cheat Sheets - {SCHOOL}",
        description="Printable Python reference cards: the syntax you look up most, on one page.",
        body=body,
        canonical=SITE + "/python/cheatsheets",
    )
