"""Season 4: The Anomaly.

Objects, traits, errors, iterators. Ops, Science and Tactical. This is
where the checkers stop being tables: shields have state, iterators are
lazy, errors have names, and versions must sort numerically.
"""

from .helpers import _m, py_cases, py_custom, rs_cases, rs_custom

# -------------------------------------------------------------- 25
_m(
    season=4, num=25, slug="25-shield-generator", id="bridge-s4m25", station="ops",
    title="The Shield Generator", stardate="Stardate 55143.0",
    crew=["tkala", "raghunathan"],
    blurb="The shields need to remember how charged they are. Right now every hit "
          "is the first hit.",
    briefing="""
<p>Commander Raghunathan is back, with a copy of the other ship's computer, and the
first thing she wants is our own shields to work properly before anyone reads it. The
shield routine has no memory: every hit is treated as the first, so the display reads
"98%" after ninety hits.</p>

<p>Chief T'Kala wants a shield generator that <em>knows</em> its charge. It takes hits,
which reduce it but never below zero. It recharges, but never past capacity. It reports
a whole-number percentage, rounded down, and it can say plainly whether it is down.
Four small behaviours, one object, and a memory.</p>
""",
    debrief="""
<p>The shields remember. After ninety hits they read 10%, which is honest, and after a
recharge they read 100% and not 140%, which is progress. Commander Raghunathan has put
the other computer's core on the science bench and has not yet turned it on.</p>
""",
    objectives=[
        "A new generator starts at full charge, 100%",
        "A hit reduces the charge; two hits reduce it twice",
        "Charge never drops below zero, and is_down reports it",
        "Recharging never exceeds capacity",
        "Percent is a whole number, rounded down",
    ],
    hint="Store the capacity and the current charge as attributes. <code>hit</code> "
         "subtracts and clamps at 0; <code>recharge</code> adds and clamps at capacity; "
         "<code>percent</code> is charge times 100, integer-divided by capacity.",
    py_spec="""
<p>Write a class <code>Shields</code>:</p>
<ul>
  <li><code>Shields(capacity)</code> starts fully charged.</li>
  <li><code>.hit(damage)</code> reduces the charge, never below 0.</li>
  <li><code>.recharge(amount)</code> increases it, never above capacity.</li>
  <li><code>.percent()</code> returns the charge as a whole-number percentage of
    capacity, rounded down.</li>
  <li><code>.is_down()</code> returns <code>True</code> when the charge is 0.</li>
</ul>
""",
    py_stub='''class Shields:
    """A shield generator that remembers its charge."""

    def __init__(self, capacity):
        # TODO
        pass

    def hit(self, damage):
        # TODO
        pass

    def recharge(self, amount):
        # TODO
        pass

    def percent(self):
        # TODO
        return 100

    def is_down(self):
        # TODO
        return False
''',
    py_reference='''class Shields:
    """A shield generator that remembers its charge."""

    def __init__(self, capacity):
        self.capacity = capacity
        self.charge = capacity

    def hit(self, damage):
        self.charge = max(0, self.charge - damage)

    def recharge(self, amount):
        self.charge = min(self.capacity, self.charge + amount)

    def percent(self):
        return (self.charge * 100) // self.capacity

    def is_down(self):
        return self.charge == 0
''',
    py_checker=py_custom('''
def _t0():
    s = Shields(1000)
    return s.percent()
_g = _guard(0, _t0, "Shields(1000).percent()")
if _g is not _FAILED:
    _report(0, _g == 100, f"new generator reads {_g}%, wanted 100")

def _t1():
    s = Shields(1000)
    s.hit(250)
    a = s.percent()
    s.hit(250)
    return a, s.percent()
_g = _guard(1, _t1, "two hits of 250")
if _g is not _FAILED:
    _report(1, _g == (75, 50), f"after one hit {_g[0]}%, after two {_g[1]}%, wanted 75 and 50")

def _t2():
    s = Shields(100)
    s.hit(150)
    return s.percent(), s.is_down()
_g = _guard(2, _t2, "hit for more than the charge")
if _g is not _FAILED:
    _report(2, _g == (0, True), f"percent {_g[0]}, is_down {_g[1]}, wanted 0 and True")

def _t3():
    s = Shields(100)
    s.hit(30)
    s.recharge(500)
    return s.percent()
_g = _guard(3, _t3, "recharge past capacity")
if _g is not _FAILED:
    _report(3, _g == 100, f"after over-recharge reads {_g}%, wanted 100")

def _t4():
    s = Shields(300)
    s.hit(100)
    return s.percent()
_g = _guard(4, _t4, "Shields(300) after a hit of 100")
if _g is not _FAILED:
    _report(4, _g == 66 and isinstance(_g, int), f"reads {_g!r}, wanted 66 (an int, rounded down)")
'''),
    rs_spec="""
<p>Write a struct <code>Shields</code> with:</p>
<ul>
  <li><code>Shields::new(capacity: u32) -&gt; Shields</code>, fully charged.</li>
  <li><code>fn hit(&amp;mut self, damage: u32)</code>: reduce the charge, never below 0.</li>
  <li><code>fn recharge(&amp;mut self, amount: u32)</code>: increase it, never above capacity.</li>
  <li><code>fn percent(&amp;self) -&gt; u32</code>: charge as a whole-number percentage,
    rounded down.</li>
  <li><code>fn is_down(&amp;self) -&gt; bool</code>: true when the charge is 0.</li>
</ul>
""",
    rs_stub='''/// A shield generator that remembers its charge.
struct Shields {
    // TODO: fields
}

impl Shields {
    fn new(capacity: u32) -> Shields {
        // TODO
        Shields {}
    }
    fn hit(&mut self, damage: u32) {
        // TODO
    }
    fn recharge(&mut self, amount: u32) {
        // TODO
    }
    fn percent(&self) -> u32 {
        // TODO
        100
    }
    fn is_down(&self) -> bool {
        // TODO
        false
    }
}
''',
    rs_reference='''/// A shield generator that remembers its charge.
struct Shields {
    capacity: u32,
    charge: u32,
}

impl Shields {
    fn new(capacity: u32) -> Shields {
        Shields { capacity, charge: capacity }
    }
    fn hit(&mut self, damage: u32) {
        self.charge = self.charge.saturating_sub(damage);
    }
    fn recharge(&mut self, amount: u32) {
        self.charge = (self.charge + amount).min(self.capacity);
    }
    fn percent(&self) -> u32 {
        self.charge * 100 / self.capacity
    }
    fn is_down(&self) -> bool {
        self.charge == 0
    }
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let r = std::panic::catch_unwind(|| { let s = Shields::new(1000); s.percent() });
    match r { Ok(p) => __report(0, p == 100, format!("new generator reads {}%, wanted 100", p)),
              Err(_) => __report(0, false, "panicked".into()) }

    let r = std::panic::catch_unwind(|| { let mut s = Shields::new(1000); s.hit(250); let a = s.percent(); s.hit(250); (a, s.percent()) });
    match r { Ok(p) => __report(1, p == (75, 50), format!("after one hit {}%, after two {}%, wanted 75 and 50", p.0, p.1)),
              Err(_) => __report(1, false, "panicked".into()) }

    let r = std::panic::catch_unwind(|| { let mut s = Shields::new(100); s.hit(150); (s.percent(), s.is_down()) });
    match r { Ok(p) => __report(2, p == (0, true), format!("percent {}, is_down {}, wanted 0 and true", p.0, p.1)),
              Err(_) => __report(2, false, "hit for more than the charge panicked (u32 underflow?)".into()) }

    let r = std::panic::catch_unwind(|| { let mut s = Shields::new(100); s.hit(30); s.recharge(500); s.percent() });
    match r { Ok(p) => __report(3, p == 100, format!("after over-recharge reads {}%, wanted 100", p)),
              Err(_) => __report(3, false, "panicked".into()) }

    let r = std::panic::catch_unwind(|| { let mut s = Shields::new(300); s.hit(100); s.percent() });
    match r { Ok(p) => __report(4, p == 66, format!("reads {}%, wanted 66 (rounded down)", p)),
              Err(_) => __report(4, false, "panicked".into()) }
}
'''),
)

