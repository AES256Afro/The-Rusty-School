"""Level 4: Pythonic.

Objects, generators, decorators, context managers, typing and
concurrency. Everything here has a plainer alternative you already know.
The point of this level is that these are the idioms other Python
programmers expect to read.
"""

from __future__ import annotations

from .kit import callout, code, exercise, link, out, repl, table, tb, term, voice

LESSONS = []


def _add(**kw):
    LESSONS.append(kw)


# ---------------------------------------------------------------- 31
_add(
    level=4,
    num="31",
    slug="31-classes",
    id="py-31-classes",
    card="Bundle data and the things that act on it into one named thing.",
    title="Classes and Objects",
    emoji="🏛️",
    desc="Defining classes, __init__, self, instance versus class attributes, and when a class is the wrong answer.",
    lede="""You have been using objects since Lesson 1: every string, list and dictionary is
    one. This is the lesson where you build your own.""",
    body=f"""
    <h2>The problem a class solves</h2>
    {code('''# Without a class: data and behaviour drift apart
guybrush = {"name": "Guybrush", "insults": 7, "hp": 100}


def take_damage(pirate, amount):
    pirate["hp"] -= amount
    return pirate["hp"]


print(take_damage(guybrush, 30))
print(guybrush["hp"])''',
          expect="""70
70""")}
    <p>
      That works. It also has nothing stopping you writing <code>guybrush["hp"]</code> in one
      place and <code>guybrush["health"]</code> in another, or calling
      <code>take_damage</code> on a dictionary that represents a ship. A class ties the shape
      of the data to the operations that are allowed on it, and gives the pair a name.
    </p>

    <h2>Your first class</h2>
    {code('''class Pirate:
    """Someone with a name, some insults and a will to live."""

    def __init__(self, name, insults=0):
        self.name = name
        self.insults = insults
        self.hp = 100

    def learn(self, insult):
        self.insults += 1
        return f"{self.name} learns: {insult}"

    def take_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        return self.hp


guybrush = Pirate("Guybrush", insults=3)
elaine = Pirate("Elaine")

print(guybrush.name, guybrush.insults, guybrush.hp)
print(elaine.name, elaine.insults, elaine.hp)
print(guybrush.learn("You fight like a dairy farmer!"))
print(guybrush.insults, elaine.insults)
print(guybrush.take_damage(30))''',
          expect="""Guybrush 3 100
Elaine 0 100
Guybrush learns: You fight like a dairy farmer!
4 0
70""")}

    {table(
        ["Word", "Means"],
        [["<code>class Pirate:</code>", "A blueprint. No pirate exists yet"],
         ["<code>Pirate(\"Guybrush\")</code>", "Build one. This is an <strong>instance</strong>"],
         ["<code>__init__</code>", "Runs automatically when an instance is built. Set up the data here"],
         ["<code>self</code>", "The particular instance this call is about"],
         ["<code>self.name = name</code>", "An <strong>attribute</strong>: data belonging to this instance"],
         ["<code>def learn(self, ...)</code>", "A <strong>method</strong>: a function belonging to the class"]],
    )}

    <h2>self, demystified</h2>
    {code('''class Counter:
    def __init__(self):
        self.count = 0

    def bump(self):
        self.count += 1


a = Counter()
b = Counter()

a.bump()
a.bump()
b.bump()

print(a.count, b.count)

# a.bump() is literally shorthand for this
Counter.bump(a)
print(a.count)''',
          expect="""2 1
3""")}

    {voice("LOGIC", "Medium: Success",
           "self is not magic and it is not a keyword. It is just the first parameter, and "
           "Python passes the instance into it automatically when you use the dot. "
           "a.bump() and Counter.bump(a) are the same call written two ways.",
           "Which is why forgetting self in a method definition gives you 'takes 0 positional "
           "arguments but 1 was given'. Python passed the instance and your function had "
           "nowhere to put it.")}

    <h2>Instance attributes versus class attributes</h2>
    {code('''class Pirate:
    crew_name = "The Sea Monkeys"      # shared by every pirate
    count = 0

    def __init__(self, name):
        self.name = name               # unique to each pirate
        Pirate.count += 1


a = Pirate("Guybrush")
b = Pirate("Elaine")

print(a.crew_name, b.crew_name)
print(Pirate.count)

Pirate.crew_name = "The Mighty Pirates"
print(a.crew_name, b.crew_name)

a.crew_name = "Solo Act"               # this creates an INSTANCE attribute
print(a.crew_name, b.crew_name)''',
          expect="""The Sea Monkeys The Sea Monkeys
2
The Mighty Pirates The Mighty Pirates
Solo Act The Mighty Pirates""")}
    {callout("danger", "🪤 Mutable class attributes are the list-default trap again",
             "<p>A class attribute that is a list or dict is shared by <em>every</em> "
             "instance, exactly like a mutable default argument. Put mutable state in "
             "<code>__init__</code> as <code>self.something = []</code>, always.</p>")}
    {code('''class Bad:
    items = []            # one list, shared by all


class Good:
    def __init__(self):
        self.items = []   # a fresh list per instance


a, b = Bad(), Bad()
a.items.append("grog")
print("Bad: ", a.items, b.items)

c, d = Good(), Good()
c.items.append("grog")
print("Good:", c.items, d.items)''',
          expect="""Bad:  ['grog'] ['grog']
Good: ['grog'] []""")}

    <h2>Making objects print nicely</h2>
    {code('''class Pirate:
    def __init__(self, name, insults=0):
        self.name = name
        self.insults = insults

    def __repr__(self):
        """For programmers: should look like the code that rebuilds it."""
        return f"Pirate({self.name!r}, insults={self.insults})"

    def __str__(self):
        """For humans."""
        return f"{self.name} ({self.insults} insults)"


guy = Pirate("Guybrush", 8)

print(guy)              # uses __str__
print(repr(guy))        # uses __repr__
print([guy])            # containers always use __repr__
print(f"{guy} vs {guy!r}")''',
          expect="""Guybrush (8 insults)
Pirate('Guybrush', insults=8)
[Pirate('Guybrush', insults=8)]
Guybrush (8 insults) vs Pirate('Guybrush', insults=8)""")}
    <p>
      Without <code>__repr__</code> you get <code>&lt;__main__.Pirate object at
      0x104f2b3d0&gt;</code>, which tells you nothing while debugging. Writing
      <code>__repr__</code> is the single highest-value five seconds you can spend on a class.
      If you only write one, write that one: <code>print</code> falls back to it when
      <code>__str__</code> is missing.
    </p>

    <h2>Properties: computed attributes</h2>
    {code('''class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @property
    def area(self):
        """Computed on demand, but used like an attribute."""
        return self.width * self.height

    @property
    def description(self):
        return "square" if self.width == self.height else "oblong"


r = Rectangle(3, 4)
print(r.area, r.description)

r.width = 4
print(r.area, r.description)''',
          expect="""12 oblong
16 square""")}
    <p>
      <code>@property</code> turns a method into something you read like an attribute: no
      brackets. It lets you start with a plain attribute and later replace it with a
      calculation without changing a single line of the code that uses it. That is a genuinely
      useful escape hatch, and it is why Python does not need Java-style getters everywhere.
    </p>

    <h2>Validation with a setter</h2>
    {code('''class Account:
    def __init__(self, balance=0):
        self._balance = balance          # the underscore means "internal"

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise ValueError(f"balance cannot be negative, got {value}")
        self._balance = value


acc = Account(100)
acc.balance = 250
print(acc.balance)

try:
    acc.balance = -50
except ValueError as err:
    print("Refused:", err)''',
          expect="""250
Refused: balance cannot be negative, got -50""")}
    {callout("info", "🔒 Python has no private",
             "<p>A single leading underscore (<code>_balance</code>) is a convention meaning "
             "'this is internal, do not touch'. Nothing enforces it. Python's philosophy here "
             "is 'we are all consenting adults': you are trusted not to reach into someone "
             "else's internals, and if you do, the breakage is yours to own. Two underscores "
             "(<code>__balance</code>) triggers name mangling, which discourages accidents but "
             "still is not real privacy.</p>")}

    <h2>When a class is the wrong answer</h2>
    {code('''# Not a class. This is a function wearing a costume.
class Calculator:
    def add(self, a, b):
        return a + b


# Just write the function
def add(a, b):
    return a + b


print(add(2, 3))''',
          expect="5")}
    <p>Reach for a class when you have <strong>state plus behaviour that belongs to it</strong>. If:</p>
    <ul>
      <li>there is no state, write a function;</li>
      <li>the state never changes and there is no behaviour, use a
      <a href="33-dataclasses.html">dataclass or a named tuple</a>;</li>
      <li>you have exactly one instance and it exists forever, a module is a fine singleton;</li>
      <li>you are writing <code>class</code> because it feels more professional, stop.</li>
    </ul>

    {exercise(1, "A bank account",
              "<p>Write an <code>Account</code> class with a holder, a balance, "
              "<code>deposit</code>, <code>withdraw</code> (refusing overdrafts), a transaction "
              "count, and a good <code>__repr__</code>.</p>",
              code('''class Account:
    """A very simple bank account that refuses to go negative."""

    def __init__(self, holder, balance=0):
        self.holder = holder
        self.balance = balance
        self.transactions = 0

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("deposit must be positive")
        self.balance += amount
        self.transactions += 1
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError(f"cannot withdraw {amount}, balance is {self.balance}")
        self.balance -= amount
        self.transactions += 1
        return self.balance

    def __repr__(self):
        return f"Account({self.holder!r}, balance={self.balance})"


acc = Account("Guybrush", 100)
acc.deposit(50)
acc.withdraw(30)
print(acc)
print(f"{acc.transactions} transactions")

try:
    acc.withdraw(1000)
except ValueError as err:
    print("Refused:", err)''',
                   expect="""Account('Guybrush', balance=120)
2 transactions
Refused: cannot withdraw 1000, balance is 120"""))}

    {exercise(2, "Find the shared-state bug",
              "<p>Every deck somehow contains everyone's cards. Why?</p>"
              + code('''class Deck:
    cards = []

    def add(self, card):
        self.cards.append(card)''', run=False, verify="compile"),
              "<p><code>cards</code> is a class attribute, so there is exactly one list and "
              "every deck shares it. <code>self.cards.append</code> does not create a new list, "
              "it mutates the shared one.</p>"
              + code('''class Deck:
    def __init__(self):
        self.cards = []          # a fresh list for every deck

    def add(self, card):
        self.cards.append(card)
        return self

    def __repr__(self):
        return f"Deck({self.cards})"


a, b = Deck(), Deck()
a.add("ace")
print(a, b)''', expect="Deck(['ace']) Deck([])"))}

    {exercise(3, "Temperature with validation",
              "<p>Write a <code>Temperature</code> class storing Celsius, exposing "
              "<code>fahrenheit</code> as a readable and writable property, and refusing "
              "anything below absolute zero.</p>",
              code('''class Temperature:
    """A temperature, stored in Celsius, readable in either scale."""

    ABSOLUTE_ZERO_C = -273.15

    def __init__(self, celsius=0.0):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < self.ABSOLUTE_ZERO_C:
            raise ValueError(f"{value}C is below absolute zero")
        self._celsius = float(value)

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5 / 9

    def __repr__(self):
        return f"Temperature({self._celsius:.1f})"


t = Temperature(100)
print(t, t.fahrenheit)

t.fahrenheit = 32
print(t, t.celsius)

try:
    Temperature(-300)
except ValueError as err:
    print("Refused:", err)''',
                   expect="""Temperature(100.0) 212.0
Temperature(0.0) 0.0
Refused: -300C is below absolute zero""")
              + "<p>Setting <code>fahrenheit</code> quietly routes through the "
              "<code>celsius</code> setter, so the validation applies to both scales without "
              "being written twice. That is the payoff of properties.</p>")}
""",
)

