"""Season 6: Terminus.

Four long missions, eight objectives each, several functions apiece.
Every station at once. And an ending, because the whole comedy register
only works if the show is willing to mean it occasionally.
"""

from .helpers import _m, py_custom, rs_custom

# -------------------------------------------------------------- 41
_m(
    season=6, num=41, slug="41-the-manifold", id="bridge-s6m41", station="engineering",
    title="The Manifold", stardate="Stardate 55168.0",
    crew=["raghunathan", "skree", "dubois", "tannenbaum"],
    minutes=45,
    blurb="Tomorrow's stardate is in both logs. The other ship's release notes say "
          "what fixed it. Now write the fix.",
    briefing="""
<p>Commander Raghunathan has read the other ship's release notes for version 1.10.3
eleven times and has finally said it out loud: <em>pressure|flow mismatch</em> is the
plasma manifold. It is the fault behind the incident nobody talks about, and it is
scheduled, according to both logs, for tomorrow. The other Magnanimous did not have the
fix in time. It has brought it back.</p>

<p>The fix is a validator. Flow through the manifold should track pressure: the expected
flow is four times the square root of the pressure, and a reading whose flow is more than
ten percent off that expectation is a mismatch. One mismatch is noise. Two are a
warning. Three in a row is the incident, and the core must be told before it happens.
This is three functions, eight objectives, and the reason the other ship came. Ensign
Tannenbaum has asked to help and, for the first time, been told yes.</p>
""",
    debrief="""
<p>The validator is in. It flags two mismatches in the last hour of our log, neither
consecutive. Commander Raghunathan has looked at the manifold itself, with the torch,
and found the seal the notes describe. She has replaced it. It took four minutes. She has
been standing next to it since.</p>
""",
    objectives=[
        "expected_flow: four times the square root of pressure, to two places",
        "is_mismatch: a flow more than ten percent off expectation",
        "is_mismatch: exactly ten percent off is not a mismatch",
        "mismatches: the indices of every mismatched reading",
        "mismatches: no readings, no indices",
        "status: 'nominal' when nothing is wrong",
        "status: 'mismatch at N readings' otherwise",
        "status: 'critical' when three or more mismatches are consecutive",
    ],
    hint="Build the three functions on top of each other: <code>status</code> uses "
         "<code>mismatches</code>, which uses <code>is_mismatch</code>, which uses "
         "<code>expected_flow</code>. For 'consecutive', walk the indices and count a "
         "run; reset the run whenever the gap is more than one.",
    py_spec="""
<p>Three functions:</p>
<ul>
  <li><code>expected_flow(pressure)</code>: <code>4 * sqrt(pressure)</code>, rounded to two
    decimal places.</li>
  <li><code>is_mismatch(pressure, flow)</code>: <code>True</code> if <code>flow</code>
    differs from the (unrounded) expected flow by <strong>more than</strong> ten percent
    of the expected flow.</li>
  <li><code>mismatches(readings)</code>: <code>readings</code> is a list of
    <code>(pressure, flow)</code> tuples; return the list of indices that mismatch.</li>
  <li><code>status(readings)</code>: <code>"nominal"</code> if none mismatch;
    <code>"critical"</code> if three or more mismatched indices are consecutive; otherwise
    <code>"mismatch at N readings"</code> with N the count.</li>
</ul>
""",
    py_stub='''import math


def expected_flow(pressure):
    """Flow the manifold should show at this pressure: 4 * sqrt(pressure), 2 dp."""
    # TODO
    return 0.0


def is_mismatch(pressure, flow):
    """True if flow is more than 10% away from the expected flow."""
    # TODO
    return False


def mismatches(readings):
    """Indices of the (pressure, flow) readings that mismatch."""
    # TODO
    return []


def status(readings):
    """'nominal', 'critical' (3+ consecutive mismatches), or 'mismatch at N readings'."""
    # TODO
    return "nominal"
''',
    py_reference='''import math


def expected_flow(pressure):
    """Flow the manifold should show at this pressure: 4 * sqrt(pressure), 2 dp."""
    return round(4 * math.sqrt(pressure), 2)


def is_mismatch(pressure, flow):
    """True if flow is more than 10% away from the expected flow."""
    expected = 4 * math.sqrt(pressure)
    return abs(flow - expected) > 0.1 * expected + 1e-9


def mismatches(readings):
    """Indices of the (pressure, flow) readings that mismatch."""
    return [i for i, (p, f) in enumerate(readings) if is_mismatch(p, f)]


def status(readings):
    """'nominal', 'critical' (3+ consecutive mismatches), or 'mismatch at N readings'."""
    bad = mismatches(readings)
    if not bad:
        return "nominal"
    run = 1
    for a, b in zip(bad, bad[1:]):
        run = run + 1 if b == a + 1 else 1
        if run >= 3:
            return "critical"
    return f"mismatch at {len(bad)} readings"
''',
    py_checker=py_custom('''
_g = _guard(0, lambda: (expected_flow(16), expected_flow(2)), "expected_flow(16), expected_flow(2)")
if _g is not _FAILED:
    _report(0, abs(_g[0] - 16.0) < 1e-9 and abs(_g[1] - 5.66) < 1e-9, f"got {_g}, wanted (16.0, 5.66)")

_g = _guard(1, lambda: (is_mismatch(16, 18.0), is_mismatch(16, 14.0), is_mismatch(16, 16.5)), "is_mismatch at 16 with 18, 14, 16.5")
if _g is not _FAILED:
    _report(1, _g == (True, True, False), f"got {_g}, wanted (True, True, False)")

_g = _guard(2, lambda: (is_mismatch(16, 17.6), is_mismatch(16, 14.4), is_mismatch(16, 17.61)), "exactly 10% off, and just over")
if _g is not _FAILED:
    _report(2, _g == (False, False, True), f"got {_g}, wanted (False, False, True): 17.6 and 14.4 are exactly 10% off")

_r = [(16, 16.0), (16, 20.0), (25, 20.0), (25, 30.0), (9, 12.0)]
_g = _guard(3, lambda: mismatches(_r), "mismatches(...)")
if _g is not _FAILED:
    _report(3, _g == [1, 3], f"got {_g}, wanted [1, 3]")

_g = _guard(4, lambda: mismatches([]), "mismatches([])")
if _g is not _FAILED:
    _report(4, _g == [], f"got {_g}, wanted []")

_g = _guard(5, lambda: status([(16, 16.0), (25, 20.0), (9, 12.0)]), "status, all fine")
if _g is not _FAILED:
    _report(5, _g == "nominal", f"got {_g!r}, wanted 'nominal'")

_g = _guard(6, lambda: status(_r), "status, two mismatches, not consecutive")
if _g is not _FAILED:
    _report(6, _g == "mismatch at 2 readings", f"got {_g!r}, wanted 'mismatch at 2 readings'")

_g = _guard(7, lambda: status([(16, 16.0), (16, 30.0), (16, 30.0), (16, 30.0), (16, 16.0)]), "status, three in a row")
if _g is not _FAILED:
    _report(7, _g == "critical", f"got {_g!r}, wanted 'critical'")
'''),
    rs_spec="""
<p>Four functions:</p>
<ul>
  <li><code>expected_flow(pressure: f64) -&gt; f64</code>: <code>4 * sqrt(pressure)</code>,
    rounded to two decimal places.</li>
  <li><code>is_mismatch(pressure: f64, flow: f64) -&gt; bool</code>: true if
    <code>flow</code> differs from the (unrounded) expected flow by <strong>more
    than</strong> ten percent of it.</li>
  <li><code>mismatches(readings: &amp;[(f64, f64)]) -&gt; Vec&lt;usize&gt;</code>: the
    indices of readings that mismatch.</li>
  <li><code>status(readings: &amp;[(f64, f64)]) -&gt; String</code>: <code>"nominal"</code>
    if none; <code>"critical"</code> if three or more mismatched indices are consecutive;
    otherwise <code>"mismatch at N readings"</code>.</li>
</ul>
""",
    rs_stub='''/// Flow the manifold should show at this pressure: 4 * sqrt(pressure), 2 dp.
fn expected_flow(pressure: f64) -> f64 {
    // TODO
    0.0
}

/// True if flow is more than 10% away from the expected flow.
fn is_mismatch(pressure: f64, flow: f64) -> bool {
    // TODO
    false
}

/// Indices of the (pressure, flow) readings that mismatch.
fn mismatches(readings: &[(f64, f64)]) -> Vec<usize> {
    // TODO
    Vec::new()
}

/// "nominal", "critical" (3+ consecutive mismatches), or "mismatch at N readings".
fn status(readings: &[(f64, f64)]) -> String {
    // TODO
    String::from("nominal")
}
''',
    rs_reference='''/// Flow the manifold should show at this pressure: 4 * sqrt(pressure), 2 dp.
fn expected_flow(pressure: f64) -> f64 {
    (4.0 * pressure.sqrt() * 100.0).round() / 100.0
}

/// True if flow is more than 10% away from the expected flow.
fn is_mismatch(pressure: f64, flow: f64) -> bool {
    let expected = 4.0 * pressure.sqrt();
    (flow - expected).abs() > 0.1 * expected + 1e-9
}

/// Indices of the (pressure, flow) readings that mismatch.
fn mismatches(readings: &[(f64, f64)]) -> Vec<usize> {
    readings.iter().enumerate()
        .filter(|(_, &(p, f))| is_mismatch(p, f))
        .map(|(i, _)| i)
        .collect()
}

/// "nominal", "critical" (3+ consecutive mismatches), or "mismatch at N readings".
fn status(readings: &[(f64, f64)]) -> String {
    let bad = mismatches(readings);
    if bad.is_empty() {
        return "nominal".to_string();
    }
    let mut run = 1;
    for w in bad.windows(2) {
        run = if w[1] == w[0] + 1 { run + 1 } else { 1 };
        if run >= 3 {
            return "critical".to_string();
        }
    }
    format!("mismatch at {} readings", bad.len())
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let g = (expected_flow(16.0), expected_flow(2.0));
    __report(0, (g.0 - 16.0).abs() < 1e-9 && (g.1 - 5.66).abs() < 1e-9, format!("got {:?}, wanted (16.0, 5.66)", g));

    let g = (is_mismatch(16.0, 18.0), is_mismatch(16.0, 14.0), is_mismatch(16.0, 16.5));
    __report(1, g == (true, true, false), format!("got {:?}, wanted (true, true, false)", g));

    let g = (is_mismatch(16.0, 17.6), is_mismatch(16.0, 14.4), is_mismatch(16.0, 17.61));
    __report(2, g == (false, false, true), format!("got {:?}, wanted (false, false, true): 17.6 and 14.4 are exactly 10% off", g));

    let r = [(16.0, 16.0), (16.0, 20.0), (25.0, 20.0), (25.0, 30.0), (9.0, 12.0)];
    let g = mismatches(&r);
    __report(3, g == vec![1, 3], format!("got {:?}, wanted [1, 3]", g));

    let g = mismatches(&[]);
    __report(4, g.is_empty(), format!("got {:?}, wanted []", g));

    let g = status(&[(16.0, 16.0), (25.0, 20.0), (9.0, 12.0)]);
    __report(5, g == "nominal", format!("got {:?}, wanted \\"nominal\\"", g));

    let g = status(&r);
    __report(6, g == "mismatch at 2 readings", format!("got {:?}, wanted \\"mismatch at 2 readings\\"", g));

    let g = status(&[(16.0, 16.0), (16.0, 30.0), (16.0, 30.0), (16.0, 30.0), (16.0, 16.0)]);
    __report(7, g == "critical", format!("got {:?}, wanted \\"critical\\"", g));
}
'''),
    away="""
<p><strong>Away mission, for your own editor:</strong> turn the validator into a real
program. Read readings from a CSV file, one <code>pressure,flow</code> per line, print
the status, and exit with a non-zero code on <em>critical</em> so a shell script can
react. Then add a <code>--tolerance</code> flag with a default of 10 percent. Nothing
here is graded; it is the point at which a browser console should make you want a real
one.</p>
""",
)

