"""Season 5: Deep Space.

Concurrency, async, performance. Engineering and Sickbay. This is the
season where the two languages disagree, on purpose: Python's
concurrency here is asyncio, because that is what runs in a browser;
Rust's is threads, because the compiler will not let you have the bug.
"""

from .helpers import _m, py_async, py_cases, py_custom, rs_cases, rs_custom

# -------------------------------------------------------------- 33
_m(
    season=5, num=33, slug="33-everyone-wants-the-sensors", id="bridge-s5m33",
    station="engineering",
    title="Everyone Wants the Sensors", stardate="Stardate 55155.5",
    crew=["raghunathan", "skree", "tannenbaum"],
    minutes=30,
    blurb="Six science teams, six timeslots on the array, and two teams have been "
          "given the same one. Lt. Skree says this is arithmetically impossible, "
          "and yet.",
    briefing="""
<p>Welcome to Engineering. Six science teams have queued for the long-range array, and
each request runs at the same time as the others. Two teams have received identical
timeslots. Lt. Skree reports this is "arithmetically impossible, and yet". Commander
Raghunathan has stopped sighing, which everybody agrees is the bad sign.</p>

<p>The scheduler looks at the first free slot, then goes off to talk to the array, then
takes the slot. Between <em>looking</em> and <em>taking</em>, it lets go, and another
request looks at the same slot. That gap is the whole bug. In Python the gap is an
<code>await</code>. In Rust it is the moment between two separate locks, and the fix is
to hold one lock across the choice and the take. Ensign Tannenbaum wrote the gap. He
says it "seemed polite".</p>
""",
    debrief="""
<p>Six teams, six slots, no repeats, and the seventh team gets a polite nothing instead
of a crash. Commander Raghunathan has resumed sighing, which is a relief to everyone.
Lt. Skree has the array for the next hour and has pointed it at the other ship.</p>
""",
    objectives=[
        "Every team receives a slot",
        "No slot is issued twice",
        "When teams equal slots, every slot is used and none is left free",
        "A seventh team, with six slots, gets None instead of a crash",
        "The requests can still run concurrently",
    ],
    hint="Python: take the slot <em>before</em> the <code>await</code>, in one step "
         "(<code>pop</code>), so nothing can slip in between. Rust: lock once, choose "
         "and remove inside that single lock, then let go.",
    py_spec="""
<p>Fix <code>Scheduler.request</code> so that concurrent requests never receive the same
slot. <code>Scheduler(slots)</code> holds free slots; <code>await
scheduler.request(team)</code> gives that team a free slot (recording it in
<code>assigned</code>) or <code>None</code> if none remain. It must stay an
<code>async</code> method: the requests are gathered concurrently.</p>
""",
    py_stub='''import asyncio


class Scheduler:
    """Hands out array timeslots to science teams, one each, no repeats."""

    def __init__(self, slots):
        self.free = list(slots)
        self.assigned = {}

    async def request(self, team):
        """Give `team` a free slot, or None if none are left."""
        if not self.free:
            self.assigned[team] = None
            return None
        slot = self.free[0]          # look at the first free slot
        await asyncio.sleep(0)       # talk to the array (this yields!)
        self.free.pop(0)             # take it
        self.assigned[team] = slot
        return slot
''',
    py_reference='''import asyncio


class Scheduler:
    """Hands out array timeslots to science teams, one each, no repeats."""

    def __init__(self, slots):
        self.free = list(slots)
        self.assigned = {}

    async def request(self, team):
        """Give `team` a free slot, or None if none are left."""
        if not self.free:
            self.assigned[team] = None
            return None
        slot = self.free.pop(0)      # look AND take, with nothing in between
        await asyncio.sleep(0)       # now talk to the array
        self.assigned[team] = slot
        return slot
''',
    py_checker=py_async('''
import asyncio, inspect

async def _archie_main():
    teams = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"]
    s = Scheduler([1, 2, 3, 4, 5, 6])
    try:
        results = await asyncio.gather(*(s.request(t) for t in teams))
    except Exception as e:
        for i in range(3):
            _report(i, False, f"six requests raised {type(e).__name__}: {e}")
    else:
        _report(0, len(results) == 6 and all(r is not None for r in results), f"slots issued: {results}")
        _report(1, len(set(results)) == len(results), f"slots issued: {results}, wanted no repeats")
        _report(2, sorted(results) == [1, 2, 3, 4, 5, 6] and s.free == [], f"free afterwards: {s.free}, wanted []")

    s2 = Scheduler([1, 2, 3, 4, 5, 6])
    try:
        r2 = await asyncio.gather(*(s2.request(t) for t in teams + ["eta"]))
    except Exception as e:
        _report(3, False, f"seven requests raised {type(e).__name__}: {e}")
    else:
        nones = sum(1 for r in r2 if r is None)
        issued = [r for r in r2 if r is not None]
        _report(3, nones == 1 and sorted(issued) == [1, 2, 3, 4, 5, 6], f"seven teams got {r2}")

    _report(4, inspect.iscoroutinefunction(Scheduler.request), "request must remain an async def")
'''),
    rs_spec="""
<p>Fix <code>allocate</code> so that concurrent threads never take the same slot.
<code>allocate(teams, slots)</code> spawns one thread per team; each takes a slot from
the shared pool, or <code>None</code> if the pool is empty. It returns
<code>(team, slot)</code> pairs in team order. The threads and the shared
<code>Arc&lt;Mutex&lt;..&gt;&gt;</code> must stay: the point is to make them correct.</p>
""",
    rs_stub='''use std::sync::{Arc, Mutex};
use std::thread;

/// Give every team a slot from the pool, one each, no repeats.
/// Teams past the end of the pool get None.
fn allocate(teams: &[&str], slots: Vec<u32>) -> Vec<(String, Option<u32>)> {
    let pool = Arc::new(Mutex::new(slots));
    let mut handles = Vec::new();
    for &team in teams {
        let pool = Arc::clone(&pool);
        let team = team.to_string();
        handles.push(thread::spawn(move || {
            // Look at the first free slot...
            let chosen = pool.lock().unwrap().first().copied();
            thread::yield_now();                    // ...talk to the array...
            if let Some(s) = chosen {
                pool.lock().unwrap().retain(|&x| x != s);   // ...then take it.
            }
            (team, chosen)
        }));
    }
    handles.into_iter().map(|h| h.join().unwrap()).collect()
}
''',
    rs_reference='''use std::sync::{Arc, Mutex};
use std::thread;

/// Give every team a slot from the pool, one each, no repeats.
/// Teams past the end of the pool get None.
fn allocate(teams: &[&str], slots: Vec<u32>) -> Vec<(String, Option<u32>)> {
    let pool = Arc::new(Mutex::new(slots));
    let mut handles = Vec::new();
    for &team in teams {
        let pool = Arc::clone(&pool);
        let team = team.to_string();
        handles.push(thread::spawn(move || {
            // Choose AND take under one lock, so nothing can slip in between.
            let chosen = {
                let mut p = pool.lock().unwrap();
                if p.is_empty() { None } else { Some(p.remove(0)) }
            };
            thread::yield_now();
            (team, chosen)
        }));
    }
    handles.into_iter().map(|h| h.join().unwrap()).collect()
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let teams = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta"];
    let mut all_some = true;
    let mut no_dupes = true;
    let mut all_used = true;
    let mut worst: Vec<Option<u32>> = Vec::new();
    for _ in 0..100 {
        let got = allocate(&teams, vec![1, 2, 3, 4, 5, 6]);
        let slots: Vec<Option<u32>> = got.iter().map(|(_, s)| *s).collect();
        if slots.iter().any(|s| s.is_none()) { all_some = false; worst = slots.clone(); }
        let mut seen = std::collections::HashSet::new();
        for s in slots.iter().flatten() {
            if !seen.insert(*s) { no_dupes = false; worst = slots.clone(); }
        }
        let mut sorted: Vec<u32> = slots.iter().flatten().copied().collect();
        sorted.sort();
        if sorted != vec![1, 2, 3, 4, 5, 6] { all_used = false; worst = slots.clone(); }
    }
    __report(0, all_some, format!("over 100 runs, every team got a slot: {} (a bad run: {:?})", all_some, worst));
    __report(1, no_dupes, format!("over 100 runs, no slot issued twice: {} (a bad run: {:?})", no_dupes, worst));
    __report(2, all_used, format!("over 100 runs, all six slots used: {}", all_used));

    let seven = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta"];
    let got = allocate(&seven, vec![1, 2, 3, 4, 5, 6]);
    let nones = got.iter().filter(|(_, s)| s.is_none()).count();
    let mut issued: Vec<u32> = got.iter().filter_map(|(_, s)| *s).collect();
    issued.sort();
    __report(3, nones == 1 && issued == vec![1, 2, 3, 4, 5, 6], format!("seven teams got {:?}", got.iter().map(|(_, s)| *s).collect::<Vec<_>>()));

    let names: Vec<String> = allocate(&teams, vec![1, 2, 3, 4, 5, 6]).into_iter().map(|(t, _)| t).collect();
    __report(4, names == teams, format!("results in team order: {:?}", names));
}
'''),
)