# -------------------------------------------------------------- 26
_m(
    season=4, num=26, slug="26-anomaly-readings", id="bridge-s4m26", station="science",
    title="Readings, One at a Time", stardate="Stardate 55144.4",
    crew=["skree"],
    blurb="The other ship's sensor log is enormous. Lt. Skree wants to read it one "
          "value at a time, not load it all and hope.",
    briefing="""
<p>The other Magnanimous kept everything. Its sensor log is nineteen years long and Lt.
Skree does not want it in memory all at once; Skree wants to walk it, one reading at a
time, stopping whenever the pattern shows up.</p>

<p>Build a sequence that produces readings on demand: a start value, a step, and a count.
It should hand out one value when asked and not before, so that asking for the first
three of a million costs three. Skree describes this as "the difference between reading
a book and being hit with it".</p>
""",
    debrief="""
<p>Skree is walking the other ship's log. So far it is identical to ours, entry for
entry, up to a stardate nineteen years ago. Skree has asked for the next reading. Then
the next. Skree has stopped saying "hm" and started writing things down.</p>
""",
    objectives=[
        "Produces start, start+step, ... for exactly count values",
        "A count of zero produces nothing",
        "It is lazy: values come one at a time on demand, not as a prebuilt list",
        "The first three of a million cost three",
        "It composes: the values can be doubled with a standard adaptor",
    ],
    hint="Python: <code>yield</code> inside a loop makes a generator, and generators are "
         "lazy by nature. Rust: a struct holding <code>current</code>, <code>step</code> "
         "and <code>remaining</code>, and <code>impl Iterator</code> with a "
         "<code>next</code> that returns <code>None</code> when nothing remains.",
    py_spec="""
<p>Write <code>readings(start, step, count)</code> as a <strong>generator</strong>: it
yields <code>start</code>, then <code>start + step</code>, and so on, for exactly
<code>count</code> values. It must be lazy: a generator object, not a list.</p>
""",
    py_stub='''def readings(start, step, count):
    """Yield count values: start, start+step, start+2*step, ..."""
    # TODO: this builds the whole list up front, which is the problem.
    return [start + i * step for i in range(count)]
''',
    py_reference='''def readings(start, step, count):
    """Yield count values: start, start+step, start+2*step, ..."""
    value = start
    for _ in range(count):
        yield value
        value += step
''',
    py_checker=py_custom('''
import inspect, itertools, time

_g = _guard(0, lambda: list(readings(10, 5, 4)), "list(readings(10, 5, 4))")
if _g is not _FAILED:
    _report(0, _g == [10, 15, 20, 25], f"got {_short(_g)}, wanted [10, 15, 20, 25]")

_g = _guard(1, lambda: list(readings(3, 1, 0)), "list(readings(3, 1, 0))")
if _g is not _FAILED:
    _report(1, _g == [], f"got {_short(_g)}, wanted []")

_g = _guard(2, lambda: readings(0, 1, 5), "readings(0, 1, 5)")
if _g is not _FAILED:
    _report(2, inspect.isgenerator(_g), f"readings(...) returned a {type(_g).__name__}, wanted a generator")

def _t3():
    t = time.time()
    first = list(itertools.islice(readings(0, 2, 1_000_000), 3))
    return first, time.time() - t
_g = _guard(3, _t3, "first three of a million")
if _g is not _FAILED:
    _report(3, _g[0] == [0, 2, 4] and _g[1] < 0.5, f"got {_short(_g[0])} in {_g[1]:.3f}s, wanted [0, 2, 4] quickly")

_g = _guard(4, lambda: list(map(lambda x: x * 2, readings(1, 1, 3))), "map(double, readings(1, 1, 3))")
if _g is not _FAILED:
    _report(4, _g == [2, 4, 6], f"got {_short(_g)}, wanted [2, 4, 6]")
'''),
    rs_spec="""
<p>Keep the struct as given and implement <code>Iterator</code> for it, so that
<code>Readings::new(start, step, count)</code> yields <code>start</code>, then
<code>start + step</code>, and so on, for exactly <code>count</code> values, then
<code>None</code>. Because it is a real iterator, <code>.take()</code>, <code>.map()</code>
and <code>.collect()</code> all work on it for free.</p>
""",
    rs_stub='''/// A lazy sequence of readings: start, start+step, ... for `count` values.
struct Readings {
    current: i64,
    step: i64,
    remaining: usize,
}

impl Readings {
    fn new(start: i64, step: i64, count: usize) -> Readings {
        Readings { current: start, step, remaining: count }
    }
}

impl Iterator for Readings {
    type Item = i64;
    fn next(&mut self) -> Option<i64> {
        // TODO: hand out one value, advance, and stop when nothing remains.
        None
    }
}
''',
    rs_reference='''/// A lazy sequence of readings: start, start+step, ... for `count` values.
struct Readings {
    current: i64,
    step: i64,
    remaining: usize,
}

impl Readings {
    fn new(start: i64, step: i64, count: usize) -> Readings {
        Readings { current: start, step, remaining: count }
    }
}

impl Iterator for Readings {
    type Item = i64;
    fn next(&mut self) -> Option<i64> {
        if self.remaining == 0 {
            return None;
        }
        let value = self.current;
        self.current += self.step;
        self.remaining -= 1;
        Some(value)
    }
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let got: Vec<i64> = Readings::new(10, 5, 4).collect();
    __report(0, got == vec![10, 15, 20, 25], format!("collect() gave {:?}, wanted [10, 15, 20, 25]", got));

    let got: Vec<i64> = Readings::new(3, 1, 0).collect();
    __report(1, got.is_empty(), format!("count 0 gave {:?}, wanted []", got));

    let mut it = Readings::new(0, 1, 5);
    let a = it.next(); let b = it.next();
    __report(2, a == Some(0) && b == Some(1), format!("next() twice gave {:?} then {:?}, wanted Some(0) then Some(1)", a, b));

    let t = std::time::Instant::now();
    let first: Vec<i64> = Readings::new(0, 2, 1_000_000).take(3).collect();
    let el = t.elapsed();
    __report(3, first == vec![0, 2, 4] && el.as_millis() < 500, format!("take(3) of a million gave {:?} in {:?}", first, el));

    let got: Vec<i64> = Readings::new(1, 1, 3).map(|x| x * 2).collect();
    __report(4, got == vec![2, 4, 6], format!("map(x*2) gave {:?}, wanted [2, 4, 6]", got));
}
'''),
)

