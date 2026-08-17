/* ============================================================
   Per-lesson mini-quizzes (Python)

   The sister file to the Rusty School's assets/lesson-quizzes.js, and
   it works the same way: py.js loads it on lesson pages only and
   injects the questions above the "Mark lesson complete" button, so
   none of the generated lesson pages had to change.

   Scores live in the shared rusty-quiz-best map under "lesson-<id>",
   so they sync to accounts and feed XP like every other score.

   Writing rules:
     * Test the misconception, not the vocabulary.
     * Every wrong option is something a beginner actually believes.
     * The explanation is the payload: say why the tempting wrong
       answer is wrong, not just why the right one is right.
     * Every `code` snippet is executed by tools/verify-quiz-code.py,
       and its stated answer checked against what Python really does.
   ============================================================ */
window.PY_LESSON_QUIZ = {

  /* ---------------- Base Camp ---------------- */

  "py-f1-machine": [
    {
      q: "Your program is working on some data. Where does it live while the program runs?",
      options: [
        "In memory (RAM), which is fast and forgets everything when power is lost",
        "On the disk, because that is where all data is kept",
        "Inside the CPU, which holds the program's data while it works",
        "In the operating system, which manages it on the program's behalf",
      ],
      answer: 0,
      explain:
        "Working data lives in RAM: fast, and wiped when the power goes. Disk is slow " +
        "and permanent, which is exactly why saving is a thing you must do deliberately. " +
        "The CPU holds only a tiny amount at any instant, and it is computing rather " +
        "than storing.",
    },
    {
      q: "Why do computers use binary?",
      options: [
        "Because hardware can reliably tell two states apart, and ten would be fragile",
        "Because binary arithmetic is faster than decimal arithmetic",
        "Because it uses less electricity",
        "Because early computers had only two working parts",
      ],
      answer: 0,
      explain:
        "It is an engineering answer. \"Voltage present\" versus \"voltage absent\" is " +
        "easy to distinguish reliably, even with noise and manufacturing variation. " +
        "Distinguishing ten voltage levels is possible and far more error-prone. The " +
        "maths itself is not faster in binary.",
    },
  ],

  "py-f2-programming": [
    {
      q: "What is an algorithm?",
      options: [
        "A precise sequence of steps that solves a problem",
        "A piece of Python code that performs a calculation",
        "A mathematical formula used inside a program",
        "A feature built into a programming language",
      ],
      answer: 0,
      explain:
        "An algorithm is the plan, and it exists independently of any language: a recipe " +
        "and long division are both algorithms. Code is one way to write one down. " +
        "Keeping the two separate is what lets you think about a problem before arguing " +
        "with syntax.",
    },
    {
      q: "Why do programming languages exist, rather than writing instructions the CPU understands directly?",
      options: [
        "Machine instructions are unreadable to humans, so we write something translatable instead",
        "CPUs cannot be programmed directly at all",
        "Languages make programs run faster than raw instructions",
        "Each CPU maker requires its own language",
      ],
      answer: 0,
      explain:
        "You can write machine code directly, and people did. It is agonising and " +
        "specific to one chip. A language lets you write something a human can read and " +
        "have it translated, which is also why the same Python runs on very different " +
        "hardware.",
    },
  ],

  "py-f3-python": [
    {
      q: "What does it mean that Python is \"interpreted\"?",
      options: [
        "Your code is read and executed as the program runs, without a separate build step",
        "Python code is never converted into anything else",
        "Python is slower because it re-reads the file on every line",
        "Errors can only be found by running the program",
      ],
      answer: 0,
      explain:
        "There is no separate compile step you run: you type <code>python script.py</code> " +
        "and it goes. Python does compile internally to bytecode first, so \"never " +
        "converted\" is wrong. The practical upshot is a fast edit-and-run cycle, at the " +
        "cost of some speed and of some errors only appearing when a line actually runs.",
    },
    {
      q: "Where does the name Python come from?",
      options: [
        "Monty Python's Flying Circus",
        "The snake, chosen for the logo",
        "An acronym from the original design document",
        "The Greek myth of the serpent at Delphi",
      ],
      answer: 0,
      explain:
        "Guido van Rossum named it after the comedy troupe, not the snake. The snakes " +
        "arrived later and stuck. This is why the docs are full of spam, eggs and dead " +
        "parrots, and why <code>import antigravity</code> is a real thing you can type.",
    },
  ],

  "py-f4-why-python": [
    {
      q: "Which of these is the most honest reason to pick something other than Python?",
      options: [
        "You need tight control over memory and CPU time, as in a game engine or embedded device",
        "The project is large, because Python does not scale to big codebases",
        "You need the program to be readable by other people",
        "You are working with data, which Python handles poorly",
      ],
      answer: 0,
      explain:
        "Python's costs are speed and memory control, so systems work with hard real-time " +
        "or tiny-hardware constraints is where it genuinely loses. Large codebases are " +
        "fine, especially with type hints. Readability and data work are two of its " +
        "greatest strengths, not weaknesses.",
    },
    {
      q: "Python is often called slow. What is the nuance that matters in practice?",
      options: [
        "The interpreter is slow, but heavy libraries do their work in C, so real programs are often fast",
        "It is a myth: Python is as fast as C",
        "It only matters for programs that use the internet",
        "Speed depends entirely on your computer",
      ],
      answer: 0,
      explain:
        "Pure Python loops are genuinely slow. But NumPy, pandas and friends push the " +
        "actual work into optimised C, so a well-written data program spends almost no " +
        "time in the interpreter. Knowing which of your code is which is most of " +
        "practical Python performance.",
    },
  ],

  "py-f5-terminal": [
    {
      q: "You run a command and get \"no such file or directory\", but you can see the file. Why?",
      options: [
        "You are not in the folder you think you are; the path is relative to where you stand",
        "The file is corrupted",
        "The terminal cannot see files created by other programs",
        "You need administrator permission to read it",
      ],
      answer: 0,
      explain:
        "Relative paths are interpreted from your current directory, so the same command " +
        "works in one folder and fails in another. <code>pwd</code> tells you where you " +
        "are and <code>ls</code> tells you what is there. This is the single most common " +
        "beginner terminal confusion.",
    },
    {
      q: "What does <code>cd ..</code> do?",
      options: [
        "Moves up one level, to the parent folder",
        "Moves to your home folder",
        "Moves to the previous folder you were in",
        "Lists the folders above the current one",
      ],
      answer: 0,
      explain:
        "<code>..</code> always means \"the folder that contains this one\". Home is " +
        "<code>cd ~</code> or plain <code>cd</code>, and the previous folder is " +
        "<code>cd -</code>. That same <code>..</code> is what path-traversal attacks " +
        "abuse, which comes up again when you write anything that opens files by name.",
    },
  ],

  "py-f6-lab": [
    {
      q: "What is a virtual environment for?",
      options: [
        "Giving each project its own private set of installed packages",
        "Running Python in a sandbox so it cannot damage your computer",
        "Making Python run faster for that project",
        "Letting several people work on the same project at once",
      ],
      answer: 0,
      explain:
        "Without one, every project shares one global pile of packages, and two projects " +
        "needing different versions of the same library becomes a genuinely miserable " +
        "afternoon. It is not a security sandbox, and it does not affect speed.",
    },
    {
      q: "You installed a package but Python says <code>ModuleNotFoundError</code>. What is the most likely cause?",
      options: [
        "The virtual environment is not activated, so you are using a different Python",
        "The package failed to install and printed no error",
        "You need to restart your computer",
        "The package name is case-sensitive and you typed it wrong",
      ],
      answer: 0,
      explain:
        "Activation applies to one terminal window, and forgetting it after opening a new " +
        "one is behind a large share of these. Check for the environment name in your " +
        "prompt. The runner-up cause is having installed into a different Python than the " +
        "one running your script.",
    },
  ],

  /* ---------------- Level 1 ---------------- */

  "py-01-hello": [
    {
      q: "What does this print?",
      code: 'print("2" + "2")',
      options: ["22", "4", "2 + 2", "A TypeError"],
      answer: 0,
      explain:
        "Both are strings, and <code>+</code> on strings joins them. Quotes are the whole " +
        "difference: <code>2 + 2</code> without quotes is 4. Mixing the two, " +
        "<code>\"2\" + 2</code>, is the TypeError, and it is one of the most common " +
        "beginner errors there is.",
    },
    {
      q: "What is a comment for?",
      options: [
        "Explaining why the code does something, to humans; Python ignores it entirely",
        "Describing what each line does, so the code is self-documenting",
        "Temporarily storing code you might need later",
        "Telling Python how to interpret the next line",
      ],
      answer: 0,
      explain:
        "The best comments explain <em>why</em>, because <em>what</em> is usually already " +
        "visible in the code. A comment restating the obvious is noise that will one day " +
        "contradict the code it sits above. Python ignores everything after " +
        "<code>#</code>.",
    },
  ],

  "py-02-variables": [
    {
      q: "What does this print?",
      code: "a = 5\nb = a\na = 10\nprint(b)",
      options: ["5", "10", "Nothing; b is undefined", "An error"],
      answer: 0,
      explain:
        "<code>b = a</code> copied the value 5 at that moment. Rebinding <code>a</code> " +
        "afterwards creates no link back to <code>b</code>. This intuition breaks for " +
        "lists, where two names can refer to one object, which is exactly the aliasing " +
        "trap in Lesson 11.",
    },
    {
      q: "Which name follows Python's conventions for an ordinary variable?",
      options: ["user_name", "userName", "UserName", "USERNAME"],
      answer: 0,
      explain:
        "PEP 8 says snake_case for variables and functions. <code>userName</code> is " +
        "camelCase from other languages, <code>UserName</code> is reserved by convention " +
        "for classes, and <code>USERNAME</code> signals a constant. Conventions carry " +
        "meaning, which is why following them makes code readable at a glance.",
    },
    {
      q: "What does \"dynamically typed\" mean?",
      options: [
        "A variable's type is determined by the value it currently holds and can change",
        "Python has no types at all",
        "Types are checked before the program runs",
        "You must declare a variable's type before using it",
      ],
      answer: 0,
      explain:
        "Values have types; names do not. <code>x = 5</code> then <code>x = \"five\"</code> " +
        "is perfectly legal. Python is very much typed, just not statically: " +
        "<code>\"a\" + 1</code> still fails, only at the moment it runs rather than " +
        "before.",
    },
  ],

  "py-03-numbers": [
    {
      q: "What does <code>7 // 2</code> give?",
      options: ["3", "3.5", "4", "1"],
      answer: 0,
      explain:
        "<code>//</code> is floor division: it divides and rounds down, discarding the " +
        "remainder. Plain <code>/</code> gives 3.5 and always returns a float, even for " +
        "<code>4 / 2</code>. The remainder alone is <code>%</code>, which gives 1 here.",
    },
    {
      q: "Why does <code>0.1 + 0.2 == 0.3</code> come out False?",
      options: [
        "Floats are binary approximations, and 0.1 cannot be represented exactly",
        "Python has a bug in its float handling",
        "Because == does not work on floats",
        "Because the numbers must be rounded first",
      ],
      answer: 0,
      explain:
        "In binary, 0.1 is a repeating fraction, exactly as 1/3 is in decimal. The tiny " +
        "error is real and shared by nearly every language. Compare with a tolerance " +
        "using <code>math.isclose</code>, or use <code>Decimal</code> when you are " +
        "handling money.",
    },
    {
      q: "What is <code>-7 % 3</code> in Python?",
      options: ["2", "-1", "1", "-2"],
      answer: 0,
      explain:
        "Python's modulo takes the sign of the divisor, so the result is 2, not the -1 " +
        "that C and Java give. That makes <code>%</code> reliable for wrapping around a " +
        "range even with negative numbers, and it surprises people arriving from other " +
        "languages.",
    },
  ],

  "py-04-strings": [
    {
      q: "What does this print?",
      code: 'word = "Python"\nprint(word[1:4])',
      options: ["yth", "ytho", "Pyt", "yth n"],
      answer: 0,
      explain:
        "Slicing includes the start and excludes the end, so indices 1, 2 and 3 give " +
        "\"yth\". Half-open ranges look arbitrary until you notice that " +
        "<code>len</code> of the slice is just end minus start, and that " +
        "<code>a[:n]</code> and <code>a[n:]</code> split cleanly with no overlap.",
    },
    {
      q: "What happens here?",
      code: 'name = "ada"\nname[0] = "A"',
      options: [
        "A TypeError: strings cannot be changed in place",
        "name becomes \"Ada\"",
        "Nothing; the line has no effect",
        "A SyntaxError",
      ],
      answer: 0,
      explain:
        "Strings are immutable. Every method that appears to change one actually returns " +
        "a new string, which is why <code>name.upper()</code> does nothing unless you " +
        "assign the result. Here you want <code>name = name.capitalize()</code>.",
    },
    {
      q: "Why prefer an f-string over <code>+</code> for building text?",
      options: [
        "It handles any type without conversion and reads closer to the final output",
        "It runs the code inside the braces at import time",
        "It is the only way to insert a variable into a string",
        "It automatically escapes user input",
      ],
      answer: 0,
      explain:
        "<code>f\"Age: {age}\"</code> works whether <code>age</code> is a number or a " +
        "string, while <code>\"Age: \" + age</code> raises a TypeError on a number. It " +
        "also reads like the output, which matters more than it sounds. It does no " +
        "escaping of any kind.",
    },
  ],

  "py-05-input": [
    {
      q: "What does <code>input()</code> always return?",
      options: [
        "A string, no matter what the user typed",
        "The type that best matches what was typed",
        "A number if the input looks numeric, otherwise a string",
        "Whatever type you assign it to",
      ],
      answer: 0,
      explain:
        "Always a string. This is why <code>input(\"Age: \") + 1</code> fails and why " +
        "<code>int(input(...))</code> is such a common pattern. Forgetting it produces " +
        "the classic bug where \"10\" and \"9\" compare in the wrong order, because " +
        "strings compare alphabetically.",
    },
    {
      q: "The user types \"abc\" when you call <code>int(input())</code>. What happens?",
      options: [
        "A ValueError, which you should catch with try/except",
        "int() returns 0",
        "int() returns None",
        "Python asks the user to try again",
      ],
      answer: 0,
      explain:
        "<code>int(\"abc\")</code> raises ValueError. Any program that reads from a human " +
        "must expect nonsense, so wrap the conversion in <code>try</code> and ask again " +
        "in a loop. Assuming good input is how prototypes become embarrassing.",
    },
  ],

  "py-06-booleans": [
    {
      q: "What is the difference between <code>==</code> and <code>is</code>?",
      options: [
        "== compares values; is asks whether they are the very same object",
        "They are the same, but is is faster",
        "== works on numbers and is works on everything else",
        "is compares values and == compares types",
      ],
      answer: 0,
      explain:
        "Two lists with identical contents are <code>==</code> but not <code>is</code>. " +
        "Use <code>is</code> only for <code>None</code>, <code>True</code> and " +
        "<code>False</code>. Small integers and short strings are sometimes cached, which " +
        "makes <code>is</code> appear to work on them and then fail mysteriously later.",
    },
    {
      q: "Which of these is truthy?",
      options: ['"False"', "0", "[]", "None"],
      answer: 0,
      explain:
        "Any non-empty string is truthy, including the string \"False\", which catches " +
        "people reading values from files or forms. Empty containers, zero and " +
        "<code>None</code> are all falsy. This is why " +
        "<code>if user_input == \"true\"</code> needs care.",
    },
    {
      q: "What does <code>and</code> actually return?",
      options: [
        "One of its operands, not necessarily True or False",
        "Always True or False",
        "The second operand, always",
        "An error if the operands are not booleans",
      ],
      answer: 0,
      explain:
        "<code>\"a\" and \"b\"</code> is <code>\"b\"</code>, and <code>0 and \"b\"</code> " +
        "is <code>0</code>. It short-circuits and returns the operand that decided the " +
        "outcome. That is what makes <code>name = given or \"anonymous\"</code> a common " +
        "idiom for defaults.",
    },
  ],

  "py-07-decisions": [
    {
      q: "Why does indentation matter in Python?",
      options: [
        "It is the syntax for grouping statements; other languages use braces",
        "It is a style convention the linter enforces",
        "It only matters inside functions",
        "It makes the code easier to read but has no effect",
      ],
      answer: 0,
      explain:
        "Indentation <em>is</em> the block structure. Get it wrong and you get an " +
        "IndentationError, or worse, code that runs with the wrong meaning, such as a " +
        "line that was supposed to be inside a loop running once at the end. Mixing tabs " +
        "and spaces is the classic way to produce a file that looks right and is not.",
    },
    {
      q: "What is the difference between several <code>if</code> statements and <code>if/elif</code>?",
      options: [
        "elif is only checked when earlier conditions failed; separate ifs are all checked",
        "They behave identically",
        "elif can only be used once per if",
        "Separate ifs run faster",
      ],
      answer: 0,
      explain:
        "With <code>elif</code>, at most one branch runs. With separate " +
        "<code>if</code>s, several can run, which produces bugs when the branches " +
        "overlap: reassigning a value in one and then having the next also match. Use " +
        "<code>elif</code> when the cases are alternatives.",
    },
  ],

  "py-08-while": [
    {
      q: "What is the most common cause of an infinite <code>while</code> loop?",
      options: [
        "The condition never becomes false because nothing inside changes it",
        "Forgetting the colon at the end of the line",
        "Using a comparison instead of an assignment",
        "Looping over a collection that keeps growing",
      ],
      answer: 0,
      explain:
        "You are responsible for progress toward the exit, and forgetting to update the " +
        "variable in the condition is the classic slip. Ctrl-C stops a runaway. This is " +
        "exactly the risk <code>for</code> removes by taking an iterator that runs out on " +
        "its own.",
    },
    {
      q: "What is the difference between <code>break</code> and <code>continue</code>?",
      options: [
        "break leaves the loop entirely; continue skips to the next iteration",
        "break stops the program; continue stops the loop",
        "They are the same, but break also returns a value",
        "continue leaves the loop and break skips one iteration",
      ],
      answer: 0,
      explain:
        "<code>break</code> exits; <code>continue</code> jumps back to the top for the " +
        "next round. A useful trap to know: <code>continue</code> in a " +
        "<code>while</code> loop skips the rest of the body, including any line that was " +
        "supposed to advance the counter, which turns it into an infinite loop.",
    },
  ],

  "py-09-for": [
    {
      q: "What does <code>range(1, 5)</code> produce?",
      options: ["1, 2, 3, 4", "1, 2, 3, 4, 5", "0, 1, 2, 3, 4", "1, 5"],
      answer: 0,
      explain:
        "Start included, stop excluded, exactly like slicing. <code>range(5)</code> alone " +
        "gives 0 to 4, which is why it pairs naturally with list indices. The consistency " +
        "of half-open ranges across the language is deliberate.",
    },
    {
      q: "You need both the position and the value while looping. What is the Pythonic way?",
      options: [
        "for i, item in enumerate(items):",
        "for i in range(len(items)):",
        "Keep a counter variable and increment it",
        "for item in items.with_index():",
      ],
      answer: 0,
      explain:
        "<code>enumerate</code> gives both and reads cleanly. The " +
        "<code>range(len(...))</code> version works but is noisier and invites off-by-one " +
        "mistakes, and it is the single most common thing experienced Python programmers " +
        "flag in beginner code.",
    },
  ],

  "py-10-errors": [
    {
      q: "Which end of a traceback should you read first?",
      options: [
        "The bottom, where the error type and message are",
        "The top, where the program started",
        "The middle, where your own code appears",
        "It does not matter; the whole thing says the same thing",
      ],
      answer: 0,
      explain:
        "The last line names the exception and explains it. The lines above are the call " +
        "chain that led there, most recent last. Read the bottom line, then scan upward " +
        "for the topmost frame that is your file rather than a library.",
    },
    {
      q: "You get <code>NameError: name 'scoer' is not defined</code>. What is the cause?",
      options: [
        "A typo: you used a name you never assigned",
        "You used a variable before importing it",
        "The variable is out of scope",
        "You assigned it inside an if that did not run",
      ],
      answer: 0,
      explain:
        "Nine times out of ten it is a typo, and Python often suggests the closest real " +
        "name. The other cases are real but rarer: assigning inside a branch that never " +
        "ran produces the same error and is worth knowing about when the spelling is " +
        "definitely right.",
    },
    {
      q: "What does <code>IndexError: list index out of range</code> mean?",
      options: [
        "You asked for a position that does not exist in the sequence",
        "The list is empty",
        "The index was a string rather than a number",
        "You tried to modify a list while looping over it",
      ],
      answer: 0,
      explain:
        "The position is outside the list. An empty list is one way to get there, but so " +
        "is the classic <code>items[len(items)]</code>, since valid indices stop one " +
        "before the length. A string index would be a TypeError instead.",
    },
  ],

  /* ---------------- Level 2 ---------------- */

  "py-11-lists": [
    {
      q: "What does this print?",
      code: "a = [1, 2, 3]\nb = a\nb.append(4)\nprint(a)",
      options: ["[1, 2, 3, 4]", "[1, 2, 3]", "[4]", "A TypeError"],
      answer: 0,
      explain:
        "This is the aliasing trap. <code>b = a</code> makes a second name for the same " +
        "list, not a copy, so appending through either name changes the one object. Use " +
        "<code>b = a.copy()</code> or <code>b = a[:]</code> when you want an independent " +
        "list. Numbers behave differently only because they are immutable.",
    },
    {
      q: "What does <code>items[-1]</code> give you?",
      options: [
        "The last element",
        "An IndexError",
        "The element before the first, wrapping around",
        "The list in reverse",
      ],
      answer: 0,
      explain:
        "Negative indices count from the end, so -1 is last and -2 second to last. It " +
        "saves the noisy <code>items[len(items) - 1]</code>. The same works in slices: " +
        "<code>items[:-1]</code> is everything but the last element.",
    },
    {
      q: "Why is modifying a list while looping over it a bad idea?",
      options: [
        "The loop tracks positions, so removing items makes it skip elements",
        "Python raises an error immediately",
        "The list becomes read-only during the loop",
        "It is fine as long as you only append",
      ],
      answer: 0,
      explain:
        "Removing an item shifts everything down while the loop's index moves up, so " +
        "elements get skipped silently, which is worse than an error. Build a new list " +
        "with a comprehension instead, or iterate over a copy with " +
        "<code>for x in items[:]</code>.",
    },
  ],

  "py-12-tuples": [
    {
      q: "What is the main practical difference between a tuple and a list?",
      options: [
        "A tuple cannot be changed after creation",
        "A tuple can only hold two items",
        "A tuple must hold items of the same type",
        "A tuple cannot be looped over",
      ],
      answer: 0,
      explain:
        "Immutability is the difference, and it is why tuples can be dictionary keys " +
        "while lists cannot. The convention that follows is that tuples suit fixed " +
        "records where position has meaning, like a coordinate, and lists suit " +
        "collections of similar things.",
    },
    {
      q: "What does this print?",
      code: "def stats():\n    return 1, 2, 3\n\nlow, mid, high = stats()\nprint(high)",
      options: ["3", "(1, 2, 3)", "1", "A TypeError"],
      answer: 0,
      explain:
        "Returning several values actually returns one tuple, and unpacking pulls it " +
        "apart by position. This is why swapping is just <code>a, b = b, a</code>. If " +
        "the counts do not match you get a ValueError about unpacking.",
    },
  ],

  "py-13-dicts": [
    {
      q: "What is the difference between <code>d[\"key\"]</code> and <code>d.get(\"key\")</code>?",
      options: [
        "Indexing raises KeyError if missing; get returns None instead",
        "get is faster because it does not check",
        "They are identical",
        "get only works on string keys",
      ],
      answer: 0,
      explain:
        "The difference is what happens when the key is absent. Use indexing when a " +
        "missing key means a bug you want to hear about, and <code>get</code> (optionally " +
        "with a default, as in <code>d.get(\"k\", 0)</code>) when absence is expected.",
    },
    {
      q: "Which of these cannot be a dictionary key?",
      options: ["A list", "A tuple", "A string", "A number"],
      answer: 0,
      explain:
        "Keys must be hashable, which in practice means immutable. A list can change, so " +
        "its hash would change and the dictionary could never find it again. A tuple of " +
        "immutable things is fine, which is why coordinates make good keys.",
    },
    {
      q: "You need to count how many times each word appears. What is the cleanest approach?",
      options: [
        "collections.Counter, or a dict with .get(word, 0) + 1",
        "A list of pairs you search each time",
        "Two parallel lists, one of words and one of counts",
        "Sort the words and count runs manually",
      ],
      answer: 0,
      explain:
        "<code>Counter</code> exists precisely for this and gives you " +
        "<code>most_common()</code> for free. The <code>.get(word, 0) + 1</code> pattern " +
        "is the same idea by hand. Parallel lists are the classic beginner approach and " +
        "go wrong the moment the two drift out of step.",
    },
  ],

  "py-14-sets": [
    {
      q: "What is the fastest way to remove duplicates from a list?",
      options: [
        "list(set(items)), accepting that order is lost",
        "Loop and check with `in` against a new list",
        "Sort it and delete neighbours that match",
        "items.deduplicate()",
      ],
      answer: 0,
      explain:
        "Converting to a set and back is one expression and very fast. The cost is order, " +
        "so when order matters use <code>list(dict.fromkeys(items))</code>, which " +
        "preserves first appearance because dictionaries keep insertion order.",
    },
    {
      q: "Why is <code>x in big_set</code> so much faster than <code>x in big_list</code>?",
      options: [
        "A set hashes the value and jumps straight to it; a list checks each element",
        "Sets are stored in faster memory",
        "Lists must be sorted before searching",
        "Sets are smaller, so there is less to search",
      ],
      answer: 0,
      explain:
        "Set membership is roughly constant time regardless of size, while a list scan " +
        "grows with length. Swapping a list for a set in a membership check is one of the " +
        "few optimisations that is both trivial and occasionally enormous.",
    },
  ],

  "py-15-nested": [
    {
      q: "You have a list of dictionaries and want every name. What is the cleanest way?",
      options: [
        "[person[\"name\"] for person in people]",
        "A for loop that appends to a new list",
        "people.get(\"name\")",
        "map(people, \"name\")",
      ],
      answer: 0,
      explain:
        "A comprehension says what you want rather than how to accumulate it, and this " +
        "shape (list of records, pull one field) is the single most common one in real " +
        "Python. The loop is fine and just longer; the other two are not real.",
    },
    {
      q: "How do you safely read <code>data[\"user\"][\"address\"][\"city\"]</code> when parts may be missing?",
      options: [
        "Chain .get() with sensible defaults, or catch KeyError around the whole access",
        "Use a try/except around each individual key",
        "Check `if data` before accessing",
        "Use data.get(\"user.address.city\")",
      ],
      answer: 0,
      explain:
        "<code>data.get(\"user\", {}).get(\"address\", {}).get(\"city\")</code> " +
        "degrades to <code>None</code> rather than exploding. Catching " +
        "<code>KeyError</code> around the whole expression is equally valid and often " +
        "clearer. Dotted-string lookup is not a thing in plain Python.",
    },
  ],

  "py-16-comprehensions": [
    {
      q: "What does this produce?",
      code: "print([n * 2 for n in range(5) if n % 2 == 0])",
      options: ["[0, 4, 8]", "[0, 2, 4, 6, 8]", "[2, 6, 10]", "[0, 4, 8, 12, 16]"],
      answer: 0,
      explain:
        "The filter runs first, keeping 0, 2 and 4, then each is doubled to give 0, 4 and " +
        "8. Reading a comprehension in that order, source then condition then " +
        "transformation, makes them much easier to parse than reading left to right.",
    },
    {
      q: "When should you NOT use a comprehension?",
      options: [
        "When it needs several conditions or nesting and stops being readable",
        "When the result is a dictionary",
        "When the source is a file",
        "When you need more than ten items",
      ],
      answer: 0,
      explain:
        "Comprehensions are for expressing a transformation clearly. Once one carries two " +
        "nested loops and a couple of conditions, an ordinary loop is kinder to whoever " +
        "reads it next. Cleverness that needs re-reading is not a saving.",
    },
  ],

  "py-17-functions": [
    {
      q: "What does a function return if it has no <code>return</code> statement?",
      options: ["None", "0", "The last value it computed", "Nothing at all; it errors"],
      answer: 0,
      explain:
        "Every function returns something, and with no <code>return</code> that something " +
        "is <code>None</code>. This is behind the classic bug where " +
        "<code>result = my_list.sort()</code> leaves <code>result</code> as " +
        "<code>None</code>, because <code>sort</code> sorts in place and returns nothing.",
    },
    {
      q: "What is the main reason to write a function?",
      options: [
        "To name a process, so it can be understood, tested and reused",
        "To make the program run faster",
        "Because long files are not allowed",
        "To avoid using loops",
      ],
      answer: 0,
      explain:
        "Naming is the underrated part. A well-named function turns five lines of \"what " +
        "is this doing\" into one line that says it. Reuse is a bonus; a function used " +
        "exactly once can still be entirely worth extracting.",
    },
  ],

  "py-18-arguments": [
    {
      q: "What does this print?",
      code: "def add(item, basket=[]):\n    basket.append(item)\n    return basket\n\nprint(add(1))\nprint(add(2))",
      options: ["[1] then [1, 2]", "[1] then [2]", "[1, 2] then [1, 2]", "A TypeError"],
      answer: 0,
      explain:
        "The mutable default trap, and one of Python's genuinely surprising corners. The " +
        "default list is created once when the function is defined, not per call, so it " +
        "accumulates. The fix is <code>basket=None</code> and " +
        "<code>if basket is None: basket = []</code> inside.",
    },
    {
      q: "What does <code>**kwargs</code> collect?",
      options: [
        "Any extra keyword arguments, as a dictionary",
        "Any extra positional arguments, as a tuple",
        "All arguments, in the order given",
        "Only arguments with default values",
      ],
      answer: 0,
      explain:
        "<code>*args</code> gathers extra positional arguments into a tuple; " +
        "<code>**kwargs</code> gathers extra keyword ones into a dict. The stars are the " +
        "syntax, not the names, so <code>*a, **kw</code> works identically. They are " +
        "mostly for wrappers that pass arguments straight through.",
    },
  ],

  "py-19-scope": [
    {
      q: "What does this print?",
      code: "count = 0\n\ndef bump():\n    count = 10\n\nbump()\nprint(count)",
      options: ["0", "10", "None", "An UnboundLocalError"],
      answer: 0,
      explain:
        "Assigning inside a function creates a new local name that shadows the global one, " +
        "so the global is untouched. Reading a global works without ceremony; writing one " +
        "needs the <code>global</code> keyword, which is usually a sign the code would be " +
        "better returning a value instead.",
    },
    {
      q: "What does the LEGB rule describe?",
      options: [
        "The order Python searches for a name: Local, Enclosing, Global, Built-in",
        "The order in which functions are defined",
        "The four kinds of variable a program may have",
        "How imports are resolved between modules",
      ],
      answer: 0,
      explain:
        "Python looks in the local scope first, then any enclosing function, then module " +
        "level, then the built-ins. It explains why naming a variable <code>list</code> " +
        "quietly breaks <code>list()</code> for the rest of that scope: yours is found " +
        "first.",
    },
  ],

  "py-20-modules": [
    {
      q: "What does <code>if __name__ == \"__main__\":</code> do?",
      options: [
        "Runs the block only when the file is executed directly, not when imported",
        "Marks the entry point Python requires in every file",
        "Prevents the module from being imported twice",
        "Defines the function to run first",
      ],
      answer: 0,
      explain:
        "Without it, importing a module runs its demo code as a side effect, which is " +
        "surprising and occasionally destructive. With it, the file works both as a " +
        "script and as an importable library, which is why nearly every real Python file " +
        "has one.",
    },
    {
      q: "Why is <code>from module import *</code> discouraged?",
      options: [
        "It hides where names came from and can silently overwrite existing ones",
        "It is much slower than a normal import",
        "It only works at the top of a file",
        "It fails if the module has more than a few names",
      ],
      answer: 0,
      explain:
        "You lose the ability to tell at a glance where a name is from, and two star " +
        "imports can quietly clobber each other, producing a bug that depends on import " +
        "order. Import the module, or import the specific names you want.",
    },
  ],

  /* ---------------- Level 3 ---------------- */

  "py-21-files": [
    {
      q: "Why use <code>with open(...) as f:</code> rather than <code>f = open(...)</code>?",
      options: [
        "It closes the file automatically, even if an exception is raised",
        "It is faster because it buffers differently",
        "It is the only way to read a file line by line",
        "It locks the file so nothing else can modify it",
      ],
      answer: 0,
      explain:
        "The guarantee is cleanup on the way out, however you leave. Files left open can " +
        "hold buffered writes that never reach disk, and on a long-running program you " +
        "eventually run out of file handles. This is the context manager pattern from " +
        "Lesson 36.",
    },
    {
      q: "You open a file and get a UnicodeDecodeError. What is the likely cause?",
      options: [
        "The file is not in the encoding Python assumed, or is binary",
        "The file is corrupted",
        "The file is too large to read at once",
        "You need administrator permission",
      ],
      answer: 0,
      explain:
        "Python assumes a text encoding, usually UTF-8, and a file saved as something " +
        "else, or a binary file like an image, will not decode. Pass " +
        "<code>encoding=</code> explicitly when you know it, and open binary files with " +
        "<code>\"rb\"</code>.",
    },
  ],

  "py-22-exceptions": [
    {
      q: "Why is a bare <code>except:</code> a bad habit?",
      options: [
        "It catches everything, including Ctrl-C and genuine bugs, and hides them",
        "It is slower than catching a specific exception",
        "It only works at the top level of a program",
        "It cannot be combined with finally",
      ],
      answer: 0,
      explain:
        "It swallows KeyboardInterrupt, SystemExit and the typo in your own code, turning " +
        "a clear crash into mysterious silence. Catch what you can actually handle. " +
        "<code>except Exception:</code> is at least narrower, and even that deserves a " +
        "reason.",
    },
    {
      q: "What is the <code>else</code> clause of a try block for?",
      options: [
        "Code that should run only if no exception was raised",
        "Code that runs if the exception was not caught",
        "An alternative to except for simple cases",
        "Code that runs whether or not there was an exception",
      ],
      answer: 0,
      explain:
        "It keeps the <code>try</code> block down to only the line that might fail, so " +
        "you do not accidentally catch an exception from the follow-up code. " +
        "<code>finally</code> is the one that always runs.",
    },
    {
      q: "When should you catch an exception rather than let it propagate?",
      options: [
        "When you can actually do something useful about it at that level",
        "Whenever one might occur, to keep the program running",
        "Only at the very top of the program",
        "Never; exceptions should always crash the program",
      ],
      answer: 0,
      explain:
        "Catching without a plan produces programs that limp on in a broken state, which " +
        "is harder to debug than a clean crash. If this layer cannot retry, substitute a " +
        "default or explain it to the user, let it rise to one that can.",
    },
  ],

  "py-23-data-formats": [
    {
      q: "Why use the <code>csv</code> module instead of splitting lines on commas?",
      options: [
        "It handles quoted fields containing commas and newlines correctly",
        "It is faster on large files",
        "It automatically converts numbers to int and float",
        "Splitting on commas does not work at all",
      ],
      answer: 0,
      explain:
        "A field like <code>\"Smith, John\"</code> contains a comma inside quotes, and " +
        "naive splitting mangles it. Quoting rules are fiddly enough that hand-rolling " +
        "them is a reliable source of bugs. Note the module gives you strings, so " +
        "conversion is still your job.",
    },
    {
      q: "What does <code>json.dumps()</code> do?",
      options: [
        "Turns a Python object into a JSON string",
        "Reads a JSON string into a Python object",
        "Writes JSON directly to a file",
        "Checks whether a string is valid JSON",
      ],
      answer: 0,
      explain:
        "The <code>s</code> means string. <code>dumps</code> serialises to a string and " +
        "<code>loads</code> parses from one; <code>dump</code> and <code>load</code> " +
        "without the s work on files. Everyone mixes these up at least once.",
    },
  ],

  "py-24-dates": [
    {
      q: "Why is a \"naive\" datetime risky?",
      options: [
        "It has no time zone, so comparing or storing it can be silently wrong",
        "It cannot be formatted as a string",
        "It only works for dates after 1970",
        "It cannot be compared to another datetime",
      ],
      answer: 0,
      explain:
        "Without a time zone there is no way to know what instant it refers to, so two " +
        "naive datetimes from different places are not comparable. Store UTC, attach a " +
        "time zone, and convert only for display.",
    },
    {
      q: "What is the ISO 8601 format good for?",
      options: [
        "Unambiguous storage and sorting, because text order matches time order",
        "Being the friendliest format to show users",
        "Storing dates in the smallest number of bytes",
        "Handling time zones automatically",
      ],
      answer: 0,
      explain:
        "<code>2026-08-17</code> sorts correctly as plain text and cannot be misread the " +
        "way <code>08/09/2026</code> can, where half the world reads a different month. " +
        "Store ISO, display something friendlier.",
    },
  ],

  "py-25-regex": [
    {
      q: "Why use a raw string like <code>r\"\\d+\"</code> for patterns?",
      options: [
        "So backslashes reach the regex engine instead of being eaten by Python",
        "It makes matching faster",
        "It is required syntax for the re module",
        "It makes the pattern case-insensitive",
      ],
      answer: 0,
      explain:
        "Without the <code>r</code>, Python processes the backslash first and the regex " +
        "engine may never see it, which is why patterns mysteriously fail. Using raw " +
        "strings for every pattern removes an entire category of confusion.",
    },
    {
      q: "When is a regular expression the wrong tool?",
      options: [
        "For nested structures like HTML or JSON, which need a real parser",
        "For finding a fixed word in a string",
        "For validating simple formats",
        "For splitting on multiple separators",
      ],
      answer: 0,
      explain:
        "Regexes cannot handle arbitrary nesting, so HTML and JSON need real parsers. " +
        "They are also overkill for a fixed substring, where <code>in</code> is clearer " +
        "and faster. Reach for them for genuinely pattern-shaped text problems.",
    },
  ],

  "py-26-venv": [
    {
      q: "What does <code>pip freeze > requirements.txt</code> record?",
      options: [
        "Exact versions of everything currently installed, so the setup can be reproduced",
        "The packages your code imports",
        "The packages available on PyPI",
        "Which packages need updating",
      ],
      answer: 0,
      explain:
        "It records what is installed, exact versions and all, which is what makes a " +
        "build reproducible. Note it captures everything in the environment rather than " +
        "just your direct dependencies, which is why per-project environments matter so " +
        "much.",
    },
    {
      q: "You activate a virtual environment. What actually changed?",
      options: [
        "Your PATH now finds that environment's python and pip first",
        "Python was reinstalled inside the project folder",
        "Your global packages were hidden from the operating system",
        "A background process started managing your packages",
      ],
      answer: 0,
      explain:
        "Activation is mostly a PATH change, which is why it applies to one terminal " +
        "session and vanishes when you open a new one. Knowing that makes the whole thing " +
        "far less mysterious, and explains why " +
        "<code>which python</code> is such a useful diagnostic.",
    },
  ],

  "py-27-cli": [
    {
      q: "Why prefer <code>argparse</code> over reading <code>sys.argv</code> yourself?",
      options: [
        "You get --help, validation and error messages for a few lines of setup",
        "sys.argv does not include the arguments",
        "argparse is faster to start up",
        "sys.argv only works on Linux",
      ],
      answer: 0,
      explain:
        "Everything a command-line tool is expected to do, usage text, type conversion, " +
        "required arguments, sensible errors, comes nearly free. Hand-parsing " +
        "<code>sys.argv</code> works for one positional argument and gets unpleasant " +
        "immediately after.",
    },
    {
      q: "What should a command-line program return when it fails?",
      options: [
        "A non-zero exit code, so other tools can tell it failed",
        "Zero, as long as it printed an error message",
        "Nothing; exit codes are for compiled programs",
        "The number of errors encountered",
      ],
      answer: 0,
      explain:
        "Zero means success and anything else means failure. Scripts and CI pipelines " +
        "branch on this, so a program that prints \"error\" and exits zero will be " +
        "treated as having worked. Use <code>sys.exit(1)</code>.",
    },
  ],

  "py-28-debugging": [
    {
      q: "Why prefer the <code>logging</code> module over <code>print</code> for a real program?",
      options: [
        "Levels, timestamps and destinations can be changed without editing the code",
        "print is too slow for production",
        "logging output cannot be accidentally committed",
        "print does not work when a program runs in the background",
      ],
      answer: 0,
      explain:
        "You can dial the verbosity from a config, route output to a file, and get " +
        "timestamps and module names for free, all without touching the call sites. " +
        "<code>print</code> is completely fine while you are actively poking at " +
        "something.",
    },
    {
      q: "What is the most reliable first step when hunting a bug?",
      options: [
        "Reproduce it consistently, so you can tell when it is fixed",
        "Read the code carefully until you spot the mistake",
        "Add print statements everywhere",
        "Rewrite the suspicious function",
      ],
      answer: 0,
      explain:
        "Without a reliable reproduction you cannot tell a fix from a coincidence, and " +
        "intermittent bugs \"go away\" constantly. Reproduce, narrow to the smallest " +
        "case, then look. Reading and printing come after, and rewriting first is how you " +
        "get two bugs.",
    },
  ],

  "py-29-testing": [
    {
      q: "What makes a good test?",
      options: [
        "It fails when the behaviour breaks and passes otherwise, testing behaviour not implementation",
        "It covers as many lines as possible",
        "It tests every function in the file",
        "It runs quickly, whatever it checks",
      ],
      answer: 0,
      explain:
        "A test's value is the failure it will one day give you. Tests tied to internals " +
        "break every time you refactor without catching real bugs, which trains people to " +
        "ignore them. Coverage is a weak proxy: it measures lines run, not anything " +
        "checked.",
    },
    {
      q: "Your test passes whether or not the code is correct. What is it worth?",
      options: [
        "Nothing, and worse than nothing: it gives false confidence",
        "It still documents the intended behaviour",
        "It is fine as long as other tests are stronger",
        "It is useful for measuring coverage",
      ],
      answer: 0,
      explain:
        "A test that cannot fail is a liability, because it looks like protection. This is " +
        "why writing the test first is such a good habit: you watch it fail, so you know " +
        "it is capable of failing.",
    },
  ],

  "py-30-style": [
    {
      q: "What do type hints actually do at runtime?",
      options: [
        "Nothing; they are for humans and tools like mypy",
        "They enforce the type and raise a TypeError on mismatch",
        "They convert values to the declared type",
        "They make the code run faster",
      ],
      answer: 0,
      explain:
        "Python does not check them when running, which surprises people arriving from " +
        "typed languages. Their value is that mypy can check them before you run, and " +
        "that they document intent in a way that cannot drift silently the way a comment " +
        "can.",
    },
    {
      q: "Why let a formatter like black or ruff decide your layout?",
      options: [
        "It ends style arguments, so review time goes to logic instead",
        "Formatted code runs faster",
        "It is required by PEP 8",
        "It catches bugs that linters miss",
      ],
      answer: 0,
      explain:
        "The win is social. When a tool decides, nobody spends review comments on line " +
        "breaks, and every file in the project looks the same. Formatting has no effect " +
        "on behaviour, and finding bugs is the linter's job, not the formatter's.",
    },
  ],

  /* ---------------- Level 4 ---------------- */

  "py-31-classes": [
    {
      q: "What is <code>self</code>?",
      options: [
        "The particular instance the method was called on, passed automatically",
        "A keyword that refers to the class itself",
        "A required name that Python treats specially",
        "A reference to the parent class",
      ],
      answer: 0,
      explain:
        "Python passes the instance as the first argument, and <code>self</code> is just " +
        "the conventional name for it: you could call it anything and it would work. The " +
        "class itself is <code>cls</code> in classmethods, and the parent is " +
        "<code>super()</code>.",
    },
    {
      q: "What is the difference between a class attribute and an instance attribute?",
      options: [
        "A class attribute is shared by every instance; an instance attribute belongs to one",
        "Class attributes are constants and instance attributes can change",
        "Class attributes are private and instance attributes are public",
        "They are the same, written differently",
      ],
      answer: 0,
      explain:
        "One lives on the class and is shared; the other is created per instance, usually " +
        "in <code>__init__</code>. A mutable class attribute, such as a list, is the same " +
        "trap as a mutable default argument: every instance appends to the one object.",
    },
    {
      q: "When is a class the wrong tool?",
      options: [
        "When it has one method and no state, where a function is clearer",
        "When you have fewer than three attributes",
        "When the program is a script rather than a library",
        "When you are not using inheritance",
      ],
      answer: 0,
      explain:
        "A class exists to bundle state with the behaviour that acts on it. With no state " +
        "to hold, you have written a function with extra ceremony. Classes with a single " +
        "method called once are a common way of making simple code look complicated.",
    },
  ],

  "py-32-inheritance": [
    {
      q: "What does <code>super().__init__()</code> do?",
      options: [
        "Runs the parent class's initialiser, so its setup work happens too",
        "Creates a new instance of the parent class",
        "Copies the parent's attributes into this instance",
        "Declares which class to inherit from",
      ],
      answer: 0,
      explain:
        "It calls up the chain so the parent can do its own setup. Skip it and attributes " +
        "the parent expected to exist simply will not, producing an AttributeError " +
        "somewhere far away and much later.",
    },
    {
      q: "Why is composition usually preferred over inheritance?",
      options: [
        "It couples classes loosely, and deep hierarchies get rigid and hard to change",
        "Inheritance is slower at runtime",
        "Python's inheritance is unreliable with more than one parent",
        "Composition requires less code",
      ],
      answer: 0,
      explain:
        "Inheritance says \"is a\" and drags the whole parent along, including parts you " +
        "did not want. Holding an object and delegating to it says \"has a\", and is far " +
        "easier to rearrange later. Inheritance is a genuine tool, just an overused one.",
    },
    {
      q: "What does <code>__repr__</code> exist for?",
      options: [
        "An unambiguous representation aimed at developers, shown in the REPL and debuggers",
        "The friendly text shown to end users",
        "Converting the object to a dictionary",
        "Comparing two objects for equality",
      ],
      answer: 0,
      explain:
        "<code>__repr__</code> is for you, ideally something that shows the object's real " +
        "state. <code>__str__</code> is the friendly one, and falls back to " +
        "<code>__repr__</code> when absent. Writing a good <code>__repr__</code> pays for " +
        "itself the first time you debug a list of your objects.",
    },
  ],

  "py-33-dataclasses": [
    {
      q: "What does <code>@dataclass</code> generate for you?",
      options: [
        "__init__, __repr__ and __eq__ from the annotated fields",
        "Getters and setters for every attribute",
        "A class that cannot be modified",
        "Type checking on assignment",
      ],
      answer: 0,
      explain:
        "It writes the boilerplate you would have typed. Immutability is " +
        "<code>frozen=True</code> and is opt-in, and the type annotations are still hints " +
        "only: nothing checks them at runtime, exactly as everywhere else in Python.",
    },
    {
      q: "Why use an <code>Enum</code> instead of plain strings for a set of states?",
      options: [
        "A typo becomes an error instead of a silently invalid value",
        "Enums use less memory than strings",
        "Strings cannot be compared reliably",
        "Enums are required for match statements",
      ],
      answer: 0,
      explain:
        "<code>Status.ACTIVE</code> fails loudly if you misspell it; " +
        "<code>\"activ\"</code> sails through and produces a bug somewhere else entirely. " +
        "You also get a single place listing every legal value, which is worth a lot when " +
        "someone new reads the code.",
    },
  ],

  "py-34-generators": [
    {
      q: "What does a function containing <code>yield</code> return when you call it?",
      options: [
        "A generator object; none of the body has run yet",
        "The first yielded value",
        "A list of all the yielded values",
        "None, until you iterate it",
      ],
      answer: 0,
      explain:
        "Calling it runs nothing at all. You get a generator, and the body advances only " +
        "as you iterate. This is why a generator function with a print at the top appears " +
        "silent until you loop over the result, which surprises people the first time.",
    },
    {
      q: "What is the main practical reason to use a generator?",
      options: [
        "It produces values one at a time, so memory does not grow with the sequence",
        "It is faster than a list in every case",
        "It can be iterated many times",
        "It automatically removes duplicates",
      ],
      answer: 0,
      explain:
        "Memory. Reading a ten-gigabyte file line by line is fine; building a list of " +
        "every line is not. The cost is that a generator is consumed once: iterate it " +
        "twice and the second pass sees nothing, which is a classic source of confusion.",
    },
  ],

  "py-35-decorators": [
    {
      q: "What is a decorator, mechanically?",
      options: [
        "A function that takes a function and returns a replacement for it",
        "A special comment that changes how Python compiles the function",
        "A class that wraps another class",
        "A way to add type checking to a function",
      ],
      answer: 0,
      explain:
        "<code>@thing</code> above <code>def f</code> is exactly " +
        "<code>f = thing(f)</code>. Once that clicks, decorators stop being magic: they " +
        "are ordinary functions taking and returning functions, which is possible because " +
        "functions are objects.",
    },
    {
      q: "Why use <code>functools.wraps</code> inside a decorator?",
      options: [
        "It preserves the wrapped function's name and docstring, which would otherwise be lost",
        "It makes the decorator run faster",
        "It allows the decorator to take arguments",
        "It is required for the decorator to work at all",
      ],
      answer: 0,
      explain:
        "Without it, every decorated function reports itself as <code>wrapper</code> with " +
        "no docstring, which breaks help text, debugging and anything that introspects. " +
        "One line, and it saves a genuinely baffling afternoon.",
    },
  ],

  "py-36-context-managers": [
    {
      q: "What does <code>with</code> guarantee?",
      options: [
        "__exit__ runs when the block ends, even if an exception was raised",
        "The block runs without errors",
        "Any resources are garbage collected immediately",
        "The block runs in a separate scope",
      ],
      answer: 0,
      explain:
        "Cleanup happens on the way out, whatever the exit route. That is why " +
        "<code>with</code> is right for files, locks, database transactions and sockets: " +
        "anything with a release step you must not skip when something goes wrong.",
    },
    {
      q: "What is the easiest way to write your own context manager?",
      options: [
        "@contextlib.contextmanager on a generator, with a yield in the middle",
        "Subclass contextlib.ContextManager",
        "Define __with__ on the class",
        "Pass a cleanup function to with",
      ],
      answer: 0,
      explain:
        "The decorator turns a generator into a context manager: setup before the " +
        "<code>yield</code>, cleanup after, and a <code>try/finally</code> around it if " +
        "cleanup must survive exceptions. Writing <code>__enter__</code> and " +
        "<code>__exit__</code> by hand is the other way and is more code.",
    },
  ],

  "py-37-functional": [
    {
      q: "When is a lambda the right choice?",
      options: [
        "For a tiny throwaway expression, typically as a key= argument",
        "Whenever a function is only used once",
        "When the function must run faster",
        "For any function of one line",
      ],
      answer: 0,
      explain:
        "<code>sorted(items, key=lambda p: p.age)</code> is exactly the sweet spot. As " +
        "soon as a lambda needs a name, a branch or explaining, a <code>def</code> is " +
        "clearer and gets a real name in tracebacks. Lambdas are not faster.",
    },
    {
      q: "Why do most Python programmers prefer a comprehension to <code>map</code> and <code>filter</code>?",
      options: [
        "It reads more directly and does both jobs in one expression",
        "map and filter are deprecated",
        "Comprehensions are significantly faster",
        "map cannot be used with lambdas",
      ],
      answer: 0,
      explain:
        "<code>[f(x) for x in xs if cond(x)]</code> says the whole thing in one place, " +
        "where the equivalent needs nesting two calls and usually two lambdas. " +
        "<code>map</code> is still tidy when you already have a named function, as in " +
        "<code>map(str.strip, lines)</code>.",
    },
  ],

  "py-38-typing": [
    {
      q: "What does <code>Optional[str]</code> mean?",
      options: [
        "The value is either a str or None",
        "The argument may be omitted when calling",
        "The value can be any type",
        "The type hint is optional and may be ignored",
      ],
      answer: 0,
      explain:
        "It is exactly <code>str | None</code>, and modern Python spells it that way. It " +
        "says nothing about whether the argument is required: a parameter can be " +
        "mandatory and still accept <code>None</code>.",
    },
    {
      q: "What is a <code>Protocol</code> for?",
      options: [
        "Describing the shape a type must have, without requiring inheritance",
        "Defining a network protocol",
        "Marking a class as abstract",
        "Declaring which methods are public",
      ],
      answer: 0,
      explain:
        "It gives duck typing a name a checker can verify: anything with the right " +
        "methods satisfies it, with no base class involved. That fits how Python is " +
        "actually written, where you care whether a thing has <code>.read()</code> rather " +
        "than what it inherits from.",
    },
  ],

  "py-39-concurrency": [
    {
      q: "What does the GIL prevent?",
      options: [
        "Two threads running Python bytecode at the same time in one process",
        "Threads from being created at all",
        "Programs from using more than one CPU core, ever",
        "Threads from sharing memory safely",
      ],
      answer: 0,
      explain:
        "One lock, one thread running Python bytecode at a time in a process. Threads " +
        "still help enormously for I/O, because the lock is released while waiting. To " +
        "use several cores for computation you need processes, which is exactly what " +
        "<code>multiprocessing</code> is for.",
    },
    {
      q: "Your program downloads 100 files and is slow. Threads or processes?",
      options: [
        "Threads: the work is waiting on the network, not computing",
        "Processes, to use every core",
        "Neither; the GIL makes both pointless",
        "Processes, because threads cannot do networking",
      ],
      answer: 0,
      explain:
        "Downloading is waiting, and waiting releases the GIL, so threads overlap the " +
        "waits beautifully. Processes would work but cost far more memory and startup " +
        "time for no benefit. Save processes for CPU-bound work.",
    },
  ],

  "py-40-async": [
    {
      q: "What happens when you call an async function without awaiting it?",
      options: [
        "You get a coroutine object and the body never runs",
        "It runs in the background",
        "It runs immediately and blocks",
        "A SyntaxError",
      ],
      answer: 0,
      explain:
        "Calling it builds a coroutine and executes nothing. Python warns about \"never " +
        "awaited\" precisely because this silently does nothing. To run it concurrently " +
        "rather than sequentially, hand it to <code>asyncio.gather</code> or a " +
        "<code>TaskGroup</code>.",
    },
    {
      q: "Why does one blocking call ruin an async program?",
      options: [
        "It stops the event loop, so every other task is frozen until it finishes",
        "It raises an exception in the event loop",
        "It forces the loop to restart",
        "It only affects tasks created after it",
      ],
      answer: 0,
      explain:
        "The loop is a single thread cooperatively switching between tasks. A synchronous " +
        "<code>requests.get</code> or <code>time.sleep</code> never yields control, so " +
        "everything stops. Use the async equivalents, or push the blocking work to a " +
        "thread with <code>asyncio.to_thread</code>.",
    },
  ],

  /* ---------------- Level 5 ---------------- */

  "py-41-automation": [
    {
      q: "What is the safest way to develop a script that renames or deletes files in bulk?",
      options: [
        "Print what it would do first, and only act once the output looks right",
        "Run it on the real folder and check the result",
        "Keep a backup and run it",
        "Ask for confirmation on each file",
      ],
      answer: 0,
      explain:
        "A dry run costs nothing and catches the off-by-one that would have renamed four " +
        "hundred files wrongly. Backups help you recover; a dry run means you do not need " +
        "to. Confirming each file is fine for ten and useless for a thousand.",
    },
    {
      q: "Why prefer <code>pathlib</code> over building paths with string concatenation?",
      options: [
        "It handles separators and edge cases correctly across operating systems",
        "It is faster",
        "String paths are deprecated",
        "It can only be used with the standard library",
      ],
      answer: 0,
      explain:
        "<code>Path(\"data\") / \"file.txt\"</code> does the right thing everywhere, while " +
        "gluing strings with slashes breaks on Windows and doubles separators when a " +
        "trailing one sneaks in. It also gives you <code>.exists()</code>, " +
        "<code>.suffix</code> and friends without a second import.",
    },
  ],

  "py-42-http": [
    {
      q: "What does HTTP status 404 mean, precisely?",
      options: [
        "The server understood the request and has nothing at that address",
        "The server is down",
        "You are not allowed to see the resource",
        "The request was malformed",
      ],
      answer: 0,
      explain:
        "Not found, from a server that answered you perfectly well. Server down would " +
        "mean no response or a 5xx; not allowed is 401 or 403; malformed is 400. Reading " +
        "the first digit gets you most of the way: 4xx is your fault, 5xx is theirs.",
    },
    {
      q: "Why should you check <code>response.raise_for_status()</code> or the status code?",
      options: [
        "A failed request still returns a response object, so failure is silent otherwise",
        "It retries the request automatically",
        "It converts the response to JSON",
        "It is required before reading the body",
      ],
      answer: 0,
      explain:
        "You get a response object for a 500 exactly as for a 200, and calling " +
        "<code>.json()</code> on an error page gives a confusing parse error rather than " +
        "the real problem. Checking the status turns a mysterious failure into an obvious " +
        "one.",
    },
  ],

  "py-43-scraping": [
    {
      q: "What should you check before scraping a site?",
      options: [
        "Its terms of service and robots.txt, and whether an API exists instead",
        "That your scraper runs fast enough",
        "That the HTML is valid",
        "Nothing; public pages are public",
      ],
      answer: 0,
      explain:
        "Public to read does not mean licensed to harvest, and many sites offer an API " +
        "that is easier and explicitly allowed. Rate-limit yourself, identify your bot " +
        "honestly, and remember the legal picture varies by country and by use.",
    },
    {
      q: "Why is your scraper likely to break next month?",
      options: [
        "It depends on the page's HTML structure, which the site can change at any time",
        "Websites detect scrapers automatically",
        "BeautifulSoup releases break compatibility often",
        "HTML standards change frequently",
      ],
      answer: 0,
      explain:
        "You are depending on an interface nobody promised you. A class rename ships and " +
        "your selectors return nothing. Write scrapers to fail loudly rather than " +
        "silently returning empty results, and prefer an API whenever one exists.",
    },
  ],

  "py-44-web-apps": [
    {
      q: "Why should a web app never build SQL by concatenating user input?",
      options: [
        "Input can change the query's meaning: SQL injection",
        "It is slower than parameterised queries",
        "The database rejects concatenated strings",
        "It only works for SELECT statements",
      ],
      answer: 0,
      explain:
        "Input pasted into a query can end it and start another. Parameterised queries " +
        "send the SQL and the values separately, so a value is only ever a value. This is " +
        "decades old, still in the OWASP top ten, and completely solved by using " +
        "placeholders every time.",
    },
    {
      q: "What is the practical difference between Flask and FastAPI for a beginner?",
      options: [
        "FastAPI is async-first with automatic validation and docs from type hints",
        "Flask is deprecated",
        "FastAPI cannot serve HTML",
        "Flask cannot handle more than one request at a time",
      ],
      answer: 0,
      explain:
        "FastAPI leans on type hints to validate requests and generate interactive docs, " +
        "and is built around async. Flask is smaller and synchronous by default, which " +
        "makes it very easy to reason about. Both are excellent and widely used.",
    },
  ],

  "py-45-databases": [
    {
      q: "What does a database transaction give you?",
      options: [
        "All the changes happen, or none do",
        "A backup of the data before changes",
        "Faster writes by batching them",
        "Protection from other programs reading the data",
      ],
      answer: 0,
      explain:
        "Atomicity. Moving money between accounts must not stop halfway, and a transaction " +
        "is what makes the pair of updates a single all-or-nothing operation. Speed and " +
        "isolation are separate properties.",
    },
    {
      q: "Why is SQLite a good default for small projects?",
      options: [
        "It needs no server: the whole database is one file, and it ships with Python",
        "It is faster than every other database",
        "It supports more SQL features than PostgreSQL",
        "It handles thousands of concurrent writers well",
      ],
      answer: 0,
      explain:
        "Zero setup, one file you can copy or delete, and <code>sqlite3</code> is already " +
        "installed. Its genuine limit is concurrent writing, which is exactly when you " +
        "graduate to Postgres. For a personal tool it is very often the right answer " +
        "forever.",
    },
  ],

  "py-46-data": [
    {
      q: "Why is a NumPy array faster than a Python list for numerical work?",
      options: [
        "Elements are one type in a contiguous block, and operations run in compiled C",
        "Arrays are stored on the graphics card",
        "Lists are not designed to hold numbers",
        "Arrays use less memory per element only",
      ],
      answer: 0,
      explain:
        "A Python list holds pointers to separate objects; an array holds raw values side " +
        "by side, so operations run as tight compiled loops with no per-element " +
        "interpreter overhead. This is why vectorised code beats a Python <code>for</code> " +
        "loop so dramatically.",
    },
    {
      q: "What is the first thing to do with a dataset you have just loaded?",
      options: [
        "Look at it: shape, dtypes, head, and how many values are missing",
        "Plot it",
        "Remove every row with a missing value",
        "Convert it to a NumPy array",
      ],
      answer: 0,
      explain:
        "Nearly every data bug is a wrong assumption about the data. Five minutes on " +
        "<code>.shape</code>, <code>.dtypes</code>, <code>.head()</code> and " +
        "<code>.isna().sum()</code> catches the column read as text and the missing " +
        "values encoded as -999. Dropping rows before understanding them is how you lose " +
        "half your data quietly.",
    },
  ],

  "py-47-charts": [
    {
      q: "When is it genuinely misleading to start a bar chart's y-axis above zero?",
      options: [
        "Almost always, because bar length is the comparison being made",
        "Never; it is a normal way to show detail",
        "Only when the data is financial",
        "Only if the axis is unlabelled",
      ],
      answer: 0,
      explain:
        "A bar says \"compare these lengths\", so truncating the axis exaggerates " +
        "differences and is a classic way to lie with a true chart. Line charts showing " +
        "change over time are the accepted exception, since the reader is comparing slope " +
        "rather than length.",
    },
    {
      q: "What is the most common mistake in a beginner's chart?",
      options: [
        "No axis labels or units, so the reader cannot tell what is shown",
        "Using the wrong colour palette",
        "Too few data points",
        "Not using a chart library",
      ],
      answer: 0,
      explain:
        "A chart is a piece of communication, and an unlabelled axis makes it unreadable " +
        "regardless of how pretty it is. Labels, units and a title that says the finding " +
        "rather than the variable are worth more than any styling.",
    },
  ],

  "py-48-games": [
    {
      q: "What is the game loop?",
      options: [
        "Repeat forever: handle input, update the world, draw it",
        "The loop that plays background music",
        "The loop that waits for the player to press a key",
        "The sequence of levels in the game",
      ],
      answer: 0,
      explain:
        "Input, update, draw, over and over, many times a second. Every game from Pong to " +
        "a modern engine has this shape. Recognising it makes game code far less " +
        "intimidating: it is one loop with three jobs.",
    },
    {
      q: "Why should movement be scaled by elapsed time rather than a fixed amount per frame?",
      options: [
        "Otherwise the game runs faster on faster computers",
        "It makes collision detection more accurate",
        "It reduces memory use",
        "It is required by pygame",
      ],
      answer: 0,
      explain:
        "Moving five pixels per frame means twice the speed at twice the frame rate. " +
        "Multiplying by delta time makes speed real-world rather than hardware-dependent. " +
        "Old DOS games running absurdly fast on newer machines is exactly this bug.",
    },
  ],

  "py-49-desktop": [
    {
      q: "What does \"event-driven\" mean for a GUI program?",
      options: [
        "Your code responds to callbacks; a loop you do not write dispatches them",
        "The program runs events in the order you wrote them",
        "Every action is logged as an event",
        "The interface updates on a timer",
      ],
      answer: 0,
      explain:
        "You register handlers and the toolkit's loop calls them when things happen. That " +
        "inverts control compared with a script that runs top to bottom, and it is why " +
        "long work in a handler freezes the whole window: the loop cannot dispatch " +
        "anything while your code is running.",
    },
  ],

  "py-50-packaging": [
    {
      q: "What does <code>pip install -e .</code> do?",
      options: [
        "Installs the project so your edits take effect without reinstalling",
        "Installs only the dependencies",
        "Installs the package globally rather than in the environment",
        "Installs an older version for compatibility",
      ],
      answer: 0,
      explain:
        "Editable mode links to your source instead of copying it, which is exactly what " +
        "you want while developing: change a file, run the command, see the change. A " +
        "normal install copies, so edits do nothing until you reinstall.",
    },
    {
      q: "Under semantic versioning, when must you bump the first number?",
      options: [
        "When you change something that could break existing users",
        "When you add a significant feature",
        "Once a year, for marketing",
        "When you rewrite internals",
      ],
      answer: 0,
      explain:
        "The leading number is the compatibility promise, and raising it says \"read the " +
        "changelog before upgrading\". Features that break nothing bump the middle number, " +
        "fixes bump the last, and internal rewrites that keep the API bump nothing but the " +
        "patch.",
    },
  ],

  "py-51-performance": [
    {
      q: "What should you do before optimising anything?",
      options: [
        "Measure, to find where the time actually goes",
        "Rewrite the slowest-looking loop",
        "Add caching to the main function",
        "Switch to NumPy",
      ],
      answer: 0,
      explain:
        "Intuitions about performance are wrong often enough that guessing wastes real " +
        "time and usually makes code worse. <code>cProfile</code> and <code>timeit</code> " +
        "take minutes and regularly point somewhere you would never have looked.",
    },
    {
      q: "Your function checks <code>if x in big_list</code> inside a loop and is slow. What is the biggest win?",
      options: [
        "Convert the list to a set first",
        "Rewrite the loop as a comprehension",
        "Use multiprocessing",
        "Add type hints so Python can optimise it",
      ],
      answer: 0,
      explain:
        "Membership in a list scans it; in a set it hashes and jumps. That is an " +
        "algorithmic change, which beats micro-optimisation every time. Comprehensions " +
        "are about clarity, and type hints do nothing at runtime.",
    },
  ],

  "py-52-security": [
    {
      q: "How should a password be stored?",
      options: [
        "Hashed with a slow algorithm designed for passwords, such as bcrypt or argon2",
        "Encrypted, so it can be decrypted when needed",
        "Hashed with SHA-256 for speed",
        "In a database column only administrators can read",
      ],
      answer: 0,
      explain:
        "Hashing is one-way, so a stolen database does not hand over the passwords, and " +
        "slowness is the point: it makes brute force expensive. SHA-256 is fast, which is " +
        "a virtue everywhere else and a flaw here. If you can decrypt it, so can an " +
        "attacker who gets your key.",
    },
    {
      q: "Why is <code>eval()</code> on input from outside your program dangerous?",
      options: [
        "It executes arbitrary code with your program's permissions",
        "It is slow",
        "It only works on numbers",
        "It can crash on malformed input",
      ],
      answer: 0,
      explain:
        "It runs whatever it is given, so a string can delete files or open a network " +
        "connection. For turning text into data, use <code>json.loads</code> or " +
        "<code>ast.literal_eval</code>, which handle literals and nothing else.",
    },
    {
      q: "Where should an API key live?",
      options: [
        "In an environment variable or a secrets manager, never in the code",
        "In a config file committed with the project",
        "In the code, but in a separate module",
        "In a comment, so it is not executed",
      ],
      answer: 0,
      explain:
        "Anything in the repository is one push from being public, and bots scan public " +
        "repositories for exactly this. Environment variables keep the secret out of your " +
        "source entirely, which is why the Anthropic SDK reads one by default in the " +
        "Jarvis Build.",
    },
  ],

  /* ---------------- Level 6 ---------------- */

  "py-53-how-llms-work": [
    {
      q: "What is a language model fundamentally doing?",
      options: [
        "Predicting the next token, repeatedly",
        "Looking up answers in a database of text",
        "Searching the internet and summarising results",
        "Following rules written by its developers",
      ],
      answer: 0,
      explain:
        "One token at a time, each prediction informed by everything so far. Everything " +
        "else, apparent reasoning included, emerges from doing that extremely well at " +
        "scale. There is no lookup table, and no search unless a tool is explicitly " +
        "provided.",
    },
    {
      q: "What does the context window limit?",
      options: [
        "How much text the model can consider at once, prompt and reply together",
        "How long the model can spend thinking",
        "How many separate conversations it can hold",
        "How much it can remember between sessions",
      ],
      answer: 0,
      explain:
        "It is the total working space for one request. Between sessions it remembers " +
        "nothing at all: what looks like memory is your program resending the history, " +
        "which is the central insight of the whole Jarvis Build.",
    },
  ],

  "py-54-first-api-call": [
    {
      q: "Where should your API key come from in code?",
      options: [
        "An environment variable, read automatically by the SDK",
        "A constant at the top of the file, for clarity",
        "A prompt asking the user to type it each run",
        "A config file next to the script",
      ],
      answer: 0,
      explain:
        "The SDK looks for <code>ANTHROPIC_API_KEY</code> by itself, so your code never " +
        "mentions the key and stays safe to share or commit. A key in a file is one " +
        "careless push from being scraped by a bot, and people have woken up to real " +
        "bills.",
    },
    {
      q: "Why check the <code>type</code> of each block in <code>response.content</code>?",
      options: [
        "A reply can contain several kinds of block, and not all of them have .text",
        "The blocks arrive out of order",
        "Text blocks may be empty",
        "It is required before printing",
      ],
      answer: 0,
      explain:
        "<code>content</code> is a list, and once tools are involved a block may be a " +
        "tool request with no <code>.text</code> at all. The " +
        "<code>response.content[0].text</code> shortcut works right up until it dies with " +
        "an AttributeError you will not enjoy debugging.",
    },
  ],

  "py-55-memory": [
    {
      q: "How does a chat assistant \"remember\" earlier turns?",
      options: [
        "Your program keeps a list and resends the whole conversation each time",
        "The API stores the conversation against your key",
        "The model retains it in its weights",
        "A session id links the requests together",
      ],
      answer: 0,
      explain:
        "The API is stateless: it knows only what you send in that request. Memory is a " +
        "Python list you append to. Once that lands, personality, notes and tools all " +
        "stop being mysterious, because they are all just text you assemble before " +
        "sending.",
    },
    {
      q: "Why does a long conversation get more expensive per message?",
      options: [
        "You resend the entire history every time, so the input grows each turn",
        "The model charges more for later messages",
        "Longer conversations use a bigger model",
        "The context window costs money to keep open",
      ],
      answer: 0,
      explain:
        "Turn twenty sends twenty turns of history. The words are cheap; the repetition " +
        "adds up. The fixes are trimming old turns and prompt caching, which reprices the " +
        "stable prefix.",
    },
  ],

  "py-56-streaming": [
    {
      q: "What does streaming actually improve?",
      options: [
        "How soon the first words appear; the full reply takes the same time",
        "The total time to generate the reply",
        "The cost of the request",
        "The quality of the response",
      ],
      answer: 0,
      explain:
        "It changes perceived latency, not real throughput. You start reading in a " +
        "fraction of a second instead of watching a blank screen, which is the difference " +
        "between a program that feels alive and one that looks crashed.",
    },
    {
      q: "Why does printing a stream need <code>flush=True</code>?",
      options: [
        "Output is buffered by default, so fragments would not appear until a newline",
        "It forces the API to send the next chunk",
        "It prevents the text being garbled",
        "It closes the stream cleanly",
      ],
      answer: 0,
      explain:
        "Python buffers writes for speed, which is exactly wrong when you print " +
        "word-by-word with no newlines: the text sits in memory and lands all at once " +
        "anyway. <code>flush=True</code> pushes each piece out, and <code>end=\"\"</code> " +
        "stops each landing on its own line.",
    },
  ],

  "py-57-tools": [
    {
      q: "When a model \"uses a tool\", what actually happens?",
      options: [
        "It returns a request naming a tool and arguments; your code runs it and sends the result back",
        "The model executes the function on its own servers",
        "The API runs the function in a sandbox",
        "The model generates and runs Python code",
      ],
      answer: 0,
      explain:
        "The model cannot run anything. It asks; your program decides whether and how to " +
        "comply, then feeds the answer back. Every safety property follows from that: it " +
        "cannot use a tool you did not write, or do anything your function does not do.",
    },
    {
      q: "Tool results are sent back to the API with which role?",
      options: ['"user"', '"assistant"', '"tool"', '"system"'],
      answer: 0,
      explain:
        "They go back as a user turn, which surprises everybody, because the user did not " +
        "say it. The protocol treats anything your side supplies as coming from you. " +
        "Getting this wrong produces a confusing 400 rather than a helpful message.",
    },
    {
      q: "Why must a tool result carry the <code>tool_use_id</code> from the request?",
      options: [
        "It matches each result to the call it answers, since several can run at once",
        "It authenticates the result",
        "It tells the model which tool to run next",
        "It is used for billing",
      ],
      answer: 0,
      explain:
        "A single turn can request several tools, so results must be pairable with " +
        "requests. Copy the id from the block; inventing one is rejected. This is also " +
        "why you append the assistant turn unmodified, so its requests are still there to " +
        "match against.",
    },
  ],

  "py-58-your-data": [
    {
      q: "What does retrieval-augmented generation actually involve?",
      options: [
        "Searching your documents and putting the relevant text into the prompt",
        "Training the model on your documents",
        "Uploading your files to the model provider permanently",
        "Fine-tuning a copy of the model for you",
      ],
      answer: 0,
      explain:
        "Search, then paste the relevant part into the question. That is the whole idea. " +
        "It is dramatically cheaper than training, updates the instant you edit a file, " +
        "and lets you see exactly which text produced an answer.",
    },
    {
      q: "Why chunk documents with some overlap between pieces?",
      options: [
        "So a sentence split across a boundary still appears whole somewhere",
        "To make retrieval faster",
        "To reduce the number of chunks",
        "Because the API limits chunk size",
      ],
      answer: 0,
      explain:
        "Clean cuts slice sentences in half and leave both pieces useless. Overlapping " +
        "windows guarantee every sentence sits intact in at least one chunk, at the cost " +
        "of storing a little more.",
    },
  ],

  "py-59-voice": [
    {
      q: "What is the main honest trade when adding voice to an assistant?",
      options: [
        "Latency and accuracy: speech adds delay and transcription errors on top of everything else",
        "Voice models cost nothing but are slow",
        "Voice requires a local model",
        "Speech recognition only works in English",
      ],
      answer: 0,
      explain:
        "You add two more steps that can be slow and wrong, and a transcription mistake " +
        "propagates into the prompt where it becomes a confidently wrong answer. Voice is " +
        "delightful when it works and worth entering with clear eyes.",
    },
  ],

  "py-60-local-models": [
    {
      q: "What is the genuine advantage of running a model locally?",
      options: [
        "Nothing leaves your machine, and there is no per-token cost",
        "Local models are more capable than hosted ones",
        "It is always faster",
        "You avoid needing any hardware",
      ],
      answer: 0,
      explain:
        "Privacy is absolute and the marginal cost is electricity. The trade is real: " +
        "open-weight models you can run at home are generally less capable than the " +
        "largest hosted ones, and speed depends entirely on your hardware.",
    },
  ],

  "py-61-assemble-jarvis": [
    {
      q: "Why split the assistant into config, memory, tools and chat modules?",
      options: [
        "Each has one job, so you can change one without reading the others",
        "Python requires modules over a certain file size",
        "It makes the program run faster",
        "It is needed for the code to be importable",
      ],
      answer: 0,
      explain:
        "Separation of concerns. Changing how history is stored should not mean reading " +
        "the tool code. It is the difference between a script you wrote and a program you " +
        "can still maintain in three months.",
    },
  ],

  "py-62-ethics-cost": [
    {
      q: "How should you count tokens to estimate cost?",
      options: [
        "client.messages.count_tokens(), which counts the way the billing model counts",
        "A general-purpose tokenizer library",
        "Divide the character count by four",
        "len(text.split()) for a word count",
      ],
      answer: 0,
      explain:
        "Tokenizers differ between model families, so borrowing one from another " +
        "ecosystem gives a confidently wrong number. The character and word " +
        "approximations are fine for a rough sense and no good for a spending cap.",
    },
    {
      q: "What is the most reliable way to avoid a surprise bill?",
      options: [
        "A hard cap your own code checks before every call, plus a bound on every loop",
        "Choosing a cheaper model",
        "Watching the dashboard regularly",
        "Setting max_tokens low",
      ],
      answer: 0,
      explain:
        "Every surprise-bill story is an unbounded loop running unattended. A cheaper " +
        "model and a low <code>max_tokens</code> both reduce the per-call cost but " +
        "multiply by infinity just as well. The fix is arithmetic your code performs " +
        "before it spends anything.",
    },
  ],
};
