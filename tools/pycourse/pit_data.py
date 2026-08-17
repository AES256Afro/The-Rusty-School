"""The Snake Pit: puzzle data.

Every puzzle is a dict. The types:

  predict  the `code` runs and prints exactly `expected`
  fix      the `code` is broken; `solution` is the fix that prints `expected`
  bug      the `code` has a subtle bug; `solution` fixes it to print `expected`

tools/pyverify.py --pit runs each puzzle's runnable code (the solution for
fix/bug, the code itself for predict) and checks its output against
`expected`. So every "it prints:" claim in the pit is proven, exactly like
the lessons. Broken `code` for fix/bug puzzles is never executed.
"""

from __future__ import annotations

PUZZLES = []


def _p(**kw):
    PUZZLES.append(kw)


# ================================================================ EGG
_p(
    id="egg-1", tier="egg", type="predict",
    title="First words",
    task="What does this print?",
    code='''print("hi" * 3)''',
    expected="hihihi",
    hint="Multiplying a string repeats it. No spaces are added.",
    explain="`*` on a string repeats it. 'hi' three times, joined with nothing, is 'hihihi'.",
)
_p(
    id="egg-2", tier="egg", type="predict",
    title="Two kinds of divide",
    task="Predict both lines.",
    code='''print(7 / 2)
print(7 // 2)''',
    expected="3.5\n3",
    hint="One slash keeps the decimal; two slashes throw the remainder away.",
    explain="`/` always gives a float, so 3.5. `//` divides and discards the remainder, so 3.",
)
_p(
    id="egg-3", tier="egg", type="bug",
    title="The reassignment that isn't",
    task="This should print 15 but prints 10. Fix it.",
    code='''score = 10
score + 5
print(score)''',
    solution='''score = 10
score = score + 5
print(score)''',
    expected="15",
    hint="`score + 5` computes a value and then throws it away. Nothing was stored.",
    explain="`score + 5` on its own is a value nobody kept. You must assign it back: "
            "`score = score + 5` (or `score += 5`).",
)
_p(
    id="egg-4", tier="egg", type="fix",
    title="Mind the quotes",
    task="This won't run. Fix it so it prints the greeting.",
    code='''print(Hello, world!)''',
    solution='''print("Hello, world!")''',
    expected="Hello, world!",
    hint="Text needs quotes, or Python tries to read it as code.",
    explain="Without quotes, Python reads `Hello, world!` as code and fails. Text is a string, "
            "so it needs quotes around it.",
)
_p(
    id="egg-5", tier="egg", type="predict",
    title="f-string windows",
    task="What prints?",
    code='''name = "Guybrush"
n = 8
print(f"{name} knows {n} insults")''',
    expected="Guybrush knows 8 insults",
    hint="Inside an f-string, the braces are little windows showing a value.",
    explain="The `f` makes the braces evaluate: `{name}` and `{n}` are replaced by their values.",
)
_p(
    id="egg-6", tier="egg", type="predict",
    title="The remainder operator",
    task="Predict the output.",
    code='''for n in [10, 11, 12]:
    print(n, n % 2)''',
    expected="10 0\n11 1\n12 0",
    hint="`%` gives the remainder. What is left over when you divide by 2?",
    explain="`n % 2` is 0 for even numbers and 1 for odd. It is how you test evenness.",
)