# ---------------------------------------------------------------- 32
_add(
    level=4,
    num="32",
    slug="32-inheritance",
    id="py-32-inheritance",
    card="Inheritance, composition, dunder methods, and why you should usually prefer the second one.",
    title="Inheritance and Dunder Methods",
    emoji="🧬",
    desc="Subclassing, super(), method overriding, dunder methods, and why composition usually beats inheritance.",
    lede="""Classes can build on other classes. This is the most over-used feature in
    programming, so this lesson teaches it and then teaches you when not to.""",
    body=f"""
    <h2>Inheriting</h2>
    {code('''class Character:
    def __init__(self, name, hp=100):
        self.name = name
        self.hp = hp

    def speak(self):
        return f"{self.name} says nothing."

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r}, hp={self.hp})"


class Pirate(Character):
    def __init__(self, name, insults=0):
        super().__init__(name, hp=120)      # run the parent's setup
        self.insults = insults

    def speak(self):                        # override the parent's version
        return f"{self.name}: You fight like a dairy farmer!"


class Ghost(Character):
    def speak(self):
        parent_line = super().speak()       # extend rather than replace
        return parent_line + " (it is a ghost, so this is unsurprising)"


for character in [Character("Otis"), Pirate("Guybrush", 8), Ghost("LeChuck", hp=999)]:
    print(character)
    print("  " + character.speak())''',
          expect="""Character('Otis', hp=100)
  Otis says nothing.
Pirate('Guybrush', hp=120)
  Guybrush: You fight like a dairy farmer!
Ghost('LeChuck', hp=999)
  LeChuck says nothing. (it is a ghost, so this is unsurprising)""")}
    <p>Three things happened there:</p>
    <ul>
      <li><strong>Inheriting</strong> means a <code>Pirate</code> gets everything
      <code>Character</code> has for free.</li>
      <li><strong>Overriding</strong> means defining a method the parent already has; yours
      wins.</li>
      <li><strong><code>super()</code></strong> calls the parent's version, so you can extend
      rather than replace. Forgetting <code>super().__init__()</code> is the classic bug: the
      parent's attributes never get set.</li>
    </ul>

    <h2>isinstance, and the type of a thing</h2>
    {code('''class Character: pass
class Pirate(Character): pass


guy = Pirate()

print(isinstance(guy, Pirate))
print(isinstance(guy, Character))     # a pirate IS a character
print(type(guy) is Pirate)
print(type(guy) is Character)         # but its exact type is not Character
print(Pirate.__mro__)''',
          expect="""True
True
True
False
(<class '__main__.Pirate'>, <class '__main__.Character'>, <class 'object'>)""")}
    <p>
      <code>__mro__</code> is the method resolution order: the exact list of classes Python
      searches, in order, when you use a dot. Everything inherits from <code>object</code> in
      the end.
    </p>

    <h2>Dunder methods: hooking into the language</h2>
    <p>
      Those <code>__double_underscore__</code> names are how your objects plug into Python's
      own syntax. Define the right one and <code>+</code>, <code>len()</code>,
      <code>==</code>, <code>in</code> and <code>for</code> all start working on your type.
    </p>
    {code('''class Inventory:
    def __init__(self, items=None):
        self.items = list(items or [])

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def __contains__(self, item):
        return item in self.items

    def __add__(self, other):
        return Inventory(self.items + other.items)

    def __eq__(self, other):
        return isinstance(other, Inventory) and sorted(self.items) == sorted(other.items)

    def __repr__(self):
        return f"Inventory({self.items!r})"


bag = Inventory(["map", "grog"])
pockets = Inventory(["mints"])

print(len(bag))
print(bag[0])
print("grog" in bag)
print(bag + pockets)
print(Inventory(["a", "b"]) == Inventory(["b", "a"]))

for item in bag:            # works via __getitem__, no __iter__ needed
    print(" -", item)''',
          expect="""2
map
True
Inventory(['map', 'grog', 'mints'])
True
 - map
 - grog""")}
    {table(
        ["Write this", "And this works"],
        [["<code>__len__</code>", "<code>len(x)</code>, and truthiness"],
         ["<code>__getitem__</code>", "<code>x[0]</code>, slicing, and iteration"],
         ["<code>__iter__</code>", "<code>for i in x</code> (the proper way, Lesson 34)"],
         ["<code>__contains__</code>", "<code>y in x</code>"],
         ["<code>__eq__</code>", "<code>x == y</code>"],
         ["<code>__lt__</code>", "<code>x &lt; y</code>, and <code>sorted()</code>"],
         ["<code>__add__</code>", "<code>x + y</code>"],
         ["<code>__call__</code>", "<code>x()</code>, making the object callable"],
         ["<code>__enter__</code> / <code>__exit__</code>", "<code>with x:</code> (Lesson 36)"]],
    )}

    {callout("warn", "⚖️ If you write __eq__, think about __hash__",
             "<p>Defining <code>__eq__</code> sets <code>__hash__</code> to None, so your "
             "objects can no longer go in a set or be dictionary keys. That is deliberate: two "
             "objects that are equal must hash the same, and Python will not guess your rule. "
             "Either define <code>__hash__</code> too, or use a "
             "<a href='33-dataclasses.html'>frozen dataclass</a>, which does it for you.</p>")}

    <h2>Sorting your own objects</h2>
    {code('''from functools import total_ordering


@total_ordering
class Score:
    def __init__(self, name, points):
        self.name = name
        self.points = points

    def __eq__(self, other):
        return self.points == other.points

    def __lt__(self, other):
        return self.points < other.points

    def __repr__(self):
        return f"{self.name}({self.points})"


scores = [Score("Otis", 42), Score("Guybrush", 95), Score("Elaine", 88)]

print(sorted(scores))
print(max(scores))
print(Score("a", 10) >= Score("b", 10))''',
          expect="""[Otis(42), Elaine(88), Guybrush(95)]
Guybrush(95)
True""")}
    <p>
      <code>@total_ordering</code> fills in <code>&gt;</code>, <code>&lt;=</code> and
      <code>&gt;=</code> from the two you wrote. Often though, the simplest answer is no dunder
      methods at all: <code>sorted(scores, key=lambda s: s.points)</code>.
    </p>

    <h2>Composition usually beats inheritance</h2>
    {code('''# Inheritance: a Car IS an Engine? Obviously not.
class Engine:
    def start(self):
        return "vroom"


class BadCar(Engine):          # wrong relationship
    pass


# Composition: a Car HAS an Engine. Much better.
class Car:
    def __init__(self, engine):
        self.engine = engine

    def start(self):
        return f"Car starting: {self.engine.start()}"


print(BadCar().start())
print(Car(Engine()).start())''',
          expect="""vroom
Car starting: vroom""")}

    {voice("CONCEPTUALIZATION", "Formidable: Success",
           "The test is a sentence. 'A pirate is a character': true, inherit. 'A car is an "
           "engine': false, so the car should hold an engine instead.",
           "Inheritance couples you to the parent's entire interface forever, including the "
           "parts you did not want. Composition lets you keep only the piece you need and swap "
           "it later. Deep inheritance hierarchies are the classic sign of a codebase written "
           "by someone who had just learned about inheritance.")}

    <h2>Abstract base classes: promising an interface</h2>
    {code('''from abc import ABC, abstractmethod


class Storage(ABC):
    """Anything that can save and load a value."""

    @abstractmethod
    def save(self, key, value): ...

    @abstractmethod
    def load(self, key): ...

    def save_many(self, pairs):
        """A useful method every subclass gets for free."""
        for key, value in pairs.items():
            self.save(key, value)
        return len(pairs)


class MemoryStorage(Storage):
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def load(self, key):
        return self.data.get(key)


store = MemoryStorage()
print(store.save_many({"ship": "Sea Monkey", "crew": 12}))
print(store.load("ship"))

try:
    Storage()
except TypeError as err:
    print("TypeError:", err)''',
          expect="""2
Sea Monkey
TypeError: Can't instantiate abstract class Storage without an implementation for abstract methods 'load', 'save'""")}
    <p>
      An abstract base class says "any subclass must provide these". You cannot build the base
      itself, and forgetting a method fails loudly at construction rather than quietly at 3am.
      It is how you write a plugin interface: one <code>Storage</code> for memory, one for a
      file, one for a database, all interchangeable.
    </p>

    <h2>Duck typing: the Python way</h2>
    {code('''class Duck:
    def speak(self):
        return "quack"


class Robot:
    def speak(self):
        return "beep"


def make_it_talk(thing):
    """No inheritance, no interface, no type check. Just: can it speak?"""
    return thing.speak()


for thing in [Duck(), Robot()]:
    print(make_it_talk(thing))''',
          expect="""quack
beep""")}
    <p>
      "If it walks like a duck and quacks like a duck, it is a duck." Python mostly does not
      care what class something is, only whether it has the method you are about to call. This
      is why Python needs far less inheritance than Java or C++: you can substitute any object
      that behaves right, with no shared ancestor at all. Lesson 38's <code>Protocol</code>
      lets you type-check exactly this.
    </p>

    {exercise(1, "A shape hierarchy",
              "<p>Write an abstract <code>Shape</code> with an abstract <code>area</code> and a "
              "concrete <code>describe</code>. Implement <code>Circle</code> and "
              "<code>Rectangle</code>, then sort a list of them by area.</p>",
              code('''from abc import ABC, abstractmethod
import math


class Shape(ABC):
    @abstractmethod
    def area(self): ...

    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2


class Rectangle(Shape):
    def __init__(self, width, height):
        self.width, self.height = width, height

    def area(self):
        return self.width * self.height


shapes = [Circle(3), Rectangle(2, 5), Circle(1)]
for shape in sorted(shapes, key=lambda s: s.area()):
    print(shape.describe())''',
                   expect="""Circle with area 3.14
Rectangle with area 10.00
Circle with area 28.27"""))}

    {exercise(2, "Inheritance or composition?",
              "<p>For each, say which you would use and why.</p>"
              "<ol><li>A <code>SavingsAccount</code> and a <code>CurrentAccount</code>.</li>"
              "<li>A <code>Logger</code> that a <code>WebServer</code> uses.</li>"
              "<li><code>Dog</code>, <code>Cat</code> and <code>Animal</code>.</li>"
              "<li>A <code>Playlist</code> and the <code>Song</code>s in it.</li>"
              "<li>A <code>Button</code> that needs to be clickable and draggable and "
              "resizable.</li></ol>",
              "<ol><li><strong>Inheritance.</strong> Both genuinely are accounts and share "
              "behaviour.</li>"
              "<li><strong>Composition.</strong> A server is not a logger, it has one. It "
              "should also be swappable for a silent one in tests.</li>"
              "<li><strong>Inheritance,</strong> and it is the textbook example precisely "
              "because real domains are rarely this clean.</li>"
              "<li><strong>Composition.</strong> A playlist contains songs.</li>"
              "<li><strong>Composition,</strong> almost certainly. Three separate behaviours "
              "combined is what mixins and multiple inheritance were invented for, and it is "
              "also where inheritance hierarchies most reliably become unmaintainable. Prefer "
              "small collaborating objects.</li></ol>")}

    {exercise(3, "Make a class feel built in",
              "<p>Write a <code>Playlist</code> supporting <code>len()</code>, indexing, "
              "<code>in</code>, <code>+</code>, iteration and a readable repr.</p>",
              code('''class Playlist:
    """A named list of songs that behaves like a built-in sequence."""

    def __init__(self, name, songs=None):
        self.name = name
        self.songs = list(songs or [])

    def __len__(self):
        return len(self.songs)

    def __getitem__(self, index):
        return self.songs[index]

    def __contains__(self, song):
        return song in self.songs

    def __add__(self, other):
        return Playlist(f"{self.name} + {other.name}", self.songs + other.songs)

    def __repr__(self):
        return f"Playlist({self.name!r}, {len(self.songs)} songs)"


sea = Playlist("Sea Shanties", ["Wellerman", "Drunken Sailor"])
grog = Playlist("Grog Anthems", ["A Pirate I Was Meant To Be"])

print(sea, len(sea))
print(sea[0])
print("Wellerman" in sea)

both = sea + grog
print(both)
for song in both:
    print(" -", song)''',
                   expect="""Playlist('Sea Shanties', 2 songs) 2
Wellerman
True
Playlist('Sea Shanties + Grog Anthems', 3 songs)
 - Wellerman
 - Drunken Sailor
 - A Pirate I Was Meant To Be""")
              + "<p>Nobody using this class needs to know it is not a list. That is the whole "
              "point of the dunder protocol: your types get to be first-class citizens of the "
              "language.</p>")}
""",
)

# ---------------------------------------------------------------- 33
_add(
    level=4,
    num="33",
    slug="33-dataclasses",
    id="py-33-dataclasses",
    card="Classes that hold data, written in a quarter of the lines. Plus enums and structural match.",
    title="Dataclasses, Enums and match",
    emoji="🎁",
    desc="dataclasses, frozen instances, field defaults, Enum, and structural pattern matching on objects.",
    lede="""Most classes exist only to hold a few named values. Python has a decorator that
    writes the boring parts for you, and it is one of the best things added in a decade.""",
    body=f"""
    <h2>The boilerplate problem</h2>
    {code('''class PirateManual:
    def __init__(self, name, role, insults=0):
        self.name = name
        self.role = role
        self.insults = insults

    def __repr__(self):
        return f"PirateManual(name={self.name!r}, role={self.role!r}, insults={self.insults!r})"

    def __eq__(self, other):
        if not isinstance(other, PirateManual):
            return NotImplemented
        return (self.name, self.role, self.insults) == (other.name, other.role, other.insults)


print(PirateManual("Guybrush", "captain", 8))''',
          expect="PirateManual(name='Guybrush', role='captain', insults=8)")}
    <p>Fourteen lines, and every field is written three times. Now the same thing:</p>
    {code('''from dataclasses import dataclass


@dataclass
class Pirate:
    name: str
    role: str
    insults: int = 0


guy = Pirate("Guybrush", "captain", 8)
print(guy)
print(guy.name, guy.insults)
print(Pirate("Elaine", "governor") == Pirate("Elaine", "governor"))''',
          expect="""Pirate(name='Guybrush', role='captain', insults=8)
Guybrush 8
True""")}
    <p>
      <code>@dataclass</code> writes <code>__init__</code>, <code>__repr__</code> and
      <code>__eq__</code> from the annotations. The type hints are required (that is how it
      finds the fields) and, as ever, not enforced at runtime.
    </p>

    <h2>Defaults, and the list trap solved properly</h2>
    {code('''from dataclasses import dataclass, field


@dataclass
class Ship:
    name: str
    crew: list[str] = field(default_factory=list)      # a NEW list per instance
    cargo: dict[str, int] = field(default_factory=dict)
    seaworthy: bool = True


a = Ship("Sea Monkey")
b = Ship("Flying Dutchman")

a.crew.append("Otis")
print(a)
print(b)''',
          expect="""Ship(name='Sea Monkey', crew=['Otis'], cargo={}, seaworthy=True)
Ship(name='Flying Dutchman', crew=[], cargo={}, seaworthy=True)""")}
    {callout("tip", "🛡️ default_factory is the fix, and it is enforced",
             "<p>Writing <code>crew: list = []</code> in a dataclass raises "
             "<code>ValueError: mutable default</code> at class creation time. The language "
             "learned from Lesson 18's landmine and made this one impossible to step on.</p>")}

    <h2>Frozen: immutable and hashable</h2>
    {code('''from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


p = Point(3, 4)
print(p)

try:
    p.x = 10
except Exception as err:
    print(type(err).__name__, err)

# frozen dataclasses are hashable, so they work as keys and in sets
grid = {Point(0, 0): "start", Point(3, 4): "treasure"}
print(grid[Point(3, 4)])
print(len({Point(1, 1), Point(1, 1)}))''',
          expect="""Point(x=3, y=4)
FrozenInstanceError cannot assign to field 'x'
treasure
1""")}
    <p>
      <code>frozen=True</code> gives you value semantics: two points with the same coordinates
      are equal, hash the same, and cannot be modified by a function you passed them to. For
      coordinates, money, configuration and anything you put in a set, this is what you want.
    </p>

    <h2>The other useful options</h2>
    {code('''from dataclasses import dataclass, field, asdict, astuple


@dataclass(order=True, slots=True)
class Score:
    points: int
    name: str = field(compare=False)      # not used when sorting
    notes: str = field(default="", repr=False)


scores = [Score(42, "Otis"), Score(95, "Guybrush"), Score(88, "Elaine")]
print(sorted(scores))
print(max(scores).name)
print(asdict(scores[0]))
print(astuple(scores[0]))''',
          expect="""[Score(points=42, name='Otis'), Score(points=88, name='Elaine'), Score(points=95, name='Guybrush')]
Guybrush
{'points': 42, 'name': 'Otis', 'notes': ''}
(42, 'Otis', '')""")}
    {table(
        ["Option", "Does"],
        [["<code>order=True</code>", "Adds <code>&lt;</code>, <code>&gt;</code> etc, comparing fields in order"],
         ["<code>frozen=True</code>", "Immutable and hashable"],
         ["<code>slots=True</code>", "Faster and smaller; no arbitrary attributes (3.10+)"],
         ["<code>kw_only=True</code>", "Callers must name every argument"],
         ["<code>field(compare=False)</code>", "Exclude from == and sorting"],
         ["<code>field(repr=False)</code>", "Hide from the repr (good for secrets)"],
         ["<code>asdict(x)</code>", "Convert to a plain dict, ready for JSON"]],
    )}

    <h2>__post_init__ for validation</h2>
    {code('''from dataclasses import dataclass


@dataclass
class Booking:
    name: str
    seats: int
    price_each: float
    total: float = 0.0

    def __post_init__(self):
        if self.seats < 1:
            raise ValueError(f"seats must be at least 1, got {self.seats}")
        self.total = round(self.seats * self.price_each, 2)


print(Booking("Elaine", 3, 24.99))

try:
    Booking("Otis", 0, 10.0)
except ValueError as err:
    print("Refused:", err)''',
          expect="""Booking(name='Elaine', seats=3, price_each=24.99, total=74.97)
Refused: seats must be at least 1, got 0""")}

    <h2>Enums: named constants that cannot be mistyped</h2>
    {code('''from enum import Enum, auto


class Status(Enum):
    DRAFT = auto()
    PUBLISHED = auto()
    ARCHIVED = auto()


class Suit(Enum):
    HEARTS = "♥"
    SPADES = "♠"


print(Status.DRAFT)
print(Status.DRAFT.name, Status.DRAFT.value)
print(Status("2") if False else Status(2))
print(Suit.HEARTS.value)
print(list(Status))
print(Status.DRAFT == Status.DRAFT, Status.DRAFT == Status.PUBLISHED)''',
          expect="""Status.DRAFT
DRAFT 1
Status.PUBLISHED
♥
[<Status.DRAFT: 1>, <Status.PUBLISHED: 2>, <Status.ARCHIVED: 3>]
True False""")}

    {voice("PARANOIA", "Medium: Success",
           "The alternative is strings. status == 'published' compiles, runs, and silently "
           "does nothing when someone writes 'Published' or 'publshed'.",
           "Status.PUBLISHED cannot be misspelled: a typo is an AttributeError immediately, "
           "your editor autocompletes it, and you can list every valid value. Any time you "
           "find yourself writing a fixed set of magic strings, that is an enum asking to be "
           "born.")}

    {code('''from enum import StrEnum


class Level(StrEnum):          # Python 3.11+
    DEBUG = "debug"
    INFO = "info"
    ERROR = "error"


print(Level.INFO)
print(Level.INFO == "info")               # behaves as a string too
print(f"level={Level.ERROR}")
print(sorted(Level, key=lambda l: l.value))''',
          expect="""info
True
level=error
[<Level.DEBUG: 'debug'>, <Level.ERROR: 'error'>, <Level.INFO: 'info'>]""")}
    <p>
      Notice <code>print(Level.INFO)</code> gave <code>info</code>, not
      <code>Level.INFO</code>. That is the whole point of <code>StrEnum</code>: it <em>is</em> a
      string, so it drops straight into f-strings, JSON and database columns while still being
      a real enum in your code. A plain <code>Enum</code> would have printed
      <code>Level.INFO</code> and confused whatever you handed it to.
    </p>

    <h2>match, properly: structural pattern matching</h2>
    {code('''from dataclasses import dataclass


@dataclass
class Click:
    x: int
    y: int


@dataclass
class KeyPress:
    key: str


@dataclass
class Quit:
    pass


def handle(event):
    match event:
        case Quit():
            return "Goodbye."
        case Click(x=0, y=0):
            return "Clicked the very corner."
        case Click(x=x, y=y) if x == y:
            return f"Clicked the diagonal at {x}."
        case Click(x=x, y=y):
            return f"Clicked at ({x}, {y})."
        case KeyPress(key="q"):
            return "Quit key."
        case KeyPress(key=key):
            return f"Pressed {key!r}."
        case _:
            return "No idea what that was."


for event in [Quit(), Click(0, 0), Click(5, 5), Click(2, 9), KeyPress("q"), KeyPress("a"), 42]:
    print(handle(event))''',
          expect="""Goodbye.
Clicked the very corner.
Clicked the diagonal at 5.
Clicked at (2, 9).
Quit key.
Pressed 'a'.
No idea what that was.""")}
    <p>
      This is far more than a switch statement. It matches on <em>shape</em>: the type, the
      field values, and a guard condition, pulling out the parts you name as it goes. Compare
      the pile of <code>isinstance</code> checks and attribute lookups you would otherwise
      write.
    </p>

    <h2>Matching data shapes</h2>
    {code('''def describe(data):
    match data:
        case []:
            return "an empty list"
        case [single]:
            return f"one item: {single}"
        case [first, *rest]:
            return f"{first}, then {len(rest)} more"
        case {"type": "user", "name": str(name)}:
            return f"a user called {name}"
        case {"type": kind}:
            return f"some {kind}"
        case str() | bytes():
            return "text of some kind"
        case _:
            return "something else"


for item in [[], [1], [1, 2, 3], {"type": "user", "name": "Elaine"},
             {"type": "ship"}, "hello", 3.14]:
    print(describe(item))''',
          expect="""an empty list
one item: 1
1, then 2 more
a user called Elaine
some ship
text of some kind
something else""")}
    {callout("warn", "🪤 A bare name in a case always matches",
             "<p><code>case status:</code> does not compare against a variable called "
             "<code>status</code>; it <em>captures</em> whatever came in and always matches, "
             "swallowing every case below it. To compare against a constant, use a dotted name "
             "(<code>case Status.DRAFT:</code>) or a literal. This is the one genuinely "
             "surprising rule in <code>match</code>.</p>")}

    {exercise(1, "Convert a class to a dataclass",
              "<p>Rewrite this with <code>@dataclass</code>, keeping the behaviour and adding "
              "ordering by price.</p>"
              + code('''class Product:
    def __init__(self, name, price, tags=None):
        self.name = name
        self.price = price
        self.tags = tags if tags is not None else []

    def __repr__(self):
        return f"Product({self.name!r}, {self.price!r}, {self.tags!r})"''',
                     run=False, verify="compile"),
              code('''from dataclasses import dataclass, field


@dataclass(order=True)
class Product:
    price: float
    name: str = field(compare=False)
    tags: list[str] = field(default_factory=list, compare=False)


items = [
    Product(24.99, "Rubber chicken", ["novelty"]),
    Product(4.50, "Grog"),
    Product(12.00, "Map"),
]

for product in sorted(items):
    print(f"{product.price:6.2f}  {product.name}")''',
                   expect="""  4.50  Grog
 12.00  Map
 24.99  Rubber chicken""")
              + "<p>Putting <code>price</code> first is deliberate: <code>order=True</code> "
              "compares fields in declaration order, so the field you want to sort by goes "
              "first. Alternatively keep the natural order and use "
              "<code>sorted(items, key=lambda p: p.price)</code>.</p>")}

    {exercise(2, "Enum instead of magic strings",
              "<p>Rewrite this so invalid states are impossible.</p>"
              + code('''def advance(status):
    if status == "draft":
        return "review"
    elif status == "review":
        return "published"
    return status''', run=False, verify="compile"),
              code('''from enum import Enum


class Status(Enum):
    DRAFT = "draft"
    REVIEW = "review"
    PUBLISHED = "published"


NEXT = {Status.DRAFT: Status.REVIEW, Status.REVIEW: Status.PUBLISHED}


def advance(status: Status) -> Status:
    """Move to the next status, or stay put if already final."""
    return NEXT.get(status, status)


print(advance(Status.DRAFT))
print(advance(Status.REVIEW))
print(advance(Status.PUBLISHED))

try:
    Status("deleted")
except ValueError as err:
    print("Refused:", err)''',
                   expect="""Status.REVIEW
Status.PUBLISHED
Status.PUBLISHED
Refused: 'deleted' is not a valid Status""")
              + "<p>The transition table as a dictionary is a bonus: the rules are now data "
              "you can print, test and change, instead of control flow you have to read.</p>")}

    {exercise(3, "Match on a command",
              "<p>Write a text-adventure command parser using <code>match</code> on a split "
              "list of words. Handle go, take with and without a quantity, look, and unknown "
              "input.</p>",
              code('''def parse(line):
    match line.lower().split():
        case ["look"] | ["l"]:
            return "You see trees. Many trees."
        case ["go", direction]:
            return f"You walk {direction}."
        case ["take", item]:
            return f"Taken: {item}."
        case ["take", count, item] if count.isdigit():
            return f"Taken {count} x {item}."
        case ["say", *words]:
            return f"You say: {' '.join(words)}"
        case []:
            return "Say something."
        case [verb, *_]:
            return f"I do not know how to {verb}."


for line in ["look", "go north", "take grog", "take 3 mints",
             "say you fight like a cow", "", "dance wildly"]:
    print(parse(line))''',
                   expect="""You see trees. Many trees.
You walk north.
Taken: grog.
Taken 3 x mints.
You say: you fight like a cow
Say something.
I do not know how to dance.""")
              + "<p>Compare this to the same parser written with nested "
              "<code>if len(parts) == 2 and parts[0] == ...</code> checks. This is the case "
              "where <code>match</code> is not a nicety, it is a different quality of "
              "code.</p>")}
""",
)

# ---------------------------------------------------------------- 34
_add(
    level=4,
    num="34",
    slug="34-generators",
    id="py-34-generators",
    card="yield: produce values one at a time instead of building a list you cannot afford.",
    title="Iterators and Generators",
    emoji="🌊",
    desc="The iterator protocol, generator functions, yield, laziness, infinite sequences and itertools.",
    lede="""How does a for loop actually work? The answer unlocks the ability to process a
    hundred gigabyte file on a laptop with eight gigabytes of memory.""",
    body=f"""
    <h2>What a for loop really does</h2>
    {code('''crew = ["Guybrush", "Elaine"]

it = iter(crew)          # ask for an iterator
print(next(it))
print(next(it))

try:
    next(it)
except StopIteration:
    print("StopIteration: that is the loop's stop signal")''',
          expect="""Guybrush
Elaine
StopIteration: that is the loop's stop signal""")}
    <p>
      Every <code>for</code> loop is that: call <code>iter()</code>, call <code>next()</code>
      until <code>StopIteration</code>. Anything that supports those two calls can be looped
      over, which is why <code>for</code> works identically on lists, strings, dictionaries,
      files and things you write yourself.
    </p>

    <h2>Generators: iterators without the ceremony</h2>
    {code('''def countdown(n):
    """A generator: it yields values instead of returning one."""
    while n > 0:
        yield n
        n -= 1
    yield "Liftoff!"


for value in countdown(3):
    print(value)

print(type(countdown(3)))
print(list(countdown(2)))''',
          expect="""3
2
1
Liftoff!
<class 'generator'>
[2, 1, 'Liftoff!']""")}
    <p>
      One word, <code>yield</code>, changes everything. The function no longer runs to
      completion and returns a value. It runs until the first <code>yield</code>, hands that
      value out, and <strong>freezes</strong>, keeping all its local variables. The next
      <code>next()</code> resumes exactly where it stopped.
    </p>

    {code('''def noisy():
    print("  starting")
    yield 1
    print("  woke up again")
    yield 2
    print("  finishing")


gen = noisy()
print("nothing has run yet")
print(next(gen))
print(next(gen))''',
          expect="""nothing has run yet
  starting
1
  woke up again
2""")}

    {voice("CONCEPTUALIZATION", "Formidable: Success",
           "Calling a generator function runs none of its body. It hands you a paused "
           "computation: a program frozen mid-sentence, holding its own place.",
           "This is the same idea as async/await, and as coroutines in every language that "
           "has them. Once you see a function as something that can be suspended and resumed "
           "rather than something that runs start to finish, a whole category of programming "
           "opens up.")}

    <h2>Why it matters: memory</h2>
    {code('''import sys


def squares_list(n):
    return [i * i for i in range(n)]


def squares_gen(n):
    for i in range(n):
        yield i * i


as_list = squares_list(1_000_000)
as_gen = squares_gen(1_000_000)

print(f"list:      {sys.getsizeof(as_list):>10,} bytes")
print(f"generator: {sys.getsizeof(as_gen):>10,} bytes")
print(f"same total: {sum(as_list) == sum(squares_gen(1_000_000))}")''',
          expect="""list:       8,448,728 bytes
generator:        200 bytes
same total: True""")}
    <p>
      Eight megabytes versus two hundred bytes, for the same answer. The generator never holds
      more than one value at a time. For a million items on a modern laptop this is a
      curiosity; for a log file bigger than your RAM it is the entire difference between
      possible and impossible.
    </p>

    <h2>The real-world shape: processing a big file</h2>
    {code('''from pathlib import Path

Path("server.log").write_text("""INFO  started
ERROR disk full
INFO  retrying
ERROR still full
INFO  done
""", encoding="utf-8")


def read_lines(path):
    """Yield each line, stripped. Never holds the whole file."""
    with open(path, encoding="utf-8") as f:
        for line in f:
            yield line.rstrip("\\n")


def only_errors(lines):
    """Yield only the ERROR lines."""
    for line in lines:
        if line.startswith("ERROR"):
            yield line


def messages(lines):
    """Yield just the message part."""
    for line in lines:
        yield line.split(maxsplit=1)[1]


pipeline = messages(only_errors(read_lines("server.log")))

for message in pipeline:
    print(message)''',
          expect="""disk full
still full""")}
    <p>
      That is a pipeline. Nothing is read until the <code>for</code> loop pulls, and then each
      line flows through all three stages one at a time. The file could be a terabyte and the
      memory use would not change. This is exactly how Unix pipes work, and it is one of the
      most reusable structures in programming.
    </p>

    <h2>Infinite sequences, which lists cannot do</h2>
    {code('''def fibonacci():
    """Every Fibonacci number. All of them. Forever."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


from itertools import islice

print(list(islice(fibonacci(), 10)))

# find the first Fibonacci number over a thousand
for n in fibonacci():
    if n > 1000:
        print("first over 1000:", n)
        break''',
          expect="""[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
first over 1000: 1597""")}

    <h2>Generator expressions</h2>
    {code('''numbers = range(1, 11)

squares_list = [n * n for n in numbers]        # builds it all
squares_gen = (n * n for n in numbers)         # builds nothing yet

print(squares_list)
print(type(squares_gen).__name__)
print(sum(squares_gen))
print(sum(squares_gen))          # exhausted! generators are one-shot''',
          expect="""[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
generator
385
0""")}
    {callout("danger", "🪤 A generator can only be walked once",
             "<p>Once consumed, it is empty, and it will not tell you: the second "
             "<code>sum</code> quietly returns 0. If you need the values twice, either build a "
             "list or call the generator function again. This catches everyone, usually in the "
             "form of 'my second loop did nothing'.</p>")}

    <h2>yield from: delegating</h2>
    {code('''def chain(*iterables):
    for it in iterables:
        yield from it          # yield every value from that one


def flatten(nested):
    """Flatten any depth of nested lists."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


print(list(chain([1, 2], "ab", (3, 4))))
print(list(flatten([1, [2, [3, [4, 5]], 6], 7])))''',
          expect="""[1, 2, 'a', 'b', 3, 4]
[1, 2, 3, 4, 5, 6, 7]""")}

    <h2>Writing an iterator class</h2>
    {code('''class Countdown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        """Return a fresh iterator each time, so this can be looped twice."""
        n = self.start
        while n > 0:
            yield n
            n -= 1


c = Countdown(3)
print(list(c))
print(list(c))          # works again, unlike a bare generator''',
          expect="""[3, 2, 1]
[3, 2, 1]""")}
    <p>
      Making <code>__iter__</code> a generator function is the tidiest way to build a reusable
      iterable. Each <code>for</code> loop calls <code>__iter__</code> again and gets a fresh
      generator, so the one-shot problem disappears.
    </p>

    <h2>itertools: the ones worth knowing</h2>
    {code('''from itertools import count, cycle, islice, chain, groupby, pairwise, accumulate

print(list(islice(count(10, 5), 4)))
print(list(islice(cycle("ab"), 5)))
print(list(chain([1, 2], [3])))
print(list(accumulate([1, 2, 3, 4])))
print(list(pairwise([1, 2, 3, 4])))

crew = [("deck", "Otis"), ("deck", "Meathook"), ("bridge", "Elaine")]
for station, people in groupby(crew, key=lambda pair: pair[0]):
    print(station, [name for _, name in people])''',
          expect="""[10, 15, 20, 25]
['a', 'b', 'a', 'b', 'a']
[1, 2, 3]
[1, 3, 6, 10]
[(1, 2), (2, 3), (3, 4)]
deck ['Otis', 'Meathook']
bridge ['Elaine']""")}
    {callout("warn", "🔤 groupby needs sorted input",
             "<p>It groups <em>consecutive</em> equal keys, like the Unix <code>uniq</code> "
             "command, not like SQL's GROUP BY. Sort by the same key first or you will get "
             "several groups with the same name. This surprises people constantly.</p>")}

    {exercise(1, "A generator pipeline",
              "<p>Write three generators that read numbers, keep the even ones, and square "
              "them. Chain them and prove nothing is computed until you ask.</p>",
              code('''def numbers(n):
    print("  (numbers started)")
    for i in range(1, n + 1):
        yield i


def evens(source):
    for n in source:
        if n % 2 == 0:
            yield n


def squared(source):
    for n in source:
        yield n * n


pipeline = squared(evens(numbers(10)))
print("built the pipeline, nothing has run")
print(list(pipeline))''',
                   expect="""built the pipeline, nothing has run
  (numbers started)
[4, 16, 36, 64, 100]"""))}

    {exercise(2, "Read a file backwards",
              "<p>Write a generator that yields the lines of a file in reverse order. Then "
              "explain honestly what it costs.</p>",
              code('''from pathlib import Path

Path("log.txt").write_text("one\\ntwo\\nthree\\n", encoding="utf-8")


def reversed_lines(path):
    """Yield lines last-first. Reads the whole file: see the note."""
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    for line in reversed(lines):
        yield line.rstrip("\\n")


print(list(reversed_lines("log.txt")))''',
                   expect="['three', 'two', 'one']")
              + "<p>The honest cost: this loads the entire file into memory, which throws away "
              "the main benefit of a generator. Reading a file backwards genuinely requires "
              "either holding it all or seeking from the end in chunks, because you cannot "
              "know where the last line starts without reaching the end. Being able to say "
              "'this generator is not actually lazy, and here is why' matters more than the "
              "code.</p>")}

    {exercise(3, "A moving average",
              "<p>Write a generator that yields the running average of a stream of numbers, "
              "using constant memory.</p>",
              code('''def running_average(numbers):
    """Yield the mean of everything seen so far."""
    total = 0
    count = 0
    for n in numbers:
        total += n
        count += 1
        yield total / count


for average in running_average([10, 20, 30, 40]):
    print(f"{average:.2f}")''',
                   expect="""10.00
15.00
20.00
25.00""")
              + "<p>Two variables, regardless of stream length. This is what people mean by "
              "streaming computation, and it is how systems process data that will never fit "
              "in memory: keep only what you need to produce the next answer.</p>")}
""",
)

# ---------------------------------------------------------------- 35
_add(
    level=4,
    num="35",
    slug="35-decorators",
    id="py-35-decorators",
    card="Wrap a function in another function. The @ symbol you have been seeing everywhere.",
    title="Decorators",
    emoji="🎀",
    desc="Functions as objects, closures, writing decorators, functools.wraps, arguments, and the built-in ones.",
    lede="""You have used @property, @dataclass and @staticmethod without knowing what the @
    does. It is simpler than it looks, and it is one of Python's genuinely elegant ideas.""",
    body=f"""
    <h2>Functions are objects</h2>
    {code('''def greet(name):
    return f"Hello, {name}"


# a function can be assigned, passed and returned like any other value
say = greet
print(say("Guybrush"))
print(greet.__name__)


def apply_twice(func, value):
    return func(func(value))


print(apply_twice(str.upper, "ho"))


def make_multiplier(n):
    def multiply(x):
        return x * n          # remembers n: this is a closure
    return multiply


triple = make_multiplier(3)
print(triple(5))''',
          expect="""Hello, Guybrush
greet
HO
15""")}
    <p>
      Everything a decorator does rests on those two facts: a function can be passed to
      another function, and a function can remember variables from where it was defined.
    </p>

    <h2>A decorator, built by hand</h2>
    {code('''def shout(func):
    """Take a function, return a new one that shouts the result."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper() + "!"
    return wrapper


def greet(name):
    return f"hello, {name}"


greet = shout(greet)          # replace the name with the wrapped version
print(greet("guybrush"))''',
          expect="HELLO, GUYBRUSH!")}
    <p>Now the same thing with the syntax:</p>
    {code('''def shout(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper() + "!"
    return wrapper


@shout
def greet(name):
    return f"hello, {name}"


print(greet("elaine"))''',
          expect="HELLO, ELAINE!")}
    <p>
      <code>@shout</code> above a definition means exactly <code>greet = shout(greet)</code>.
      That is the whole feature. Everything else is what you choose to put in the wrapper.
    </p>

    <h2>The one thing you must remember: functools.wraps</h2>
    {code('''import functools


def bad(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def good(func):
    @functools.wraps(func)          # copy the name, docstring and signature over
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@bad
def alpha():
    """The alpha function."""


@good
def beta():
    """The beta function."""


print(alpha.__name__, "|", alpha.__doc__)
print(beta.__name__, "|", beta.__doc__)''',
          expect="""wrapper | None
beta | The beta function.""")}
    {callout("danger", "🏷️ Always use @functools.wraps",
             "<p>Without it, every decorated function in your program is called "
             "<code>wrapper</code> and has no docstring. Debugging, logging, "
             "<code>help()</code> and test frameworks all break in confusing ways. One line, "
             "and you never think about it again.</p>")}

    <h2>A useful one: timing</h2>
    {code('''import functools, time


def timed(func):
    """Print how long a function took."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} took under a second: {elapsed < 1}")
        return result
    return wrapper


@timed
def slow_sum(n):
    return sum(range(n))


print(slow_sum(1_000_000))''',
          expect="""  slow_sum took under a second: True
499999500000""")}

    <h2>Decorators that take arguments</h2>
    {code('''import functools


def repeat(times):
    """A decorator factory: returns the actual decorator."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator


@repeat(3)
def insult():
    return "You fight like a dairy farmer!"


for line in insult():
    print(line)''',
          expect="""You fight like a dairy farmer!
You fight like a dairy farmer!
You fight like a dairy farmer!""")}

    {voice("LOGIC", "Formidable: Success",
           "Three levels of function, which is where people's eyes glaze over. Read it "
           "outside-in: repeat(3) is called first and returns decorator. Then decorator is "
           "applied to insult and returns wrapper. Then wrapper is what you actually call.",
           "@repeat(3) means insult = repeat(3)(insult). Every decorator with brackets works "
           "this way, including @app.route('/') in Flask and @pytest.mark.parametrize.")}

    <h2>Retry: the decorator everyone eventually writes</h2>
    {code('''import functools


def retry(attempts=3):
    """Retry a function when it raises, up to a limit."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as err:
                    last_error = err
                    print(f"  attempt {attempt} failed: {err}")
            raise last_error
        return wrapper
    return decorator


calls = {"n": 0}


@retry(attempts=3)
def flaky():
    calls["n"] += 1
    if calls["n"] < 3:
        raise ConnectionError("network hiccup")
    return "succeeded on attempt 3"


print(flaky())''',
          expect="""  attempt 1 failed: network hiccup
  attempt 2 failed: network hiccup
succeeded on attempt 3""")}
    <p>
      In real use you would add a delay between attempts and only retry specific exceptions.
      The library <code>tenacity</code> does all of that, and now you know exactly what it is
      doing.
    </p>

    <h2>The built-in decorators worth knowing</h2>
    {code('''import functools


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2

    @staticmethod
    def describe():
        """No self: just a function that lives in the class's namespace."""
        return "A circle is round."

    @classmethod
    def unit(cls):
        """Gets the class, not an instance. The standard 'alternative constructor'."""
        return cls(1)


print(Circle(2).area)
print(Circle.describe())
print(Circle.unit().radius)


@functools.lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


print(fib(35))
print(fib.cache_info().hits > 0)''',
          expect="""12.56636
A circle is round.
1
9227465
True""")}
    <p>
      <code>@lru_cache</code> is the single best value-for-effort decorator in the standard
      library. That <code>fib(35)</code> would take many seconds without it and is instant
      with it, because every repeated call is answered from memory. It only works for
      functions whose result depends purely on their arguments, and whose arguments are
      hashable.
    </p>
    {table(
        ["Decorator", "Does"],
        [["<code>@property</code>", "Method usable as an attribute"],
         ["<code>@staticmethod</code>", "A function in a class, with no self"],
         ["<code>@classmethod</code>", "Receives the class; used for alternative constructors"],
         ["<code>@functools.wraps</code>", "Preserve the wrapped function's identity"],
         ["<code>@functools.lru_cache</code>", "Memoise results"],
         ["<code>@functools.cache</code>", "The same, simpler, 3.9+"],
         ["<code>@dataclass</code>", "Write the boilerplate (Lesson 33)"],
         ["<code>@abstractmethod</code>", "Subclasses must implement it (Lesson 32)"]],
    )}

    <h2>Stacking</h2>
    {code('''import functools


def bold(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        return f"<b>{func(*a, **kw)}</b>"
    return wrapper


def italic(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        return f"<i>{func(*a, **kw)}</i>"
    return wrapper


@bold
@italic
def text():
    return "hello"


print(text())''',
          expect="<b><i>hello</i></b>")}
    <p>
      Decorators apply bottom-up: <code>italic</code> wraps the function first, then
      <code>bold</code> wraps that. The result reads top-down in the output, which is a happy
      accident that makes stacking feel natural.
    </p>

    {exercise(1, "A logging decorator",
              "<p>Write <code>@logged</code> that prints the call with its arguments and then "
              "the result. It must work with any function.</p>",
              code('''import functools


def logged(func):
    """Print each call and its result."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        shown = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        print(f"-> {func.__name__}({', '.join(shown)})")
        result = func(*args, **kwargs)
        print(f"<- {result!r}")
        return result
    return wrapper


@logged
def add(a, b=0):
    return a + b


add(2, b=3)
add("ho", "ho")''',
                   expect="""-> add(2, b=3)
<- 5
-> add('ho', 'ho')
<- 'hoho'"""))}

    {exercise(2, "Validate arguments",
              "<p>Write <code>@positive</code> that raises <code>ValueError</code> if any "
              "numeric argument is negative, before the function runs.</p>",
              code('''import functools


def positive(func):
    """Reject any negative number passed to func."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for value in list(args) + list(kwargs.values()):
            if isinstance(value, (int, float)) and value < 0:
                raise ValueError(f"{func.__name__} got a negative value: {value}")
        return func(*args, **kwargs)
    return wrapper


@positive
def area(width, height):
    return width * height


print(area(3, 4))

try:
    area(3, -4)
except ValueError as err:
    print("Refused:", err)''',
                   expect="""12
Refused: area got a negative value: -4"""))}

    {exercise(3, "Count calls, and expose the count",
              "<p>Write <code>@counted</code> that tracks how many times a function was "
              "called and makes the number readable from outside.</p>",
              code('''import functools


def counted(func):
    """Count calls. The count is readable as func.calls."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper


@counted
def hello(name):
    return f"hi {name}"


hello("a")
hello("b")
hello("c")
print(f"{hello.__name__} was called {hello.calls} times")''',
                   expect="hello was called 3 times")
              + "<p>Attaching state to the wrapper function object is the standard trick, and "
              "it works because functions are objects and you can hang attributes on them. It "
              "is how <code>lru_cache</code> exposes <code>cache_info()</code>.</p>")}
""",
)

# ---------------------------------------------------------------- 36
_add(
    level=4,
    num="36",
    slug="36-context-managers",
    id="py-36-context-managers",
    card="The with statement, and how to write your own guaranteed cleanup.",
    title="Context Managers",
    emoji="🚪",
    desc="How with works, writing __enter__ and __exit__, contextlib.contextmanager, and suppressing exceptions.",
    lede="""You have used with on every file since Lesson 21. Here is what it actually does,
    and how to build your own guarantee that something always gets cleaned up.""",
    body=f"""
    <h2>The problem it solves</h2>
    {code('''# Setup, work, cleanup. The cleanup must happen even if the work explodes.
print("open the door")
try:
    print("do the work")
    raise ValueError("something went wrong")
except ValueError as err:
    print("caught:", err)
finally:
    print("close the door")''',
          expect="""open the door
do the work
caught: something went wrong
close the door""")}
    <p>
      That <code>try/finally</code> is correct and tedious, and you have to remember it every
      single time. A context manager packages the pattern so the caller cannot forget.
    </p>

    <h2>Writing one with a class</h2>
    {code('''class Door:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print(f"opening {self.name}")
        return self                # whatever `as` binds to

    def __exit__(self, exc_type, exc_value, traceback):
        print(f"closing {self.name}")
        return False               # False means "do not swallow the exception"

    def knock(self):
        return "nobody answers"


with Door("the vault") as door:
    print(door.knock())

print("---")

try:
    with Door("the trapdoor") as door:
        raise RuntimeError("floor gives way")
except RuntimeError as err:
    print("caught outside:", err)''',
          expect="""opening the vault
nobody answers
closing the vault
---
opening the trapdoor
closing the trapdoor
caught outside: floor gives way""")}
    <p>
      Note the second case: the exception fired inside the block, <code>__exit__</code> still
      ran, and only then did the error continue outward. That guarantee is the entire point.
    </p>
    {table(
        ["Piece", "Runs", "Gets"],
        [["<code>__enter__</code>", "on entering the block", "nothing; returns what <code>as</code> binds"],
         ["<code>__exit__</code>", "always, on the way out", "the exception type, value and traceback, or three Nones"],
         ["<code>return True</code> from <code>__exit__</code>", "", "swallows the exception. Use with great care"]],
    )}

    <h2>The easy way: @contextmanager</h2>
    {code('''from contextlib import contextmanager


@contextmanager
def door(name):
    print(f"opening {name}")
    try:
        yield name              # everything before this is __enter__
    finally:
        print(f"closing {name}")   # everything after is __exit__


with door("the hatch") as which:
    print(f"inside {which}")''',
          expect="""opening the hatch
inside the hatch
closing the hatch""")}
    <p>
      One generator, one <code>yield</code>. Setup above, cleanup below, wrapped in
      <code>try/finally</code> so the cleanup survives an exception. This is how most context
      managers are written in practice.
    </p>

    <h2>A genuinely useful one: timing a block</h2>
    {code('''import time
from contextlib import contextmanager


@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: finished in under a second: {elapsed < 1}")


with timer("summing a million"):
    total = sum(range(1_000_000))

print(f"{total:,}")''',
          expect="""summing a million: finished in under a second: True
499,999,500,000""")}

    <h2>Temporarily changing something, and putting it back</h2>
    {code('''import os
from contextlib import contextmanager


@contextmanager
def env(**changes):
    """Set environment variables for the duration of the block."""
    original = {k: os.environ.get(k) for k in changes}
    os.environ.update({k: str(v) for k, v in changes.items()})
    try:
        yield
    finally:
        for key, value in original.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


print("before:", os.environ.get("SHIP", "not set"))

with env(SHIP="Sea Monkey"):
    print("inside:", os.environ["SHIP"])

print("after: ", os.environ.get("SHIP", "not set"))''',
          expect="""before: not set
inside: Sea Monkey
after:  not set""")}

    {voice("VOLITION", "Medium: Success",
           "This is the pattern worth internalising: anything you change temporarily should be "
           "changed inside a context manager that puts it back.",
           "Working directory, environment variables, log levels, database transactions, "
           "locks, mocked functions in tests. Every one of them has been left in the wrong "
           "state by an early return or an exception in code that did it by hand.")}

    <h2>contextlib's ready-made tools</h2>
    {code('''from contextlib import suppress, redirect_stdout
import io
from pathlib import Path

# 1. suppress: a try/except/pass that is honest about being one
with suppress(FileNotFoundError):
    Path("nope.txt").unlink()
print("no explosion")

# 2. redirect_stdout: capture prints
buffer = io.StringIO()
with redirect_stdout(buffer):
    print("this goes into the buffer")
print("captured:", buffer.getvalue().strip())''',
          expect="""no explosion
captured: this goes into the buffer""")}
    {callout("warn", "🤫 suppress is still swallowing an error",
             "<p><code>with suppress(FileNotFoundError)</code> is fine and readable. "
             "<code>with suppress(Exception)</code> is a bare except with better marketing. "
             "Name the specific exception you are prepared to ignore, and be sure you really "
             "are prepared to ignore it.</p>")}

    <h2>Several at once</h2>
    {code('''from pathlib import Path

Path("in.txt").write_text("grog\\nmap\\nsword\\n", encoding="utf-8")

with (
    open("in.txt", encoding="utf-8") as source,
    open("out.txt", "w", encoding="utf-8") as target,
):
    for line in source:
        target.write(line.upper())

print(Path("out.txt").read_text(encoding="utf-8").strip())''',
          expect="""GROG
MAP
SWORD""")}
    <p>
      Both files are guaranteed closed, in reverse order, whatever happens. The bracketed
      multi-line form needs Python 3.10 or newer; before that you separated them with commas
      on one long line.
    </p>

    <h2>The catch: exceptions during cleanup</h2>
    {code('''from contextlib import contextmanager


@contextmanager
def careless():
    yield
    print("this cleanup NEVER runs when the block raises")


@contextmanager
def careful():
    try:
        yield
    finally:
        print("this cleanup always runs")


for manager in (careless, careful):
    try:
        with manager():
            raise ValueError("boom")
    except ValueError:
        print(f"  ({manager.__name__} finished)")''',
          expect="""  (careless finished)
this cleanup always runs
  (careful finished)""")}
    <p>
      If you write <code>@contextmanager</code> without <code>try/finally</code>, the code
      after <code>yield</code> is skipped whenever the block raises, which is precisely the
      case you were trying to protect. The <code>try/finally</code> is not optional
      decoration.
    </p>

    {exercise(1, "A working-directory manager",
              "<p>Write a context manager that changes the working directory and always "
              "changes back.</p>",
              code('''import os
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def working_directory(path):
    """Change directory for the duration of the block, then change back."""
    previous = Path.cwd()
    Path(path).mkdir(parents=True, exist_ok=True)
    os.chdir(path)
    try:
        yield Path(path)
    finally:
        os.chdir(previous)


start = Path.cwd().name

with working_directory("cargo/hold"):
    print("inside:", Path.cwd().name)
    Path("manifest.txt").write_text("47 barrels\\n", encoding="utf-8")

print("back where we started:", Path.cwd().name == start)
print(Path("cargo/hold/manifest.txt").read_text(encoding="utf-8").strip())''',
                   expect="""inside: hold
back where we started: True
47 barrels""")
              + "<p>Doing this by hand is a classic source of bugs: one early <code>return</code> "
              "and the rest of the program is running in the wrong folder, with symptoms that "
              "appear far away.</p>")}

    {exercise(2, "A transaction that rolls back",
              "<p>Write a context manager over a dictionary that commits changes on success "
              "and discards them if the block raises.</p>",
              code('''from contextlib import contextmanager
import copy


@contextmanager
def transaction(data):
    """Work on a copy; only commit it if the block finishes cleanly."""
    working = copy.deepcopy(data)
    yield working
    data.clear()
    data.update(working)


accounts = {"Guybrush": 100, "Elaine": 250}

with transaction(accounts) as draft:
    draft["Guybrush"] -= 50
    draft["Elaine"] += 50
print("committed:", accounts)

try:
    with transaction(accounts) as draft:
        draft["Guybrush"] -= 500
        raise ValueError("insufficient funds")
except ValueError as err:
    print("rolled back:", err)

print("unchanged: ", accounts)''',
                   expect="""committed: {'Guybrush': 50, 'Elaine': 300}
rolled back: insufficient funds
unchanged:  {'Guybrush': 50, 'Elaine': 300}""")
              + "<p>Note there is deliberately no <code>try/finally</code> here: the commit "
              "must be skipped when the block raises. This is the one case where the code "
              "after <code>yield</code> should <em>not</em> be protected, and knowing which "
              "one you want is the whole skill.</p>")}

    {exercise(3, "Explain the guarantee",
              "<p>A colleague says: 'I always close my files, so <code>with</code> is just "
              "syntax sugar.' Give the counter-example.</p>",
              code('''# Their version
def read_config(path):
    f = open(path, encoding="utf-8")
    data = f.read()
    value = int(data)          # if this raises ValueError...
    f.close()                  # ...this line never runs
    return value


# The point: the close is skipped on any exception, and on any early return.
try:
    read_config("/dev/null")
except ValueError:
    print("the file object is now leaked until garbage collection")

# The version that cannot leak
def read_config_safely(path):
    with open(path, encoding="utf-8") as f:
        data = f.read()
    return int(data)


try:
    read_config_safely("/dev/null")
except ValueError:
    print("file already closed, guaranteed, before this line ran")''',
                   expect="""the file object is now leaked until garbage collection
file already closed, guaranteed, before this line ran""")
              + "<p>CPython's reference counting usually closes the leaked file quickly, which "
              "is why this rarely bites in small scripts and does bite under load, on other "
              "Python implementations, or when the exception is caught far away. The "
              "guarantee, not the tidiness, is the reason.</p>")}
""",
)

# ---------------------------------------------------------------- 37
_add(
    level=4,
    num="37",
    slug="37-functional",
    id="py-37-functional",
    card="lambda, map, filter, functools and the functional style, used in moderation.",
    title="Functional Tools",
    emoji="🧮",
    desc="Lambdas, map and filter, functools.reduce and partial, and when a comprehension is better.",
    lede="""Python borrowed a handful of ideas from functional programming. Some are used
    constantly, some are quietly discouraged, and knowing which is which marks you out.""",
    body=f"""
    <h2>lambda: a function with no name</h2>
    {code('''square = lambda x: x * x        # legal, and not recommended
print(square(5))


def square_properly(x):
    return x * x


print(square_properly(5))

# where lambda genuinely earns its place: as a throwaway argument
crew = [("Guybrush", 8), ("Elaine", 3), ("Otis", 12)]

print(sorted(crew, key=lambda pair: pair[1]))
print(max(crew, key=lambda pair: pair[1]))''',
          expect="""25
25
[('Elaine', 3), ('Guybrush', 8), ('Otis', 12)]
('Otis', 12)""")}
    <p>
      A lambda is a single expression with an implicit return. No statements, no loops, no
      multiple lines. That limitation is deliberate: if you need more, you need a
      <code>def</code>.
    </p>
    {callout("warn", "🏷️ Never assign a lambda to a name",
             "<p><code>square = lambda x: x * x</code> gets you a function called "
             "<code>&lt;lambda&gt;</code> in every traceback, no docstring, and no annotations. "
             "PEP 8 says use <code>def</code>. Lambdas are for the moment you need a function "
             "for one line and then never again.</p>")}

    <h2>map and filter</h2>
    {code('''numbers = [1, 2, 3, 4, 5, 6]

print(list(map(lambda n: n * n, numbers)))
print(list(filter(lambda n: n % 2 == 0, numbers)))

# the comprehension versions, which most Python programmers prefer
print([n * n for n in numbers])
print([n for n in numbers if n % 2 == 0])

# map is genuinely nice with an existing named function
print(list(map(str.upper, ["grog", "map"])))
print(list(map(int, ["1", "2", "3"])))''',
          expect="""[1, 4, 9, 16, 25, 36]
[2, 4, 6]
[1, 4, 9, 16, 25, 36]
[2, 4, 6]
['GROG', 'MAP']
[1, 2, 3]""")}

    {voice("RHETORIC", "Medium: Success",
           "Guido van Rossum wanted to remove map and filter from Python 3 entirely, on the "
           "grounds that comprehensions do the same job more readably. They survived.",
           "The house rule that emerged: use a comprehension when there is a lambda involved, "
           "and use map when you already have a named function to apply. list(map(int, parts)) "
           "is lovely. list(map(lambda x: x.strip().lower(), parts)) is not.")}

    <h2>functools.reduce</h2>
    {code('''from functools import reduce

numbers = [1, 2, 3, 4, 5]

print(reduce(lambda a, b: a + b, numbers))
print(sum(numbers))                        # just use this

# reduce earns its place when there is no built-in for the operation
print(reduce(lambda a, b: a * b, numbers))

import math
print(math.prod(numbers))                  # since 3.8, so use this too

words = ["the", "rubber", "chicken"]
print(reduce(lambda a, b: a if len(a) > len(b) else b, words))''',
          expect="""15
15
120
120
chicken""")}
    <p>
      <code>reduce</code> folds a sequence down to one value. It is powerful, it is famously
      hard to read, and Python has built-ins for nearly every common case:
      <code>sum</code>, <code>math.prod</code>, <code>max</code>, <code>min</code>,
      <code>any</code>, <code>all</code>, <code>"".join</code>. Reach for it only when none of
      those fit.
    </p>

    <h2>functools.partial: freezing arguments</h2>
    {code('''from functools import partial


def power(base, exponent):
    return base ** exponent


square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5), cube(5))

# genuinely useful for callbacks and configuration
def log(level, message):
    return f"[{level}] {message}"


info = partial(log, "INFO")
error = partial(log, "ERROR")

print(info("all is well"))
print(error("the hull has failed"))''',
          expect="""25 125
[INFO] all is well
[ERROR] the hull has failed""")}

    <h2>operator: named versions of the symbols</h2>
    {code('''from operator import itemgetter, attrgetter, methodcaller
from dataclasses import dataclass

crew = [{"name": "Otis", "pay": 40}, {"name": "Elaine", "pay": 250}]

print(sorted(crew, key=itemgetter("pay"), reverse=True)[0]["name"])
print(list(map(itemgetter("name"), crew)))


@dataclass
class P:
    name: str
    pay: int


people = [P("Otis", 40), P("Elaine", 250)]
print(max(people, key=attrgetter("pay")).name)
print(list(map(methodcaller("upper"), ["grog", "map"])))''',
          expect="""Elaine
['Otis', 'Elaine']
Elaine
['GROG', 'MAP']""")}
    <p>
      <code>itemgetter("pay")</code> is a slightly faster and arguably clearer
      <code>lambda d: d["pay"]</code>. Use whichever your team reads more easily; both are
      idiomatic.
    </p>

    <h2>Pure functions, and why they are worth preferring</h2>
    {code('''# Impure: reaches outside itself and changes something
total = 0


def add_impure(n):
    global total
    total += n
    return total


# Pure: same input, same output, no side effects, ever
def add_pure(running_total, n):
    return running_total + n


print(add_impure(5), add_impure(5))      # different answers, same call
print(add_pure(0, 5), add_pure(0, 5))    # identical, always''',
          expect="""5 10
5 5""")}
    <p>Pure functions are:</p>
    <ul>
      <li><strong>testable</strong> without any setup;</li>
      <li><strong>cacheable</strong>, since the answer cannot change (this is exactly why
      <code>lru_cache</code> requires it);</li>
      <li><strong>safe to run in parallel</strong>, because there is nothing to race over;</li>
      <li><strong>readable</strong>, because everything affecting the result is visible in the
      signature.</li>
    </ul>
    <p>
      You cannot write a whole program this way: something has to touch a file eventually. The
      practical goal is a pure core with a thin impure shell around it, and that idea will
      improve your code more than any syntax in this level.
    </p>

    <h2>The one that catches everybody</h2>
    {code('''# A classic: building functions in a loop
makers = [lambda: i for i in range(3)]
print([f() for f in makers])          # all 2! not 0, 1, 2

# The fix: bind the value now, with a default argument
makers = [lambda i=i: i for i in range(3)]
print([f() for f in makers])''',
          expect="""[2, 2, 2]
[0, 1, 2]""")}
    <p>
      The lambdas captured the <em>variable</em> <code>i</code>, not its value. By the time
      they ran, the loop had finished and <code>i</code> was 2. This is called late binding,
      it exists in JavaScript too, and the default-argument trick is the standard workaround.
    </p>

    {exercise(1, "Sort records three ways",
              "<p>Given a list of dictionaries, sort by pay descending, then by name, then by "
              "the length of the name, using the tool you find clearest each time.</p>",
              code('''from operator import itemgetter

crew = [
    {"name": "Guybrush", "pay": 100},
    {"name": "Otis", "pay": 40},
    {"name": "Elaine", "pay": 250},
]

print([c["name"] for c in sorted(crew, key=itemgetter("pay"), reverse=True)])
print([c["name"] for c in sorted(crew, key=itemgetter("name"))])
print([c["name"] for c in sorted(crew, key=lambda c: len(c["name"]))])''',
                   expect="""['Elaine', 'Guybrush', 'Otis']
['Elaine', 'Guybrush', 'Otis']
['Otis', 'Elaine', 'Guybrush']"""))}

    {exercise(2, "Rewrite the functional pile",
              "<p>This works and nobody can read it. Rewrite it clearly.</p>"
              + code('''from functools import reduce
result = reduce(lambda a, b: a + b,
                map(lambda x: x * 2,
                    filter(lambda x: x % 2 == 0, range(1, 11))))''',
                     run=False, verify="compile"),
              code('''result = sum(n * 2 for n in range(1, 11) if n % 2 == 0)
print(result)

# or, if the steps deserve names
def is_even(n):
    return n % 2 == 0


evens = [n for n in range(1, 11) if is_even(n)]
doubled = [n * 2 for n in evens]
print(sum(doubled))''',
                   expect="""60
60""")
              + "<p>Same answer, and you can see what it means without reading inside-out. "
              "Nested map/filter/reduce is the classic sign of someone applying a style rather "
              "than solving a problem.</p>")}

    {exercise(3, "Build a small pipeline",
              "<p>Write <code>compose</code> that takes any number of functions and returns "
              "one function applying them left to right. Use it to clean up some text.</p>",
              code('''from functools import reduce


def compose(*functions):
    """Return a function applying each of these in order, left to right."""
    def piped(value):
        return reduce(lambda acc, f: f(acc), functions, value)
    return piped


def strip(text):
    return text.strip()


def lower(text):
    return text.lower()


def collapse_spaces(text):
    return " ".join(text.split())


clean = compose(strip, lower, collapse_spaces)

print(repr(clean("   The   SECRET of   Monkey Island   ")))''',
                   expect="'the secret of monkey island'")
              + "<p>This is one of the few places <code>reduce</code> genuinely reads well, "
              "because folding a list of functions over a value <em>is</em> the operation. "
              "Named pipeline stages also make each step separately testable.</p>")}
""",
)

# ---------------------------------------------------------------- 38
_add(
    level=4,
    num="38",
    slug="38-typing",
    id="py-38-typing",
    card="Type hints that actually pay off: generics, Protocols, Optional, and mypy in anger.",
    title="Type Hints for Real",
    emoji="🔬",
    desc="Generics, Protocol, Optional, Literal, TypedDict, and using mypy to catch bugs before they run.",
    lede="""Lesson 30 introduced the notation. This lesson is about the payoff: a checker that
    reads your whole program and finds the bug in the branch you never tested.""",
    body=f"""
    <h2>Recap, then onwards</h2>
    {code('''def total(prices: list[float], discount: float = 0.0) -> float:
    """Sum prices, applying a discount fraction."""
    return round(sum(prices) * (1 - discount), 2)


print(total([10.0, 24.99], discount=0.1))''',
          expect="31.49")}

    <h2>Optional, and the billion dollar mistake</h2>
    {code('''def find_pirate(name: str, crew: dict[str, int]) -> int | None:
    """Return the pirate's insult count, or None if they are not aboard."""
    return crew.get(name)


crew = {"Guybrush": 8}

found = find_pirate("Guybrush", crew)
missing = find_pirate("LeChuck", crew)

print(found, missing)

# mypy will refuse this, because found might be None:
#   error: Unsupported operand types for + ("None" and "int")
if found is not None:
    print(found + 1)''',
          expect="""8 None
9""")}
    <p>
      <code>int | None</code> is the modern spelling of <code>Optional[int]</code>. Its value
      is that mypy then <em>forces</em> you to handle the None case before using the value.
      Tony Hoare, who invented the null reference in 1965, later called it his "billion dollar
      mistake"; optional types are the fix, and Python has them if you opt in.
    </p>

    <h2>Generics: functions that work with any type, honestly</h2>
    {code('''def first[T](items: list[T]) -> T | None:
    """Return the first item, or None if empty. Python 3.12+ syntax."""
    return items[0] if items else None


print(first([1, 2, 3]))
print(first(["grog", "map"]))
print(first([]))''',
          expect="""1
grog
None""")}
    <p>
      The <code>[T]</code> says "this function works with some type T, and whatever goes in is
      what comes out". mypy then knows <code>first([1,2,3])</code> is an <code>int</code> and
      <code>first(["a"])</code> is a <code>str</code>. That is much more useful than
      <code>Any</code>, which switches checking off entirely.
    </p>
    {code('''from typing import TypeVar

T = TypeVar("T")


def first_old(items: list[T]) -> T | None:
    """The pre-3.12 spelling, which you will still see everywhere."""
    return items[0] if items else None


print(first_old(["still works"]))''',
          expect="still works")}

    <h2>Protocol: duck typing that a checker can verify</h2>
    {code('''from typing import Protocol


class Speaker(Protocol):
    """Anything with a speak() returning a string."""

    def speak(self) -> str: ...


class Duck:
    def speak(self) -> str:
        return "quack"


class Robot:
    def speak(self) -> str:
        return "beep"


def make_it_talk(thing: Speaker) -> str:
    return thing.speak()


print(make_it_talk(Duck()))
print(make_it_talk(Robot()))''',
          expect="""quack
beep""")}

    {voice("INTERFACING", "Formidable: Success",
           "This is the piece that makes typed Python feel like Python rather than Java. "
           "Neither Duck nor Robot inherits from Speaker. They have never heard of it.",
           "The check is structural: does this class have a speak() that returns a str? If "
           "yes, it qualifies. You can even write a Protocol for a third-party class you "
           "cannot modify, and suddenly their objects satisfy your interface.")}

    <h2>Literal and TypedDict: describing shapes precisely</h2>
    {code('''from typing import Literal, TypedDict


class Pirate(TypedDict):
    name: str
    insults: int
    role: Literal["captain", "lookout", "cook"]


def describe(pirate: Pirate) -> str:
    return f"{pirate['name']} the {pirate['role']} ({pirate['insults']} insults)"


guy: Pirate = {"name": "Guybrush", "insults": 8, "role": "captain"}
print(describe(guy))

# mypy rejects both of these, at check time, without running anything:
#   {"name": "Otis", "insults": 2, "role": "admiral"}   <- not in the Literal
#   {"name": "Otis", "insults": 2}                      <- missing "role"''',
          expect="Guybrush the captain (8 insults)")}
    <p>
      <code>TypedDict</code> is how you type the dictionaries that come back from JSON APIs
      without converting them to classes. <code>Literal</code> restricts a value to an exact
      set, which is the type-level version of the enum idea from Lesson 33.
    </p>

    <h2>What mypy actually catches</h2>
    {code('''def apply_discount(price: float, percent: int) -> float:
    return price * (1 - percent / 100)


def checkout(items: list[dict[str, float]]) -> float:
    total = 0.0
    for item in items:
        total += item["price"]
    return apply_discount(total, "10")      # <- a string, not an int''',
          run=False, verify="compile")}
    {term("""$ mypy shop.py
shop.py:10: error: Argument 2 to "apply_discount" has incompatible type
    "str"; expected "int"  [arg-type]
Found 1 error in 1 file (checked 1 source file)""")}
    <p>
      That bug is in a code path that might only run at checkout, with a real customer, at the
      weekend. mypy found it in under a second, without running the program, without a test.
      That is the actual argument for typing: it is a test suite you get for free, covering
      every line, including the ones you forgot.
    </p>

    <h2>Adopting it gradually</h2>
    {code('''from typing import Any


def legacy(data: Any) -> Any:
    """Any switches checking off. Useful as a staging post, not a destination."""
    return data


def modern(data: dict[str, int]) -> list[str]:
    return sorted(data)


print(modern({"b": 2, "a": 1}))''',
          expect="['a', 'b']")}
    <p>The workable order for adding types to an existing project:</p>
    <ol class="steps">
      <li><strong>Turn mypy on with default settings.</strong> Untyped code is simply ignored,
      so it will report almost nothing at first.</li>
      <li><strong>Type your function signatures</strong>, starting with the ones other modules
      call. Do not bother annotating every local variable; mypy infers those.</li>
      <li><strong>Fix what it finds.</strong> A surprising number will be real.</li>
      <li><strong>Ratchet strictness up</strong> one flag at a time, per module, in
      <code>pyproject.toml</code>. <code>disallow_untyped_defs</code> is the big one.</li>
    </ol>
    {code('''# pyproject.toml
[tool.mypy]
python_version = "3.13"
warn_return_any = true
warn_unused_ignores = true

# start strict only where you are ready
[[tool.mypy.overrides]]
module = "myapp.core.*"
disallow_untyped_defs = true''', run=False, verify="skip")}

    <h2>Where types are worth it, and where they are not</h2>
    {table(
        ["Situation", "Verdict"],
        [["A library other people import", "Yes, fully. The hints are your API documentation"],
         ["An application with more than one contributor", "Yes, on function boundaries"],
         ["Data pipelines with complex structures", "Yes. TypedDict pays for itself immediately"],
         ["A 30-line script", "No. The overhead exceeds the benefit"],
         ["A Jupyter notebook you will delete tomorrow", "No"],
         ["Code full of dynamic tricks and getattr", "Sometimes impossible. Be honest and use Any"]],
    )}

    {callout("warn", "🎭 Hints are still not enforced at runtime",
             "<p>Nothing in this lesson stops <code>total(\"nonsense\")</code> from running. If "
             "you need runtime validation, that is what "
             "<a href='https://docs.pydantic.dev' target='_blank' rel='noopener'>Pydantic</a> "
             "is for: it uses the same annotations to actually check data at the boundary, "
             "which is why it is the backbone of FastAPI. Types for your tools, Pydantic for "
             "your inputs.</p>")}

    {exercise(1, "Type a real function",
              "<p>Add complete hints, including the awkward return type.</p>"
              + code('''def group_by_role(crew):
    result = {}
    for member in crew:
        result.setdefault(member["role"], []).append(member["name"])
    return result''', run=False, verify="compile"),
              code('''from typing import TypedDict


class Member(TypedDict):
    name: str
    role: str


def group_by_role(crew: list[Member]) -> dict[str, list[str]]:
    """Map each role to the names of the people doing it."""
    result: dict[str, list[str]] = {}
    for member in crew:
        result.setdefault(member["role"], []).append(member["name"])
    return result


print(group_by_role([
    {"name": "Otis", "role": "lookout"},
    {"name": "Meathook", "role": "lookout"},
    {"name": "Elaine", "role": "captain"},
]))''',
                   expect="{'lookout': ['Otis', 'Meathook'], 'captain': ['Elaine']}")
              + "<p>The annotation on <code>result</code> is needed because mypy cannot infer "
              "the type of an empty dictionary. That is the one local variable you usually do "
              "have to annotate.</p>")}

    {exercise(2, "Write a Protocol",
              "<p>Define a <code>Saveable</code> protocol for anything with "
              "<code>save(path)</code> and <code>name</code>, then write a function that backs "
              "up a list of them. Show two unrelated classes satisfying it.</p>",
              code('''from typing import Protocol


class Saveable(Protocol):
    name: str

    def save(self, path: str) -> int: ...


class Document:
    def __init__(self, name: str, body: str) -> None:
        self.name = name
        self.body = body

    def save(self, path: str) -> int:
        return len(self.body)


class Image:
    def __init__(self, name: str, pixels: int) -> None:
        self.name = name
        self.pixels = pixels

    def save(self, path: str) -> int:
        return self.pixels * 3


def back_up(items: list[Saveable], folder: str) -> int:
    """Save everything, returning the total bytes written."""
    total = 0
    for item in items:
        written = item.save(f"{folder}/{item.name}")
        print(f"  {item.name}: {written} bytes")
        total += written
    return total


print("total:", back_up([Document("log.txt", "hello"), Image("map.png", 100)], "backup"))''',
                   expect="""  log.txt: 5 bytes
  map.png: 300 bytes
total: 305""")
              + "<p>Neither class inherits from anything, and no class knows the other exists. "
              "That is duck typing with a safety net.</p>")}

    {exercise(3, "Find the type error by eye",
              "<p>mypy reports one error here. Where, and why?</p>"
              + code('''def parse_scores(raw: str) -> dict[str, int]:
    scores = {}
    for line in raw.splitlines():
        name, value = line.split(":")
        scores[name.strip()] = value.strip()
    return scores''', run=False, verify="compile"),
              "<p>The annotation promises <code>dict[str, int]</code> but "
              "<code>value.strip()</code> is a <code>str</code>, so the dictionary holds "
              "strings. Everything downstream that does arithmetic on those values would fail "
              "at runtime, probably far from here.</p>"
              + code('''def parse_scores(raw: str) -> dict[str, int]:
    """Parse 'name: score' lines into a mapping of name to score."""
    scores: dict[str, int] = {}
    for line in raw.splitlines():
        name, value = line.split(":")
        scores[name.strip()] = int(value.strip())
    return scores


print(parse_scores("Guybrush: 95\\nOtis: 42"))''',
                     expect="{'Guybrush': 95, 'Otis': 42}")
              + "<p>This is the single most common category of bug that typing catches in real "
              "codebases: a value that is a string where everyone assumed a number, usually "
              "arriving from user input, a CSV file or a JSON payload.</p>")}
""",
)

# ---------------------------------------------------------------- 39
_add(
    level=4,
    num="39",
    slug="39-concurrency",
    id="py-39-concurrency",
    card="Threads, processes and the GIL, explained honestly rather than defensively.",
    title="Concurrency: Threads and Processes",
    emoji="🧵",
    desc="The Global Interpreter Lock, when threads help, when processes are needed, and how to choose.",
    lede="""Python's threading has a famous asterisk. Here is what it actually is, why it
    exists, and how to pick the right tool without folklore.""",
    body=f"""
    <h2>Two different problems</h2>
    {table(
        ["Kind of work", "What it is", "Called"],
        [["Downloading 100 web pages", "Mostly waiting for something else", "<strong>I/O bound</strong>"],
         ["Resizing 100 photos", "Mostly using the CPU", "<strong>CPU bound</strong>"]],
    )}
    <p>
      Nearly all confusion about Python concurrency comes from not asking this question first.
      The answer determines the tool, and using the wrong one makes your program slower, not
      faster.
    </p>

    <h2>The GIL, without the mythology</h2>
    <p>
      CPython has a <strong>Global Interpreter Lock</strong>: a single lock that means only one
      thread executes Python bytecode at a time. It exists because it makes the interpreter
      simpler and single-threaded code faster, and because CPython's memory management is not
      thread-safe without it.
    </p>
    <p>The consequences, stated precisely:</p>
    <ul>
      <li><strong>Threads do not speed up pure-Python CPU work.</strong> Four threads doing
      arithmetic take about as long as one, plus overhead.</li>
      <li><strong>Threads absolutely do speed up waiting.</strong> The lock is released while
      a thread waits on the network, a disk or a lock, so a hundred threads can wait at the
      same time.</li>
      <li><strong>Well-written C extensions release the lock too.</strong> NumPy's heavy
      numeric work is genuinely parallel across threads.</li>
      <li><strong>It is not part of the language.</strong> Jython and IronPython have no GIL,
      and Python 3.13 shipped an experimental free-threaded build that removes it. The rules
      above are about CPython today.</li>
    </ul>

    {voice("ENCYCLOPEDIA", "Formidable: Success",
           "PEP 703, accepted in 2023, lays out a path to making CPython work without the GIL, "
           "and 3.13 shipped it as an optional build. It is not the default: removing the lock "
           "costs single-threaded performance and requires every C extension in the ecosystem "
           "to be audited.",
           "So 'Python cannot do threads' is folklore, and 'the GIL is about to disappear' is "
           "premature. Both statements are the kind of thing people repeat without checking.")}

    <h2>Threads, where they shine</h2>
    {code('''import time
from concurrent.futures import ThreadPoolExecutor


def fetch(page):
    """Pretend to download something: mostly waiting."""
    time.sleep(0.1)
    return f"page {page}: 200 OK"


start = time.perf_counter()
sequential = [fetch(n) for n in range(8)]
sequential_time = time.perf_counter() - start

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=8) as pool:
    threaded = list(pool.map(fetch, range(8)))
threaded_time = time.perf_counter() - start

print(sequential[0])
print(f"sequential took about 0.8s: {0.7 < sequential_time < 1.2}")
print(f"threaded took about 0.1s:   {threaded_time < 0.4}")
print(f"same results: {sequential == threaded}")''',
          expect="""page 0: 200 OK
sequential took about 0.8s: True
threaded took about 0.1s:   True
same results: True""")}
    <p>
      Eight tasks that each wait a tenth of a second: eight tenths sequentially, one tenth in
      parallel. The GIL is irrelevant here because none of these threads wants the CPU. This
      is most real-world concurrency: talking to APIs, databases and files.
    </p>

    <h2>Processes, for actual CPU work</h2>
    {code('''from concurrent.futures import ProcessPoolExecutor


def count_primes(limit):
    """Deliberately CPU-heavy."""
    count = 0
    for n in range(2, limit):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            count += 1
    return count


if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(count_primes, [20000, 20000, 20000, 20000]))
    print(results)''',
          run=False, verify="compile")}
    <p>
      Each process is a separate Python interpreter with its own GIL, so they genuinely run on
      different cores. The costs are real: starting a process is slow (tens of milliseconds),
      and every argument and result must be pickled and copied between processes. Use them for
      chunky work, never for tiny tasks.
    </p>
    {callout("danger", "🪤 Processes need the __main__ guard",
             "<p>On Windows and macOS, child processes re-import your module to find the "
             "function they are running. Without <code>if __name__ == \"__main__\":</code>, "
             "every child re-runs your top-level code and spawns more children. It is a fork "
             "bomb written by accident, and everybody does it once.</p>")}

    <h2>Choosing</h2>
    {table(
        ["Your work", "Use", "Why"],
        [["Waiting on network or disk, tens of tasks", "<code>ThreadPoolExecutor</code>", "Simple, shares memory, waiting is free"],
         ["Waiting on network, thousands of tasks", "<code>asyncio</code> (Lesson 40)", "Threads cost about 8MB of stack each; coroutines cost bytes"],
         ["Heavy CPU work on many cores", "<code>ProcessPoolExecutor</code>", "Real parallelism, at the cost of copying"],
         ["Heavy numeric arrays", "NumPy, and often nothing else", "It already releases the GIL and uses vector instructions"],
         ["It is fast enough already", "Nothing", "Concurrency is a bug multiplier. Earn it first"]],
    )}

    <h2>The dangerous part: shared state</h2>
    {code('''import threading

counter = 0


def increment_unsafe():
    global counter
    for _ in range(100_000):
        counter += 1          # read, add, write: three steps, interruptible


threads = [threading.Thread(target=increment_unsafe) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"expected 400000, got {counter}")
print(f"correct? {counter == 400_000}")''',
          run=False, verify="compile")}
    <p>
      That program is a genuine race condition: <code>counter += 1</code> is three operations,
      and a thread can be interrupted between them, losing an update. On modern CPython you
      will often get the right answer anyway, which is worse than always getting it wrong,
      because the bug only appears under load, in production, at 3am.
    </p>
    {code('''import threading

counter = 0
lock = threading.Lock()


def increment_safe():
    global counter
    for _ in range(100_000):
        with lock:            # only one thread inside at a time
            counter += 1


threads = [threading.Thread(target=increment_safe) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(f"expected 400000, got {counter}")''',
          expect="expected 400000, got 400000")}

    <h2>The better answer: do not share</h2>
    {code('''from concurrent.futures import ThreadPoolExecutor


def work(n):
    """Pure function: takes a value, returns a value, shares nothing."""
    return n * n


with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(work, range(6)))

print(results)
print(sum(results))''',
          expect="""[0, 1, 4, 9, 16, 25]
55""")}
    <p>
      No lock, no race, no possibility of one. Threads that communicate by returning values
      rather than by mutating shared state are dramatically easier to get right. When you must
      share, use <code>queue.Queue</code>, which is thread-safe by design, rather than a list
      and a prayer.
    </p>

    <h2>Futures, when tasks finish at different times</h2>
    {code('''import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def fetch(page):
    time.sleep(0.05 * (4 - page))       # later pages finish first
    return f"page {page}"


with ThreadPoolExecutor(max_workers=4) as pool:
    futures = {pool.submit(fetch, n): n for n in range(4)}
    for future in as_completed(futures):
        print("finished:", future.result())''',
          expect="""finished: page 3
finished: page 2
finished: page 1
finished: page 0""")}
    <p>
      <code>submit</code> returns a <code>Future</code>: a promise of a result.
      <code>as_completed</code> yields them in the order they finish, so you can start
      processing the fast ones without waiting for the slow one. Exceptions are re-raised when
      you call <code>.result()</code>, which is a considerate design: nothing is swallowed.
    </p>

    {exercise(1, "I/O bound or CPU bound?",
              "<p>For each, name the tool.</p>"
              "<ol><li>Download 500 images from an API.</li>"
              "<li>Resize those 500 images.</li>"
              "<li>Read 10,000 small files and count the lines.</li>"
              "<li>Train a machine learning model.</li>"
              "<li>Poll three sensors every second for a day.</li></ol>",
              "<ol><li><strong>I/O bound.</strong> Threads, or asyncio at this volume.</li>"
              "<li><strong>CPU bound.</strong> Processes, or a library like Pillow that "
              "releases the GIL.</li>"
              "<li><strong>Mostly I/O bound,</strong> though at 10,000 files the per-file "
              "overhead starts to matter. Threads, and measure.</li>"
              "<li><strong>CPU bound,</strong> and you should not be writing the concurrency "
              "yourself: PyTorch already uses every core and your GPU.</li>"
              "<li><strong>I/O bound and mostly idle.</strong> Threads are plenty; asyncio is "
              "elegant. The real constraint is the sensors, not Python.</li></ol>")}

    {exercise(2, "Fix the race",
              "<p>This should collect results from four threads. It sometimes loses some. Fix "
              "it two ways.</p>"
              + code('''import threading

results = []


def work(n):
    results.append(n * n)


threads = [threading.Thread(target=work, args=(i,)) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()''', run=False, verify="compile"),
              "<p>Fix one, a lock:</p>"
              + code('''import threading

results = []
lock = threading.Lock()


def work(n):
    value = n * n
    with lock:
        results.append(value)


threads = [threading.Thread(target=work, args=(i,)) for i in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print(sorted(results))''', expect="[0, 1, 4, 9]")
              + "<p>Fix two, which is better: stop sharing.</p>"
              + code('''from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(lambda n: n * n, range(4)))

print(results)''', expect="[0, 1, 4, 9]")
              + "<p>The second version has no shared state, needs no lock, keeps the results "
              "in order, and is four lines. As a bonus, <code>list.append</code> is actually "
              "atomic in CPython today, so version one was probably safe by accident, which is "
              "exactly the kind of thing you should never rely on.</p>")}

    {exercise(3, "Measure before you optimise",
              "<p>Write a small benchmark comparing sequential and threaded execution of a "
              "waiting task, and report the speedup honestly.</p>",
              code('''import time
from concurrent.futures import ThreadPoolExecutor


def slow_task(n):
    time.sleep(0.05)
    return n


def timed(label, func):
    start = time.perf_counter()
    result = func()
    elapsed = time.perf_counter() - start
    print(f"{label:12} {elapsed:.2f}s")
    return elapsed, result


sequential, _ = timed("sequential", lambda: [slow_task(n) for n in range(10)])

def threaded_run():
    with ThreadPoolExecutor(max_workers=10) as pool:
        return list(pool.map(slow_task, range(10)))

threaded, _ = timed("threaded", threaded_run)

print(f"speedup: {sequential / threaded:.1f}x")
print(f"worth it: {sequential / threaded > 2}")''',
                   run=False, verify="compile")
              + "<p>This one has no run button because the exact timings depend on the machine, "
              "and a lesson should not promise numbers it cannot prove. Run it locally: you "
              "should see roughly 0.5s sequential and 0.05s threaded, close to a tenfold "
              "speedup. Then change <code>time.sleep</code> to a CPU-heavy loop and watch the "
              "speedup vanish. That experiment teaches the GIL better than any "
              "explanation.</p>")}
""",
)

# ---------------------------------------------------------------- 40
_add(
    level=4,
    num="40",
    slug="40-async",
    id="py-40-async",
    card="async and await: thousands of things waiting at once, on one thread.",
    title="async and await",
    emoji="⚡",
    desc="Coroutines, the event loop, asyncio.gather, TaskGroup, and when async is the wrong choice.",
    lede="""The last piece of modern Python. It looks like magic, it is really just the
    generator idea from Lesson 34 wearing a very good suit.""",
    body=f"""
    <h2>The idea</h2>
    <p>
      A thread waiting on the network is a thread doing nothing, holding several megabytes of
      stack. <strong>async</strong> replaces that with a coroutine: a function that can pause
      itself at a marked point, hand control back, and be resumed later. Thousands of them fit
      in the memory one thread would use, and they all take turns on a single thread.
    </p>

    <h2>Your first coroutine</h2>
    {code('''import asyncio


async def greet(name):
    """async def makes a coroutine function."""
    await asyncio.sleep(0.01)          # pause here, let others run
    return f"Hello, {name}"


async def main():
    result = await greet("Guybrush")
    print(result)


asyncio.run(main())''',
          expect="Hello, Guybrush")}
    {table(
        ["Word", "Means"],
        [["<code>async def</code>", "This function is a coroutine; calling it returns a coroutine object, it does not run"],
         ["<code>await</code>", "Pause here until that finishes, and let other tasks use the time"],
         ["<code>asyncio.run(...)</code>", "Start the event loop and run this until it is done"]],
    )}
    {code('''import asyncio


async def greet(name):
    return f"Hello, {name}"


coro = greet("Elaine")
print(type(coro))
print(asyncio.run(coro))''',
          expect="""<class 'coroutine'>
Hello, Elaine""")}

    <h2>The payoff: doing many things at once</h2>
    {code('''import asyncio, time


async def fetch(page):
    await asyncio.sleep(0.1)           # pretend network delay
    return f"page {page}"


async def one_at_a_time():
    return [await fetch(n) for n in range(5)]


async def all_at_once():
    return await asyncio.gather(*(fetch(n) for n in range(5)))


start = time.perf_counter()
asyncio.run(one_at_a_time())
sequential = time.perf_counter() - start

start = time.perf_counter()
results = asyncio.run(all_at_once())
concurrent = time.perf_counter() - start

print(results)
print(f"sequential about 0.5s: {0.4 < sequential < 0.9}")
print(f"concurrent about 0.1s: {concurrent < 0.3}")''',
          expect="""['page 0', 'page 1', 'page 2', 'page 3', 'page 4']
sequential about 0.5s: True
concurrent about 0.1s: True""")}

    {voice("PERCEPTION", "Formidable: Success",
           "Look carefully at the first version. It has await in it, and it is still "
           "sequential. Every await stops and waits for that one call.",
           "await means 'wait for this'. It does not mean 'do this in the background'. To get "
           "concurrency you must start several things before awaiting any of them, which is "
           "what gather does. Nearly every async performance complaint comes down to this "
           "misunderstanding.")}

    <h2>Tasks: starting work in the background</h2>
    {code('''import asyncio


async def work(name, seconds):
    await asyncio.sleep(seconds)
    print(f"  {name} done")
    return name


async def main():
    slow = asyncio.create_task(work("slow", 0.2))     # starts immediately
    fast = asyncio.create_task(work("fast", 0.05))

    print("both are now running")
    results = [await fast, await slow]
    return results


print(asyncio.run(main()))''',
          expect="""both are now running
  fast done
  slow done
['fast', 'slow']""")}

    <h2>TaskGroup: the modern, safer way</h2>
    {code('''import asyncio


async def fetch(page):
    await asyncio.sleep(0.01)
    if page == 3:
        raise ValueError("page 3 is missing")
    return f"page {page}"


async def main():
    failures = []
    try:
        async with asyncio.TaskGroup() as group:
            tasks = [group.create_task(fetch(n)) for n in range(5)]
    except* ValueError as errors:
        failures.extend(errors.exceptions)      # note: no `return` in here

    if failures:
        print(f"caught {len(failures)} failure(s):", failures[0])
        return "aborted"
    return [t.result() for t in tasks]


print(asyncio.run(main()))''',
          expect="""caught 1 failure(s): page 3 is missing
aborted""")}
    <p>
      <code>TaskGroup</code> (Python 3.11+) guarantees that every task finishes or is
      cancelled before the block exits, and it collects failures into an
      <code>ExceptionGroup</code> caught with <code>except*</code>. Before this existed it was
      easy to leave orphaned tasks running silently after an error. Prefer it to bare
      <code>gather</code> in new code.
    </p>
    <p>
      One rule that catches people: <code>return</code>, <code>break</code> and
      <code>continue</code> are <strong>not allowed inside an <code>except*</code> block</strong>,
      because an exception group can trigger several handlers and Python refuses to guess which
      return wins. Collect what you need into a variable, then act on it after the block, which
      is what the example above does.
    </p>

    <h2>Timeouts, which you will always need</h2>
    {code('''import asyncio


async def slow():
    await asyncio.sleep(10)
    return "eventually"


async def main():
    try:
        async with asyncio.timeout(0.05):
            return await slow()
    except TimeoutError:
        return "gave up waiting"


print(asyncio.run(main()))''',
          expect="gave up waiting")}

    <h2>The rules of the road</h2>
    <ul>
      <li><strong>async is contagious.</strong> To <code>await</code> something you must be in
      an <code>async def</code>, whose caller must await it too, all the way up to
      <code>asyncio.run</code>. People call this "function colouring", and it is the main
      complaint about async in every language that has it.</li>
      <li><strong>Never block inside a coroutine.</strong> One <code>time.sleep(5)</code> or
      one ordinary <code>requests.get</code> freezes the entire event loop, and every other
      task with it. Use the async equivalents.</li>
      <li><strong>Your libraries must cooperate.</strong> <code>requests</code> is blocking;
      you want {link("httpx", "https://www.python-httpx.org")} or
      {link("aiohttp", "https://docs.aiohttp.org")}. Databases need async drivers too.</li>
    </ul>
    {code('''import asyncio, time


async def blocking_mistake():
    time.sleep(0.1)          # WRONG: freezes everything
    return "blocked"


async def correct():
    await asyncio.sleep(0.1)  # right: yields control
    return "yielded"


async def escape_hatch():
    """When you must call blocking code, push it to a thread."""
    return await asyncio.to_thread(time.sleep, 0.01) or "ran in a thread"


async def main():
    return [await correct(), await escape_hatch()]


print(asyncio.run(main()))''',
          expect="['yielded', 'ran in a thread']")}

    <h2>Async iteration</h2>
    {code('''import asyncio


async def stream_pages(count):
    """An async generator: yields values as they become available."""
    for n in range(count):
        await asyncio.sleep(0.01)
        yield f"page {n}"


async def main():
    async for page in stream_pages(3):
        print("received", page)

    results = [p async for p in stream_pages(2)]
    return results


print(asyncio.run(main()))''',
          expect="""received page 0
received page 1
received page 2
['page 0', 'page 1']""")}
    <p>
      This is exactly how you will consume a streaming response from a language model in
      Level 6: tokens arrive one at a time, and <code>async for</code> processes each as it
      lands rather than waiting for the whole reply.
    </p>

    <h2>Threads or async?</h2>
    {table(
        ["Situation", "Choose", "Because"],
        [["Fewer than about 100 concurrent waits", "Threads", "Simpler, and works with every library"],
         ["Thousands of concurrent connections", "async", "Coroutines cost bytes; threads cost megabytes"],
         ["A web server or API client", "async", "The whole ecosystem is built for it now"],
         ["Existing blocking libraries you cannot replace", "Threads", "Async needs async-aware libraries"],
         ["CPU-heavy work", "Neither: processes", "Async gives you zero extra CPU (Lesson 39)"],
         ["It is already fast enough", "Neither", "Async makes code harder to read and debug. Earn it"]],
    )}

    {callout("info", "🐢 A last honest note",
             "<p>Async is not faster at doing work. It is better at waiting. If your program "
             "spends its time computing rather than waiting, async will make it slower and "
             "harder to read. Measure first, exactly as in Lesson 39, and let the numbers pick "
             "the tool.</p>")}

    {exercise(1, "Sequential to concurrent",
              "<p>This takes four times longer than it needs to. Fix it.</p>"
              + code('''import asyncio


async def check(site):
    await asyncio.sleep(0.1)
    return f"{site}: ok"


async def main():
    results = []
    for site in ["a.com", "b.com", "c.com", "d.com"]:
        results.append(await check(site))
    return results''', run=False, verify="compile"),
              code('''import asyncio


async def check(site):
    await asyncio.sleep(0.1)
    return f"{site}: ok"


async def main():
    sites = ["a.com", "b.com", "c.com", "d.com"]
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(check(s)) for s in sites]
    return [t.result() for t in tasks]


for line in asyncio.run(main()):
    print(line)''',
                   expect="""a.com: ok
b.com: ok
c.com: ok
d.com: ok""")
              + "<p>The loop awaited each check before starting the next. Creating all the "
              "tasks first lets every wait overlap, turning 0.4 seconds into 0.1.</p>")}

    {exercise(2, "Add a timeout and a fallback",
              "<p>Write a function that fetches a value but returns a default if it takes too "
              "long.</p>",
              code('''import asyncio


async def fetch_slowly(delay, value):
    await asyncio.sleep(delay)
    return value


async def with_fallback(coro, seconds, default):
    """Await coro, or return default if it takes longer than seconds."""
    try:
        async with asyncio.timeout(seconds):
            return await coro
    except TimeoutError:
        return default


async def main():
    quick = await with_fallback(fetch_slowly(0.01, "live data"), 0.1, "cached")
    slow = await with_fallback(fetch_slowly(1.0, "live data"), 0.05, "cached")
    return quick, slow


print(asyncio.run(main()))''',
                   expect="('live data', 'cached')")
              + "<p>Every network call in production code should have a timeout. Without one, "
              "a single unresponsive server can hold a request open until something else in "
              "the stack gives up, and that is how one slow dependency takes down a whole "
              "service.</p>")}

    {exercise(3, "Spot the blocking call",
              "<p>This async program is no faster than the sequential version. Why?</p>"
              + code('''import asyncio, time


async def process(item):
    time.sleep(0.1)          # <- here
    return item * 2


async def main():
    return await asyncio.gather(*(process(n) for n in range(10)))''',
                     run=False, verify="compile"),
              "<p><code>time.sleep</code> blocks the thread. The event loop cannot switch to "
              "another task while it is running, so all ten run one after another and "
              "<code>gather</code> buys nothing.</p>"
              + code('''import asyncio


async def process(item):
    await asyncio.sleep(0.1)          # yields control properly
    return item * 2


async def main():
    return await asyncio.gather(*(process(n) for n in range(10)))


print(asyncio.run(main()))''', expect="[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]")
              + "<p>The same trap covers <code>requests.get</code>, ordinary file reads, and "
              "any CPU-heavy loop. If you cannot avoid blocking code, wrap it in "
              "<code>asyncio.to_thread</code> so it runs off the event loop.</p>")}

    {callout("info", "🎉 That is Level 4",
             "<p>Classes, inheritance, dataclasses, generators, decorators, context managers, "
             "functional tools, real typing, threads and async. You can now read essentially "
             "any Python codebase you encounter. Take the "
             "<a href='../quiz.html'>Level 4 quiz</a>, then Level 5 goes outside and builds "
             "things with all of it.</p>")}
""",
)
