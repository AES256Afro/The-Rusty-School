"""Level 2: The Toolbox.

Collections and functions. This is where a beginner stops writing
programs that could have been done by hand and starts writing programs
that could not.
"""

from __future__ import annotations

from .kit import callout, code, exercise, link, out, repl, table, tb, term, voice

LESSONS = []


def _add(**kw):
    LESSONS.append(kw)


# ---------------------------------------------------------------- 11
_add(
    level=2,
    num="11",
    slug="11-lists",
    id="py-11-lists",
    card="The workhorse container: ordered, changeable, and the source of one famous surprise.",
    title="Lists: Many Things at Once",
    emoji="📋",
    desc="Creating, indexing, slicing and mutating lists, plus the aliasing trap that catches everyone.",
    lede="""Up to now every variable has held exactly one thing. That is a very small world.
    A list holds as many things as you like, in order, and it changes everything.""",
    body=f"""
    <h2>A list is things in a row</h2>
    {code('''inventory = ["rubber chicken", "map", "grog", "sword"]

print(inventory)
print(len(inventory))
print(inventory[0])
print(inventory[-1])''',
          expect="""['rubber chicken', 'map', 'grog', 'sword']
4
rubber chicken
sword""")}
    <p>
      Square brackets, commas between items. Positions count from zero, negatives count from
      the right, and slicing works exactly as it did for strings, because both are sequences.
    </p>
    {code('''letters = ["a", "b", "c", "d", "e", "f"]

print(letters[1:4])
print(letters[:3])
print(letters[-2:])
print(letters[::2])
print(letters[::-1])''',
          expect="""['b', 'c', 'd']
['a', 'b', 'c']
['e', 'f']
['a', 'c', 'e']
['f', 'e', 'd', 'c', 'b', 'a']""")}

    <h2>Unlike strings, lists can be changed</h2>
    {code('''crew = ["Guybrush", "Elaine", "Otis"]

crew[2] = "Meathook"            # replace in place
print(crew)

crew.append("Carla")            # add one to the end
print(crew)

crew.insert(0, "LeChuck")       # add at a position
print(crew)

crew.remove("LeChuck")          # remove by value (the first match)
print(crew)

gone = crew.pop()               # remove the last, and give it back
print(gone, crew)

del crew[0]                     # remove by position
print(crew)''',
          expect="""['Guybrush', 'Elaine', 'Meathook']
['Guybrush', 'Elaine', 'Meathook', 'Carla']
['LeChuck', 'Guybrush', 'Elaine', 'Meathook', 'Carla']
['Guybrush', 'Elaine', 'Meathook', 'Carla']
Carla ['Guybrush', 'Elaine', 'Meathook']
['Elaine', 'Meathook']""")}
    <p>
      This is the crucial difference from strings. Strings are immutable: every operation
      returns a new string. Lists are mutable: operations change the list you already have.
      Almost every surprise in this lesson comes from that one fact.
    </p>

    <h2>The methods worth knowing</h2>
    {table(
        ["Method", "Does", "Changes the list?"],
        [
            ["<code>.append(x)</code>", "Add one item at the end", "Yes"],
            ["<code>.extend(other)</code>", "Add all of another list's items", "Yes"],
            ["<code>.insert(i, x)</code>", "Add at position i", "Yes"],
            ["<code>.remove(x)</code>", "Delete the first x. Raises ValueError if absent", "Yes"],
            ["<code>.pop()</code> / <code>.pop(i)</code>", "Remove and return the last, or the i-th", "Yes"],
            ["<code>.sort()</code>", "Sort in place", "Yes, and returns None"],
            ["<code>.reverse()</code>", "Reverse in place", "Yes"],
            ["<code>.clear()</code>", "Empty it", "Yes"],
            ["<code>.count(x)</code>", "How many x", "No"],
            ["<code>.index(x)</code>", "Position of the first x", "No"],
            ["<code>sorted(list)</code>", "A <em>new</em> sorted list", "No"],
            ["<code>list.copy()</code>", "A shallow copy", "No"],
        ],
    )}

    {callout("danger", "🪤 sort() returns None",
             "<p><code>names = names.sort()</code> is the classic disaster: "
             "<code>.sort()</code> sorts the list and returns <code>None</code>, so you have "
             "just thrown your list away and replaced it with nothing. Either "
             "<code>names.sort()</code> on its own line, or "
             "<code>names = sorted(names)</code>. Never both.</p>")}

    {code('''scores = [88, 42, 95, 61]

new_list = sorted(scores)
print(scores, "unchanged")
print(new_list, "the sorted copy")

scores.sort()
print(scores, "now sorted in place")

scores.sort(reverse=True)
print(scores, "descending")''',
          expect="""[88, 42, 95, 61] unchanged
[42, 61, 88, 95] the sorted copy
[42, 61, 88, 95] now sorted in place
[95, 88, 61, 42] descending""")}

    <h2>Sorting by something other than the value</h2>
    {code('''crew = ["Guybrush", "Otis", "Elaine", "Meathook"]

print(sorted(crew))                    # alphabetical
print(sorted(crew, key=len))           # by length
print(sorted(crew, key=str.lower))     # case-insensitive
print(max(crew, key=len))''',
          expect="""['Elaine', 'Guybrush', 'Meathook', 'Otis']
['Otis', 'Elaine', 'Guybrush', 'Meathook']
['Elaine', 'Guybrush', 'Meathook', 'Otis']
Guybrush""")}
    <p>
      <code>key=</code> takes a function and sorts by what that function returns. It is one of
      the most useful arguments in the whole language, and it comes back constantly once you
      have data with structure. Note <code>Guybrush</code> and <code>Meathook</code> are both
      eight letters, and Python kept them in their original relative order: Python's sort is
      <strong>stable</strong>, which is a guarantee you can rely on.
    </p>

    <h2>Searching and testing</h2>
    {code('''inventory = ["map", "grog", "sword"]

print("grog" in inventory)
print("banana" in inventory)
print(inventory.index("grog"))
print(inventory.count("grog"))''',
          expect="""True
False
1
1""")}

    <h2>The trap: two names, one list</h2>
    {code('''original = ["a", "b", "c"]
copy = original          # this is NOT a copy

copy.append("d")

print("original:", original)
print("copy:    ", copy)
print("same object?", original is copy)''',
          expect="""original: ['a', 'b', 'c', 'd']
copy:     ['a', 'b', 'c', 'd']
same object? True""")}

    {voice("PERCEPTION", "Formidable: Success",
           "Remember Lesson 2, where b = a copied the value and the two went their separate "
           "ways? That was true for a number. It is not true here.",
           "A variable does not hold a list. It holds an arrow pointing at a list. "
           "copy = original draws a second arrow at the same list. There is one list and two "
           "names for it, and changing it through either name changes it for both.")}

    <p>Three ways to make a genuine copy:</p>
    {code('''original = ["a", "b", "c"]

copy1 = original.copy()
copy2 = list(original)
copy3 = original[:]

copy1.append("changed")
print(original)
print(copy1)''',
          expect="""['a', 'b', 'c']
['a', 'b', 'c', 'changed']""")}
    <p>
      All three are equivalent for a flat list. If your list contains other lists, these are
      <em>shallow</em> copies: the outer list is new, the inner lists are still shared. For
      that, <code>copy.deepcopy()</code>, which Lesson 15 covers.
    </p>

    <h2>Building a list up</h2>
    {code('''squares = []

for n in range(1, 6):
    squares.append(n * n)

print(squares)
print(sum(squares), min(squares), max(squares))''',
          expect="""[1, 4, 9, 16, 25]
55 1 25""")}
    <p>
      Start empty, append in a loop, use afterwards. This is <em>the</em> most common shape in
      beginner Python, and in Lesson 16 you will learn to write it in one line with a
      comprehension. Learn it this way first; the short version means nothing if you cannot
      see the loop inside it.
    </p>

    <h2>Lists of anything, including lists</h2>
    {code('''mixed = [42, "grog", 3.5, True, None]
print(mixed)

grid = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
print(grid[1])
print(grid[1][2])

for row in grid:
    print(" ".join(str(n) for n in row))''',
          expect="""[42, 'grog', 3.5, True, None]
[4, 5, 6]
6
1 2 3
4 5 6
7 8 9""")}
    <p>
      A list can hold anything, including other lists. <code>grid[1][2]</code> reads as "row
      1, then item 2 of that". Mixed-type lists are legal but usually a smell: if the items
      mean different things, you probably want a dictionary (Lesson 13) or a class
      (Lesson 31).
    </p>

    {exercise(1, "Inventory manager",
              "<p>Start with three items. Add two, remove one by name, sort what remains, and "
              "print a numbered list.</p>",
              code('''inventory = ["sword", "map", "grog"]

inventory.append("rubber chicken")
inventory.append("mints")
inventory.remove("grog")
inventory.sort()

print(f"You are carrying {len(inventory)} things:")
for i, item in enumerate(inventory, start=1):
    print(f"  {i}. {item}")''',
                   expect="""You are carrying 4 things:
  1. map
  2. mints
  3. rubber chicken
  4. sword"""))}

    {exercise(2, "Statistics without a library",
              "<p>For the list <code>[88, 42, 95, 61, 73]</code>, print the highest, lowest, "
              "total, average to one decimal place, and the median.</p>",
              code('''scores = [88, 42, 95, 61, 73]

print(f"Highest: {max(scores)}")
print(f"Lowest:  {min(scores)}")
print(f"Total:   {sum(scores)}")
print(f"Average: {sum(scores) / len(scores):.1f}")

ordered = sorted(scores)
middle = len(ordered) // 2
print(f"Median:  {ordered[middle]}")''',
                   expect="""Highest: 95
Lowest:  42
Total:   359
Average: 71.8
Median:  73""")
              + "<p>That median is only correct for an odd number of values. For an even "
              "count you must average the middle two, which is exactly the sort of edge case "
              "that makes people reach for the standard library: "
              "<code>import statistics; statistics.median(scores)</code> handles both.</p>")}

    {exercise(3, "Predict the aliasing",
              "<p>What does this print? Think carefully.</p>"
              + code('''a = [1, 2, 3]
b = a
c = a.copy()

b.append(4)
c.append(5)

print(a)
print(b)
print(c)''', run=False, verify="compile"),
              "<p><code>[1, 2, 3, 4]</code>, then <code>[1, 2, 3, 4]</code>, then "
              "<code>[1, 2, 3, 5]</code>.</p>"
              "<p><code>b</code> is another name for <code>a</code>, so appending through "
              "<code>b</code> shows up in <code>a</code>. <code>c</code> is a real copy, so it "
              "goes its own way.</p>"
              "<p>If you got this right, you understand the single most important thing in "
              "this lesson, and you have avoided a bug that costs professionals real hours.</p>")}
""",
)