# ================================================================ GARTER
_p(
    id="garter-1", tier="garter", type="predict",
    title="Slicing basics",
    task="Predict all three lines.",
    code='''word = "MONKEY"
print(word[0])
print(word[-1])
print(word[1:4])''',
    expected="M\nY\nONK",
    hint="Index 0 is the first character; -1 is the last. A slice stops BEFORE its end index.",
    explain="Counting from 0: word[0] is M, word[-1] is Y. The slice [1:4] takes positions 1, 2, "
            "3 (not 4), giving ONK.",
)
_p(
    id="garter-2", tier="garter", type="bug",
    title="Off by one",
    task="This should print all three names but crashes. Fix it.",
    code='''crew = ["Guybrush", "Elaine", "Otis"]
for i in range(1, 4):
    print(crew[i])''',
    solution='''crew = ["Guybrush", "Elaine", "Otis"]
for name in crew:
    print(name)''',
    expected="Guybrush\nElaine\nOtis",
    hint="Three items live at positions 0, 1 and 2. range(1, 4) reaches 3, which is out of range.",
    explain="`range(1, 4)` yields 1, 2, 3, but the last valid index is 2. Loop over the list "
            "directly instead of indexing: it can never go out of range.",
)
_p(
    id="garter-2b", tier="garter", type="predict",
    title="The input trap",
    task="A program adds two inputs of '2' and '3'. What does `print(a + b)` show?",
    code='''a = "2"
b = "3"
print(a + b)''',
    expected="23",
    hint="input() always returns text. What does + do to two strings?",
    explain="input() hands back strings, and + on two strings joins them. '2' + '3' is '23', not "
            "5. You must convert with int() first. This is the classic week-one bug.",
)
_p(
    id="garter-3", tier="garter", type="fix",
    title="The missing colon",
    task="Fix the syntax so it prints the verdict.",
    code='''score = 85
if score >= 60
    print("pass")''',
    solution='''score = 85
if score >= 60:
    print("pass")''',
    expected="pass",
    hint="Every `if`, `for`, `while` and `def` line ends with one particular character.",
    explain="An `if` line must end with a colon. It is the single most common syntax error "
            "in Python.",
)
_p(
    id="garter-4", tier="garter", type="predict",
    title="Truthiness",
    task="Predict each line.",
    code='''print(bool(0))
print(bool(""))
print(bool("0"))
print(bool([]))''',
    expected="False\nFalse\nTrue\nFalse",
    hint="Empty and zero are falsy. A non-empty string is truthy, even the string '0'.",
    explain="0, '' and [] are all falsy. But '0' is a non-empty string, so it is truthy. The "
            "third line catching people out is the whole point.",
)
_p(
    id="garter-5", tier="garter", type="bug",
    title="The endless loop",
    task="This never stops. Fix it so it counts down from 3.",
    code='''n = 3
while n > 0:
    print(n)''',
    solution='''n = 3
while n > 0:
    print(n)
    n -= 1''',
    expected="3\n2\n1",
    hint="The condition tests `n`, but nothing inside the loop ever changes `n`.",
    explain="`n` starts at 3 and never changes, so `n > 0` is true forever. The loop needs "
            "`n -= 1` so the condition eventually becomes false.",
)
_p(
    id="garter-6", tier="garter", type="predict",
    title="String methods chain",
    task="What prints?",
    code='''text = "  Hello World  "
print(text.strip().lower())''',
    expected="hello world",
    hint="strip() removes the surrounding spaces; lower() makes it lowercase. Left to right.",
    explain="Methods chain left to right: strip() first removes the outer spaces, then lower() "
            "lowercases the result.",
)

