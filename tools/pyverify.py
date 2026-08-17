#!/usr/bin/env python3
"""Prove every code example in The Python School.

The Rusty School's house rule is that no Rust example is published until
it has been compiled and run. This is that rule, automated, for Python.

For every code block in the generated pages:

  data-verify="run"      execute it. If the lesson printed an expected
                         output underneath, the real output must match it
                         exactly. If it did not, the program must at
                         least finish without raising.
  data-verify="compile"  parse it, so typos and syntax errors cannot ship,
                         but do not execute (it may need the network, a
                         file, or a package we do not want to install).
  data-verify="skip"     deliberately broken code, shown to teach a lesson.

    python3 tools/pyverify.py                  # check everything
    python3 tools/pyverify.py learn/01-hello   # check matching pages only
    python3 tools/pyverify.py -v               # show every block

Exit status is non-zero if anything failed, so this can gate a commit.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "docs" / "python"
TIMEOUT = 30

BLOCK_RE = re.compile(
    r'<pre(?P<attrs>[^>]*?)data-verify="(?P<mode>run|compile|skip)"(?P<rest>[^>]*)>'
    r"<code[^>]*>(?P<code>.*?)</code></pre>"
    r'(?P<tail>\s*<pre class="out"><code class="nohl">(?P<expect>.*?)</code></pre>)?',
    re.DOTALL,
)
STDIN_RE = re.compile(r'data-stdin="([^"]*)"')


class Failure(Exception):
    pass


def find_python() -> str:
    """Prefer a modern interpreter; the course targets 3.11+."""
    candidates = [
        os.environ.get("PYTHON_SCHOOL_PYTHON"),
        str(Path.home() / ".local/share/uv/python/cpython-3.13-macos-aarch64-none/bin/python3.13"),
        "python3.14", "python3.13", "python3.12", "python3.11", "python3",
    ]
    for cand in candidates:
        if not cand:
            continue
        try:
            res = subprocess.run(
                [cand, "-c", "import sys; print(sys.version_info.major, sys.version_info.minor)"],
                capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            continue
        if res.returncode == 0:
            major, minor = (int(n) for n in res.stdout.split())
            if (major, minor) >= (3, 11):
                return cand
    raise SystemExit("No Python 3.11+ found. Set PYTHON_SCHOOL_PYTHON to one.")


# When a human runs a program in a terminal, the characters they type are
# echoed back by the terminal itself, so the transcript in a lesson shows
# "Name: Guybrush" on one line. Piped stdin is not echoed, and the school's
# in-browser runner echoes deliberately so the output looks like a terminal.
# This preamble makes the verifier agree with both of them.
ECHO_INPUT = '''\
import builtins as _b, sys as _s
_real = _b.input


def _echoing_input(prompt=""):
    _s.stdout.write(str(prompt))
    line = _real()
    _s.stdout.write(line + "\\n")
    return line


_b.input = _echoing_input
'''


def run_snippet(python: str, src: str, stdin: str, workdir: Path) -> tuple[int, str]:
    """Run one snippet in a scratch directory and return (code, merged output)."""
    script = workdir / "snippet.py"
    script.write_text(src, encoding="utf-8")
    # sitecustomize is imported automatically at startup, which keeps the
    # snippet file itself pristine so traceback line numbers stay honest
    (workdir / "sitecustomize.py").write_text(ECHO_INPUT, encoding="utf-8")
    env = dict(os.environ, PYTHONPATH=str(workdir))
    # -u and merging stderr into stdout keep the two streams interleaved in
    # the order they were actually written, which is what the reader sees in
    # a terminal and what the in-browser runner produces. Capturing them
    # separately and concatenating would reorder a lesson that deliberately
    # prints to both.
    proc = subprocess.run(
        [python, "-u", str(script)],
        input=stdin,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=TIMEOUT,
        cwd=workdir,
        env=env,
    )
    return proc.returncode, proc.stdout


def normalise(text: str) -> str:
    return "\n".join(line.rstrip() for line in text.strip().splitlines())


def check_page(python: str, path: Path, verbose: bool) -> tuple[int, int, list[str]]:
    source = path.read_text(encoding="utf-8")
    checked = skipped = 0
    problems: list[str] = []

    for i, match in enumerate(BLOCK_RE.finditer(source), start=1):
        mode = match.group("mode")
        code = html.unescape(match.group("code"))
        expect = match.group("expect")
        expect = html.unescape(expect) if expect is not None else None
        attrs = match.group("attrs") + match.group("rest")
        stdin_match = STDIN_RE.search(attrs)
        stdin = html.unescape(stdin_match.group(1)) if stdin_match else ""
        if stdin and not stdin.endswith("\n"):
            stdin += "\n"

        label = f"{path.relative_to(PAGES)} block {i}"

        if mode == "skip":
            skipped += 1
            continue

        if mode == "compile":
            try:
                compile(code, "<lesson>", "exec")
                checked += 1
            except SyntaxError as err:
                problems.append(f"{label}: syntax error on line {err.lineno}: {err.msg}\n"
                                f"    {(err.text or '').strip()}")
            continue

        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            try:
                status, output = run_snippet(python, code, stdin, work)
            except subprocess.TimeoutExpired:
                problems.append(f"{label}: still running after {TIMEOUT}s (infinite loop?)")
                continue

        if status != 0:
            problems.append(f"{label}: exited {status}\n"
                            + "\n".join("    " + l for l in output.strip().splitlines()[-8:]))
            continue

        checked += 1
        if expect is not None:
            got, want = normalise(output), normalise(expect)
            if got != want:
                problems.append(
                    f"{label}: output does not match what the lesson promises\n"
                    f"  --- lesson says ---\n"
                    + "\n".join("  | " + l for l in want.splitlines())
                    + f"\n  --- python says ---\n"
                    + "\n".join("  | " + l for l in got.splitlines())
                )
            elif verbose:
                print(f"  ok  {label} ({len(want.splitlines())} lines of output matched)")
        elif verbose:
            print(f"  ok  {label} (ran cleanly)")

    return checked, skipped, problems


def check_pit(python: str) -> list[str]:
    """Run every Snake Pit puzzle and prove its promised output.

    predict puzzles run their own code; fix/bug puzzles run the solution.
    The broken code shown for fix/bug puzzles is never executed.
    """
    import importlib

    sys.path.insert(0, str(ROOT / "tools"))
    try:
        pit_data = importlib.import_module("pycourse.pit_data")
    except ModuleNotFoundError:
        return []

    puzzles = pit_data.PUZZLES
    problems: list[str] = []
    seen_ids: set[str] = set()

    for puzzle in puzzles:
        pid = puzzle["id"]
        if pid in seen_ids:
            problems.append(f"pit puzzle {pid}: duplicate id")
        seen_ids.add(pid)

        code = puzzle["code"] if puzzle["type"] == "predict" else puzzle.get("solution")
        if code is None:
            problems.append(f"pit puzzle {pid}: {puzzle['type']} needs a solution")
            continue

        with tempfile.TemporaryDirectory() as tmp:
            work = Path(tmp)
            try:
                status, output = run_snippet(python, code, "", work)
            except subprocess.TimeoutExpired:
                problems.append(f"pit puzzle {pid}: still running after {TIMEOUT}s")
                continue

        if status != 0:
            problems.append(f"pit puzzle {pid}: exited {status}\n"
                            + "\n".join("    " + l for l in output.strip().splitlines()[-6:]))
            continue

        got, want = normalise(output), normalise(puzzle["expected"])
        if got != want:
            problems.append(
                f"pit puzzle {pid}: output does not match its 'it prints' claim\n"
                f"  --- claims ---\n"
                + "\n".join("  | " + l for l in want.splitlines())
                + "\n  --- python says ---\n"
                + "\n".join("  | " + l for l in got.splitlines())
            )

    print(f"{len(puzzles)} Snake Pit puzzles verified.")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify The Python School's code examples")
    parser.add_argument("filter", nargs="?", default="", help="only pages whose path contains this")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args()

    if not PAGES.exists():
        raise SystemExit("docs/python does not exist yet. Run tools/pybuild.py first.")

    python = find_python()
    version = subprocess.run([python, "--version"], capture_output=True, text=True).stdout.strip()
    print(f"Verifying with {version} ({python})")

    if not args.filter:
        pit_problems = check_pit(python)
    else:
        pit_problems = []

    pages = sorted(p for p in PAGES.rglob("*.html") if args.filter in str(p))
    total_checked = total_skipped = 0
    all_problems: list[str] = []

    for path in pages:
        checked, skipped, problems = check_page(python, path, args.verbose)
        total_checked += checked
        total_skipped += skipped
        all_problems.extend(problems)

    all_problems.extend(pit_problems)

    print(f"\n{total_checked} blocks verified, {total_skipped} deliberately skipped, "
          f"across {len(pages)} pages.")

    if all_problems:
        print(f"\n{len(all_problems)} PROBLEM(S):\n")
        for p in all_problems:
            print(p + "\n")
        return 1

    print("Every published example does what the lesson says it does. 🐍")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