# ---------------------------------------------------------------- 12
_add(
    level=2,
    num="12",
    slug="12-tuples",
    id="py-12-tuples",
    card="Lists that cannot change, why that is a feature, and the unpacking trick you will use daily.",
    title="Tuples and Unpacking",
    emoji="🔒",
    desc="Immutable sequences, tuple unpacking, returning several values, and when to use a tuple over a list.",
    lede="""A tuple is a list that has been set in resin. That sounds like a downside. It is
    the reason tuples show up everywhere in real Python.""",
    body=f"""
    <h2>Round brackets instead of square</h2>
    {code('''point = (3, 7)
colours = ("red", "green", "blue")

print(point, colours)
print(point[0], colours[-1])
print(len(colours))''',
          expect="""(3, 7) ('red', 'green', 'blue')
3 blue
3""")}
    <p>Everything you can <em>read</em> from a list works. Everything that would change it does not:</p>
    {code('''point = (3, 7)
point[0] = 10''', run=False, verify="skip")}
    {tb("TypeError: 'tuple' object does not support item assignment")}

    <h2>Why would you want that?</h2>
    <ul>
      <li><strong>It documents intent.</strong> A tuple says "these belong together and this
      set will not change": a coordinate, an RGB colour, a database row.</li>
      <li><strong>It cannot be broken by accident.</strong> Hand a list to a function and the
      function might append to it. Hand a tuple and it cannot.</li>
      <li><strong>It can be a dictionary key.</strong> Lists cannot (Lesson 13 explains why).</li>
      <li><strong>It is slightly smaller and faster.</strong> True, and almost never the
      reason to choose one.</li>
    </ul>

    {callout("warn", "🪤 The one-item tuple",
             "<p><code>(5)</code> is just the number 5 in brackets. A one-item tuple needs a "
             "trailing comma: <code>(5,)</code>. It looks like a typo, it is required, and it "
             "has confused every Python programmer who ever lived at least once.</p>")}
    {code('''not_a_tuple = (5)
actually_a_tuple = (5,)

print(type(not_a_tuple))
print(type(actually_a_tuple))''',
          expect="""<class 'int'>
<class 'tuple'>""")}

    <h2>Unpacking: the feature you will use every day</h2>
    {code('''point = (3, 7)
x, y = point
print(x, y)

# the brackets are optional, which is why this works
name, role, age = "Guybrush", "pirate", 24
print(f"{name} the {role}, aged {age}")

# and why swapping is one line
a, b = 1, 2
a, b = b, a
print(a, b)''',
          expect="""3 7
Guybrush the pirate, aged 24
2 1""")}
    <p>
      The number of names on the left must match the number of values on the right, or Python
      raises <code>ValueError: too many values to unpack</code>. Unless you use a star:
    </p>
    {code('''scores = [95, 88, 72, 61, 40]

best, *rest = scores
print(best, rest)

first, *middle, last = scores
print(first, middle, last)''',
          expect="""95 [88, 72, 61, 40]
95 [88, 72, 61] 40""")}
    <p>
      The starred name soaks up everything left over, and always becomes a list. There can be
      at most one of them, for the obvious reason.
    </p>

    <h2>Returning several things at once</h2>
    {code('''def split_name(full_name):
    parts = full_name.split()
    return parts[0], parts[-1]


first, last = split_name("Guybrush Ulysses Threepwood")
print(first, last)

both = split_name("Elaine Marley")
print(both, type(both))''',
          expect="""Guybrush Threepwood
('Elaine', 'Marley') <class 'tuple'>""")}
    <p>
      A function can only return one object, but that object can be a tuple, so in practice
      Python functions return as many values as they like. Notice you did not have to write
      any brackets: a bare comma-separated list of values <em>is</em> a tuple. This is the
      single most common use of tuples in real code.
    </p>

    <h2>Tuples in loops</h2>
    {code('''crew = [
    ("Guybrush", "pirate", 24),
    ("Elaine", "governor", 28),
    ("Otis", "prisoner", 41),
]

for name, role, age in crew:
    print(f"{name:10} {role:10} {age}")''',
          expect="""Guybrush   pirate     24
Elaine     governor   28
Otis       prisoner   41""")}
    <p>
      The loop unpacks each tuple automatically. This is exactly how <code>enumerate</code>
      and <code>zip</code> from Lesson 9 work: they hand you tuples, and you unpack them in
      the <code>for</code> line without thinking about it.
    </p>

    <h2>Named tuples, when positions get confusing</h2>
    {code('''from collections import namedtuple

Pirate = namedtuple("Pirate", ["name", "role", "insults"])

guy = Pirate("Guybrush", "pirate", 7)

print(guy)
print(guy.name, guy.insults)
print(guy[0])                 # still a tuple underneath
name, role, insults = guy     # still unpacks
print(role)''',
          expect="""Pirate(name='Guybrush', role='pirate', insults=7)
Guybrush 7
Guybrush
pirate""")}
    <p>
      <code>guy.name</code> beats <code>guy[0]</code> the moment you have more than two
      fields. For anything more elaborate, Lesson 33's <code>dataclass</code> is the modern
      answer, but named tuples are perfect when you want something immutable and light.
    </p>

    {exercise(1, "Min, max and average in one function",
              "<p>Write a function that takes a list of numbers and returns three values. Call "
              "it and unpack the result.</p>",
              code('''def summarise(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)


lowest, highest, average = summarise([88, 42, 95, 61, 73])

print(f"Lowest:  {lowest}")
print(f"Highest: {highest}")
print(f"Average: {average:.1f}")''',
                   expect="""Lowest:  42
Highest: 95
Average: 71.8"""))}

    {exercise(2, "Tuple or list?",
              "<p>For each, say which you would choose and why.</p>"
              "<ol><li>The RGB values of a colour.</li>"
              "<li>The names of everyone who has signed up to a newsletter.</li>"
              "<li>A row read from a spreadsheet.</li>"
              "<li>The days of the week.</li>"
              "<li>The cards currently in a player's hand.</li></ol>",
              "<ol><li><strong>Tuple.</strong> Exactly three parts, fixed meaning, will not "
              "grow.</li>"
              "<li><strong>List.</strong> The whole point is that people join and leave.</li>"
              "<li><strong>Tuple</strong> (or a named tuple). A row has a fixed shape.</li>"
              "<li><strong>Tuple.</strong> There have been seven since Babylon and there will "
              "be seven tomorrow.</li>"
              "<li><strong>List.</strong> Cards are drawn and played constantly.</li></ol>"
              "<p>The question that decides it is almost always: does the number of items "
              "change during the program's life?</p>")}

    {exercise(3, "Unpack the mess",
              "<p>From this data, print each film's title and its highest rating, using "
              "unpacking rather than indexes.</p>"
              + code('''data = [
    ("Monkey Island", 9, 8, 10),
    ("Disco Elysium", 10, 10, 9),
    ("Grim Fandango", 9, 9, 9),
]''', run=False, verify="compile"),
              code('''data = [
    ("Monkey Island", 9, 8, 10),
    ("Disco Elysium", 10, 10, 9),
    ("Grim Fandango", 9, 9, 9),
]

for title, *ratings in data:
    print(f"{title:15} best score {max(ratings)}")''',
                   expect="""Monkey Island   best score 10
Disco Elysium   best score 10
Grim Fandango   best score 9""")
              + "<p><code>for title, *ratings in data</code> unpacks and stars in one move. "
              "This is the kind of line that makes people say Python is elegant.</p>")}
""",
)

# ---------------------------------------------------------------- 13
_add(
    level=2,
    num="13",
    slug="13-dicts",
    id="py-13-dicts",
    card="Look things up by name instead of position. The most useful container in the language.",
    title="Dictionaries: Look It Up",
    emoji="🗂️",
    desc="Key-value pairs, .get(), looping over items, nested dictionaries, and why dicts are everywhere.",
    lede="""If lists are a row of numbered boxes, a dictionary is a filing cabinet with labels.
    It is the container that real programs are actually made of.""",
    body=f"""
    <h2>Keys and values</h2>
    {code('''pirate = {
    "name": "Guybrush",
    "role": "pirate",
    "insults": 7,
    "has_ship": False,
}

print(pirate["name"])
print(pirate["insults"])
print(len(pirate))''',
          expect="""Guybrush
7
4""")}
    <p>
      Curly braces, <code>key: value</code> pairs, commas between. You look things up by
      <strong>key</strong>, not by position, which is why a dictionary stays readable when a
      tuple of eight fields does not.
    </p>

    <h2>Adding, changing, removing</h2>
    {code('''pirate = {"name": "Guybrush", "insults": 7}

pirate["ship"] = "Sea Monkey"      # add
pirate["insults"] += 1             # change
print(pirate)

del pirate["ship"]                 # remove
print(pirate)

removed = pirate.pop("insults")    # remove and give back
print(removed, pirate)''',
          expect="""{'name': 'Guybrush', 'insults': 8, 'ship': 'Sea Monkey'}
{'name': 'Guybrush', 'insults': 8}
8 {'name': 'Guybrush'}""")}
    <p>
      Assigning to a key that does not exist creates it. Assigning to one that does replaces
      it. There is no separate "add" and "update", which is one less thing to remember.
    </p>

    <h2>The missing key problem</h2>
    {code('''pirate = {"name": "Guybrush"}
print(pirate["ship"])''', run=False, verify="skip")}
    {tb("KeyError: 'ship'")}
    <p>Three ways to handle it, in order of how often you want them:</p>
    {code('''pirate = {"name": "Guybrush"}

print(pirate.get("ship"))                     # None instead of an explosion
print(pirate.get("ship", "no ship yet"))      # your own default
print("ship" in pirate)                       # just ask

if "name" in pirate:
    print(f"Captain {pirate['name']}")''',
          expect="""None
no ship yet
False
Captain Guybrush""")}
    {callout("tip", "🎯 .get() is the one you want",
             "<p>Reach for <code>.get(key, default)</code> by default and square brackets only "
             "when a missing key genuinely means the program is broken. Letting it crash is "
             "sometimes right: silently defaulting a missing price to zero is worse than "
             "stopping.</p>")}

    <h2>Looping</h2>
    {code('''scores = {"Guybrush": 95, "Elaine": 88, "Otis": 72}

for name in scores:
    print(name)

print("---")

for name, score in scores.items():
    print(f"{name:10} {score}")

print("---")

print(list(scores.keys()))
print(list(scores.values()))
print(sum(scores.values()))''',
          expect="""Guybrush
Elaine
Otis
---
Guybrush   95
Elaine     88
Otis       72
---
['Guybrush', 'Elaine', 'Otis']
[95, 88, 72]
255""")}
    <p>
      Looping over a dictionary gives you the <strong>keys</strong>. Almost always you want
      <code>.items()</code>, which gives you both as a tuple that the <code>for</code> line
      unpacks for you.
    </p>

    {voice("ENCYCLOPEDIA", "Medium: Success",
           "Since Python 3.7, dictionaries keep their insertion order as a language guarantee, "
           "not an accident. Before that they were officially unordered and code that relied "
           "on order was broken. If you read an old tutorial saying 'dictionaries have no "
           "order', it is describing a Python that no longer exists.")}

    <h2>Sorting a dictionary</h2>
    {code('''scores = {"Guybrush": 95, "Elaine": 88, "Otis": 72, "Meathook": 91}

for name, score in sorted(scores.items(), key=lambda pair: pair[1], reverse=True):
    print(f"{score:3}  {name}")''',
          expect=""" 95  Guybrush
 91  Meathook
 88  Elaine
 72  Otis""")}
    <p>
      <code>lambda pair: pair[1]</code> is a tiny throwaway function meaning "the second part
      of each pair", so we sort by score rather than by name. Lambdas get a proper treatment
      in Lesson 37; for now, read it as "sort by this bit".
    </p>

    <h2>Counting things: the classic use</h2>
    {code('''text = "the rubber chicken with a pulley in the middle"

counts = {}
for word in text.split():
    counts[word] = counts.get(word, 0) + 1

for word, n in counts.items():
    if n > 1:
        print(f"{word}: {n}")''',
          expect="the: 2")}
    <p>
      <code>counts.get(word, 0) + 1</code> is the counting idiom: "whatever it was, or zero if
      new, plus one". Memorise it. The standard library also has a purpose-built tool:
    </p>
    {code('''from collections import Counter

text = "the rubber chicken with a pulley in the middle"
counts = Counter(text.split())

print(counts.most_common(3))
print(counts["the"])
print(counts["banana"])      # missing keys are 0, not an error''',
          expect="""[('the', 2), ('rubber', 1), ('chicken', 1)]
2
0""")}

    <h2>What can be a key?</h2>
    {code('''valid = {
    "text": 1,
    42: 2,
    3.5: 3,
    True: 4,
    ("x", "y"): 5,       # tuples are fine: they cannot change
}
print(valid[("x", "y")])

# {["x", "y"]: 5}       # TypeError: unhashable type: 'list' ''',
          expect="5")}
    <p>
      Keys must be <strong>immutable</strong>. The reason is mechanical: a dictionary finds
      things instantly by computing a number from the key (a hash) and using it as an address.
      If the key could change afterwards, the address would be wrong and the value would be
      lost. Lists can change, so lists cannot be keys. Tuples cannot, so they can.
    </p>

    {callout("info", "⚡ Why dictionaries are fast",
             "<p>Looking up <code>d[\"name\"]</code> in a dictionary of one item takes about "
             "the same time as in a dictionary of one million. Searching a list means checking "
             "items one by one, so a million-item list takes a million times longer than a "
             "one-item list. If you ever find yourself writing <code>for x in big_list: if "
             "x.id == wanted</code> inside another loop, a dictionary keyed by id will make "
             "your program dramatically faster. This is the single highest-value performance "
             "trick a beginner can learn.</p>")}

    <h2>Nested dictionaries: the shape of real data</h2>
    {code('''game = {
    "title": "The Secret of Monkey Island",
    "year": 1990,
    "characters": {
        "Guybrush": {"role": "hero", "insults": 8},
        "LeChuck": {"role": "villain", "insults": 3},
    },
    "islands": ["Melee", "Monkey"],
}

print(game["title"])
print(game["characters"]["Guybrush"]["insults"])
print(game["islands"][0])

for name, info in game["characters"].items():
    print(f"{name:10} {info['role']:8} {info['insults']} insults")''',
          expect="""The Secret of Monkey Island
8
Melee
Guybrush   hero     8 insults
LeChuck    villain  3 insults""")}
    <p>
      Dictionaries containing dictionaries containing lists is exactly the shape of JSON,
      which is how essentially every web API on earth sends data. When you call an AI model in
      Level 6, this is what comes back. Get comfortable here and Level 5 becomes easy.
    </p>

    {exercise(1, "Phone book",
              "<p>Build a dictionary of three names to phone numbers. Look one up safely, "
              "handle a missing one, add a fourth, and print them all sorted by name.</p>",
              code('''book = {
    "Elaine": "555-0100",
    "Guybrush": "555-0199",
    "Otis": "555-0110",
}

print(book.get("Elaine"))
print(book.get("LeChuck", "not in the book"))

book["Meathook"] = "555-0123"

for name in sorted(book):
    print(f"{name:10} {book[name]}")''',
                   expect="""555-0100
not in the book
Elaine     555-0100
Guybrush   555-0199
Meathook   555-0123
Otis       555-0110""")
              + "<p><code>sorted(book)</code> sorts the keys, because looping a dict gives "
              "keys. Short and idiomatic.</p>")}

    {exercise(2, "Letter frequency",
              "<p>Count how often each letter appears in a word, ignoring case, and print the "
              "counts in alphabetical order.</p>",
              code('''word = "Mississippi"

counts = {}
for letter in word.lower():
    counts[letter] = counts.get(letter, 0) + 1

for letter in sorted(counts):
    print(f"{letter}: {counts[letter]}")''',
                   expect="""i: 4
m: 1
p: 2
s: 4"""))}

    {exercise(3, "Invert a dictionary",
              "<p>Turn <code>{{'a': 1, 'b': 2, 'c': 3}}</code> into "
              "<code>{{1: 'a', 2: 'b', 3: 'c'}}</code>. Then explain what happens if two keys "
              "share a value.</p>",
              code('''original = {"a": 1, "b": 2, "c": 3}

flipped = {}
for key, value in original.items():
    flipped[value] = key

print(flipped)

# and the catch
clash = {"a": 1, "b": 1}
flipped_clash = {}
for key, value in clash.items():
    flipped_clash[value] = key
print(flipped_clash)''',
                   expect="""{1: 'a', 2: 'b', 3: 'c'}
{1: 'b'}""")
              + "<p>The second one silently loses data: both keys map to 1, so the later one "
              "wins and 'a' vanishes. Inverting a dictionary is only safe when the values are "
              "unique, and noticing that <em>before</em> shipping is exactly the kind of "
              "thinking that separates working code from code that works today.</p>")}
""",
)