# ================================================================ RATTLER
_p(
    id="rattler-1", tier="rattler", type="predict",
    title="Aliasing",
    task="Predict the output. Think carefully.",
    code='''a = [1, 2, 3]
b = a
b.append(4)
print(a)''',
    expected="[1, 2, 3, 4]",
    hint="`b = a` does not copy the list. Both names point at the same one.",
    explain="`b = a` makes a second name for the same list, not a copy. Appending through `b` "
            "changes the one list, which `a` also sees. Use `a.copy()` for a real copy.",
)
_p(
    id="rattler-2", tier="rattler", type="predict",
    title="sort returns None",
    task="Predict what prints.",
    code='''nums = [3, 1, 2]
result = nums.sort()
print(result)''',
    expected="None",
    hint="`.sort()` sorts the list in place. What does it return?",
    explain=".sort() sorts the list in place and returns None. `result` catches that None. "
            "Use `sorted(nums)` if you want the sorted list as a value.",
)
_p(
    id="rattler-3", tier="rattler", type="bug",
    title="Counting wrong",
    task="This should count each letter but only ever shows 1s. Fix it.",
    code='''counts = {}
for letter in "aabbc":
    counts[letter] = 1
print(counts)''',
    solution='''counts = {}
for letter in "aabbc":
    counts[letter] = counts.get(letter, 0) + 1
print(counts)''',
    expected="{'a': 2, 'b': 2, 'c': 1}",
    hint="Setting the count to 1 every time throws away the previous count.",
    explain="`counts[letter] = 1` overwrites. The counting idiom is "
            "`counts.get(letter, 0) + 1`: the old count (or 0 if new) plus one.",
)
_p(
    id="rattler-4", tier="rattler", type="predict",
    title="Dict get with default",
    task="Predict both lines.",
    code='''d = {"a": 1}
print(d.get("a", 0))
print(d.get("z", 0))''',
    expected="1\n0",
    hint="`.get(key, default)` returns the value if present, otherwise the default.",
    explain="'a' is present so its value 1 comes back. 'z' is missing so the default 0 comes "
            "back, with no KeyError.",
)
_p(
    id="rattler-5", tier="rattler", type="predict",
    title="Sets remove duplicates",
    task="What is the length?",
    code='''items = [1, 2, 2, 3, 3, 3]
print(len(set(items)))''',
    expected="3",
    hint="A set holds each value at most once.",
    explain="set([1,2,2,3,3,3]) is {1, 2, 3}, which has 3 members. Sets discard duplicates.",
)
_p(
    id="rattler-6", tier="rattler", type="bug",
    title="Modifying while iterating",
    task="This tries to remove evens but skips some. Fix it.",
    code='''nums = [1, 2, 3, 4, 5, 6]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)
print(nums)''',
    solution='''nums = [1, 2, 3, 4, 5, 6]
nums = [n for n in nums if n % 2 != 0]
print(nums)''',
    expected="[1, 3, 5]",
    hint="Removing items from a list while looping over it makes the loop skip elements.",
    explain="Removing during iteration shifts the indices, so the loop skips items. Build a new "
            "list with a comprehension instead of mutating the one you are looping over.",
)

# ================================================================ BOA
_p(
    id="boa-1", tier="boa", type="bug",
    title="The mutable default",
    task="Each call should start with an empty list. Why don't they? Fix it.",
    code='''def add(item, bag=[]):
    bag.append(item)
    return bag

print(add("a"))
print(add("b"))''',
    solution='''def add(item, bag=None):
    if bag is None:
        bag = []
    bag.append(item)
    return bag

print(add("a"))
print(add("b"))''',
    expected="['a']\n['b']",
    hint="The default list is created once, when the function is defined, and shared by every "
         "call that uses it.",
    explain="A mutable default is created once and reused, so it accumulates across calls. The "
            "fix is always the same: default to None and build a fresh list inside.",
)
_p(
    id="boa-2", tier="boa", type="predict",
    title="Return versus print",
    task="Predict the output.",
    code='''def double(n):
    print(n * 2)

x = double(5)
print(x)''',
    expected="10\nNone",
    hint="The function prints but never returns. What does a function with no return give back?",
    explain="double prints 10, but has no return, so it gives back None. `x` catches that None. "
            "print shows something; return hands a value back.",
)
_p(
    id="boa-3", tier="boa", type="predict",
    title="Local scope",
    task="Predict what prints.",
    code='''x = 10

def change():
    x = 20

change()
print(x)''',
    expected="10",
    hint="Assigning to `x` inside the function creates a new local `x`, not the outer one.",
    explain="`x = 20` inside change() makes a brand-new local variable. The global `x` is "
            "untouched, so it prints 10.",
)
_p(
    id="boa-4", tier="boa", type="predict",
    title="args and unpacking",
    task="Predict the output.",
    code='''def total(*nums):
    return sum(nums)

values = [1, 2, 3, 4]
print(total(*values))''',
    expected="10",
    hint="`*nums` collects arguments into a tuple; `*values` spreads a list back into arguments.",
    explain="`*values` spreads the list into four separate arguments; `*nums` collects them "
            "into a tuple; sum adds them to 10. The star packs on one side and unpacks on the "
            "other.",
)
_p(
    id="boa-5", tier="boa", type="bug",
    title="Comparing the wrong way",
    task="This should greet only when logged in and not banned. It always greets. Fix it.",
    code='''logged_in = True
banned = False
if logged_in and banned == False:
    print("Welcome")
else:
    print("Denied")''',
    solution='''logged_in = True
banned = False
if logged_in and not banned:
    print("Welcome")
else:
    print("Denied")''',
    expected="Welcome",
    hint="The logic is actually correct here; the fix is to write it the clear, Pythonic way.",
    explain="`banned == False` works but reads awkwardly and is a common place to slip a bug. "
            "`not banned` is clearer and idiomatic. Both give 'Welcome' for this input.",
)
_p(
    id="boa-6", tier="boa", type="predict",
    title="Default argument evaluated once",
    task="Predict both lines.",
    code='''def greet(name, greeting="Hello"):
    return f"{greeting}, {name}"

print(greet("Otis"))
print(greet("Elaine", "Ahoy"))''',
    expected="Hello, Otis\nAhoy, Elaine",
    hint="When you don't pass greeting, the default is used.",
    explain="First call uses the default 'Hello'. Second call overrides it with 'Ahoy'. "
            "Defaults fill in only the arguments you omit.",
)

