"""Level 1: First Words.

Ten lessons that contain the whole language in miniature. If you only
ever finish one level of this school, finish this one: everything after
it is elaboration.
"""

from __future__ import annotations

from .kit import callout, code, exercise, link, out, repl, table, tb, term, voice

LESSONS = []


def _add(**kw):
    LESSONS.append(kw)


# ---------------------------------------------------------------- 1
_add(
    level=1,
    num="1",
    slug="01-hello",
    id="py-01-hello",
    card="print(), your first program, comments, and why errors are completely normal.",
    title="Hello, World!",
    emoji="👋",
    desc="Your first Python program: print(), strings, comments, and what to do when it goes wrong.",
    lede="""Tradition demands that your first program says hello to the world. Tradition is
    right, and it will take you about four seconds.""",
    body=f"""
    <h2>The program</h2>
    <p>Press ▶ run.</p>
    {code('print("Hello, world!")', expect="Hello, world!")}
    <p>
      That is a complete, real Python program. Not a toy version, not a simplified teaching
      dialect. If you put that line in a file called <code>hello.py</code> and ran it on a
      server in a data centre, it would do exactly the same thing.
    </p>

    <h2>Taking it apart</h2>
    <p>Four things are happening in those twenty-one characters:</p>
    {table(
        ["Piece", "Name", "What it does"],
        [
            ["<code>print</code>", "A function", "A named action that already exists. Somebody wrote it so you do not have to"],
            ["<code>( )</code>", "Brackets, or 'parens'", "How you <em>call</em> a function: 'do it now, with this'"],
            ["<code>\"Hello, world!\"</code>", "A string", "Text. The quotes mark where it starts and stops"],
            ["The whole line", "A statement", "One complete instruction"],
        ],
    )}
    <p>
      <code>print</code> means "show this to the human". It does not mean paper. Nobody has
      printed anything on paper from a program on purpose since about 1994, but the name
      stuck, the way "dialling" a phone stuck.
    </p>

    {voice("INTERFACING", "Easy: Success",
           "The quotes are a fence, not decoration. Inside the fence, Python does not think, "
           "it just carries the characters through. Outside the fence, every word has to mean "
           "something. Confusing the inside for the outside is the single most common mistake "
           "of week one.")}

    <h2>Print more than one thing</h2>
    {code('''print("Guybrush Threepwood")
print("Mighty programmer")
print("Also: mighty pirate")''',
          expect="""Guybrush Threepwood
Mighty programmer
Also: mighty pirate""")}
    <p>
      Each <code>print</code> ends with a new line. Three prints, three lines. Python runs
      your file strictly top to bottom, like reading a recipe, and never skips ahead.
    </p>
    <p>You can also hand <code>print</code> several things at once, separated by commas:</p>
    {code('print("Grog level:", 7, "out of", 10)',
          expect="Grog level: 7 out of 10")}
    <p>
      Notice Python put spaces between them for free. Notice also that <code>7</code> has no
      quotes: it is a number, not text, and Lesson 3 is about why that distinction matters.
    </p>

    <h2>Single or double quotes?</h2>
    {code("""print("Both of these work.")
print('There is no difference.')
print("Use doubles when the text has an apostrophe: it's easier.")
print('Use singles when the text has "quotes" in it.')""",
          expect="""Both of these work.
There is no difference.
Use doubles when the text has an apostrophe: it's easier.
Use singles when the text has "quotes" in it.""")}
    <p>
      Python genuinely does not care. Pick doubles as your default (that is what the
      autoformatter in Lesson 30 will do anyway) and switch when it saves you an escape.
    </p>

    <h2>Comments: notes to humans</h2>
    <p>
      Anything after a <code>#</code> is ignored by Python entirely. It exists for the next
      person to read the file, who is usually you, six months from now, having forgotten
      everything.
    </p>
    {code('''# This line does nothing at all. It is for you.
print("Insult the swordsman")   # notes can also sit after code

# print("This line is switched off.")
print("This line is not.")''',
          expect="""Insult the swordsman
This line is not.""")}
    <p>
      That third trick, putting a <code>#</code> in front of a line to disable it, is called
      commenting out, and you will do it fifty times a day while hunting bugs. In your editor
      the shortcut is <code>Ctrl+/</code> (<code>Cmd+/</code> on a Mac).
    </p>

    {callout("tip", "✍️ What makes a good comment",
             "<p>Bad: <code># add one to x</code>. We can see that. Good: "
             "<code># the API counts from 1, not 0</code>. Comments should explain "
             "<strong>why</strong>, because the <em>what</em> is already sitting right there "
             "in the code.</p>")}

    <h2>Your first error, on purpose</h2>
    <p>
      Errors are not failures. They are Python telling you, in detail, what it could not
      understand. Here is a broken line:
    </p>
    {code('print("Look behind you, a three-headed monkey!)', run=False, verify="skip")}
    <p>Python says:</p>
    {tb('''  File "hello.py", line 1
    print("Look behind you, a three-headed monkey!)
          ^
SyntaxError: unterminated string literal (detected at line 1)''')}
    <p>Read it like a form:</p>
    <ul>
      <li><strong>Where:</strong> file <code>hello.py</code>, line 1.</li>
      <li><strong>What:</strong> <code>SyntaxError</code>, which means "this is not valid
      Python", found before anything ran.</li>
      <li><strong>Which bit:</strong> the little <code>^</code> points at the guilty
      character.</li>
      <li><strong>Why:</strong> "unterminated string literal": a fence was opened and never
      closed. The closing quote is missing.</li>
    </ul>
    <p>
      Modern Python error messages are genuinely excellent, and they got dramatically better
      in 3.10 and 3.11. Lesson 10 is devoted entirely to reading them. For now, absorb the
      one habit that matters: <strong>read the last line first</strong>. It names the problem.
    </p>

    {voice("VOLITION", "Medium: Success",
           "You are going to see hundreds of these. Thousands. Experienced programmers do not "
           "see fewer errors than you, they see more, because they write more code. What "
           "changes is the reaction time: from twenty minutes of despair, down to four seconds "
           "of 'ah, a missing quote'.")}

    <h2>Two ways to run Python</h2>
    {table(
        ["Way", "How", "Good for"],
        [
            ["A file", "Write <code>hello.py</code>, run <code>python3 hello.py</code>",
             "Real programs you want to keep and re-run"],
            ["The REPL", "Type <code>python3</code> with no filename",
             "Trying one thing quickly. It prints the answer to every line automatically"],
        ],
    )}
    {repl(""">>> print("Hello")
Hello
>>> 2 + 2
4
>>> "grog " * 3
'grog grog grog '""")}
    <p>
      Notice that in the REPL, <code>2 + 2</code> shows <code>4</code> without any
      <code>print</code>. That convenience exists <em>only</em> in the REPL. In a file, a line
      that just says <code>2 + 2</code> computes 4 and throws it away in silence. Beginners
      lose an afternoon to this at least once, so now you will not.
    </p>

    {exercise(1, "Introduce yourself",
              "<p>Write a program that prints three lines: your name, one thing you want to "
              "build, and how many years you have been meaning to learn this.</p>",
              code('''print("Chris")
print("I want to build a tool that renames my photo library.")
print("I have been meaning to do this for 3 years.")''',
                   expect="""Chris
I want to build a tool that renames my photo library.
I have been meaning to do this for 3 years."""))}

    {exercise(2, "Fix the broken program",
              "<p>Three separate mistakes. Find and fix all of them.</p>"
              + code('''Print("The first mistake is on this line.")
print(Second mistake here.)
print("Third mistake is at the end."''', run=False, verify="skip"),
              "<ol><li><code>Print</code> with a capital P. Python is case sensitive; the "
              "function is <code>print</code>. You would get "
              "<code>NameError: name 'Print' is not defined</code>.</li>"
              "<li>No quotes around the text, so Python tries to read <code>Second mistake "
              "here.</code> as code and gives up.</li>"
              "<li>The closing bracket is missing.</li></ol>"
              + code('''print("The first mistake is on this line.")
print("Second mistake here.")
print("Third mistake is at the end.")''',
                     expect="""The first mistake is on this line.
Second mistake here.
Third mistake is at the end."""))}

    {exercise(3, "Draw something",
              "<p>Print a small picture using text. A house, a ship, a crab, anything. Multiple "
              "<code>print</code> lines stack up, so you have a canvas.</p>",
              code(r'''print("      |>>>")
print("      |")
print("  __ _|__")
print("  \\      /")
print("~~~\\~~~~/~~~~~~~")''',
                   expect=r"""      |>>>
      |
  __ _|__
  \      /
~~~\~~~~/~~~~~~~""")
              + "<p>The doubled backslashes are not a typo. A backslash has a special "
              "meaning inside a string (Lesson 4 explains it), so to print one you write two. "
              "Or you can put an <code>r</code> in front of the quote, like "
              "<code>r\"\\_/\"</code>, which means 'raw: take this literally'.</p>")}
""",
)