# ---------------------------------------------------------------- 14
_add(
    level=2,
    num="14",
    slug="14-sets",
    id="py-14-sets",
    card="Unordered collections with no duplicates, and the fastest way to ask 'have I seen this?'",
    title="Sets: No Duplicates Allowed",
    emoji="🎯",
    desc="Sets, deduplication, membership testing, and set operations like union and intersection.",
    lede="""The container everyone forgets exists, and then uses constantly once they
    remember. A set is a bag where nothing appears twice and order means nothing.""",
    body=f"""
    <h2>Duplicates simply vanish</h2>
    {code('''visited = {"Melee", "Monkey", "Melee", "Booty", "Monkey"}
print(sorted(visited))
print(len(visited))''',
          expect="""['Booty', 'Melee', 'Monkey']
3""")}
    {callout("warn", "🔀 Why sorted() is in that example",
             "<p>A set has <strong>no order</strong>, and printing one raw shows its items in "
             "whatever arrangement the internal table happens to produce. That arrangement can "
             "differ between runs, between machines and between Python versions. Every example "
             "on this page sorts before printing, and you should too, whenever a human is "
             "going to read the output.</p>")}
    <p>
      Curly braces like a dictionary, but with single values instead of pairs. Adding
      something already present does nothing at all, which is the entire point.
    </p>
    {callout("warn", "🪤 The empty set",
             "<p><code>{{}}</code> is an empty <em>dictionary</em>, not an empty set. Python "
             "had dictionaries first and they got the braces. For an empty set you must write "
             "<code>set()</code>.</p>")}

    <h2>The one-line deduplicate</h2>
    {code('''names = ["Otis", "Elaine", "Otis", "Guybrush", "Elaine", "Otis"]

unique = list(set(names))
print(sorted(unique))
print(f"{len(names)} entries, {len(unique)} unique")''',
          expect="""['Elaine', 'Guybrush', 'Otis']
6 entries, 3 unique""")}
    <p>
      Note the <code>sorted</code>. Sets have no order, so <code>list(set(...))</code> can
      come back in any arrangement. If you need the original order preserved while removing
      duplicates, use a dictionary instead, which keeps insertion order:
    </p>
    {code('''names = ["Otis", "Elaine", "Otis", "Guybrush", "Elaine"]
print(list(dict.fromkeys(names)))''',
          expect="['Otis', 'Elaine', 'Guybrush']")}

    <h2>Membership, at speed</h2>
    {code('''allowed = {"guybrush", "elaine", "otis"}

print("elaine" in allowed)
print("lechuck" in allowed)

allowed.add("meathook")
allowed.discard("otis")        # no error if it is absent
print(sorted(allowed))''',
          expect="""True
False
['elaine', 'guybrush', 'meathook']""")}
    <p>
      <code>in</code> on a set is effectively instant no matter how big the set is, exactly
      like a dictionary key lookup and for the same reason. <code>in</code> on a list checks
      items one at a time. If you are testing membership against thousands of items inside a
      loop, converting the list to a set once can turn minutes into milliseconds.
    </p>

    {voice("LOGIC", "Medium: Success",
           "This is the first optimisation worth learning, because it is not a trick, it is a "
           "correction. You were using the wrong container. Choosing the right data structure "
           "beats clever code almost every time, and it usually makes the code shorter too.")}

    <h2>Set arithmetic</h2>
    {code('''pirates = {"Guybrush", "LeChuck", "Meathook"}
governors = {"Elaine", "Guybrush"}

print(sorted(pirates | governors))      # union: everyone
print(sorted(pirates & governors))      # intersection: in both
print(sorted(pirates - governors))      # difference: pirates only
print(sorted(pirates ^ governors))      # symmetric difference: in one but not both''',
          expect="""['Elaine', 'Guybrush', 'LeChuck', 'Meathook']
['Guybrush']
['LeChuck', 'Meathook']
['Elaine', 'LeChuck', 'Meathook']""")}
    {table(
        ["Operator", "Method", "Means"],
        [["<code>|</code>", "<code>.union()</code>", "in either"],
         ["<code>&amp;</code>", "<code>.intersection()</code>", "in both"],
         ["<code>-</code>", "<code>.difference()</code>", "in the first only"],
         ["<code>^</code>", "<code>.symmetric_difference()</code>", "in exactly one"],
         ["<code>&lt;=</code>", "<code>.issubset()</code>", "all of these are in that"]],
    )}
    <p>
      These turn fiddly loops into one readable line. "Which users signed up but never logged
      in" is <code>signed_up - logged_in</code>. "Which tags do these two articles share" is
      <code>a &amp; b</code>. Whenever you catch yourself writing a loop with an
      <code>if x in other_list</code> inside it, stop and ask whether this is set arithmetic
      wearing a disguise.
    </p>

    <h2>What sets cannot do</h2>
    <ul>
      <li><strong>No order.</strong> There is no <code>set[0]</code>. If order matters, you
      want a list.</li>
      <li><strong>No duplicates,</strong> obviously. If you need to count occurrences, you
      want <code>Counter</code>.</li>
      <li><strong>Items must be immutable,</strong> for the same hashing reason as dictionary
      keys. Sets of tuples are fine, sets of lists are not.</li>
    </ul>

    <h2>Choosing a container</h2>
    {table(
        ["If you need...", "Use", "Why"],
        [
            ["An ordered collection you will change", "<code>list</code>", "The default. Order and duplicates both kept"],
            ["A fixed group that belongs together", "<code>tuple</code>", "Cannot be changed by accident, can be a dict key"],
            ["Lookup by name or id", "<code>dict</code>", "Instant lookup, readable code"],
            ["Uniqueness or fast membership", "<code>set</code>", "Duplicates gone, <code>in</code> is instant"],
            ["Counting occurrences", "<code>Counter</code>", "A dict that starts every count at zero"],
        ],
    )}

    {exercise(1, "Common interests",
              "<p>Two people list their hobbies. Print what they share, what only the first "
              "one does, and the combined list, all sorted.</p>",
              code('''alice = {"sailing", "insults", "cartography", "grog"}
bob = {"grog", "swordfighting", "sailing"}

print("Both:      ", sorted(alice & bob))
print("Alice only:", sorted(alice - bob))
print("Together:  ", sorted(alice | bob))''',
                   expect="""Both:       ['grog', 'sailing']
Alice only: ['cartography', 'insults']
Together:   ['cartography', 'grog', 'insults', 'sailing', 'swordfighting']"""))}

    {exercise(2, "Unique words",
              "<p>Count how many distinct words appear in a sentence, ignoring case and full "
              "stops, and list any that appear more than once.</p>",
              code('''text = "The dog saw the cat. The cat saw the dog."

words = text.lower().replace(".", "").split()
unique = set(words)

print(f"{len(words)} words, {len(unique)} distinct")

repeated = sorted(w for w in unique if words.count(w) > 1)
print("repeated:", repeated)''',
                   expect="""10 words, 4 distinct
repeated: ['cat', 'dog', 'saw', 'the']""")
              + "<p>Honest note: <code>words.count(w)</code> inside a loop scans the whole "
              "list every time, which is wasteful. For ten words nobody cares; for ten million "
              "you would use <code>Counter</code>. Knowing when you are allowed not to care is "
              "part of the job.</p>")}

    {exercise(3, "Which container?",
              "<p>Pick the right one for each, and say why.</p>"
              "<ol><li>Every unique IP address that hit a web server today.</li>"
              "<li>The order players took their turns in.</li>"
              "<li>Looking up a product's price by its barcode.</li>"
              "<li>Checking whether a word is in a 300,000 word dictionary, a million times.</li></ol>",
              "<ol><li><strong>set.</strong> Unique is in the requirement.</li>"
              "<li><strong>list.</strong> Order is the entire point, and repeats are "
              "possible.</li>"
              "<li><strong>dict</strong>, keyed by barcode. Instant lookup by name.</li>"
              "<li><strong>set.</strong> A list would do 300,000 comparisons per check, a "
              "million times over. A set does one. This is the difference between a program "
              "that finishes and one you kill after an hour.</li></ol>")}
""",
)

