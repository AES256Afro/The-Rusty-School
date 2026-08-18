"""Season 3: First Contact.

Functions, structured data, parsing. Ops, Science, and at the end, the
Tactical station, which is where the ship starts refusing bad input.
"""

from .helpers import _m, py_cases, rs_cases

# -------------------------------------------------------------- 17
_m(
    season=3, num=17, slug="17-crew-directory", id="bridge-s3m17", station="ops",
    title="The Crew Directory", stardate="Stardate 55131.0",
    crew=["dubois", "tkala"],
    blurb="A signal on long-range sensors. The Captain wants every lieutenant on the "
          "bridge, and the directory cannot say who they are.",
    briefing="""
<p>Lt. Skree has confirmed the long-range contact is artificial, slow, and not
responding to hails. The Captain has asked for every officer of a given rank to report
to the bridge, and the crew directory has responded by listing everyone, which is not
what he asked and is also, in the Chief's words, "just the crew".</p>

<p>The directory holds each person as a name and a rank. Given a rank, it should return
the names of everyone holding it, in the order they appear in the directory. That is
the whole request. The Captain has been told it will take five minutes and is standing
behind you.</p>
""",
    debrief="""
<p>Four lieutenants on the bridge, in directory order. The Captain has thanked you and
then asked whether the directory could also tell him who is on shift, which it cannot,
and which he has written down for later.</p>
""",
    objectives=[
        "Everyone of one rank, in directory order",
        "A rank held by exactly one person",
        "A rank held by nobody: an empty result",
        "Names are returned, not the whole records",
        "An empty directory",
    ],
    hint="Loop over the records, and for each one whose rank matches, keep the name. In "
         "Python that is a comprehension with a condition; in Rust, "
         "<code>filter</code> then <code>map</code>.",
    py_spec="""
<p>Write <code>find_by_rank(crew, rank)</code>: <code>crew</code> is a list of
<code>(name, rank)</code> tuples. Return a list of the <em>names</em> whose rank equals
<code>rank</code>, in the order they appear.</p>
""",
    py_stub='''def find_by_rank(crew, rank):
    """Names of everyone holding `rank`, in directory order."""
    # TODO
    return crew
''',
    py_reference='''def find_by_rank(crew, rank):
    """Names of everyone holding `rank`, in directory order."""
    return [name for name, r in crew if r == rank]
''',
    py_checker=py_cases("find_by_rank", [
        (([("Skree", "Lieutenant"), ("Tannenbaum", "Ensign"), ("Okafor", "Lieutenant"), ("Ng", "Lieutenant")], "Lieutenant"),
         ["Skree", "Okafor", "Ng"]),
        (([("Skree", "Lieutenant"), ("Tannenbaum", "Ensign")], "Ensign"), ["Tannenbaum"]),
        (([("Skree", "Lieutenant"), ("Tannenbaum", "Ensign")], "Admiral"), []),
        (([("Raghunathan", "Commander")], "Commander"), ["Raghunathan"]),
        (([], "Ensign"), []),
    ]),
    rs_spec="""
<p>Write <code>find_by_rank(crew: &amp;[(&amp;str, &amp;str)], rank: &amp;str) -&gt;
Vec&lt;String&gt;</code>: each record is <code>(name, rank)</code>. Return the
<em>names</em> whose rank equals <code>rank</code>, in the order they appear.</p>
""",
    rs_stub='''/// Names of everyone holding `rank`, in directory order.
fn find_by_rank(crew: &[(&str, &str)], rank: &str) -> Vec<String> {
    // TODO
    crew.iter().map(|(name, _)| name.to_string()).collect()
}
''',
    rs_reference='''/// Names of everyone holding `rank`, in directory order.
fn find_by_rank(crew: &[(&str, &str)], rank: &str) -> Vec<String> {
    crew.iter()
        .filter(|(_, r)| *r == rank)
        .map(|(name, _)| name.to_string())
        .collect()
}
''',
    rs_checker=rs_cases("find_by_rank", [
        (['&[("Skree", "Lieutenant"), ("Tannenbaum", "Ensign"), ("Okafor", "Lieutenant"), ("Ng", "Lieutenant")]', '"Lieutenant"'],
         'vec!["Skree", "Okafor", "Ng"]'),
        (['&[("Skree", "Lieutenant"), ("Tannenbaum", "Ensign")]', '"Ensign"'], 'vec!["Tannenbaum"]'),
        (['&[("Skree", "Lieutenant"), ("Tannenbaum", "Ensign")]', '"Admiral"'], 'Vec::<&str>::new()'),
        (['&[("Raghunathan", "Commander")]', '"Commander"'], 'vec!["Raghunathan"]'),
        (['&[]', '"Ensign"'], 'Vec::<&str>::new()'),
    ]),
)