# -------------------------------------------------------------- 34
_m(
    season=5, num=34, slug="34-parallel-sweep", id="bridge-s5m34", station="engineering",
    title="The Parallel Sweep", stardate="Stardate 55157.0",
    crew=["raghunathan", "dubois"],
    minutes=25,
    blurb="Reading eight sensors takes eight times as long as reading one. It does "
          "not need to.",
    briefing="""
<p>Each sensor takes fifty milliseconds to answer. The full sweep reads them one after
another, so eight sensors take four hundred milliseconds, and the Captain, who has
been told the other ship is doing something, would like the number to be fifty.</p>

<p>The sensors do not depend on each other. Ask them all at once and wait for all the
answers. In Python that is <code>asyncio.gather</code>. In Rust it is a thread per
sensor, scoped so the compiler knows they finish before you return. The results must
come back in the order the sensors were asked, whatever order they answered in.</p>
""",
    debrief="""
<p>Fifty-three milliseconds for the full sweep. The other ship is powering up its
transporter. Commander Raghunathan has said, quietly, that she left something over
there, and the Captain has asked what, and she has said "later".</p>
""",
    objectives=[
        "Reads every sensor and returns (name, value) pairs",
        "Results come back in the order asked",
        "An empty list of sensors returns an empty result",
        "Eight sensors finish in well under the sequential time",
        "Values are correct for each sensor",
    ],
    hint="Python: <code>values = await asyncio.gather(*(read_sensor(n) for n in "
         "names))</code>, then zip with the names. Rust: inside "
         "<code>thread::scope</code>, spawn one closure per name, collect the handles, "
         "then join them in order.",
    py_spec="""
<p>Rewrite <code>sweep_all(names)</code> so the sensor reads happen concurrently. Keep
<code>read_sensor</code> exactly as it is; it is the slow thing you are working around.
Return a list of <code>(name, value)</code> in the order given.</p>
""",
    py_stub='''import asyncio


async def read_sensor(name):
    """Pretend to talk to a sensor. Takes 50 ms. Do not change this."""
    await asyncio.sleep(0.05)
    return len(name) * 7


async def sweep_all(names):
    """Read every sensor and return [(name, value)] in the given order."""
    # One at a time. Eight sensors take 400 ms. Make them overlap.
    results = []
    for n in names:
        results.append((n, await read_sensor(n)))
    return results
''',
    py_reference='''import asyncio


async def read_sensor(name):
    """Pretend to talk to a sensor. Takes 50 ms. Do not change this."""
    await asyncio.sleep(0.05)
    return len(name) * 7


async def sweep_all(names):
    """Read every sensor and return [(name, value)] in the given order."""
    values = await asyncio.gather(*(read_sensor(n) for n in names))
    return list(zip(names, values))
''',
    py_checker=py_async('''
import asyncio, time

async def _archie_main():
    try:
        got = await sweep_all(["port", "aft", "dorsal"])
    except Exception as e:
        for i in range(2): _report(i, False, f"raised {type(e).__name__}: {e}")
        got = None
    if got is not None:
        got = list(got)
        _report(0, len(got) == 3 and all(len(p) == 2 for p in got), f"got {_short(got)}")
        _report(1, [p[0] for p in got] == ["port", "aft", "dorsal"], f"order was {[p[0] for p in got]}")

    try:
        empty = list(await sweep_all([]))
        _report(2, empty == [], f"empty sweep gave {empty}")
    except Exception as e:
        _report(2, False, f"empty sweep raised {type(e).__name__}: {e}")

    names = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"]
    t = time.time()
    try:
        got8 = list(await sweep_all(names))
        el = time.time() - t
        _report(3, el < 0.25, f"eight sensors took {el:.3f}s (sequential would be 0.40s, concurrent about 0.05s)")
        _report(4, got8 == [(n, len(n) * 7) for n in names], f"values: {_short(got8)}")
    except Exception as e:
        _report(3, False, f"raised {type(e).__name__}: {e}")
        _report(4, False, "not reached")
'''),
    rs_spec="""
<p>Rewrite <code>sweep_all(names)</code> so the sensor reads happen in parallel threads.
Keep <code>read_sensor</code> exactly as it is. Return <code>(name, value)</code> pairs
in the order given. <code>std::thread::scope</code> lets the threads borrow
<code>names</code> safely.</p>
""",
    rs_stub='''use std::thread;
use std::time::Duration;

/// Pretend to talk to a sensor. Takes 50 ms. Do not change this.
fn read_sensor(name: &str) -> u32 {
    thread::sleep(Duration::from_millis(50));
    name.len() as u32 * 7
}

/// Read every sensor and return (name, value) in the given order.
fn sweep_all(names: &[&str]) -> Vec<(String, u32)> {
    // One at a time. Eight sensors take 400 ms. Make them overlap.
    names.iter().map(|n| (n.to_string(), read_sensor(n))).collect()
}
''',
    rs_reference='''use std::thread;
use std::time::Duration;

/// Pretend to talk to a sensor. Takes 50 ms. Do not change this.
fn read_sensor(name: &str) -> u32 {
    thread::sleep(Duration::from_millis(50));
    name.len() as u32 * 7
}

/// Read every sensor and return (name, value) in the given order.
fn sweep_all(names: &[&str]) -> Vec<(String, u32)> {
    thread::scope(|s| {
        let handles: Vec<_> = names
            .iter()
            .map(|&n| s.spawn(move || (n.to_string(), read_sensor(n))))
            .collect();
        handles.into_iter().map(|h| h.join().unwrap()).collect()
    })
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let got = sweep_all(&["port", "aft", "dorsal"]);
    __report(0, got.len() == 3, format!("got {:?}", got));
    let names: Vec<&str> = got.iter().map(|(n, _)| n.as_str()).collect();
    __report(1, names == vec!["port", "aft", "dorsal"], format!("order was {:?}", names));

    let empty = sweep_all(&[]);
    __report(2, empty.is_empty(), format!("empty sweep gave {:?}", empty));

    let eight = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8"];
    let t = std::time::Instant::now();
    let got8 = sweep_all(&eight);
    let el = t.elapsed();
    __report(3, el.as_millis() < 250, format!("eight sensors took {:?} (sequential would be 400ms, parallel about 50ms)", el));
    let want: Vec<(String, u32)> = eight.iter().map(|n| (n.to_string(), n.len() as u32 * 7)).collect();
    __report(4, got8 == want, format!("values: {:?}", got8));
}
'''),
)