# ---------------------------------------------------------------- 15
_add(
    level=2,
    num="15",
    slug="15-nested",
    id="py-15-nested",
    card="Lists of dictionaries and dictionaries of lists: the shape all real data arrives in.",
    title="Nested Data",
    emoji="🪆",
    desc="Working with lists of dictionaries, safe navigation of deep structures, and shallow versus deep copies.",
    lede="""Real data is never a flat list. It is a list of records, each with fields, some of
    which are themselves lists. Here is how to keep your head.""",
    body=f"""
    <h2>The shape you will meet a thousand times</h2>
    {code('''crew = [
    {"name": "Guybrush", "role": "captain", "skills": ["insults", "sailing"]},
    {"name": "Elaine", "role": "governor", "skills": ["politics", "swordplay", "rescue"]},
    {"name": "Otis", "role": "lookout", "skills": []},
]

print(len(crew))
print(crew[0]["name"])
print(crew[1]["skills"][0])
print(len(crew[2]["skills"]))''',
          expect="""3
Guybrush
politics
0""")}
    <p>
      A list of dictionaries. Every API response, every CSV file, every database query result
      and every JSON file you ever open will look roughly like this. Read the access
      left to right: <code>crew[1]</code> is a dictionary,
      <code>["skills"]</code> is its list, <code>[0]</code> is the first of those.
    </p>

    <h2>Looping over it</h2>
    {code('''crew = [
    {"name": "Guybrush", "role": "captain", "skills": ["insults", "sailing"]},
    {"name": "Elaine", "role": "governor", "skills": ["politics", "swordplay", "rescue"]},
    {"name": "Otis", "role": "lookout", "skills": []},
]

for member in crew:
    skills = ", ".join(member["skills"]) or "none listed"
    print(f"{member['name']:10} ({member['role']:9}) {skills}")''',
          expect="""Guybrush   (captain  ) insults, sailing
Elaine     (governor ) politics, swordplay, rescue
Otis       (lookout  ) none listed""")}
    <p>
      <code>x or y</code> gives you <code>x</code> unless it is falsy, in which case
      <code>y</code>. An empty string is falsy, so an empty skill list produces "none listed".
      That is the truthiness rule from Lesson 6 doing real work.
    </p>

    {callout("warn", "🪤 Quotes inside f-strings",
             "<p>Notice <code>{{member['name']}}</code> uses single quotes inside a "
             "double-quoted f-string. Before Python 3.12 reusing the same quote character "
             "inside the braces was an error. It is legal now, but mixing them is still "
             "clearer and works on every version.</p>")}

    <h2>Filtering and summarising</h2>
    {code('''crew = [
    {"name": "Guybrush", "role": "captain", "pay": 100},
    {"name": "Elaine", "role": "governor", "pay": 250},
    {"name": "Otis", "role": "lookout", "pay": 40},
    {"name": "Meathook", "role": "lookout", "pay": 45},
]

lookouts = [m for m in crew if m["role"] == "lookout"]
print([m["name"] for m in lookouts])

total = sum(m["pay"] for m in crew)
print(f"Total wages: {total}")

richest = max(crew, key=lambda m: m["pay"])
print(f"Best paid: {richest['name']}")

by_pay = sorted(crew, key=lambda m: m["pay"], reverse=True)
for m in by_pay:
    print(f"  {m['pay']:4}  {m['name']}")''',
          expect="""['Otis', 'Meathook']
Total wages: 435
Best paid: Elaine
   250  Elaine
   100  Guybrush
    45  Meathook
    40  Otis""")}
    <p>
      Those square-bracket lines are list comprehensions, which is the next lesson. Even
      before you can write them, you can read them: "the name of m, for every m in crew".
    </p>

    <h2>Grouping</h2>
    {code('''crew = [
    {"name": "Guybrush", "role": "captain"},
    {"name": "Otis", "role": "lookout"},
    {"name": "Meathook", "role": "lookout"},
]

by_role = {}
for member in crew:
    role = member["role"]
    by_role.setdefault(role, []).append(member["name"])

for role, names in by_role.items():
    print(f"{role}: {', '.join(names)}")''',
          expect="""captain: Guybrush
lookout: Otis, Meathook""")}
    <p>
      <code>setdefault(key, [])</code> means "give me the list at this key, creating an empty
      one first if needed". It is the standard grouping idiom. The tidier alternative:
    </p>
    {code('''from collections import defaultdict

pairs = [("captain", "Guybrush"), ("lookout", "Otis"), ("lookout", "Meathook")]

by_role = defaultdict(list)
for role, name in pairs:
    by_role[role].append(name)

print(dict(by_role))''',
          expect="{'captain': ['Guybrush'], 'lookout': ['Otis', 'Meathook']}")}

    <h2>Navigating safely when data is missing</h2>
    {code('''response = {"user": {"profile": {"name": "Elaine"}}}
broken = {"user": {}}

print(response["user"]["profile"]["name"])

# this would raise KeyError on `broken`
name = broken.get("user", {}).get("profile", {}).get("name", "unknown")
print(name)''',
          expect="""Elaine
unknown""")}
    <p>
      Chained <code>.get()</code> calls with <code>{{}}</code> as the default let you walk a
      deep structure without exploding when a level is missing. Real API responses are missing
      fields constantly, and this pattern is the difference between a script that survives
      contact with reality and one that does not.
    </p>

    <h2>Shallow copies bite here</h2>
    {code('''import copy

original = {"name": "ship", "crew": ["Otis", "Meathook"]}

shallow = original.copy()
deep = copy.deepcopy(original)

shallow["crew"].append("Stowaway")

print("original:", original["crew"])
print("deep:    ", deep["crew"])''',
          expect="""original: ['Otis', 'Meathook', 'Stowaway']
deep:     ['Otis', 'Meathook']""")}

    {voice("PARANOIA", "Medium: Success",
           "The shallow copy copied the outer dictionary and then pointed at the very same "
           "inner list. You changed something you believed you owned and altered the original "
           "from a distance. This is the bug that takes a whole afternoon, because the line "
           "that breaks is nowhere near the line that caused it.",
           "copy.deepcopy() copies all the way down. It is slower. Use it when you mean it.")}

    <h2>Printing nested data readably</h2>
    {code('''import json

game = {
    "title": "Monkey Island",
    "crew": [{"name": "Guybrush", "insults": 8}],
}

print(game)
print()
print(json.dumps(game, indent=2))''',
          expect="""{'title': 'Monkey Island', 'crew': [{'name': 'Guybrush', 'insults': 8}]}

{
  "title": "Monkey Island",
  "crew": [
    {
      "name": "Guybrush",
      "insults": 8
    }
  ]
}""")}
    <p>
      <code>json.dumps(x, indent=2)</code> is the fastest way to see the shape of confusing
      data. Keep it in your fingers. There is also <code>pprint</code> in the standard library,
      which does the same job while keeping Python's own notation.
    </p>

    {exercise(1, "Report from records",
              "<p>From this data, print each film with its average rating to one decimal "
              "place, sorted best first.</p>"
              + code('''films = [
    {"title": "Monkey Island", "ratings": [9, 8, 10]},
    {"title": "Disco Elysium", "ratings": [10, 10, 9]},
    {"title": "Grim Fandango", "ratings": [9, 9, 9]},
]''', run=False, verify="compile"),
              code('''films = [
    {"title": "Monkey Island", "ratings": [9, 8, 10]},
    {"title": "Disco Elysium", "ratings": [10, 10, 9]},
    {"title": "Grim Fandango", "ratings": [9, 9, 9]},
]

def average(film):
    return sum(film["ratings"]) / len(film["ratings"])


for film in sorted(films, key=average, reverse=True):
    print(f"{film['title']:15} {average(film):.1f}")''',
                   expect="""Disco Elysium   9.7
Monkey Island   9.0
Grim Fandango   9.0""")
              + "<p>Giving the key function a name instead of using a lambda makes this read "
              "beautifully: 'sorted by average, biggest first'.</p>")}

    {exercise(2, "Invert the structure",
              "<p>Turn a dictionary of person to skills into a dictionary of skill to the "
              "people who have it.</p>"
              + code('''people = {
    "Guybrush": ["insults", "sailing"],
    "Elaine": ["politics", "sailing"],
    "Otis": ["complaining"],
}''', run=False, verify="compile"),
              code('''people = {
    "Guybrush": ["insults", "sailing"],
    "Elaine": ["politics", "sailing"],
    "Otis": ["complaining"],
}

by_skill = {}
for person, skills in people.items():
    for skill in skills:
        by_skill.setdefault(skill, []).append(person)

for skill in sorted(by_skill):
    print(f"{skill:12} {', '.join(by_skill[skill])}")''',
                   expect="""complaining  Otis
insults      Guybrush
politics     Elaine
sailing      Guybrush, Elaine""")
              + "<p>A loop inside a loop over nested data, building a new nested structure. "
              "This exact shape appears in search indexes, tag clouds and recommendation "
              "systems.</p>")}

    {exercise(3, "Survive the missing field",
              "<p>Print each user's city, using 'unknown' when any part of the path is "
              "missing. Do not let it crash.</p>"
              + code('''users = [
    {"name": "Elaine", "address": {"city": "Melee"}},
    {"name": "Otis", "address": {}},
    {"name": "Guybrush"},
]''', run=False, verify="compile"),
              code('''users = [
    {"name": "Elaine", "address": {"city": "Melee"}},
    {"name": "Otis", "address": {}},
    {"name": "Guybrush"},
]

for user in users:
    city = user.get("address", {}).get("city", "unknown")
    print(f"{user['name']:10} {city}")''',
                   expect="""Elaine     Melee
Otis       unknown
Guybrush   unknown"""))}
""",
)