# ---------------------------------------------------------------- 2
_add(
    level=1,
    num="2",
    slug="02-variables",
    id="py-02-variables",
    card="Labelled boxes for your data, naming rules, and why Python never asks for a type.",
    title="Variables: Naming Things",
    emoji="📦",
    desc="Assignment, variable names, PEP 8 conventions, and how Python's dynamic typing actually works.",
    lede="""A program that cannot remember anything can only do one thing. Variables are how
    a program remembers, and naming them well is a genuine craft.""",
    body=f"""
    <h2>A label stuck on a value</h2>
    {code('''name = "Guybrush"
grog = 7

print(name)
print(grog)''',
          expect="""Guybrush
7""")}
    <p>
      The <code>=</code> is not the equals of mathematics. Read it as "gets" or "is now":
      <em>name gets "Guybrush"</em>. It is an instruction, and it always runs right to left:
      work out the value on the right, then attach the label on the left.
    </p>

    {voice("LOGIC", "Easy: Success",
           "This is why x = x + 1 is not the nonsense it looks like. The right side is "
           "computed first using the old value, and only then is the label moved to the "
           "answer. In maths that line has no solutions. In programming it means 'add one'.")}

    <h2>Changing your mind</h2>
    {code('''score = 0
print("Start:", score)

score = 10
print("After one insult:", score)

score = score + 5
print("After the follow-up:", score)

score += 5          # the same thing, written the way everyone writes it
print("Final:", score)''',
          expect="""Start: 0
After one insult: 10
After the follow-up: 15
Final: 20""")}
    <p>
      A variable is a label, and labels can move. Nothing is carved in stone.
      <code>+=</code> is shorthand, and its family is worth memorising now:
    </p>
    {table(
        ["Shorthand", "Means", "Example"],
        [["<code>x += 3</code>", "<code>x = x + 3</code>", "add"],
         ["<code>x -= 3</code>", "<code>x = x - 3</code>", "subtract"],
         ["<code>x *= 2</code>", "<code>x = x * 2</code>", "double"],
         ["<code>x /= 2</code>", "<code>x = x / 2</code>", "halve"]],
    )}

    {callout("info", "🦀 A note for anyone who has seen Rust",
             "<p>In Rust, variables are locked by default and you must ask for permission to "
             "change one. Python is the opposite: everything is changeable, always, and it "
             "trusts you completely. That trust is why Python is fast to write and why big "
             "Python programs need discipline that the compiler will not enforce for you.</p>")}

    <h2>Python never asks you for a type</h2>
    {code('''thing = 42
print(thing, type(thing))

thing = "now I am text"
print(thing, type(thing))

thing = 3.5
print(thing, type(thing))''',
          expect="""42 <class 'int'>
now I am text <class 'str'>
3.5 <class 'float'>""")}
    <p>
      The <em>value</em> has a type; the <em>label</em> does not. This is called dynamic
      typing, and it is a huge part of why Python feels light. It is also how you get a
      program that runs fine for a month and then explodes because a variable you assumed was
      a number turned out to be text. Level 4 shows you type hints, which let you write down
      your assumptions so tools can check them.
    </p>

    <h2>The rules for names</h2>
    {table(
        ["Rule", "Good", "Bad"],
        [
            ["Letters, digits and underscores only", "<code>player_2</code>", "<code>player-2</code> (that is a minus sign)"],
            ["Cannot start with a digit", "<code>score_1</code>", "<code>1st_score</code>"],
            ["Case matters", "<code>name</code> and <code>Name</code> are different", "assuming they are the same"],
            ["No spaces", "<code>total_gold</code>", "<code>total gold</code>"],
            ["Not a Python keyword", "<code>class_name</code>", "<code>class</code>, <code>for</code>, <code>if</code>"],
        ],
    )}
    <p>And the conventions, which are not rules but might as well be:</p>
    <ul>
      <li><strong>lower_case_with_underscores</strong> for variables and functions. This is
      called snake_case and, yes, that is a happy coincidence.</li>
      <li><strong>ALL_CAPS</strong> for things that should never change:
      <code>MAX_PLAYERS = 8</code>.</li>
      <li><strong>CapWords</strong> for classes, which you meet in Lesson 31.</li>
    </ul>
    <p>
      These come from {link("PEP 8", "https://peps.python.org/pep-0008/")}, Python's official
      style guide. Following it means any Python programmer on earth can read your code
      without friction. It is worth the ten seconds.
    </p>

    <h2>Naming is the actual skill</h2>
    {code('''# Technically fine. Humanly useless.
a = 5
b = 3
c = a * b

# What the same code should look like
rows = 5
seats_per_row = 3
total_seats = rows * seats_per_row

print(f"The theatre holds {total_seats} people.")''',
          expect="The theatre holds 15 people.")}
    <p>
      Both versions run identically. Only one of them can be understood at 2am during an
      outage. There is an old joke that the two hard problems in computer science are cache
      invalidation, naming things, and off-by-one errors. The joke is only funny because the
      middle one is true.
    </p>

    {voice("RHETORIC", "Medium: Success",
           "A name is an argument you are making about what something is. 'data' claims "
           "nothing. 'unpaid_invoices' claims a great deal, and if the variable ever holds a "
           "paid invoice, the name itself becomes the bug report.")}

    <h2>Several at once</h2>
    {code('''x, y = 10, 20
print(x, y)

x, y = y, x          # swap, with no temporary variable
print(x, y)

a = b = c = 0        # all three point at the same 0
print(a, b, c)''',
          expect="""10 20
20 10
0 0 0""")}
    <p>
      That swap line is a small piece of Python showing off. In most languages it takes three
      lines and a temporary variable. You will use it more than you expect.
    </p>

    {callout("warn", "🪤 Using a name before it exists",
             "<p>Python reads top to bottom. Using a variable before you have assigned it "
             "gives you <code>NameError: name 'total' is not defined</code>. Ninety percent of "
             "the time that means a typo: <code>totl</code> in one place and <code>total</code> "
             "in another. Python will not guess what you meant, and that is a kindness.</p>")}

    {exercise(1, "Ship's manifest",
              "<p>Create variables for a ship's name, its crew size and its top speed in "
              "knots. Print a sentence using all three. Then the crew grows by 4: update the "
              "variable and print the sentence again.</p>",
              code('''ship_name = "Sea Monkey"
crew_size = 12
top_speed = 9.5

print(f"The {ship_name} sails with {crew_size} crew at {top_speed} knots.")

crew_size += 4
print(f"After recruitment: {crew_size} crew.")''',
                   expect="""The Sea Monkey sails with 12 crew at 9.5 knots.
After recruitment: 16 crew."""))}

    {exercise(2, "Predict the output",
              "<p>Do not run it. What does this print, and why?</p>"
              + code('''a = 5
b = a
a = 100
print(a, b)''', run=False, verify="compile"),
              "<p><code>100 5</code>.</p>"
              "<p><code>b = a</code> copied the <em>value</em> that <code>a</code> was "
              "pointing at, at that moment. It did not tie the two labels together. Changing "
              "<code>a</code> afterwards has no effect on <code>b</code>.</p>"
              "<p>Keep this picture. In Lesson 11 you will meet lists, where the same line "
              "behaves quite differently, and this is the memory that will save you.</p>")}

    {exercise(3, "Rename for clarity",
              "<p>Rewrite this so a stranger could understand it in one read.</p>"
              + code('''p = 24.99
q = 3
r = p * q
s = r * 0.2
t = r + s
print(t)''', run=False, verify="compile"),
              code('''price_each = 24.99
quantity = 3
subtotal = price_each * quantity
vat = subtotal * 0.2
total = subtotal + vat

print(f"Total including VAT: {total:.2f}")''', expect="Total including VAT: 89.96")
              + "<p>The <code>:.2f</code> means 'show this number with two decimal places', "
              "which you will meet properly in Lesson 4. Without it you would get "
              "<code>89.964</code>, and money with three decimal places makes accountants "
              "reach for their pens.</p>")}
""",
)

