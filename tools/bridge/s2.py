"""Season 2: Routine Patrol.

Loops, collections, iteration. Helm, Ops, and the newly opened Science
station. Every mission here is a list going in and something coming out.
"""

from .helpers import _m, py_cases, rs_cases

# --------------------------------------------------------------- 9
_m(
    season=2, num=9, slug="09-the-manifest", id="bridge-s2m9", station="ops",
    title="The Manifest", stardate="Stardate 55118.4",
    crew=["tkala", "tannenbaum"],
    blurb="Forty crates came aboard. The manifest says the total mass is 'crate'. "
          "That is not a mass.",
    briefing="""
<p>Forty crates were loaded at Starbase 11 and the cargo manifest's total mass field now
reads, in full, <em>"crate"</em>. Chief T'Kala, who signs for cargo and takes signing
seriously, has declined to sign for a mass of "crate".</p>

<p>Ensign Tannenbaum's summing routine, on inspection, adds the <em>first</em> crate to
itself forty times and then, for reasons that remain unclear, formats the result as
its own name. The Chief would like a number. Any number, provided it is the right one.</p>
""",
    debrief="""
<p>The manifest reads 4,120 kilograms and Chief T'Kala has signed for it. She has also
initialled Gerald's entry, since Gerald technically counts as cargo. Gerald weighs four
kilograms and is listed as "live plant, do not stack".</p>
""",
    objectives=[
        "Four crates add up correctly",
        "A single crate is its own total",
        "An empty hold has a mass of zero",
        "Forty identical crates",
        "Large masses do not lose anything",
    ],
    hint="A running total: start at zero and add every crate. Both languages have a "
         "one-liner for this (<code>sum</code>, <code>.iter().sum()</code>), and it is "
         "worth writing the loop by hand once first.",
    py_spec="""
<p>Write <code>total_mass(crates)</code>: <code>crates</code> is a list of whole-number
masses in kilograms. Return their total. An empty list has a total of <code>0</code>.</p>
""",
    py_stub='''def total_mass(crates):
    """Total mass of every crate in the hold. Empty hold: 0."""
    # TODO
    return "crate"
''',
    py_reference='''def total_mass(crates):
    """Total mass of every crate in the hold. Empty hold: 0."""
    total = 0
    for mass in crates:
        total += mass
    return total
''',
    py_checker=py_cases("total_mass", [
        (([120, 80, 45, 300],), 545), (([1000],), 1000), (([],), 0),
        (([103] * 40,), 4120), (([2_000_000, 3_000_000, 5],), 5_000_005),
    ]),
    rs_spec="""
<p>Write <code>total_mass(crates: &amp;[u64]) -&gt; u64</code>: the crates' total mass
in kilograms. An empty slice has a total of <code>0</code>.</p>
""",
    rs_stub='''/// Total mass of every crate in the hold. Empty hold: 0.
fn total_mass(crates: &[u64]) -> u64 {
    // TODO
    0
}
''',
    rs_reference='''/// Total mass of every crate in the hold. Empty hold: 0.
fn total_mass(crates: &[u64]) -> u64 {
    let mut total = 0;
    for mass in crates {
        total += mass;
    }
    total
}
''',
    rs_checker=rs_cases("total_mass", [
        (["&[120, 80, 45, 300]"], "545"), (["&[1000]"], "1000"), (["&[]"], "0"),
        (["&[103; 40]"], "4120"), (["&[2_000_000, 3_000_000, 5]"], "5_000_005"),
    ]),
)

