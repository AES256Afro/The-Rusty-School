"""The glossary: every term the school defines, A to Z, each linking back
to the lesson that teaches it."""

from __future__ import annotations

from .kit import SCHOOL, SITE, esc, page

NL = chr(10)

# (term, definition_html, lesson_slug, lesson_label)
TERMS = [
    ("argument", "A value you pass into a function when you call it. Different from a parameter, "
     "which is the name the function gives it.", "17-functions", "Lesson 17"),
    ("f-string", "A string prefixed with <code>f</code> whose <code>{braces}</code> are replaced "
     "by the values inside them. The one obviously correct way to build text from values.",
     "04-strings", "Lesson 4"),
    ("assert", "A statement that raises <code>AssertionError</code> if its condition is false. "
     "The simplest form of a test.", "29-testing", "Lesson 29"),
    ("async / await", "Keywords for concurrency: <code>async def</code> makes a coroutine that "
     "can pause at <code>await</code> points, letting thousands of tasks share one thread while "
     "they wait.", "40-async", "Lesson 40"),
    ("boolean", "A value that is either <code>True</code> or <code>False</code>. Named after "
     "George Boole.", "06-booleans", "Lesson 6"),
    ("bug", "A gap between what you believe your code does and what it actually does. Found by "
     "making beliefs visible and testing them.", "10-errors", "Lesson 10"),
    ("class", "A blueprint that bundles data (attributes) and the operations on it (methods) "
     "into one named type.", "31-classes", "Lesson 31"),
    ("closure", "A function that remembers variables from the scope where it was defined, even "
     "after that scope has finished. The basis of decorators.", "19-scope", "Lesson 19"),
    ("comprehension", "A one-line way to build a list, dict or set from a loop, e.g. "
     "<code>[n*n for n in range(5)]</code>.", "16-comprehensions", "Lesson 16"),
    ("context manager", "An object used with <code>with</code> that guarantees setup and "
     "cleanup happen, even if an error is raised. Files are the classic example.",
     "36-context-managers", "Lesson 36"),
    ("context window", "The maximum amount of text, measured in tokens, a language model can "
     "consider at once, including the whole conversation and its reply.", "53-how-llms-work",
     "Lesson 53"),
    ("dataclass", "A class decorated with <code>@dataclass</code> so Python writes its "
     "<code>__init__</code>, <code>__repr__</code> and <code>__eq__</code> from the field "
     "annotations.", "33-dataclasses", "Lesson 33"),
    ("decorator", "A function that wraps another function to add behaviour, applied with "
     "<code>@name</code> above a definition.", "35-decorators", "Lesson 35"),
    ("dictionary", "A collection of key-value pairs, looked up by key rather than by position. "
     "The container real programs are made of.", "13-dicts", "Lesson 13"),
    ("docstring", "A string as the first line of a function, class or module, kept by Python as "
     "its documentation and shown by <code>help()</code>.", "17-functions", "Lesson 17"),
    ("duck typing", "Caring whether an object has the method you need, not what class it is. "
     "'If it quacks like a duck.'", "32-inheritance", "Lesson 32"),
    ("embedding", "A list of numbers representing the meaning of a piece of text, so that "
     "similar meanings have similar vectors. The engine of semantic search.", "58-your-data",
     "Lesson 58"),
    ("environment variable", "A value stored outside your code, in the operating system's "
     "environment, used to keep secrets like API keys out of your files.", "54-first-api-call",
     "Lesson 54"),
    ("exception", "An error raised at runtime that stops normal flow, handled with "
     "<code>try</code> and <code>except</code>.", "22-exceptions", "Lesson 22"),
    ("float", "A number with a decimal point. Stored in binary, so tiny rounding errors are "
     "normal; use <code>Decimal</code> for money.", "03-numbers", "Lesson 3"),
    ("function", "A named, reusable block of steps. The single most important idea for keeping "
     "programs understandable.", "17-functions", "Lesson 17"),
    ("generator", "A function using <code>yield</code> that produces values lazily, one at a "
     "time, using almost no memory.", "34-generators", "Lesson 34"),
    ("GIL", "The Global Interpreter Lock: in standard CPython, only one thread runs Python "
     "bytecode at a time, so threads speed up waiting but not CPU-bound work.", "39-concurrency",
     "Lesson 39"),
    ("hallucination", "When a language model produces fluent but fabricated output. A property "
     "of predicting plausible text, not a bug that can be fully removed.", "53-how-llms-work",
     "Lesson 53"),
    ("immutable", "Unable to be changed after creation. Strings, tuples and frozen dataclasses "
     "are immutable; lists and dicts are not.", "04-strings", "Lesson 4"),
    ("indentation", "The leading spaces that define blocks in Python. Unlike most languages, the "
     "layout is the syntax. Four spaces, never tabs.", "07-decisions", "Lesson 7"),
    ("index", "The position of an item in a sequence, counting from zero. <code>x[0]</code> is "
     "the first item, <code>x[-1]</code> the last.", "04-strings", "Lesson 4"),
    ("int", "A whole number. Python integers grow to any size and never overflow.",
     "03-numbers", "Lesson 3"),
    ("interpreter", "The program that runs your Python. Standard Python is CPython; Pyodide is "
     "CPython compiled to run in a browser.", "f3-python", "Base Camp 3"),
    ("JSON", "A text format for structured data, borrowed from JavaScript, used by nearly every "
     "web API. Maps onto Python dicts and lists.", "23-data-formats", "Lesson 23"),
    ("lambda", "A tiny anonymous function of one expression, e.g. <code>lambda x: x*2</code>. "
     "For throwaway use as an argument, never assigned to a name.", "37-functional", "Lesson 37"),
    ("list", "An ordered, changeable collection. The default container in Python.", "11-lists",
     "Lesson 11"),
    ("list comprehension", "See comprehension.", "16-comprehensions", "Lesson 16"),
    ("local scope", "The region inside a function where its own variables live. Names assigned "
     "in a function are local unless declared otherwise.", "19-scope", "Lesson 19"),
    ("method", "A function that belongs to an object, called with a dot, e.g. "
     "<code>text.upper()</code>.", "04-strings", "Lesson 4"),
    ("module", "A <code>.py</code> file of code you can import. The standard library is hundreds "
     "of them.", "20-modules", "Lesson 20"),
    ("mutable", "Able to be changed in place after creation. Lists, dicts and sets are mutable; "
     "the source of the aliasing surprise.", "11-lists", "Lesson 11"),
    ("None", "Python's value for 'deliberately nothing'. Returned by functions with no "
     "<code>return</code>; compared with <code>is None</code>.", "06-booleans", "Lesson 6"),
    ("PEP 8", "Python's official style guide. Following it means any Python programmer can read "
     "your code without friction.", "30-style", "Lesson 30"),
    ("pip", "The tool that installs packages from PyPI into your environment.", "26-venv",
     "Lesson 26"),
    ("prompt injection", "An attack where text the model reads contains hidden instructions "
     "aimed at it. Unsolved, and the central risk of giving a model tools.", "62-ethics-cost",
     "Lesson 62"),
    ("property", "A method used like an attribute via <code>@property</code>, so a value can be "
     "computed on demand or validated on assignment.", "31-classes", "Lesson 31"),
    ("PyPI", "The Python Package Index: half a million public packages installable with pip.",
     "26-venv", "Lesson 26"),
    ("RAG", "Retrieval-augmented generation: find the relevant piece of your own data and paste "
     "it into the prompt so a model can answer from information it was never trained on.",
     "58-your-data", "Lesson 58"),
    ("recursion", "A function that calls itself. Needs a base case that returns without "
     "recursing, or it runs forever.", "58-your-data", "Lesson 58"),
    ("regular expression", "A tiny language for describing shapes of text, used via the "
     "<code>re</code> module for search and replace.", "25-regex", "Lesson 25"),
    ("REPL", "The interactive Python prompt (Read, Evaluate, Print, Loop). A calculator that "
     "speaks Python; the best tool for 'what does this do?'.", "f6-lab", "Base Camp 6"),
    ("return", "Hands a value back from a function to its caller. Different from print, which "
     "shows a value and returns nothing.", "17-functions", "Lesson 17"),
    ("scope", "Where a name is visible. Python searches Local, Enclosing, Global, Built-in, in "
     "that order (LEGB).", "19-scope", "Lesson 19"),
    ("secrets", "The standard module for cryptographically safe random values: tokens, "
     "passwords, keys. Never use <code>random</code> for security.", "52-security", "Lesson 52"),
    ("set", "An unordered collection with no duplicates and instant membership testing.",
     "14-sets", "Lesson 14"),
    ("shadowing (variable)", "Reusing a name with a fresh <code>let</code>-style assignment, or "
     "accidentally hiding a built-in like <code>list</code> by assigning to that name.",
     "19-scope", "Lesson 19"),
    ("slice", "A piece of a sequence, <code>x[start:stop]</code>, including the start and "
     "excluding the stop.", "04-strings", "Lesson 4"),
    ("SQL injection", "An attack where user input rewrites a database query. Prevented by "
     "parameterised queries with <code>?</code> placeholders, never f-strings.", "45-databases",
     "Lesson 45"),
    ("streaming", "Displaying a model's reply token by token as it is generated, so the wait "
     "feels alive rather than frozen.", "56-streaming", "Lesson 56"),
    ("string", "Text, written in quotes. A sequence of characters, and immutable.", "04-strings",
     "Lesson 4"),
    ("system prompt", "Standing instructions that set an assistant's persona and rules, applied "
     "to every turn, separate from the conversation.", "54-first-api-call", "Lesson 54"),
    ("temperature", "A dial controlling how randomly a model samples its next token. Low is "
     "focused and predictable; high is creative and surprising.", "53-how-llms-work",
     "Lesson 53"),
    ("token", "The chunk of text a language model reads and predicts, roughly three-quarters of "
     "a word. You pay per token.", "53-how-llms-work", "Lesson 53"),
    ("tool use", "Letting a model ask your code to run functions (function calling), so it can "
     "act: check data, do maths, control things. Powerful and risky.", "57-tools", "Lesson 57"),
    ("traceback", "The report Python prints when an exception is not caught, naming what broke, "
     "where, and why. Read it from the bottom.", "10-errors", "Lesson 10"),
    ("truthiness", "How any value is treated as True or False: empty and zero are falsy, "
     "everything else is truthy.", "06-booleans", "Lesson 6"),
    ("try / except", "The way to handle exceptions: attempt the risky code, catch the specific "
     "errors you can deal with.", "22-exceptions", "Lesson 22"),
    ("tuple", "An ordered, unchangeable collection. Documents that a fixed group of values "
     "belongs together.", "12-tuples", "Lesson 12"),
    ("type hint", "An annotation like <code>name: str</code> that documents the expected type. "
     "Not enforced at runtime, but checked by tools like mypy.", "38-typing", "Lesson 38"),
    ("unpacking", "Assigning several names from a sequence at once, e.g. "
     "<code>a, b = point</code>, or spreading with a star.", "12-tuples", "Lesson 12"),
    ("variable", "A label attached to a value, created with <code>=</code>. In Python the value "
     "has a type; the label does not.", "02-variables", "Lesson 2"),
    ("virtual environment", "A private, isolated set of installed packages for one project, so "
     "projects with conflicting versions never collide.", "26-venv", "Lesson 26"),
    ("walrus operator", "<code>:=</code>, which assigns a value and returns it in one "
     "expression, e.g. <code>if (n := len(x)) > 3:</code>.", "41-automation", "Lesson 41"),
]