# -------------------------------------------------------------- 42
_m(
    season=6, num=42, slug="42-the-two-logs", id="bridge-s6m42", station="science",
    title="The Two Logs", stardate="Stardate 55169.5",
    crew=["skree", "raghunathan", "dubois"],
    minutes=45,
    blurb="Two logs, nineteen years apart, and one place where they stop agreeing. "
          "Find it, count it, and read what comes after.",
    briefing="""
<p>Lt. Skree wants the two logs read properly, start to finish, by a program rather than
by Skree, because Skree has been reading them for six days and has started to see the
pattern on the inside of Skree's eyelids.</p>

<p>Parse the log text into entries, ignoring blank lines and comment lines beginning
with a hash. Find the first index where the two logs disagree, if they ever do. Count
entries by level. Return everything after a given stardate. Four functions, all of them
things you have built pieces of before, assembled into one tool. The Captain has asked
what comes after the divergence in the other log. Skree has said "us, I think".</p>
""",
    debrief="""
<p>The logs agree, entry for entry, up to stardate 55170.1, tomorrow, 06:14. Ours ends
there. Theirs continues: <em>"WARN|manifold seal replaced by hand, four minutes"</em>,
then nineteen years of the ordinary, then a final line, dated today: <em>"INFO|not
yet"</em>. Skree has read that line, and then read it again, and then said, to nobody
in particular, "it came back to say that".</p>
""",
    objectives=[
        "parse_log: entries from lines, stardate as a number",
        "parse_log: blank lines and # comments are skipped",
        "first_divergence: the index of the first differing entry",
        "first_divergence: identical logs give nothing",
        "first_divergence: a shorter log diverges at its own end",
        "count_levels: a count per level, sorted by level",
        "after: entries strictly after a stardate, in order",
        "after: nothing after the last stardate",
    ],
    hint="Reuse the Season 3 parser for one line. <code>first_divergence</code> is a "
         "<code>zip</code> and a comparison, plus a length check for the shorter-log "
         "case. <code>count_levels</code> is a dictionary or map. Read each objective's "
         "wording for 'strictly'.",
    py_spec="""
<p>Four functions. An entry is a dict <code>{"stardate": float, "level": str,
"message": str}</code>.</p>
<ul>
  <li><code>parse_log(text)</code>: one entry per non-blank line that does not start with
    <code>#</code>, from <code>"stardate|LEVEL|message"</code> (message may contain pipes;
    trim it).</li>
  <li><code>first_divergence(ours, theirs)</code>: the index of the first position where
    the entries differ, or where one log has run out; <code>None</code> if identical.</li>
  <li><code>count_levels(entries)</code>: a dict of level to count.</li>
  <li><code>after(entries, stardate)</code>: entries with a stardate strictly greater than
    the given one, in order.</li>
</ul>
""",
    py_stub='''def parse_log(text):
    """Entries from log text; skip blank lines and lines starting with #."""
    # TODO
    return []


def first_divergence(ours, theirs):
    """Index of the first differing entry (or where one runs out), or None."""
    # TODO
    return None


def count_levels(entries):
    """{level: count}"""
    # TODO
    return {}


def after(entries, stardate):
    """Entries with stardate strictly greater than the given one."""
    # TODO
    return []
''',
    py_reference='''def parse_log(text):
    """Entries from log text; skip blank lines and lines starting with #."""
    entries = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        stardate, level, message = line.split("|", 2)
        entries.append({"stardate": float(stardate), "level": level, "message": message.strip()})
    return entries


def first_divergence(ours, theirs):
    """Index of the first differing entry (or where one runs out), or None."""
    for i, (a, b) in enumerate(zip(ours, theirs)):
        if a != b:
            return i
    if len(ours) != len(theirs):
        return min(len(ours), len(theirs))
    return None


def count_levels(entries):
    """{level: count}"""
    counts = {}
    for e in entries:
        counts[e["level"]] = counts.get(e["level"], 0) + 1
    return counts


def after(entries, stardate):
    """Entries with stardate strictly greater than the given one."""
    return [e for e in entries if e["stardate"] > stardate]
''',
    py_checker=py_custom('''
_ours_text = """# UES Magnanimous, main log
55169.0|INFO|nominal
55169.5|WARN|pressure|flow mismatch

55170.1|INFO|watch change
"""
_theirs_text = """55169.0|INFO|nominal
55169.5|WARN|pressure|flow mismatch
55170.1|INFO|watch change
55170.2|WARN|manifold seal replaced by hand, four minutes
"""
_E = lambda s, l, m: {"stardate": s, "level": l, "message": m}

_g = _guard(0, lambda: parse_log(_ours_text), "parse_log(ours)")
if _g is not _FAILED:
    _report(0, len(_g) == 3 and _g[0] == _E(55169.0, "INFO", "nominal") and _g[1]["message"] == "pressure|flow mismatch",
            f"got {len(_g)} entries; first {_short(_g[0]) if _g else None}")
    _report(1, len(_g) == 3, f"got {len(_g)} entries from text with a comment and a blank line, wanted 3")
else:
    _report(1, False, "not reached")

_ours = [_E(55169.0, "INFO", "nominal"), _E(55169.5, "WARN", "pressure|flow mismatch"), _E(55170.1, "INFO", "watch change")]
_theirs = _ours + [_E(55170.2, "WARN", "manifold seal replaced by hand, four minutes")]
_diff = [_E(55169.0, "INFO", "nominal"), _E(55169.5, "INFO", "nominal"), _E(55170.1, "INFO", "watch change")]

_g = _guard(2, lambda: first_divergence(_ours, _diff), "first_divergence, differs at 1")
if _g is not _FAILED:
    _report(2, _g == 1, f"got {_g!r}, wanted 1")
_g = _guard(3, lambda: first_divergence(_ours, list(_ours)), "first_divergence, identical")
if _g is not _FAILED:
    _report(3, _g is None, f"got {_g!r}, wanted None")
_g = _guard(4, lambda: first_divergence(_ours, _theirs), "first_divergence, theirs is longer")
if _g is not _FAILED:
    _report(4, _g == 3, f"got {_g!r}, wanted 3 (ours runs out at index 3)")

_g = _guard(5, lambda: count_levels(_theirs), "count_levels(theirs)")
if _g is not _FAILED:
    _report(5, dict(_g) == {"INFO": 2, "WARN": 2}, f"got {_short(dict(_g) if hasattr(_g, 'items') else _g)}, wanted INFO 2, WARN 2")

_g = _guard(6, lambda: after(_theirs, 55169.5), "after(theirs, 55169.5)")
if _g is not _FAILED:
    _report(6, [e["stardate"] for e in _g] == [55170.1, 55170.2], f"got stardates {[e['stardate'] for e in _g]}, wanted [55170.1, 55170.2] (strictly after)")
_g = _guard(7, lambda: after(_theirs, 55170.2), "after(theirs, last stardate)")
if _g is not _FAILED:
    _report(7, _g == [], f"got {_short(_g)}, wanted []")
'''),
    rs_spec="""
<p>Keep the struct as given. Four functions:</p>
<ul>
  <li><code>parse_log(text: &amp;str) -&gt; Vec&lt;Entry&gt;</code>: one entry per non-blank
    line that does not start with <code>#</code>, from <code>"stardate|LEVEL|message"</code>
    (message may contain pipes; trim it).</li>
  <li><code>first_divergence(ours: &amp;[Entry], theirs: &amp;[Entry]) -&gt;
    Option&lt;usize&gt;</code>: the first index where entries differ or one log runs out;
    <code>None</code> if identical.</li>
  <li><code>count_levels(entries: &amp;[Entry]) -&gt; Vec&lt;(String, usize)&gt;</code>:
    a count per level, sorted by level.</li>
  <li><code>after(entries: &amp;[Entry], stardate: f64) -&gt; Vec&lt;Entry&gt;</code>:
    entries with a stardate strictly greater than the given one, in order.</li>
</ul>
""",
    rs_stub='''#[derive(Debug, Clone, PartialEq)]
struct Entry {
    stardate: f64,
    level: String,
    message: String,
}

/// Entries from log text; skip blank lines and lines starting with '#'.
fn parse_log(text: &str) -> Vec<Entry> {
    // TODO
    Vec::new()
}

/// Index of the first differing entry (or where one runs out), or None.
fn first_divergence(ours: &[Entry], theirs: &[Entry]) -> Option<usize> {
    // TODO
    None
}

/// (level, count) pairs, sorted by level.
fn count_levels(entries: &[Entry]) -> Vec<(String, usize)> {
    // TODO
    Vec::new()
}

/// Entries with stardate strictly greater than the given one.
fn after(entries: &[Entry], stardate: f64) -> Vec<Entry> {
    // TODO
    Vec::new()
}
''',
    rs_reference='''use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq)]
struct Entry {
    stardate: f64,
    level: String,
    message: String,
}

/// Entries from log text; skip blank lines and lines starting with '#'.
fn parse_log(text: &str) -> Vec<Entry> {
    text.lines()
        .map(str::trim)
        .filter(|l| !l.is_empty() && !l.starts_with('#'))
        .map(|l| {
            let mut parts = l.splitn(3, '|');
            Entry {
                stardate: parts.next().unwrap_or("0").trim().parse().unwrap_or(0.0),
                level: parts.next().unwrap_or("").to_string(),
                message: parts.next().unwrap_or("").trim().to_string(),
            }
        })
        .collect()
}

/// Index of the first differing entry (or where one runs out), or None.
fn first_divergence(ours: &[Entry], theirs: &[Entry]) -> Option<usize> {
    for (i, (a, b)) in ours.iter().zip(theirs.iter()).enumerate() {
        if a != b {
            return Some(i);
        }
    }
    if ours.len() != theirs.len() {
        Some(ours.len().min(theirs.len()))
    } else {
        None
    }
}

/// (level, count) pairs, sorted by level.
fn count_levels(entries: &[Entry]) -> Vec<(String, usize)> {
    let mut counts: BTreeMap<&str, usize> = BTreeMap::new();
    for e in entries {
        *counts.entry(e.level.as_str()).or_insert(0) += 1;
    }
    counts.into_iter().map(|(k, v)| (k.to_string(), v)).collect()
}

/// Entries with stardate strictly greater than the given one.
fn after(entries: &[Entry], stardate: f64) -> Vec<Entry> {
    entries.iter().filter(|e| e.stardate > stardate).cloned().collect()
}
''',
    rs_checker=rs_custom('''
fn e(s: f64, l: &str, m: &str) -> Entry { Entry { stardate: s, level: l.to_string(), message: m.to_string() } }
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let ours_text = "# UES Magnanimous, main log\\n55169.0|INFO|nominal\\n55169.5|WARN|pressure|flow mismatch\\n\\n55170.1|INFO|watch change\\n";
    let g = parse_log(ours_text);
    __report(0, g.len() == 3 && g[0] == e(55169.0, "INFO", "nominal") && g[1].message == "pressure|flow mismatch",
             format!("got {} entries; first {:?}", g.len(), g.first()));
    __report(1, g.len() == 3, format!("got {} entries from text with a comment and a blank line, wanted 3", g.len()));

    let ours = vec![e(55169.0, "INFO", "nominal"), e(55169.5, "WARN", "pressure|flow mismatch"), e(55170.1, "INFO", "watch change")];
    let mut theirs = ours.clone();
    theirs.push(e(55170.2, "WARN", "manifold seal replaced by hand, four minutes"));
    let diff = vec![e(55169.0, "INFO", "nominal"), e(55169.5, "INFO", "nominal"), e(55170.1, "INFO", "watch change")];

    let g = first_divergence(&ours, &diff);
    __report(2, g == Some(1), format!("got {:?}, wanted Some(1)", g));
    let g = first_divergence(&ours, &ours.clone());
    __report(3, g == None, format!("got {:?}, wanted None", g));
    let g = first_divergence(&ours, &theirs);
    __report(4, g == Some(3), format!("got {:?}, wanted Some(3) (ours runs out at index 3)", g));

    let g = count_levels(&theirs);
    __report(5, g == vec![("INFO".to_string(), 2), ("WARN".to_string(), 2)], format!("got {:?}, wanted [(INFO, 2), (WARN, 2)]", g));

    let g: Vec<f64> = after(&theirs, 55169.5).iter().map(|x| x.stardate).collect();
    __report(6, g == vec![55170.1, 55170.2], format!("got stardates {:?}, wanted [55170.1, 55170.2] (strictly after)", g));
    let g = after(&theirs, 55170.2);
    __report(7, g.is_empty(), format!("got {} entries, wanted 0", g.len()));
}
'''),
    away="""
<p><strong>Away mission:</strong> point the parser at a real file. Write a small tool that
takes two log paths on the command line, prints the first divergence with a few lines of
context from each side, and a level summary for both. Add <code>--after
STARDATE</code>. Then write three tests for <code>first_divergence</code>, including the
shorter-log case, because that is the one you will get wrong when you refactor it.</p>
""",
)

