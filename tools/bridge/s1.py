"""Season 1: Shakedown Cruise.

Output, variables, types, decisions. Cadet through Ensign. Helm and Ops
only, because those are the two stations a Cadet is allowed near.
"""

from .helpers import _m, py_cases, rs_cases

# --------------------------------------------------------------- 1
_m(
    season=1, num=1, slug="01-long-cold-cup", id="bridge-s1m1", station="helm",
    title="The Long Cold Cup", stardate="Stardate 55103.2",
    crew=["dubois", "raghunathan", "tannenbaum", "skree"],
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
    py_checker=py_cases("brew_report", [
        ((61,), "too cold"), ((82,), "acceptable"), ((90,), "acceptable"),
        ((96,), "acceptable"), ((97,), "the Captain is happy"),
    ]),
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
    rs_checker=rs_cases("brew_report", [
        (["61"], '"too cold"'), (["82"], '"acceptable"'), (["90"], '"acceptable"'),
        (["96"], '"acceptable"'), (["97"], '"the Captain is happy"'),
    ]),
)

# --------------------------------------------------------------- 2
_m(
    season=1, num=2, slug="02-roll-call", id="bridge-s1m2", station="ops",
    title="Roll Call", stardate="Stardate 55104.7",
    crew=["tkala", "tannenbaum"],
    blurb="The morning roll call announces every officer as 'None None reporting'. "
          "Chief T'Kala would like her name back.",
    briefing="""
<p>Since the last software update, the bridge roll call has greeted every officer as
<em>"None None reporting"</em>. Chief T'Kala, who is two and a half metres tall and has
never once needed to raise her voice, has asked, very gently, for her name back.</p>

<p>The routine that assembles the greeting was written by Ensign Tannenbaum during what
he describes as "a very productive night shift". It concatenates a rank and a surname.
It concatenates them wrong.</p>
""",
    debrief="""
<p>Roll call now reads "Chief T'Kala reporting", and the Chief has thanked you by
introducing you to the plant on the bridge. The plant is called Gerald. Gerald is on the
duty roster. Do not ask.</p>
""",
    objectives=[
        "Ensign Tannenbaum reporting",
        "Chief T'Kala reporting, apostrophe intact",
        "A one-word surname",
        "A double-barrelled Captain",
        "Exactly one space between rank and surname, and one before 'reporting'",
    ],
    hint="You want a formatted string: an f-string in Python, <code>format!</code> in "
         "Rust. Count the spaces in the expected output; a stray one is the usual "
         "culprit.",
    py_spec="""
<p>Write <code>roll_call(rank, surname)</code>, which returns the string
<code>"&lt;rank&gt; &lt;surname&gt; reporting"</code>. So
<code>roll_call("Ensign", "Tannenbaum")</code> is
<code>"Ensign Tannenbaum reporting"</code>.</p>
""",
    py_stub='''def roll_call(rank, surname):
    """Announce an officer: '<rank> <surname> reporting'."""
    # TODO: build the greeting from the two parts.
    return "None None reporting"
''',
    py_reference='''def roll_call(rank, surname):
    """Announce an officer: '<rank> <surname> reporting'."""
    return f"{rank} {surname} reporting"
''',
    py_checker=py_cases("roll_call", [
        (("Ensign", "Tannenbaum"), "Ensign Tannenbaum reporting"),
        (("Chief", "T'Kala"), "Chief T'Kala reporting"),
        (("Lieutenant", "Skree"), "Lieutenant Skree reporting"),
        (("Captain", "Dubois-Okonkwo"), "Captain Dubois-Okonkwo reporting"),
        (("Commander", "Raghunathan"), "Commander Raghunathan reporting"),
    ]),
    rs_spec="""
<p>Write <code>roll_call(rank: &amp;str, surname: &amp;str) -&gt; String</code>, which
returns <code>"&lt;rank&gt; &lt;surname&gt; reporting"</code>. So
<code>roll_call("Ensign", "Tannenbaum")</code> is
<code>"Ensign Tannenbaum reporting"</code>.</p>
""",
    rs_stub='''/// Announce an officer: "<rank> <surname> reporting".
fn roll_call(rank: &str, surname: &str) -> String {
    // TODO: build the greeting from the two parts.
    String::from("None None reporting")
}
''',
    rs_reference='''/// Announce an officer: "<rank> <surname> reporting".
fn roll_call(rank: &str, surname: &str) -> String {
    format!("{rank} {surname} reporting")
}
''',
    rs_checker=rs_cases("roll_call", [
        (['"Ensign"', '"Tannenbaum"'], '"Ensign Tannenbaum reporting"'),
        (['"Chief"', '"T\'Kala"'], '"Chief T\'Kala reporting"'),
        (['"Lieutenant"', '"Skree"'], '"Lieutenant Skree reporting"'),
        (['"Captain"', '"Dubois-Okonkwo"'], '"Captain Dubois-Okonkwo reporting"'),
        (['"Commander"', '"Raghunathan"'], '"Commander Raghunathan reporting"'),
    ]),
)