# -------------------------------------------------------------- 27
_m(
    season=4, num=27, slug="27-errors-with-names", id="bridge-s4m27", station="tactical",
    title="Errors With Names", stardate="Stardate 55146.1",
    crew=["tkala", "tannenbaum"],
    blurb="'Something went wrong' is not an error message. Chief T'Kala wants "
          "failures that say what failed.",
    briefing="""
<p>Since the heading validator went in, the helm has been refusing bad input, which is
correct, and reporting every refusal as <em>"something went wrong"</em>, which is not.
Ensign Tannenbaum typed <em>"north"</em> and 720 and got the same message for both, and
has pointed out, not unreasonably, that he cannot learn from that.</p>

<p>Chief T'Kala wants errors with names. Not a number: an out-of-range heading. Two
different failures, two different errors, each carrying the thing that was wrong with it,
so the message can say <em>"720 is not a heading"</em> and mean it. In Python that is
your own exception class. In Rust it is an enum, and the compiler will make sure every
caller handles both.</p>
""",
    debrief="""
<p>"north is not a number." "720 is out of range." Ensign Tannenbaum has read both
messages and understood both messages, and has typed 180, which worked. Chief T'Kala has
made a small note in her list and moved on to item two.</p>
""",
    objectives=[
        "A valid heading is accepted and returned as a number",
        "Text that is not a number raises the named error, carrying the text",
        "A number out of range raises the named error, carrying the number",
        "The error is a specific type, distinguishable from any other failure",
        "Whitespace around a valid heading is fine",
    ],
    hint="Python: define <code>class HeadingError(ValueError)</code>, and raise it with a "
         "message that includes the offending value. Rust: an enum with two variants "
         "holding data, <code>NotANumber(String)</code> and <code>OutOfRange(i64)</code>, "
         "returned in <code>Err</code>.",
    py_spec="""
<p>Define <code>class HeadingError(ValueError)</code>. Write
<code>set_heading(text)</code>: return the heading as an <code>int</code> if
<code>text</code> is a whole number 0 to 359 (whitespace allowed). Otherwise raise
<code>HeadingError</code> whose message contains the offending text or number, for
example <code>"north is not a number"</code> or <code>"720 is out of range"</code>.</p>
""",
    py_stub='''class HeadingError(ValueError):
    """Raised for a heading that is not a number, or is out of range."""


def set_heading(text):
    """Return the heading 0..359, or raise HeadingError saying what was wrong."""
    # TODO
    raise Exception("something went wrong")
''',
    py_reference='''class HeadingError(ValueError):
    """Raised for a heading that is not a number, or is out of range."""


def set_heading(text):
    """Return the heading 0..359, or raise HeadingError saying what was wrong."""
    stripped = text.strip()
    try:
        heading = int(stripped)
    except ValueError:
        raise HeadingError(f"{stripped} is not a number")
    if not 0 <= heading <= 359:
        raise HeadingError(f"{heading} is out of range")
    return heading
''',
    py_checker=py_custom('''
_g = _guard(0, lambda: set_heading("180"), "set_heading('180')")
if _g is not _FAILED:
    _report(0, _g == 180, f"returned {_g!r}, wanted 180")

def _t1():
    try:
        set_heading("north")
    except HeadingError as e:
        return ("HeadingError", str(e))
    except Exception as e:
        return (type(e).__name__, str(e))
    return ("no error", "")
_g = _guard(1, _t1, "set_heading('north')")
if _g is not _FAILED:
    _report(1, _g[0] == "HeadingError" and "north" in _g[1], f"raised {_g[0]}: {_g[1]!r}, wanted HeadingError mentioning 'north'")

def _t2():
    try:
        set_heading("720")
    except HeadingError as e:
        return ("HeadingError", str(e))
    except Exception as e:
        return (type(e).__name__, str(e))
    return ("no error", "")
_g = _guard(2, _t2, "set_heading('720')")
if _g is not _FAILED:
    _report(2, _g[0] == "HeadingError" and "720" in _g[1], f"raised {_g[0]}: {_g[1]!r}, wanted HeadingError mentioning 720")

_g = _guard(3, lambda: issubclass(HeadingError, ValueError) and HeadingError is not ValueError, "HeadingError type")
if _g is not _FAILED:
    _report(3, _g, "HeadingError should be its own subclass of ValueError")

_g = _guard(4, lambda: set_heading("  45 "), "set_heading('  45 ')")
if _g is not _FAILED:
    _report(4, _g == 45, f"returned {_g!r}, wanted 45")
'''),
    rs_spec="""
<p>Keep the enum as given. Write <code>set_heading(text: &amp;str) -&gt; Result&lt;u16,
HeadingError&gt;</code>: <code>Ok(heading)</code> if <code>text</code> is a whole number
0 to 359 (whitespace allowed); <code>Err(HeadingError::NotANumber(text))</code> if it
does not parse as an integer; <code>Err(HeadingError::OutOfRange(n))</code> if it
parses but is outside 0 to 359.</p>
""",
    rs_stub='''#[derive(Debug, PartialEq)]
enum HeadingError {
    NotANumber(String),
    OutOfRange(i64),
}

/// Ok(heading) for 0..=359, or an error that says what was wrong.
fn set_heading(text: &str) -> Result<u16, HeadingError> {
    // TODO
    Err(HeadingError::NotANumber(String::from("something went wrong")))
}
''',
    rs_reference='''#[derive(Debug, PartialEq)]
enum HeadingError {
    NotANumber(String),
    OutOfRange(i64),
}

/// Ok(heading) for 0..=359, or an error that says what was wrong.
fn set_heading(text: &str) -> Result<u16, HeadingError> {
    let stripped = text.trim();
    let n: i64 = stripped
        .parse()
        .map_err(|_| HeadingError::NotANumber(stripped.to_string()))?;
    if !(0..=359).contains(&n) {
        return Err(HeadingError::OutOfRange(n));
    }
    Ok(n as u16)
}
''',
    rs_checker=rs_cases("set_heading", [
        (['"180"'], "Ok(180)"),
        (['"north"'], 'Err(HeadingError::NotANumber("north".to_string()))'),
        (['"720"'], "Err(HeadingError::OutOfRange(720))"),
        (['"-1"'], "Err(HeadingError::OutOfRange(-1))"),
        (['"  45 "'], "Ok(45)"),
    ]),
)