# -------------------------------------------------------------- 35
_m(
    season=5, num=35, slug="35-the-slow-lookup", id="bridge-s5m35", station="engineering",
    title="The Slow Lookup", stardate="Stardate 55158.6",
    crew=["skree", "raghunathan"],
    minutes=25,
    blurb="Which of our two hundred thousand log entries also appear in theirs? The "
          "current answer will be ready in about a week.",
    briefing="""
<p>Lt. Skree wants every entry id in our log that also appears in the other ship's log,
in our order. Both logs have about two hundred thousand entries. The current routine
checks each of ours against every one of theirs, which is forty billion comparisons,
and Skree has calculated it will finish "on Thursday, of a different week".</p>

<p>The fix is not a faster loop. It is a different data structure: put theirs into a
set, where membership is a hash lookup rather than a scan, and the same job takes a
fraction of a second. ARCHIE will check the small cases first, then a medium one with a
stopwatch, and only if that is fast will it attempt the full two hundred thousand. Do
not, Commander Raghunathan says, make it attempt the full two hundred thousand the
slow way.</p>
""",
    debrief="""
<p>Sixty-six thousand shared entries in a tenth of a second. Every one of them is from
before the gap. After the gap, nothing matches, until tomorrow's stardate, which is in
both. Skree has stopped writing and started reading what Skree has written.</p>
""",
    objectives=[
        "Common ids on a small case, in our order",
        "No overlap gives nothing",
        "Ids in theirs but not ours are not included",
        "A medium case is fast (a set, not a scan)",
        "The full two hundred thousand, if the medium case was fast",
    ],
    hint="Build a set from <code>theirs</code> once, then keep each of <code>ours</code> "
         "that is in the set. That is O(n) instead of O(n²). Rust: "
         "<code>HashSet</code>; Python: <code>set()</code>.",
    py_spec="""
<p>Write <code>common_ids(ours, theirs)</code>: return the ids from <code>ours</code>
that also appear in <code>theirs</code>, in the order they appear in <code>ours</code>.
Both inputs are lists of integers with no duplicates. It must be fast for two hundred
thousand entries each.</p>
""",
    py_stub='''def common_ids(ours, theirs):
    """Ids in `ours` that also appear in `theirs`, in our order."""
    # Forty billion comparisons at full size. There is a better structure.
    return [x for x in ours if x in theirs]
''',
    py_reference='''def common_ids(ours, theirs):
    """Ids in `ours` that also appear in `theirs`, in our order."""
    lookup = set(theirs)
    return [x for x in ours if x in lookup]
''',
    py_checker=py_custom('''
import time

_g = _guard(0, lambda: common_ids([5, 1, 9, 3, 7], [3, 4, 5, 6]), "small case")
if _g is not _FAILED:
    _report(0, _g == [5, 3], f"got {_short(_g)}, wanted [5, 3]")

_g = _guard(1, lambda: common_ids([1, 2, 3], [4, 5, 6]), "no overlap")
if _g is not _FAILED:
    _report(1, _g == [], f"got {_short(_g)}, wanted []")

_g = _guard(2, lambda: common_ids([1, 2], [1, 2, 3, 4]), "theirs has extras")
if _g is not _FAILED:
    _report(2, _g == [1, 2], f"got {_short(_g)}, wanted [1, 2]")

_ours = list(range(0, 60000, 2))
_theirs = list(range(0, 90000, 3))
_t = time.time()
_g = _guard(3, lambda: common_ids(_ours, _theirs), "medium case")
_el = time.time() - _t
_fast = _g is not _FAILED and _el < 0.3
if _g is not _FAILED:
    _report(3, _fast and _g == list(range(0, 60000, 6)), f"30,000 x 30,000 took {_el:.3f}s (a set does this in milliseconds; a scan takes seconds)")

if not _fast:
    _report(4, False, "not attempted: the medium case was already slow, and the full size would take a very long time")
else:
    _ours = list(range(0, 400000, 2))
    _theirs = list(range(0, 600000, 3))
    _t = time.time()
    _g = _guard(4, lambda: common_ids(_ours, _theirs), "full size")
    _el = time.time() - _t
    if _g is not _FAILED:
        _report(4, _el < 3.0 and len(_g) == 66667 and _g[:3] == [0, 6, 12], f"200,000 x 200,000 took {_el:.3f}s, {len(_g)} common")
'''),
    rs_spec="""
<p>Write <code>common_ids(ours: &amp;[u32], theirs: &amp;[u32]) -&gt; Vec&lt;u32&gt;</code>:
the ids from <code>ours</code> that also appear in <code>theirs</code>, in the order
they appear in <code>ours</code>. Both inputs have no duplicates. It must be fast for
two hundred thousand entries each.</p>
""",
    rs_stub='''/// Ids in `ours` that also appear in `theirs`, in our order.
fn common_ids(ours: &[u32], theirs: &[u32]) -> Vec<u32> {
    // Forty billion comparisons at full size. There is a better structure.
    ours.iter().copied().filter(|x| theirs.contains(x)).collect()
}
''',
    rs_reference='''use std::collections::HashSet;

/// Ids in `ours` that also appear in `theirs`, in our order.
fn common_ids(ours: &[u32], theirs: &[u32]) -> Vec<u32> {
    let lookup: HashSet<u32> = theirs.iter().copied().collect();
    ours.iter().copied().filter(|x| lookup.contains(x)).collect()
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let got = common_ids(&[5, 1, 9, 3, 7], &[3, 4, 5, 6]);
    __report(0, got == vec![5, 3], format!("got {:?}, wanted [5, 3]", got));
    let got = common_ids(&[1, 2, 3], &[4, 5, 6]);
    __report(1, got.is_empty(), format!("got {:?}, wanted []", got));
    let got = common_ids(&[1, 2], &[1, 2, 3, 4]);
    __report(2, got == vec![1, 2], format!("got {:?}, wanted [1, 2]", got));

    let ours: Vec<u32> = (0..40000).map(|i| i * 2).collect();
    let theirs: Vec<u32> = (0..40000).map(|i| i * 3).collect();
    let t = std::time::Instant::now();
    let got = common_ids(&ours, &theirs);
    let el = t.elapsed();
    let fast = el.as_millis() < 500;
    let want: Vec<u32> = (0..80000).step_by(6).map(|x| x as u32).collect();
    __report(3, fast && got == want, format!("40,000 x 40,000 took {:?} (a HashSet does this in milliseconds)", el));

    if !fast {
        __report(4, false, "not attempted: the medium case was already slow".to_string());
    } else {
        let ours: Vec<u32> = (0..200000).map(|i| i * 2).collect();
        let theirs: Vec<u32> = (0..200000).map(|i| i * 3).collect();
        let t = std::time::Instant::now();
        let got = common_ids(&ours, &theirs);
        let el = t.elapsed();
        __report(4, el.as_millis() < 3000 && got.len() == 66667 && got[..3] == [0, 6, 12], format!("200,000 x 200,000 took {:?}, {} common", el, got.len()));
    }
}
'''),
)