# --------------------------------------------------------------- 3
_m(
    season=1, num=3, slug="03-which-deck", id="bridge-s1m3", station="helm",
    title="Which Deck?", stardate="Stardate 55106.1",
    crew=["skree", "tannenbaum"],
    blurb="The turbolift keeps delivering people one deck short. Lt. Skree has "
          "measured this and is not amused.",
    briefing="""
<p>Compartments aboard the Maggie are numbered from 1, twelve to a deck. Compartment 1
is on Deck 1, compartment 12 is on Deck 1, and compartment 13 is on Deck 2. This has
been true for nineteen years and nobody had to think about it until the turbolift's
routing table was "tidied up".</p>

<p>Lt. Skree has now been delivered to the wrong deck four times, has timed each
occurrence, and has produced a table. The table shows the lift is wrong exactly at every
twelfth compartment. Skree considers this "suspiciously regular for a coincidence".
Skree is right.</p>
""",
    debrief="""
<p>The turbolift is delivering people to the deck they asked for. Lt. Skree has updated
the table, noted a 100% success rate over eleven trials, and filed it under "resolved,
pending long-term observation". Skree does not close things.</p>
""",
    objectives=[
        "Compartment 1 is on Deck 1",
        "Compartment 12, the last on Deck 1, is still on Deck 1",
        "Compartment 13 is on Deck 2",
        "Compartment 24 is on Deck 2",
        "Compartment 100 is on Deck 9",
    ],
    hint="Integer division gets you most of the way, but compartments start at 1, not "
         "0. Try subtracting one before you divide, and adding one after. Then check "
         "compartment 12 by hand.",
    py_spec="""
<p>Write <code>deck_of(compartment)</code>: compartments are numbered from 1, twelve per
deck. Return the deck number, also from 1. So compartments 1 to 12 are Deck 1, 13 to 24
are Deck 2, and so on.</p>
""",
    py_stub='''def deck_of(compartment):
    """Return which deck (from 1) a compartment (from 1) is on. Twelve per deck."""
    # TODO: careful at compartments 12 and 13.
    return 0
''',
    py_reference='''def deck_of(compartment):
    """Return which deck (from 1) a compartment (from 1) is on. Twelve per deck."""
    return (compartment - 1) // 12 + 1
''',
    py_checker=py_cases("deck_of", [
        ((1,), 1), ((12,), 1), ((13,), 2), ((24,), 2), ((100,), 9),
    ]),
    rs_spec="""
<p>Write <code>deck_of(compartment: u32) -&gt; u32</code>: compartments are numbered
from 1, twelve per deck. Return the deck number, also from 1. So compartments 1 to 12
are Deck 1, 13 to 24 are Deck 2, and so on.</p>
""",
    rs_stub='''/// Which deck (from 1) is a compartment (from 1) on? Twelve per deck.
fn deck_of(compartment: u32) -> u32 {
    // TODO: careful at compartments 12 and 13.
    0
}
''',
    rs_reference='''/// Which deck (from 1) is a compartment (from 1) on? Twelve per deck.
fn deck_of(compartment: u32) -> u32 {
    (compartment - 1) / 12 + 1
}
''',
    rs_checker=rs_cases("deck_of", [
        (["1"], "1"), (["12"], "1"), (["13"], "2"), (["24"], "2"), (["100"], "9"),
    ]),
)