# -------------------------------------------------------------- 28
_m(
    season=4, num=28, slug="28-top-readings", id="bridge-s4m28", station="science",
    title="The Loudest Three", stardate="Stardate 55147.7",
    crew=["skree", "dubois"],
    blurb="A million readings, and Lt. Skree wants the biggest few, largest first, "
          "without breaking a sweat.",
    briefing="""
<p>The pattern in the other ship's log is a set of spikes. Lt. Skree wants the largest
few readings from any stretch of the log, largest first, and wants the request to be
one expression, because Skree has been reading about iterator chains and has decided
they are "the correct shape for thoughts".</p>

<p>The Captain, passing, asked whether the spikes were dangerous. Skree said they were
"nineteen years old". The Captain said that was not an answer. Skree agreed that it was
not, and went back to the console.</p>
""",
    debrief="""
<p>Three spikes, on three consecutive stardates, each larger than the last, ending the
day before the log stops. Skree has put the numbers next to ours. Ours has the first
spike. Today. Skree has asked the Captain to come back to the console.</p>
""",
    objectives=[
        "The three largest, largest first",
        "Ties are kept, not collapsed",
        "Fewer readings than asked for: all of them, largest first",
        "Asking for zero gives nothing",
        "The input is not modified",
    ],
    hint="Sort a <em>copy</em> in descending order and take the first n. Python: "
         "<code>sorted(readings, reverse=True)[:n]</code>. Rust: clone into a Vec, "
         "<code>sort_unstable_by(|a, b| b.cmp(a))</code>, <code>truncate(n)</code>. "
         "The last objective is why it must be a copy.",
    py_spec="""
<p>Write <code>top_n(readings, n)</code>: return a new list of the <code>n</code> largest
readings in descending order. If there are fewer than <code>n</code>, return all of them
sorted descending. Do not modify <code>readings</code>.</p>
""",
    py_stub='''def top_n(readings, n):
    """The n largest readings, largest first. Do not modify the input."""
    # TODO
    readings.sort(reverse=True)
    return readings[:n]
''',
    py_reference='''def top_n(readings, n):
    """The n largest readings, largest first. Do not modify the input."""
    return sorted(readings, reverse=True)[:n]
''',
    py_checker=py_custom('''
_g = _guard(0, lambda: top_n([4, 91, 7, 63, 88, 12], 3), "top_n([4, 91, 7, 63, 88, 12], 3)")
if _g is not _FAILED:
    _report(0, _g == [91, 88, 63], f"got {_short(_g)}, wanted [91, 88, 63]")

_g = _guard(1, lambda: top_n([5, 9, 9, 2, 9], 3), "top_n([5, 9, 9, 2, 9], 3)")
if _g is not _FAILED:
    _report(1, _g == [9, 9, 9], f"got {_short(_g)}, wanted [9, 9, 9]")

_g = _guard(2, lambda: top_n([3, 1, 2], 10), "top_n([3, 1, 2], 10)")
if _g is not _FAILED:
    _report(2, _g == [3, 2, 1], f"got {_short(_g)}, wanted [3, 2, 1]")

_g = _guard(3, lambda: top_n([3, 1, 2], 0), "top_n([3, 1, 2], 0)")
if _g is not _FAILED:
    _report(3, _g == [], f"got {_short(_g)}, wanted []")

def _t4():
    data = [4, 91, 7]
    top_n(data, 2)
    return data
_g = _guard(4, _t4, "input after top_n")
if _g is not _FAILED:
    _report(4, _g == [4, 91, 7], f"input is now {_short(_g)}, wanted it unchanged as [4, 91, 7]")
'''),
    rs_spec="""
<p>Write <code>top_n(readings: &amp;[i32], n: usize) -&gt; Vec&lt;i32&gt;</code>: the
<code>n</code> largest readings in descending order. If there are fewer than
<code>n</code>, all of them sorted descending. The input slice is borrowed, so it cannot
be modified; that objective is one Rust checks for you.</p>
""",
    rs_stub='''/// The n largest readings, largest first.
fn top_n(readings: &[i32], n: usize) -> Vec<i32> {
    // TODO
    readings.iter().copied().take(n).collect()
}
''',
    rs_reference='''/// The n largest readings, largest first.
fn top_n(readings: &[i32], n: usize) -> Vec<i32> {
    let mut v = readings.to_vec();
    v.sort_unstable_by(|a, b| b.cmp(a));
    v.truncate(n);
    v
}
''',
    rs_checker=rs_cases("top_n", [
        (["&[4, 91, 7, 63, 88, 12]", "3"], "vec![91, 88, 63]"),
        (["&[5, 9, 9, 2, 9]", "3"], "vec![9, 9, 9]"),
        (["&[3, 1, 2]", "10"], "vec![3, 2, 1]"),
        (["&[3, 1, 2]", "0"], "Vec::<i32>::new()"),
        (["&[-5, -1, -9]", "2"], "vec![-1, -5]"),
    ]),
)