# ---------------------------------------------------------------- 16
_add(
    level=2,
    num="16",
    slug="16-comprehensions",
    id="py-16-comprehensions",
    card="Build a whole list in one line. The most Python-looking thing in Python.",
    title="Comprehensions",
    emoji="✨",
    desc="List, dict and set comprehensions, filtering, and when a comprehension is the wrong choice.",
    lede="""Take a loop that builds a list, and fold it into a single line that reads like a
    sentence. Used well this is Python at its best. Used badly it is a war crime.""",
    body=f"""
    <h2>From loop to comprehension</h2>
    <p>Here is the loop you already know:</p>
    {code('''squares = []
for n in range(1, 6):
    squares.append(n * n)
print(squares)''',
          expect="[1, 4, 9, 16, 25]")}
    <p>And here it is again:</p>
    {code('''squares = [n * n for n in range(1, 6)]
print(squares)''',
          expect="[1, 4, 9, 16, 25]")}
    <p>
      The pieces are the same, rearranged. The thing you append comes first, then the loop.
      Read it aloud: "n times n, for each n in one to five".
    </p>
    {out("""[  n * n     for n in range(1, 6)  ]
   ^^^^^     ^^^^^^^^^^^^^^^^^^^^
   what      where it comes from
   you keep""")}

    <h2>Adding a filter</h2>
    {code('''numbers = [4, 9, 15, 22, 30, 7]

evens = [n for n in numbers if n % 2 == 0]
print(evens)

big_doubled = [n * 2 for n in numbers if n > 10]
print(big_doubled)''',
          expect="""[4, 22, 30]
[30, 44, 60]""")}
    <p>The <code>if</code> goes at the end and decides what gets in. Reading order:</p>
    <ol>
      <li>Take each <code>n</code> from <code>numbers</code>,</li>
      <li>keep it only if the condition is true,</li>
      <li>and put <code>n * 2</code> in the new list.</li>
    </ol>

    <h2>Transforming text</h2>
    {code('''crew = ["  guybrush ", "ELAINE", " otis  "]

tidy = [name.strip().title() for name in crew]
print(tidy)

lengths = [len(name) for name in tidy]
print(lengths)

initials = [name[0] for name in tidy]
print(initials)''',
          expect="""['Guybrush', 'Elaine', 'Otis']
[8, 6, 4]
['G', 'E', 'O']""")}

    <h2>Dictionary and set comprehensions</h2>
    {code('''words = ["grog", "sword", "map"]

lengths = {word: len(word) for word in words}
print(lengths)

first_letters = {word[0] for word in words}
print(sorted(first_letters))

scores = {"Guybrush": 95, "Elaine": 88, "Otis": 42}
passed = {name: score for name, score in scores.items() if score >= 50}
print(passed)''',
          expect="""{'grog': 4, 'sword': 5, 'map': 3}
['g', 'm', 's']
{'Guybrush': 95, 'Elaine': 88}""")}
    <p>
      Same syntax, different brackets. <code>[ ]</code> makes a list, <code>{{ }}</code> with a
      colon makes a dictionary, <code>{{ }}</code> without makes a set. Filtering a dictionary
      down to the entries you want is one of the most useful lines in day-to-day Python.
    </p>

    <h2>The conditional version</h2>
    {code('''numbers = [4, 9, 15, 22]

labels = ["even" if n % 2 == 0 else "odd" for n in numbers]
print(labels)''',
          expect="['even', 'odd', 'odd', 'even']")}
    {callout("warn", "🤔 Two different ifs, two different places",
             "<p><code>[x for x in items if cond]</code> filters: the if is at the end and "
             "decides what is included. <code>[a if cond else b for x in items]</code> "
             "chooses: the if is at the front and decides what value each item becomes. If you "
             "need an <code>else</code>, it goes at the front. This trips up everyone.</p>")}

    <h2>Nested loops in a comprehension</h2>
    {code('''pairs = [(a, b) for a in "AB" for b in [1, 2]]
print(pairs)

grid = [[1, 2], [3, 4], [5, 6]]
flat = [n for row in grid for n in row]
print(flat)''',
          expect="""[('A', 1), ('A', 2), ('B', 1), ('B', 2)]
[1, 2, 3, 4, 5, 6]""")}
    <p>
      The loops read in the same order you would write them normally: outer first, inner
      second. Flattening a list of lists is the common case and worth memorising as a phrase.
    </p>

    <h2>Generator expressions: the lazy cousin</h2>
    {code('''numbers = range(1, 1_000_001)

# builds a million-item list in memory first
total_list = sum([n * n for n in numbers])

# produces one value at a time and never stores them all
total_gen = sum(n * n for n in numbers)

print(total_list == total_gen)
print(f"{total_gen:,}")''',
          expect="""True
333,333,833,333,500,000""")}
    <p>
      Round brackets (or none at all, inside a function call) give you a
      <strong>generator expression</strong>: it computes values on demand instead of building
      the whole list. For a million squares that is the difference between using about 40MB of
      memory and using almost none. When you are feeding straight into
      <code>sum</code>, <code>max</code>, <code>any</code> or a <code>for</code> loop, drop the
      square brackets. Lesson 34 goes deeper.
    </p>

    <h2>any and all</h2>
    {code('''scores = [95, 88, 42, 71]

print(any(s < 50 for s in scores))
print(all(s >= 40 for s in scores))
print(sum(1 for s in scores if s >= 70))''',
          expect="""True
True
3""")}
    <p>
      <code>any</code> and <code>all</code> plus a generator expression is how you ask "is
      there at least one" and "is every single one" in a single readable line. They also stop
      early as soon as the answer is decided.
    </p>

    <h2>When not to use one</h2>
    {code('''# Do not do this to people.
result = [y for x in range(10) if x % 2 == 0 for y in range(x) if y % 3 == 0 and y > 1]
print(result)''',
          expect="[3, 3, 3, 6]")}

    {voice("RHETORIC", "Medium: Success",
           "You wrote it, and today you understand it. That is not the test. The test is "
           "whether a colleague can read it at speed on a Friday afternoon, or whether you can "
           "in March.",
           "If a comprehension needs more than one loop and one condition, or it does not fit "
           "comfortably on one line, write the loop. Nobody has ever been fired for clarity.")}

    <p>Also: if the loop is doing something rather than collecting something, use a loop.</p>
    {code('''# wrong: building a list of Nones purely for the side effect
# [print(n) for n in range(3)]

# right
for n in range(3):
    print(n)''',
          expect="""0
1
2""")}

    {exercise(1, "Rewrite as comprehensions",
              "<p>Turn each of these into one line.</p>"
              + code('''# A
result = []
for word in ["grog", "map", "sword"]:
    result.append(word.upper())

# B
long_words = []
for word in ["grog", "a", "sword", "of"]:
    if len(word) > 2:
        long_words.append(word)

# C
lengths = {}
for word in ["grog", "map"]:
    lengths[word] = len(word)''', run=False, verify="compile"),
              code('''result = [word.upper() for word in ["grog", "map", "sword"]]
long_words = [w for w in ["grog", "a", "sword", "of"] if len(w) > 2]
lengths = {word: len(word) for word in ["grog", "map"]}

print(result)
print(long_words)
print(lengths)''',
                   expect="""['GROG', 'MAP', 'SWORD']
['grog', 'sword']
{'grog': 4, 'map': 3}"""))}

    {exercise(2, "FizzBuzz in one line",
              "<p>Produce a list of the FizzBuzz results for 1 to 15 using a single "
              "comprehension. Then decide whether you would actually ship it.</p>",
              code('''result = [
    "FizzBuzz" if n % 15 == 0
    else "Fizz" if n % 3 == 0
    else "Buzz" if n % 5 == 0
    else str(n)
    for n in range(1, 16)
]
print(result)''',
                   expect="['1', '2', 'Fizz', '4', 'Buzz', 'Fizz', '7', '8', 'Fizz', 'Buzz', '11', 'Fizz', '13', '14', 'FizzBuzz']")
              + "<p>It works, and chained conditional expressions are legal. Would you ship "
              "it? Probably not: the loop version from Lesson 9 is clearer and just as short "
              "in practice. The right answer to 'can Python do this in one line' is often "
              "'yes, and no'.</p>")}

    {exercise(3, "Filter records",
              "<p>From a list of dictionaries, produce a list of the names of everyone paid "
              "more than 50, sorted alphabetically.</p>"
              + code('''crew = [
    {"name": "Guybrush", "pay": 100},
    {"name": "Otis", "pay": 40},
    {"name": "Elaine", "pay": 250},
    {"name": "Meathook", "pay": 45},
]''', run=False, verify="compile"),
              code('''crew = [
    {"name": "Guybrush", "pay": 100},
    {"name": "Otis", "pay": 40},
    {"name": "Elaine", "pay": 250},
    {"name": "Meathook", "pay": 45},
]

well_paid = sorted(m["name"] for m in crew if m["pay"] > 50)
print(well_paid)''',
                   expect="['Elaine', 'Guybrush']")
              + "<p>A generator expression passed straight to <code>sorted</code>, with no "
              "intermediate list. This is what fluent Python looks like: not clever, just "
              "direct.</p>")}
""",
)

