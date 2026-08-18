"""Authoring helpers for missions.

Most missions are "call this function with these inputs, expect these
outputs". Writing that checker by hand forty times is how typos get into
the answers, so `py_cases` and `rs_cases` generate it from a table.
Anything stateful (classes, iterators, races) still gets a hand-written
checker; the wire format is the same either way.

WIRE FORMAT, one line per objective, parsed by bridge.js:

    BRIDGE|<index>|<PASS or FAIL>|<what came back>
"""

from __future__ import annotations

MISSIONS: list[dict] = []


def _m(**kw):
    """Register a mission. Fills in the per-language keys it can."""
    kw.setdefault("crew", [])
    kw.setdefault("minutes", 15)
    MISSIONS.append(kw)


# ------------------------------------------------------------ Python
def py_cases(fn: str, cases: list, check: str = "_got == _want") -> str:
    """Checker that calls `fn(*args)` per case and compares.

    cases: [(args_tuple, want), ...]
    check: a Python expression over _got and _want. Defaults to equality.
           For floats use "abs(_got - _want) < 1e-6".
    """
    return f'''
def _short(x):
    s = repr(x)
    return s if len(s) <= 70 else s[:67] + "..."

_cases = {cases!r}
for _i, (_args, _want) in enumerate(_cases):
    _call = "{fn}(" + ", ".join(_short(a) for a in _args) + ")"
    try:
        _got = {fn}(*_args)
    except Exception as _e:
        print(f"BRIDGE|{{_i}}|FAIL|{{_call}} raised {{type(_e).__name__}}: {{_e}}")
        continue
    try:
        _ok = bool({check})
    except Exception:
        _ok = False
    print(f"BRIDGE|{{_i}}|{{'PASS' if _ok else 'FAIL'}}|{{_call}} returned {{_short(_got)}}, wanted {{_short(_want)}}")
'''


def py_custom(body: str) -> str:
    """A hand-written checker. Gets the same _report helper for free."""
    return '''
def _short(x):
    s = repr(x)
    return s if len(s) <= 70 else s[:67] + "..."

def _report(i, ok, detail=""):
    print(f"BRIDGE|{i}|{'PASS' if ok else 'FAIL'}|{detail}")

def _guard(i, thunk, detail=""):
    """Run thunk; a raised exception is a FAIL with the exception shown."""
    try:
        return thunk()
    except Exception as e:
        _report(i, False, (detail + " " if detail else "") + f"raised {type(e).__name__}: {e}")
        return _FAILED

class _Failed: pass
_FAILED = _Failed()
''' + body


def py_async(body: str) -> str:
    """A hand-written checker whose work lives in `async def _archie_main()`.

    Locally (plain CPython, no running loop) it is run with asyncio.run().
    In the browser, Pyodide's event loop is already running and would refuse
    that, so the coroutine is handed back in _archie_pending and the harness
    awaits it at top level. `body` must define _archie_main.
    """
    return py_custom(body) + '''

import asyncio as _asyncio, sys as _sys
if _sys.platform == "emscripten":
    _archie_pending = _archie_main()
else:
    _asyncio.run(_archie_main())
'''


# -------------------------------------------------------------- Rust
RS_PRELUDE = '''
fn __short(s: String) -> String {
    if s.chars().count() <= 70 { s } else { s.chars().take(67).collect::<String>() + "..." }
}
fn __report(i: usize, ok: bool, detail: String) {
    println!("BRIDGE|{}|{}|{}", i, if ok { "PASS" } else { "FAIL" }, detail);
}
'''


def rs_cases(fn: str, cases: list, check: str = "got == want",
             want_ty: str | None = None) -> str:
    """Checker that calls `fn(args...)` per case, in Rust.

    cases: [(["arg1_src", "arg2_src"], "want_src"), ...] where every element
           is Rust SOURCE, so "61", "\\"too cold\\"", "vec![1, 2]" all work.
    check: a Rust boolean expression over `got` and `want`.
           For f64 use "(got - want).abs() < 1e-6".
    want_ty: an explicit type for `want`, needed when a bare literal such
           as `None` or `Some((12.5, -3.25))` cannot be inferred on its own.
    A panic inside the learner's function is caught and reported rather
    than taking every later objective down with it.
    """
    ty = f": {want_ty}" if want_ty else ""
    blocks = []
    for i, (args, want) in enumerate(cases):
        call = f"{fn}({', '.join(args)})"
        # Escape for embedding as a raw string literal in Rust.
        call_lit = 'r#"' + call.replace('"#', '"\\#') + '"#'
        blocks.append(f'''
    match std::panic::catch_unwind(|| {call}) {{
        Ok(got) => {{
            let want{ty} = {want};
            let ok = {check};
            __report({i}, ok, __short(format!("{{}} returned {{:?}}, wanted {{:?}}", {call_lit}, got, want)));
        }}
        Err(_) => __report({i}, false, format!("{{}} panicked", {call_lit})),
    }}''')
    return RS_PRELUDE + '''
fn main() {
    std::panic::set_hook(Box::new(|_| {}));
''' + "".join(blocks) + '''
}
'''


def rs_custom(body: str) -> str:
    """A hand-written Rust checker. Must define main()."""
    return RS_PRELUDE + body