# -------------------------------------------------------------- 29
_m(
    season=4, num=29, slug="29-cargo-priorities", id="bridge-s4m29", station="ops",
    title="Cargo Priorities", stardate="Stardate 55149.2",
    crew=["tkala", "raghunathan"],
    blurb="If we have to abandon ship, what goes on the shuttles first? Priority "
          "first, then the light stuff, and no arguing.",
    briefing="""
<p>Nobody has said the words "abandon ship". Chief T'Kala has, however, asked for the
cargo loading order to be worked out "as an exercise", and Commander Raghunathan has
asked for it "today", and neither of them is making eye contact with the other.</p>

<p>Each crate has a name, a priority from 1 to 5, and a mass. Load the highest priority
first. Among equal priorities, load the lightest first, so more of it fits. The result is
just the names, in loading order. It is a sort with two keys, and the second key runs
the opposite way to the first, which is the bit that catches people.</p>
""",
    debrief="""
<p>Medical first, then the light priority-fours, then everything else. Chief T'Kala has
printed the list and put it in the pocket of her jacket. She has not said why. Gerald is
priority five, mass four, and loads second.</p>
""",
    objectives=[
        "Higher priority loads before lower",
        "Equal priority: lighter loads first",
        "Both rules together on a mixed manifest",
        "A single crate",
        "An empty manifest",
    ],
    hint="Sort by a compound key. Python: <code>key=lambda c: (-c['priority'], "
         "c['mass'])</code>, negating the priority so it runs descending. Rust: "
         "<code>sort_by(|a, b| b.priority.cmp(&amp;a.priority).then(a.mass.cmp(&amp;b.mass)))</code>.",
    py_spec="""
<p>Write <code>loading_order(crates)</code>: <code>crates</code> is a list of dicts with
keys <code>"name"</code>, <code>"priority"</code> (higher loads first) and
<code>"mass"</code> (among equal priorities, lighter loads first). Return the list of
names in loading order.</p>
""",
    py_stub='''def loading_order(crates):
    """Names in loading order: priority descending, then mass ascending."""
    # TODO
    return [c["name"] for c in crates]
''',
    py_reference='''def loading_order(crates):
    """Names in loading order: priority descending, then mass ascending."""
    ordered = sorted(crates, key=lambda c: (-c["priority"], c["mass"]))
    return [c["name"] for c in ordered]
''',
    py_checker=py_cases("loading_order", [
        (([{"name": "spares", "priority": 2, "mass": 50}, {"name": "medical", "priority": 5, "mass": 80}],), ["medical", "spares"]),
        (([{"name": "water", "priority": 4, "mass": 300}, {"name": "rations", "priority": 4, "mass": 120}],), ["rations", "water"]),
        (([{"name": "spares", "priority": 2, "mass": 50}, {"name": "water", "priority": 4, "mass": 300},
           {"name": "medical", "priority": 5, "mass": 80}, {"name": "gerald", "priority": 5, "mass": 4},
           {"name": "rations", "priority": 4, "mass": 120}],), ["gerald", "medical", "rations", "water", "spares"]),
        (([{"name": "torch", "priority": 1, "mass": 1}],), ["torch"]),
        (([],), []),
    ]),
    rs_spec="""
<p>Keep the struct as given. Write <code>loading_order(crates: &amp;[Crate]) -&gt;
Vec&lt;String&gt;</code>: names in loading order, priority descending, and among equal
priorities mass ascending.</p>
""",
    rs_stub='''#[derive(Debug, Clone)]
struct Crate {
    name: String,
    priority: u8,
    mass: u32,
}

/// Names in loading order: priority descending, then mass ascending.
fn loading_order(crates: &[Crate]) -> Vec<String> {
    // TODO
    crates.iter().map(|c| c.name.clone()).collect()
}
''',
    rs_reference='''#[derive(Debug, Clone)]
struct Crate {
    name: String,
    priority: u8,
    mass: u32,
}

/// Names in loading order: priority descending, then mass ascending.
fn loading_order(crates: &[Crate]) -> Vec<String> {
    let mut v = crates.to_vec();
    v.sort_by(|a, b| b.priority.cmp(&a.priority).then(a.mass.cmp(&b.mass)));
    v.into_iter().map(|c| c.name).collect()
}
''',
    rs_checker=rs_custom('''
fn c(name: &str, priority: u8, mass: u32) -> Crate {
    Crate { name: name.to_string(), priority, mass }
}
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let got = loading_order(&[c("spares", 2, 50), c("medical", 5, 80)]);
    __report(0, got == vec!["medical", "spares"], format!("got {:?}, wanted [medical, spares]", got));

    let got = loading_order(&[c("water", 4, 300), c("rations", 4, 120)]);
    __report(1, got == vec!["rations", "water"], format!("got {:?}, wanted [rations, water]", got));

    let got = loading_order(&[c("spares", 2, 50), c("water", 4, 300), c("medical", 5, 80), c("gerald", 5, 4), c("rations", 4, 120)]);
    __report(2, got == vec!["gerald", "medical", "rations", "water", "spares"], format!("got {:?}, wanted [gerald, medical, rations, water, spares]", got));

    let got = loading_order(&[c("torch", 1, 1)]);
    __report(3, got == vec!["torch"], format!("got {:?}, wanted [torch]", got));

    let got = loading_order(&[]);
    __report(4, got.is_empty(), format!("got {:?}, wanted []", got));
}
'''),
)