# ---------------------------------------------------------------- 17
_add(
    level=2,
    num="17",
    slug="17-functions",
    id="py-17-functions",
    card="Bundle steps under a name. The single most important idea in programming.",
    title="Functions: Naming a Process",
    emoji="🧩",
    desc="def, arguments, return values, docstrings, and why functions are how programs stay understandable.",
    lede="""Everything so far has been one long strip of instructions. Functions let you cut
    that strip into named pieces, and that is what makes big programs possible at all.""",
    body=f"""
    <h2>Defining and calling</h2>
    {code('''def greet():
    print("Welcome to the Scumm Bar.")
    print("Mind the grog.")


greet()
greet()''',
          expect="""Welcome to the Scumm Bar.
Mind the grog.
Welcome to the Scumm Bar.
Mind the grog.""")}
    <p>Three parts:</p>
    <ul>
      <li><code>def</code> means "define". You are describing a process, not doing it yet.</li>
      <li>The name, the brackets and a colon.</li>
      <li>An indented block: the body.</li>
    </ul>
    <p>
      Defining a function runs nothing. The body only executes when you <em>call</em> it, by
      writing its name with brackets. Forgetting the brackets is a classic: <code>greet</code>
      is the function itself, <code>greet()</code> is the act of running it.
    </p>

    <h2>Arguments: information going in</h2>
    {code('''def greet(name):
    print(f"Welcome, {name}.")


greet("Guybrush")
greet("Elaine")''',
          expect="""Welcome, Guybrush.
Welcome, Elaine.""")}
    {code('''def describe(name, role, insults):
    print(f"{name} the {role} knows {insults} insults.")


describe("Guybrush", "pirate", 8)
describe(role="governor", name="Elaine", insults=3)''',
          expect="""Guybrush the pirate knows 8 insults.
Elaine the governor knows 3 insults.""")}
    <p>
      Passing by position is the default. Passing by name (keyword arguments) works in any
      order and makes the call site far easier to read, especially when there are booleans
      involved: <code>send(urgent=True)</code> beats <code>send(True)</code> every time.
    </p>

    <h2>return: information coming out</h2>
    {code('''def double(n):
    return n * 2


result = double(21)
print(result)
print(double(double(5)))''',
          expect="""42
20""")}

    {callout("danger", "🪤 print is not return",
             "<p>This is the most common confusion of Level 2. <code>print</code> shows "
             "something to a human and produces nothing. <code>return</code> hands a value "
             "back to the code that called the function. A function that prints cannot be used "
             "in a calculation; a function that returns can be used anywhere.</p>")}
    {code('''def add_printing(a, b):
    print(a + b)


def add_returning(a, b):
    return a + b


x = add_printing(2, 3)
y = add_returning(2, 3)

print(f"x is {x}")
print(f"y is {y}")
print(add_returning(1, 1) + add_returning(2, 2))''',
          expect="""5
x is None
y is 5
6""")}
    <p>
      <code>add_printing</code> returned <code>None</code>, because a function with no
      <code>return</code> returns <code>None</code>. That <code>None</code> then poisons
      whatever you do with it. Rule of thumb: <strong>functions should return values and let
      the caller decide about printing</strong>. It makes them testable, reusable, and
      combinable.
    </p>

    <h2>return exits immediately</h2>
    {code('''def check_age(age):
    if age < 0:
        return "That is not an age."
    if age < 18:
        return "Too young."
    return "Welcome."


print(check_age(-5))
print(check_age(12))
print(check_age(30))''',
          expect="""That is not an age.
Too young.
Welcome.""")}
    <p>
      The moment a <code>return</code> runs, the function is over: nothing after it executes.
      This "early return" style flattens what would otherwise be nested <code>if/else</code>
      pyramids, and it is generally considered better than one exit point at the bottom.
    </p>

    <h2>Docstrings: telling the next person</h2>
    {code('''def split_bill(total, people, tip_rate=0.15):
    """Work out what each person owes, including tip.

    Args:
        total: the bill before tip
        people: how many are splitting it
        tip_rate: as a fraction, so 0.15 means 15 percent

    Returns:
        The amount each person owes, as a float.
    """
    return (total * (1 + tip_rate)) / people


print(f"{split_bill(87.50, 4):.2f}")
print(split_bill.__doc__.splitlines()[0])
help(split_bill)''',
          expect='''25.16
Work out what each person owes, including tip.
Help on function split_bill in module __main__:

split_bill(total, people, tip_rate=0.15)
    Work out what each person owes, including tip.

    Args:
        total: the bill before tip
        people: how many are splitting it
        tip_rate: as a fraction, so 0.15 means 15 percent

    Returns:
        The amount each person owes, as a float.
''')}
    <p>
      A string as the first line of a function body becomes its documentation. It is not a
      comment: Python keeps it, <code>help()</code> prints it, your editor shows it on hover,
      and documentation tools generate whole websites from it. Write one for anything that is
      not instantly obvious.
    </p>

    <h2>Why functions actually matter</h2>
    {code('''def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32


for city, temp in [("Melee", 28), ("Booty", 31), ("Blood", 19)]:
    print(f"{city:8} {temp}C = {celsius_to_fahrenheit(temp):.1f}F")''',
          expect="""Melee    28C = 82.4F
Booty    31C = 87.8F
Blood    19C = 66.2F""")}
    <p>Four reasons, in order of importance:</p>
    <ol>
      <li><strong>Naming.</strong> <code>celsius_to_fahrenheit(t)</code> says what it is.
      <code>t * 9 / 5 + 32</code> makes the reader do the work every time.</li>
      <li><strong>One place to fix.</strong> A bug in the formula gets fixed once, not in nine
      scattered copies, one of which you will miss.</li>
      <li><strong>Testability.</strong> You can check a function in isolation (Lesson 29).
      You cannot easily test line 47 of a long script.</li>
      <li><strong>Thinking.</strong> A named function is a concept you can hold in your head
      as one thing, which is how you fit a big program into a small skull.</li>
    </ol>

    {voice("CONCEPTUALIZATION", "Formidable: Success",
           "This is the whole trick of software, and it never stops working. You cannot hold "
           "ten thousand lines in your mind. You can hold twenty names. Each name hides a "
           "hundred lines you have already stopped worrying about.",
           "Every abstraction you will ever meet, functions, classes, modules, packages, "
           "services, is this same move performed at a larger scale.")}

    <h2>A worked example: refactoring</h2>
    {code('''# Before: one long strip, hard to follow, impossible to test
crew = [{"name": "Guybrush", "pay": 100}, {"name": "Otis", "pay": 40}]
total = 0
for m in crew:
    total += m["pay"]
avg = total / len(crew)
print(f"Total {total}, average {avg:.1f}")
for m in crew:
    if m["pay"] < avg:
        print(f"{m['name']} is paid below average")''',
          expect="""Total 140, average 70.0
Otis is paid below average""")}
    {code('''def total_pay(crew):
    """Sum everyone's pay."""
    return sum(member["pay"] for member in crew)


def average_pay(crew):
    """Mean pay across the crew."""
    return total_pay(crew) / len(crew)


def below_average(crew):
    """Names of everyone paid less than the mean."""
    threshold = average_pay(crew)
    return [m["name"] for m in crew if m["pay"] < threshold]


crew = [{"name": "Guybrush", "pay": 100}, {"name": "Otis", "pay": 40}]

print(f"Total {total_pay(crew)}, average {average_pay(crew):.1f}")
for name in below_average(crew):
    print(f"{name} is paid below average")''',
          expect="""Total 140, average 70.0
Otis is paid below average""")}
    <p>
      Longer, and much better. Each piece has a name, does one thing, and can be tested on its
      own. The last four lines now read like a description of the task rather than an
      implementation of it.
    </p>

    {exercise(1, "Temperature converter",
              "<p>Write two functions that convert both ways, and prove they round-trip.</p>",
              code('''def c_to_f(celsius):
    """Convert Celsius to Fahrenheit."""
    return celsius * 9 / 5 + 32


def f_to_c(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    return (fahrenheit - 32) * 5 / 9


print(c_to_f(100))
print(f_to_c(212))
print(f_to_c(c_to_f(37)))''',
                   expect="""212.0
100.0
37.0"""))}

    {exercise(2, "Is it a palindrome?",
              "<p>Write <code>is_palindrome(text)</code> that returns True or False, ignoring "
              "case, spaces and punctuation. Test it on several phrases.</p>",
              code('''def is_palindrome(text):
    """True if text reads the same backwards, ignoring case and punctuation."""
    cleaned = "".join(c.lower() for c in text if c.isalnum())
    return cleaned == cleaned[::-1]


for phrase in ["Never odd or even", "A man, a plan, a canal: Panama", "Monkey Island"]:
    print(f"{is_palindrome(phrase)!s:6} {phrase}")''',
                   expect="""True   Never odd or even
True   A man, a plan, a canal: Panama
False  Monkey Island""")
              + "<p><code>.isalnum()</code> is True for letters and digits only, which strips "
              "punctuation and spaces in one go. <code>{{value!s:6}}</code> converts to a "
              "string first so the width padding applies.</p>")}

    {exercise(3, "Grade calculator",
              "<p>Write <code>grade(score)</code> returning a letter, and a second function "
              "that takes a dictionary of names to scores and prints a report sorted by score. "
              "Neither function should print anything except the report one.</p>",
              code('''def grade(score):
    """Convert a percentage to a letter grade."""
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def report(scores):
    """Print every student, best first, with their letter grade."""
    for name, score in sorted(scores.items(), key=lambda pair: pair[1], reverse=True):
        print(f"{name:10} {score:3}  {grade(score)}")


report({"Guybrush": 95, "Otis": 58, "Elaine": 82, "Meathook": 71})''',
                   expect="""Guybrush    95  A
Elaine      82  B
Meathook    71  C
Otis        58  F""")
              + "<p><code>grade</code> is a pure function: same input, same output, no side "
              "effects. Those are the easiest things in the world to test and to trust.</p>")}
""",
)

# ---------------------------------------------------------------- 18
_add(
    level=2,
    num="18",
    slug="18-arguments",
    id="py-18-arguments",
    card="Defaults, *args, **kwargs, and the mutable default argument: Python's most famous gotcha.",
    title="Arguments in Depth",
    emoji="🎛️",
    desc="Default values, keyword-only arguments, *args and **kwargs, and the mutable default trap.",
    lede="""Python's argument handling is unusually flexible, which makes functions pleasant
    to call and hides exactly one legendary landmine.""",
    body=f"""
    <h2>Default values</h2>
    {code('''def greet(name, greeting="Welcome"):
    return f"{greeting}, {name}."


print(greet("Guybrush"))
print(greet("Elaine", "Good evening"))
print(greet("Otis", greeting="Get out"))''',
          expect="""Welcome, Guybrush.
Good evening, Elaine.
Get out, Otis.""")}
    <p>
      Arguments with defaults are optional and must come after the ones without. Defaults are
      how a function grows new abilities without breaking every existing call, which matters
      enormously once other people use your code.
    </p>

    <h2>The famous landmine</h2>
    {code('''def add_crew(name, crew=[]):        # do NOT do this
    crew.append(name)
    return crew


print(add_crew("Guybrush"))
print(add_crew("Elaine"))
print(add_crew("Otis"))''',
          expect="""['Guybrush']
['Guybrush', 'Elaine']
['Guybrush', 'Elaine', 'Otis']""")}

    {voice("PARANOIA", "Legendary: Success",
           "Look at it. Every call was supposed to start from an empty list, and they are all "
           "sharing one.",
           "The default value is created once, when the function is defined, not each time it "
           "is called. There is exactly one list, it lives on the function object itself, and "
           "every call that does not pass its own gets that same one. It has been quietly "
           "accumulating since the program started.")}

    <p>The fix is always the same:</p>
    {code('''def add_crew(name, crew=None):
    if crew is None:
        crew = []
    crew.append(name)
    return crew


print(add_crew("Guybrush"))
print(add_crew("Elaine"))
print(add_crew("Otis", ["LeChuck"]))''',
          expect="""['Guybrush']
['Elaine']
['LeChuck', 'Otis']""")}
    {callout("danger", "📏 The rule, memorised in one line",
             "<p><strong>Never use a mutable value as a default.</strong> Not a list, not a "
             "dictionary, not a set. Use <code>None</code> and create it inside. Numbers, "
             "strings, tuples and booleans are immutable and perfectly safe.</p>")}

    <h2>*args: any number of positional arguments</h2>
    {code('''def total(*numbers):
    print(f"got {numbers} which is a {type(numbers).__name__}")
    return sum(numbers)


print(total(1, 2, 3))
print(total(10, 20))
print(total())''',
          expect="""got (1, 2, 3) which is a tuple
6
got (10, 20) which is a tuple
30
got () which is a tuple
0""")}
    <p>
      The star collects every extra positional argument into a tuple. The name
      <code>args</code> is pure convention; the star is what does the work.
    </p>

    <h2>**kwargs: any number of named arguments</h2>
    {code('''def describe(**details):
    for key, value in details.items():
        print(f"{key:10} {value}")


describe(name="Guybrush", role="pirate", insults=8)''',
          expect="""name       Guybrush
role       pirate
insults    8""")}
    <p>Two stars collect named arguments into a dictionary. Both together:</p>
    {code('''def log(message, *tags, level="INFO", **extra):
    tag_text = f" [{' '.join(tags)}]" if tags else ""
    extra_text = "".join(f" {k}={v}" for k, v in extra.items())
    print(f"{level}: {message}{tag_text}{extra_text}")


log("Ship departed")
log("Ship sank", "urgent", "nautical", level="ERROR", depth=40, souls=12)''',
          expect="""INFO: Ship departed
ERROR: Ship sank [urgent nautical] depth=40 souls=12""")}
    <p>
      The order is fixed and worth remembering: positional, <code>*args</code>,
      keyword-with-defaults, <code>**kwargs</code>. You will see this signature constantly in
      library code, and now it is not mysterious.
    </p>

    <h2>Unpacking at the call site</h2>
    {code('''def make_pirate(name, role, insults):
    return f"{name} the {role} ({insults} insults)"


details = ["Guybrush", "pirate", 8]
print(make_pirate(*details))

as_dict = {"name": "Elaine", "role": "governor", "insults": 3}
print(make_pirate(**as_dict))''',
          expect="""Guybrush the pirate (8 insults)
Elaine the governor (3 insults)""")}
    <p>
      The same stars work in reverse when calling: <code>*</code> spreads a list into
      positional arguments, <code>**</code> spreads a dictionary into named ones. This is how
      you pass configuration around without writing out every field.
    </p>

    <h2>Forcing arguments to be named</h2>
    {code('''def transfer(amount, *, from_account, to_account):
    return f"Moving {amount} from {from_account} to {to_account}"


print(transfer(100, from_account="checking", to_account="savings"))
# transfer(100, "checking", "savings")   # TypeError: takes 1 positional argument''',
          expect="Moving 100 from checking to savings")}
    <p>
      A bare <code>*</code> in the signature means "everything after this must be passed by
      name". Use it whenever the arguments could be confused with each other. Nobody has ever
      swapped two accounts by accident when the names were required.
    </p>
    <p>
      There is a mirror feature: a <code>/</code> in the signature marks arguments that must be
      positional. You will see it in the standard library's documentation and rarely need to
      write it.
    </p>

    <h2>Mutable arguments change the caller's data</h2>
    {code('''def add_item(inventory, item):
    inventory.append(item)          # changes the caller's list


def add_item_safely(inventory, item):
    return inventory + [item]       # returns a new list


bag = ["map"]
add_item(bag, "grog")
print(bag)

bag2 = ["map"]
new_bag = add_item_safely(bag2, "grog")
print(bag2, new_bag)''',
          expect="""['map', 'grog']
['map'] ['map', 'grog']""")}
    <p>
      Both are legitimate designs. What matters is that you choose deliberately and say so in
      the name and the docstring. A function that quietly modifies what you handed it is a
      function that will surprise someone, and the someone is usually you.
    </p>

    {exercise(1, "Flexible greeter",
              "<p>Write <code>greet</code> that takes any number of names, plus an optional "
              "greeting and an optional excited flag that adds an exclamation mark. The flag "
              "must be keyword-only.</p>",
              code('''def greet(*names, greeting="Hello", excited=False):
    """Greet everyone by name."""
    if not names:
        return f"{greeting}, nobody."
    joined = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else names[0]
    end = "!" if excited else "."
    return f"{greeting}, {joined}{end}"


print(greet("Guybrush"))
print(greet("Guybrush", "Elaine"))
print(greet("Guybrush", "Elaine", "Otis", greeting="Ahoy", excited=True))
print(greet())''',
                   expect="""Hello, Guybrush.
Hello, Guybrush and Elaine.
Ahoy, Guybrush, Elaine and Otis!
Hello, nobody."""))}

    {exercise(2, "Spot the landmine",
              "<p>This cache is meant to remember results. Why does it leak between calls, and "
              "how would you fix it while keeping the feature?</p>"
              + code('''def remember(key, value, store={}):
    store[key] = value
    return store''', run=False, verify="compile"),
              "<p>It is the mutable default again, except here the sharing is arguably the "
              "intent: it does successfully cache. The problem is that it is invisible, "
              "un-resettable, and shared with every other caller in the program including "
              "code you did not write.</p>"
              "<p>If you want a cache, say so out loud:</p>"
              + code('''_store = {}


def remember(key, value, store=None):
    """Remember a value. Uses the module cache unless given its own store."""
    target = _store if store is None else store
    target[key] = value
    return target


print(remember("a", 1))
print(remember("b", 2))
print(remember("c", 3, store={}))''',
                     expect="""{'a': 1}
{'a': 1, 'b': 2}
{'c': 3}""")
              + "<p>Now the shared state has a name, lives at module level where a reader will "
              "see it, and can be bypassed. Python also has "
              "<code>functools.lru_cache</code> for real caching, which Lesson 35 covers.</p>")}

    {exercise(3, "Pass-through wrapper",
              "<p>Write <code>shout</code> that calls any function with any arguments and "
              "prints the result in capitals. It must work with functions you have never "
              "seen.</p>",
              code('''def shout(func, *args, **kwargs):
    """Call func with whatever it was given, and print the result loudly."""
    result = func(*args, **kwargs)
    print(str(result).upper())
    return result


def introduce(name, role="pirate"):
    return f"{name} the {role}"


shout(introduce, "Guybrush")
shout(introduce, "Elaine", role="governor")
shout(max, 3, 9, 2)''',
                   expect="""GUYBRUSH THE PIRATE
ELAINE THE GOVERNOR
9""")
              + "<p>Collecting with <code>*args, **kwargs</code> and immediately spreading "
              "them again is the standard shape of any wrapper. It is exactly how decorators "
              "work, which is Lesson 35, and you have now written the hard part of one.</p>")}