# -------------------------------------------------------------- 36
_m(
    season=5, num=36, slug="36-warp-tables", id="bridge-s5m36", station="engineering",
    title="The Warp Tables", stardate="Stardate 55160.1",
    crew=["raghunathan", "tannenbaum"],
    minutes=25,
    blurb="The warp energy table is computed by a formula that calls itself twice. "
          "By entry forty it has called itself four hundred million times.",
    briefing="""
<p>The energy needed for warp factor <em>n</em> is the sum of the energies for
<em>n - 1</em> and <em>n - 2</em>, starting from 2 and 3. Ensign Tannenbaum wrote this
down exactly as stated, as a function that calls itself twice, and it is beautiful and
correct and for factor 40 it makes four hundred million calls. For factor 80 it would
finish after the ship was decommissioned.</p>

<p>The formula is fine. The repetition is the problem: it computes the same small values
over and over. Remember them, or build the table from the bottom up in a loop, and
factor 80 takes no time at all. ARCHIE will time a medium factor first and only try
factor 80 if that was fast, because Commander Raghunathan does not want to explain a
frozen console to the Captain again.</p>
""",
    debrief="""
<p>Factor 80 in a millisecond. Ensign Tannenbaum has asked why the slow version was
wrong if it gave the right answer, and Commander Raghunathan has told him it was not
wrong, it was <em>late</em>, and that in Engineering those are the same thing. He has
written that down. It is the first thing he has written down all season.</p>
""",
    objectives=[
        "Factors 0 and 1 are 2 and 3",
        "Small factors match the recurrence",
        "Factor 40 is 433,494,437",
        "A medium factor is fast (no repeated work)",
        "Factor 80 is 99,194,853,094,755,497, if the medium one was fast",
    ],
    hint="Either build up from the bottom in a loop, keeping the last two values, or "
         "cache results in a dictionary or map so each factor is computed once. Python's "
         "<code>functools.lru_cache</code> is a one-line version of the second.",
    py_spec="""
<p>Rewrite <code>warp_energy(n)</code> so it returns the same values as the recurrence
(<code>warp_energy(0) == 2</code>, <code>warp_energy(1) == 3</code>, and each later
value is the sum of the two before it) but without repeating work, so that
<code>warp_energy(80)</code> is instant.</p>
""",
    py_stub='''def warp_energy(n):
    """Energy for warp factor n: 2, 3, 5, 8, 13, ... (each the sum of the two before)."""
    # Correct, and exponentially slow. Factor 40 makes 400 million calls.
    if n == 0:
        return 2
    if n == 1:
        return 3
    return warp_energy(n - 1) + warp_energy(n - 2)
''',
    py_reference='''def warp_energy(n):
    """Energy for warp factor n: 2, 3, 5, 8, 13, ... (each the sum of the two before)."""
    a, b = 2, 3
    for _ in range(n):
        a, b = b, a + b
    return a
''',
    py_checker=py_custom('''
import time

_g = _guard(0, lambda: (warp_energy(0), warp_energy(1)), "factors 0 and 1")
if _g is not _FAILED:
    _report(0, _g == (2, 3), f"got {_g}, wanted (2, 3)")

_g = _guard(1, lambda: [warp_energy(k) for k in range(2, 11)], "factors 2..10")
if _g is not _FAILED:
    _report(1, _g == [5, 8, 13, 21, 34, 55, 89, 144, 233], f"got {_short(_g)}, wanted [5, 8, 13, 21, 34, 55, 89, 144, 233]")

_t = time.time()
_g = _guard(3, lambda: warp_energy(35), "factor 35")
_el = time.time() - _t
_fast = _g is not _FAILED and _el < 0.15
if _g is not _FAILED:
    _report(3, _fast and _g == 39088169, f"factor 35 took {_el:.3f}s (the slow version takes seconds, the fast one microseconds)")

if not _fast:
    _report(2, False, "not attempted: factor 35 was already slow, factor 40 would take much longer")
    _report(4, False, "not attempted: factor 35 was already slow, factor 80 would not finish")
else:
    _g = _guard(2, lambda: warp_energy(40), "factor 40")
    if _g is not _FAILED:
        _report(2, _g == 433494437, f"got {_g}, wanted 433494437")
    _g = _guard(4, lambda: warp_energy(80), "factor 80")
    if _g is not _FAILED:
        _report(4, _g == 99194853094755497, f"got {_g}, wanted 99194853094755497")
'''),
    rs_spec="""
<p>Rewrite <code>warp_energy(n: u32) -&gt; u64</code> so it returns the same values as
the recurrence (<code>warp_energy(0) == 2</code>, <code>warp_energy(1) == 3</code>, and
each later value is the sum of the two before it) but without repeating work, so that
<code>warp_energy(80)</code> is instant.</p>
""",
    rs_stub='''/// Energy for warp factor n: 2, 3, 5, 8, 13, ... (each the sum of the two before).
fn warp_energy(n: u32) -> u64 {
    // Correct, and exponentially slow. Factor 40 makes 400 million calls.
    match n {
        0 => 2,
        1 => 3,
        _ => warp_energy(n - 1) + warp_energy(n - 2),
    }
}
''',
    rs_reference='''/// Energy for warp factor n: 2, 3, 5, 8, 13, ... (each the sum of the two before).
fn warp_energy(n: u32) -> u64 {
    let (mut a, mut b) = (2u64, 3u64);
    for _ in 0..n {
        let next = a + b;
        a = b;
        b = next;
    }
    a
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let g = (warp_energy(0), warp_energy(1));
    __report(0, g == (2, 3), format!("got {:?}, wanted (2, 3)", g));
    let g: Vec<u64> = (2..11).map(warp_energy).collect();
    __report(1, g == vec![5, 8, 13, 21, 34, 55, 89, 144, 233], format!("got {:?}", g));

    let t = std::time::Instant::now();
    let g = warp_energy(42);
    let el = t.elapsed();
    let fast = el.as_millis() < 300;
    __report(3, fast && g == 1134903170, format!("factor 42 took {:?} (the slow version takes seconds, the fast one microseconds)", el));

    if !fast {
        __report(2, false, "not attempted: factor 42 was already slow".to_string());
        __report(4, false, "not attempted: factor 42 was already slow, factor 80 would not finish".to_string());
    } else {
        let g = warp_energy(40);
        __report(2, g == 433494437, format!("got {}, wanted 433494437", g));
        let g = warp_energy(80);
        __report(4, g == 99194853094755497, format!("got {}, wanted 99194853094755497", g));
    }
}
'''),
)