# -------------------------------------------------------------- 18
_m(
    season=3, num=18, slug="18-parsing-the-log", id="bridge-s3m18", station="science",
    title="Parsing the Log", stardate="Stardate 55132.6",
    crew=["skree", "raghunathan"],
    blurb="The contact's transmission is a text log, one line per entry, pipes between "
          "the fields. Some messages contain pipes.",
    briefing="""
<p>The contact is transmitting. It is a maintenance log, in a format we recognise,
because it is ours: a stardate, a level, and a message, separated by pipe characters.
Lt. Skree wants each line broken into its three parts so the analysis suite can read
it.</p>

<p>Commander Raghunathan, reading over Skree's shoulder, has pointed at a line whose
message reads <em>"pressure|flow mismatch"</em> and asked what happens to <em>that</em>
pipe. Skree has gone quiet. It should stay in the message. Only the first two pipes
separate fields; anything after them is message, pipes and all.</p>
""",
    debrief="""
<p>Every line parses, including the one with the pipe in it. The log is nineteen years
old and belongs to a vessel with the same hull number as the Maggie. Skree has said
"hm" again. Commander Raghunathan has stopped reading and gone to check something in
Engineering.</p>
""",
    objectives=[
        "A normal line splits into stardate, level and message",
        "The stardate is a number, not text",
        "A message containing a pipe is kept whole",
        "Leading and trailing whitespace on the message is trimmed",
        "A different level and an empty message",
    ],
    hint="Split on the pipe, but only twice: Python's <code>split('|', 2)</code>, Rust's "
         "<code>splitn(3, '|')</code>. Then convert the first part to a number and trim "
         "the last one.",
    py_spec="""
<p>Write <code>parse_entry(line)</code>: <code>line</code> looks like
<code>"55103.2|WARN|coolant low"</code>. Return a dict with keys <code>"stardate"</code>
(a float), <code>"level"</code> (a string) and <code>"message"</code> (a string, whitespace
trimmed at both ends). Only the <strong>first two</strong> pipes separate fields; the
message may contain more.</p>
""",
    py_stub='''def parse_entry(line):
    """'55103.2|WARN|coolant low' -> {"stardate": 55103.2, "level": "WARN", "message": "coolant low"}"""
    # TODO
    return {}
''',
    py_reference='''def parse_entry(line):
    """'55103.2|WARN|coolant low' -> {"stardate": 55103.2, "level": "WARN", "message": "coolant low"}"""
    stardate, level, message = line.split("|", 2)
    return {"stardate": float(stardate), "level": level, "message": message.strip()}
''',
    py_checker=py_cases("parse_entry", [
        (("55103.2|WARN|coolant low",), {"stardate": 55103.2, "level": "WARN", "message": "coolant low"}),
        (("55110.0|INFO|nominal",), {"stardate": 55110.0, "level": "INFO", "message": "nominal"}),
        (("55111.5|WARN|pressure|flow mismatch",), {"stardate": 55111.5, "level": "WARN", "message": "pressure|flow mismatch"}),
        (("55112.1|ERROR|  hull breach deck 3  ",), {"stardate": 55112.1, "level": "ERROR", "message": "hull breach deck 3"}),
        (("55113.9|DEBUG|",), {"stardate": 55113.9, "level": "DEBUG", "message": ""}),
    ]),
    rs_spec="""
<p>Keep the <code>LogEntry</code> struct as given. Write
<code>parse_entry(line: &amp;str) -&gt; LogEntry</code>: <code>line</code> looks like
<code>"55103.2|WARN|coolant low"</code>. The stardate is an <code>f64</code>, the level
a <code>String</code>, the message a <code>String</code> trimmed at both ends. Only the
<strong>first two</strong> pipes separate fields; the message may contain more.</p>
""",
    rs_stub='''#[derive(Debug, PartialEq)]
struct LogEntry {
    stardate: f64,
    level: String,
    message: String,
}

/// "55103.2|WARN|coolant low" -> LogEntry { 55103.2, "WARN", "coolant low" }
fn parse_entry(line: &str) -> LogEntry {
    // TODO
    LogEntry { stardate: 0.0, level: String::new(), message: line.to_string() }
}
''',
    rs_reference='''#[derive(Debug, PartialEq)]
struct LogEntry {
    stardate: f64,
    level: String,
    message: String,
}

/// "55103.2|WARN|coolant low" -> LogEntry { 55103.2, "WARN", "coolant low" }
fn parse_entry(line: &str) -> LogEntry {
    let mut parts = line.splitn(3, '|');
    let stardate = parts.next().unwrap_or("0").trim().parse().unwrap_or(0.0);
    let level = parts.next().unwrap_or("").to_string();
    let message = parts.next().unwrap_or("").trim().to_string();
    LogEntry { stardate, level, message }
}
''',
    rs_checker=rs_cases("parse_entry", [
        (['"55103.2|WARN|coolant low"'], 'LogEntry { stardate: 55103.2, level: "WARN".into(), message: "coolant low".into() }'),
        (['"55110.0|INFO|nominal"'], 'LogEntry { stardate: 55110.0, level: "INFO".into(), message: "nominal".into() }'),
        (['"55111.5|WARN|pressure|flow mismatch"'], 'LogEntry { stardate: 55111.5, level: "WARN".into(), message: "pressure|flow mismatch".into() }'),
        (['"55112.1|ERROR|  hull breach deck 3  "'], 'LogEntry { stardate: 55112.1, level: "ERROR".into(), message: "hull breach deck 3".into() }'),
        (['"55113.9|DEBUG|"'], 'LogEntry { stardate: 55113.9, level: "DEBUG".into(), message: "".into() }'),
    ]),
)

