#!/usr/bin/env python3
"""Compile every `code:` snippet in docs/assets/lesson-quizzes.js.

The Rusty School's rule is that no example ships unless it has been
through the compiler. Quiz questions are examples too: a question whose
snippet does not compile teaches a beginner something false at exactly
the moment they are trying to check their understanding.

Snippets that are meant NOT to compile (the question is "why is this
rejected?") are listed in EXPECT_FAIL, and this script fails if one of
them starts compiling.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SRC = Path("docs/assets/lesson-quizzes.js")

# Snippets that must be REJECTED by the compiler, keyed by lesson id.
# The question in each case is about why Rust refuses.
EXPECT_FAIL = {
    "06-ownership": ["let s2 = s1;"],
    "10-collections": ["v.push(*n);"],
}


def snippets():
    """Yield (lesson_id, index, code) for every code field in the file."""
    text = SRC.read_text(encoding="utf-8")
    # Find each lesson block: "id": [ ... ]
    for lesson_match in re.finditer(r'"([\w-]+)":\s*\[', text):
        lesson = lesson_match.group(1)
        start = lesson_match.end()
        depth = 1
        i = start
        while i < len(text) and depth:
            if text[i] == "[":
                depth += 1
            elif text[i] == "]":
                depth -= 1
            i += 1
        block = text[start:i]
        for n, m in enumerate(re.finditer(r"code:\s*('(?:[^'\\]|\\.)*')", block), start=1):
            yield lesson, n, json.loads('"' + m.group(1)[1:-1].replace('"', '\\"') + '"')


def wrap(code: str) -> str:
    """Give the snippet a main() if it does not have one."""
    return code if "fn main(" in code else code + "\n\nfn main() {}\n"


def main() -> int:
    if not SRC.exists():
        print(f"missing {SRC}")
        return 1

    checked = failures = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        for lesson, n, code in snippets():
            checked += 1
            should_fail = any(
                marker in code for marker in EXPECT_FAIL.get(lesson, [])
            )
            src = tmpdir / f"{lesson}_{n}.rs"
            src.write_text(wrap(code), encoding="utf-8")
            proc = subprocess.run(
                ["rustc", "--edition", "2021", "--crate-type", "bin",
                 "-o", str(tmpdir / f"{lesson}_{n}.out"), str(src)],
                capture_output=True, text=True,
            )
            compiled = proc.returncode == 0

            if should_fail and compiled:
                failures += 1
                print(f"\n{lesson} snippet {n}: compiled, but the question says it "
                      f"should be REJECTED")
            elif not should_fail and not compiled:
                failures += 1
                first = [l for l in proc.stderr.splitlines() if l.startswith("error")]
                print(f"\n{lesson} snippet {n}: does not compile")
                for line in first[:3]:
                    print("   ", line)

    print(f"\n{checked} quiz snippets checked.")
    if failures:
        print(f"{failures} problem(s). Fix before shipping.")
        return 1
    print("Every quiz snippet compiles (or fails exactly as the question claims). 🦀")
    return 0


if __name__ == "__main__":
    sys.exit(main())