# -------------------------------------------------------------- 37
_m(
    season=5, num=37, slug="37-reading-the-traceback", id="bridge-s5m37", station="sickbay",
    title="Reading the Traceback", stardate="Stardate 55161.7",
    crew=["skree", "tannenbaum", "raghunathan"],
    minutes=25,
    blurb="A median routine with several things wrong with it. Sickbay is where you "
          "find out which, one symptom at a time.",
    briefing="""
<p>Welcome to Sickbay, which on this ship is where broken code goes to be diagnosed
rather than replaced. Commander Raghunathan's rule is that you do not rewrite a
routine until you can say what was wrong with it, because otherwise you will write
the same thing wrong again.</p>

<p>The patient is a median function. It has more than one thing wrong with it. Run the
diagnostics, read what ARCHIE says about each failing objective, and fix <em>that</em>.
Then run again. Lt. Skree has already diagnosed it from across the room, but has been
asked, gently, to let you do it.</p>
""",
    debrief="""
<p>Four faults: it sorted the caller's list in place, it picked the element after the
middle, it used integer division on the even case, and it fell over on an empty list.
Lt. Skree says that was three faults and a symptom. Commander Raghunathan says that is
what four faults looks like from across the room.</p>
""",
    objectives=[
        "The median of an odd-length list is the middle value",
        "The median of an even-length list is the mean of the two middle values, 2.5 not 2",
        "The caller's list is not reordered",
        "An empty list gives None, not a crash",
        "A single value is its own median",
    ],
    hint="Sort a copy. For odd length the middle index is <code>n // 2</code>. For even, "
         "average the two middle values with real division. Check for empty first. Each "
         "failing objective points at one of those.",
    py_spec="""
<p>Fix <code>median(values)</code> so it returns the median of a list of numbers: the
middle value when the count is odd, the mean of the two middle values when even, and
<code>None</code> for an empty list. It must not modify the caller's list.</p>
""",
    py_stub='''def median(values):
    """The median of a list of numbers, or None for an empty list."""
    values.sort()
    n = len(values)
    if n % 2 == 1:
        return values[n // 2 + 1]
    return (values[n // 2 - 1] + values[n // 2]) // 2
''',
    py_reference='''def median(values):
    """The median of a list of numbers, or None for an empty list."""
    if not values:
        return None
    ordered = sorted(values)
    n = len(ordered)
    if n % 2 == 1:
        return ordered[n // 2]
    return (ordered[n // 2 - 1] + ordered[n // 2]) / 2
''',
    py_checker=py_custom('''
_g = _guard(0, lambda: median([9, 1, 5]), "median([9, 1, 5])")
if _g is not _FAILED:
    _report(0, _g == 5, f"got {_g!r}, wanted 5")

_g = _guard(1, lambda: median([4, 1, 3, 2]), "median([4, 1, 3, 2])")
if _g is not _FAILED:
    _report(1, _g == 2.5, f"got {_g!r}, wanted 2.5")

def _t2():
    data = [3, 1, 2]
    median(data)
    return data
_g = _guard(2, _t2, "caller's list after median()")
if _g is not _FAILED:
    _report(2, _g == [3, 1, 2], f"the caller's list is now {_g}, wanted it left as [3, 1, 2]")

_g = _guard(3, lambda: median([]), "median([])")
if _g is not _FAILED:
    _report(3, _g is None, f"got {_g!r}, wanted None")

_g = _guard(4, lambda: median([7]), "median([7])")
if _g is not _FAILED:
    _report(4, _g == 7, f"got {_g!r}, wanted 7")
'''),
    rs_spec="""
<p>Fix <code>median(values: &amp;[f64]) -&gt; Option&lt;f64&gt;</code>: the middle value
when the count is odd, the mean of the two middle values when even, and
<code>None</code> for an empty slice. Several things are wrong with it; the failing
objectives will tell you which.</p>
""",
    rs_stub='''/// The median of a list of numbers, or None for an empty list.
fn median(values: &[f64]) -> Option<f64> {
    let mut v = values.to_vec();
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let n = v.len();
    if n % 2 == 1 {
        Some(v[n / 2 + 1])
    } else {
        Some((v[n / 2 - 1] + v[n / 2]) / 2.0)
    }
}
''',
    rs_reference='''/// The median of a list of numbers, or None for an empty list.
fn median(values: &[f64]) -> Option<f64> {
    if values.is_empty() {
        return None;
    }
    let mut v = values.to_vec();
    v.sort_by(|a, b| a.partial_cmp(b).unwrap());
    let n = v.len();
    if n % 2 == 1 {
        Some(v[n / 2])
    } else {
        Some((v[n / 2 - 1] + v[n / 2]) / 2.0)
    }
}
''',
    rs_checker=rs_cases("median", [
        (["&[9.0, 1.0, 5.0]"], "Some(5.0)"),
        (["&[4.0, 1.0, 3.0, 2.0]"], "Some(2.5)"),
        (["&[-3.0, -1.0, -2.0]"], "Some(-2.0)"),
        (["&[]"], "None"),
        (["&[7.0]"], "Some(7.0)"),
    ], check="match (got, want) { (Some(a), Some(b)) => (a - b).abs() < 1e-9, (None, None) => true, _ => false }",
       want_ty="Option<f64>"),
)