# -------------------------------------------------------------- 19
_m(
    season=3, num=19, slug="19-reconciliation", id="bridge-s3m19", station="ops",
    title="Inventory Reconciliation", stardate="Stardate 55134.1",
    crew=["tkala", "tannenbaum"],
    blurb="What Stores thinks it has and what Stores actually has are two different "
          "lists. Chief T'Kala wants the differences, and only the differences.",
    briefing="""
<p>Chief T'Kala has done a physical count of Stores, with a torch, and would like it
compared against the computer's idea of Stores. She wants a list of every item where the
two disagree, with how far off the computer is: actual minus expected, so a shortfall is
negative. Items that agree should not appear at all; she does not need to be told what
is fine.</p>

<p>Items in one list but not the other count as zero in the list they are missing from.
Ensign Tannenbaum asked whether that was "a bit harsh". The Chief said the torch does
not lie.</p>
""",
    debrief="""
<p>Three discrepancies. Two are rounding. One is a case of forty coffee filters that
does not exist on any manifest and that nobody will explain. Chief T'Kala has logged it
as "found property" and moved it nearer the replicator.</p>
""",
    objectives=[
        "Items that differ, with actual minus expected, sorted by name",
        "Items that agree are left out entirely",
        "An item missing from the actual count is a shortfall of the full amount",
        "An item missing from the expected list is a surplus of the full amount",
        "Two identical inventories produce nothing",
    ],
    hint="Take the union of the names from both sides, look each up with a default of "
         "zero, and keep the ones where the numbers differ. Sort by name at the end so "
         "the order is stable.",
    py_spec="""
<p>Write <code>reconcile(expected, actual)</code>: both are dicts of item name to count.
Return a list of <code>(name, difference)</code> tuples for every item whose counts
differ, where <code>difference</code> is <code>actual - expected</code>. A name absent
from either dict counts as 0 there. Sort the result by name.</p>
""",
    py_stub='''def reconcile(expected, actual):
    """[(name, actual - expected)] for every disagreement, sorted by name."""
    # TODO
    return []
''',
    py_reference='''def reconcile(expected, actual):
    """[(name, actual - expected)] for every disagreement, sorted by name."""
    names = set(expected) | set(actual)
    out = []
    for name in sorted(names):
        diff = actual.get(name, 0) - expected.get(name, 0)
        if diff != 0:
            out.append((name, diff))
    return out
''',
    py_checker=py_cases("reconcile", [
        (({"coil": 10, "gasket": 4, "torch": 2}, {"coil": 8, "gasket": 4, "torch": 5}), [("coil", -2), ("torch", 3)]),
        (({"coil": 10, "gasket": 4}, {"coil": 10, "gasket": 4, "torch": 0}), []),
        (({"coil": 10, "torch": 3}, {"coil": 10}), [("torch", -3)]),
        (({"coil": 10}, {"coil": 10, "filters": 40}), [("filters", 40)]),
        (({"coil": 1, "gasket": 1}, {"gasket": 1, "coil": 1}), []),
    ]),
    rs_spec="""
<p>Write <code>reconcile(expected: &amp;[(&amp;str, i32)], actual: &amp;[(&amp;str, i32)])
-&gt; Vec&lt;(String, i32)&gt;</code>: each input is a list of <code>(name, count)</code>
with unique names. Return <code>(name, actual - expected)</code> for every item whose
counts differ. A name absent from either side counts as 0 there. Sort by name.</p>
""",
    rs_stub='''/// (name, actual - expected) for every disagreement, sorted by name.
fn reconcile(expected: &[(&str, i32)], actual: &[(&str, i32)]) -> Vec<(String, i32)> {
    // TODO
    Vec::new()
}
''',
    rs_reference='''use std::collections::BTreeMap;

/// (name, actual - expected) for every disagreement, sorted by name.
fn reconcile(expected: &[(&str, i32)], actual: &[(&str, i32)]) -> Vec<(String, i32)> {
    let mut diffs: BTreeMap<&str, i32> = BTreeMap::new();
    for &(name, n) in expected {
        *diffs.entry(name).or_insert(0) -= n;
    }
    for &(name, n) in actual {
        *diffs.entry(name).or_insert(0) += n;
    }
    diffs.into_iter()
        .filter(|&(_, d)| d != 0)
        .map(|(name, d)| (name.to_string(), d))
        .collect()
}
''',
    rs_checker=rs_cases("reconcile", [
        (['&[("coil", 10), ("gasket", 4), ("torch", 2)]', '&[("coil", 8), ("gasket", 4), ("torch", 5)]'],
         'vec![("coil".to_string(), -2), ("torch".to_string(), 3)]'),
        (['&[("coil", 10), ("gasket", 4)]', '&[("coil", 10), ("gasket", 4), ("torch", 0)]'], 'Vec::<(String, i32)>::new()'),
        (['&[("coil", 10), ("torch", 3)]', '&[("coil", 10)]'], 'vec![("torch".to_string(), -3)]'),
        (['&[("coil", 10)]', '&[("coil", 10), ("filters", 40)]'], 'vec![("filters".to_string(), 40)]'),
        (['&[("coil", 1), ("gasket", 1)]', '&[("gasket", 1), ("coil", 1)]'], 'Vec::<(String, i32)>::new()'),
    ]),
)