# -------------------------------------------------------------- 10
_m(
    season=2, num=10, slug="10-hottest-reading", id="bridge-s2m10", station="helm",
    title="The Hottest Reading", stardate="Stardate 55119.9",
    crew=["raghunathan", "skree"],
    blurb="Which coolant loop is running hottest? The display shows the first one, "
          "always, regardless.",
    briefing="""
<p>The engineering display is meant to show the hottest of the eight coolant loops so
that whoever is on watch knows where to look first. It shows loop one. It always shows
loop one. Loop one is, in fact, the coldest, and has been for a month.</p>

<p>Commander Raghunathan found the routine returns the <em>first</em> reading rather
than the largest. Lt. Skree has added that when there are no readings at all, the
display shows "-1 degrees", which Skree describes as "a temperature that is also a
lie". The Commander would like the real maximum, and nothing at all when there is
nothing to measure.</p>
""",
    debrief="""
<p>The display shows loop six, at 71 degrees, which is where Commander Raghunathan has
been standing with a torch for a month. When there are no readings it now shows nothing,
which Lt. Skree has approved as "the only honest thing it has ever displayed".</p>
""",
    objectives=[
        "The largest of several readings",
        "A single reading is the maximum",
        "The maximum is not the first reading",
        "All negative readings: the least negative wins",
        "No readings at all: nothing, not a made-up number",
    ],
    hint="Keep the best-so-far as you walk the list, and start it from the first element, "
         "not from zero, or the all-negative case will bite. Python returns "
         "<code>None</code> for empty; Rust returns an <code>Option</code>, and "
         "<code>.iter().max()</code> already does exactly this.",
    py_spec="""
<p>Write <code>hottest(readings)</code>: return the largest number in the list, or
<code>None</code> if the list is empty.</p>
""",
    py_stub='''def hottest(readings):
    """The largest reading, or None if there are none."""
    # TODO: this returns the first one, which is the bug.
    if readings:
        return readings[0]
    return -1
''',
    py_reference='''def hottest(readings):
    """The largest reading, or None if there are none."""
    if not readings:
        return None
    best = readings[0]
    for r in readings[1:]:
        if r > best:
            best = r
    return best
''',
    py_checker=py_cases("hottest", [
        (([42, 71, 58, 63],), 71), (([55],), 55), (([12, 30, 29],), 30),
        (([-40, -12, -25],), -12), (([],), None),
    ]),
    rs_spec="""
<p>Write <code>hottest(readings: &amp;[i32]) -&gt; Option&lt;i32&gt;</code>: the largest
reading, or <code>None</code> if the slice is empty.</p>
""",
    rs_stub='''/// The largest reading, or None if there are none.
fn hottest(readings: &[i32]) -> Option<i32> {
    // TODO: this returns the first one, which is the bug.
    if readings.is_empty() { Some(-1) } else { Some(readings[0]) }
}
''',
    rs_reference='''/// The largest reading, or None if there are none.
fn hottest(readings: &[i32]) -> Option<i32> {
    readings.iter().copied().max()
}
''',
    rs_checker=rs_cases("hottest", [
        (["&[42, 71, 58, 63]"], "Some(71)"), (["&[55]"], "Some(55)"),
        (["&[12, 30, 29]"], "Some(30)"), (["&[-40, -12, -25]"], "Some(-12)"),
        (["&[]"], "None"),
    ]),
)

