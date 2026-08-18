#!/usr/bin/env python3
"""Build The Bridge into docs/bridge/.

Usage:  python3 tools/bridgebuild.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from bridge import build_all

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def main() -> int:
    pages = build_all()
    for rel, html in pages:
        target = DOCS / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        print(f"  wrote docs/{rel} ({len(html):,} bytes)")
    print(f"Done: {len(pages)} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