# -------------------------------------------------------------- 20
_m(
    season=3, num=20, slug="20-coordinates", id="bridge-s3m20", station="science",
    title="Coordinates, With Feeling", stardate="Stardate 55135.7",
    crew=["skree", "dubois"],
    blurb="The contact's position arrives as text. Some of it is not a position.",
    briefing="""
<p>The contact is sending its position as a pair of numbers in a string, comma
separated, with whatever spacing its transmitter felt like. <em>"12.5, -3.25"</em> is a
position. <em>"12.5,-3.25"</em> is the same position. <em>"twelve, three"</em> is not a
position, and neither is <em>"12.5"</em> on its own, and Lt. Skree wants those rejected
rather than guessed at.</p>

<p>The Captain has asked whether "rejected" means the ship will crash. It means the
function returns nothing, and the caller decides. The Captain has said "good" and gone
back to looking at the viewscreen, where the contact is now visible as a dot.</p>
""",
    debrief="""
<p>The contact is at 12.5 by minus 3.25, relative, and closing very slowly. Lt. Skree
has confirmed it is a ship. Skree has also confirmed, after a pause, that its transponder
reads <em>UES Magnanimous</em>. Commander Raghunathan has come back to the bridge.</p>
""",
    objectives=[
        "A well-formed pair with a space after the comma",
        "The same pair with no spaces at all",
        "Words instead of numbers are rejected",
        "A single number with no comma is rejected",
        "Extra whitespace around either number is fine",
    ],
    hint="Split on the comma; if you do not get exactly two parts, reject. Trim each "
         "part and try to convert it to a number; if either fails, reject. Python: catch "
         "the ValueError. Rust: <code>parse().ok()</code> and the <code>?</code> operator "
         "inside a function returning <code>Option</code>.",
    py_spec="""
<p>Write <code>parse_coords(text)</code>: return a tuple <code>(x, y)</code> of floats
parsed from <code>"x, y"</code>, tolerating any whitespace around the numbers. Return
<code>None</code> if the text is not exactly two numbers separated by one comma.</p>
""",
    py_stub='''def parse_coords(text):
    """'12.5, -3.25' -> (12.5, -3.25); anything malformed -> None."""
    # TODO
    return None
''',
    py_reference='''def parse_coords(text):
    """'12.5, -3.25' -> (12.5, -3.25); anything malformed -> None."""
    parts = text.split(",")
    if len(parts) != 2:
        return None
    try:
        return (float(parts[0].strip()), float(parts[1].strip()))
    except ValueError:
        return None
''',
    py_checker=py_cases("parse_coords", [
        (("12.5, -3.25",), (12.5, -3.25)),
        (("12.5,-3.25",), (12.5, -3.25)),
        (("twelve, three",), None),
        (("12.5",), None),
        (("  0.0 ,   7  ",), (0.0, 7.0)),
    ], check="(_got is None and _want is None) or (_got is not None and _want is not None and abs(_got[0]-_want[0]) < 1e-9 and abs(_got[1]-_want[1]) < 1e-9)"),
    rs_spec="""
<p>Write <code>parse_coords(text: &amp;str) -&gt; Option&lt;(f64, f64)&gt;</code>: parse
<code>"x, y"</code> into a pair, tolerating any whitespace around the numbers. Return
<code>None</code> if the text is not exactly two numbers separated by one comma.</p>
""",
    rs_stub='''/// "12.5, -3.25" -> Some((12.5, -3.25)); anything malformed -> None.
fn parse_coords(text: &str) -> Option<(f64, f64)> {
    // TODO
    None
}
''',
    rs_reference='''/// "12.5, -3.25" -> Some((12.5, -3.25)); anything malformed -> None.
fn parse_coords(text: &str) -> Option<(f64, f64)> {
    let mut parts = text.split(',');
    let x = parts.next()?.trim().parse::<f64>().ok()?;
    let y = parts.next()?.trim().parse::<f64>().ok()?;
    if parts.next().is_some() {
        return None;
    }
    Some((x, y))
}
''',
    rs_checker=rs_cases("parse_coords", [
        (['"12.5, -3.25"'], "Some((12.5, -3.25))"),
        (['"12.5,-3.25"'], "Some((12.5, -3.25))"),
        (['"twelve, three"'], "None"),
        (['"12.5"'], "None"),
        (['"  0.0 ,   7  "'], "Some((0.0, 7.0))"),
    ], check="match (got, want) { (Some((a, b)), Some((c, d))) => (a - c).abs() < 1e-9 && (b - d).abs() < 1e-9, (None, None) => true, _ => false }",
       want_ty="Option<(f64, f64)>"),
)

