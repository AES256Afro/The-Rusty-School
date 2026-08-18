#!/usr/bin/env python3
"""Verify every mission on The Bridge.

Two checks per mission per language, and the second one matters as much
as the first:

  1. reference + checker  ->  every objective must PASS.
     A mission whose own answer fails is broken.

  2. stub + checker       ->  at least one objective must FAIL.
     A checker that passes the untouched starter code is not testing
     anything, and would hand out a commendation for writing nothing.
     This is the check that catches a checker wired up wrong.

Python runs locally; Rust compiles with rustc. Neither needs the network,
so this can gate a commit.

Usage:  python3 tools/verify-bridge.py
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bridge.mission_data import MISSIONS

WIRE = re.compile(r"^BRIDGE\|(\d+)\|(PASS|FAIL)\|(.*)$")


def parse(output: str, count: int):
    """Return a list of True/False/None, one per objective."""
    results = [None] * count
    for line in output.splitlines():
        m = WIRE.match(line.strip())
        if not m:
            continue
        idx = int(m.group(1))
        if 0 <= idx < count:
            results[idx] = m.group(2) == "PASS"
    return results


def run_python(code: str) -> str:
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(code)
        path = f.name
    try:
        p = subprocess.run([sys.executable, path], capture_output=True, text=True, timeout=60)
        return p.stdout + p.stderr
    finally:
        Path(path).unlink(missing_ok=True)


def run_rust(code: str) -> str:
    if not shutil.which("rustc"):
        return "__NO_RUSTC__"
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "mission.rs"
        out = Path(tmp) / "mission"
        src.write_text(code, encoding="utf-8")
        c = subprocess.run(
            ["rustc", "--edition", "2021", "-o", str(out), str(src)],
            capture_output=True, text=True,
        )
        if c.returncode != 0:
            return "__COMPILE_FAIL__\n" + c.stderr
        p = subprocess.run([str(out)], capture_output=True, text=True, timeout=60)
        return p.stdout + p.stderr


RUNNERS = {"py": run_python, "rs": run_rust}
NAMES = {"py": "Python", "rs": "Rust"}


def main() -> int:
    problems = 0
    checked = 0
    skipped_rust = False

    for m in MISSIONS:
        n = len(m["objectives"])
        for lang in ("py", "rs"):
            label = f"{m['id']} [{NAMES[lang]}]"
            checker = m[lang + "_checker"]

            # 1. the reference must pass everything
            out = RUNNERS[lang](m[lang + "_reference"] + "\n" + checker)
            if out == "__NO_RUSTC__":
                skipped_rust = True
                continue
            checked += 1
            if out.startswith("__COMPILE_FAIL__"):
                problems += 1
                print(f"\n{label}: the REFERENCE does not compile")
                for line in out.splitlines()[1:4]:
                    print("   ", line)
                continue
            res = parse(out, n)
            if not all(r is True for r in res):
                problems += 1
                print(f"\n{label}: the REFERENCE does not pass its own objectives")
                for i, r in enumerate(res):
                    if r is not True:
                        state = "no result" if r is None else "FAILED"
                        print(f"    objective {i + 1} {state}: {m['objectives'][i]}")

            # 2. the stub must NOT pass everything
            out = RUNNERS[lang](m[lang + "_stub"] + "\n" + checker)
            checked += 1
            if out.startswith("__COMPILE_FAIL__"):
                # A stub that does not compile is a legitimate starting state.
                continue
            res = parse(out, n)
            if all(r is True for r in res):
                problems += 1
                print(f"\n{label}: the STUB passes every objective")
                print("    The checker is not testing anything. A learner would be")
                print("    commended for changing nothing.")

    print(f"\n{len(MISSIONS)} mission(s), {checked} runs.")
    if skipped_rust:
        print("Rust was skipped: rustc is not on PATH.")
    if problems:
        print(f"{problems} problem(s). Fix before shipping.")
        return 1
    print("Every reference passes its objectives, and every stub fails at least one. 🖖")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