# ================================================================ COBRA
_p(
    id="cobra-1", tier="cobra", type="predict",
    title="Comprehension with filter",
    task="Predict the output.",
    code='''result = [n * n for n in range(6) if n % 2 == 0]
print(result)''',
    expected="[0, 4, 16]",
    hint="Take each n in 0..5, keep only the even ones, and square what remains.",
    explain="The evens in range(6) are 0, 2, 4. Squared: 0, 4, 16. The `if` filters, the front "
            "expression transforms.",
)
_p(
    id="cobra-2", tier="cobra", type="predict",
    title="Generators are one-shot",
    task="Predict both lines.",
    code='''gen = (n for n in range(3))
print(list(gen))
print(list(gen))''',
    expected="[0, 1, 2]\n[]",
    hint="A generator can only be walked once. After that it is exhausted.",
    explain="The first list() consumes the generator. The second finds it empty and returns []. "
            "Generators are single-use; build a list if you need the values twice.",
)
_p(
    id="cobra-3", tier="cobra", type="bug",
    title="Class attribute shared by all",
    task="Each deck should have its own cards. They all share one list. Fix it.",
    code='''class Deck:
    cards = []
    def add(self, c):
        self.cards.append(c)

a = Deck()
b = Deck()
a.add("ace")
print(b.cards)''',
    solution='''class Deck:
    def __init__(self):
        self.cards = []
    def add(self, c):
        self.cards.append(c)

a = Deck()
b = Deck()
a.add("ace")
print(b.cards)''',
    expected="[]",
    hint="`cards = []` at the class level is one list shared by every instance, like a mutable "
         "default.",
    explain="A mutable class attribute is shared by all instances. Give each instance its own "
            "list by assigning `self.cards = []` in __init__.",
)
_p(
    id="cobra-4", tier="cobra", type="predict",
    title="enumerate with start",
    task="Predict the output.",
    code='''for i, letter in enumerate("abc", start=1):
    print(i, letter)''',
    expected="1 a\n2 b\n3 c",
    hint="enumerate yields (index, item) pairs; start sets where the index begins.",
    explain="enumerate pairs each item with a counter, and start=1 makes it count from 1 "
            "instead of 0.",
)
_p(
    id="cobra-5", tier="cobra", type="predict",
    title="dict comprehension",
    task="What prints?",
    code='''words = ["hi", "bye", "yo"]
print({w: len(w) for w in words})''',
    expected="{'hi': 2, 'bye': 3, 'yo': 2}",
    hint="A dict comprehension builds key: value pairs. Here the key is the word, the value its "
         "length.",
    explain="`{w: len(w) for w in words}` maps each word to its length. Same idea as a list "
            "comprehension, with a colon making key/value pairs.",
)
_p(
    id="cobra-6", tier="cobra", type="predict",
    title="__repr__ in a container",
    task="Predict the output.",
    code='''class P:
    def __init__(self, n):
        self.n = n
    def __repr__(self):
        return f"P({self.n})"

print([P(1), P(2)])''',
    expected="[P(1), P(2)]",
    hint="Containers use __repr__ to show their contents, not __str__.",
    explain="When you print a list, each element is shown using its __repr__. Without one you "
            "would get an ugly memory-address string.",
)