# -------------------------------------------------------------- 21
_m(
    season=3, num=21, slug="21-duty-roster", id="bridge-s3m21", station="ops",
    title="The Duty Roster", stardate="Stardate 55137.3",
    crew=["tkala", "tannenbaum"],
    blurb="Who is on watch after Ensign Tannenbaum? The roster says 'nobody', "
          "which is how you get an unwatched bridge.",
    briefing="""
<p>The watch rotation is a list of names, in order, and after the last name it goes back
to the first. This is what a rotation is. The current routine, asked who follows the
last name on the list, returns nothing, and on two occasions this month the bridge has
been unattended for a full shift, during one of which Gerald was, technically, in
command.</p>

<p>Chief T'Kala wants: given the roster and the person currently on watch, the next
person, wrapping around at the end. If the current person is not on the roster at all,
return nothing, because that is a different problem and she wants to hear about it.</p>
""",
    debrief="""
<p>The rotation wraps. Nobody is following Gerald any more, and Gerald has been formally
relieved of command with a small ceremony that Chief T'Kala insists was "not a joke".
The contact is now close enough to see hull plating. It has the same dent as ours.</p>
""",
    objectives=[
        "The next name in the middle of the roster",
        "After the last name comes the first",
        "A roster of one wraps to itself",
        "Someone not on the roster: nothing",
        "An empty roster: nothing",
    ],
    hint="Find the position of the current name. If it is not there, return nothing. "
         "Otherwise the answer is at position plus one, <em>modulo the length</em>, "
         "which is what makes the last one wrap to the first.",
    py_spec="""
<p>Write <code>next_on_duty(roster, current)</code>: <code>roster</code> is a list of
names in rotation order. Return the name that follows <code>current</code>, wrapping from
the last name back to the first. Return <code>None</code> if <code>current</code> is
not in the roster.</p>
""",
    py_stub='''def next_on_duty(roster, current):
    """Who follows `current` in the rotation? Wraps around. None if not listed."""
    # TODO
    i = roster.index(current) if current in roster else -1
    return roster[i + 1] if 0 <= i + 1 < len(roster) else None
''',
    py_reference='''def next_on_duty(roster, current):
    """Who follows `current` in the rotation? Wraps around. None if not listed."""
    if current not in roster:
        return None
    i = roster.index(current)
    return roster[(i + 1) % len(roster)]
''',
    py_checker=py_cases("next_on_duty", [
        ((["Skree", "Tannenbaum", "Okafor", "Ng"], "Tannenbaum"), "Okafor"),
        ((["Skree", "Tannenbaum", "Okafor", "Ng"], "Ng"), "Skree"),
        ((["T'Kala"], "T'Kala"), "T'Kala"),
        ((["Skree", "Tannenbaum"], "Gerald"), None),
        (([], "Skree"), None),
    ]),
    rs_spec="""
<p>Write <code>next_on_duty(roster: &amp;[&amp;str], current: &amp;str) -&gt;
Option&lt;String&gt;</code>: the name that follows <code>current</code> in rotation
order, wrapping from the last back to the first. <code>None</code> if
<code>current</code> is not in the roster.</p>
""",
    rs_stub='''/// Who follows `current` in the rotation? Wraps around. None if not listed.
fn next_on_duty(roster: &[&str], current: &str) -> Option<String> {
    // TODO
    let i = roster.iter().position(|&n| n == current)?;
    roster.get(i + 1).map(|s| s.to_string())
}
''',
    rs_reference='''/// Who follows `current` in the rotation? Wraps around. None if not listed.
fn next_on_duty(roster: &[&str], current: &str) -> Option<String> {
    let i = roster.iter().position(|&n| n == current)?;
    Some(roster[(i + 1) % roster.len()].to_string())
}
''',
    rs_checker=rs_cases("next_on_duty", [
        (['&["Skree", "Tannenbaum", "Okafor", "Ng"]', '"Tannenbaum"'], 'Some("Okafor".to_string())'),
        (['&["Skree", "Tannenbaum", "Okafor", "Ng"]', '"Ng"'], 'Some("Skree".to_string())'),
        (['&["T\'Kala"]', '"T\'Kala"'], 'Some("T\'Kala".to_string())'),
        (['&["Skree", "Tannenbaum"]', '"Gerald"'], "None"),
        (['&[]', '"Skree"'], "None"),
    ]),
)

