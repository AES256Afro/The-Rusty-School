#!/usr/bin/env python3
"""Build the campus search index.

Both schools are static HTML, so the honest way to index them is to read
what actually shipped rather than to re-derive it from source. This walks
docs/**/*.html, pulls out the title, the description, every heading and a
chunk of body text, and writes one JSON file that the search overlay
fetches the first time somebody opens it.

    python3 tools/build-search-index.py            # write the index
    python3 tools/build-search-index.py --list     # show what it found

Run it after tools/pybuild.py, and after editing any hand-written Rust
page. It is deliberately dependency-free: html.parser is in the standard
library, and by Level 3 of the Python course you can read every line.
"""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUT = DOCS / "assets" / "search-index.json"

# Pages that are furniture rather than teaching material. No point
# sending somebody searching for "ownership" to the privacy policy.
SKIP = {"404.html", "privacy.html", "account.html", "python/account.html"}

# How much body text to keep per page. Enough that a phrase from the
# middle of a lesson still finds it, small enough that the whole index
# stays a lazy one-time download rather than a page-weight problem.
BODY_CHARS = 1400


class PageReader(HTMLParser):
    """Pull the title, description, headings and readable text out of a page."""

    SKIP_TAGS = {"script", "style", "nav", "header", "footer", "template"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.description = ""
        self.badge = ""
        self.headings: list[str] = []
        self.text: list[str] = []
        self._skip_depth = 0
        self._in_title = False
        self._heading: str | None = None
        self._badge: str | None = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
        elif tag == "title":
            self._in_title = True
        elif tag == "meta" and a.get("name") == "description":
            self.description = a.get("content", "")
        elif tag in ("h1", "h2", "h3"):
            self._heading = ""
        elif (tag == "span" and self._badge is None and not self.badge
                and "badge" in a.get("class", "").split()):
            # The level chip a lesson already prints ("Level 2 · The Toolbox").
            self._badge = ""

    def handle_endtag(self, tag):
        if tag in self.SKIP_TAGS:
            self._skip_depth = max(0, self._skip_depth - 1)
        elif tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3") and self._heading is not None:
            h = " ".join(self._heading.split())
            if h:
                self.headings.append(h)
            self._heading = None
        elif tag == "span" and self._badge is not None:
            self.badge = " ".join(self._badge.split())
            self._badge = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
            return
        if self._skip_depth:
            return
        if self._badge is not None:
            self._badge += data
        if self._heading is not None:
            self._heading += data
        self.text.append(data)


def clean(text: str) -> str:
    return " ".join(text.split())


def canonical_url(path: Path) -> str:
    """Match the pretty URLs Cloudflare Pages serves."""
    rel = path.relative_to(DOCS).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[: -len(".html")]


def classify(rel: str) -> tuple[str, str]:
    """Return (school, kind) for a page, for filter chips and icons."""
    # The Bridge is campus-level rather than part of either school, so it
    # gets its own filter chip instead of being mislabelled as Rust.
    if rel.startswith("bridge/"):
        return "bridge", "page" if rel == "bridge/index.html" else "mission"
    school = "python" if rel.startswith("python/") else "rust"
    tail = rel[len("python/"):] if school == "python" else rel
    if tail.startswith("learn/") and not tail.endswith("learn/index.html"):
        kind = "lesson"
    elif tail.startswith("build/") and not tail.endswith("build/index.html"):
        kind = "project"
    elif tail in ("dojo.html", "pit.html"):
        kind = "puzzles"
    else:
        kind = "page"
    return school, kind


def read_page(path: Path) -> dict | None:
    html = path.read_text(encoding="utf-8", errors="replace")
    reader = PageReader()
    reader.feed(html)

    title = clean(reader.title)
    # "Lesson 7: Borrowing - The Rusty School" reads better as just the
    # lesson name; the school is shown as a chip beside the result.
    title = re.sub(r"\s*-\s*The (Rusty|Python) School\s*$", "", title)
    title = re.sub(r"\s*-\s*The Bridge\s*$", "", title)
    if not title:
        return None

    rel = path.relative_to(DOCS).as_posix()
    school, kind = classify(rel)
    body = clean(" ".join(reader.text))
    # every page opens with the accessibility skip link; it is not content
    body = re.sub(r"^Skip to content\s*", "", body)

    return {
        "u": canonical_url(path),
        "t": title,
        "s": school,
        "k": kind,
        "l": reader.badge[:40],
        "d": clean(reader.description)[:180],
        "h": reader.headings[:24],
        "b": body[:BODY_CHARS],
    }


def build() -> list[dict]:
    pages = []
    for path in sorted(DOCS.rglob("*.html")):
        rel = path.relative_to(DOCS).as_posix()
        if rel in SKIP:
            continue
        entry = read_page(path)
        if entry:
            pages.append(entry)
    # Lessons first, then projects, then everything else: a tie in score
    # should fall towards teaching material.
    order = {"lesson": 0, "project": 1, "puzzles": 2, "page": 3}
    pages.sort(key=lambda p: (order.get(p["k"], 9), p["u"]))
    return pages


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the campus search index")
    ap.add_argument("--list", action="store_true", help="show what was found, write nothing")
    args = ap.parse_args()

    pages = build()
    blob = json.dumps(pages, separators=(",", ":"), ensure_ascii=False)

    if args.list:
        for p in pages:
            print(f"  {p['s']:7} {p['k']:8} {p['u']:44} {p['t'][:46]}")
        print(f"\n{len(pages)} pages, index would be {len(blob):,} bytes")
        return 0

    OUT.write_text(blob, encoding="utf-8")
    counts: dict[str, int] = {}
    for p in pages:
        counts[p["s"] + "/" + p["k"]] = counts.get(p["s"] + "/" + p["k"], 0) + 1
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(blob):,} bytes, {len(pages)} pages)")
    for key in sorted(counts):
        print(f"  {key:18} {counts[key]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