# -------------------------------------------------------------- 30
_m(
    season=4, num=30, slug="30-access-code", id="bridge-s4m30", station="tactical",
    title="The Access Code", stardate="Stardate 55150.8",
    crew=["tkala", "raghunathan", "tannenbaum"],
    blurb="The other ship's core wants an access code. Chief T'Kala wants every "
          "reason a proposed code is weak, not just the first.",
    briefing="""
<p>The other computer will talk, but it wants an access code set first, and Chief T'Kala
has rules for codes. At least eight characters. At least one digit. At least one upper
case letter. No spaces. Ensign Tannenbaum's first proposal was <em>"pass"</em>, which
breaks three of them, and the Chief wants him told about all three at once rather than
one at a time across three attempts.</p>

<p>So this checker does not stop at the first problem. It collects every rule the code
breaks, in the order the rules are listed, and returns them. A code that breaks nothing
returns an empty list, which is how you know it is good. Compare this with the
transporter check from last season, which stopped at the first refusal; both shapes are
right for different jobs.</p>
""",
    debrief="""
<p>Ensign Tannenbaum's fourth proposal passed. It is not <em>"Password1"</em>, because
Chief T'Kala added a fifth rule on the spot for that. The other computer has accepted
the code and asked, in text, whether "the technician" is still aboard. Commander
Raghunathan has typed yes.</p>
""",
    objectives=[
        "A good code returns no problems",
        "Too short is reported",
        "Several problems are all reported, in rule order",
        "A space anywhere is reported",
        "Exactly eight characters is long enough",
    ],
    hint="Start with an empty list, test each rule in order, and append the message "
         "when a rule fails. Return the list. Do not return early; that is the whole "
         "difference from last season's transporter check.",
    py_spec="""
<p>Write <code>code_problems(code)</code>: return a list of the rules the code breaks,
in this order, using these exact strings: <code>"too short"</code> (fewer than 8
characters), <code>"needs a digit"</code>, <code>"needs an upper case letter"</code>,
<code>"contains a space"</code>. A code that breaks nothing returns <code>[]</code>.</p>
""",
    py_stub='''def code_problems(code):
    """Every rule the code breaks, in order. Empty list means it is fine."""
    # TODO
    if len(code) < 8:
        return ["too short"]
    return []
''',
    py_reference='''def code_problems(code):
    """Every rule the code breaks, in order. Empty list means it is fine."""
    problems = []
    if len(code) < 8:
        problems.append("too short")
    if not any(ch.isdigit() for ch in code):
        problems.append("needs a digit")
    if not any(ch.isupper() for ch in code):
        problems.append("needs an upper case letter")
    if " " in code:
        problems.append("contains a space")
    return problems
''',
    py_checker=py_cases("code_problems", [
        (("Magnanim0us",), []),
        (("Ab1",), ["too short"]),
        (("pass",), ["too short", "needs a digit", "needs an upper case letter"]),
        (("Open Sesame 1",), ["contains a space"]),
        (("Gerald99",), []),
    ]),
    rs_spec="""
<p>Write <code>code_problems(code: &amp;str) -&gt; Vec&lt;&amp;'static str&gt;</code>: the
rules the code breaks, in this order, using these exact strings: <code>"too short"</code>
(fewer than 8 characters), <code>"needs a digit"</code>, <code>"needs an upper case
letter"</code>, <code>"contains a space"</code>. A code that breaks nothing returns an
empty vector.</p>
""",
    rs_stub='''/// Every rule the code breaks, in order. Empty means it is fine.
fn code_problems(code: &str) -> Vec<&'static str> {
    // TODO
    if code.chars().count() < 8 { vec!["too short"] } else { vec![] }
}
''',
    rs_reference='''/// Every rule the code breaks, in order. Empty means it is fine.
fn code_problems(code: &str) -> Vec<&'static str> {
    let mut problems = Vec::new();
    if code.chars().count() < 8 {
        problems.push("too short");
    }
    if !code.chars().any(|c| c.is_ascii_digit()) {
        problems.push("needs a digit");
    }
    if !code.chars().any(|c| c.is_uppercase()) {
        problems.push("needs an upper case letter");
    }
    if code.contains(' ') {
        problems.push("contains a space");
    }
    problems
}
''',
    rs_checker=rs_cases("code_problems", [
        (['"Magnanim0us"'], "Vec::<&str>::new()"),
        (['"Ab1"'], 'vec!["too short"]'),
        (['"pass"'], 'vec!["too short", "needs a digit", "needs an upper case letter"]'),
        (['"Open Sesame 1"'], 'vec!["contains a space"]'),
        (['"Gerald99"'], "Vec::<&str>::new()"),
    ]),
)

