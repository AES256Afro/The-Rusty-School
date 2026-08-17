"""The Insult Compiler: error-message swordfighting.

Monkey Island taught a generation that you win a swordfight by knowing the
right comeback, not by swinging harder. Here the insults are real Python
error messages and the ripostes are the fixes. Reading a traceback and
knowing instantly what it means is the single most useful beginner skill,
so we made it a duel.

Each round: one real error message, and three candidate fixes. The
`answer` index is the one that actually resolves it.
"""

from __future__ import annotations

import json

from .kit import SCHOOL, SITE, page

# error: the message the swordfighter reads out
# options: three candidate ripostes
# answer: index of the correct one
# explain: why it lands
INSULTS = [
    {
        "error": "TypeError: can only concatenate str (not \"int\") to str",
        "options": [
            "Convert the number to text first, or use an f-string",
            "Add more quotes around the number",
            "Restart the program; it is a fluke",
        ],
        "answer": 0,
        "explain": "You tried to add text and a number. Wrap the number in str(), or drop both "
                   "into an f-string, which converts for you.",
    },
    {
        "error": "IndentationError: expected an indented block after 'if' statement on line 3",
        "options": [
            "Add a colon to the end of line 3",
            "Indent the line under the if by four spaces",
            "Delete the if statement entirely",
        ],
        "answer": 1,
        "explain": "You wrote `if ...:` and then did not indent the body. The block under an if "
                   "must be indented, conventionally four spaces.",
    },
    {
        "error": "NameError: name 'scoer' is not defined. Did you mean: 'score'?",
        "options": [
            "Define a new variable called scoer",
            "Fix the typo: it should be score",
            "Import the scoer module",
        ],
        "answer": 1,
        "explain": "A NameError is almost always a typo. Python even suggests the fix: `scoer` "
                   "should be `score`.",
    },
    {
        "error": "ValueError: invalid literal for int() with base 10: 'twelve'",
        "options": [
            "Use a bigger number",
            "int() cannot parse a spelled-out word; pass digits like '12'",
            "Wrap it in another int()",
        ],
        "answer": 1,
        "explain": "int('twelve') fails because int() reads digits, not English. The string must "
                   "look like a number, e.g. '12'.",
    },
    {
        "error": "IndexError: list index out of range",
        "options": [
            "The index is past the end; the last valid index is len(x) - 1",
            "Lists cannot be indexed at all",
            "Add more brackets",
        ],
        "answer": 0,
        "explain": "You reached past the end of the list. Three items live at indices 0, 1, 2; "
                   "index 3 is out of range. Use x[-1] for the last item.",
    },
    {
        "error": "KeyError: 'captain'",
        "options": [
            "The dictionary has no key 'captain'; use .get('captain', default)",
            "Capitalise the key",
            "Convert the dictionary to a list",
        ],
        "answer": 0,
        "explain": "You asked a dictionary for a key it does not have. Use `.get(key, default)` "
                   "to return a fallback instead of crashing.",
    },
    {
        "error": "AttributeError: 'int' object has no attribute 'upper'",
        "options": [
            "Numbers do not have .upper(); that is a string method",
            "Import the upper module",
            "Call .UPPER() instead",
        ],
        "answer": 0,
        "explain": "`.upper()` belongs to strings. This variable is an int, which usually means "
                   "it is not the type you thought. Print type(x) to check.",
    },
    {
        "error": "SyntaxError: '(' was never closed",
        "options": [
            "Add a closing bracket, often on the line above the one named",
            "Remove all the brackets",
            "Add a semicolon",
        ],
        "answer": 0,
        "explain": "An opening bracket has no partner. The real culprit is often the line above "
                   "the one Python names. Balance the brackets.",
    },
    {
        "error": "TypeError: unsupported operand type(s) for /: 'str' and 'int'",
        "options": [
            "You are dividing text by a number; convert the text with int() or float() first",
            "Use // instead of /",
            "Divide by a string too",
        ],
        "answer": 0,
        "explain": "Division needs two numbers. One side is still a string, probably straight "
                   "from input(). Convert it before dividing.",
    },
    {
        "error": "ZeroDivisionError: division by zero",
        "options": [
            "Check the divisor is not zero before dividing",
            "Divide by a very small number instead",
            "Use * instead of /",
        ],
        "answer": 0,
        "explain": "Nothing can be divided by zero. Guard with `if divisor != 0:` or catch the "
                   "exception, especially when the divisor comes from data.",
    },
    {
        "error": "TypeError: 'NoneType' object is not subscriptable",
        "options": [
            "Something returned None where you expected a list or dict; check what it was",
            "Add [0] to fix it",
            "None can be indexed with negative numbers only",
        ],
        "answer": 0,
        "explain": "You indexed into None. Very often a function returned None (it printed "
                   "instead of returning, or a .get missed). Trace back what produced the None.",
    },
    {
        "error": "TypeError: sort() takes no positional arguments",
        "options": [
            "Pass reverse as a keyword: sort(reverse=True), not sort(True)",
            "Use sorted() with no arguments",
            "sort() cannot be called at all",
        ],
        "answer": 0,
        "explain": ".sort() wants keyword arguments like `reverse=True` or `key=...`, not a bare "
                   "positional. Name the argument.",
    },
    {
        "error": "RecursionError: maximum recursion depth exceeded",
        "options": [
            "Your recursive function has no base case, so it never stops",
            "Increase max_tokens",
            "Recursion is not allowed in Python",
        ],
        "answer": 0,
        "explain": "A recursive function that never hits a stopping condition calls itself "
                   "forever. Add a base case that returns without recursing.",
    },
    {
        "error": "ModuleNotFoundError: No module named 'requests'",
        "options": [
            "Install it into this environment: pip install requests",
            "Rename your file to requests.py",
            "Spell it Requests with a capital R",
        ],
        "answer": 0,
        "explain": "The package is not installed in the Python you are running. Activate your "
                   "venv and `python -m pip install requests`.",
    },
    {
        "error": "UnboundLocalError: cannot access local variable 'count' where it is not "
                 "associated with a value",
        "options": [
            "Assigning to count inside the function made it local; read it before assigning, or use global/return",
            "Delete the count variable",
            "count is a reserved word",
        ],
        "answer": 0,
        "explain": "Assigning to a name anywhere in a function makes it local for the whole "
                   "function. It was read before being set. Pass it in and return it instead of "
                   "reaching for a global.",
    },
    {
        "error": "TypeError: 'tuple' object does not support item assignment",
        "options": [
            "Tuples are immutable; use a list if you need to change items",
            "Use round brackets more carefully",
            "Add a comma",
        ],
        "answer": 0,
        "explain": "A tuple cannot be changed after it is made. If you need to modify items, you "
                   "wanted a list, with square brackets.",
    },
]