""",
)

# ---------------------------------------------------------------- 19
_add(
    level=2,
    num="19",
    slug="19-scope",
    id="py-19-scope",
    card="Where names live, why a function cannot see inside another, and the LEGB rule.",
    title="Scope: Where Names Live",
    emoji="🔭",
    desc="Local and global scope, the LEGB rule, shadowing, and why global is usually the wrong answer.",
    lede="""Every name you create lives somewhere. Knowing where saves you from the two most
    confusing errors in Python: the variable that vanished, and the one that refused to
    change.""",
    body=f"""
    <h2>What happens inside stays inside</h2>
    {code('''def make_grog():
    strength = 11          # created inside the function
    print(f"inside: {strength}")


make_grog()
# print(strength)          # NameError: name 'strength' is not defined
print("outside: cannot see it")''',
          expect="""inside: 11
outside: cannot see it""")}
    <p>
      Names created inside a function are <strong>local</strong> to it. They come into
      existence when the call starts and disappear when it ends. This is a feature: it means
      you can name a variable <code>total</code> inside a function without wondering whether
      some other function forty lines away is also using <code>total</code>.
    </p>

    <h2>Reading outwards is allowed</h2>
    {code('''ship_name = "Sea Monkey"          # global


def announce():
    print(f"Now boarding the {ship_name}")


announce()''',
          expect="Now boarding the Sea Monkey")}
    <p>
      A function can <em>read</em> names from outside. Python looks in ever-widening circles,
      which has a name you will see in every Python book: <strong>LEGB</strong>.
    </p>
    {table(
        ["Letter", "Scope", "Means"],
        [["<strong>L</strong>", "Local", "Inside this function"],
         ["<strong>E</strong>", "Enclosing", "Inside the function that contains this one"],
         ["<strong>G</strong>", "Global", "At the top level of this file"],
         ["<strong>B</strong>", "Built-in", "Python's own names: <code>print</code>, <code>len</code>, <code>str</code>"]],
    )}
    <p>Python checks them in that order and stops at the first match.</p>

    <h2>Writing outwards is not</h2>
    {code('''count = 0


def increment():
    count = count + 1       # UnboundLocalError


try:
    increment()
except UnboundLocalError as err:
    print("Error:", err)''',
          expect="Error: cannot access local variable 'count' where it is not associated with a value")}

    {voice("LOGIC", "Formidable: Success",
           "Read the rule that causes this, because it is not obvious: if a function assigns "
           "to a name anywhere in its body, Python treats that name as local for the whole "
           "function, including lines before the assignment.",
           "So count = count + 1 tries to read a local count that does not exist yet. Not the "
           "global one. The decision was made when the function was compiled, before a single "
           "line ran.")}

    <p>You can override it, and you usually should not:</p>
    {code('''count = 0


def increment():
    global count
    count += 1


increment()
increment()
print(count)''',
          expect="2")}

    <h2>Why global is usually the wrong answer</h2>
    <p>
      <code>global</code> works. It also means any function anywhere can change that value,
      so when it holds something wrong you have the entire file as your list of suspects.
      Prefer passing values in and returning them out:
    </p>
    {code('''def increment(count):
    """Return the next count. Changes nothing outside."""
    return count + 1


count = 0
count = increment(count)
count = increment(count)
print(count)''',
          expect="2")}
    <p>
      Now the function is testable, reusable, and impossible to blame for an action at a
      distance. This is the shape of a <strong>pure function</strong>: it takes values,
      returns a value, and touches nothing else. Not everything can be pure, but the parts
      that can, should be.
    </p>

    <h2>Shadowing: same name, different scope</h2>
    {code('''name = "global Guybrush"


def outer():
    name = "outer Elaine"

    def inner():
        name = "inner Otis"
        print("inner sees: ", name)

    inner()
    print("outer sees: ", name)


outer()
print("module sees:", name)''',
          expect="""inner sees:  inner Otis
outer sees:  outer Elaine
module sees: global Guybrush""")}
    <p>
      Three separate variables that happen to share a name. Each function sees its own. Legal,
      occasionally useful, and a reliable way to confuse yourself if you do it on purpose.
    </p>

    <h2>nonlocal: reaching one level out</h2>
    {code('''def counter():
    count = 0

    def increment():
        nonlocal count
        count += 1
        return count

    return increment


tally = counter()
print(tally(), tally(), tally())''',
          expect="1 2 3")}
    <p>
      <code>nonlocal</code> means "the one in the enclosing function, not a new local and not
      the global". The pattern above is a <strong>closure</strong>: <code>increment</code>
      remembers <code>count</code> even after <code>counter</code> has finished. It is the
      foundation of decorators (Lesson 35) and one of the genuinely beautiful ideas in
      programming.
    </p>

    <h2>Shadowing built-ins: the sneaky one</h2>
    {code('''list = [1, 2, 3]           # now `list` is your list, not the type
print(list)

del list                    # undo the damage
print(list((1, 2, 3)))      # the built-in is back''',
          expect="""[1, 2, 3]
[1, 2, 3]""")}
    {callout("warn", "🪤 Names to avoid",
             "<p><code>list</code>, <code>dict</code>, <code>set</code>, <code>str</code>, "
             "<code>int</code>, <code>type</code>, <code>id</code>, <code>sum</code>, "
             "<code>max</code>, <code>min</code>, <code>input</code>, <code>file</code>, "
             "<code>next</code>. Python lets you use them as variables and then the real ones "
             "stop working, usually thirty lines later, with an error that makes no sense. Add "
             "an underscore: <code>list_</code>, or better, name it what it actually is: "
             "<code>names</code>.</p>")}

    {exercise(1, "Predict the scope",
              "<p>What does this print? Work it out before running.</p>"
              + code('''x = 10


def show():
    x = 20
    print("inside:", x)


show()
print("outside:", x)''', run=False, verify="compile"),
              "<p><code>inside: 20</code> then <code>outside: 10</code>.</p>"
              "<p>The assignment inside <code>show</code> created a brand new local "
              "<code>x</code>. The global one was never touched. If you wanted to change it "
              "you would need <code>global x</code>, and you almost certainly do not want "
              "to.</p>")}

    {exercise(2, "Fix the accumulator",
              "<p>This should total a list. It raises an error. Fix it two ways: once with "
              "<code>global</code>, once properly.</p>"
              + code('''total = 0


def add(n):
    total += n


add(5)''', run=False, verify="skip"),
              "<p>The quick fix:</p>"
              + code('''total = 0


def add(n):
    global total
    total += n


add(5)
add(10)
print(total)''', expect="15")
              + "<p>The one you should ship:</p>"
              + code('''def add(total, n):
    """Return the new total."""
    return total + n


total = 0
total = add(total, 5)
total = add(total, 10)
print(total)

# or simply
print(sum([5, 10]))''', expect="""15
15""")
              + "<p>The second version can be tested in one line and cannot be broken by "
              "anything else in the program. And once it is written that way, you notice "
              "Python already has <code>sum</code>.</p>")}

    {exercise(3, "Build a bank account with a closure",
              "<p>Write a function that returns two functions: one to deposit and one to check "
              "the balance. The balance must not be reachable from outside except through "
              "them.</p>",
              code('''def open_account(starting=0):
    """Return (deposit, balance) functions sharing a private balance."""
    balance = starting

    def deposit(amount):
        nonlocal balance
        balance += amount
        return balance

    def check():
        return balance

    return deposit, check


deposit, check = open_account(100)

print(check())
deposit(50)
deposit(25)
print(check())''',
                   expect="""100
175""")
              + "<p>There is no way to reach <code>balance</code> from outside those two "
              "functions. That is encapsulation, achieved with nothing but scope. Classes "
              "(Lesson 31) are the more common way to do this, but closures got there "
              "first.</p>")}