# -------------------------------------------------------------- 11
_m(
    season=2, num=11, slug="11-signal-cleanup", id="bridge-s2m11", station="science",
    title="Signal Cleanup", stardate="Stardate 55121.3",
    crew=["skree"],
    blurb="The long-range array reports a thousand readings, most of them noise. "
          "Lt. Skree wants only the ones that matter, in the order they arrived.",
    briefing="""
<p>Welcome to the Science station. Lt. Skree has been waiting for you, in the sense that
Skree has been standing very still by the console for some time.</p>

<p>The long-range array delivers readings in the order it takes them. Most are below
the noise floor. Skree wants every reading <em>above</em> a threshold, in their original
order, and has been extremely specific that "above" means strictly greater than: a
reading equal to the floor is noise, by definition, and Skree has the definition
printed out.</p>
""",
    debrief="""
<p>Skree has the filtered signal and has said "adequate", which the crew has learned to
receive as effusive praise. There is a faint pattern in the readings. Skree has filed
it under "pending long-term observation" and gone to lunch, which Skree does at exactly
the same time every day.</p>
""",
    objectives=[
        "Keeps only readings above the threshold, in order",
        "A reading equal to the threshold is noise and is dropped",
        "Nothing above the threshold: an empty result",
        "Everything above the threshold: the whole list, unchanged",
        "Negative thresholds work too",
    ],
    hint="Build a new list containing each reading that passes the test. Do not modify "
         "the input while walking it. A comprehension or <code>filter</code> is the "
         "natural shape; a loop with <code>append</code> is just as good.",
    py_spec="""
<p>Write <code>above_threshold(readings, threshold)</code>: return a new list of the
readings that are <strong>strictly greater</strong> than <code>threshold</code>, keeping
their original order.</p>
""",
    py_stub='''def above_threshold(readings, threshold):
    """Every reading strictly above the threshold, in order."""
    # TODO
    return readings
''',
    py_reference='''def above_threshold(readings, threshold):
    """Every reading strictly above the threshold, in order."""
    return [r for r in readings if r > threshold]
''',
    py_checker=py_cases("above_threshold", [
        (([3, 12, 7, 20, 1], 5), [12, 7, 20]), (([5, 6, 5, 4], 5), [6]),
        (([1, 2, 3], 10), []), (([8, 9, 10], 0), [8, 9, 10]),
        (([-5, -1, -3, 0], -3), [-1, 0]),
    ]),
    rs_spec="""
<p>Write <code>above_threshold(readings: &amp;[i32], threshold: i32) -&gt;
Vec&lt;i32&gt;</code>: the readings that are <strong>strictly greater</strong> than
<code>threshold</code>, in their original order.</p>
""",
    rs_stub='''/// Every reading strictly above the threshold, in order.
fn above_threshold(readings: &[i32], threshold: i32) -> Vec<i32> {
    // TODO
    readings.to_vec()
}
''',
    rs_reference='''/// Every reading strictly above the threshold, in order.
fn above_threshold(readings: &[i32], threshold: i32) -> Vec<i32> {
    readings.iter().copied().filter(|&r| r > threshold).collect()
}
''',
    rs_checker=rs_cases("above_threshold", [
        (["&[3, 12, 7, 20, 1]", "5"], "vec![12, 7, 20]"), (["&[5, 6, 5, 4]", "5"], "vec![6]"),
        (["&[1, 2, 3]", "10"], "Vec::<i32>::new()"), (["&[8, 9, 10]", "0"], "vec![8, 9, 10]"),
        (["&[-5, -1, -3, 0]", "-3"], "vec![-1, 0]"),
    ]),
)