# -------------------------------------------------------------- 22
_m(
    season=3, num=22, slug="22-overlapping-watches", id="bridge-s3m22", station="science",
    title="Overlapping Watches", stardate="Stardate 55138.8",
    crew=["skree", "raghunathan"],
    blurb="Two stardate ranges. Do they overlap? The answer at the exact edge has "
          "caused an argument.",
    briefing="""
<p>To line up the other ship's log with ours, Lt. Skree needs to know whether two
stardate ranges overlap. Each range is a start and an end, and both ends are
<em>inclusive</em>: a range from 10 to 12 includes 12.</p>

<p>The argument is about ranges that touch. Skree says a range ending at 12 and a range
starting at 12 share a moment and therefore overlap. Commander Raghunathan agrees, but
wanted it written down, because "the last time we didn't write it down, we got a
turbolift that stops one deck short". It is written down. Touching counts.</p>
""",
    debrief="""
<p>The two logs line up. There is a nineteen-year gap in the middle, and on our side of
the gap, an entry that reads <em>"pressure|flow mismatch"</em>. On theirs, the same
entry, the same stardate, the same handwriting. Skree has removed the word "pending"
from the file entirely.</p>
""",
    objectives=[
        "Clearly overlapping ranges",
        "Clearly separate ranges",
        "Ranges that touch at exactly one point overlap, because ends are inclusive",
        "One range entirely inside the other",
        "The same overlap in the other order",
    ],
    hint="Two inclusive ranges overlap when each one starts no later than the other "
         "ends: <code>a_start &lt;= b_end and b_start &lt;= a_end</code>. Getting the "
         "touching case right is a matter of <code>&lt;=</code> versus <code>&lt;</code>.",
    py_spec="""
<p>Write <code>overlaps(a, b)</code>: <code>a</code> and <code>b</code> are
<code>(start, end)</code> tuples with <code>start &lt;= end</code>, both ends
<strong>inclusive</strong>. Return <code>True</code> if the ranges share at least one
point.</p>
""",
    py_stub='''def overlaps(a, b):
    """Do two inclusive (start, end) ranges share at least one point?"""
    # TODO
    return False
''',
    py_reference='''def overlaps(a, b):
    """Do two inclusive (start, end) ranges share at least one point?"""
    return a[0] <= b[1] and b[0] <= a[1]
''',
    py_checker=py_cases("overlaps", [
        (((10.0, 15.0), (12.0, 20.0)), True),
        (((10.0, 12.0), (14.0, 16.0)), False),
        (((10.0, 12.0), (12.0, 16.0)), True),
        (((10.0, 20.0), (13.0, 14.0)), True),
        (((12.0, 20.0), (10.0, 15.0)), True),
    ]),
    rs_spec="""
<p>Write <code>overlaps(a: (f64, f64), b: (f64, f64)) -&gt; bool</code>: each is
<code>(start, end)</code> with <code>start &lt;= end</code>, both ends
<strong>inclusive</strong>. Return <code>true</code> if the ranges share at least one
point.</p>
""",
    rs_stub='''/// Do two inclusive (start, end) ranges share at least one point?
fn overlaps(a: (f64, f64), b: (f64, f64)) -> bool {
    // TODO
    false
}
''',
    rs_reference='''/// Do two inclusive (start, end) ranges share at least one point?
fn overlaps(a: (f64, f64), b: (f64, f64)) -> bool {
    a.0 <= b.1 && b.0 <= a.1
}
''',
    rs_checker=rs_cases("overlaps", [
        (["(10.0, 15.0)", "(12.0, 20.0)"], "true"),
        (["(10.0, 12.0)", "(14.0, 16.0)"], "false"),
        (["(10.0, 12.0)", "(12.0, 16.0)"], "true"),
        (["(10.0, 20.0)", "(13.0, 14.0)"], "true"),
        (["(12.0, 20.0)", "(10.0, 15.0)"], "true"),
    ]),
)