# -------------------------------------------------------------- 31
_m(
    season=4, num=31, slug="31-signal-compression", id="bridge-s4m31", station="science",
    title="Signal Compression", stardate="Stardate 55152.4",
    crew=["skree", "raghunathan"],
    blurb="The spikes are a message, and the message is repetitive. Lt. Skree wants "
          "it compressed so the shape shows.",
    briefing="""
<p>The spikes in both logs, ours and theirs, are a message. It is long and mostly
repetition, and Lt. Skree wants it run-length encoded so the structure is visible:
<em>"aaabcc"</em> becomes <em>"a3b1c2"</em>, each character followed by how many times it
repeats in a row.</p>

<p>Commander Raghunathan looked at the first compressed line and did not say anything.
Skree asked whether the compression was wrong. The Commander said it was right, and that
was the trouble.</p>
""",
    debrief="""
<p>Compressed, the message is nineteen characters long. It is a stardate, and it is
tomorrow's. Beneath it, in both logs, is a second line that Skree has compressed to
<em>"n1o1t1 1y1e1t1"</em>. Skree has read this aloud. Nobody on the bridge has said
anything for some time.</p>
""",
    objectives=[
        "Runs of repeated characters are counted",
        "A single character has a count of one",
        "Runs longer than nine digits correctly",
        "Non-letters and spaces are encoded like anything else",
        "An empty message compresses to an empty message",
    ],
    hint="Walk the string keeping the current character and a count. When the character "
         "changes, emit the previous character and its count and reset. Do not forget to "
         "emit the final run after the loop ends; that is the classic slip.",
    py_spec="""
<p>Write <code>compress(text)</code>: run-length encode <code>text</code>, so each run of
identical characters becomes the character followed by the run length. So
<code>"aaabcc"</code> becomes <code>"a3b1c2"</code>. An empty string returns an empty
string.</p>
""",
    py_stub='''def compress(text):
    """Run-length encode: 'aaabcc' -> 'a3b1c2'."""
    # TODO
    return text
''',
    py_reference='''def compress(text):
    """Run-length encode: 'aaabcc' -> 'a3b1c2'."""
    if not text:
        return ""
    out = []
    current = text[0]
    count = 1
    for ch in text[1:]:
        if ch == current:
            count += 1
        else:
            out.append(f"{current}{count}")
            current = ch
            count = 1
    out.append(f"{current}{count}")
    return "".join(out)
''',
    py_checker=py_cases("compress", [
        (("aaabcc",), "a3b1c2"), (("x",), "x1"), (("z" * 12 + "q",), "z12q1"),
        (("!! ..",), "!2 1.2"), (("",), ""),
    ]),
    rs_spec="""
<p>Write <code>compress(text: &amp;str) -&gt; String</code>: run-length encode
<code>text</code>, so each run of identical characters becomes the character followed by
the run length. So <code>"aaabcc"</code> becomes <code>"a3b1c2"</code>. An empty string
returns an empty string.</p>
""",
    rs_stub='''/// Run-length encode: "aaabcc" -> "a3b1c2".
fn compress(text: &str) -> String {
    // TODO
    text.to_string()
}
''',
    rs_reference='''/// Run-length encode: "aaabcc" -> "a3b1c2".
fn compress(text: &str) -> String {
    let mut out = String::new();
    let mut chars = text.chars();
    let Some(mut current) = chars.next() else { return out; };
    let mut count = 1;
    for ch in chars {
        if ch == current {
            count += 1;
        } else {
            out.push(current);
            out.push_str(&count.to_string());
            current = ch;
            count = 1;
        }
    }
    out.push(current);
    out.push_str(&count.to_string());
    out
}
''',
    rs_checker=rs_cases("compress", [
        (['"aaabcc"'], '"a3b1c2"'), (['"x"'], '"x1"'), (['"zzzzzzzzzzzzq"'], '"z12q1"'),
        (['"!! .."'], '"!2 1.2"'), (['""'], '""'),
    ]),
)