# ---------------------------------------------------------------- 3
_add(
    level=1,
    num="3",
    slug="03-numbers",
    id="py-03-numbers",
    card="Whole numbers, decimals, the two kinds of division, and the great 0.1 + 0.2 scandal.",
    title="Numbers and Maths",
    emoji="🔢",
    desc="Integers, floats, operators, integer division and modulo, and why 0.1 + 0.2 is not 0.3.",
    lede="""Python is a very good calculator that happens to also be a programming language.
    Ten minutes here saves you an entire category of confusing bug.""",
    body=f"""
    <h2>Two kinds of number</h2>
    {code('''crew = 12          # int: a whole number
speed = 9.5        # float: a number with a decimal point

print(type(crew))
print(type(speed))''',
          expect="""<class 'int'>
<class 'float'>""")}
    <p>
      <code>int</code> is short for integer, meaning whole. <code>float</code> is short for
      floating point, which refers to the decimal point being able to move around. That is the
      whole distinction, and it matters more than it looks.
    </p>

    {callout("tip", "♾️ Python integers do not overflow",
             "<p>In most languages an integer has a maximum size and quietly wraps around when "
             "you exceed it, which has caused real satellites to fail. Python integers grow to "
             "fit memory. <code>2 ** 1000</code> is a perfectly ordinary thing to ask for, and "
             "Python will hand you all 302 digits.</p>")}
    {code("print(2 ** 100)", expect="1267650600228229401496703205376")}

    <h2>The operators</h2>
    {table(
        ["You write", "It means", "Example", "Result"],
        [
            ["<code>+</code>", "add", "<code>7 + 3</code>", "<code>10</code>"],
            ["<code>-</code>", "subtract", "<code>7 - 3</code>", "<code>4</code>"],
            ["<code>*</code>", "multiply", "<code>7 * 3</code>", "<code>21</code>"],
            ["<code>/</code>", "divide (always a float)", "<code>7 / 2</code>", "<code>3.5</code>"],
            ["<code>//</code>", "divide and throw away the remainder", "<code>7 // 2</code>", "<code>3</code>"],
            ["<code>%</code>", "the remainder only", "<code>7 % 2</code>", "<code>1</code>"],
            ["<code>**</code>", "to the power of", "<code>7 ** 2</code>", "<code>49</code>"],
        ],
    )}
    {code('''print(7 / 2)
print(7 // 2)
print(7 % 2)
print(7 ** 2)
print(10 / 5)      # still a float, even though it divides exactly''',
          expect="""3.5
3
1
49
2.0""")}

    <h2>The two division signs are worth your attention</h2>
    <p>
      <code>//</code> and <code>%</code> look like curiosities. They are two of the most
      useful operators in programming.
    </p>
    {code('''total_minutes = 137

hours = total_minutes // 60      # how many whole hours fit
minutes = total_minutes % 60     # what is left over

print(f"{total_minutes} minutes is {hours}h {minutes}m")''',
          expect="137 minutes is 2h 17m")}
    <p>That pattern converts seconds to clocks, pennies to pounds, and items to pages.</p>
    <p><code>%</code> also answers "is this divisible by":</p>
    {code('''for number in [10, 15, 21, 30]:
    if number % 5 == 0:
        print(f"{number} divides by 5 exactly")
    else:
        print(f"{number} does not")''',
          expect="""10 divides by 5 exactly
15 divides by 5 exactly
21 does not
30 divides by 5 exactly""")}
    <p>
      "Remainder is zero" is how you test for even numbers (<code>n % 2 == 0</code>), how you
      make something happen every tenth time round a loop, and how you write FizzBuzz, the
      most famous interview question there is.
    </p>

    <h2>Order of operations</h2>
    {code('''print(2 + 3 * 4)        # multiplication happens first
print((2 + 3) * 4)      # brackets win
print(2 ** 3 ** 2)      # powers go right to left: 2 ** 9''',
          expect="""14
20
512""")}
    <p>
      The rules are the ones you learned at school. The advice is simpler than the rules:
      <strong>use brackets whenever there is the slightest doubt</strong>. They cost nothing
      and they are free documentation.
    </p>

    <h2>The 0.1 + 0.2 scandal</h2>
    {code("print(0.1 + 0.2)", expect="0.30000000000000004")}

    {voice("HALF LIGHT", "Legendary: Failure",
           "The machine is broken. The foundations are rotten. Nothing can be trusted.",
           "Sit down. Nothing is broken. This is arithmetic working exactly as specified, and "
           "every language on this planet does it: JavaScript, Java, C, Rust, your pocket "
           "calculator if you push it hard enough.")}

    <p>
      Computers store floats in binary. In binary, one tenth is a recurring number, exactly as
      one third is recurring in decimal (0.3333...). You have to stop writing digits somewhere,
      so the stored value is very slightly off, and the errors add up. The standard that
      defines this behaviour is {link("IEEE 754", "https://en.wikipedia.org/wiki/IEEE_754")},
      published in 1985 and implemented by essentially every CPU on earth.
    </p>
    <p>What to actually do about it:</p>
    {code('''# 1. Never compare floats with ==
print(0.1 + 0.2 == 0.3)

# 2. Compare with a tolerance instead
import math
print(math.isclose(0.1 + 0.2, 0.3))

# 3. Round for display
print(round(0.1 + 0.2, 2))

# 4. For money, use exact decimal arithmetic
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))''',
          expect="""False
True
0.3
0.3""")}
    <p>
      Rule of thumb: floats for measurements, <code>Decimal</code> for money, ints for
      counting. Financial software that uses floats for currency is a bug with a launch party.
    </p>

    <h2>Converting between types</h2>
    {code('''print(int("42") + 1)        # text to whole number
print(float("3.5") + 1)     # text to decimal
print(str(42) + " crabs")   # number to text
print(int(9.99))            # float to int: chops, does not round
print(round(9.99))          # this is what you usually wanted''',
          expect="""43
4.5
42 crabs
9
10""")}
    {callout("danger", "🪤 int() chops, it does not round",
             "<p><code>int(9.99)</code> is <code>9</code>. It removes everything after the "
             "point rather than rounding to the nearest. If you want nearest, say "
             "<code>round()</code>. This mistake has caused real money to go missing in real "
             "systems.</p>")}

    <h2>The maths module</h2>
    {code('''import math

print(math.sqrt(144))
print(math.pi)
print(math.floor(9.99), math.ceil(9.01))
print(math.factorial(5))''',
          expect="""12.0
3.141592653589793
9 10
120""")}
    <p>
      <code>import</code> loads a module: a file of code somebody else already wrote and
      tested. <code>math</code> ships with Python. Lesson 20 covers imports properly, but you
      can use them now with no ceremony.
    </p>

    {exercise(1, "Split the bill",
              "<p>A meal costs 87.50 and is shared by 4 people, with a 15% tip. Print the "
              "total including tip, and what each person pays, both to two decimal places.</p>",
              code('''bill = 87.50
people = 4
tip_rate = 0.15

tip = bill * tip_rate
total = bill + tip
each = total / people

print(f"Bill:  {bill:.2f}")
print(f"Tip:   {tip:.2f}")
print(f"Total: {total:.2f}")
print(f"Each:  {each:.2f}")''',
                   expect="""Bill:  87.50
Tip:   13.12
Total: 100.62
Each:  25.16""")
              + "<p>Look closely at the tip. The true answer is 13.125, and Python printed "
              "<strong>13.12</strong>, not 13.13. That is not a bug, it is two of this "
              "lesson's ideas colliding: <code>round</code> and <code>:.2f</code> use "
              "round-half-to-even (so exact halves go to the even digit, which spreads "
              "rounding error out instead of always pushing it up), and floats cannot hold "
              "most decimals exactly anyway. For a tip, nobody cares. For a payroll system, "
              "this is why you use <code>Decimal</code>.</p>")}

    {exercise(2, "Seconds to a clock",
              "<p>Turn 9,384 seconds into hours, minutes and seconds. Use <code>//</code> and "
              "<code>%</code> and nothing else clever.</p>",
              code('''total = 9384

hours = total // 3600
remainder = total % 3600
minutes = remainder // 60
seconds = remainder % 60

print(f"{hours}h {minutes}m {seconds}s")
print(f"{hours:02d}:{minutes:02d}:{seconds:02d}")''',
                   expect="""2h 36m 24s
02:36:24""")
              + "<p>The <code>:02d</code> means 'a whole number, at least two digits, padded "
              "with a zero'. That is how you make a clock look like a clock.</p>")}

    {exercise(3, "Predict, then run",
              "<p>Work out each answer on paper first.</p>"
              + code('''print(17 // 5)
print(-17 // 5)
print(17 % 5)
print(-17 % 5)''', run=False, verify="compile"),
              "<p><code>3</code>, then <code>-4</code>, then <code>2</code>, then "
              "<code>3</code>.</p>"
              "<p>The negative ones surprise nearly everybody. Python's <code>//</code> rounds "
              "<em>down</em> (towards negative infinity), not towards zero, so -17 // 5 is -4 "
              "rather than -3. And <code>%</code> always takes the sign of the right-hand "
              "side, so -17 % 5 is a positive 3.</p>"
              "<p>This is genuinely different from C, Java and Rust, which round towards zero. "
              "Python's choice is more mathematically consistent and occasionally more "
              "surprising. Now you know, which puts you ahead of a lot of working "
              "programmers.</p>")}
""",
)

# ---------------------------------------------------------------- 4
_add(
    level=1,
    num="4",
    slug="04-strings",
    id="py-04-strings",
    card="f-strings, slicing, and the twenty string methods that do 90% of real text work.",
    title="Text: Strings in Depth",
    emoji="✂️",
    desc="f-strings, indexing, slicing, string methods, escapes and immutability, with examples you can run.",
    lede="""Most programs are mostly text: names, messages, files, web pages, prompts to
    language models. Python's text handling is one of the best there is.""",
    body=f"""
    <h2>f-strings: the only way you need</h2>
    <p>
      Putting values inside text used to be awkward. Since Python 3.6 there is one obviously
      correct way, and it is lovely. Put an <code>f</code> before the quote and then put
      expressions inside curly braces.
    </p>
    {code('''name = "Guybrush"
insults = 7

print(f"{name} knows {insults} insults.")
print(f"After tonight, {insults + 3}.")
print(f"His name in capitals is {name.upper()}.")''',
          expect="""Guybrush knows 7 insults.
After tonight, 10.
His name in capitals is GUYBRUSH.""")}
    <p>Anything that produces a value can go in the braces: maths, function calls, anything.</p>

    <h3>Formatting inside the braces</h3>
    {code('''price = 1234.5678
ratio = 0.8734
name = "grog"

print(f"{price:.2f}")        # two decimal places
print(f"{price:,.2f}")       # thousands separators too
print(f"{ratio:.1%}")        # as a percentage
print(f"{name:>12}|")        # right aligned in 12 characters
print(f"{name:<12}|")        # left aligned
print(f"{name:^12}|")        # centred
print(f"{42:04d}")           # padded with zeros''',
          expect="""1234.57
1,234.57
87.3%
        grog|
grog        |
    grog    |
0042""")}
    <p>
      Those alignment tools are how you print a table that lines up without fighting it. There
      is a whole {link("format specification mini-language", "https://docs.python.org/3/library/string.html#format-specification-mini-language")}
      behind them; the seven above cover nearly everything you will ever need.
    </p>

    {callout("tip", "🐛 The debugging f-string",
             "<p>Put <code>=</code> after a variable inside the braces and Python prints the "
             "name as well as the value. It is the fastest debugging tool in the language and "
             "far too few people know about it.</p>")}
    {code('''total = 47
items = 3
print(f"{total=} {items=} {total / items=:.2f}")''',
          expect="total=47 items=3 total / items=15.67")}

    <h2>Strings are sequences</h2>
    <p>
      A string is a row of characters, each with a numbered position. Python counts from
      <strong>zero</strong>, which feels wrong for about a week and then feels obvious forever.
    </p>
    {code('''word = "MONKEY"
#        012345
#       -654321   (negative numbers count from the right)

print(word[0])
print(word[3])
print(word[-1])
print(len(word))''',
          expect="""M
K
Y
6""")}

    <h3>Slicing: taking a piece</h3>
    {code('''title = "The Secret of Monkey Island"

print(title[0:3])       # from 0, up to but NOT including 3
print(title[4:10])      # characters 4 through 9
print(title[:3])        # from the start
print(title[14:])       # to the end
print(title[-6:])       # the last six
print(title[::2])       # every second character
print(title[::-1])      # backwards''',
          expect="""The
Secret
The
Monkey Island
Island
TeSce fMne sad
dnalsI yeknoM fo terceS ehT""")}
    <p>
      The rule that trips everyone: the start is included, the end is not.
      <code>[0:3]</code> gives you three characters. It looks arbitrary until you notice
      <code>[0:3]</code> and <code>[3:6]</code> fit together perfectly with no gap and no
      overlap, which is why it was chosen.
    </p>

    {voice("VISUAL CALCULUS", "Medium: Success",
           "Do not picture the numbers on the characters. Picture them in the gaps between "
           "the characters, like fence posts: |T|h|e| with 0 before the T and 3 after the e. "
           "Slicing cuts at the posts. Suddenly it is obvious.")}

    <h2>Strings cannot be changed</h2>
    {code('''word = "grog"
# word[0] = "f"     # this raises TypeError

better = "f" + word[1:]
print(word)
print(better)''',
          expect="""grog
frog""")}
    <p>
      Strings are <strong>immutable</strong>: every operation makes a new string rather than
      editing the old one. This sounds like a limitation and is actually a gift. It means a
      string handed to a function cannot be secretly altered under your feet, which removes a
      whole species of bug.
    </p>

    <h2>The methods that do the real work</h2>
    {code('''messy = "   The Governor, ELAINE Marley   "

print(messy.strip())
print(messy.strip().lower())
print(messy.strip().upper())
print(messy.strip().title())
print(messy.strip().replace("Marley", "Threepwood"))
print(len(messy), len(messy.strip()))''',
          expect="""The Governor, ELAINE Marley
the governor, elaine marley
THE GOVERNOR, ELAINE MARLEY
The Governor, Elaine Marley
The Governor, ELAINE Threepwood
33 27""")}
    {table(
        ["Method", "Does", "Example result"],
        [
            ["<code>.strip()</code>", "Remove whitespace at both ends", "<code>'hi'</code>"],
            ["<code>.lower()</code> / <code>.upper()</code>", "Change case", "<code>'hi'</code> / <code>'HI'</code>"],
            ["<code>.title()</code>", "Capitalise Each Word", "<code>'Hi There'</code>"],
            ["<code>.replace(a, b)</code>", "Swap every a for b", "<code>'ho ho'</code>"],
            ["<code>.split(sep)</code>", "Break into a list", "<code>['a', 'b']</code>"],
            ["<code>.join(items)</code>", "Glue a list together", "<code>'a-b'</code>"],
            ["<code>.startswith(x)</code>", "True or False", "<code>True</code>"],
            ["<code>.find(x)</code>", "Position, or -1 if absent", "<code>4</code>"],
            ["<code>.count(x)</code>", "How many times", "<code>2</code>"],
            ["<code>.zfill(n)</code>", "Pad with leading zeros", "<code>'007'</code>"],
        ],
    )}

    <h3>split and join, the two workhorses</h3>
    {code('''crew = "Guybrush,Elaine,Otis,Meathook"

members = crew.split(",")
print(members)
print(len(members), "crew members")

print(" and ".join(members))
print("\\n".join(members))''',
          expect="""['Guybrush', 'Elaine', 'Otis', 'Meathook']
4 crew members
Guybrush and Elaine and Otis and Meathook
Guybrush
Elaine
Otis
Meathook""")}
    <p>
      <code>split</code> and <code>join</code> are opposites, and between them they handle a
      startling proportion of real-world data work. Note the slightly backwards-looking
      <code>separator.join(list)</code> order. Everyone writes it the wrong way round the
      first ten times.
    </p>

    <h2>Escapes: characters with special jobs</h2>
    {code(r'''print("Line one\nLine two")
print("Column\tone\tColumn two")
print("She said \"hello\" to me.")
print('It\'s fine with single quotes too.')
print("A backslash: \\")
print(r"A raw string ignores escapes: C:\new\table")''',
          expect=r"""Line one
Line two
Column	one	Column two
She said "hello" to me.
It's fine with single quotes too.
A backslash: \
A raw string ignores escapes: C:\new\table""")}
    <p>
      That last one matters on Windows and in Lesson 25 on regular expressions.
      <code>"C:\new"</code> contains a newline, because <code>\\n</code> is special.
      <code>r"C:\new"</code> is the literal text you meant.
    </p>

    <h2>Multi-line strings</h2>
    {code('''sign = """
   ==========================
     STAN'S PREVIOUSLY OWNED
        VESSELS
   ==========================
"""
print(sign)''',
          expect="""
   ==========================
     STAN'S PREVIOUSLY OWNED
        VESSELS
   ==========================
""")}
    <p>
      Three quotes let a string span lines. These are also how Python documents functions
      (Lesson 17) and how you will write prompts for a language model in Level 6.
    </p>

    {exercise(1, "Clean up user input",
              "<p>Someone typed <code>\"  ELAINE.MARLEY@melee.gov  \"</code>. Produce a tidy "
              "lowercase address with no surrounding spaces, then print just the part before "
              "the @ and just the domain.</p>",
              code('''raw = "  ELAINE.MARLEY@melee.gov  "

email = raw.strip().lower()
user, domain = email.split("@")

print(f"clean:  {email}")
print(f"user:   {user}")
print(f"domain: {domain}")''',
                   expect="""clean:  elaine.marley@melee.gov
user:   elaine.marley
domain: melee.gov"""))}

    {exercise(2, "Initials",
              "<p>From a full name like <code>\"guybrush ulysses threepwood\"</code>, print "
              "initials in the form <code>G.U.T.</code></p>",
              code('''full = "guybrush ulysses threepwood"

parts = full.split()
initials = ".".join(part[0].upper() for part in parts) + "."
print(initials)''',
                   expect="G.U.T.")
              + "<p>That <code>for</code> inside the brackets is a generator expression, and "
              "you meet it properly in Lesson 16. Reading it aloud works: 'the first letter, "
              "uppercased, of each part'.</p>")}

    {exercise(3, "Is it a palindrome?",
              "<p>Check whether a phrase reads the same backwards, ignoring case and spaces. "
              "Test it on <code>\"Never odd or even\"</code>.</p>",
              code('''phrase = "Never odd or even"

cleaned = phrase.lower().replace(" ", "")
print(cleaned)
print(cleaned == cleaned[::-1])''',
                   expect="""neveroddoreven
True""")
              + "<p><code>[::-1]</code> is the idiomatic Python reverse. It reads as 'the whole "
              "thing, stepping backwards', and once you have seen it twice you will never "
              "forget it.</p>")}
""",
)