# -------------------------------------------------------------- 43
_m(
    season=6, num=43, slug="43-the-handshake", id="bridge-s6m43", station="tactical",
    title="The Handshake", stardate="Stardate 55169.9",
    crew=["tkala", "raghunathan", "skree"],
    minutes=45,
    blurb="Before the other ship's computer will hand over the rest, it wants a "
          "framed, checksummed message, and it will reject anything malformed.",
    briefing="""
<p>The other computer wants to talk properly now, and properly means framed messages: a
fixed prefix, the message length, the message, and a checksum, pipes between. It will
reject a frame with the wrong prefix, a length that does not match, or a checksum that
does not add up, and it will say nothing about why, because it is a computer, and a
computer from nineteen years in the future at that.</p>

<p>Chief T'Kala wants both directions: <em>frame</em> a message for sending, and
<em>unframe</em> one for receiving, refusing anything malformed. Because the length is in
the frame, a message may itself contain pipes and still come back whole. The checksum is
the sum of the message's bytes, modulo 256, as two hex digits. Eight objectives. Lt.
Skree has pointed out that if we get this wrong the other ship simply says nothing, "which
is what it has mostly done, so we would not know". This is true and unhelpful.</p>
""",
    debrief="""
<p>The handshake completes. The other computer sends one frame, checksum correct, and
the message is a personnel file. Commander Priya Raghunathan. Shore leave: <em>granted,
55170.3</em>. Tomorrow. Filed nineteen years ago on a ship that had just replaced a
manifold seal by hand, by a version of her who had four minutes to spare and used them
for this. She has read it. She has said "oh". She has sat down.</p>
""",
    objectives=[
        "checksum: the byte sum modulo 256, as two lower-case hex digits",
        "checksum: an empty message is 00",
        "frame: 'MAGN|<length>|<message>|<checksum>'",
        "unframe: a good frame gives back the message",
        "unframe: a message containing pipes survives the round trip",
        "unframe: a wrong prefix is refused",
        "unframe: a length that does not match is refused",
        "unframe: a corrupted checksum is refused",
    ],
    hint="Split on the pipe at most three times, so the message keeps its own pipes: "
         "prefix, length, then the rest, and the checksum is the last field of the rest. "
         "Use the declared length to cut the message out of the rest exactly. Refuse on "
         "any check that fails, and only then recompute the checksum and compare.",
    py_spec="""
<p>Three functions:</p>
<ul>
  <li><code>checksum(message)</code>: sum of the message's UTF-8 bytes modulo 256, as two
    lower-case hex digits, e.g. <code>"7f"</code>.</li>
  <li><code>frame(message)</code>: <code>f"MAGN|{len(message)}|{message}|{checksum}"</code>,
    where the length is the number of characters.</li>
  <li><code>unframe(text)</code>: the message from a well-formed frame, or
    <code>None</code> if the prefix is not <code>MAGN</code>, the length field does not
    match the message, or the checksum does not match.</li>
</ul>
""",
    py_stub='''def checksum(message):
    """Sum of the UTF-8 bytes modulo 256, as two lower-case hex digits."""
    # TODO
    return "00"


def frame(message):
    """'MAGN|<length>|<message>|<checksum>'"""
    # TODO
    return message


def unframe(text):
    """The message from a well-formed frame, or None if anything is off."""
    # TODO
    return None
''',
    py_reference='''def checksum(message):
    """Sum of the UTF-8 bytes modulo 256, as two lower-case hex digits."""
    return f"{sum(message.encode('utf-8')) % 256:02x}"


def frame(message):
    """'MAGN|<length>|<message>|<checksum>'"""
    return f"MAGN|{len(message)}|{message}|{checksum(message)}"


def unframe(text):
    """The message from a well-formed frame, or None if anything is off."""
    parts = text.split("|", 2)
    if len(parts) != 3 or parts[0] != "MAGN":
        return None
    try:
        length = int(parts[1])
    except ValueError:
        return None
    rest = parts[2]
    if len(rest) < length + 3 or rest[length] != "|":
        return None
    message, given = rest[:length], rest[length + 1:]
    if len(given) != 2 or given != checksum(message):
        return None
    return message
''',
    py_checker=py_custom('''
_g = _guard(0, lambda: (checksum("hi"), checksum("Gerald")), "checksum('hi'), checksum('Gerald')")
if _g is not _FAILED:
    _report(0, _g == ("d1", "4f"), f"got {_g}, wanted ('d1', '4f')")
_g = _guard(1, lambda: checksum(""), "checksum('')")
if _g is not _FAILED:
    _report(1, _g == "00", f"got {_g!r}, wanted '00'")
_g = _guard(2, lambda: frame("hi"), "frame('hi')")
if _g is not _FAILED:
    _report(2, _g == "MAGN|2|hi|d1", f"got {_g!r}, wanted 'MAGN|2|hi|d1'")
_g = _guard(3, lambda: unframe("MAGN|2|hi|d1"), "unframe(good frame)")
if _g is not _FAILED:
    _report(3, _g == "hi", f"got {_g!r}, wanted 'hi'")
_g = _guard(4, lambda: unframe(frame("shore|leave|granted")), "round trip with pipes")
if _g is not _FAILED:
    _report(4, _g == "shore|leave|granted", f"got {_g!r}, wanted 'shore|leave|granted'")
_g = _guard(5, lambda: unframe("MAGX|2|hi|d1"), "unframe(wrong prefix)")
if _g is not _FAILED:
    _report(5, _g is None, f"got {_g!r}, wanted None")
_g = _guard(6, lambda: unframe("MAGN|3|hi|d1"), "unframe(wrong length)")
if _g is not _FAILED:
    _report(6, _g is None, f"got {_g!r}, wanted None")
_g = _guard(7, lambda: unframe("MAGN|2|hi|d2"), "unframe(bad checksum)")
if _g is not _FAILED:
    _report(7, _g is None, f"got {_g!r}, wanted None")
'''),
    rs_spec="""
<p>Three functions:</p>
<ul>
  <li><code>checksum(message: &amp;str) -&gt; String</code>: sum of the message's UTF-8
    bytes modulo 256, as two lower-case hex digits, e.g. <code>"7f"</code>.</li>
  <li><code>frame(message: &amp;str) -&gt; String</code>:
    <code>"MAGN|{length}|{message}|{checksum}"</code>, where the length is the number of
    characters.</li>
  <li><code>unframe(text: &amp;str) -&gt; Option&lt;String&gt;</code>: the message from a
    well-formed frame, or <code>None</code> if the prefix is not <code>MAGN</code>, the
    length field does not match the message, or the checksum does not match.</li>
</ul>
""",
    rs_stub='''/// Sum of the UTF-8 bytes modulo 256, as two lower-case hex digits.
fn checksum(message: &str) -> String {
    // TODO
    String::from("00")
}

/// "MAGN|<length>|<message>|<checksum>"
fn frame(message: &str) -> String {
    // TODO
    message.to_string()
}

/// The message from a well-formed frame, or None if anything is off.
fn unframe(text: &str) -> Option<String> {
    // TODO
    None
}
''',
    rs_reference='''/// Sum of the UTF-8 bytes modulo 256, as two lower-case hex digits.
fn checksum(message: &str) -> String {
    let sum: u32 = message.bytes().map(|b| b as u32).sum();
    format!("{:02x}", sum % 256)
}

/// "MAGN|<length>|<message>|<checksum>"
fn frame(message: &str) -> String {
    format!("MAGN|{}|{}|{}", message.chars().count(), message, checksum(message))
}

/// The message from a well-formed frame, or None if anything is off.
fn unframe(text: &str) -> Option<String> {
    let mut parts = text.splitn(3, '|');
    if parts.next()? != "MAGN" {
        return None;
    }
    let length: usize = parts.next()?.parse().ok()?;
    let rest = parts.next()?;
    let chars: Vec<char> = rest.chars().collect();
    if chars.len() < length + 3 || chars[length] != '|' {
        return None;
    }
    let message: String = chars[..length].iter().collect();
    let given: String = chars[length + 1..].iter().collect();
    if given.len() != 2 || given != checksum(&message) {
        return None;
    }
    Some(message)
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let g = (checksum("hi"), checksum("Gerald"));
    __report(0, g.0 == "d1" && g.1 == "4f", format!("got {:?}, wanted (\\"d1\\", \\"4f\\")", g));
    let g = checksum("");
    __report(1, g == "00", format!("got {:?}, wanted \\"00\\"", g));
    let g = frame("hi");
    __report(2, g == "MAGN|2|hi|d1", format!("got {:?}, wanted \\"MAGN|2|hi|d1\\"", g));
    let g = unframe("MAGN|2|hi|d1");
    __report(3, g.as_deref() == Some("hi"), format!("got {:?}, wanted Some(\\"hi\\")", g));
    let g = unframe(&frame("shore|leave|granted"));
    __report(4, g.as_deref() == Some("shore|leave|granted"), format!("got {:?}, wanted the message with its pipes", g));
    let g = unframe("MAGX|2|hi|d1");
    __report(5, g.is_none(), format!("got {:?}, wanted None", g));
    let g = unframe("MAGN|3|hi|d1");
    __report(6, g.is_none(), format!("got {:?}, wanted None", g));
    let g = unframe("MAGN|2|hi|d2");
    __report(7, g.is_none(), format!("got {:?}, wanted None", g));
}
'''),
    away="""
<p><strong>Away mission:</strong> make it a real protocol. Write a tiny server that
accepts framed messages over a local socket (Python's <code>socket</code>, Rust's
<code>std::net</code>), unframes them, and replies with a framed acknowledgement, and a
client that sends three messages including one deliberately corrupted. Watch the server
refuse it. Then swap the checksum for a real hash and notice how little else changes.</p>
""",
)