# ================================================================ BASILISK
_p(
    id="basilisk-1", tier="basilisk", type="predict",
    title="Late binding closures",
    task="Predict the output. This one catches almost everybody.",
    code='''funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])''',
    expected="[2, 2, 2]",
    hint="The lambdas capture the variable i, not its value. By the time they run, the loop is "
         "over.",
    explain="Each lambda closes over the variable `i`, not the value it had. After the loop, i "
            "is 2, so every call returns 2. The fix is `lambda i=i: i` to bind now.",
)
_p(
    id="basilisk-2", tier="basilisk", type="predict",
    title="is versus ==",
    task="Predict all three lines.",
    code='''a = [1, 2, 3]
b = [1, 2, 3]
print(a == b)
print(a is b)
print(a is a)''',
    expected="True\nFalse\nTrue",
    hint="== compares contents; is compares identity (same object in memory).",
    explain="a and b have equal contents (==) but are different objects (is is False). a is "
            "itself, so `a is a` is True.",
)
_p(
    id="basilisk-3", tier="basilisk", type="predict",
    title="Default and the walrus",
    task="Predict the output.",
    code='''values = [1, 2, 3, 4, 5]
if (n := len(values)) > 3:
    print(f"{n} items, that's a lot")''',
    expected="5 items, that's a lot",
    hint="The walrus operator := assigns and returns in one step.",
    explain="`n := len(values)` assigns 5 to n AND yields 5 for the comparison. n is then usable "
            "in the body. The walrus assigns inside an expression.",
)
_p(
    id="basilisk-4", tier="basilisk", type="bug",
    title="Shallow copy of nested data",
    task="Changing the copy changes the original's inner list. Fix it so it doesn't.",
    code='''import copy
original = {"crew": ["Otis"]}
shallow = original.copy()
shallow["crew"].append("Meathook")
print(original["crew"])''',
    solution='''import copy
original = {"crew": ["Otis"]}
deep = copy.deepcopy(original)
deep["crew"].append("Meathook")
print(original["crew"])''',
    expected="['Otis']",
    hint=".copy() copies the outer dict but the inner list is still shared.",
    explain="A shallow copy duplicates the top level only; the inner list is shared. "
            "copy.deepcopy copies all the way down, so the original is untouched.",
)
_p(
    id="basilisk-5", tier="basilisk", type="predict",
    title="Chained comparison",
    task="Predict both lines.",
    code='''print(1 < 2 < 3)
print(3 > 2 > 1 > 0)''',
    expected="True\nTrue",
    hint="Python lets you chain comparisons like a mathematician: 1 < 2 < 3 means 1<2 and 2<3.",
    explain="Chained comparisons are evaluated pairwise and combined with `and`. Both chains "
            "hold, so both are True.",
)
_p(
    id="basilisk-6", tier="basilisk", type="predict",
    title="Generator in sum, exhausted",
    task="Predict the output.",
    code='''gen = (x for x in range(4))
print(sum(gen))
print(sum(gen))''',
    expected="6\n0",
    hint="sum walks the generator to the end. The second sum finds nothing left.",
    explain="The first sum consumes the generator (0+1+2+3 = 6). The second sees an exhausted "
            "generator and sums nothing, giving 0. A silent, classic bug.",
)