# -------------------------------------------------------------- 38
_m(
    season=5, num=38, slug="38-write-the-test", id="bridge-s5m38", station="sickbay",
    title="Write the Test", stardate="Stardate 55163.2",
    crew=["raghunathan", "tkala"],
    minutes=25,
    blurb="This time you do not write the function. You write the thing that decides "
          "whether somebody else's function is right.",
    briefing="""
<p>Commander Raghunathan has four implementations of the shield clamp from Season 1,
written by four different people, and she does not want to read them. She wants a
<em>test</em>: a function that takes a clamp implementation, tries it, and says whether
it is correct. Then she can run it on all four and only read the ones that fail.</p>

<p>A test is only worth anything if it can fail. So ARCHIE will hand your test a correct
clamp and expect a yes, and then several broken ones, each broken in a specific way, and
expect a no for each. If your test says yes to a broken clamp, it did not check the
thing that was broken. That is the whole discipline of testing, in one mission.</p>
""",
    debrief="""
<p>Two of the four clamps failed your test. One was Ensign Tannenbaum's, which had no
lower bound. The other was Chief T'Kala's, which returned 99 for anything over 100,
because, she says, "nothing on this ship is ever actually at 100 percent". She has been
asked to fix it and has said she will "think about it".</p>
""",
    objectives=[
        "Accepts a correct clamp",
        "Rejects a clamp with no lower bound",
        "Rejects a clamp whose upper bound is off by one",
        "Rejects a clamp that does nothing at all",
        "Accepts a second correct clamp written a different way",
    ],
    hint="Call the clamp with a handful of chosen inputs and compare against what a "
         "correct clamp returns: something negative, zero, something in range, exactly "
         "100, something above 100. Return whether every one matched. The inputs you "
         "choose <em>are</em> the test.",
    py_spec="""
<p>Write <code>test_clamp(clamp)</code>: <code>clamp</code> is a function of one integer
argument. Return <code>True</code> if it correctly clamps to 0..100 inclusive (values
below 0 become 0, above 100 become 100, others unchanged), and <code>False</code>
otherwise.</p>
""",
    py_stub='''def test_clamp(clamp):
    """Does `clamp` correctly limit values to 0..100? True if so."""
    # TODO: try it on inputs that would expose each way it could be wrong.
    return True
''',
    py_reference='''def test_clamp(clamp):
    """Does `clamp` correctly limit values to 0..100? True if so."""
    cases = [(-20, 0), (0, 0), (55, 55), (100, 100), (101, 100), (140, 100)]
    return all(clamp(x) == want for x, want in cases)
''',
    py_checker=py_custom('''
def _good(p):
    return max(0, min(100, p))

def _good2(p):
    if p < 0:
        return 0
    elif p > 100:
        return 100
    else:
        return p

def _no_lower(p):
    return min(100, p)

def _off_by_one(p):
    return min(99, max(0, p))

def _identity(p):
    return p

_g = _guard(0, lambda: test_clamp(_good), "test_clamp(correct clamp)")
if _g is not _FAILED:
    _report(0, _g is True, f"returned {_g!r} for a correct clamp, wanted True")

_g = _guard(1, lambda: test_clamp(_no_lower), "test_clamp(no lower bound)")
if _g is not _FAILED:
    _report(1, _g is False, f"returned {_g!r} for a clamp that lets negatives through, wanted False")

_g = _guard(2, lambda: test_clamp(_off_by_one), "test_clamp(upper bound 99)")
if _g is not _FAILED:
    _report(2, _g is False, f"returned {_g!r} for a clamp that tops out at 99, wanted False")

_g = _guard(3, lambda: test_clamp(_identity), "test_clamp(identity)")
if _g is not _FAILED:
    _report(3, _g is False, f"returned {_g!r} for a clamp that does nothing, wanted False")

_g = _guard(4, lambda: test_clamp(_good2), "test_clamp(correct clamp, if/elif style)")
if _g is not _FAILED:
    _report(4, _g is True, f"returned {_g!r} for a second correct clamp, wanted True")
'''),
    rs_spec="""
<p>Write <code>test_clamp(clamp: fn(i32) -&gt; i32) -&gt; bool</code>: return
<code>true</code> if <code>clamp</code> correctly limits values to 0..=100 (below 0
becomes 0, above 100 becomes 100, others unchanged), and <code>false</code> otherwise.</p>
""",
    rs_stub='''/// Does `clamp` correctly limit values to 0..=100? True if so.
fn test_clamp(clamp: fn(i32) -> i32) -> bool {
    // TODO: try it on inputs that would expose each way it could be wrong.
    let _ = clamp;
    true
}
''',
    rs_reference='''/// Does `clamp` correctly limit values to 0..=100? True if so.
fn test_clamp(clamp: fn(i32) -> i32) -> bool {
    let cases = [(-20, 0), (0, 0), (55, 55), (100, 100), (101, 100), (140, 100)];
    cases.iter().all(|&(x, want)| clamp(x) == want)
}
''',
    rs_checker=rs_custom('''
fn good(p: i32) -> i32 { p.clamp(0, 100) }
fn good2(p: i32) -> i32 { if p < 0 { 0 } else if p > 100 { 100 } else { p } }
fn no_lower(p: i32) -> i32 { p.min(100) }
fn off_by_one(p: i32) -> i32 { p.clamp(0, 99) }
fn identity(p: i32) -> i32 { p }

fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let g = test_clamp(good);
    __report(0, g, format!("returned {} for a correct clamp, wanted true", g));
    let g = test_clamp(no_lower);
    __report(1, !g, format!("returned {} for a clamp that lets negatives through, wanted false", g));
    let g = test_clamp(off_by_one);
    __report(2, !g, format!("returned {} for a clamp that tops out at 99, wanted false", g));
    let g = test_clamp(identity);
    __report(3, !g, format!("returned {} for a clamp that does nothing, wanted false", g));
    let g = test_clamp(good2);
    __report(4, g, format!("returned {} for a second correct clamp, wanted true", g));
}
'''),
)