# -------------------------------------------------------------- 44
_m(
    season=6, num=44, slug="44-terminus", id="bridge-s6m44", station="helm",
    title="Terminus", stardate="Stardate 55170.1",
    crew=["dubois", "raghunathan", "skree", "tkala", "tannenbaum", "archie"],
    minutes=45,
    blurb="Tomorrow. The seal is replaced, the logs agree, and the Captain would like "
          "a course. Every station, one last time.",
    briefing="""
<p>It is 06:14 on stardate 55170.1, and nothing has happened. The manifold is holding.
The logs, run through your reconciler, agree to the entry. Across two kilometres of
nothing, the other Magnanimous has lowered its shields, and its transponder has switched
to <em>UES Magnanimous, decommissioned</em>, which Lt. Skree says is "the most polite way
a ship has ever said goodbye".</p>

<p>The Captain wants a course home, and he wants it from you: a heading from where we
are to where we are going, kept honest in the range 0 to 359; a distance; an ETA at a
given warp factor, rounded <em>up</em>, because you do not tell a crew "three point two
hours" and arrive in four; a fuel check; and, because he is the Captain and it is
tradition, the countdown, and a log entry to close the season on. Eight objectives.
Ensign Tannenbaum will press the button. Supervised.</p>
""",
    debrief="""
<p>Heading 227, nineteen light-hours, warp four, ETA one hour. The countdown ran. The
Ensign pressed the button, and pressed it well. Behind us the other Magnanimous, having
delivered one line of release notes and one shore-leave form nineteen years late, went
quietly dark, and Skree logged it as "resolved" without the "pending", and then, after
a moment, added: "thank you".</p>

<p>Commander Raghunathan has filed for shore leave, dated tomorrow, and it has been
granted, and she has been seen, briefly, to smile. Chief T'Kala has put Gerald back by
the viewscreen. The coffee is at ninety-four degrees. Ensign Tannenbaum has asked what
he should fix next, and the Captain has said "nothing, for one whole day", and Bo has
looked genuinely lost.</p>

<p><strong>You have completed The Bridge.</strong> Report to the mission board; the
dedication plaque is waiting for a name. Whatever you built here, in whichever language,
or both: a while loop, a list, a dictionary of functions, a search, a check that refuses
bad input, and a state machine that will not skip a step. That is not a starship. It is
every program you will ever write. Welcome aboard.</p>
""",
    objectives=[
        "heading_to: the compass bearing from one point to another, whole degrees",
        "heading_to: never negative, always 0 to 359",
        "distance_to: straight-line distance, two decimal places",
        "eta_hours: distance over warp cubed, rounded UP to whole hours",
        "eta_hours: an exact number of hours is not rounded up further",
        "fuel_ok: enough fuel for the trip at that warp, at 3 units per light-hour",
        "engage: the countdown from Season 2, from 3, then the course",
        "log_entry: the closing line, formatted exactly",
    ],
    hint="<code>atan2(dy, dx)</code> gives an angle in radians from the x axis; convert "
         "to degrees, then to a compass bearing with <code>(90 - angle) % 360</code>. "
         "Round distance to two places, ETA with <code>ceil</code>. Everything else is "
         "string formatting you have done all season.",
    py_spec="""
<p>Points are <code>(x, y)</code> tuples in light-hours. Six functions:</p>
<ul>
  <li><code>heading_to(a, b)</code>: compass bearing from <code>a</code> to <code>b</code>
    as a whole number 0..359, where north (positive y) is 0 and east (positive x) is 90.
    Compute <code>(90 - degrees(atan2(dy, dx))) % 360</code>, then round to the nearest
    whole degree, mod 360.</li>
  <li><code>distance_to(a, b)</code>: straight-line distance, rounded to two places.</li>
  <li><code>eta_hours(distance, warp)</code>: <code>distance / warp**3</code>, rounded
    <strong>up</strong> to a whole number of hours.</li>
  <li><code>fuel_ok(distance, fuel)</code>: <code>True</code> if <code>fuel &gt;= 3 *
    distance</code>.</li>
  <li><code>engage(heading, warp)</code>: <code>"3... 2... 1... engage: heading H at
    warp W"</code>.</li>
  <li><code>log_entry(stardate, text)</code>: <code>"Stardate {stardate:.1f} | {text}"</code>.</li>
</ul>
""",
    py_stub='''import math


def heading_to(a, b):
    """Compass bearing from a to b, whole degrees 0..359. North is 0, east is 90."""
    # TODO
    return 0


def distance_to(a, b):
    """Straight-line distance, two decimal places."""
    # TODO
    return 0.0


def eta_hours(distance, warp):
    """distance / warp**3, rounded UP to whole hours."""
    # TODO
    return 0


def fuel_ok(distance, fuel):
    """Enough fuel at 3 units per light-hour?"""
    # TODO
    return False


def engage(heading, warp):
    """'3... 2... 1... engage: heading H at warp W'"""
    # TODO
    return ""


def log_entry(stardate, text):
    """'Stardate 55170.1 | text'"""
    # TODO
    return ""
''',
    py_reference='''import math


def heading_to(a, b):
    """Compass bearing from a to b, whole degrees 0..359. North is 0, east is 90."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    bearing = (90 - math.degrees(math.atan2(dy, dx))) % 360
    return round(bearing) % 360


def distance_to(a, b):
    """Straight-line distance, two decimal places."""
    return round(math.hypot(b[0] - a[0], b[1] - a[1]), 2)


def eta_hours(distance, warp):
    """distance / warp**3, rounded UP to whole hours."""
    return math.ceil(distance / warp ** 3)


def fuel_ok(distance, fuel):
    """Enough fuel at 3 units per light-hour?"""
    return fuel >= 3 * distance


def engage(heading, warp):
    """'3... 2... 1... engage: heading H at warp W'"""
    return f"3... 2... 1... engage: heading {heading} at warp {warp}"


def log_entry(stardate, text):
    """'Stardate 55170.1 | text'"""
    return f"Stardate {stardate:.1f} | {text}"
''',
    py_checker=py_custom('''
_g = _guard(0, lambda: (heading_to((0, 0), (0, 10)), heading_to((0, 0), (10, 0)), heading_to((0, 0), (10, 10))), "north, east, north-east")
if _g is not _FAILED:
    _report(0, _g == (0, 90, 45), f"got {_g}, wanted (0, 90, 45)")
_g = _guard(1, lambda: (heading_to((0, 0), (-10, 0)), heading_to((0, 0), (-1, -1)), heading_to((5, 5), (0, 0))), "west, south-west, back to origin")
if _g is not _FAILED:
    _report(1, _g == (270, 225, 225) and all(0 <= h <= 359 for h in _g), f"got {_g}, wanted (270, 225, 225)")
_g = _guard(2, lambda: (distance_to((0, 0), (3, 4)), distance_to((1, 1), (4, 5)), distance_to((0, 0), (1, 1))), "distances")
if _g is not _FAILED:
    _report(2, _g == (5.0, 5.0, 1.41), f"got {_g}, wanted (5.0, 5.0, 1.41)")
_g = _guard(3, lambda: (eta_hours(19, 4), eta_hours(100, 2)), "eta 19 at warp 4, 100 at warp 2")
if _g is not _FAILED:
    _report(3, _g == (1, 13), f"got {_g}, wanted (1, 13): 19/64 rounds up to 1, 100/8 = 12.5 rounds up to 13")
_g = _guard(4, lambda: (eta_hours(64, 4), eta_hours(16, 2)), "exact hours")
if _g is not _FAILED:
    _report(4, _g == (1, 2), f"got {_g}, wanted (1, 2): exact results are not rounded up further")
_g = _guard(5, lambda: (fuel_ok(19, 57), fuel_ok(19, 56), fuel_ok(0, 0)), "fuel checks")
if _g is not _FAILED:
    _report(5, _g == (True, False, True), f"got {_g}, wanted (True, False, True)")
_g = _guard(6, lambda: engage(227, 4), "engage(227, 4)")
if _g is not _FAILED:
    _report(6, _g == "3... 2... 1... engage: heading 227 at warp 4", f"got {_g!r}")
_g = _guard(7, lambda: log_entry(55170.1, "course laid in, all stations nominal"), "log_entry")
if _g is not _FAILED:
    _report(7, _g == "Stardate 55170.1 | course laid in, all stations nominal", f"got {_g!r}")
'''),
    rs_spec="""
<p>Points are <code>(f64, f64)</code> in light-hours. Six functions:</p>
<ul>
  <li><code>heading_to(a: (f64, f64), b: (f64, f64)) -&gt; u32</code>: compass bearing,
    whole degrees 0..359, north (positive y) 0, east (positive x) 90. Compute
    <code>(90 - atan2(dy, dx).to_degrees()).rem_euclid(360)</code>, round to the nearest
    whole degree, mod 360.</li>
  <li><code>distance_to(a, b) -&gt; f64</code>: straight-line distance, two places.</li>
  <li><code>eta_hours(distance: f64, warp: u32) -&gt; u32</code>: distance over warp cubed,
    rounded <strong>up</strong> to whole hours.</li>
  <li><code>fuel_ok(distance: f64, fuel: f64) -&gt; bool</code>: <code>fuel &gt;= 3 *
    distance</code>.</li>
  <li><code>engage(heading: u32, warp: u32) -&gt; String</code>: <code>"3... 2... 1...
    engage: heading H at warp W"</code>.</li>
  <li><code>log_entry(stardate: f64, text: &amp;str) -&gt; String</code>:
    <code>"Stardate {stardate:.1} | {text}"</code>.</li>
</ul>
""",
    rs_stub='''/// Compass bearing from a to b, whole degrees 0..=359. North is 0, east is 90.
fn heading_to(a: (f64, f64), b: (f64, f64)) -> u32 {
    // TODO
    0
}

/// Straight-line distance, two decimal places.
fn distance_to(a: (f64, f64), b: (f64, f64)) -> f64 {
    // TODO
    0.0
}

/// distance / warp^3, rounded UP to whole hours.
fn eta_hours(distance: f64, warp: u32) -> u32 {
    // TODO
    0
}

/// Enough fuel at 3 units per light-hour?
fn fuel_ok(distance: f64, fuel: f64) -> bool {
    // TODO
    false
}

/// "3... 2... 1... engage: heading H at warp W"
fn engage(heading: u32, warp: u32) -> String {
    // TODO
    String::new()
}

/// "Stardate 55170.1 | text"
fn log_entry(stardate: f64, text: &str) -> String {
    // TODO
    String::new()
}
''',
    rs_reference='''/// Compass bearing from a to b, whole degrees 0..=359. North is 0, east is 90.
fn heading_to(a: (f64, f64), b: (f64, f64)) -> u32 {
    let (dx, dy) = (b.0 - a.0, b.1 - a.1);
    let bearing = (90.0 - dy.atan2(dx).to_degrees()).rem_euclid(360.0);
    (bearing.round() as u32) % 360
}

/// Straight-line distance, two decimal places.
fn distance_to(a: (f64, f64), b: (f64, f64)) -> f64 {
    ((b.0 - a.0).hypot(b.1 - a.1) * 100.0).round() / 100.0
}

/// distance / warp^3, rounded UP to whole hours.
fn eta_hours(distance: f64, warp: u32) -> u32 {
    (distance / (warp as f64).powi(3)).ceil() as u32
}

/// Enough fuel at 3 units per light-hour?
fn fuel_ok(distance: f64, fuel: f64) -> bool {
    fuel >= 3.0 * distance
}

/// "3... 2... 1... engage: heading H at warp W"
fn engage(heading: u32, warp: u32) -> String {
    format!("3... 2... 1... engage: heading {heading} at warp {warp}")
}

/// "Stardate 55170.1 | text"
fn log_entry(stardate: f64, text: &str) -> String {
    format!("Stardate {stardate:.1} | {text}")
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let g = (heading_to((0.0, 0.0), (0.0, 10.0)), heading_to((0.0, 0.0), (10.0, 0.0)), heading_to((0.0, 0.0), (10.0, 10.0)));
    __report(0, g == (0, 90, 45), format!("got {:?}, wanted (0, 90, 45)", g));
    let g = (heading_to((0.0, 0.0), (-10.0, 0.0)), heading_to((0.0, 0.0), (-1.0, -1.0)), heading_to((5.0, 5.0), (0.0, 0.0)));
    __report(1, g == (270, 225, 225), format!("got {:?}, wanted (270, 225, 225)", g));
    let g = (distance_to((0.0, 0.0), (3.0, 4.0)), distance_to((1.0, 1.0), (4.0, 5.0)), distance_to((0.0, 0.0), (1.0, 1.0)));
    __report(2, (g.0 - 5.0).abs() < 1e-9 && (g.1 - 5.0).abs() < 1e-9 && (g.2 - 1.41).abs() < 1e-9, format!("got {:?}, wanted (5.0, 5.0, 1.41)", g));
    let g = (eta_hours(19.0, 4), eta_hours(100.0, 2));
    __report(3, g == (1, 13), format!("got {:?}, wanted (1, 13): 19/64 rounds up to 1, 100/8 = 12.5 rounds up to 13", g));
    let g = (eta_hours(64.0, 4), eta_hours(16.0, 2));
    __report(4, g == (1, 2), format!("got {:?}, wanted (1, 2): exact results are not rounded up further", g));
    let g = (fuel_ok(19.0, 57.0), fuel_ok(19.0, 56.0), fuel_ok(0.0, 0.0));
    __report(5, g == (true, false, true), format!("got {:?}, wanted (true, false, true)", g));
    let g = engage(227, 4);
    __report(6, g == "3... 2... 1... engage: heading 227 at warp 4", format!("got {:?}", g));
    let g = log_entry(55170.1, "course laid in, all stations nominal");
    __report(7, g == "Stardate 55170.1 | course laid in, all stations nominal", format!("got {:?}", g));
}
'''),
    away="""
<p><strong>Away mission, the last one:</strong> put the whole ship in one program. A
command-line tool with subcommands: <code>manifold</code> (mission 41), <code>logs</code>
(42), <code>frame</code> and <code>unframe</code> (43), <code>course</code> (44). One
entry point, shared error handling, tests for each. It is the same shape as every real
tool you will ever admire, and you have already written every part of it. Then, if you
like, publish it: a package on PyPI, or a crate on crates.io, with a README that
explains what a Magnanimous is. Somebody will find it.</p>
""",
)