def build() -> str:
    data = json.dumps(INSULTS, separators=(",", ":"))

    body = f"""  <section class="lesson-header">
    <span class="kicker">The Insult Compiler</span>
    <h1>The <span class="grad">Insult Compiler</span> ⚔️</h1>
    <p class="lede muted">
      Swordfighting, the Monkey Island way: you win not by swinging harder but by knowing the
      right comeback. Here every insult is a real Python error message, and every riposte is
      the fix. Land the right one and you strike; flail and you take a hit.
    </p>
  </section>

  <div class="callout tip">
    <span class="co-title">🗡️ Why a duel?</span>
    Reading an error and knowing instantly what it means is the single most useful skill a
    beginner can have, and the thing that most separates a four-second fix from a twenty-minute
    panic. So we turned it into a fight. Win a bout to earn the Insult Duelist achievement; win
    without a single miss for Sword Master.
  </div>

  <div id="duel-root"></div>

  <div class="callout info" style="margin-top:26px">
    <span class="co-title">📖 Want the reference?</span>
    Every error type here is explained properly in
    <a href="learn/10-errors.html">Lesson 10: Reading Errors Without Fear</a>. The duel is the
    reflex training; the lesson is the understanding underneath it.
  </div>

<script>window.PY_INSULTS = {data};</script>
"""
    return page(
        path="insults.html",
        title=f"The Insult Compiler - {SCHOOL}",
        description="Error-message swordfighting: match real Python tracebacks to the fix that "
                    "resolves them.",
        body=body,
        canonical=SITE + "/python/insults",
        main_class="container narrow",
    )