# -------------------------------------------------------------- 12
_m(
    season=2, num=12, slug="12-duplicate-requisitions", id="bridge-s2m12", station="ops",
    title="Duplicate Requisitions", stardate="Stardate 55122.8",
    crew=["tannenbaum", "tkala"],
    blurb="Ensign Tannenbaum submitted the same requisition eleven times, 'to be "
          "safe'. Stores would like the list without the repeats.",
    briefing="""
<p>Ensign Tannenbaum, worried that his requisition for a replacement plasma coupling
"might not have gone through", submitted it eleven times. It went through eleven times.
Stores now has a list of forty items with a great many repeats and a standing question
about whether the Ensign is allowed near forms.</p>

<p>Chief T'Kala wants the list with each item appearing once, keeping the
<em>first</em> occurrence in place, so the order stays the order things were asked
for. She has been clear that sorting it would be cheating, and that she can tell.</p>
""",
    debrief="""
<p>Twelve distinct items, in the order they were first requested. Ensign Tannenbaum has
been issued one plasma coupling and a short document titled "Once Is Enough", which he
has read, he says, several times.</p>
""",
    objectives=[
        "Repeats removed, first appearance kept in place",
        "An already-unique list is unchanged",
        "Every item the same collapses to one",
        "Order is preserved, not sorted",
        "An empty list stays empty",
    ],
    hint="Walk the list keeping a record of what you have already seen (a set is "
         "ideal), and only keep an item the first time. Converting to a set and back "
         "loses the order, which is the fourth objective.",
    py_spec="""
<p>Write <code>unique_in_order(items)</code>: return a new list with duplicates removed,
keeping the first occurrence of each item and the original order of first appearances.</p>
""",
    py_stub='''def unique_in_order(items):
    """Each item once, in order of first appearance."""
    # TODO
    return items
''',
    py_reference='''def unique_in_order(items):
    """Each item once, in order of first appearance."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result
''',
    py_checker=py_cases("unique_in_order", [
        ((["coupling", "coil", "coupling", "gasket", "coil"],), ["coupling", "coil", "gasket"]),
        ((["a", "b", "c"],), ["a", "b", "c"]),
        ((["coupling"] * 11,), ["coupling"]),
        ((["zeta", "alpha", "zeta", "mu"],), ["zeta", "alpha", "mu"]),
        (([],), []),
    ]),
    rs_spec="""
<p>Write <code>unique_in_order(items: &amp;[&amp;str]) -&gt; Vec&lt;String&gt;</code>:
duplicates removed, keeping the first occurrence of each item and the original order of
first appearances.</p>
""",
    rs_stub='''/// Each item once, in order of first appearance.
fn unique_in_order(items: &[&str]) -> Vec<String> {
    // TODO
    items.iter().map(|s| s.to_string()).collect()
}
''',
    rs_reference='''use std::collections::HashSet;

/// Each item once, in order of first appearance.
fn unique_in_order(items: &[&str]) -> Vec<String> {
    let mut seen = HashSet::new();
    let mut result = Vec::new();
    for &item in items {
        if seen.insert(item) {
            result.push(item.to_string());
        }
    }
    result
}
''',
    rs_checker=rs_cases("unique_in_order", [
        (['&["coupling", "coil", "coupling", "gasket", "coil"]'], 'vec!["coupling", "coil", "gasket"]'),
        (['&["a", "b", "c"]'], 'vec!["a", "b", "c"]'),
        (['&["coupling"; 11]'], 'vec!["coupling"]'),
        (['&["zeta", "alpha", "zeta", "mu"]'], 'vec!["zeta", "alpha", "mu"]'),
        (['&[]'], 'Vec::<&str>::new()'),
    ]),
)

# -------------------------------------------------------------- 13
_m(
    season=2, num=13, slug="13-countdown", id="bridge-s2m13", station="helm",
    title="Countdown to Warp", stardate="Stardate 55124.0",
    crew=["dubois", "tannenbaum"],
    blurb="The Captain likes a countdown. The current one goes '5... 5... 5... 5... "
          "5... engage', which is not the same thing.",
    briefing="""
<p>The Captain enjoys the countdown before a warp jump. It is, he says, "the one bit of
theatre we are still allowed". Ensign Tannenbaum's new countdown routine announces the
starting number over and over and then says "engage", which the Captain has described
as "less theatre, more a man shouting a number".</p>

<p>The routine should count down from the starting number to one, each followed by
three dots and a space, and finish with the word <em>engage</em>. From zero, it should
simply say <em>engage</em>. The Captain has been extremely clear about the dots.</p>
""",
    debrief="""
<p>"5... 4... 3... 2... 1... engage." The Captain has run it three times for no
operational reason and Ensign Tannenbaum has been permitted to press the button once,
supervised. Lt. Skree has asked what the dots are for. Nobody has a good answer.</p>
""",
    objectives=[
        "From five: '5... 4... 3... 2... 1... engage'",
        "From one: '1... engage'",
        "From zero: just 'engage'",
        "From three",
        "From ten, and the double digits do not break the spacing",
    ],
    hint="Loop from n down to 1, collecting each number followed by '... ', then add "
         "'engage'. Building a list of parts and joining them is tidier than "
         "concatenating in the loop, and it makes the zero case fall out for free.",
    py_spec="""
<p>Write <code>countdown(n)</code>: return a single string counting down from
<code>n</code> to 1, each number followed by <code>"... "</code>, and ending with
<code>"engage"</code>. So <code>countdown(3)</code> is
<code>"3... 2... 1... engage"</code>, and <code>countdown(0)</code> is
<code>"engage"</code>.</p>
""",
    py_stub='''def countdown(n):
    """'5... 4... 3... 2... 1... engage', or just 'engage' from zero."""
    # TODO
    return "engage"
''',
    py_reference='''def countdown(n):
    """'5... 4... 3... 2... 1... engage', or just 'engage' from zero."""
    parts = []
    for k in range(n, 0, -1):
        parts.append(f"{k}... ")
    return "".join(parts) + "engage"
''',
    py_checker=py_cases("countdown", [
        ((5,), "5... 4... 3... 2... 1... engage"), ((1,), "1... engage"),
        ((0,), "engage"), ((3,), "3... 2... 1... engage"),
        ((10,), "10... 9... 8... 7... 6... 5... 4... 3... 2... 1... engage"),
    ]),
    rs_spec="""
<p>Write <code>countdown(n: u32) -&gt; String</code>: count down from <code>n</code> to
1, each number followed by <code>"... "</code>, ending with <code>"engage"</code>. So
<code>countdown(3)</code> is <code>"3... 2... 1... engage"</code>, and
<code>countdown(0)</code> is <code>"engage"</code>.</p>
""",
    rs_stub='''/// "5... 4... 3... 2... 1... engage", or just "engage" from zero.
fn countdown(n: u32) -> String {
    // TODO
    String::from("engage")
}
''',
    rs_reference='''/// "5... 4... 3... 2... 1... engage", or just "engage" from zero.
fn countdown(n: u32) -> String {
    let mut out = String::new();
    for k in (1..=n).rev() {
        out.push_str(&format!("{k}... "));
    }
    out.push_str("engage");
    out
}
''',
    rs_checker=rs_cases("countdown", [
        (["5"], '"5... 4... 3... 2... 1... engage"'), (["1"], '"1... engage"'),
        (["0"], '"engage"'), (["3"], '"3... 2... 1... engage"'),
        (["10"], '"10... 9... 8... 7... 6... 5... 4... 3... 2... 1... engage"'),
    ]),
)

