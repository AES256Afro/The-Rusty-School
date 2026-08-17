/* ============================================================
   Per-lesson mini-quizzes (Rust)

   Two or three questions at the foot of every lesson. app.js loads
   this file on lesson pages only and injects the quiz above the
   "Mark lesson complete" button, so no lesson HTML has to change.

   Scores live in the existing rusty-quiz-best map under the key
   "lesson-<id>", which means they sync to accounts for free.

   Writing rules, learned the hard way:
     * Test the misconception, not the vocabulary. A question whose
       answer is a definition teaches nothing.
     * Every wrong option should be something a beginner actually
       believes. Silly distractors make the right answer findable
       without understanding.
     * The explanation is the real payload. Say why the right answer
       is right AND why the tempting wrong one is wrong.
     * Every `code` snippet here has been compiled by
       tools/verify-quiz-code.sh. Same rule as the lessons.
   ============================================================ */
window.RUSTY_LESSON_QUIZ = {

  /* ---------------- Base Camp ---------------- */

  "f1-computers": [
    {
      q: "Why do computers use binary rather than ordinary decimal digits?",
      options: [
        "Because it is easy to build hardware that reliably tells two states apart",
        "Because binary maths is faster than decimal maths",
        "Because early programmers preferred it and we are stuck with the choice",
        "Because binary uses less electricity than decimal would",
      ],
      answer: 0,
      explain:
        "It is a physics and engineering answer, not a mathematical one. A circuit can " +
        "reliably distinguish \"voltage present\" from \"voltage absent\", and that " +
        "reliability is everything. Distinguishing ten different voltage levels is " +
        "possible but far more fragile. The maths itself is not faster in binary; there " +
        "is simply less to get wrong.",
    },
    {
      q: "Your program is running and holding some data. Where does that data live?",
      options: [
        "In memory (RAM), which is fast and forgets everything when power is lost",
        "On the storage drive, because that is where files are kept",
        "In the CPU itself, which holds everything the program needs",
        "In the operating system, which stores it for the program",
      ],
      answer: 0,
      explain:
        "Working data lives in RAM: fast, and wiped the moment power goes. Storage is " +
        "slow and permanent, which is why you must explicitly save. The CPU holds only " +
        "a tiny amount at a time in its registers, and it is doing the work rather than " +
        "storing it. That distinction is behind an enormous amount of programming.",
    },
    {
      q: "What does a compiler actually do?",
      options: [
        "Translates the code you wrote into instructions the machine can execute",
        "Runs your code line by line as it reads it",
        "Checks your code for mistakes and nothing more",
        "Downloads the libraries your program needs",
      ],
      answer: 0,
      explain:
        "It translates, once, ahead of time, producing something the machine runs " +
        "directly. Running line by line as it reads is an interpreter, which is roughly " +
        "how Python works. Catching mistakes is a very valuable side effect of having to " +
        "understand your code well enough to translate it, but it is not the job.",
    },
  ],

  "f2-toolbox": [
    {
      q: "What is the practical difference between an absolute and a relative path?",
      options: [
        "An absolute path works from anywhere; a relative one depends on where you are",
        "An absolute path is longer, but they behave identically",
        "A relative path only works for files inside your home folder",
        "An absolute path is for folders and a relative path is for files",
      ],
      answer: 0,
      explain:
        "An absolute path starts at the root and means the same thing no matter your " +
        "current directory. A relative path is interpreted from wherever you are " +
        "standing, which is exactly why the same command can work in one folder and " +
        "fail in another. When something mysteriously cannot find a file, this is the " +
        "first thing to check.",
    },
    {
      q: "Why use a library instead of writing the code yourself?",
      options: [
        "Someone already solved it, and their version has been tested by many people",
        "Libraries always run faster than code you would write",
        "It is considered bad practice to write your own functions",
        "Libraries are the only way to do complicated things",
      ],
      answer: 0,
      explain:
        "The value is other people's debugging. A widely used library has met edge cases " +
        "you have not thought of yet. Speed is not guaranteed, and writing your own code " +
        "is completely normal. The real trade is that every dependency is also code you " +
        "did not read and now rely on, which is why adding one should be a decision " +
        "rather than a reflex.",
    },
  ],

  "f3-git": [
    {
      q: "What is a commit, in one sentence?",
      options: [
        "A saved snapshot of your project at a moment, with a note about why",
        "A backup copy of your files uploaded to GitHub",
        "A list of the changes you made since the last time you saved a file",
        "A request for someone to review your work",
      ],
      answer: 0,
      explain:
        "A snapshot plus a message. The message is the part beginners skip and later " +
        "wish they had not, because \"why\" is the thing you cannot reconstruct from the " +
        "code six months on. It is not a backup either: commits live in your local repo " +
        "until you push them somewhere else.",
    },
    {
      q: "You have made commits locally but your teammate cannot see them on GitHub. Why?",
      options: [
        "You have not pushed yet; commits are local until you send them",
        "Commits take a few minutes to appear on GitHub",
        "Your teammate needs to refresh their copy with git pull",
        "You committed to the wrong file",
      ],
      answer: 0,
      explain:
        "Committing and sharing are deliberately separate steps. Everything stays on " +
        "your machine until you push, which is what lets you commit freely while " +
        "offline or mid-experiment. A pull on their end cannot help, because there is " +
        "nothing on the server to pull yet.",
    },
  ],

  "f4-standards": [
    {
      q: "A library goes from version 1.4.2 to 2.0.0. Under semantic versioning, what does that tell you?",
      options: [
        "Something changed in a way that can break code using the old version",
        "There are major new features, but your existing code is safe",
        "It is the second stable release, and nothing more",
        "The library was rewritten from scratch",
      ],
      answer: 0,
      explain:
        "The leading number is the compatibility promise. Bumping it says \"this may " +
        "break you\". New features that do not break anything bump the middle number; " +
        "fixes bump the last. That is the entire point: the version tells you how " +
        "carefully to read the changelog before upgrading.",
    },
    {
      q: "Why does Rust ship a formatter (rustfmt) that everyone is expected to use?",
      options: [
        "It ends formatting arguments so review time goes to logic instead",
        "Formatted code runs measurably faster",
        "The compiler refuses to build inconsistently formatted code",
        "It is the only way to catch style mistakes",
      ],
      answer: 0,
      explain:
        "The win is social, not technical. When the formatter decides, nobody spends " +
        "review time on brace placement, and every Rust codebase looks familiar. The " +
        "compiler does not care about your whitespace at all, and formatting has no " +
        "effect on the compiled output.",
    },
  ],

  "f5-mindset": [
    {
      q: "You have followed six tutorials and still cannot start a project alone. What does that mean?",
      options: [
        "Following along and building from nothing are different skills; you have practised only one",
        "You need to find better tutorials before trying to build anything",
        "You have not memorised enough syntax yet",
        "Programming may not be for you",
      ],
      answer: 0,
      explain:
        "This is tutorial hell, and it is a completely predictable result rather than a " +
        "personal failing. Following a tutorial exercises comprehension; building " +
        "exercises decision-making, and only one of those is being trained. The way out " +
        "is a blank file and something small you actually want, which will feel much " +
        "harder for a while because it is a harder thing.",
    },
    {
      q: "What makes a good question when you are stuck?",
      options: [
        "What you tried, what you expected, and what actually happened, with the real error",
        "A clear description of the goal, so people can suggest the best approach",
        "The full file, so nothing is left out",
        "An apology for being a beginner, so people are patient",
      ],
      answer: 0,
      explain:
        "Tried, expected, happened, plus the exact error text. That shape lets someone " +
        "help in one reply instead of five clarifying questions, and writing it out " +
        "solves the problem surprisingly often on its own. Dumping an entire file makes " +
        "helping expensive, and nobody needs the apology.",
    },
  ],

  /* ---------------- Level 1 ---------------- */

  "01-hello-world": [
    {
      q: "What is the difference between <code>cargo build</code> and <code>cargo run</code>?",
      options: [
        "run compiles if needed and then executes; build only compiles",
        "build is for release versions and run is for testing",
        "They are the same, but run prints more information",
        "build checks for errors without producing a program",
      ],
      answer: 0,
      explain:
        "<code>cargo run</code> is <code>cargo build</code> followed by executing the " +
        "result, skipping the compile if nothing changed. The one that checks without " +
        "producing a program is <code>cargo check</code>, which is much faster and worth " +
        "knowing when you just want to know whether it compiles.",
    },
    {
      q: "Why does <code>println!</code> end with an exclamation mark?",
      options: [
        "It is a macro, not a function: it writes code for you at compile time",
        "It signals that the line prints something to the screen",
        "It means the call could fail and crash the program",
        "It is a naming convention for functions from the standard library",
      ],
      answer: 0,
      explain:
        "The <code>!</code> always means macro. Macros generate code before compilation, " +
        "which is how <code>println!</code> can accept any number of arguments and check " +
        "your format string at compile time. An ordinary function could not do either. " +
        "Nothing about it implies printing or failure.",
    },
    {
      q: "What does this print?",
      code: 'fn main() {\n    // println!("first");\n    println!("second");\n}',
      options: ["second", "first\nsecond", "first", "Nothing: it will not compile"],
      answer: 0,
      explain:
        "Everything after <code>//</code> is a comment: the compiler ignores it " +
        "entirely, so the first line does not exist as far as the program is concerned. " +
        "Commenting a line out to see what changes is one of the most useful debugging " +
        "habits you can build.",
    },
  ],

  "02-variables": [
    {
      q: "Why does Rust make variables immutable unless you write <code>mut</code>?",
      options: [
        "Most values never need to change, and unexpected changes are a huge source of bugs",
        "Immutable variables are faster to access",
        "It makes the language easier for the compiler to parse",
        "So that variables can be shared safely between threads automatically",
      ],
      answer: 0,
      explain:
        "It is a default chosen from experience: values that change unexpectedly are " +
        "behind an enormous share of real bugs, so Rust makes changing them something " +
        "you say out loud. There is no speed difference, and immutability alone does not " +
        "make something thread-safe, though it helps a great deal.",
    },
    {
      q: "What does this print?",
      code: 'fn main() {\n    let x = 5;\n    let x = x + 1;\n    let x = x * 2;\n    println!("{x}");\n}',
      options: ["12", "5", "It will not compile: x is immutable", "11"],
      answer: 0,
      explain:
        "This is shadowing, and it compiles even though <code>x</code> is immutable. " +
        "Each <code>let</code> creates a brand-new variable that happens to reuse the " +
        "name, so nothing was ever mutated: 5, then 6, then 12. This is why shadowing is " +
        "not a loophole in immutability.",
    },
    {
      q: "What is the real difference between shadowing and <code>mut</code>?",
      options: [
        "Shadowing makes a new variable, so it can change the type; mut changes the value in place",
        "Shadowing only works inside functions, while mut works anywhere",
        "They are two spellings of the same thing",
        "Shadowing is slower because it allocates twice",
      ],
      answer: 0,
      explain:
        "Shadowing creates a new binding, so <code>let spaces = \"   \";</code> followed " +
        "by <code>let spaces = spaces.len();</code> is fine even though the type changed " +
        "from string to number. With <code>mut</code> the type is fixed for the " +
        "variable's life. That type-changing ability is the main reason to reach for " +
        "shadowing.",
    },
  ],

  "03-types": [
    {
      q: "Why does Rust have both <code>i32</code> and <code>u32</code>?",
      options: [
        "u32 cannot be negative, so it uses its whole range for positive numbers",
        "u32 is faster because it skips the sign check",
        "i32 is for maths and u32 is for counting only",
        "u32 can hold twice as many digits as i32",
      ],
      answer: 0,
      explain:
        "The <code>u</code> is unsigned: no negatives, so the same 32 bits reach twice as " +
        "far upward. Choosing an unsigned type also documents an intent the compiler " +
        "enforces, which is why lengths and counts are unsigned. They are the same size " +
        "and the same speed.",
    },
    {
      q: "What happens here?",
      code: 'fn main() {\n    let x: f64 = 7.0 / 2.0;\n    let y: i32 = 7 / 2;\n    println!("{x} {y}");\n}',
      options: [
        "3.5 3",
        "3.5 3.5",
        "3 3",
        "It will not compile: you cannot divide integers",
      ],
      answer: 0,
      explain:
        "Integer division throws away the remainder rather than rounding, so " +
        "<code>7 / 2</code> is 3, not 3.5 and not 4. Float division keeps it. This " +
        "single behaviour is behind a large share of surprising off-by-one results in " +
        "every language that has it.",
    },
    {
      q: "What is a tuple good for that an array is not?",
      options: [
        "Holding values of different types together",
        "Holding more than a fixed number of values",
        "Being changed after creation",
        "Being looped over easily",
      ],
      answer: 0,
      explain:
        "A tuple groups mixed types, like <code>(String, i32, bool)</code>, which is why " +
        "it is the natural way to return several values from a function. An array " +
        "requires every element to be the same type. Neither can grow, which is what " +
        "<code>Vec</code> is for.",
    },
  ],

  "04-functions": [
    {
      q: "What does this function return?",
      code: 'fn add(a: i32, b: i32) -> i32 {\n    a + b\n}\n\nfn main() {\n    println!("{}", add(2, 3));\n}',
      options: [
        "5, because the last expression without a semicolon is the return value",
        "Nothing: it is missing a return statement",
        "5, but only because add is a simple function",
        "It will not compile: the last line needs a semicolon",
      ],
      answer: 0,
      explain:
        "Rust functions return their final expression, and leaving the semicolon off is " +
        "what makes it an expression rather than a statement. Adding a semicolon there " +
        "would turn it into a statement that evaluates to <code>()</code>, and the " +
        "compiler would complain about the mismatched return type. That error is a rite " +
        "of passage.",
    },
    {
      q: "Why must function parameters have type annotations, when local variables often do not?",
      options: [
        "So the compiler can check every call site without reading the whole program",
        "Because the compiler cannot infer types inside functions",
        "It is a style rule rather than a requirement",
        "Because parameters can change type between calls",
      ],
      answer: 0,
      explain:
        "The signature is a contract. Because it is written down, callers can be checked " +
        "independently and error messages point at the actual mistake rather than " +
        "somewhere three functions away. Inference works fine inside a body; it is " +
        "deliberately not used across the boundary.",
    },
  ],

  "05-control-flow": [
    {
      q: "What does this print?",
      code: 'fn main() {\n    let n = 7;\n    let label = if n % 2 == 0 { "even" } else { "odd" };\n    println!("{label}");\n}',
      options: [
        "odd, because if is an expression that produces a value",
        "It will not compile: if cannot be assigned to a variable",
        "odd, but only because both branches return the same type",
        "true",
      ],
      answer: 0,
      explain:
        "<code>if</code> is an expression in Rust, so it evaluates to a value you can " +
        "bind. Both arms must have the same type, which is true here. This is why Rust " +
        "has no need for the <code>? :</code> ternary operator other languages use.",
    },
    {
      q: "When would you use <code>loop</code> rather than <code>while</code>?",
      options: [
        "When you want to repeat until something inside decides to break, possibly with a value",
        "When you need the loop to run faster",
        "When you know exactly how many iterations you need",
        "When looping over a collection",
      ],
      answer: 0,
      explain:
        "<code>loop</code> says \"forever until I break\", and uniquely it can return a " +
        "value with <code>break value</code>, which is perfect for retry loops. A known " +
        "count or a collection both want <code>for</code>. Picking the loop that matches " +
        "your intent makes the code read correctly.",
    },
    {
      q: "What is the danger of <code>while</code> that <code>for</code> avoids?",
      options: [
        "Forgetting to advance the condition, producing an infinite loop",
        "It cannot loop over collections at all",
        "It is slower because the condition is checked each time",
        "It cannot use break or continue",
      ],
      answer: 0,
      explain:
        "With <code>while</code> you are responsible for making progress toward the exit, " +
        "and forgetting is easy. <code>for</code> takes an iterator that runs out on its " +
        "own, which removes both infinite loops and index mistakes. That is why " +
        "<code>for</code> is the one you reach for by default.",
    },
  ],

  /* ---------------- Level 2 ---------------- */

  "06-ownership": [
    {
      q: "Why does Rust need ownership at all?",
      options: [
        "To free memory automatically and safely, without a garbage collector",
        "To make programs use less memory than other languages",
        "To stop two threads running at the same time",
        "To let the compiler optimise loops more aggressively",
      ],
      answer: 0,
      explain:
        "Every language must decide when to release memory. Manual freeing invites " +
        "use-after-free and double-free bugs; a garbage collector costs runtime and " +
        "pauses. Ownership answers the question at compile time, so there is no " +
        "collector and no runtime cost, which is the whole trade Rust is making.",
    },
    {
      q: "What happens here?",
      code: 'fn main() {\n    let s1 = String::from("hello");\n    let s2 = s1;\n    println!("{s1}");\n}',
      options: [
        "It does not compile: s1 was moved into s2",
        "It prints hello, because s2 is a copy",
        "It prints nothing, because s1 is now empty",
        "It compiles but crashes at runtime",
      ],
      answer: 0,
      explain:
        "Assigning a <code>String</code> moves ownership, so <code>s1</code> is no longer " +
        "usable and the compiler stops you. This is the error that makes people think " +
        "Rust is hostile, and it is genuinely preventing a double-free. Use " +
        "<code>&s1</code> to borrow, or <code>s1.clone()</code> if you really want two.",
    },
    {
      q: "Why can integers be assigned twice when Strings cannot?",
      options: [
        "Integers are Copy: a fixed-size value on the stack, so copying is trivial",
        "Integers are immutable and Strings are not",
        "Integers are smaller, so Rust makes an exception for speed",
        "Integers are owned by the compiler rather than your code",
      ],
      answer: 0,
      explain:
        "Types that are entirely a small fixed-size value on the stack implement " +
        "<code>Copy</code>, so assignment duplicates the bits and both remain valid. A " +
        "<code>String</code> owns memory on the heap, so duplicating it would mean two " +
        "owners of one allocation, and that is precisely the bug ownership exists to " +
        "prevent.",
    },
  ],

  "07-borrowing": [
    {
      q: "What are the two borrowing rules?",
      options: [
        "Any number of shared borrows, or exactly one mutable borrow, never both at once",
        "One borrow at a time, always",
        "Mutable borrows must be declared before shared ones",
        "You may borrow only values you did not create",
      ],
      answer: 0,
      explain:
        "Many readers or one writer, never simultaneously. That single rule eliminates " +
        "data races by construction, and it is the same rule a reader-writer lock " +
        "enforces at runtime, except the compiler enforces it for free before your " +
        "program ever runs.",
    },
    {
      q: "Does this compile?",
      code: 'fn main() {\n    let mut s = String::from("hi");\n    let r1 = &s;\n    let r2 = &s;\n    println!("{r1} {r2}");\n    let r3 = &mut s;\n    r3.push_str(" there");\n    println!("{r3}");\n}',
      options: [
        "Yes: the shared borrows are finished before the mutable one starts",
        "No: you cannot have a mutable borrow after shared ones",
        "No: r1 and r2 cannot both borrow s",
        "Yes, but only because s is declared mut",
      ],
      answer: 0,
      explain:
        "A borrow lasts until its last use, not until the end of the block. " +
        "<code>r1</code> and <code>r2</code> are done after the first " +
        "<code>println!</code>, so the mutable borrow that follows is fine. This is " +
        "non-lexical lifetimes, and it is why a lot of intuitively reasonable code " +
        "compiles that older Rust would have rejected.",
    },
    {
      q: "What is a slice?",
      options: [
        "A borrowed view of part of a collection, holding no ownership of its own",
        "A copy of part of a collection",
        "A collection that can grow from either end",
        "A pointer to a single element",
      ],
      answer: 0,
      explain:
        "A slice borrows a contiguous run of an existing collection: a pointer and a " +
        "length, owning nothing. That is why taking a slice is free and why the borrow " +
        "checker will not let the underlying collection be modified while the slice is " +
        "alive. <code>&str</code> is exactly this over a <code>String</code>.",
    },
  ],

  "08-structs": [
    {
      q: "Why does printing a struct with <code>{:?}</code> require <code>#[derive(Debug)]</code>?",
      options: [
        "Rust adds no behaviour you did not ask for; the derive generates the code",
        "Debug printing is slow, so it must be opted into",
        "It is only needed for structs with more than one field",
        "The derive marks the struct as safe to print to a terminal",
      ],
      answer: 0,
      explain:
        "Nothing is automatic in Rust. Formatting requires an implementation, and " +
        "<code>derive</code> writes the obvious one for you at compile time. You could " +
        "write it by hand and sometimes will, when the automatic output is not the shape " +
        "you want.",
    },
    {
      q: "What is the difference between <code>&self</code> and <code>self</code> in a method?",
      options: [
        "&self borrows the value; self takes ownership and consumes it",
        "&self is for reading and self is for writing",
        "They are interchangeable and &self is just shorter",
        "self is only valid in associated functions",
      ],
      answer: 0,
      explain:
        "<code>&self</code> borrows, so the caller keeps the value: this is the common " +
        "case. Plain <code>self</code> takes ownership and the caller cannot use it " +
        "afterwards, which is exactly right for conversions like " +
        "<code>into_bytes</code>. Writing needs <code>&mut self</code>.",
    },
    {
      q: "Why is <code>new</code> a convention rather than a keyword in Rust?",
      options: [
        "It is just an associated function; Rust has no special constructor concept",
        "Because constructors are discouraged in Rust",
        "Because new is reserved for the standard library",
        "Because structs cannot have real constructors",
      ],
      answer: 0,
      explain:
        "There is no constructor mechanism at all. <code>new</code> is an ordinary " +
        "associated function that happens to return <code>Self</code>, and the name is " +
        "pure convention. That is why you can freely have <code>with_capacity</code>, " +
        "<code>from_str</code> and several others alongside it.",
    },
  ],

  "09-enums": [
    {
      q: "What problem does <code>Option&lt;T&gt;</code> solve?",
      options: [
        "It makes \"there might be nothing here\" visible in the type and impossible to ignore",
        "It lets a variable hold more than one type at a time",
        "It makes values optional so you can leave them out",
        "It stops variables being used before they are set",
      ],
      answer: 0,
      explain:
        "Languages with null let any value secretly be nothing, and the compiler cannot " +
        "help. <code>Option</code> puts that possibility in the type, so you must handle " +
        "the <code>None</code> case to get at the value. Tony Hoare called null his " +
        "billion-dollar mistake; this is the fix.",
    },
    {
      q: "Why must a <code>match</code> be exhaustive?",
      options: [
        "So adding a new variant later becomes a compile error everywhere it matters",
        "So the compiler can generate a faster jump table",
        "Because match cannot have a default case",
        "So the code reads more clearly",
      ],
      answer: 0,
      explain:
        "This is one of Rust's best features in practice. Add a variant to an enum and " +
        "every <code>match</code> that has not considered it fails to compile, handing " +
        "you a to-do list instead of a runtime surprise. You can opt out with " +
        "<code>_</code>, which is sometimes right and sometimes throws that benefit away.",
    },
    {
      q: "When is <code>if let</code> the better choice over <code>match</code>?",
      options: [
        "When you care about exactly one pattern and want to ignore the rest",
        "When the enum has only two variants",
        "When you need to handle every case",
        "When matching on a value that could be null",
      ],
      answer: 0,
      explain:
        "<code>if let</code> is sugar for a <code>match</code> with one arm and a " +
        "<code>_ =&gt; {}</code>. It is clearer when one case matters, and it quietly " +
        "gives up exhaustiveness checking, which is the trade you are making. Reach for " +
        "<code>match</code> when the other cases deserve thought.",
    },
  ],

  "10-collections": [
    {
      q: "What is the difference between <code>v[5]</code> and <code>v.get(5)</code>?",
      options: [
        "Indexing panics if out of range; get returns an Option you can handle",
        "get is slower because it checks bounds",
        "Indexing works on arrays and get works on vectors",
        "They are identical; get is just more explicit",
      ],
      answer: 0,
      explain:
        "Both check the bounds. The difference is what happens when the check fails: " +
        "indexing panics and stops the program, while <code>get</code> returns " +
        "<code>None</code> and hands you the decision. Use indexing when being out of " +
        "range is a bug, and <code>get</code> when it is a possibility.",
    },
    {
      q: "Why does this fail to compile?",
      code: 'fn main() {\n    let mut v = vec![1, 2, 3];\n    for n in &v {\n        v.push(*n);\n    }\n}',
      options: [
        "The loop borrows v, so pushing (which needs a mutable borrow) is not allowed",
        "You cannot dereference n inside a loop",
        "vec! creates an immutable vector",
        "push needs an index argument",
      ],
      answer: 0,
      explain:
        "The <code>for</code> loop holds a shared borrow of <code>v</code> for its whole " +
        "body, and <code>push</code> wants a mutable one. Many readers or one writer, " +
        "never both. In C++ this compiles and can invalidate the iterator when the " +
        "vector reallocates, which is exactly the crash Rust is refusing to let you " +
        "write.",
    },
    {
      q: "What does <code>HashMap</code> give you that <code>Vec</code> does not?",
      options: [
        "Lookup by a key of your choosing, in roughly constant time",
        "The ability to store different types together",
        "Guaranteed ordering of the elements",
        "Automatic sorting as you insert",
      ],
      answer: 0,
      explain:
        "A <code>Vec</code> finds things by position; a <code>HashMap</code> finds them " +
        "by key without scanning. The cost is that iteration order is unspecified, " +
        "which surprises people: if you need order, sort the keys when you iterate or " +
        "use a <code>BTreeMap</code>.",
    },
  ],

  /* ---------------- Level 3 ---------------- */

  "11-errors": [
    {
      q: "When should a program panic rather than return a <code>Result</code>?",
      options: [
        "When the failure means a bug in the program itself and continuing is meaningless",
        "Whenever an error occurs, because panicking is simpler",
        "Only in tests, never in real code",
        "When the error message needs to be shown to a user",
      ],
      answer: 0,
      explain:
        "Panic is for broken assumptions: the thing that happened should have been " +
        "impossible. Expected problems, like a missing file or bad input, are ordinary " +
        "and deserve a <code>Result</code> so the caller can decide. Panicking on those " +
        "takes the choice away from code that might have handled it fine.",
    },
    {
      q: "What does <code>?</code> do?",
      options: [
        "Returns the error from the current function early, or unwraps the success value",
        "Panics with a message if the value is an error",
        "Converts a Result into an Option",
        "Retries the operation once before failing",
      ],
      answer: 0,
      explain:
        "On <code>Ok</code> it hands you the value and carries on; on <code>Err</code> " +
        "it returns immediately from your function with that error, converting the type " +
        "if needed. It replaces about five lines of match with one character, which is " +
        "why real Rust error handling reads so cleanly.",
    },
    {
      q: "Why is <code>unwrap()</code> discouraged in production code?",
      options: [
        "It panics on failure, discarding the error and any chance to recover",
        "It is slower than matching on the Result",
        "It only works on Option, not Result",
        "It hides the value's type from the compiler",
      ],
      answer: 0,
      explain:
        "It converts a recoverable situation into a crash, and throws away the " +
        "explanation on the way out. It is genuinely fine in prototypes, examples and " +
        "tests. When you do want to assert an invariant, <code>expect(\"why this " +
        "cannot fail\")</code> at least leaves a note for whoever hits it.",
    },
  ],

  "12-traits": [
    {
      q: "What is a trait, in one sentence?",
      options: [
        "A set of behaviour a type can implement, which other code can then require",
        "A base type that other types inherit from",
        "A collection of related functions grouped under a name",
        "A way to add fields to an existing type",
      ],
      answer: 0,
      explain:
        "A trait describes what a type can do, and generic code can demand it. It is " +
        "deliberately not inheritance: there is no parent type and no shared fields, " +
        "only shared capability. That distinction is what lets you implement your own " +
        "trait for someone else's type.",
    },
    {
      q: "What does <code>fn largest&lt;T: PartialOrd&gt;(list: &[T]) -&gt; &T</code> promise?",
      options: [
        "It works for any type that can be compared with <, checked at compile time",
        "It works for any type at all, with comparison checked at runtime",
        "It only works for numbers",
        "It returns a copy of the largest element",
      ],
      answer: 0,
      explain:
        "The bound <code>T: PartialOrd</code> is a compile-time requirement: any type " +
        "with ordering works, and anything else is rejected at the call site. Rust then " +
        "generates specialised code per type, so the generality costs nothing at " +
        "runtime. Note the return is <code>&T</code>, a borrow, not a copy.",
    },
    {
      q: "Why does Rust require a trait bound instead of just trying the operation?",
      options: [
        "So errors appear at the definition and every caller is checked honestly",
        "Because the compiler cannot tell what operations a type supports",
        "To make generic code run faster",
        "Because traits are needed to allocate memory for T",
      ],
      answer: 0,
      explain:
        "It is the same contract idea as function signatures. With bounds, a generic " +
        "function is checked once against its promises, and mistakes point at the " +
        "caller who broke them. Languages that substitute first produce errors deep " +
        "inside library code, which is far harder to read.",
    },
  ],

  "13-lifetimes": [
    {
      q: "What does a lifetime annotation actually do?",
      options: [
        "Describes how long references are valid so the compiler can check them",
        "Controls when a value is dropped from memory",
        "Makes a reference live longer than it otherwise would",
        "Marks a value as safe to share between threads",
      ],
      answer: 0,
      explain:
        "Annotations describe relationships that already exist; they never change them. " +
        "You are telling the compiler how the inputs and outputs relate so it can verify " +
        "no reference outlives what it points at. Nothing about the generated program " +
        "changes.",
    },
    {
      q: "Why does this need a lifetime annotation?",
      code: "fn longest<'a>(a: &'a str, b: &'a str) -> &'a str {\n    if a.len() > b.len() { a } else { b }\n}",
      options: [
        "The compiler cannot tell whether the returned reference came from a or b",
        "Because the function takes more than one argument",
        "Because &str is always borrowed",
        "Because the function compares lengths",
      ],
      answer: 0,
      explain:
        "The return could be either input, so the compiler cannot work out how long it " +
        "stays valid on its own. The annotation says the result lives as long as the " +
        "shorter of the two, which is enough to check every call. Return a reference to " +
        "only one parameter and elision handles it silently.",
    },
    {
      q: "Why do you rarely write lifetimes in everyday Rust?",
      options: [
        "Elision rules infer the common patterns automatically",
        "Most code avoids references entirely",
        "The compiler adds them to your source when it compiles",
        "They are only needed in library code",
      ],
      answer: 0,
      explain:
        "Three elision rules cover the overwhelmingly common shapes, so you only write " +
        "lifetimes when the relationship is genuinely ambiguous. They were required " +
        "everywhere in early Rust, and the rules exist because that was miserable.",
    },
  ],

  "14-iterators": [
    {
      q: "What does \"iterators are lazy\" mean?",
      options: [
        "Nothing happens until something consumes them; adaptors just build a recipe",
        "They run in the background while your program continues",
        "They cache results so repeated passes are faster",
        "They only load part of a collection into memory",
      ],
      answer: 0,
      explain:
        "<code>map</code> and <code>filter</code> build a description of work and do " +
        "none of it. A consumer like <code>collect</code>, <code>sum</code> or a " +
        "<code>for</code> loop drives the whole chain in a single pass. This is why a " +
        "chain of ten adaptors does not make ten intermediate vectors.",
    },
    {
      q: "What does this print?",
      code: 'fn main() {\n    let v = vec![1, 2, 3, 4];\n    let r: Vec<i32> = v.iter().map(|x| x * 2).filter(|x| x > &4).collect();\n    println!("{r:?}");\n}',
      options: ["[6, 8]", "[2, 4, 6, 8]", "[4, 6, 8]", "[3, 4]"],
      answer: 0,
      explain:
        "Doubling gives 2, 4, 6, 8, then keeping only those greater than 4 leaves 6 and " +
        "8. Order matters enormously here: filtering before doubling would keep 3 and 4, " +
        "then double them to 6 and 8 as well, but for different reasons and with " +
        "different intermediate values.",
    },
    {
      q: "What makes a closure different from a function?",
      options: [
        "It can capture variables from the scope where it was written",
        "It is always faster because it is inlined",
        "It cannot take parameters",
        "It must be defined inside another function",
      ],
      answer: 0,
      explain:
        "Capturing the surrounding environment is the whole point, and it is why " +
        "closures pair so well with iterators: the closure can refer to things outside " +
        "the chain. How it captures, by reference or by move, is what the " +
        "<code>Fn</code>, <code>FnMut</code> and <code>FnOnce</code> traits describe.",
    },
  ],

  /* ---------------- Level 4 ---------------- */

  "15-smart-pointers": [
    {
      q: "When do you actually need <code>Box&lt;T&gt;</code>?",
      options: [
        "For recursive types, or when you want a trait object with a known size",
        "Whenever you want to put data on the heap for speed",
        "To share one value between several owners",
        "To make a value mutable from several places",
      ],
      answer: 0,
      explain:
        "A recursive type would be infinitely large without indirection, and " +
        "<code>Box</code> gives it a fixed size. It is also how you hold a " +
        "<code>dyn Trait</code>. Sharing is <code>Rc</code>'s job and interior " +
        "mutability is <code>RefCell</code>'s; boxing for speed is usually the opposite " +
        "of an optimisation.",
    },
    {
      q: "What does <code>Rc&lt;T&gt;</code> provide, and what is its limit?",
      options: [
        "Multiple owners of the same data, but it is not safe across threads",
        "Multiple mutable owners, safely, in any context",
        "A reference that can outlive its owner",
        "Shared ownership with automatic locking",
      ],
      answer: 0,
      explain:
        "<code>Rc</code> counts references and drops the value when the count hits zero. " +
        "Its counter is not synchronised, so it is single-threaded only, and the " +
        "compiler enforces that. Across threads you need <code>Arc</code>, which does " +
        "the same job with atomic counting and a small cost.",
    },
    {
      q: "What does <code>RefCell&lt;T&gt;</code> change about borrowing?",
      options: [
        "The rules are the same but checked at runtime, panicking if broken",
        "It removes the borrowing rules for that value",
        "It allows two mutable borrows at once",
        "It makes borrows thread-safe",
      ],
      answer: 0,
      explain:
        "The rules do not change; only the timing does. Break them and you get a panic " +
        "instead of a compile error, which is a real cost you accept when the compiler " +
        "cannot prove a pattern is fine. That is the whole trade of interior mutability.",
    },
  ],

  "16-concurrency": [
    {
      q: "What is \"fearless concurrency\" actually claiming?",
      options: [
        "The ownership rules make data races a compile error rather than a runtime bug",
        "Rust programs cannot deadlock",
        "Threads in Rust are faster than in other languages",
        "You never need locks in Rust",
      ],
      answer: 0,
      explain:
        "Data races, two threads touching the same data with at least one writing, are " +
        "caught at compile time by the same borrowing rules you already know. Note what " +
        "is not claimed: deadlocks are still entirely possible, and you very much still " +
        "need locks.",
    },
    {
      q: "Why does <code>thread::spawn</code> so often need a <code>move</code> closure?",
      options: [
        "The thread may outlive the current scope, so it must own what it uses",
        "move makes the closure run faster",
        "Threads cannot borrow anything at all",
        "It is required for all closures that take no arguments",
      ],
      answer: 0,
      explain:
        "The compiler cannot prove the spawning function will outlive the thread, so " +
        "borrowing would risk a dangling reference. <code>move</code> transfers " +
        "ownership into the closure, making the question moot. Scoped threads are the " +
        "modern way to borrow safely instead.",
    },
    {
      q: "Why is it <code>Arc&lt;Mutex&lt;T&gt;&gt;</code> and not <code>Mutex&lt;Arc&lt;T&gt;&gt;</code>?",
      options: [
        "Each thread needs its own handle to one shared lock protecting the data",
        "It is a convention; either order works",
        "Mutex cannot be the outer type",
        "Arc must always be innermost for atomic counting to work",
      ],
      answer: 0,
      explain:
        "You share the lock, and the lock protects the data. <code>Arc</code> outside " +
        "gives every thread a handle to the same <code>Mutex</code>. Reversed, each " +
        "thread would lock its own mutex around a shared pointer, which protects " +
        "nothing at all while looking like it does.",
    },
  ],

  "17-cargo": [
    {
      q: "What does <code>Cargo.lock</code> do that <code>Cargo.toml</code> does not?",
      options: [
        "Records the exact versions used, so every build resolves identically",
        "Lists which dependencies are allowed to be updated",
        "Stores the compiled output of your dependencies",
        "Locks the project so others cannot change dependencies",
      ],
      answer: 0,
      explain:
        "<code>Cargo.toml</code> states requirements like \"1.x\"; the lock file pins " +
        "exactly what was chosen. Commit it for applications so builds are reproducible. " +
        "For libraries the convention is usually not to, since the consuming application " +
        "does the resolving.",
    },
    {
      q: "Where do unit tests conventionally live in Rust?",
      options: [
        "In the same file as the code, in a #[cfg(test)] module",
        "In a separate tests/ directory only",
        "In a doc comment above each function",
        "In a file named test.rs at the project root",
      ],
      answer: 0,
      explain:
        "Unit tests sit beside the code they test, in a module marked " +
        "<code>#[cfg(test)]</code> so it is compiled only when testing. That gives them " +
        "access to private functions. The <code>tests/</code> directory is for " +
        "integration tests, which see only your public API.",
    },
  ],

  "18-strings": [
    {
      q: "Why can you not write <code>s[0]</code> on a <code>String</code>?",
      options: [
        "UTF-8 characters vary in byte length, so a byte index is not a character",
        "Strings are immutable so indexing is not allowed",
        "Because indexing is only defined for Vec",
        "Because it would be too slow",
      ],
      answer: 0,
      explain:
        "A byte index could land mid-character and produce nonsense, so Rust refuses " +
        "rather than pretending. Use <code>.chars().nth(0)</code> for a character, or " +
        "slice by a byte range you know is a boundary. Languages that allow the index " +
        "quietly break on any non-English text.",
    },
    {
      q: "What is the difference between <code>String</code> and <code>&str</code>?",
      options: [
        "String owns its text and can grow; &str is a borrowed view of some text",
        "String is UTF-8 and &str is ASCII",
        "&str is a newer replacement for String",
        "String is for variables and &str is for constants",
      ],
      answer: 0,
      explain:
        "Ownership again, in string form. <code>String</code> is a growable, owned " +
        "buffer; <code>&str</code> borrows a view of text owned by someone else, " +
        "including string literals. Take <code>&str</code> in function parameters so " +
        "callers can pass either.",
    },
    {
      q: "What does <code>\"héllo\".len()</code> return?",
      options: [
        "6, because len counts bytes and é takes two",
        "5, because there are five characters",
        "5, because Rust counts Unicode scalar values",
        "It will not compile without specifying an encoding",
      ],
      answer: 0,
      explain:
        "<code>len</code> is bytes, and <code>é</code> is two of them in UTF-8. For a " +
        "count of characters use <code>.chars().count()</code>, which is a different " +
        "and slower operation because it must walk the string. Being forced to choose is " +
        "the point.",
    },
  ],

  "19-patterns": [
    {
      q: "What does <code>let Some(x) = opt else { return; };</code> do?",
      options: [
        "Binds x if the pattern matches, otherwise runs the else block, which must diverge",
        "Assigns None to x if the option is empty",
        "Panics if opt is None",
        "Creates x only inside the else block",
      ],
      answer: 0,
      explain:
        "This is <code>let else</code>, and it is the tidiest way to handle the failure " +
        "case up front and keep the happy path unindented. The <code>else</code> block " +
        "must diverge, by returning, breaking or panicking, which is what guarantees " +
        "<code>x</code> is bound for the rest of the function.",
    },
    {
      q: "What is a match guard?",
      options: [
        "An extra if condition on an arm, checked after the pattern matches",
        "A way to stop a match from being exhaustive",
        "A check that the matched value is not null",
        "A pattern that matches several variants at once",
      ],
      answer: 0,
      explain:
        "A guard lets an arm depend on something patterns cannot express, like " +
        "<code>Some(n) if n &gt; 10</code>. One important subtlety: guards are invisible " +
        "to the exhaustiveness checker, so a guarded arm never counts as covering a " +
        "case.",
    },
  ],

  "20-errors-pro": [
    {
      q: "When should you reach for <code>anyhow</code> rather than <code>thiserror</code>?",
      options: [
        "In applications, where you mostly want context and a readable report",
        "In libraries, so callers get a rich error type",
        "Whenever you need error messages to be translated",
        "When performance matters, since anyhow is faster",
      ],
      answer: 0,
      explain:
        "The split is about who reads the error. An application wants to add context and " +
        "print something useful, which is <code>anyhow</code>. A library's callers want " +
        "to match on specific cases and decide, which needs the concrete typed errors " +
        "<code>thiserror</code> helps you write.",
    },
    {
      q: "What does <code>Box&lt;dyn Error&gt;</code> buy you, and what does it cost?",
      options: [
        "Any error type can be returned, but callers can no longer match on specifics",
        "Faster error propagation, at the cost of memory",
        "Automatic conversion between error types, with no downside",
        "Errors that can cross thread boundaries safely",
      ],
      answer: 0,
      explain:
        "It erases the type, so <code>?</code> accepts anything that implements " +
        "<code>Error</code>. Convenient in a <code>main</code> or a quick tool, and " +
        "unhelpful to a caller who wanted to handle a missing file differently from a " +
        "parse failure. That is exactly why libraries avoid it.",
    },
  ],

  "21-async": [
    {
      q: "Why does an async function do nothing until you await it?",
      options: [
        "It returns a Future, which is a description of work that has not started",
        "The runtime queues it and runs it a moment later",
        "Because async functions must be spawned to run",
        "Because the compiler optimises away unused calls",
      ],
      answer: 0,
      explain:
        "Calling an async function builds a <code>Future</code> and runs none of the " +
        "body. Something must poll it, which is what <code>await</code> or a spawn does. " +
        "This laziness is a deliberate design choice and the reason an un-awaited future " +
        "triggers a warning: you built the work and never did it.",
    },
    {
      q: "When are threads the better choice over async?",
      options: [
        "For CPU-bound work; async shines when you are mostly waiting on I/O",
        "Whenever you need more than one task, since async is single-threaded",
        "For anything involving files, since async only works on networks",
        "When you need tasks to share memory",
      ],
      answer: 0,
      explain:
        "Async is a way to wait on thousands of things cheaply. If your tasks are " +
        "computing rather than waiting, there is nothing to interleave and threads are " +
        "the right tool. Async runtimes are usually multi-threaded, and shared memory " +
        "works in both.",
    },
  ],

  "22-unsafe": [
    {
      q: "What does <code>unsafe</code> actually turn off?",
      options: [
        "Only a handful of extra abilities; the borrow checker still applies",
        "All of Rust's safety checks within the block",
        "The borrow checker, for that block only",
        "Runtime bounds checking on arrays",
      ],
      answer: 0,
      explain:
        "This is the most common misunderstanding. <code>unsafe</code> unlocks five " +
        "specific abilities, such as dereferencing raw pointers and calling unsafe " +
        "functions. Everything else, including the borrow checker, is fully in force. It " +
        "is not an escape hatch from Rust, it is a small, named set of extra powers.",
    },
    {
      q: "What is the point of wrapping unsafe code in a safe abstraction?",
      options: [
        "Callers cannot misuse it, and the unsafe reasoning is confined to a small area",
        "It makes the unsafe code run faster",
        "It is required by the compiler",
        "It lets you avoid writing safety comments",
      ],
      answer: 0,
      explain:
        "This is the pattern the whole standard library is built on: " +
        "<code>Vec</code> is full of unsafe code and its API cannot be misused. " +
        "Auditing becomes tractable because the dangerous reasoning lives in a few " +
        "small, heavily commented places rather than smeared across the codebase.",
    },
  ],

  "23-performance": [
    {
      q: "You benchmark your program and it is slow. What is the first thing to check?",
      options: [
        "That you built in release mode, not debug",
        "Whether you should replace Vec with an array",
        "Whether the clones can be removed",
        "Whether iterators are slower than loops here",
      ],
      answer: 0,
      explain:
        "Debug builds skip optimisation entirely and can be ten to a hundred times " +
        "slower. Benchmarking one is measuring nothing useful, and this catches people " +
        "constantly. <code>cargo run --release</code> first, then start thinking about " +
        "your code.",
    },
    {
      q: "What is a \"zero-cost abstraction\"?",
      options: [
        "A high-level construct that compiles to the same code a hand-written version would",
        "A feature that uses no memory",
        "Code that the compiler removes entirely",
        "An abstraction that is free to write but slow to run",
      ],
      answer: 0,
      explain:
        "Iterator chains compiling to the same machine code as a hand-rolled loop is the " +
        "canonical example. The promise is that you pay nothing extra for the readable " +
        "version. Worth verifying rather than trusting: the claim holds remarkably " +
        "often, and \"remarkably often\" is not \"always\".",
    },
    {
      q: "Why is guessing which line is slow such a bad habit?",
      options: [
        "Intuitions about performance are wrong often enough that measuring is the only reliable route",
        "Because all lines cost roughly the same",
        "Because the compiler reorders code, so line numbers are meaningless",
        "Because slowness is always caused by allocation",
      ],
      answer: 0,
      explain:
        "Experienced engineers guess wrong regularly, which is why profilers exist. " +
        "Optimising the wrong thing costs real time and often makes the code worse for " +
        "no gain. Measure, change one thing, measure again.",
    },
  ],
};
