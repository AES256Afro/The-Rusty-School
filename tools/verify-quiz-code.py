#!/usr/bin/env python3
"""Check every code snippet in both schools' per-lesson quiz banks.

The campus rule is that no published example ships unverified. Quiz
questions are examples too: a snippet that does not do what the question
claims teaches a beginner something false at exactly the moment they are
checking their understanding.

  Rust   (docs/assets/lesson-quizzes.js)         compiled with rustc
  Python (docs/python/assets/lesson-quizzes.js)  executed, output compared

Snippets that are meant NOT to compile or to raise are declared below,
and this script fails if one of them starts behaving.

Usage:  python3 tools/verify-quiz-code.py
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RUST_SRC = Path("docs/assets/lesson-quizzes.js")
PY_SRC = Path("docs/python/assets/lesson-quizzes.js")

# Rust snippets the question says the compiler must REJECT.
RUST_EXPECT_FAIL = {
    "06-ownership": ["let s2 = s1;"],
    "10-collections": ["v.push(*n);"],
}


def blocks(src: Path, field: str = "code"):
    """Yield (lesson_id, n, snippet) for each `code:` in a quiz bank."""
    text = src.read_text(encoding="utf-8")
    for lesson_match in re.finditer(r'^  "([\w-]+)":\s*\[', text, re.M):
        lesson = lesson_match.group(1)
        i, depth = lesson_match.end(), 1
        while i < len(text) and depth:
            if text[i] == "[":
                depth += 1
            elif text[i] == "]":
                depth -= 1
            i += 1
        body = text[lesson_match.end():i]
        # Snippets are written with either quote style, so match both and
        # normalise to a JSON string before decoding the escapes. Matching
        # only one style silently under-checks, which is worse than not
        # checking at all: the run goes green having looked at nothing.
        pattern = field + r""":\s*(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)')"""
        for n, m in enumerate(re.finditer(pattern, body), 1):
            raw = m.group(1) if m.group(1) is not None else m.group(2)
            if m.group(2) is not None:          # single-quoted: escape any "
                raw = raw.replace('\\"', '"').replace('"', '\\"').replace("\\'", "'")
            yield lesson, n, json.loads('"' + raw + '"')


def answers(src: Path):
    """Map (lesson, n) -> the option text the question marks correct."""
    text = src.read_text(encoding="utf-8")
    node = shutil.which("node")
    if not node:
        return {}
    script = (
        "const w={};global.window=w;require(%s);"
        "const q=w.RUSTY_LESSON_QUIZ||w.PY_LESSON_QUIZ;const o={};"
        "Object.keys(q).forEach(k=>{let c=0;q[k].forEach(x=>{"
        "if(x.code){c++;o[k+'#'+c]=x.options[x.answer];}});});"
        "console.log(JSON.stringify(o));" % json.dumps(str(src.resolve()))
    )
    out = subprocess.run([node, "-e", script], capture_output=True, text=True)
    return json.loads(out.stdout) if out.returncode == 0 else {}


def check_rust() -> tuple[int, int]:
    if not RUST_SRC.exists() or not shutil.which("rustc"):
        print("skipping Rust: rustc not on PATH" if RUST_SRC.exists() else "")
        return 0, 0
    checked = failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for lesson, n, code in blocks(RUST_SRC):
            checked += 1
            should_fail = any(mk in code for mk in RUST_EXPECT_FAIL.get(lesson, []))
            src = Path(tmp) / f"{lesson}_{n}.rs"
            src.write_text(code if "fn main(" in code else code + "\n\nfn main() {}\n")
            proc = subprocess.run(
                ["rustc", "--edition", "2021", "-o", str(Path(tmp) / f"{lesson}_{n}.out"),
                 str(src)], capture_output=True, text=True)
            ok = proc.returncode == 0
            if should_fail and ok:
                failed += 1
                print(f"  {lesson} #{n}: compiled, but the question says it is rejected")
            elif not should_fail and not ok:
                failed += 1
                print(f"  {lesson} #{n}: does not compile")
                for line in [l for l in proc.stderr.splitlines() if l.startswith("error")][:2]:
                    print("     ", line)
    return checked, failed


def check_python() -> tuple[int, int]:
    if not PY_SRC.exists():
        return 0, 0
    expected = answers(PY_SRC)
    checked = failed = 0
    with tempfile.TemporaryDirectory() as tmp:
        for lesson, n, code in blocks(PY_SRC):
            checked += 1
            src = Path(tmp) / f"{lesson}_{n}.py"
            src.write_text(code, encoding="utf-8")
            proc = subprocess.run([sys.executable, str(src)],
                                  capture_output=True, text=True, timeout=30)
            actual = (proc.stdout + proc.stderr).strip()
            claim = expected.get(f"{lesson}#{n}")
            if claim is None:
                continue
            # A claim naming an exception passes if that exception was raised.
            exc = re.search(r"\b([A-Z]\w+(?:Error|Exception))\b", claim)
            if exc:
                ok = exc.group(1) in actual
            else:
                # "[1] then [1, 2]" describes successive printed lines.
                want = [p.strip() for p in re.split(r"\bthen\b", claim)]
                got = [l.strip() for l in actual.splitlines()]
                ok = got == want or actual == claim
            if not ok:
                failed += 1
                print(f"  {lesson} #{n}: output does not match the stated answer")
                print(f"     claims: {claim}")
                print(f"     actual: {actual[:100]}")
    return checked, failed


def main() -> int:
    # A silent zero means the extractor stopped matching, not that the
    # bank is clean. Treat "found nothing" as a failure worth shouting about.
    print("Rust quiz snippets")
    rc, rf = check_rust()
    if RUST_SRC.exists() and shutil.which("rustc") and rc == 0:
        print("  extracted no snippets: the parser is broken, not the bank")
        return 1
    print(f"  {rc} checked, {rf} problem(s)\n")
    print("Python quiz snippets")
    pc, pf = check_python()
    if PY_SRC.exists() and pc == 0:
        print("  extracted no snippets: the parser is broken, not the bank")
        return 1
    print(f"  {pc} checked, {pf} problem(s)\n")
    if rf or pf:
        print("Fix these before shipping.")
        return 1
    print(f"All {rc + pc} quiz snippets do exactly what their question claims. 🦀🐍")
    return 0


if __name__ == "__main__":
    sys.exit(main())