# -------------------------------------------------------------- 14
_m(
    season=2, num=14, slug="14-most-requested", id="bridge-s2m14", station="ops",
    title="The Most Requested Item", stardate="Stardate 55125.6",
    crew=["tkala", "tannenbaum", "raghunathan"],
    blurb="Stores wants to know what the crew asks for most, so they can stop running "
          "out of it. The answer is not, in fact, plasma couplings.",
    briefing="""
<p>Chief T'Kala would like to know which item is requisitioned most often, so Stores can
keep more of it. The naive answer is "plasma couplings", because of the Tannenbaum
incident, but the Chief wants the count done properly, over the real log, with the
Ensign's eleven duplicates already removed.</p>

<p>Where two items tie, she wants the one that comes first alphabetically, so the answer
is stable and nobody argues. Where the log is empty, she wants nothing, rather than a
guess. Commander Raghunathan has predicted the answer will be "coffee filters" and has
put money on it.</p>
""",
    debrief="""
<p>Coffee filters. Commander Raghunathan has collected. Stores has ordered a great many
coffee filters, and the Captain, on hearing this, said "good" in a tone that closed the
subject.</p>
""",
    objectives=[
        "The most frequent item in a mixed log",
        "A tie goes to the alphabetically first item",
        "A single-entry log",
        "Every entry the same",
        "An empty log: nothing, not a guess",
    ],
    hint="Count each item into a dictionary or map first, then pick the winner. For the "
         "tie rule, compare on (count, name) rather than count alone: highest count, "
         "and among equals, the smallest name.",
    py_spec="""
<p>Write <code>most_requested(log)</code>: <code>log</code> is a list of item names.
Return the name that appears most often. If several tie, return the alphabetically
first of them. Return <code>None</code> for an empty log.</p>
""",
    py_stub='''def most_requested(log):
    """The most frequent item; ties go alphabetically; None if empty."""
    # TODO
    return None
''',
    py_reference='''def most_requested(log):
    """The most frequent item; ties go alphabetically; None if empty."""
    if not log:
        return None
    counts = {}
    for item in log:
        counts[item] = counts.get(item, 0) + 1
    best = None
    for item, n in counts.items():
        if best is None or n > counts[best] or (n == counts[best] and item < best):
            best = item
    return best
''',
    py_checker=py_cases("most_requested", [
        ((["filters", "coupling", "filters", "gasket", "filters", "coupling"],), "filters"),
        ((["gasket", "coil", "gasket", "coil"],), "coil"),
        ((["torch"],), "torch"),
        ((["coil", "coil", "coil"],), "coil"),
        (([],), None),
    ]),
    rs_spec="""
<p>Write <code>most_requested(log: &amp;[&amp;str]) -&gt; Option&lt;String&gt;</code>: the
name that appears most often. If several tie, the alphabetically first of them.
<code>None</code> for an empty log.</p>
""",
    rs_stub='''/// The most frequent item; ties go alphabetically; None if empty.
fn most_requested(log: &[&str]) -> Option<String> {
    // TODO
    None
}
''',
    rs_reference='''use std::collections::HashMap;

/// The most frequent item; ties go alphabetically; None if empty.
fn most_requested(log: &[&str]) -> Option<String> {
    let mut counts: HashMap<&str, usize> = HashMap::new();
    for &item in log {
        *counts.entry(item).or_insert(0) += 1;
    }
    counts
        .into_iter()
        .max_by(|a, b| a.1.cmp(&b.1).then_with(|| b.0.cmp(a.0)))
        .map(|(name, _)| name.to_string())
}
''',
    rs_checker=rs_cases("most_requested", [
        (['&["filters", "coupling", "filters", "gasket", "filters", "coupling"]'], 'Some("filters".to_string())'),
        (['&["gasket", "coil", "gasket", "coil"]'], 'Some("coil".to_string())'),
        (['&["torch"]'], 'Some("torch".to_string())'),
        (['&["coil", "coil", "coil"]'], 'Some("coil".to_string())'),
        (['&[]'], 'None'),
    ]),
)