# -------------------------------------------------------------- 23
_m(
    season=3, num=23, slug="23-heading-validation", id="bridge-s3m23", station="tactical",
    title="Heading: Validated", stardate="Stardate 55140.2",
    crew=["tkala", "dubois", "tannenbaum"],
    blurb="The helm accepts any heading you type, including 'left', 400, and -12. "
          "Tactical would like it to stop doing that.",
    briefing="""
<p>Welcome to Tactical, which on this ship means the station that says <em>no</em>. Chief
T'Kala runs it, and she has a list.</p>

<p>Item one on the list: the helm accepts any heading a person types. Yesterday it
accepted <em>"left"</em>. Last week it accepted 400, which it treated as 40, and -12,
which it treated as a mood. A heading is a whole number from 0 to 359, and the Chief
wants text that is anything else to be refused: not corrected, not guessed at, refused,
so the person at the helm has to try again. Whitespace around a valid number is fine.
Ensign Tannenbaum typed most of the examples.</p>
""",
    debrief="""
<p>The helm refuses "left". It refuses 400. It refuses -12, and it refuses "12 degrees",
and Ensign Tannenbaum has stopped typing things into it to see what happens. The other
Magnanimous is holding station at heading 180, exactly facing us. Chief T'Kala has quietly
brought the shields up.</p>
""",
    objectives=[
        "A valid heading is accepted",
        "Whitespace around a valid heading is fine",
        "Words are refused",
        "360 and above are refused, not wrapped",
        "Negative numbers are refused",
    ],
    hint="Trim, then try to convert to a whole number; if that fails, refuse. Then check "
         "the range 0 to 359 and refuse anything outside it. Rust's "
         "<code>parse::&lt;u16&gt;()</code> already refuses negatives, and "
         "<code>.ok()?</code> makes the whole thing three lines.",
    py_spec="""
<p>Write <code>parse_heading(text)</code>: return the heading as an <code>int</code> if
<code>text</code> is a whole number from 0 to 359 (whitespace around it allowed).
Otherwise return <code>None</code>. Do not wrap or clamp: <code>"400"</code> is refused,
not turned into 40.</p>
""",
    py_stub='''def parse_heading(text):
    """A whole number 0..359 as an int, or None for anything else."""
    # TODO: this accepts far too much.
    try:
        return int(float(text)) % 360
    except ValueError:
        return None
''',
    py_reference='''def parse_heading(text):
    """A whole number 0..359 as an int, or None for anything else."""
    try:
        heading = int(text.strip())
    except ValueError:
        return None
    if 0 <= heading <= 359:
        return heading
    return None
''',
    py_checker=py_cases("parse_heading", [
        (("180",), 180), (("  45 ",), 45), (("left",), None), (("400",), None), (("-12",), None),
    ]),
    rs_spec="""
<p>Write <code>parse_heading(text: &amp;str) -&gt; Option&lt;u16&gt;</code>: the heading
if <code>text</code> is a whole number from 0 to 359 (whitespace around it allowed).
Otherwise <code>None</code>. Do not wrap or clamp: <code>"400"</code> is refused, not
turned into 40.</p>
""",
    rs_stub='''/// A whole number 0..=359, or None for anything else.
fn parse_heading(text: &str) -> Option<u16> {
    // TODO: this accepts far too much.
    text.trim().parse::<f64>().ok().map(|h| (h as i64).rem_euclid(360) as u16)
}
''',
    rs_reference='''/// A whole number 0..=359, or None for anything else.
fn parse_heading(text: &str) -> Option<u16> {
    let heading = text.trim().parse::<u16>().ok()?;
    if heading <= 359 { Some(heading) } else { None }
}
''',
    rs_checker=rs_cases("parse_heading", [
        (['"180"'], "Some(180)"), (['"  45 "'], "Some(45)"), (['"left"'], "None"),
        (['"400"'], "None"), (['"-12"'], "None"),
    ]),
)