# -------------------------------------------------------------- 39
_m(
    season=5, num=39, slug="39-the-flaky-sensor", id="bridge-s5m39", station="sickbay",
    title="The Flaky Sensor", stardate="Stardate 55164.8",
    crew=["skree", "raghunathan"],
    minutes=25,
    blurb="One sensor times out a third of the time and is fine the rest. Retry it, "
          "but know when to stop, and know when not to start.",
    briefing="""
<p>The dorsal sensor times out about a third of the time and answers perfectly the rest.
Lt. Skree does not want it replaced; Skree wants it <em>retried</em>, up to a set
number of attempts, and then given up on honestly. A timeout is worth retrying. A sensor
reporting that it is physically broken is not, and retrying it three times just wastes
three tries.</p>

<p>Commander Raghunathan adds one thing: the retry must not call the sensor more times
than it needs to. If the first read works, that is one call. Not two "to be sure". This
is a mission about restraint, and about telling two kinds of failure apart.</p>
""",
    debrief="""
<p>The dorsal sensor answers, on average, in 1.4 attempts. It has been pointed at the
other ship, and it reports that the other ship's dorsal sensor is pointed at us. Skree
has said "of course it is" and gone very still again.</p>
""",
    objectives=[
        "A read that succeeds first time is called exactly once",
        "Fails twice then succeeds, with three attempts: the value, in three calls",
        "Always times out, with three attempts: nothing, in exactly three calls",
        "One attempt and a timeout: nothing, in one call",
        "A broken sensor is not retried",
    ],
    hint="Loop up to <code>attempts</code> times. Return the value on success. On a "
         "timeout, continue to the next attempt. On any other failure, stop immediately. "
         "If the loop ends without a value, return nothing.",
    py_spec="""
<p>Write <code>read_with_retry(read, attempts)</code>: <code>read</code> is a function of
no arguments that returns a value or raises. Call it up to <code>attempts</code> times,
retrying only on <code>TimeoutError</code>, and return the first value it gives. If every
attempt times out, return <code>None</code>. Any <em>other</em> exception must
propagate immediately, not be retried.</p>
""",
    py_stub='''def read_with_retry(read, attempts):
    """Call read() up to `attempts` times, retrying only on TimeoutError."""
    # TODO
    return read()
''',
    py_reference='''def read_with_retry(read, attempts):
    """Call read() up to `attempts` times, retrying only on TimeoutError."""
    for _ in range(attempts):
        try:
            return read()
        except TimeoutError:
            continue
    return None
''',
    py_checker=py_custom('''
class _Fake:
    def __init__(self, script):
        self.script = list(script)   # each item: a value, or an exception class
        self.calls = 0
    def __call__(self):
        self.calls += 1
        item = self.script.pop(0) if self.script else TimeoutError
        if isinstance(item, type) and issubclass(item, BaseException):
            raise item("sensor")
        return item

_f = _Fake([42])
_g = _guard(0, lambda: read_with_retry(_f, 3), "succeeds first time")
if _g is not _FAILED:
    _report(0, _g == 42 and _f.calls == 1, f"got {_g!r} in {_f.calls} call(s), wanted 42 in 1")

_f = _Fake([TimeoutError, TimeoutError, 7])
_g = _guard(1, lambda: read_with_retry(_f, 3), "fails twice then succeeds")
if _g is not _FAILED:
    _report(1, _g == 7 and _f.calls == 3, f"got {_g!r} in {_f.calls} call(s), wanted 7 in 3")

_f = _Fake([TimeoutError, TimeoutError, TimeoutError, TimeoutError])
_g = _guard(2, lambda: read_with_retry(_f, 3), "always times out")
if _g is not _FAILED:
    _report(2, _g is None and _f.calls == 3, f"got {_g!r} in {_f.calls} call(s), wanted None in exactly 3")

_f = _Fake([TimeoutError, 5])
_g = _guard(3, lambda: read_with_retry(_f, 1), "one attempt, one timeout")
if _g is not _FAILED:
    _report(3, _g is None and _f.calls == 1, f"got {_g!r} in {_f.calls} call(s), wanted None in 1")

_f = _Fake([ValueError, 5])
try:
    _r = read_with_retry(_f, 3)
    _report(4, False, f"a ValueError was swallowed and {_r!r} returned after {_f.calls} call(s); it should propagate")
except ValueError:
    _report(4, _f.calls == 1, f"ValueError propagated after {_f.calls} call(s), wanted 1")
except Exception as e:
    _report(4, False, f"raised {type(e).__name__} instead of letting ValueError through")
'''),
    rs_spec="""
<p>Keep the enum as given. Write <code>read_with_retry(read: &amp;mut dyn FnMut() -&gt;
Result&lt;u32, SensorError&gt;, attempts: u32) -&gt; Option&lt;u32&gt;</code>: call
<code>read</code> up to <code>attempts</code> times, retrying only on
<code>SensorError::Timeout</code>. Return <code>Some(value)</code> on the first success.
If every attempt times out, return <code>None</code>. On <code>SensorError::Broken</code>,
stop immediately and return <code>None</code> without retrying.</p>
""",
    rs_stub='''#[derive(Debug, PartialEq)]
enum SensorError {
    Timeout,
    Broken,
}

/// Call `read` up to `attempts` times, retrying only on Timeout.
fn read_with_retry(read: &mut dyn FnMut() -> Result<u32, SensorError>, attempts: u32) -> Option<u32> {
    // TODO
    let _ = attempts;
    read().ok()
}
''',
    rs_reference='''#[derive(Debug, PartialEq)]
enum SensorError {
    Timeout,
    Broken,
}

/// Call `read` up to `attempts` times, retrying only on Timeout.
fn read_with_retry(read: &mut dyn FnMut() -> Result<u32, SensorError>, attempts: u32) -> Option<u32> {
    for _ in 0..attempts {
        match read() {
            Ok(v) => return Some(v),
            Err(SensorError::Timeout) => continue,
            Err(SensorError::Broken) => return None,
        }
    }
    None
}
''',
    rs_checker=rs_custom('''
fn fake(script: Vec<Result<u32, SensorError>>) -> (Box<dyn FnMut() -> Result<u32, SensorError>>, std::rc::Rc<std::cell::Cell<u32>>) {
    let calls = std::rc::Rc::new(std::cell::Cell::new(0));
    let c2 = calls.clone();
    let mut script = script.into_iter();
    (Box::new(move || { c2.set(c2.get() + 1); script.next().unwrap_or(Err(SensorError::Timeout)) }), calls)
}
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let (mut f, calls) = fake(vec![Ok(42)]);
    let g = read_with_retry(&mut *f, 3);
    __report(0, g == Some(42) && calls.get() == 1, format!("got {:?} in {} call(s), wanted Some(42) in 1", g, calls.get()));

    let (mut f, calls) = fake(vec![Err(SensorError::Timeout), Err(SensorError::Timeout), Ok(7)]);
    let g = read_with_retry(&mut *f, 3);
    __report(1, g == Some(7) && calls.get() == 3, format!("got {:?} in {} call(s), wanted Some(7) in 3", g, calls.get()));

    let (mut f, calls) = fake(vec![Err(SensorError::Timeout), Err(SensorError::Timeout), Err(SensorError::Timeout), Err(SensorError::Timeout)]);
    let g = read_with_retry(&mut *f, 3);
    __report(2, g == None && calls.get() == 3, format!("got {:?} in {} call(s), wanted None in exactly 3", g, calls.get()));

    let (mut f, calls) = fake(vec![Err(SensorError::Timeout), Ok(5)]);
    let g = read_with_retry(&mut *f, 1);
    __report(3, g == None && calls.get() == 1, format!("got {:?} in {} call(s), wanted None in 1", g, calls.get()));

    let (mut f, calls) = fake(vec![Err(SensorError::Broken), Ok(5)]);
    let g = read_with_retry(&mut *f, 3);
    __report(4, g == None && calls.get() == 1, format!("got {:?} in {} call(s), wanted None in 1 (Broken is not retried)", g, calls.get()));
}
'''),
)