# --------------------------------------------------------------- 4
_m(
    season=1, num=4, slug="04-badge-printer", id="bridge-s1m4", station="ops",
    title="The Badge Printer", stardate="Stardate 55107.4",
    crew=["tannenbaum", "dubois"],
    blurb="The name badges for the diplomatic reception have come out in whatever case "
          "and spacing the crew typed. The Captain's says '  yves  '.",
    briefing="""
<p>There is a diplomatic reception on Thursday, and the badge printer has produced
forty-one badges in exactly the case and spacing each crew member typed into the form.
Three badges have leading spaces. One is entirely lower case. Ensign Tannenbaum's reads
<em>"bo!!!"</em>, and he has been asked not to do that again.</p>

<p>The Captain's badge says <em>"&nbsp;&nbsp;yves&nbsp;&nbsp;"</em>. He would like it to
say <em>"YVES"</em>, and he would like it before the ambassador arrives.</p>
""",
    debrief="""
<p>Forty-one badges, all in upper case, no stray spaces. Ensign Tannenbaum's now reads
<em>"BO!!!"</em>, which he says is "somehow worse", and which nobody has offered to
fix.</p>
""",
    objectives=[
        "Leading and trailing spaces removed",
        "Lower case becomes upper case",
        "Already-clean input passes through unchanged",
        "Both problems at once",
        "Spaces inside the name are kept, only the ends are trimmed",
    ],
    hint="Two string methods, chained. One trims whitespace from the ends, one changes "
         "the case. The order does not matter here, but the third objective is worth "
         "reading twice: internal spaces stay.",
    py_spec="""
<p>Write <code>badge(name)</code>: strip whitespace from both ends of <code>name</code>
and return it in upper case. Spaces <em>inside</em> the name are kept.</p>
""",
    py_stub='''def badge(name):
    """Trim the ends and shout the name."""
    # TODO
    return name
''',
    py_reference='''def badge(name):
    """Trim the ends and shout the name."""
    return name.strip().upper()
''',
    py_checker=py_cases("badge", [
        (("  yves  ",), "YVES"), (("skree",), "SKREE"), (("T'KALA",), "T'KALA"),
        (("  bo tannenbaum ",), "BO TANNENBAUM"), (("Priya Raghunathan",), "PRIYA RAGHUNATHAN"),
    ]),
    rs_spec="""
<p>Write <code>badge(name: &amp;str) -&gt; String</code>: trim whitespace from both ends
and return the name in upper case. Spaces <em>inside</em> the name are kept.</p>
""",
    rs_stub='''/// Trim the ends and shout the name.
fn badge(name: &str) -> String {
    // TODO
    name.to_string()
}
''',
    rs_reference='''/// Trim the ends and shout the name.
fn badge(name: &str) -> String {
    name.trim().to_uppercase()
}
''',
    rs_checker=rs_cases("badge", [
        (['"  yves  "'], '"YVES"'), (['"skree"'], '"SKREE"'), (['"T\'KALA"'], '"T\'KALA"'),
        (['"  bo tannenbaum "'], '"BO TANNENBAUM"'),
        (['"Priya Raghunathan"'], '"PRIYA RAGHUNATHAN"'),
    ]),
)