def build() -> str:
    entries = []
    for term, definition, slug, label in sorted(TERMS, key=lambda t: t[0].lower()):
        entries.append(f'    <dt id="{esc(term.split()[0].lower())}">{esc(term)}</dt>')
        entries.append(f'    <dd>{definition} <a href="learn/{slug}.html">{label}</a></dd>')

    body = f"""  <section class="lesson-header">
    <span class="kicker">The glossary</span>
    <h1>Every <span class="grad">term</span>, defined 📖</h1>
    <p class="lede muted">
      {len(TERMS)} terms, A to Z, each linking back to the lesson that teaches it properly.
      Beginners revisit vocabulary constantly; this is one place to do it.
    </p>
    <input type="search" class="gloss-filter" id="gloss-filter"
      placeholder="Filter terms and definitions..." aria-label="Filter the glossary">
    <p class="muted small" id="gloss-count"></p>
  </section>

  <dl class="gloss" id="gloss-list">
{NL.join(entries)}
  </dl>
  <p class="muted" id="gloss-empty" hidden>Nothing matches that. Try a shorter search.</p>
"""
    return page(
        path="glossary.html",
        title=f"Glossary - {SCHOOL}",
        description=f"{len(TERMS)} Python terms defined, each linking to the lesson that teaches "
                    "it.",
        body=body,
        canonical=SITE + "/python/glossary",
        main_class="container narrow",
    )