# -------------------------------------------------------------- 32
_m(
    season=4, num=32, slug="32-version-numbers", id="bridge-s4m32", station="ops",
    title="Which Ship Is Newer?", stardate="Stardate 55153.9",
    crew=["raghunathan", "skree", "dubois"],
    blurb="Two ships, two software versions, and a comparison that thinks 1.10 is "
          "older than 1.9. It is not.",
    briefing="""
<p>The other computer runs Magnanimous system software version 1.10.3. Ours runs 1.9.7.
The comparison routine says ours is newer, because it compares the version strings as
text, and as text "1.9" comes after "1.10". As numbers, it does not. Version numbers
are three integers with dots between, and they compare part by part.</p>

<p>Commander Raghunathan wants a version type that parses the string, compares
numerically, and prints itself back out. In Python that means the comparison methods. In
Rust it means implementing <code>Ord</code>, after which sorting, min and max all work on
your type for free. Lt. Skree has asked whether "newer" means "better". The Commander
has said "not today".</p>
""",
    debrief="""
<p>Theirs is newer. By one release. Commander Raghunathan has pulled up the release notes
for 1.10.3, which are the same as ours plus one line: <em>"pressure|flow mismatch:
resolved"</em>. She has looked at the date on it for a while.</p>

<p><strong>The Anomaly is complete.</strong> Deep Space is open, and Engineering with
it. Whatever the other Magnanimous is, tomorrow's stardate is in both logs.</p>
""",
    objectives=[
        "Parses major, minor and patch from a string",
        "1.10.0 is newer than 1.9.7, because parts compare as numbers",
        "Equal versions compare equal",
        "Renders back to the same string",
        "A list of versions sorts correctly",
    ],
    hint="Split on the dots and convert each part to an integer. Then compare the tuple "
         "of three numbers, which Python and Rust both do part by part. Python: implement "
         "<code>__eq__</code> and <code>__lt__</code> and use "
         "<code>functools.total_ordering</code>. Rust: derive or implement "
         "<code>Ord</code> on a struct of three integers.",
    py_spec="""
<p>Write a class <code>Version</code>: <code>Version("1.10.3")</code> parses three
integers <code>major</code>, <code>minor</code>, <code>patch</code>. Instances compare
numerically part by part (<code>==</code>, <code>&lt;</code>, and the rest), so
<code>Version("1.10.0") &gt; Version("1.9.7")</code>. <code>str(v)</code> gives back
<code>"1.10.3"</code>.</p>
""",
    py_stub='''class Version:
    """A three-part version number that compares numerically."""

    def __init__(self, text):
        # TODO: parse "1.10.3" into three integers
        self.text = text

    def __str__(self):
        return self.text

    # TODO: comparison methods
''',
    py_reference='''from functools import total_ordering


@total_ordering
class Version:
    """A three-part version number that compares numerically."""

    def __init__(self, text):
        major, minor, patch = text.split(".")
        self.parts = (int(major), int(minor), int(patch))

    def __str__(self):
        return ".".join(str(p) for p in self.parts)

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts
''',
    py_checker=py_custom('''
def _t0():
    v = Version("1.10.3")
    return str(v)
_g = _guard(0, _t0, "Version('1.10.3')")
if _g is not _FAILED:
    _report(0, _g == "1.10.3", f"str() gave {_g!r}, wanted '1.10.3'")

_g = _guard(1, lambda: (Version("1.10.0") > Version("1.9.7"), Version("1.9.7") < Version("1.10.0")), "1.10.0 vs 1.9.7")
if _g is not _FAILED:
    _report(1, _g == (True, True), f"1.10.0 > 1.9.7 is {_g[0]}, 1.9.7 < 1.10.0 is {_g[1]}, wanted True and True")

_g = _guard(2, lambda: (Version("2.0.1") == Version("2.0.1"), Version("2.0.1") != Version("2.0.2")), "equality")
if _g is not _FAILED:
    _report(2, _g == (True, True), f"equal is {_g[0]}, unequal is {_g[1]}, wanted True and True")

_g = _guard(3, lambda: str(Version("0.4.12")), "str(Version('0.4.12'))")
if _g is not _FAILED:
    _report(3, _g == "0.4.12", f"got {_g!r}, wanted '0.4.12'")

_g = _guard(4, lambda: [str(v) for v in sorted([Version("1.10.0"), Version("1.2.0"), Version("1.9.7"), Version("0.9.9")])], "sorted(...)")
if _g is not _FAILED:
    _report(4, _g == ["0.9.9", "1.2.0", "1.9.7", "1.10.0"], f"sorted gave {_short(_g)}, wanted [0.9.9, 1.2.0, 1.9.7, 1.10.0]")
'''),
    rs_spec="""
<p>Keep the struct as given. Write <code>Version::parse(text: &amp;str) -&gt;
Version</code> that reads three integers from <code>"1.10.3"</code>, implement
<code>Display</code> so it prints back as <code>"1.10.3"</code>, and make it ordered
(<code>PartialEq</code>, <code>Eq</code>, <code>PartialOrd</code>, <code>Ord</code>) so
versions compare numerically part by part. Deriving works if the fields are in the right
order.</p>
""",
    rs_stub='''use std::fmt;

/// A three-part version number that compares numerically.
#[derive(Debug, Clone)]
struct Version {
    major: u32,
    minor: u32,
    patch: u32,
}

impl Version {
    fn parse(text: &str) -> Version {
        // TODO
        Version { major: 0, minor: 0, patch: 0 }
    }
}

impl fmt::Display for Version {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        // TODO
        write!(f, "0.0.0")
    }
}

// TODO: make Version comparable (PartialEq, Eq, PartialOrd, Ord)
''',
    rs_reference='''use std::fmt;

/// A three-part version number that compares numerically.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord)]
struct Version {
    major: u32,
    minor: u32,
    patch: u32,
}

impl Version {
    fn parse(text: &str) -> Version {
        let mut it = text.split('.').map(|p| p.trim().parse::<u32>().unwrap_or(0));
        Version {
            major: it.next().unwrap_or(0),
            minor: it.next().unwrap_or(0),
            patch: it.next().unwrap_or(0),
        }
    }
}

impl fmt::Display for Version {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}.{}.{}", self.major, self.minor, self.patch)
    }
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let v = Version::parse("1.10.3");
    __report(0, v.major == 1 && v.minor == 10 && v.patch == 3, format!("parsed as {}.{}.{}, wanted 1.10.3", v.major, v.minor, v.patch));

    let a = Version::parse("1.10.0"); let b = Version::parse("1.9.7");
    __report(1, a > b && b < a, format!("1.10.0 > 1.9.7 is {}, wanted true", a > b));

    let a = Version::parse("2.0.1"); let b = Version::parse("2.0.1"); let c = Version::parse("2.0.2");
    __report(2, a == b && a != c, format!("equal is {}, unequal is {}, wanted true and true", a == b, a != c));

    let s = format!("{}", Version::parse("0.4.12"));
    __report(3, s == "0.4.12", format!("Display gave {:?}, wanted \\"0.4.12\\"", s));

    let mut vs = vec![Version::parse("1.10.0"), Version::parse("1.2.0"), Version::parse("1.9.7"), Version::parse("0.9.9")];
    vs.sort();
    let got: Vec<String> = vs.iter().map(|v| v.to_string()).collect();
    __report(4, got == vec!["0.9.9", "1.2.0", "1.9.7", "1.10.0"], format!("sorted gave {:?}", got));
}
'''),
)