# --------------------------------------------------------------- 5
_m(
    season=1, num=5, slug="05-shield-clamp", id="bridge-s1m5", station="helm",
    title="One Hundred and Forty Percent", stardate="Stardate 55109.0",
    crew=["raghunathan", "tannenbaum"],
    blurb="The shield display reads 140%. The shields are not at 140%. Nothing is ever "
          "at 140%.",
    briefing="""
<p>The shield status display on the bridge currently reads <strong>140%</strong>. This
is not a real number. Commander Raghunathan has explained, twice, that the emitters
physically cannot exceed full charge and that the display is simply not being clamped.
Ensign Tannenbaum has asked whether 140% could be "a stretch goal".</p>

<p>Separately, during the last drill the same display read <strong>-20%</strong>, which
briefly convinced two junior officers that the ship had negative shields, whatever those
would be. The Commander would like both ends of the range dealt with, today.</p>
""",
    debrief="""
<p>The shield display now reads a number between 0 and 100, and Commander Raghunathan
has removed the sticky note that said "IGNORE THIS" from the corner of it. She has kept
the sticky note. She says it may be needed elsewhere.</p>
""",
    objectives=[
        "A negative reading is clamped to 0",
        "Zero stays zero",
        "A normal reading passes through unchanged",
        "Exactly 100 stays 100",
        "An overcharged reading is clamped to 100",
    ],
    hint="Two comparisons, or a pair of <code>min</code>/<code>max</code> calls. Rust "
         "has <code>.clamp(0, 100)</code>, which is one method and worth knowing.",
    py_spec="""
<p>Write <code>clamp_shields(percent)</code>: return the value limited to the range 0 to
100 inclusive. Values below 0 become 0, values above 100 become 100, everything else is
returned unchanged.</p>
""",
    py_stub='''def clamp_shields(percent):
    """Keep a shield reading honest: never below 0, never above 100."""
    # TODO
    return percent
''',
    py_reference='''def clamp_shields(percent):
    """Keep a shield reading honest: never below 0, never above 100."""
    return max(0, min(100, percent))
''',
    py_checker=py_cases("clamp_shields", [
        ((-20,), 0), ((0,), 0), ((55,), 55), ((100,), 100), ((140,), 100),
    ]),
    rs_spec="""
<p>Write <code>clamp_shields(percent: i32) -&gt; i32</code>: return the value limited to
the range 0 to 100 inclusive. Values below 0 become 0, values above 100 become 100,
everything else is returned unchanged.</p>
""",
    rs_stub='''/// Keep a shield reading honest: never below 0, never above 100.
fn clamp_shields(percent: i32) -> i32 {
    // TODO
    percent
}
''',
    rs_reference='''/// Keep a shield reading honest: never below 0, never above 100.
fn clamp_shields(percent: i32) -> i32 {
    percent.clamp(0, 100)
}
''',
    rs_checker=rs_cases("clamp_shields", [
        (["-20"], "0"), (["0"], "0"), (["55"], "55"), (["100"], "100"), (["140"], "100"),
    ]),
)

# --------------------------------------------------------------- 6
_m(
    season=1, num=6, slug="06-airlock-interlock", id="bridge-s1m6", station="ops",
    title="The Airlock Interlock", stardate="Stardate 55110.6",
    crew=["tkala", "skree"],
    blurb="An airlock is a door that must never open at the wrong time. Somebody has "
          "written the rule with an 'or' where they meant an 'and'.",
    briefing="""
<p>An airlock's outer door may open only when the inner door is sealed <strong>and</strong>
the pressure has been equalised <strong>and</strong> maintenance has not locked it out.
Three conditions, all of which must hold. This is not a complicated rule. It is,
however, currently written with an <em>or</em> in it.</p>

<p>Chief T'Kala discovered this during a routine check by watching the outer door
cheerfully report itself "ready to open" while the inner door stood wide. She closed the
inner door, sat down, and asked ARCHIE to route the fix to "someone who has read a
sentence before". Lt. Skree has offered to explain what an "and" is. The offer has been
declined.</p>
""",
    debrief="""
<p>The outer door now refuses to open unless all three conditions hold. Chief T'Kala has
gone back to watering Gerald. Lt. Skree has written a short paper on the difference
between conjunction and disjunction and left a copy on Ensign Tannenbaum's desk. It is
eleven pages.</p>
""",
    objectives=[
        "Everything in order: sealed, equalised, no lockout, so it may open",
        "Inner door open: must not open",
        "Pressure not equalised: must not open",
        "Maintenance lockout engaged: must not open, even though the rest is fine",
        "Nothing in order at all: must not open",
    ],
    hint="Three conditions joined with <em>and</em>, one of them negated. Read the "
         "fourth objective: the lockout is a reason to refuse, so it is "
         "<code>not lockout</code> (Python) or <code>!lockout</code> (Rust).",
    py_spec="""
<p>Write <code>outer_may_open(inner_sealed, pressure_equalised, lockout)</code>, three
booleans. Return <code>True</code> only when the inner door is sealed <strong>and</strong>
pressure is equalised <strong>and</strong> there is <strong>no</strong> lockout.
Otherwise <code>False</code>.</p>
""",
    py_stub='''def outer_may_open(inner_sealed, pressure_equalised, lockout):
    """May the outer door open? Sealed AND equalised AND no lockout."""
    # TODO: this is currently the bug Chief T'Kala found.
    return inner_sealed or pressure_equalised or lockout
''',
    py_reference='''def outer_may_open(inner_sealed, pressure_equalised, lockout):
    """May the outer door open? Sealed AND equalised AND no lockout."""
    return inner_sealed and pressure_equalised and not lockout
''',
    py_checker=py_cases("outer_may_open", [
        ((True, True, False), True), ((False, True, False), False),
        ((True, False, False), False), ((True, True, True), False),
        ((False, False, False), False),
    ]),
    rs_spec="""
<p>Write <code>outer_may_open(inner_sealed: bool, pressure_equalised: bool, lockout: bool)
-&gt; bool</code>. Return <code>true</code> only when the inner door is sealed
<strong>and</strong> pressure is equalised <strong>and</strong> there is
<strong>no</strong> lockout. Otherwise <code>false</code>.</p>
""",
    rs_stub='''/// May the outer door open? Sealed AND equalised AND no lockout.
fn outer_may_open(inner_sealed: bool, pressure_equalised: bool, lockout: bool) -> bool {
    // TODO: this is currently the bug Chief T'Kala found.
    inner_sealed || pressure_equalised || lockout
}
''',
    rs_reference='''/// May the outer door open? Sealed AND equalised AND no lockout.
fn outer_may_open(inner_sealed: bool, pressure_equalised: bool, lockout: bool) -> bool {
    inner_sealed && pressure_equalised && !lockout
}
''',
    rs_checker=rs_cases("outer_may_open", [
        (["true", "true", "false"], "true"), (["false", "true", "false"], "false"),
        (["true", "false", "false"], "false"), (["true", "true", "true"], "false"),
        (["false", "false", "false"], "false"),
    ]),
)