# ---------------------------------------------------------------- 5
_add(
    level=1,
    num="5",
    slug="05-input",
    id="py-05-input",
    card="Asking the human a question, and the number-one beginner trap that follows.",
    title="Talking to the Human",
    emoji="💬",
    desc="input(), converting what comes back, and why input() always hands you text.",
    lede="""So far your programs have monologued. Time to let them listen, and to meet the
    trap that catches every single beginner exactly once.""",
    body=f"""
    <h2>input() asks a question</h2>
    {code('''name = input("What is your name? ")
print(f"Nice to meet you, {name}.")''',
          stdin="Guybrush Threepwood",
          expect="""What is your name? Guybrush Threepwood
Nice to meet you, Guybrush Threepwood.""")}
    <p>
      When you press ▶ run here, your browser pops up a box. In a terminal, the program stops
      and waits for you to type and press Enter. Either way, <code>input()</code> hands back
      whatever the human typed, and you catch it in a variable.
    </p>
    <p>
      Note the trailing space in <code>"What is your name? "</code>. Without it, the cursor
      would sit flush against the question mark and look wrong. Small thing, and people notice.
    </p>

    <h2>The trap</h2>
    <p>Everything <code>input()</code> returns is text. Everything. Always.</p>
    {code('''age = input("How old are you? ")
print(f"You said: {age}")
print(f"Its type is: {type(age)}")''',
          stdin="30",
          expect="""How old are you? 30
You said: 30
Its type is: <class 'str'>""")}
    <p>So this breaks:</p>
    {code('''age = input("How old are you? ")
print(age + 10)''', run=False, verify="skip")}
    {tb('''Traceback (most recent call last):
  File "ages.py", line 2, in <module>
    print(age + 10)
          ~~~~^~~~
TypeError: can only concatenate str (not "int") to str''')}

    {voice("LOGIC", "Easy: Success",
           "Read the error as English and it is telling the truth precisely: you asked to "
           "add a str and an int, and Python refuses to guess which one you meant. Should "
           "'30' + 10 be 40, or '3010'? Both are defensible. Python declines to flip a coin "
           "on your behalf.")}

    <p>The fix is to convert, explicitly:</p>
    {code('''age = int(input("How old are you? "))
print(f"In ten years you will be {age + 10}.")''',
          stdin="30",
          expect="""How old are you? 30
In ten years you will be 40.""")}
    {table(
        ["You want", "Wrap it in", "Example"],
        [["A whole number", "<code>int()</code>", "<code>int(input(\"Age? \"))</code>"],
         ["A decimal", "<code>float()</code>", "<code>float(input(\"Price? \"))</code>"],
         ["Text", "nothing at all", "<code>input(\"Name? \")</code>"]],
    )}

    <h2>What if they type nonsense?</h2>
    <p>
      <code>int("banana")</code> raises <code>ValueError</code> and your program stops dead.
      Level 3 teaches the proper defence (<code>try</code>/<code>except</code>, Lesson 22).
      Until then, know that this is the correct instinct to be worried about: any program that
      trusts what a human typed is one typo away from a crash.
    </p>
    {callout("info", "🛡️ A preview of the grown-up answer",
             "<p>You are not expected to understand this yet. It is here so that when you "
             "reach Lesson 22 it feels familiar rather than new.</p>")}
    {code('''raw = input("How many? ")

try:
    count = int(raw)
    print(f"Right, {count} of them.")
except ValueError:
    print(f"'{raw}' is not a number I can use. Try digits only.")''',
          stdin="three",
          expect="""How many? three
'three' is not a number I can use. Try digits only.""")}

    <h2>Several questions</h2>
    {code('''name = input("Name: ")
ship = input("Ship: ")
crew = int(input("Crew size: "))

print()
print("=" * 34)
print(f"  Captain {name}")
print(f"  Vessel:  {ship}")
print(f"  Crew:    {crew} ({crew * 2} legs)")
print("=" * 34)''',
          stdin="Guybrush\nSea Monkey\n12",
          expect="""Name: Guybrush
Ship: Sea Monkey
Crew size: 12

==================================
  Captain Guybrush
  Vessel:  Sea Monkey
  Crew:    12 (24 legs)
==================================""")}
    <p>
      Two small tricks worth stealing: <code>print()</code> with nothing in it prints an empty
      line, and <code>"=" * 34</code> repeats a character to draw a rule. Multiplying text is
      a Python nicety you will use constantly for quick command-line output.
    </p>

    <h2>The other half: printing well</h2>
    {code('''print("no", "newline", "between these", end=" -> ")
print("see?")

print("a", "b", "c", sep=" | ")
print("2026", "08", "17", sep="-")''',
          expect="""no newline between these -> see?
a | b | c
2026-08-17""")}
    <p>
      <code>end=</code> replaces the newline that <code>print</code> normally adds, and
      <code>sep=</code> replaces the space it puts between items. Two keyword arguments,
      surprisingly handy, and a first look at a Python feature you meet properly in Lesson 18.
    </p>

    {exercise(1, "The tavern greeter",
              "<p>Ask for a name and a favourite drink, then print a greeting that uses both, "
              "with the name in title case however they typed it.</p>",
              code('''name = input("Name: ")
drink = input("Poison of choice: ")

print(f"Welcome to the Scumm Bar, {name.strip().title()}.")
print(f"One {drink.strip().lower()}, coming up.")''',
                   stdin="  gUYBRUSH  \n  GROG  ",
                   expect="""Name:   gUYBRUSH
Poison of choice:   GROG
Welcome to the Scumm Bar, Guybrush.
One grog, coming up."""))}

    {exercise(2, "Rectangle calculator",
              "<p>Ask for a width and a height as decimals, then print the area and the "
              "perimeter to one decimal place.</p>",
              code('''width = float(input("Width: "))
height = float(input("Height: "))

area = width * height
perimeter = 2 * (width + height)

print(f"Area:      {area:.1f}")
print(f"Perimeter: {perimeter:.1f}")''',
                   stdin="3.5\n4.2",
                   expect="""Width: 3.5
Height: 4.2
Area:      14.7
Perimeter: 15.4"""))}

    {exercise(3, "Find the bug",
              "<p>This is meant to add two numbers. Why does entering 2 and 3 produce "
              "<code>23</code>?</p>"
              + code('''a = input("First number: ")
b = input("Second number: ")
print(a + b)''', run=False, verify="skip"),
              "<p>Because <code>a</code> and <code>b</code> are strings, and <code>+</code> on "
              "two strings glues them together instead of adding. <code>\"2\" + \"3\"</code> is "
              "<code>\"23\"</code>, which is correct behaviour for the code that was actually "
              "written.</p>"
              + code('''a = int(input("First number: "))
b = int(input("Second number: "))
print(a + b)''', stdin="2\n3", expect="""First number: 2
Second number: 3
5""")
              + "<p>This bug is a rite of passage. You get it once, you never get it again.</p>")}
""",
)