# -------------------------------------------------------------- 15
_m(
    season=2, num=15, slug="15-smoothing", id="bridge-s2m15", station="science",
    title="Smoothing the Signal", stardate="Stardate 55127.2",
    crew=["skree"],
    blurb="The raw signal jitters. Lt. Skree wants a moving average, and has views on "
          "what happens at the edges.",
    briefing="""
<p>The pattern Lt. Skree filed for long-term observation is real, and it is buried in
jitter. Skree wants a moving average: for each position, the mean of that reading and
the ones before it in a window of a given size, rounded to two decimal places.</p>

<p>Skree has anticipated the question about the beginning, where a full window does not
exist yet, and answers it thus: <em>use what you have</em>. The first value averages one
reading, the second averages two, and so on until the window is full. Skree considers
this "the only defensible choice" and has already rejected two others in writing.</p>
""",
    debrief="""
<p>The smoothed signal shows a slow rise over eleven days. Skree has looked at it for a
long time, said "hm", and upgraded the file from "pending long-term observation" to
"pending". Nobody knows what the difference is, and nobody has dared ask.</p>
""",
    objectives=[
        "A window of two over four readings",
        "A window of three, with the ramp-up at the start using what exists",
        "A window of one is the readings unchanged",
        "A window larger than the whole list averages everything so far at each step",
        "Results are rounded to two decimal places",
    ],
    hint="For position i, average the readings from max(0, i - window + 1) up to and "
         "including i. Slicing makes that one line. Round each result to two places, "
         "and remember Rust rounds by multiplying, rounding, and dividing.",
    py_spec="""
<p>Write <code>moving_average(readings, window)</code>: return a list the same length as
<code>readings</code>, where each entry is the mean of that reading and up to
<code>window - 1</code> readings before it, <strong>rounded to two decimal places</strong>.
Where fewer than <code>window</code> readings exist yet, average the ones that do.</p>
""",
    py_stub='''def moving_average(readings, window):
    """Trailing mean over `window` readings, using what exists at the start."""
    # TODO
    return readings
''',
    py_reference='''def moving_average(readings, window):
    """Trailing mean over `window` readings, using what exists at the start."""
    out = []
    for i in range(len(readings)):
        start = max(0, i - window + 1)
        chunk = readings[start:i + 1]
        out.append(round(sum(chunk) / len(chunk), 2))
    return out
''',
    py_checker=py_cases("moving_average", [
        (([2, 4, 6, 8], 2), [2.0, 3.0, 5.0, 7.0]),
        (([3, 6, 9, 12, 15], 3), [3.0, 4.5, 6.0, 9.0, 12.0]),
        (([1, 5, 2], 1), [1.0, 5.0, 2.0]),
        (([10, 20, 30], 10), [10.0, 15.0, 20.0]),
        (([1, 2, 2], 3), [1.0, 1.5, 1.67]),
    ], check="len(_got) == len(_want) and all(abs(a - b) < 1e-6 for a, b in zip(_got, _want))"),
    rs_spec="""
<p>Write <code>moving_average(readings: &amp;[f64], window: usize) -&gt; Vec&lt;f64&gt;</code>:
a vector the same length as <code>readings</code>, where each entry is the mean of that
reading and up to <code>window - 1</code> readings before it, <strong>rounded to two
decimal places</strong>. Where fewer than <code>window</code> readings exist yet,
average the ones that do.</p>
""",
    rs_stub='''/// Trailing mean over `window` readings, using what exists at the start.
fn moving_average(readings: &[f64], window: usize) -> Vec<f64> {
    // TODO
    readings.to_vec()
}
''',
    rs_reference='''/// Trailing mean over `window` readings, using what exists at the start.
fn moving_average(readings: &[f64], window: usize) -> Vec<f64> {
    let mut out = Vec::with_capacity(readings.len());
    for i in 0..readings.len() {
        let start = if i + 1 >= window { i + 1 - window } else { 0 };
        let chunk = &readings[start..=i];
        let mean = chunk.iter().sum::<f64>() / chunk.len() as f64;
        out.push((mean * 100.0).round() / 100.0);
    }
    out
}
''',
    rs_checker=rs_cases("moving_average", [
        (["&[2.0, 4.0, 6.0, 8.0]", "2"], "vec![2.0, 3.0, 5.0, 7.0]"),
        (["&[3.0, 6.0, 9.0, 12.0, 15.0]", "3"], "vec![3.0, 4.5, 6.0, 9.0, 12.0]"),
        (["&[1.0, 5.0, 2.0]", "1"], "vec![1.0, 5.0, 2.0]"),
        (["&[10.0, 20.0, 30.0]", "10"], "vec![10.0, 15.0, 20.0]"),
        (["&[1.0, 2.0, 2.0]", "3"], "vec![1.0, 1.5, 1.67]"),
    ], check="got.len() == want.len() && got.iter().zip(want.iter()).all(|(a, b)| (a - b).abs() < 1e-6)"),
)