# --------------------------------------------------------------- 7
_m(
    season=1, num=7, slug="07-absolute-zero", id="bridge-s1m7", station="helm",
    title="Absolute Zero, Approximately", stardate="Stardate 55112.3",
    crew=["skree", "raghunathan"],
    blurb="The science lab wants Kelvin. The sensors report Celsius. Between them is a "
          "floating-point number and a great deal of feeling.",
    briefing="""
<p>The long-range sensor package reports temperature in Celsius. Lt. Skree's analysis
suite requires Kelvin, and Skree has requested the conversion be done "correctly, to two
decimal places, and without any of the drama that attended the last attempt".</p>

<p>The last attempt, for the record, returned 273.14999999999998 for a reading of
zero, and Skree filed a formal complaint about the "aesthetic and moral" quality of the
number. Commander Raghunathan has asked that you round it. She has also asked that
nobody mention floating point to Skree ever again.</p>
""",
    debrief="""
<p>Kelvin readings are arriving rounded to two decimal places, and Lt. Skree has
withdrawn the complaint. Skree has, however, opened a new one about the phrase
"approximately absolute zero", which Skree considers a contradiction in terms. It is
addressed to the universe.</p>
""",
    objectives=[
        "Zero Celsius is 273.15 K",
        "Absolute zero, minus 273.15, is 0.0 K",
        "Boiling water at 100 is 373.15 K",
        "Room temperature, 21.5, is 294.65 K",
        "The result is rounded to two decimal places",
    ],
    hint="Add 273.15, then round to two decimal places. Python has "
         "<code>round(x, 2)</code>. Rust does not round to places directly: multiply "
         "by 100, <code>.round()</code>, divide by 100.",
    py_spec="""
<p>Write <code>to_kelvin(celsius)</code>: add 273.15 and return the result
<strong>rounded to two decimal places</strong>. So <code>to_kelvin(0)</code> is
<code>273.15</code> and <code>to_kelvin(-273.15)</code> is <code>0.0</code>.</p>
""",
    py_stub='''def to_kelvin(celsius):
    """Celsius to Kelvin, rounded to two decimal places."""
    # TODO
    return 0.0
''',
    py_reference='''def to_kelvin(celsius):
    """Celsius to Kelvin, rounded to two decimal places."""
    return round(celsius + 273.15, 2)
''',
    py_checker=py_cases("to_kelvin", [
        ((0,), 273.15), ((-273.15,), 0.0), ((100,), 373.15), ((21.5,), 294.65),
        ((36.6,), 309.75),
    ], check="abs(_got - _want) < 1e-6"),
    rs_spec="""
<p>Write <code>to_kelvin(celsius: f64) -&gt; f64</code>: add 273.15 and return the result
<strong>rounded to two decimal places</strong>. So <code>to_kelvin(0.0)</code> is
<code>273.15</code> and <code>to_kelvin(-273.15)</code> is <code>0.0</code>.</p>
""",
    rs_stub='''/// Celsius to Kelvin, rounded to two decimal places.
fn to_kelvin(celsius: f64) -> f64 {
    // TODO
    0.0
}
''',
    rs_reference='''/// Celsius to Kelvin, rounded to two decimal places.
fn to_kelvin(celsius: f64) -> f64 {
    ((celsius + 273.15) * 100.0).round() / 100.0
}
''',
    rs_checker=rs_cases("to_kelvin", [
        (["0.0"], "273.15"), (["-273.15"], "0.0"), (["100.0"], "373.15"),
        (["21.5"], "294.65"), (["36.6"], "309.75"),
    ], check="(got - want).abs() < 1e-6"),
)