# ---------------------------------------------------------------- 6
_add(
    level=1,
    num="6",
    slug="06-booleans",
    id="py-06-booleans",
    card="True, False, comparisons, and the truthiness rules that make Python code short.",
    title="True, False and Questions",
    emoji="⚖️",
    desc="Booleans, comparison operators, and, or, not, truthiness, and the == versus is trap.",
    lede="""Before a program can decide anything, it has to ask a question that has exactly
    two possible answers. Here is how Python asks.""",
    body=f"""
    <h2>A third kind of value</h2>
    {code('''sunny = True
raining = False

print(sunny, type(sunny))
print(raining)''',
          expect="""True <class 'bool'>
False""")}
    <p>
      Capital T, capital F, no quotes. <code>"True"</code> with quotes is a piece of text and
      a completely different thing. The type is named <code>bool</code> after George Boole,
      a Victorian mathematician who worked out the algebra of true and false about ninety
      years before there was a computer to run it on.
    </p>

    <h2>Comparisons produce booleans</h2>
    {code('''print(5 > 3)
print(5 < 3)
print(5 == 5)      # equal? two equals signs!
print(5 != 5)      # not equal
print(5 >= 5)
print("a" < "b")   # alphabetical order''',
          expect="""True
False
True
False
True
True""")}

    {callout("danger", "🪤 One equals sign or two",
             "<p><code>=</code> assigns a value. <code>==</code> asks a question. Writing "
             "<code>if x = 5</code> is a <code>SyntaxError</code> in Python, which is a "
             "kindness: in C it silently compiles and has caused decades of bugs.</p>")}

    <h2>Combining questions</h2>
    {code('''age = 25
has_ticket = True
banned = False

print(age >= 18 and has_ticket)
print(age >= 65 or has_ticket)
print(not banned)
print(age >= 18 and has_ticket and not banned)''',
          expect="""True
True
True
True""")}
    {table(
        ["Operator", "True when", "Think of it as"],
        [["<code>and</code>", "both sides are true", "the strict bouncer"],
         ["<code>or</code>", "at least one side is true", "the generous bouncer"],
         ["<code>not</code>", "flips true to false", "the contrarian"]],
    )}
    <p>
      Python uses the English words, not <code>&amp;&amp;</code> and <code>||</code> like most
      other languages. Read your conditions out loud: if the sentence makes sense in English,
      it is probably right.
    </p>

    <h3>Chained comparisons, a genuine Python nicety</h3>
    {code('''score = 75

print(0 <= score <= 100)          # Python allows this and it means what you think
print(70 < score < 80)''',
          expect="""True
True""")}
    <p>
      Most languages force you to write <code>score >= 0 and score &lt;= 100</code>. Python
      lets you write it the way a mathematician would. It is one of those small touches that
      make people fond of the language.
    </p>

    <h2>Truthiness: everything can answer the question</h2>
    <p>
      Python will happily treat any value as a yes or no. The rule is simple and worth
      committing to memory: <strong>empty and zero are false, everything else is true</strong>.
    </p>
    {code('''print(bool(0), bool(1), bool(-1))
print(bool(""), bool("a"), bool(" "))
print(bool([]), bool([1]))
print(bool({}), bool({"a": 1}))
print(bool(None))''',
          expect="""False True True
False True True
False True
False True
False""")}
    <p>This is why real Python code looks like this:</p>
    {code('''name = ""

if not name:
    print("You did not give me a name.")

crew = ["Otis"]
if crew:
    print(f"There are {len(crew)} aboard.")''',
          expect="""You did not give me a name.
There are 1 aboard.""")}
    <p>
      <code>if crew:</code> rather than <code>if len(crew) > 0:</code>. Shorter, and every
      Python programmer reads it instantly. Note the space in <code>bool(" ")</code> is
      <code>True</code>: a space is a character, so the string is not empty. That distinction
      has ruined many a form validator.
    </p>

    <h2>None: the value that means "nothing here"</h2>
    {code('''winner = None

print(winner)
print(winner is None)
print(type(winner))''',
          expect="""None
True
<class 'NoneType'>""")}
    <p>
      <code>None</code> is Python's way of saying "deliberately empty". It is not zero and not
      an empty string; it is the absence of a value. Functions that do not return anything
      return <code>None</code>, and it is the standard placeholder for "not decided yet".
    </p>

    <h2>== versus is</h2>
    {code('''a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)     # same contents?
print(a is b)     # the very same object in memory?
print(a is c)''',
          expect="""True
False
True""")}
    {voice("PERCEPTION", "Medium: Success",
           "Two identical twins are equal but not identical. Point at one twin and give the "
           "finger a second name, and now you have two names for one person: that is 'is'. "
           "Python's == asks 'do these look the same', is asks 'are these literally the same "
           "thing'.")}
    <p>
      The rule in practice: use <code>==</code> for everything, except when comparing against
      <code>None</code>, <code>True</code> or <code>False</code>, where the convention is
      <code>is</code>. So: <code>if value is None:</code>, always.
    </p>

    <h2>Short circuits</h2>
    {code('''def expensive_check():
    print("  (this ran)")
    return True

print("First:")
result = False and expensive_check()

print("Second:")
result = True or expensive_check()

print("Neither of those printed the marker, because Python stopped early.")''',
          expect="""First:
Second:
Neither of those printed the marker, because Python stopped early.""")}
    <p>
      With <code>and</code>, if the left side is false the answer is already false, so Python
      never looks at the right side. This is not just an optimisation, it is a tool: it lets
      you write <code>if name and name[0] == "G":</code> without crashing on an empty name,
      because the second half never runs when the first half fails.
    </p>

    {exercise(1, "Can they ride?",
              "<p>A rollercoaster requires a height of at least 140cm, an age of at least 12, "
              "and that the rider is not currently holding a full mug of grog. Write the "
              "condition and test it with a few values.</p>",
              code('''height = 152
age = 14
holding_grog = False

can_ride = height >= 140 and age >= 12 and not holding_grog
print(f"Cleared to ride: {can_ride}")

# and one who is not
print(f"Second rider:    {130 >= 140 and 30 >= 12 and not False}")''',
                   expect="""Cleared to ride: True
Second rider:    False"""))}

    {exercise(2, "Predict the truthiness",
              "<p>For each, say True or False before running.</p>"
              + code('''print(bool("False"))
print(bool(0.0))
print(bool([0]))
print(bool(" "))
print(None == False)''', run=False, verify="compile"),
              "<ol><li><code>True</code>. It is a non-empty string. The contents are "
              "irrelevant.</li>"
              "<li><code>False</code>. Zero is zero, even as a float.</li>"
              "<li><code>True</code>. The list has one item in it. That the item is falsy does "
              "not matter.</li>"
              "<li><code>True</code>. A space is a character.</li>"
              "<li><code>False</code>. None is not False, it is None. This is exactly why the "
              "convention is <code>is None</code>.</li></ol>")}

    {exercise(3, "Fix the login check",
              "<p>This is supposed to allow entry when the password matches and the account "
              "is not locked. It has two bugs.</p>"
              + code('''password = "grog"
locked = False

if password = "grog" and locked == True:
    print("Welcome")''', run=False, verify="skip"),
              "<p>Bug one: <code>=</code> instead of <code>==</code>, which is a "
              "<code>SyntaxError</code>. Bug two: the logic is backwards; it demands the "
              "account <em>is</em> locked.</p>"
              + code('''password = "grog"
locked = False

if password == "grog" and not locked:
    print("Welcome")''', expect="Welcome")
              + "<p><code>not locked</code> rather than <code>locked == False</code>: shorter, "
              "and it reads like the sentence you would say out loud.</p>")}
""",
)

