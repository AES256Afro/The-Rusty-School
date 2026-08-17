#!/usr/bin/env python3
"""Build The Python School.

The Rusty School is *served* by a program written in Rust. The Python
School is *built* by a program written in Python: this one. It is
deliberately plain, dependency-free, standard-library-only code, because
by Level 3 of the course you will be able to read every line of it, and
in the workshop you are asked to write your own version of it.

    python3 tools/pybuild.py            # build the whole school
    python3 tools/pybuild.py --list     # show what would be written

Everything lands in docs/python/. Nothing outside that folder is touched.
Then run tools/pyverify.py, which executes every runnable example in the
built pages and checks the printed output against what we promised.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "python"


def write(path: str, content: str, *, listing: bool = False) -> None:
    target = OUT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    verb = "would write" if listing else "wrote"
    if not listing:
        target.write_text(content, encoding="utf-8")
    print(f"  {verb} {target.relative_to(ROOT)} ({len(content):,} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build The Python School")
    parser.add_argument("--list", action="store_true", help="show output without writing")
    args = parser.parse_args()

    sys.path.insert(0, str(ROOT / "tools"))
    from pycourse import build_all

    print(f"Building The Python School into {OUT.relative_to(ROOT)}/")
    pages = build_all()
    for path, content in pages:
        write(path, content, listing=args.list)
    print(f"Done: {len(pages)} pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