# --------------------------------------------------------------- 8
_m(
    season=1, num=8, slug="08-ration-arithmetic", id="bridge-s1m8", station="ops",
    title="Ration Arithmetic", stardate="Stardate 55114.9",
    crew=["dubois", "tkala", "tannenbaum"],
    blurb="How many days of food are aboard? The answer the computer gives is a "
          "fraction, and nobody eats a fraction of a day.",
    briefing="""
<p>Each ration crate feeds forty person-days: one person for forty days, forty people
for one day, or any arrangement in between. The Captain has asked how long the current
stores will last, and the computer has answered <em>"9.756 days"</em>. The Captain does
not want the point seven five six. The Captain wants to know whether to order more.</p>

<p>Chief T'Kala points out that a partial day is not a day anyone gets fed on, so the
answer should round <em>down</em>. Ensign Tannenbaum suggested rounding to the nearest,
"for morale". This was overruled by everyone present, including Gerald.</p>
""",
    debrief="""
<p>Nine days. The Captain has ordered more rations, and has also ordered that in future
the computer round down before anyone gets hopeful. Chief T'Kala has entered this into
the ship's standing orders, directly beneath the one about Gerald's watering schedule.</p>

<p><strong>You have completed the shakedown cruise.</strong> Report to the mission
board: the Science station is now open to you.</p>
""",
    objectives=[
        "Ten crates for a crew of forty last exactly ten days",
        "Ten crates for forty-one people: nine days, because a partial day does not count",
        "No crates, no days",
        "Seven crates for twenty people last fourteen days",
        "One crate for eighty people is zero whole days",
    ],
    hint="Total person-days is crates times forty. Divide by the crew size and keep only "
         "the whole number: <code>//</code> in Python, plain <code>/</code> on integers "
         "in Rust, which already discards the remainder.",
    py_spec="""
<p>Write <code>days_of_rations(crates, crew)</code>: each crate is forty person-days.
Return how many <strong>whole</strong> days the crew can be fed, rounding
<strong>down</strong>. So <code>days_of_rations(10, 41)</code> is <code>9</code>.</p>
""",
    py_stub='''def days_of_rations(crates, crew):
    """Whole days of food aboard. Forty person-days per crate. Round down."""
    # TODO
    return 0
''',
    py_reference='''def days_of_rations(crates, crew):
    """Whole days of food aboard. Forty person-days per crate. Round down."""
    return (crates * 40) // crew
''',
    py_checker=py_cases("days_of_rations", [
        ((10, 40), 10), ((10, 41), 9), ((0, 50), 0), ((7, 20), 14), ((1, 80), 0),
    ]),
    rs_spec="""
<p>Write <code>days_of_rations(crates: u32, crew: u32) -&gt; u32</code>: each crate is
forty person-days. Return how many <strong>whole</strong> days the crew can be fed,
rounding <strong>down</strong>. So <code>days_of_rations(10, 41)</code> is
<code>9</code>.</p>
""",
    rs_stub='''/// Whole days of food aboard. Forty person-days per crate. Round down.
fn days_of_rations(crates: u32, crew: u32) -> u32 {
    // TODO
    0
}
''',
    rs_reference='''/// Whole days of food aboard. Forty person-days per crate. Round down.
fn days_of_rations(crates: u32, crew: u32) -> u32 {
    (crates * 40) / crew
}
''',
    rs_checker=rs_cases("days_of_rations", [
        (["10", "40"], "10"), (["10", "41"], "9"), (["0", "50"], "0"),
        (["7", "20"], "14"), (["1", "80"], "0"),
    ]),
)