""",
)

# ---------------------------------------------------------------- 20
_add(
    level=2,
    num="20",
    slug="20-modules",
    id="py-20-modules",
    card="import, your own modules, __main__, and a guided tour of the batteries Python includes.",
    title="Modules and the Standard Library",
    emoji="📚",
    desc="Importing, writing your own modules, the __main__ guard, and a tour of the most useful standard library modules.",
    lede="""Everything so far has lived in one file. Real programs are many files, and Python
    ships with hundreds of them already written for you.""",
    body=f"""
    <h2>import</h2>
    {code('''import random
import math

print(math.sqrt(16))
print(math.pi)

random.seed(42)                      # makes the "random" repeatable
print(random.randint(1, 100))
print(random.choice(["grog", "map", "sword"]))''',
          expect="""4.0
3.141592653589793
82
grog""")}
    <p>
      <code>import math</code> makes the module available, and you reach into it with a dot.
      <code>random.seed(42)</code> fixes the sequence so the same "random" numbers come out
      every time, which is invaluable for testing and for lessons like this one that promise
      you an exact output.
    </p>

    <h2>The four import styles</h2>
    {code('''import math
from math import sqrt
from math import sqrt as square_root
import statistics as stats

print(math.sqrt(9))
print(sqrt(9))
print(square_root(9))
print(stats.mean([1, 2, 3, 4]))''',
          expect="""3.0
3.0
3.0
2.5""")}
    {table(
        ["Style", "When"],
        [["<code>import x</code>", "The default. Always obvious where a name came from"],
         ["<code>from x import y</code>", "When you use y constantly and the origin is obvious"],
         ["<code>import x as y</code>", "For long names, or by convention (<code>import pandas as pd</code>)"],
         ["<code>from x import *</code>", "Never. It dumps unknown names into your file and hides collisions"]],
    )}

    <h2>Writing your own module</h2>
    <p>A module is just a <code>.py</code> file. Make <code>pirate_tools.py</code>:</p>
    {code('''"""Helpers for pirate arithmetic."""

INSULT_LIMIT = 8


def format_name(first, last):
    """Return a properly capitalised full name."""
    return f"{first.title()} {last.title()}"


def can_duel(insults):
    """True if this pirate knows enough insults to duel."""
    return insults >= INSULT_LIMIT''',
          run=False, verify="compile")}
    <p>Then, in another file in the same folder:</p>
    {code('''import pirate_tools

print(pirate_tools.format_name("guybrush", "threepwood"))
print(pirate_tools.can_duel(9))
print(pirate_tools.INSULT_LIMIT)''',
          run=False, verify="compile")}
    <p>
      That is the whole mechanism. When your file passes about two hundred lines, or when a
      group of functions clearly belong together, split them out. Future you will be grateful.
    </p>

    <h2>The __main__ guard</h2>
    {code('''def add(a, b):
    return a + b


if __name__ == "__main__":
    print("Running directly, so here is a demo:")
    print(add(2, 3))''',
          expect="""Running directly, so here is a demo:
5""")}
    <p>
      Python sets <code>__name__</code> to <code>"__main__"</code> when a file is run directly,
      and to the module's name when it is imported. So that block runs when you type
      <code>python3 thing.py</code> and stays quiet when another file imports it.
    </p>
    {callout("tip", "🎯 Why this matters",
             "<p>Without the guard, importing a module runs everything in it, including your "
             "test prints and, memorably for someone, an entire database migration. Put "
             "definitions at the top level and <em>actions</em> inside the guard. It is one of "
             "the strongest conventions in Python.</p>")}

    <h2>A tour of the batteries</h2>
    <p>
      This is the part people mean by "batteries included". Every one of these ships with
      Python and needs no installation.
    </p>

    <h3>Numbers, chance and time</h3>
    {code('''import random, statistics, datetime

random.seed(7)
rolls = [random.randint(1, 6) for _ in range(10)]
print(rolls)
print(f"mean {statistics.mean(rolls)}, median {statistics.median(rolls)}")

born = datetime.date(1990, 10, 15)
print(f"Monkey Island was released on a {born.strftime('%A')}")''',
          expect="""[3, 2, 4, 6, 1, 1, 5, 1, 3, 5]
mean 3.1, median 3.0
Monkey Island was released on a Monday""")}

    <h3>Text and data formats</h3>
    {code('''import json, textwrap

data = {"ship": "Sea Monkey", "crew": ["Otis", "Meathook"]}
encoded = json.dumps(data)
print(encoded)
print(json.loads(encoded)["crew"][0])

long = "The rubber chicken with a pulley in the middle is arguably the finest item in adventure gaming."
print(textwrap.fill(long, width=45))''',
          expect="""{"ship": "Sea Monkey", "crew": ["Otis", "Meathook"]}
Otis
The rubber chicken with a pulley in the
middle is arguably the finest item in
adventure gaming.""")}

    <h3>Collections and iteration tools</h3>
    {code('''from collections import Counter, deque
from itertools import combinations

print(Counter("mississippi").most_common(2))

queue = deque(["a", "b"])
queue.appendleft("start")
print(list(queue))

print(list(combinations(["grog", "map", "sword"], 2)))''',
          expect="""[('i', 4), ('s', 4)]
['start', 'a', 'b']
[('grog', 'map'), ('grog', 'sword'), ('map', 'sword')]""")}

    <h3>Files, paths and the system</h3>
    {code('''import sys, pathlib, os

print(sys.version_info.major, sys.version_info.minor)
p = pathlib.Path("data") / "crew.json"
print(p)
print(p.suffix, p.stem, p.parent)''',
          expect="""3 13
data/crew.json
.json crew data""")}

    <h3>The genuinely useful oddities</h3>
    {table(
        ["Module", "For"],
        [["<code>hashlib</code>", "Hashing: checksums, and password storage done properly"],
         ["<code>secrets</code>", "Cryptographically safe random values for tokens and passwords"],
         ["<code>uuid</code>", "Unique identifiers"],
         ["<code>argparse</code>", "Command-line arguments (Lesson 27)"],
         ["<code>logging</code>", "Grown-up printing (Lesson 28)"],
         ["<code>unittest</code>", "Testing without installing anything (Lesson 29)"],
         ["<code>sqlite3</code>", "A real SQL database, in one file, built in (Lesson 45)"],
         ["<code>csv</code>", "Spreadsheet data, with the quoting rules handled (Lesson 23)"],
         ["<code>re</code>", "Regular expressions (Lesson 25)"],
         ["<code>timeit</code>", "Measuring how slow something really is (Lesson 51)"]],
    )}

    {code('''import hashlib, secrets, uuid

print(hashlib.sha256(b"swordfish").hexdigest()[:16])
print(len(secrets.token_hex(16)))
print(len(str(uuid.uuid4())))''',
          expect="""b9f195c5cc7ef6af
32
36""")}

    {voice("ENCYCLOPEDIA", "Medium: Success",
           "There are over two hundred modules in there. Nobody knows them all, and nobody "
           "needs to. The valuable habit is not memorisation, it is suspicion: before you "
           "write forty lines to parse a date or shuffle a deck, spend thirty seconds "
           "searching the standard library index. The answer is there surprisingly often, and "
           "it has been tested by millions of people.")}

    <h2>Where do modules come from?</h2>
    {code('''import sys

# Python looks in these places, in order, for anything you import
for entry in sys.path[:3]:
    print(repr(entry))''',
          run=False, verify="compile")}
    <p>
      <code>sys.path</code> is the search list: your script's folder first, then the standard
      library, then installed packages. This is why a file of your own called
      <code>random.py</code> breaks everything: yours is found first, and the real one becomes
      unreachable. Do not name your files after standard modules. Everyone does it once.
    </p>

    {exercise(1, "Dice statistics",
              "<p>Roll two dice a thousand times and report how often each total appeared, as "
              "a percentage, using the standard library. Seed with 1 so your answer matches.</p>",
              code('''import random
from collections import Counter

random.seed(1)

totals = Counter(random.randint(1, 6) + random.randint(1, 6) for _ in range(1000))

for total in sorted(totals):
    pct = totals[total] / 10
    print(f"{total:2}  {'#' * int(pct):18} {pct:.1f}%")''',
                   expect=""" 2  ##                 2.6%
 3  #####              5.2%
 4  #######            7.0%
 5  ###########        11.0%
 6  ##############     14.7%
 7  ################   16.8%
 8  #############      13.6%
 9  ###########        11.4%
10  #######            7.7%
11  #######            7.1%
12  ##                 2.9%""")
              + "<p>The shape is the famous bell curve: seven is the most common total because "
              "there are six ways to roll it and only one way to roll two.</p>")}

    {exercise(2, "Build a module",
              "<p>Write <code>textstats.py</code> with three functions (word count, average "
              "word length, most common word) and a <code>__main__</code> block that "
              "demonstrates them. Then describe how another file would use it.</p>",
              code('''"""Simple statistics about a piece of text."""

from collections import Counter


def word_count(text):
    """How many words in text."""
    return len(text.split())


def average_word_length(text):
    """Mean length of the words in text, to one decimal place."""
    words = text.split()
    if not words:
        return 0.0
    return round(sum(len(w) for w in words) / len(words), 1)


def most_common_word(text):
    """The word that appears most often, lowercased."""
    words = [w.strip(".,!?").lower() for w in text.split()]
    return Counter(words).most_common(1)[0][0]


if __name__ == "__main__":
    sample = "The rubber chicken. The pulley. The middle."
    print(word_count(sample))
    print(average_word_length(sample))
    print(most_common_word(sample))''',
                   expect="""7
5.3
the""")
              + "<p>Another file would write <code>import textstats</code> then "
              "<code>textstats.word_count(essay)</code>, and the demo block would stay "
              "silent.</p>")}

    {exercise(3, "Find the module",
              "<p>For each task, name the standard library module that already does it. No "
              "code required, just the search skill.</p>"
              "<ol><li>Work out how many days until Christmas.</li>"
              "<li>Generate a secure password reset token.</li>"
              "<li>Read a spreadsheet exported as CSV where some fields contain commas.</li>"
              "<li>Zip up a folder for backup.</li>"
              "<li>Pretty-print a deeply nested dictionary.</li>"
              "<li>Find every file ending in .jpg in a folder tree.</li></ol>",
              "<ol><li><code>datetime</code>, subtracting two dates gives a "
              "<code>timedelta</code>.</li>"
              "<li><code>secrets</code>. Not <code>random</code>, which is predictable and "
              "explicitly documented as unsuitable for security.</li>"
              "<li><code>csv</code>. Splitting on commas by hand breaks on the first quoted "
              "field, guaranteed.</li>"
              "<li><code>shutil.make_archive</code>, or <code>zipfile</code> for more "
              "control.</li>"
              "<li><code>pprint</code>, or <code>json.dumps(x, indent=2)</code>.</li>"
              "<li><code>pathlib</code>: <code>Path('.').rglob('*.jpg')</code>.</li></ol>"
              "<p>The skill being trained here is the reflex to look before you build. It is "
              "worth more than any individual module.</p>")}

    {callout("info", "🎉 That is Level 2",
             "<p>Lists, tuples, dictionaries, sets, nested data, comprehensions, functions, "
             "arguments, scope and modules. You now have the toolbox that the rest of Python "
             "is built out of. Take the <a href='../quiz.html'>Level 2 quiz</a>, and build "
             "something from the <a href='../build/index.html'>workshop</a> before Level 3 "
             "turns your scripts into software.</p>")}
""",
)
