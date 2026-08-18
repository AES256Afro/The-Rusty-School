"""Missions aboard the UES Magnanimous.

Each mission carries a shared briefing and, per language, four things:

  stub       what the learner starts with
  reference  a solution that must pass every objective (verified in CI)
  checker    code appended to the learner's, which runs the objectives and
             prints one BRIDGE| line per objective
  objectives human-readable labels, in the same order the checker prints

The checker is written per mission per language rather than generated from
a table of inputs. It is more typing, but it means a mission can test
anything the language can express (ownership, panics, iterator laziness)
instead of only what a generic args/expect runner can reach.

WIRE FORMAT, printed by every checker, one line per objective:

    BRIDGE|<index>|<PASS or FAIL>|<what came back>

bridge.js parses those lines. Anything else the program prints is shown to
the learner as their own output, which is how print-debugging keeps working
inside a graded mission.
"""

from __future__ import annotations

MISSIONS: list[dict] = []


def _m(**kw):
    MISSIONS.append(kw)


# --------------------------------------------------------------- S1 M1
_m(
    season=1,
    num=1,
    slug="01-long-cold-cup",
    id="bridge-s1m1",
    station="helm",
    title="The Long Cold Cup",
    stardate="Stardate 55103.2",
    blurb="The beverage replicator has opinions about temperature. The Captain has "
          "opinions about the replicator.",
    briefing="""
<p>The beverage replicator on Deck 4 has produced three hundred and forty consecutive
cups of lukewarm water. The Captain has raised this at three consecutive staff meetings
and is now raising it again, with feeling.</p>

<p>Ensign Tannenbaum has "already looked at it". The situation has since become worse.</p>

<p>Commander Raghunathan traced the fault to a single temperature routine and then did
not fix it, on the grounds that it is "a good first one for the new officer". This is
Engineering for <em>I am extremely tired</em>.</p>
""",
    debrief="""
<p>The replicator is producing coffee at ninety-four degrees. The Captain has been
informed and is currently describing it to people who did not ask.</p>

<p>Lt. Skree wishes it noted that the beverage is chemically identical to the previous
three hundred and forty, and that the crew's reaction is therefore "sociological rather
than thermal". Nobody has replied to this.</p>
""",
    objectives=[
        "Below the band: 61 degrees reads as too cold",
        "The lower edge: exactly 82 is already acceptable",
        "Comfortably inside: 90 is acceptable",
        "The upper edge: exactly 96 is still acceptable",
        "Above the band: 97 makes the Captain happy",
    ],
    hint="Read the specification's word <em>inclusive</em> very carefully, then look at "
         "which comparison you used at each edge. Almost every failure here is one "
         "character: <code>&lt;</code> where you wanted <code>&lt;=</code>.",
    py_spec="""
<p>Write <code>brew_report(celsius)</code>, which takes a number and returns a string:</p>
<ul>
  <li><code>"too cold"</code> when the temperature is <strong>below 82</strong></li>
  <li><code>"acceptable"</code> from <strong>82 to 96 inclusive</strong></li>
  <li><code>"the Captain is happy"</code> when it is <strong>above 96</strong></li>
</ul>
""",
    py_stub='''def brew_report(celsius):
    """Return the replicator's verdict for a temperature in Celsius."""
    # TODO: three bands. Mind the edges: 82 and 96 are both acceptable.
    return ""
''',
    py_reference='''def brew_report(celsius):
    """Return the replicator's verdict for a temperature in Celsius."""
    if celsius < 82:
        return "too cold"
    if celsius <= 96:
        return "acceptable"
    return "the Captain is happy"
''',
    py_checker='''
_cases = [
    (61, "too cold"),
    (82, "acceptable"),
    (90, "acceptable"),
    (96, "acceptable"),
    (97, "the Captain is happy"),
]

for _i, (_arg, _want) in enumerate(_cases):
    try:
        _got = brew_report(_arg)
    except Exception as _e:
        print(f"BRIDGE|{_i}|FAIL|{type(_e).__name__}: {_e}")
        continue
    _ok = _got == _want
    print(f"BRIDGE|{_i}|{'PASS' if _ok else 'FAIL'}|brew_report({_arg}) returned {_got!r}, wanted {_want!r}")
''',
    rs_spec="""
<p>Write <code>brew_report(celsius: i32) -&gt; &amp;'static str</code>, which returns:</p>
<ul>
  <li><code>"too cold"</code> when the temperature is <strong>below 82</strong></li>
  <li><code>"acceptable"</code> from <strong>82 to 96 inclusive</strong></li>
  <li><code>"the Captain is happy"</code> when it is <strong>above 96</strong></li>
</ul>
<p class="muted small">Write the function only. ARCHIE supplies <code>main</code>.</p>
""",
    rs_stub='''/// Return the replicator's verdict for a temperature in Celsius.
fn brew_report(celsius: i32) -> &'static str {
    // TODO: three bands. Mind the edges: 82 and 96 are both acceptable.
    ""
}
''',
    rs_reference='''/// Return the replicator's verdict for a temperature in Celsius.
fn brew_report(celsius: i32) -> &'static str {
    if celsius < 82 {
        "too cold"
    } else if celsius <= 96 {
        "acceptable"
    } else {
        "the Captain is happy"
    }
}
''',
    rs_checker='''
fn main() {
    let cases: [(i32, &str); 5] = [
        (61, "too cold"),
        (82, "acceptable"),
        (90, "acceptable"),
        (96, "acceptable"),
        (97, "the Captain is happy"),
    ];
    for (i, (arg, want)) in cases.iter().enumerate() {
        let got = brew_report(*arg);
        let verdict = if got == *want { "PASS" } else { "FAIL" };
        println!(
            "BRIDGE|{}|{}|brew_report({}) returned {:?}, wanted {:?}",
            i, verdict, arg, got, want
        );
    }
}
''',
)