# ---------------------------------------------------------------- 7
_add(
    level=1,
    num="7",
    slug="07-decisions",
    id="py-07-decisions",
    card="if, elif, else, and why Python makes your indentation part of the language.",
    title="Making Decisions",
    emoji="🔀",
    desc="if, elif and else, indentation as syntax, nesting, and the conditional expression.",
    lede="""This is the lesson where your programs stop being a straight line and start being
    a map with branches. It is also where Python's most famous quirk shows up.""",
    body=f"""
    <h2>if</h2>
    {code('''grog = 8

if grog > 5:
    print("That is enough grog.")
    print("Genuinely, that is plenty.")

print("This line always runs, branch or no branch.")''',
          expect="""That is enough grog.
Genuinely, that is plenty.
This line always runs, branch or no branch.""")}
    <p>Two pieces of punctuation are doing all the work:</p>
    <ul>
      <li>The <strong>colon</strong> at the end of the <code>if</code> line. It means "a block
      follows". Forgetting it is the most common syntax error in Python, by a distance.</li>
      <li>The <strong>indentation</strong> of the next lines. Those four spaces are what puts
      those lines inside the <code>if</code>.</li>
    </ul>

    <h2>Indentation is not decoration. It is the syntax.</h2>
    <p>
      Most languages mark blocks with curly braces and treat layout as a matter of taste.
      Python has no braces: the layout <em>is</em> the structure. This is the single thing
      newcomers find strangest, and the thing they defend most fiercely after six months.
    </p>
    {code('''ready = True

if ready:
    print("inside the if")
    print("also inside")
print("outside again")''',
          expect="""inside the if
also inside
outside again""")}

    {voice("ENCYCLOPEDIA", "Medium: Success",
           "The reasoning is worth knowing. In brace languages, programmers indent anyway, "
           "for humans. So there are two structures in every file: the one the compiler reads "
           "(braces) and the one the human reads (indentation). When they disagree, the human "
           "is misled. Apple's 2014 'goto fail' security bug was exactly this: a stray "
           "indented line that looked like it was inside an if and was not. Python makes them "
           "the same structure so they cannot disagree.")}

    {callout("danger", "⚠️ Four spaces. Never tabs. Never mixed.",
             "<p>Python accepts either, but mixing them in one file gives "
             "<code>TabError: inconsistent use of tabs and spaces</code>, and the two look "
             "identical on screen, which makes it maddening. Set your editor to insert four "
             "spaces when you press Tab and forget the problem exists. In VS Code that is the "
             "default. PEP 8 says four spaces, so the whole world agrees on this one.</p>")}

    <h2>if / else</h2>
    {code('''password = "grog"

if password == "swordfish":
    print("Access granted.")
else:
    print("Access denied. You fight like a dairy farmer.")''',
          expect="Access denied. You fight like a dairy farmer.")}

    <h2>if / elif / else: choosing from many</h2>
    {code('''score = 87

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score {score} earns a {grade}.")''',
          expect="Score 87 earns a B.")}
    <p>
      <code>elif</code> is short for "else if". Python checks each condition in order and
      <strong>stops at the first true one</strong>. That is why <code>score >= 80</code> works
      without also checking <code>score &lt; 90</code>: if we reached that line at all, the
      first test must have failed.
    </p>
    <p>Order matters enormously. This version is broken:</p>
    {code('''score = 95

if score >= 60:
    grade = "D"          # always wins, because it is checked first
elif score >= 90:
    grade = "A"          # unreachable
else:
    grade = "F"

print(f"Score {score} earns a {grade}. Which is wrong.")''',
          expect="Score 95 earns a D. Which is wrong.")}

    <h2>Nesting</h2>
    {code('''logged_in = True
is_admin = False

if logged_in:
    print("Welcome back.")
    if is_admin:
        print("Admin console available.")
    else:
        print("Standard account.")
else:
    print("Please sign in.")''',
          expect="""Welcome back.
Standard account.""")}
    <p>
      Each level of nesting is another four spaces. It works, and past two levels deep it
      becomes hard to read. When you find yourself at three or four, that is a signal to
      restructure, usually by pulling a piece out into a function (Lesson 17) or by returning
      early.
    </p>

    <h2>The one-line version</h2>
    {code('''age = 20
status = "adult" if age >= 18 else "minor"
print(status)

crew = []
print(f"Crew: {len(crew) if crew else 'nobody yet'}")''',
          expect="""adult
Crew: nobody yet""")}
    <p>
      This is a <strong>conditional expression</strong>, and reads value-first: "adult, if age
      is 18 or more, otherwise minor". Lovely for short choices, unreadable for long ones. If
      it does not fit comfortably on one line, use a normal <code>if</code>.
    </p>

    <h2>match: the modern multi-way branch</h2>
    <p>Python 3.10 added <code>match</code>, which is tidier when you are comparing one value
    against many possibilities:</p>
    {code('''command = "north"

match command:
    case "north" | "n":
        print("You walk north. The jungle thickens.")
    case "south" | "s":
        print("You walk south. The beach is behind you.")
    case "look":
        print("Trees. So many trees.")
    case _:
        print(f"I do not know how to '{command}'.")''',
          expect="You walk north. The jungle thickens.")}
    <p>
      The <code>_</code> case is the catch-all, like <code>else</code>. <code>match</code> can
      do far more than this (it can pull apart lists and objects), and Lesson 33 returns to it.
      For simple choices, either style is fine; <code>match</code> shines when there are many.
    </p>

    {exercise(1, "The bouncer",
              "<p>Write a program that decides entry. Under 18: refused. 18 to 20: allowed but "
              "no alcohol. 21 and over: allowed. Print a different message for each.</p>",
              code('''age = 19

if age < 18:
    print("Sorry, come back in a few years.")
elif age < 21:
    print("You are in, but soft drinks only.")
else:
    print("Enjoy your evening.")''', expect="You are in, but soft drinks only.")
              + "<p>Notice the second condition is just <code>age &lt; 21</code>, with no need "
              "for <code>age >= 18 and age &lt; 21</code>. Reaching that line already proves "
              "the first test failed.</p>")}

    {exercise(2, "FizzBuzz, the famous one",
              "<p>For the number 15: print <code>Fizz</code> if it divides by 3, "
              "<code>Buzz</code> if by 5, <code>FizzBuzz</code> if by both, and the number "
              "otherwise. Careful with the order.</p>",
              code('''n = 15

if n % 3 == 0 and n % 5 == 0:
    print("FizzBuzz")
elif n % 3 == 0:
    print("Fizz")
elif n % 5 == 0:
    print("Buzz")
else:
    print(n)''', expect="FizzBuzz")
              + "<p>The both-case must come first. Put it last and 15 matches "
              "<code>n % 3 == 0</code> and prints Fizz, and you have written the single most "
              "common wrong answer to the single most famous interview question. Lesson 9 "
              "makes it print 1 to 100.</p>")}

    {exercise(3, "Find the indentation bug",
              "<p>This should only congratulate winners. What does it actually do, and why?</p>"
              + code('''score = 20

if score > 100:
    print("New high score!")
print("Congratulations!")''', run=False, verify="compile"),
              "<p>It always congratulates. The second <code>print</code> is not indented, so "
              "it is not inside the <code>if</code> at all; it is the next statement in the "
              "program.</p>"
              + code('''score = 20

if score > 100:
    print("New high score!")
    print("Congratulations!")
else:
    print("Not this time.")''', expect="Not this time.")
              + "<p>In a brace language this bug hides. In Python it is visible the moment you "
              "look at the shape of the code, which is the entire argument for the design.</p>")}
""",
)

# ---------------------------------------------------------------- 8
_add(
    level=1,
    num="8",
    slug="08-while",
    id="py-08-while",
    card="Repeating until something changes, break and continue, and how to escape a loop that never ends.",
    title="Loops That Repeat: while",
    emoji="🔁",
    desc="The while loop, break, continue, sentinel values, and what to do about infinite loops.",
    lede="""Computers are unbelievably good at doing the same thing over and over without
    complaining. This is the lesson where you stop copying and pasting.""",
    body=f"""
    <h2>while: keep going until</h2>
    {code('''grog = 5

while grog > 0:
    print(f"{grog} mugs of grog on the wall")
    grog -= 1

print("The bar is dry.")''',
          expect="""5 mugs of grog on the wall
4 mugs of grog on the wall
3 mugs of grog on the wall
2 mugs of grog on the wall
1 mugs of grog on the wall
The bar is dry.""")}
    <p>The shape is always the same, and it has exactly three moving parts:</p>
    <ol class="steps">
      <li><strong>Set something up</strong> before the loop (<code>grog = 5</code>).</li>
      <li><strong>Ask a question</strong> at the top. True means go round again, false means
      stop.</li>
      <li><strong>Change something</strong> inside the loop so the answer eventually becomes
      false (<code>grog -= 1</code>).</li>
    </ol>
    <p>Miss step three and the loop runs forever. Which is next.</p>

    <h2>The infinite loop, and the escape hatch</h2>
    {code('''grog = 5

while grog > 0:
    print("still 5 mugs, forever, until the heat death of the universe")
    # grog never changes, so the condition is never false''', run=False, verify="skip")}

    {voice("REACTION SPEED", "Easy: Success",
           "Ctrl+C. In the terminal, hold Control and press C. The program stops immediately. "
           "Not Cmd+C on a Mac, Control+C, on every platform. Learn it now, use it today.")}

    <p>
      In this school's playground, the run button gives up after twenty seconds and tells you
      so, which is friendlier than freezing your browser. On your own machine, Ctrl+C is the
      answer. Writing an infinite loop is a rite of passage, not a disaster, and everybody has
      done it.
    </p>

    <h2>Waiting for the right answer</h2>
    {code('''answer = ""

while answer != "swordfish":
    answer = input("Password: ")
    if answer != "swordfish":
        print("  That is not the password.")

print("The door swings open.")''',
          stdin="grog\nmonkey\nswordfish",
          expect="""Password: grog
  That is not the password.
Password: monkey
  That is not the password.
Password: swordfish
The door swings open.""")}
    <p>
      This is the classic use of <code>while</code>: you do not know in advance how many times
      it will run. That is the whole difference between <code>while</code> and the
      <code>for</code> loop in the next lesson. Unknown number of repeats: <code>while</code>.
      Known collection to walk through: <code>for</code>.
    </p>

    <h2>break: leave immediately</h2>
    {code('''while True:
    command = input("> ")
    if command == "quit":
        print("Farewell.")
        break
    print(f"You try to {command}. Nothing happens.")''',
          stdin="look\ntake grog\nquit",
          expect="""> look
You try to look. Nothing happens.
> take grog
You try to take grog. Nothing happens.
> quit
Farewell.""")}
    <p>
      <code>while True:</code> with a <code>break</code> inside is a completely respectable
      pattern, not a cheat. It says "loop until I decide to stop", and it is the standard shape
      for menus, game loops and command prompts. The important thing is that a
      <code>break</code> exists somewhere and is reachable.
    </p>

    <h2>continue: skip the rest of this round</h2>
    {code('''number = 0

while number < 10:
    number += 1
    if number % 2 == 0:
        continue          # jump straight back to the top
    print(f"{number} is odd")''',
          expect="""1 is odd
3 is odd
5 is odd
7 is odd
9 is odd""")}
    {callout("danger", "🪤 continue in a while loop is a trap",
             "<p>If your <code>continue</code> jumps back <em>before</em> the line that "
             "changes the counter, you get an infinite loop. In the example above, "
             "<code>number += 1</code> is the very first line for exactly that reason. Move it "
             "to the bottom and the program hangs at 2, forever.</p>")}

    <h2>while / else, a Python curiosity</h2>
    {code('''attempts = 3

while attempts > 0:
    print(f"{attempts} attempts left")
    attempts -= 1
else:
    print("Ran out of attempts, and no break happened.")''',
          expect="""3 attempts left
2 attempts left
1 attempts left
Ran out of attempts, and no break happened.""")}
    <p>
      The <code>else</code> on a loop runs only if the loop finished naturally, without a
      <code>break</code>. It is genuinely useful for searches ("if we got through the whole
      list without finding it..."), rare in the wild, and confusing enough that many style
      guides discourage it. Know it exists so it does not startle you in someone else's code.
    </p>

    <h2>A real one: the number guessing game</h2>
    {code('''import random

secret = random.randint(1, 100)
guesses = 0

while True:
    guess = int(input("Guess (1-100): "))
    guesses += 1

    if guess < secret:
        print("  Higher.")
    elif guess > secret:
        print("  Lower.")
    else:
        print(f"Got it in {guesses} guesses.")
        break''',
          run=False, verify="compile")}
    <p>
      That is a complete, genuinely fun program in fourteen lines, and it is
      <a href="../build/01-guessing-game.html">Project 1</a> in the workshop, where you build
      it properly with input validation and a play-again loop.
    </p>

    {exercise(1, "Countdown",
              "<p>Count down from 10 to 1, then print 'Liftoff'. One line per number.</p>",
              code('''n = 10

while n > 0:
    print(n)
    n -= 1

print("Liftoff! 🚀")''',
                   expect="""10
9
8
7
6
5
4
3
2
1
Liftoff! 🚀"""))}

    {exercise(2, "Sum until zero",
              "<p>Keep asking for numbers and adding them up. When the user enters 0, stop and "
              "print the total and how many numbers were given.</p>",
              code('''total = 0
count = 0

while True:
    number = int(input("Number (0 to finish): "))
    if number == 0:
        break
    total += number
    count += 1

print(f"{count} numbers, total {total}")''',
                   stdin="5\n10\n3\n0",
                   expect="""Number (0 to finish): 5
Number (0 to finish): 10
Number (0 to finish): 3
Number (0 to finish): 0
3 numbers, total 18""")
              + "<p>A value that means 'stop' is called a <strong>sentinel</strong>. It is a "
              "standard technique, and its weakness is that the sentinel can never be real "
              "data: this program can never total a genuine zero.</p>")}

    {exercise(3, "Why does this never end?",
              "<p>Spot the bug without running it. There are two ways to fix it.</p>"
              + code('''count = 1
while count < 5:
    print(count)
count += 1''', run=False, verify="skip"),
              "<p><code>count += 1</code> is outside the loop: it is not indented. So "
              "<code>count</code> is 1 forever, the condition is true forever, and the loop "
              "prints 1 until the sun burns out.</p>"
              + code('''count = 1
while count < 5:
    print(count)
    count += 1''', expect="""1
2
3
4""")
              + "<p>The other fix is a <code>for</code> loop, which removes the possibility "
              "entirely by counting for you. That is the next lesson, and it is why "
              "experienced Python programmers reach for <code>for</code> far more often than "
              "<code>while</code>.</p>")}
""",
)