# -------------------------------------------------------------- 24
_m(
    season=3, num=24, slug="24-transporter-safety", id="bridge-s3m24", station="tactical",
    title="Transporter Safety", stardate="Stardate 55141.5",
    crew=["tkala", "raghunathan", "dubois", "skree"],
    blurb="Somebody wants to beam across to the other ship. The transporter should "
          "have opinions about that, in a specific order.",
    briefing="""
<p>The other Magnanimous has opened a channel. There is nobody on it, only their
computer, and their computer is asking for a technician. Commander Raghunathan has
volunteered, and Chief T'Kala has responded by writing down, in order, every reason
the transporter should refuse to send her.</p>

<p>Shields up: refuse, and say so, because that one kills you. Cargo over five hundred
kilos: refuse, the pattern buffer will not hold it. Lock quality below 0.9: refuse,
because ninety percent of a Commander is not a Commander. The transporter must give the
<em>first</em> applicable reason in that order, or, if there is none, permit the
transport. The Captain has asked whether "permit" means "should". It does not.</p>
""",
    debrief="""
<p>Shields down, 71 kilograms, lock at 0.98: permitted. Commander Raghunathan is
standing on the other ship's transporter pad, and the first thing she has said over the
channel is that it smells the same. The second thing is that their coffee replicator is
working perfectly.</p>

<p><strong>First Contact complete.</strong> The Anomaly is open, and it is going to be
about what, precisely, is on the other ship's computer.</p>
""",
    objectives=[
        "Shields up is refused first, whatever else is true",
        "Too heavy is refused when shields are down",
        "A weak lock is refused when the mass is fine",
        "Everything in order: permitted",
        "Exactly 500 kilograms and a lock of exactly 0.9 are both still fine",
    ],
    hint="Three checks in the stated order, each returning immediately with its reason. "
         "The last objective is the boundary: 500 is not over 500, and 0.9 is not below "
         "0.9. Python returns the reason or <code>None</code>; Rust returns a "
         "<code>Result</code> where <code>Ok(())</code> is permission.",
    py_spec="""
<p>Write <code>transport_refusal(shields_up, mass_kg, lock_quality)</code>. Return the
<strong>first</strong> applicable reason as a string, checking in this order:
<code>"shields are up"</code> if <code>shields_up</code>; <code>"too heavy"</code> if
<code>mass_kg</code> is over 500; <code>"weak lock"</code> if <code>lock_quality</code>
is below 0.9. If none apply, return <code>None</code>: the transport is permitted.</p>
""",
    py_stub='''def transport_refusal(shields_up, mass_kg, lock_quality):
    """The first reason to refuse, in the Chief's order, or None to permit."""
    # TODO
    return None
''',
    py_reference='''def transport_refusal(shields_up, mass_kg, lock_quality):
    """The first reason to refuse, in the Chief's order, or None to permit."""
    if shields_up:
        return "shields are up"
    if mass_kg > 500:
        return "too heavy"
    if lock_quality < 0.9:
        return "weak lock"
    return None
''',
    py_checker=py_cases("transport_refusal", [
        ((True, 9000, 0.1), "shields are up"),
        ((False, 501, 0.99), "too heavy"),
        ((False, 71, 0.5), "weak lock"),
        ((False, 71, 0.98), None),
        ((False, 500, 0.9), None),
    ]),
    rs_spec="""
<p>Write <code>transport_check(shields_up: bool, mass_kg: u32, lock_quality: f64) -&gt;
Result&lt;(), &amp;'static str&gt;</code>. Return the <strong>first</strong> applicable
refusal, checking in this order: <code>Err("shields are up")</code> if
<code>shields_up</code>; <code>Err("too heavy")</code> if <code>mass_kg</code> is over
500; <code>Err("weak lock")</code> if <code>lock_quality</code> is below 0.9. If none
apply, return <code>Ok(())</code>: the transport is permitted.</p>
""",
    rs_stub='''/// The first reason to refuse, in the Chief's order, or Ok(()) to permit.
fn transport_check(shields_up: bool, mass_kg: u32, lock_quality: f64) -> Result<(), &'static str> {
    // TODO
    Ok(())
}
''',
    rs_reference='''/// The first reason to refuse, in the Chief's order, or Ok(()) to permit.
fn transport_check(shields_up: bool, mass_kg: u32, lock_quality: f64) -> Result<(), &'static str> {
    if shields_up {
        return Err("shields are up");
    }
    if mass_kg > 500 {
        return Err("too heavy");
    }
    if lock_quality < 0.9 {
        return Err("weak lock");
    }
    Ok(())
}
''',
    rs_checker=rs_cases("transport_check", [
        (["true", "9000", "0.1"], 'Err("shields are up")'),
        (["false", "501", "0.99"], 'Err("too heavy")'),
        (["false", "71", "0.5"], 'Err("weak lock")'),
        (["false", "71", "0.98"], "Ok(())"),
        (["false", "500", "0.9"], "Ok(())"),
    ]),
)