# -------------------------------------------------------------- 40
_m(
    season=5, num=40, slug="40-warp-core-sequence", id="bridge-s5m40", station="engineering",
    title="The Warp Core Sequence", stardate="Stardate 55166.3",
    crew=["raghunathan", "dubois", "skree", "tkala"],
    minutes=30,
    blurb="Cold, warming, ready, engaged. The core must go through them in order, "
          "refuse to skip, and always be able to scram.",
    briefing="""
<p>The other Magnanimous has raised shields, and the Captain wants ours ready to move.
The warp core has four states, cold, warming, ready and engaged, and it moves through
them in that order and no other. You cannot engage a cold core. You cannot warm a core
that is already engaged. And from any state whatsoever, <em>scram</em> takes it straight
to cold, because that one is the emergency brake and it must never be refused.</p>

<p>Commander Raghunathan wants each transition to say whether it happened, so the
bridge can tell "engaged" from "you asked to engage a cold core and nothing occurred".
An invalid transition changes nothing and says so. This is a state machine, and it is
the shape of half of everything you will ever build: a thing with a state, and rules
about how the state may change.</p>
""",
    debrief="""
<p>Cold, warming, ready. Engaged. The Captain has said "hold there", and the Maggie is
holding, and across two kilometres of nothing the other ship is holding too. Chief
T'Kala has moved Gerald away from the viewscreen, which she has never done before.</p>

<p><strong>Deep Space is complete.</strong> Whatever happens tomorrow, the last season
opens at Commander, and it is called Terminus.</p>
""",
    objectives=[
        "A new core is cold; warm, ready, engage step through in order",
        "Skipping ahead is refused and changes nothing",
        "Going backwards without disengage is refused",
        "Disengage returns an engaged core to ready",
        "Scram works from every state and always lands on cold",
    ],
    hint="Store the state. Each method checks the current state, and only if the "
         "transition is allowed does it change state and return true. <code>scram</code> "
         "ignores the current state entirely. A <code>match</code> on the state per "
         "method keeps it readable.",
    py_spec="""
<p>Write a class <code>WarpCore</code> with attribute <code>state</code>, one of
<code>"cold"</code>, <code>"warming"</code>, <code>"ready"</code>, <code>"engaged"</code>,
starting cold. Methods <code>warm()</code> (cold to warming), <code>ready()</code>
(warming to ready), <code>engage()</code> (ready to engaged), <code>disengage()</code>
(engaged to ready) each return <code>True</code> and change state only if the core is in
the right starting state, otherwise return <code>False</code> and change nothing.
<code>scram()</code> sets the state to cold from anywhere and returns <code>True</code>.</p>
""",
    py_stub='''class WarpCore:
    """cold -> warming -> ready -> engaged, and scram from anywhere."""

    def __init__(self):
        self.state = "cold"

    def warm(self):
        # TODO
        return False

    def ready(self):
        # TODO
        return False

    def engage(self):
        # TODO
        return False

    def disengage(self):
        # TODO
        return False

    def scram(self):
        # TODO
        return False
''',
    py_reference='''class WarpCore:
    """cold -> warming -> ready -> engaged, and scram from anywhere."""

    def __init__(self):
        self.state = "cold"

    def _step(self, from_state, to_state):
        if self.state != from_state:
            return False
        self.state = to_state
        return True

    def warm(self):
        return self._step("cold", "warming")

    def ready(self):
        return self._step("warming", "ready")

    def engage(self):
        return self._step("ready", "engaged")

    def disengage(self):
        return self._step("engaged", "ready")

    def scram(self):
        self.state = "cold"
        return True
''',
    py_checker=py_custom('''
def _t0():
    c = WarpCore()
    trail = [c.state]
    ok = [c.warm(), c.ready(), c.engage()]
    trail.append(c.state)
    return trail, ok
_g = _guard(0, _t0, "the happy path")
if _g is not _FAILED:
    _report(0, _g == (["cold", "engaged"], [True, True, True]), f"started {_g[0][0]}, ended {_g[0][1]}, results {_g[1]}")

def _t1():
    c = WarpCore()
    r = c.engage()
    return r, c.state
_g = _guard(1, _t1, "engage a cold core")
if _g is not _FAILED:
    _report(1, _g == (False, "cold"), f"engage on cold returned {_g[0]}, state now {_g[1]!r}, wanted False and 'cold'")

def _t2():
    c = WarpCore()
    c.warm(); c.ready(); c.engage()
    r = c.warm()
    return r, c.state
_g = _guard(2, _t2, "warm an engaged core")
if _g is not _FAILED:
    _report(2, _g == (False, "engaged"), f"warm on engaged returned {_g[0]}, state now {_g[1]!r}, wanted False and 'engaged'")

def _t3():
    c = WarpCore()
    c.warm(); c.ready(); c.engage()
    r = c.disengage()
    return r, c.state
_g = _guard(3, _t3, "disengage")
if _g is not _FAILED:
    _report(3, _g == (True, "ready"), f"disengage returned {_g[0]}, state now {_g[1]!r}, wanted True and 'ready'")

def _t4():
    out = []
    for steps in ([], ["warm"], ["warm", "ready"], ["warm", "ready", "engage"]):
        c = WarpCore()
        for s in steps:
            getattr(c, s)()
        out.append((c.scram(), c.state))
    return out
_g = _guard(4, _t4, "scram from every state")
if _g is not _FAILED:
    _report(4, all(r == (True, "cold") for r in _g), f"scram results per state: {_g}")
'''),
    rs_spec="""
<p>Keep the enum as given. Write <code>WarpCore</code> with <code>WarpCore::new()</code>
(cold), <code>fn state(&amp;self) -&gt; CoreState</code>, and methods
<code>warm</code>, <code>ready</code>, <code>engage</code>, <code>disengage</code>, each
<code>fn(&amp;mut self) -&gt; bool</code>: they change state and return
<code>true</code> only from the correct starting state (cold to warming, warming to
ready, ready to engaged, engaged to ready), otherwise return <code>false</code> and
change nothing. <code>scram(&amp;mut self) -&gt; bool</code> sets cold from anywhere and
returns <code>true</code>.</p>
""",
    rs_stub='''#[derive(Debug, Clone, Copy, PartialEq)]
enum CoreState {
    Cold,
    Warming,
    Ready,
    Engaged,
}

/// Cold -> Warming -> Ready -> Engaged, and scram from anywhere.
struct WarpCore {
    state: CoreState,
}

impl WarpCore {
    fn new() -> WarpCore { WarpCore { state: CoreState::Cold } }
    fn state(&self) -> CoreState { self.state }
    fn warm(&mut self) -> bool { false }        // TODO
    fn ready(&mut self) -> bool { false }       // TODO
    fn engage(&mut self) -> bool { false }      // TODO
    fn disengage(&mut self) -> bool { false }   // TODO
    fn scram(&mut self) -> bool { false }       // TODO
}
''',
    rs_reference='''#[derive(Debug, Clone, Copy, PartialEq)]
enum CoreState {
    Cold,
    Warming,
    Ready,
    Engaged,
}

/// Cold -> Warming -> Ready -> Engaged, and scram from anywhere.
struct WarpCore {
    state: CoreState,
}

impl WarpCore {
    fn new() -> WarpCore { WarpCore { state: CoreState::Cold } }
    fn state(&self) -> CoreState { self.state }

    fn step(&mut self, from: CoreState, to: CoreState) -> bool {
        if self.state == from {
            self.state = to;
            true
        } else {
            false
        }
    }
    fn warm(&mut self) -> bool { self.step(CoreState::Cold, CoreState::Warming) }
    fn ready(&mut self) -> bool { self.step(CoreState::Warming, CoreState::Ready) }
    fn engage(&mut self) -> bool { self.step(CoreState::Ready, CoreState::Engaged) }
    fn disengage(&mut self) -> bool { self.step(CoreState::Engaged, CoreState::Ready) }
    fn scram(&mut self) -> bool { self.state = CoreState::Cold; true }
}
''',
    rs_checker=rs_custom('''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
    let mut c = WarpCore::new();
    let start = c.state();
    let ok = (c.warm(), c.ready(), c.engage());
    __report(0, start == CoreState::Cold && ok == (true, true, true) && c.state() == CoreState::Engaged,
             format!("started {:?}, results {:?}, ended {:?}", start, ok, c.state()));

    let mut c = WarpCore::new();
    let r = c.engage();
    __report(1, !r && c.state() == CoreState::Cold, format!("engage on cold returned {}, state now {:?}, wanted false and Cold", r, c.state()));

    let mut c = WarpCore::new();
    c.warm(); c.ready(); c.engage();
    let r = c.warm();
    __report(2, !r && c.state() == CoreState::Engaged, format!("warm on engaged returned {}, state now {:?}, wanted false and Engaged", r, c.state()));

    let mut c = WarpCore::new();
    c.warm(); c.ready(); c.engage();
    let r = c.disengage();
    __report(3, r && c.state() == CoreState::Ready, format!("disengage returned {}, state now {:?}, wanted true and Ready", r, c.state()));

    let mut all_ok = true;
    let mut detail = Vec::new();
    for steps in 0..4 {
        let mut c = WarpCore::new();
        if steps >= 1 { c.warm(); }
        if steps >= 2 { c.ready(); }
        if steps >= 3 { c.engage(); }
        let r = c.scram();
        detail.push((r, c.state()));
        if !r || c.state() != CoreState::Cold { all_ok = false; }
    }
    __report(4, all_ok, format!("scram results per state: {:?}", detail));
}
'''),
)