# ---------------------------------------------------------------- 9
_add(
    level=1,
    num="9",
    slug="09-for",
    id="py-09-for",
    card="for, range and enumerate: walking through things without ever writing a counter again.",
    title="Loops That Count: for",
    emoji="🔂",
    desc="The for loop, range(), enumerate(), looping over strings and lists, and nested loops.",
    lede="""If while is 'keep going until', for is 'do this once for each of these'. It is the
    loop you will write ninety percent of the time.""",
    body=f"""
    <h2>for: once for each item</h2>
    {code('''for item in ["rubber chicken", "grog", "map", "sword"]:
    print(f"You are carrying: {item}")''',
          expect="""You are carrying: rubber chicken
You are carrying: grog
You are carrying: map
You are carrying: sword""")}
    <p>
      Read it as English: "for each item in this collection, do the following". The variable
      <code>item</code> is created by the loop and takes each value in turn. You do not
      declare it, you do not increment it, and you cannot get the counting wrong, because
      there is no counting.
    </p>

    {voice("VOLITION", "Medium: Success",
           "Notice what just disappeared. No counter to initialise, no condition to get "
           "backwards, no increment to forget, no off-by-one at the end. An entire genus of "
           "bug, extinct, because you described what you wanted instead of how to step "
           "through it.")}

    <h2>range: when you want numbers</h2>
    {code('''for n in range(5):
    print(n)''',
          expect="""0
1
2
3
4""")}
    <p>
      <code>range(5)</code> gives five numbers <strong>starting at 0</strong>: 0, 1, 2, 3, 4.
      Five numbers, not up to five. This is the same start-included, end-excluded rule as
      slicing, and it is consistent throughout the language.
    </p>
    {code('''print(list(range(5)))
print(list(range(1, 6)))
print(list(range(0, 20, 5)))
print(list(range(10, 0, -2)))''',
          expect="""[0, 1, 2, 3, 4]
[1, 2, 3, 4, 5]
[0, 5, 10, 15]
[10, 8, 6, 4, 2]""")}
    {table(
        ["Written", "Means"],
        [["<code>range(stop)</code>", "0 up to but not including stop"],
         ["<code>range(start, stop)</code>", "start up to but not including stop"],
         ["<code>range(start, stop, step)</code>", "as above, jumping by step (negative counts down)"]],
    )}

    <h2>Looping over text</h2>
    {code('''for letter in "GROG":
    print(letter, end=" ")

print()

word = "banana"
count = 0
for letter in word:
    if letter == "a":
        count += 1
print(f"{count} letter a's in {word}")''',
          expect="""G R O G
3 letter a's in banana""")}

    <h2>enumerate: when you need the position too</h2>
    {code('''crew = ["Guybrush", "Elaine", "Otis"]

# The clumsy way, which you see beginners write:
for i in range(len(crew)):
    print(f"{i}: {crew[i]}")

print("---")

# The Python way:
for i, name in enumerate(crew):
    print(f"{i}: {name}")

print("---")

# Humans count from 1:
for position, name in enumerate(crew, start=1):
    print(f"{position}. {name}")''',
          expect="""0: Guybrush
1: Elaine
2: Otis
---
0: Guybrush
1: Elaine
2: Otis
---
1. Guybrush
2. Elaine
3. Otis""")}
    {callout("tip", "🎯 The rule of thumb",
             "<p>If you ever write <code>for i in range(len(something))</code>, stop. You "
             "almost certainly want <code>for item in something</code>, or "
             "<code>enumerate</code> if you genuinely need the index. Experienced reviewers "
             "spot that pattern instantly.</p>")}

    <h2>zip: walking two collections together</h2>
    {code('''names = ["Guybrush", "Elaine", "LeChuck"]
roles = ["pirate", "governor", "ghost"]

for name, role in zip(names, roles):
    print(f"{name:10} is a {role}")''',
          expect="""Guybrush   is a pirate
Elaine     is a governor
LeChuck    is a ghost""")}
    <p>
      <code>zip</code> stops at the shortest one, which is usually what you want and
      occasionally a silent bug. If you need it to complain about mismatched lengths, use
      <code>zip(a, b, strict=True)</code>, added in Python 3.10.
    </p>

    <h2>Accumulating: the pattern behind everything</h2>
    {code('''prices = [4.50, 12.00, 3.25, 8.75]

total = 0
for price in prices:
    total += price

print(f"Total: {total:.2f}")
print(f"Average: {total / len(prices):.2f}")
print(f"Built in: {sum(prices):.2f}")''',
          expect="""Total: 28.50
Average: 7.12
Built in: 28.50""")}
    <p>
      Start with an empty accumulator, add to it each time round, use it after. That shape
      (with a list, a string, a dictionary or a counter) is behind a huge fraction of all
      programs. Python also has <code>sum</code>, <code>min</code>, <code>max</code> and
      <code>len</code> built in, and you should use them when they fit.
    </p>

    <h2>Nested loops</h2>
    {code('''for row in range(1, 4):
    for col in range(1, 4):
        print(f"{row * col:3}", end="")
    print()''',
          expect="""  1  2  3
  2  4  6
  3  6  9""")}
    <p>
      The inner loop runs completely for every single step of the outer one: three rows times
      three columns is nine prints. This is how you handle grids, tables, chessboards and
      images. It is also where performance goes to die: two nested loops over 1,000 items each
      is a million steps. Lesson 51 has more to say about that.
    </p>

    <h2>FizzBuzz, finally complete</h2>
    {code('''for n in range(1, 21):
    if n % 15 == 0:
        print("FizzBuzz")
    elif n % 3 == 0:
        print("Fizz")
    elif n % 5 == 0:
        print("Buzz")
    else:
        print(n)''',
          expect="""1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz""")}
    <p>
      That is the whole of the famous interview screening question. It exists because a
      startling number of applicants cannot write it, and what it really tests is whether you
      thought about the order of the conditions.
    </p>

    {exercise(1, "Times table",
              "<p>Print the 7 times table from 7 x 1 to 7 x 12, one line each, neatly "
              "aligned.</p>",
              code('''for n in range(1, 13):
    print(f"7 x {n:2} = {7 * n:3}")''',
                   expect="""7 x  1 =   7
7 x  2 =  14
7 x  3 =  21
7 x  4 =  28
7 x  5 =  35
7 x  6 =  42
7 x  7 =  49
7 x  8 =  56
7 x  9 =  63
7 x 10 =  70
7 x 11 =  77
7 x 12 =  84"""))}

    {exercise(2, "Count the vowels",
              "<p>Count how many vowels are in a phrase, and report which ones appeared.</p>",
              code('''phrase = "The Secret of Monkey Island"

vowels = "aeiou"
count = 0
found = ""

for letter in phrase.lower():
    if letter in vowels:
        count += 1
        if letter not in found:
            found += letter

print(f"{count} vowels")
print(f"which were: {found}")''',
                   expect="""8 vowels
which were: eoia""")
              + "<p><code>in</code> works on strings as well as lists, and reads exactly as "
              "you would say it out loud. It is one of Python's nicest small features.</p>")}

    {exercise(3, "Draw a triangle",
              "<p>Print a right-angled triangle of stars, five rows tall, then the same "
              "triangle upside down.</p>",
              code('''for row in range(1, 6):
    print("*" * row)

print()

for row in range(5, 0, -1):
    print("*" * row)''',
                   expect="""*
**
***
****
*****

*****
****
***
**
*""")
              + "<p>No inner loop needed: multiplying a string does the repetition for you. "
              "When you can replace a loop with an expression, the code usually gets clearer, "
              "not just shorter.</p>")}
""",
)

# ---------------------------------------------------------------- 10
_add(
    level=1,
    num="10",
    slug="10-errors",
    id="py-10-errors",
    card="Tracebacks decoded, the eight errors you will actually meet, and a repeatable debugging method.",
    title="Reading Errors Without Fear",
    emoji="🚨",
    desc="How to read a Python traceback, the most common exception types, and a systematic debugging method.",
    lede="""This is the most valuable lesson in Level 1. Not because errors are interesting,
    but because the gap between a beginner and a competent programmer is mostly the speed at
    which they read an error message.""",
    body=f"""
    <h2>An error is a bug report written for you, by the machine, instantly, for free</h2>
    <p>
      Nobody writes correct code first time. Not you, not anyone. What separates people is
      that experienced programmers glance at the error, mutter something, and fix it in four
      seconds, while beginners feel a jolt of dread and start changing things at random.
    </p>
    <p>The dread is unnecessary. The message contains the answer. Here is how to read it.</p>

    <h2>Anatomy of a traceback</h2>
    {tb('''Traceback (most recent call last):
  File "adventure.py", line 12, in <module>
    show_room(rooms[3])
              ~~~~~^^^
IndexError: list index out of range''')}
    {table(
        ["Line", "What it is telling you"],
        [
            ["<code>Traceback (most recent call last)</code>", "A list of what called what. The <strong>last</strong> entry is where it actually broke"],
            ["<code>File \"adventure.py\", line 12</code>", "Exactly where to look"],
            ["<code>show_room(rooms[3])</code>", "The line itself"],
            ["<code>~~~~~^^^</code>", "Which part of the line went wrong. Python 3.11 added these and they are wonderful"],
            ["<code>IndexError</code>", "The category of problem"],
            ["<code>list index out of range</code>", "The specific problem, in English"],
        ],
    )}

    {voice("COMPOSURE", "Medium: Success",
           "Read the bottom line first. Then the file and line number. Then, only if you still "
           "need it, the middle. Most beginners read top to bottom, get lost in the call "
           "stack, and never reach the sentence that explains everything.")}

    <h2>The eight you will actually meet</h2>

    <h3>1. SyntaxError: it is not valid Python</h3>
    {code('print("hello"', run=False, verify="skip")}
    {tb('''  File "hello.py", line 1
    print("hello"
         ^
SyntaxError: '(' was never closed''')}
    <p>
      Caught before anything runs. Almost always a missing bracket, quote or colon. Key
      insight: <strong>look at the line above the one Python names</strong>. An unclosed
      bracket on line 8 is often only noticed on line 9.
    </p>

    <h3>2. IndentationError: your spacing is wrong</h3>
    {tb('''  File "game.py", line 4
    print("inside")
    ^
IndentationError: expected an indented block after 'if' statement on line 3''')}
    <p>
      You wrote a colon and then did not indent, or indented inconsistently. Four spaces, no
      tabs.
    </p>

    <h3>3. NameError: you used a name that does not exist</h3>
    {code('''score = 10
print(scroe)''', run=False, verify="skip")}
    {tb('''NameError: name 'scroe' is not defined. Did you mean: 'score'?''')}
    <p>
      Ninety percent of the time: a typo. Python 3.12 even suggests the correction. The other
      ten percent: you used a variable before creating it, or created it inside a function and
      tried to use it outside (Lesson 19).
    </p>

    <h3>4. TypeError: right idea, wrong kind of thing</h3>
    {code('print("Total: " + 42)', run=False, verify="skip")}
    {tb('TypeError: can only concatenate str (not "int") to str')}
    <p>The fix is usually a conversion or an f-string:</p>
    {code('''print("Total: " + str(42))
print(f"Total: {42}")''',
          expect="""Total: 42
Total: 42""")}

    <h3>5. ValueError: right type, impossible value</h3>
    {code('int("twelve")', run=False, verify="skip")}
    {tb("ValueError: invalid literal for int() with base 10: 'twelve'")}
    <p>
      A string is exactly what <code>int()</code> wants; that particular string is not a
      number. This is the error that user input causes, constantly.
    </p>

    <h3>6. IndexError: past the end</h3>
    {code('''crew = ["Guybrush", "Elaine", "Otis"]
print(crew[3])''', run=False, verify="skip")}
    {tb("IndexError: list index out of range")}
    <p>
      Three items means positions 0, 1 and 2. The last is always <code>len(x) - 1</code>, or
      simply <code>x[-1]</code>. This is the classic off-by-one.
    </p>

    <h3>7. KeyError: no such dictionary key</h3>
    {tb("KeyError: 'captain'")}
    <p>
      You asked a dictionary for something it does not have. Lesson 13 shows you
      <code>.get()</code>, which returns a default instead of exploding.
    </p>

    <h3>8. AttributeError: that thing cannot do that</h3>
    {code('''number = 42
number.upper()''', run=False, verify="skip")}
    {tb("AttributeError: 'int' object has no attribute 'upper'")}
    <p>
      <code>.upper()</code> is a string thing. Numbers do not have it. This one usually means
      a variable is not holding the type you thought it was, which makes it a good moment to
      <code>print(type(x))</code> and find out.
    </p>

    <h2>A method that always works</h2>
    <p>
      When the message alone is not enough, do not start changing lines at random. Do this
      instead. It is slower for thirty seconds and faster for the next two hours.
    </p>
    <ol class="steps">
      <li><strong>Read the last line.</strong> Out loud if necessary. It names the problem.</li>
      <li><strong>Go to the file and line number.</strong> Look at that line, and the one
      above it.</li>
      <li><strong>Print what you assumed.</strong> The bug is always in the gap between what
      you believe and what is true. Make the belief visible:
        {code('''row = "12,Guybrush,pirate"
parts = row.split(",")

print(f"{parts=}")
print(f"{len(parts)=}")
print(f"{type(parts[0])=}")''',
              expect="""parts=['12', 'Guybrush', 'pirate']
len(parts)=3
type(parts[0])=<class 'str'>""")}</li>
      <li><strong>Cut the program in half.</strong> Does the first half do what you expect?
      Then the bug is in the second half. Repeat. Ten halvings finds a bug in a thousand
      lines.</li>
      <li><strong>Explain it to a duck.</strong> Out loud, line by line, to a rubber duck or a
      houseplant. You will very often catch it yourself mid-sentence. This is a real, named,
      widely used technique.</li>
    </ol>

    {voice("RUBBER DUCK", "Easy: Success",
           "Go on. Tell me what line four does. No, not what it is supposed to do. What it "
           "does.",
           "...ah. You did not expect that either, did you.")}

    <h2>When you genuinely need help</h2>
    <p>A good question gets an answer in minutes. A bad one gets silence. The difference:</p>
    {table(
        ["Include", "Why"],
        [["What you are trying to do", "One sentence of context"],
         ["The smallest code that shows the problem", "Not your whole file. Cut it down; you will often solve it while cutting"],
         ["The <em>full</em> error message, as text", "Not a screenshot, not just the last line"],
         ["What you already tried", "Stops people repeating your work"],
         ["Your Python version", "<code>python3 --version</code>"]],
    )}
    <p>
      The act of writing that up solves the problem outright often enough to have a name: it
      is why Stack Overflow's "ask a question" page is the world's most effective debugger.
    </p>

    {callout("tip", "🤖 On asking an AI",
             "<p>Modern language models are genuinely good at reading tracebacks, and it is "
             "fine to use one. Two rules keep it from rotting your skill: <strong>read the "
             "error yourself first</strong> and form a hypothesis, and <strong>make it explain "
             "rather than just fix</strong>. 'Why did this happen' teaches you something; "
             "'give me the corrected code' teaches you nothing and you will meet the same bug "
             "next week. Level 6 has you build your own assistant, which makes this even more "
             "tempting, so the habit is worth forming now.</p>")}

    {exercise(1, "Diagnose without running",
              "<p>For each, name the exception type and the fix.</p>"
              + code('''# A
print("Result: " + 10)

# B
name = input("Name: ")
print(nmae)

# C
numbers = [1, 2, 3]
print(numbers[3])

# D
print(int("3.5"))''', run=False, verify="skip"),
              "<p><strong>A:</strong> <code>TypeError</code>. Use "
              "<code>f\"Result: {10}\"</code> or <code>str(10)</code>.</p>"
              "<p><strong>B:</strong> <code>NameError</code>. <code>nmae</code> is a typo for "
              "<code>name</code>.</p>"
              "<p><strong>C:</strong> <code>IndexError</code>. Three items live at 0, 1, 2. Use "
              "<code>numbers[-1]</code> for the last one.</p>"
              "<p><strong>D:</strong> <code>ValueError</code>. <code>int()</code> will not "
              "parse a decimal point in a string. Use "
              "<code>int(float(\"3.5\"))</code>, which gives 3.</p>")}

    {exercise(2, "Fix the whole program",
              "<p>Four bugs. Find them by running it and reading each error in turn, fixing "
              "one at a time. Resist the urge to fix them all at once by eye.</p>"
              + code('''crew = ["Guybrush", "Elaine", "Otis"]

print("Crew size: " + len(crew))

for i in range(4):
    print(crew[i])

if len(crew) > 2
    print("A full crew")''', run=False, verify="skip"),
              "<p>In the order Python finds them:</p>"
              "<ol><li><code>SyntaxError</code>: the <code>if</code> line has no colon. Syntax "
              "errors are found before anything runs, so this one comes first even though it "
              "is last in the file.</li>"
              "<li><code>TypeError</code>: <code>\"Crew size: \" + len(crew)</code> adds text "
              "to a number.</li>"
              "<li><code>IndexError</code>: <code>range(4)</code> reaches index 3, and there "
              "are only three crew.</li>"
              "<li>Not an error, but a design bug: hard-coding 4 instead of using "
              "<code>len(crew)</code> means adding a crew member silently breaks the "
              "program.</li></ol>"
              + code('''crew = ["Guybrush", "Elaine", "Otis"]

print(f"Crew size: {len(crew)}")

for name in crew:
    print(name)

if len(crew) > 2:
    print("A full crew")''',
                     expect="""Crew size: 3
Guybrush
Elaine
Otis
A full crew""")
              + "<p>Note the final version does not just fix the errors, it removes the "
              "possibility of two of them. <code>for name in crew</code> cannot go out of "
              "range, ever. That is the difference between fixing a bug and fixing a "
              "class of bugs.</p>")}

    {callout("info", "🎉 That is Level 1",
             "<p>You now know printing, variables, numbers, text, input, booleans, decisions, "
             "both kinds of loop, and how to read an error. That is genuinely enough to write "
             "useful programs. Take the "
             "<a href='../quiz.html'>Level 1 quiz</a>, warm up in the "
             "<a href='../pit.html'>Snake Pit</a>, then go and build "
             "<a href='../build/index.html'>the first two projects</a> before Level 2. "
             "Reading about programming and doing it are different skills, and only one of "
             "them is the job.</p>")}
""",
)