# -------------------------------------------------------------- 16
_m(
    season=2, num=16, slug="16-diagnostic-sweep", id="bridge-s2m16", station="helm",
    title="The Diagnostic Sweep", stardate="Stardate 55129.5",
    crew=["raghunathan", "dubois", "skree"],
    blurb="Every third relay needs coolant, every fifth needs plasma, and every "
          "fifteenth needs both. The old sweep just counted.",
    briefing="""
<p>The end-of-patrol diagnostic walks every relay in sequence and says what each one
needs. Every third relay needs <em>coolant</em>. Every fifth needs <em>plasma</em>. A relay
that is both a third and a fifth needs <em>coolant-plasma</em>, and everything else just
reports its number. It is the oldest routine on the ship and it has, at some point,
stopped doing any of that and started simply counting.</p>

<p>Commander Raghunathan says every engineer in the fleet has written this exact
routine as a rite of passage, and that the ones who get relay fifteen wrong the first
time are, historically, all of them. Lt. Skree does not see why fifteen would be
special. Skree will.</p>
""",
    debrief="""
<p>The sweep reports correctly, relay fifteen included, and Commander Raghunathan has
signed off the patrol. The Captain has declared the routine "traditional" and asked that
it never be replaced.</p>

<p><strong>Routine Patrol complete.</strong> Season 3 is open, and there is a signal on
long-range sensors that Lt. Skree would like to talk to you about.</p>
""",
    objectives=[
        "Relays 1 to 5: number, number, coolant, number, plasma",
        "Relay 15 is coolant-plasma, not coolant and not plasma",
        "Relays 1 to 15 in full",
        "A sweep of zero relays is empty",
        "Relay 30 is also coolant-plasma",
    ],
    hint="Check the both-case first. If you test 'divisible by three' before 'divisible "
         "by both', fifteen is caught by the first test and never reaches the right "
         "answer. Order of conditions is the whole puzzle.",
    py_spec="""
<p>Write <code>sweep(n)</code>: return a list of strings for relays 1 to <code>n</code>.
Multiples of 3 give <code>"coolant"</code>, multiples of 5 give <code>"plasma"</code>,
multiples of both give <code>"coolant-plasma"</code>, and everything else gives the
relay number as a string. <code>sweep(0)</code> is an empty list.</p>
""",
    py_stub='''def sweep(n):
    """Diagnostic labels for relays 1..n."""
    # TODO
    return [str(k) for k in range(1, n + 1)]
''',
    py_reference='''def sweep(n):
    """Diagnostic labels for relays 1..n."""
    out = []
    for k in range(1, n + 1):
        if k % 15 == 0:
            out.append("coolant-plasma")
        elif k % 3 == 0:
            out.append("coolant")
        elif k % 5 == 0:
            out.append("plasma")
        else:
            out.append(str(k))
    return out
''',
    py_checker=py_cases("sweep", [
        ((5,), ["1", "2", "coolant", "4", "plasma"]),
        ((15,), ["1", "2", "coolant", "4", "plasma", "coolant", "7", "8", "coolant",
                 "plasma", "11", "coolant", "13", "14", "coolant-plasma"]),
        ((3,), ["1", "2", "coolant"]),
        ((0,), []),
        ((30,), ["1", "2", "coolant", "4", "plasma", "coolant", "7", "8", "coolant",
                 "plasma", "11", "coolant", "13", "14", "coolant-plasma", "16", "17",
                 "coolant", "19", "plasma", "coolant", "22", "23", "coolant", "plasma",
                 "26", "coolant", "28", "29", "coolant-plasma"]),
    ]),
    rs_spec="""
<p>Write <code>sweep(n: u32) -&gt; Vec&lt;String&gt;</code>: labels for relays 1 to
<code>n</code>. Multiples of 3 give <code>"coolant"</code>, multiples of 5 give
<code>"plasma"</code>, multiples of both give <code>"coolant-plasma"</code>, and
everything else gives the relay number as a string. <code>sweep(0)</code> is empty.</p>
""",
    rs_stub='''/// Diagnostic labels for relays 1..=n.
fn sweep(n: u32) -> Vec<String> {
    // TODO
    (1..=n).map(|k| k.to_string()).collect()
}
''',
    rs_reference='''/// Diagnostic labels for relays 1..=n.
fn sweep(n: u32) -> Vec<String> {
    (1..=n)
        .map(|k| match (k % 3, k % 5) {
            (0, 0) => "coolant-plasma".to_string(),
            (0, _) => "coolant".to_string(),
            (_, 0) => "plasma".to_string(),
            _ => k.to_string(),
        })
        .collect()
}
''',
    rs_checker=rs_cases("sweep", [
        (["5"], 'vec!["1", "2", "coolant", "4", "plasma"]'),
        (["15"], 'vec!["1", "2", "coolant", "4", "plasma", "coolant", "7", "8", "coolant", "plasma", "11", "coolant", "13", "14", "coolant-plasma"]'),
        (["3"], 'vec!["1", "2", "coolant"]'),
        (["0"], 'Vec::<&str>::new()'),
        (["30"], 'vec!["1", "2", "coolant", "4", "plasma", "coolant", "7", "8", "coolant", "plasma", "11", "coolant", "13", "14", "coolant-plasma", "16", "17", "coolant", "19", "plasma", "coolant", "22", "23", "coolant", "plasma", "26", "coolant", "28", "29", "coolant-plasma"]'),
    ]),
)
