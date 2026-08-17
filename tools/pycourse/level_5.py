"""Level 5: In the Wild.

Twelve lessons on what people actually build with Python: automation,
the web, databases, data, charts, games, desktop apps, packaging,
performance and security.

Many examples here need packages or a network, so they carry no run
button. Every one of them is still parsed by the verifier, so the code
you read is at least syntactically real.
"""

from __future__ import annotations

from .kit import callout, code, exercise, link, out, repl, table, tb, term, voice

LESSONS = []


def _add(**kw):
    LESSONS.append(kw)


# ---------------------------------------------------------------- 41
_add(
    level=5,
    num="41",
    slug="41-automation",
    id="py-41-automation",
    card="Rename 4,000 files, tidy a folder, back things up, and schedule it all to run itself.",
    title="Automating the Boring Things",
    emoji="🤖",
    desc="Bulk file operations, organising folders, backups, and scheduling scripts with cron or Task Scheduler.",
    lede="""This is the lesson that pays for the course. Everybody has a folder that is a
    disaster. Today you fix it in forty lines and get the afternoon back.""",
    body=f"""
    <h2>The golden rule of automation</h2>
    {callout("danger", "🛑 Dry run first. Always. No exceptions.",
             "<p>A script that renames files is a script that can destroy files. Every tool in "
             "this lesson prints what it <em>would</em> do before it does anything, and takes "
             "an explicit flag to act for real. This is not caution for beginners; it is how "
             "professionals write destructive tools, and it will save you at least once.</p>")}

    <h2>Bulk renaming</h2>
    {code('''from pathlib import Path


def bulk_rename(folder, old_text, new_text, dry_run=True):
    """Replace old_text with new_text in every filename. Previews by default."""
    changes = []
    for path in sorted(Path(folder).iterdir()):
        if not path.is_file() or old_text not in path.name:
            continue
        target = path.with_name(path.name.replace(old_text, new_text))
        changes.append((path, target))

    for source, target in changes:
        if dry_run:
            print(f"WOULD RENAME  {source.name}  ->  {target.name}")
        else:
            source.rename(target)
            print(f"renamed  {source.name}  ->  {target.name}")

    return len(changes)


# build a mess to clean up
holiday = Path("holiday")
holiday.mkdir(exist_ok=True)
for n in (1, 2, 3):
    (holiday / f"IMG_20260817_{n:04d}.jpg").write_text("x", encoding="utf-8")

print(f"{bulk_rename('holiday', 'IMG_', 'melee-island-')} files would change")
print("---")
bulk_rename("holiday", "IMG_", "melee-island-", dry_run=False)''',
          expect="""WOULD RENAME  IMG_20260817_0001.jpg  ->  melee-island-20260817_0001.jpg
WOULD RENAME  IMG_20260817_0002.jpg  ->  melee-island-20260817_0002.jpg
WOULD RENAME  IMG_20260817_0003.jpg  ->  melee-island-20260817_0003.jpg
3 files would change
---
renamed  IMG_20260817_0001.jpg  ->  melee-island-20260817_0001.jpg
renamed  IMG_20260817_0002.jpg  ->  melee-island-20260817_0002.jpg
renamed  IMG_20260817_0003.jpg  ->  melee-island-20260817_0003.jpg""")}

    <h2>Sorting a downloads folder</h2>
    {code('''from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "Documents": {".pdf", ".docx", ".txt", ".md"},
    "Data": {".csv", ".json", ".xlsx"},
    "Archives": {".zip", ".tar", ".gz"},
}


def category_for(path):
    """Which folder should this file live in?"""
    for name, extensions in CATEGORIES.items():
        if path.suffix.lower() in extensions:
            return name
    return "Other"


def organise(folder, dry_run=True):
    """Move every file into a subfolder by type."""
    root = Path(folder)
    moved = {}
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue
        target_dir = root / category_for(path)
        moved.setdefault(target_dir.name, []).append(path.name)
        if not dry_run:
            target_dir.mkdir(exist_ok=True)
            path.rename(target_dir / path.name)
    return moved


downloads = Path("downloads")
downloads.mkdir(exist_ok=True)
for name in ["map.png", "contract.pdf", "sales.csv", "grog.mp3", "photo.jpg"]:
    (downloads / name).write_text("x", encoding="utf-8")

for category, files in sorted(organise("downloads").items()):
    print(f"{category:11} {', '.join(files)}")''',
          expect="""Data        sales.csv
Documents   contract.pdf
Images      map.png, photo.jpg
Other       grog.mp3""")}

    {voice("PERCEPTION", "Medium: Success",
           "Two things in that output are decisions rather than accidents. Archives does not "
           "appear at all, because no file matched it and the dictionary only gains a key when "
           "something lands in it. And grog.mp3 went to Other rather than being skipped.",
           "A catch-all is safer than silence here: a file that matches nothing still gets "
           "moved somewhere you can find it, instead of quietly staying put while the report "
           "implies the folder was tidied.")}

    <p>
      The same thing without the helper function, using a Python oddity that fits this shape
      exactly:
    </p>
    {code('''from pathlib import Path

CATEGORIES = {"Images": {".png", ".jpg"}, "Data": {".csv"}}


def organise(folder):
    root = Path(folder)
    moved = {}
    for path in sorted(root.iterdir()):
        if not path.is_file():
            continue
        for name, extensions in CATEGORIES.items():
            if path.suffix.lower() in extensions:
                moved.setdefault(name, []).append(path.name)
                break
        else:
            moved.setdefault("Other", []).append(path.name)
    return moved


d = Path("dl2")
d.mkdir(exist_ok=True)
for name in ["map.png", "sales.csv", "grog.mp3"]:
    (d / name).write_text("x", encoding="utf-8")

for category, files in sorted(organise("dl2").items()):
    print(f"{category:9} {files}")''',
          expect="""Data      ['sales.csv']
Images    ['map.png']
Other     ['grog.mp3']""")}
    <p>
      That <code>for ... else</code> is a genuine Python oddity: the <code>else</code> runs
      only if the loop finished without hitting <code>break</code>, which is exactly "no
      category matched".
    </p>

    <h2>Finding duplicates by content</h2>
    {code('''import hashlib
from pathlib import Path


def file_hash(path, chunk_size=8192):
    """SHA-256 of a file, read in chunks so size does not matter."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(chunk_size):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(folder):
    """Group files by content hash. Same content, different names."""
    by_hash = {}
    for path in sorted(Path(folder).rglob("*")):
        if path.is_file():
            by_hash.setdefault(file_hash(path), []).append(path.name)
    return {h: names for h, names in by_hash.items() if len(names) > 1}


dupes = Path("dupes")
dupes.mkdir(exist_ok=True)
(dupes / "map.txt").write_text("x marks the spot", encoding="utf-8")
(dupes / "map-copy.txt").write_text("x marks the spot", encoding="utf-8")
(dupes / "other.txt").write_text("something else", encoding="utf-8")

for digest, names in find_duplicates("dupes").items():
    print(f"{digest[:12]}...  {names}")''',
          expect="""421822047831...  ['map-copy.txt', 'map.txt']""")}
    <p>
      Comparing content rather than names is the right way to find duplicates: identical photos
      with different filenames are still duplicates. <code>while chunk := f.read(...)</code>
      uses the walrus operator to assign and test in one go, so the file is read in pieces and
      a 40GB video does not need 40GB of memory.
    </p>

    <h2>Backups</h2>
    {code('''import shutil
from pathlib import Path


def backup(source, destination, stamp):
    """Zip a folder into a timestamped archive. Returns the archive path."""
    Path(destination).mkdir(parents=True, exist_ok=True)
    base = Path(destination) / f"{Path(source).name}-{stamp}"
    return shutil.make_archive(str(base), "zip", source)


work = Path("ship-logs")
work.mkdir(exist_ok=True)
(work / "day1.txt").write_text("became a mighty pirate\\n", encoding="utf-8")
(work / "day2.txt").write_text("lost the ship\\n", encoding="utf-8")

archive = backup("ship-logs", "backups", "20260817")
print(Path(archive).name)
print(Path(archive).exists())''',
          expect="""ship-logs-20260817.zip
True""")}
    <p>
      In real use the stamp would be <code>datetime.now().strftime("%Y%m%d-%H%M")</code>. It is
      passed in here so the example produces the same output every time, which is the same
      testability idea from Lesson 29: functions that take the clock as an argument can be
      tested, functions that call it cannot.
    </p>

    <h2>Making it run by itself</h2>
    {table(
        ["System", "Tool", "Example"],
        [["macOS / Linux", "cron", "<code>crontab -e</code>"],
         ["macOS", "launchd", "for anything that must survive sleep"],
         ["Windows", "Task Scheduler", "the graphical wizard"],
         ["Anywhere", "GitHub Actions", "if it does not need your machine"]],
    )}
    {term("""# crontab -e, then a line like this
# minute hour day month weekday  command

0 3 * * *   /home/you/tools/.venv/bin/python /home/you/tools/backup.py
*/15 * * * * /home/you/tools/.venv/bin/python /home/you/tools/check.py

# every day at 3am, and every 15 minutes""")}
    {callout("warn", "🪤 The three things that always break scheduled scripts",
             "<p><strong>1. Paths.</strong> cron runs from your home directory, not your "
             "project. Use absolute paths everywhere, or set the working directory in the "
             "script.</p>"
             "<p><strong>2. The wrong Python.</strong> cron has a minimal PATH. Give the full "
             "path to your virtual environment's interpreter, as above.</p>"
             "<p><strong>3. Silence.</strong> Output vanishes. Log to a file "
             "(Lesson 28) or you will never know it has been failing for six weeks.</p>")}

    <h2>A complete, defensive tool</h2>
    {code('''#!/usr/bin/env python3
"""tidy: organise a folder by file type."""

import argparse
import logging
import sys
from pathlib import Path

CATEGORIES = {
    "Images": {".jpg", ".jpeg", ".png", ".gif"},
    "Documents": {".pdf", ".docx", ".txt", ".md"},
    "Data": {".csv", ".json", ".xlsx"},
}

log = logging.getLogger("tidy")


def category_for(path: Path) -> str:
    for name, extensions in CATEGORIES.items():
        if path.suffix.lower() in extensions:
            return name
    return "Other"


def tidy(folder: Path, dry_run: bool = True) -> int:
    moved = 0
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.name.startswith("."):
            continue
        target = folder / category_for(path) / path.name
        if target.exists():
            log.warning("skipping %s: %s already exists", path.name, target)
            continue
        if dry_run:
            log.info("would move %s -> %s", path.name, target.parent.name)
        else:
            target.parent.mkdir(exist_ok=True)
            path.rename(target)
            log.info("moved %s -> %s", path.name, target.parent.name)
        moved += 1
    return moved


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Organise a folder by file type.")
    parser.add_argument("folder", type=Path)
    parser.add_argument("--go", action="store_true", help="actually move files")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)-8s %(message)s",
    )

    if not args.folder.is_dir():
        log.error("not a folder: %s", args.folder)
        return 1

    count = tidy(args.folder, dry_run=not args.go)
    if not args.go:
        log.info("dry run: %d files would move. Pass --go to do it.", count)
    return 0


if __name__ == "__main__":
    sys.exit(main())''',
          run=False, verify="compile")}
    <p>
      Note every defensive choice: it previews unless told otherwise, it refuses to overwrite,
      it skips hidden files, it validates the folder before starting, it logs rather than
      prints, and it returns a proper exit code. That is the difference between a script and a
      tool you trust with your own files.
    </p>

    {exercise(1, "Extension report",
              "<p>Walk a folder tree and report how many files of each extension there are, and "
              "how much space each type uses, biggest first.</p>",
              code('''from pathlib import Path
from collections import Counter

root = Path("project")
(root / "src").mkdir(parents=True, exist_ok=True)
(root / "docs").mkdir(exist_ok=True)
for name, size in [("src/main.py", 400), ("src/utils.py", 250),
                   ("docs/readme.md", 120), ("notes.txt", 60)]:
    (root / name).write_text("x" * size, encoding="utf-8")

counts = Counter()
sizes = Counter()

for path in root.rglob("*"):
    if path.is_file():
        counts[path.suffix] += 1
        sizes[path.suffix] += path.stat().st_size

for suffix, total in sizes.most_common():
    print(f"{suffix:6} {counts[suffix]:3} files  {total:6,} bytes")''',
                   expect=""".py      2 files     650 bytes
.md      1 files     120 bytes
.txt     1 files      60 bytes"""))}

    {exercise(2, "Safe cleanup with a preview",
              "<p>Write a function that deletes files over a certain age. It must preview by "
              "default and refuse to touch anything outside the folder it was given.</p>",
              code('''from pathlib import Path


def clean_old(folder, keep_names, dry_run=True):
    """Delete files not in keep_names. Previews unless dry_run is False."""
    root = Path(folder).resolve()
    removed = []

    for path in sorted(root.iterdir()):
        if not path.is_file() or path.name in keep_names:
            continue
        # refuse anything that escaped the folder, for example via a symlink
        if root not in path.resolve().parents:
            print(f"REFUSING {path}: outside {root.name}")
            continue
        removed.append(path.name)
        if dry_run:
            print(f"WOULD DELETE {path.name}")
        else:
            path.unlink()
            print(f"deleted {path.name}")

    return removed


tmp = Path("cache")
tmp.mkdir(exist_ok=True)
for name in ["keep.txt", "old1.tmp", "old2.tmp"]:
    (tmp / name).write_text("x", encoding="utf-8")

print(f"{len(clean_old('cache', {'keep.txt'}))} files would go")
print("---")
clean_old("cache", {"keep.txt"}, dry_run=False)
print(sorted(p.name for p in Path("cache").iterdir()))''',
                   expect="""WOULD DELETE old1.tmp
WOULD DELETE old2.tmp
2 files would go
---
deleted old1.tmp
deleted old2.tmp
['keep.txt']""")
              + "<p>The <code>resolve()</code> check matters: a symlink inside the folder can "
              "point anywhere on your disk, and a delete script that follows one is a very bad "
              "afternoon. Refusing to act outside a known root is standard practice for "
              "anything destructive.</p>")}

    {exercise(3, "Design before you code",
              "<p>You want a script that watches a folder and converts any new CSV into JSON. "
              "List everything that could go wrong before writing a line.</p>",
              "<ul>"
              "<li>The file is still being written when you see it. Wait until the size stops "
              "changing, or watch for a rename.</li>"
              "<li>The CSV is malformed, or has a different set of columns than expected.</li>"
              "<li>The output already exists. Overwrite, skip, or version it?</li>"
              "<li>The file is enormous and does not fit in memory. Stream it.</li>"
              "<li>Two copies of the script run at once and fight over the same file.</li>"
              "<li>The script crashes halfway and leaves a truncated JSON file. Write to a "
              "temporary name and rename at the end, since rename is atomic.</li>"
              "<li>The encoding is not UTF-8, because someone exported it from Excel.</li>"
              "<li>Nobody notices it has been failing for a month, because there is no "
              "logging or alert.</li>"
              "</ul>"
              "<p>That list is the actual work. The conversion itself is Lesson 23 and takes "
              "six lines. Thinking about failure before you type is what separates a script "
              "that works once from a tool that runs unattended for a year.</p>")}
""",
)

# ---------------------------------------------------------------- 42
_add(
    level=5,
    num="42",
    slug="42-http",
    id="py-42-http",
    card="HTTP explained, then calling real APIs with requests: the skill that connects everything.",
    title="The Web: HTTP and APIs",
    emoji="🌐",
    desc="How HTTP works, using requests, status codes, headers, authentication, JSON APIs and rate limits.",
    lede="""Talking to other people's servers is where Python stops being a language you are
    learning and starts being a tool that does things.""",
    body=f"""
    <h2>What actually happens</h2>
    <p>
      Your program opens a connection, sends a small block of text describing what it wants,
      and gets a small block of text back with the answer attached. That is HTTP. It is
      genuinely this simple.
    </p>
    {out("""GET /repos/python/cpython HTTP/1.1
Host: api.github.com
Accept: application/json
User-Agent: python-school-example

--- and the reply ---

HTTP/1.1 200 OK
Content-Type: application/json
X-RateLimit-Remaining: 59

{"name": "cpython", "stargazers_count": 63000, ...}""")}
    {table(
        ["Method", "Means", "Should it change anything?"],
        [["<code>GET</code>", "give me this", "No. Safe to repeat"],
         ["<code>POST</code>", "here is something new", "Yes. Repeating creates duplicates"],
         ["<code>PUT</code>", "replace this entirely", "Yes, but repeating is harmless"],
         ["<code>PATCH</code>", "change part of this", "Yes"],
         ["<code>DELETE</code>", "remove this", "Yes, and repeating is usually harmless"]],
    )}
    {table(
        ["Status", "Family", "Means"],
        [["<code>200</code>, <code>201</code>, <code>204</code>", "2xx success", "It worked"],
         ["<code>301</code>, <code>302</code>, <code>304</code>", "3xx redirect", "Look elsewhere, or you already have it"],
         ["<code>400</code>", "4xx your fault", "Malformed request"],
         ["<code>401</code> / <code>403</code>", "", "Not authenticated / not allowed"],
         ["<code>404</code>", "", "No such thing"],
         ["<code>429</code>", "", "Slow down, you are rate limited"],
         ["<code>500</code>, <code>502</code>, <code>503</code>", "5xx their fault", "Their server broke. Retrying may help"]],
    )}

    <h2>requests, the one everyone uses</h2>
    {code('''import requests

response = requests.get("https://api.github.com/repos/python/cpython", timeout=10)

print(response.status_code)
print(response.headers["content-type"])

data = response.json()
print(data["full_name"], "has", data["stargazers_count"], "stars")''',
          run=False, verify="compile")}
    <p>
      No run button on this lesson's network examples: the school's in-browser Python has no
      network access, deliberately. Install <code>requests</code> in a virtual environment
      (Lesson 26) and run these on your own machine.
    </p>

    <h2>Doing it properly</h2>
    {code('''import requests


def fetch_repo(owner: str, name: str) -> dict:
    """Fetch one repository, raising a clear error on failure."""
    url = f"https://api.github.com/repos/{owner}/{name}"
    response = requests.get(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "python-school-example",
        },
        timeout=10,
    )
    response.raise_for_status()      # turns 4xx and 5xx into an exception
    return response.json()


try:
    repo = fetch_repo("python", "cpython")
    print(repo["description"])
except requests.HTTPError as err:
    print(f"HTTP {err.response.status_code}: {err.response.reason}")
except requests.Timeout:
    print("the server took too long")
except requests.RequestException as err:
    print(f"network problem: {err}")''',
          run=False, verify="compile")}
    {callout("danger", "⏱️ Always pass a timeout",
             "<p><code>requests</code> waits <strong>forever</strong> by default. One "
             "unresponsive server will hang your program until someone kills it. Every single "
             "request in production code should have a timeout, and ten seconds is a "
             "reasonable starting guess.</p>")}

    <h2>Query parameters, headers and POST</h2>
    {code('''import requests

# query string, built and escaped for you
response = requests.get(
    "https://api.github.com/search/repositories",
    params={"q": "language:python stars:>10000", "sort": "stars", "per_page": 5},
    timeout=10,
)

for repo in response.json()["items"]:
    print(f"{repo['stargazers_count']:>7,}  {repo['full_name']}")

# sending JSON
created = requests.post(
    "https://httpbin.org/post",
    json={"name": "Guybrush", "role": "captain"},
    timeout=10,
)
print(created.json()["json"])

# a form, and a file
requests.post("https://httpbin.org/post", data={"field": "value"}, timeout=10)''',
          run=False, verify="compile")}
    <p>
      Use <code>params=</code> rather than gluing a query string together yourself: it escapes
      spaces and symbols correctly. <code>json=</code> sets the content type and encodes the
      body; <code>data=</code> sends a form instead.
    </p>

    <h2>Authentication, and keeping the key out of your code</h2>
    {code('''import os
import requests

API_KEY = os.environ.get("WEATHER_API_KEY")
if not API_KEY:
    raise SystemExit("Set WEATHER_API_KEY first. Never hard-code it.")

response = requests.get(
    "https://api.example.com/v1/forecast",
    headers={"Authorization": f"Bearer {API_KEY}"},
    timeout=10,
)''',
          run=False, verify="compile")}
    {code('''# .env  (and add .env to .gitignore, today, before you forget)
WEATHER_API_KEY=abc123
GITHUB_TOKEN=ghp_xxxxxxxx''', run=False, verify="skip")}
    {code('''from dotenv import load_dotenv      # pip install python-dotenv
import os

load_dotenv()
key = os.environ["WEATHER_API_KEY"]''', run=False, verify="compile")}

    {voice("PARANOIA", "Legendary: Success",
           "A committed API key is not a small mistake. Bots scan every public commit on "
           "GitHub within seconds of it being pushed, and cloud keys have generated five "
           "figure bills overnight.",
           "Environment variables, a .env file that is gitignored, and the knowledge that git "
           "history is forever: deleting the key in a later commit does not remove it. If you "
           "ever push one, revoke it immediately. Not later. Immediately.")}

    <h2>Sessions: faster, and less repetition</h2>
    {code('''import requests

with requests.Session() as session:
    session.headers.update({
        "User-Agent": "python-school-example",
        "Accept": "application/json",
    })

    for name in ["cpython", "peps"]:
        response = session.get(f"https://api.github.com/repos/python/{name}", timeout=10)
        if response.ok:
            print(name, response.json()["stargazers_count"])''',
          run=False, verify="compile")}
    <p>
      A session reuses the underlying TCP connection, which makes repeated calls to the same
      host noticeably faster, and lets you set headers and cookies once. Use one whenever you
      make more than a single request.
    </p>

    <h2>Being a good citizen</h2>
    {code('''import time
import requests


def fetch_all(urls, session, delay=0.5, max_retries=3):
    """Fetch every URL politely: rate limited, with retries and backoff."""
    results = []

    for url in urls:
        for attempt in range(1, max_retries + 1):
            response = session.get(url, timeout=10)

            if response.status_code == 429:
                wait = int(response.headers.get("Retry-After", 2 ** attempt))
                print(f"rate limited, waiting {wait}s")
                time.sleep(wait)
                continue

            if response.status_code >= 500:
                wait = 2 ** attempt
                print(f"server error, retrying in {wait}s")
                time.sleep(wait)
                continue

            response.raise_for_status()
            results.append(response.json())
            break
        else:
            print(f"giving up on {url}")

        time.sleep(delay)

    return results''',
          run=False, verify="compile")}
    <ul>
      <li><strong>Honour 429 and Retry-After.</strong> Ignoring them gets your key banned.</li>
      <li><strong>Back off exponentially</strong> on server errors: 1s, 2s, 4s. Hammering a
      struggling server is how a small outage becomes a large one.</li>
      <li><strong>Never retry a POST blindly.</strong> You may create the same order twice.</li>
      <li><strong>Identify yourself</strong> in the User-Agent. Some APIs require it, and it
      lets an operator contact you instead of blocking you.</li>
    </ul>

    <h2>Without any packages at all</h2>
    {code('''import json
import urllib.request

request = urllib.request.Request(
    "https://api.github.com/repos/python/cpython",
    headers={"User-Agent": "python-school-example"},
)

with urllib.request.urlopen(request, timeout=10) as response:
    data = json.loads(response.read().decode("utf-8"))

print(data["name"])''',
          run=False, verify="compile")}
    <p>
      <code>urllib</code> is in the standard library and needs nothing installed, which matters
      on a locked-down machine or in a tiny container. It is clumsier than
      <code>requests</code> for anything complicated, which is exactly why
      <code>requests</code> is the most downloaded package on PyPI.
    </p>

    {exercise(1, "Read an API's documentation",
              "<p>Pick a free API with no key required: "
              "<code>https://api.github.com</code>, "
              "<code>https://pokeapi.co</code>, or "
              "<code>https://api.open-meteo.com</code>. Fetch something, print three fields, "
              "and handle a 404 gracefully.</p>",
              code('''import requests


def get_pokemon(name: str) -> dict | None:
    """Fetch one pokemon, or None if there is no such thing."""
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}", timeout=10)
    if response.status_code == 404:
        return None
    response.raise_for_status()
    return response.json()


for name in ["pikachu", "guybrush"]:
    data = get_pokemon(name)
    if data is None:
        print(f"{name}: no such pokemon")
        continue
    types = ", ".join(t["type"]["name"] for t in data["types"])
    print(f"{data['name']}: {data['height']}dm, {data['weight']}hg, type {types}")''',
                   run=False, verify="compile")
              + "<p>Treating 404 as a normal answer rather than an error is a real design "
              "decision. 'Not found' is information; letting it raise makes every caller wrap "
              "the call in a try block.</p>")}

    {exercise(2, "Cache the responses",
              "<p>Extend the fetch so repeated calls for the same thing read from a local JSON "
              "file instead of hitting the network.</p>",
              code('''import json
from pathlib import Path

import requests

CACHE = Path("api-cache")


def fetch_cached(name: str, max_age_calls: int = 1) -> dict:
    """Fetch a pokemon, using a local cache file when one exists."""
    CACHE.mkdir(exist_ok=True)
    cache_file = CACHE / f"{name.lower()}.json"

    if cache_file.exists():
        print(f"  (cache hit: {name})")
        return json.loads(cache_file.read_text(encoding="utf-8"))

    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}", timeout=10)
    response.raise_for_status()
    data = response.json()

    cache_file.write_text(json.dumps(data), encoding="utf-8")
    print(f"  (fetched and cached: {name})")
    return data''',
                   run=False, verify="compile")
              + "<p>Caching is politeness as well as speed: it is the single most effective "
              "way to stay inside a rate limit while developing, because the twentieth run of "
              "your script costs the API nothing. Real caches also need expiry, which is where "
              "the famous joke about cache invalidation comes from.</p>")}

    {exercise(3, "Read the status code table again",
              "<p>Your script starts returning 403. What are the three most likely causes, and "
              "how would you tell them apart?</p>",
              "<ol><li><strong>A missing or wrong key.</strong> Check whether the same URL "
              "works unauthenticated, and print the response body: most APIs explain the "
              "refusal in JSON.</li>"
              "<li><strong>Rate limiting dressed as 403.</strong> GitHub does exactly this for "
              "unauthenticated requests. Look for <code>X-RateLimit-Remaining: 0</code> in the "
              "response headers.</li>"
              "<li><strong>A missing User-Agent or a blocked one.</strong> Several APIs and "
              "most CDNs reject default Python user agents outright.</li></ol>"
              "<p>The general lesson: when a request fails, print "
              "<code>response.status_code</code>, <code>response.headers</code> and "
              "<code>response.text</code> before guessing. The answer is nearly always sitting "
              "in the response you did not read.</p>")}
""",
)

# ---------------------------------------------------------------- 43
_add(
    level=5,
    num="43",
    slug="43-scraping",
    id="py-43-scraping",
    card="Getting data out of web pages, and the ethics and law you need to know first.",
    title="Web Scraping",
    emoji="🕸️",
    desc="Parsing HTML with BeautifulSoup, selectors, pagination, and the legal and ethical rules of scraping.",
    lede="""When there is no API, the data is still there, in the page. Here is how to get it,
    and the rules that keep you out of trouble.""",
    body=f"""
    <h2>The rules, before the code</h2>
    {callout("danger", "⚖️ Read this section properly",
             "<p>Scraping is legal in many places and not in others, and the deciding factors "
             "are usually the site's terms of service, what you do with the data, and whether "
             "you caused harm. This is not legal advice. What follows is the professional "
             "standard of behaviour.</p>")}
    <ol class="steps">
      <li><strong>Look for an API first.</strong> Most sites worth scraping have one. It will
      be faster, more reliable and explicitly permitted.</li>
      <li><strong>Read <code>/robots.txt</code>.</strong> It tells you which paths the operator
      does not want automated access to. It is not legally binding everywhere, and ignoring it
      is bad faith.</li>
      <li><strong>Read the terms of service.</strong> Many explicitly prohibit automated
      collection.</li>
      <li><strong>Rate limit yourself.</strong> One request every second or two. You are a
      guest on someone else's hardware, and they pay for it.</li>
      <li><strong>Identify yourself</strong> in the User-Agent, with a way to contact you.</li>
      <li><strong>Never scrape personal data</strong> without a lawful basis. GDPR and similar
      laws apply to you even when the data is publicly visible.</li>
      <li><strong>Cache aggressively.</strong> Fetch once, parse many times while
      developing.</li>
    </ol>
    {code('''import urllib.robotparser

rules = urllib.robotparser.RobotFileParser()
rules.set_url("https://example.com/robots.txt")
rules.read()

if rules.can_fetch("my-scraper", "https://example.com/products"):
    print("allowed")
else:
    print("robots.txt says no. Stop.")''',
          run=False, verify="compile")}

    <h2>Parsing HTML</h2>
    {code('''from bs4 import BeautifulSoup      # pip install beautifulsoup4

html = """
<html><body>
  <h1 class="title">Stan's Previously Owned Vessels</h1>
  <ul id="ships">
    <li class="ship" data-id="1"><span class="name">Sea Monkey</span>
        <span class="price">£4,000</span></li>
    <li class="ship" data-id="2"><span class="name">Flying Dutchman</span>
        <span class="price">£12,500</span></li>
  </ul>
  <a href="/page/2">Next</a>
</body></html>
"""

soup = BeautifulSoup(html, "html.parser")

print(soup.h1.text)
print(soup.find("span", class_="name").text)

for ship in soup.find_all("li", class_="ship"):
    name = ship.find("span", class_="name").text
    price = ship.find("span", class_="price").text
    print(f"{ship['data-id']}  {name:16} {price}")

print(soup.find("a")["href"])''',
          run=False, verify="compile")}
    <p>
      That example needs <code>beautifulsoup4</code> installed, so it has no run button. The
      standard library <em>does</em> include an HTML parser, though, and for a simple job it is
      enough:
    </p>
    {code('''from html.parser import HTMLParser


class LinkFinder(HTMLParser):
    """Collect every href in a document. No packages required."""

    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.links.append(value)


finder = LinkFinder()
finder.feed("""
<p>See <a href="/python/">the course</a> and
<a href="https://rustyschool.com">the school</a>.</p>
""")
print(finder.links)''',
          expect="['/python/', 'https://rustyschool.com']")}

    <h2>Selectors, the concise way</h2>
    {code('''from bs4 import BeautifulSoup

soup = BeautifulSoup("<div class='card'><h2>Title</h2><p>Body</p></div>", "html.parser")

print(soup.select_one("div.card h2").text)
print([tag.name for tag in soup.select("div.card > *")])
print(soup.select("p")[0].get_text(strip=True))''',
          run=False, verify="compile")}
    {table(
        ["Selector", "Matches"],
        [["<code>div</code>", "every div"],
         ["<code>.card</code>", "anything with class card"],
         ["<code>#ships</code>", "the element with id ships"],
         ["<code>div.card p</code>", "a p anywhere inside a div.card"],
         ["<code>div &gt; p</code>", "a p that is a direct child"],
         ["<code>a[href^='/page']</code>", "links whose href starts with /page"]],
    )}

    <h2>A complete, polite scraper</h2>
    {code('''import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

CACHE = Path("scrape-cache")
HEADERS = {"User-Agent": "python-school-example (contact: you@example.com)"}


def get_page(url: str, session: requests.Session, delay: float = 1.5) -> str:
    """Fetch a page, using a local cache so development costs the site nothing."""
    CACHE.mkdir(exist_ok=True)
    key = CACHE / (url.replace("/", "_").replace(":", "") + ".html")

    if key.exists():
        return key.read_text(encoding="utf-8")

    response = session.get(url, timeout=10)
    response.raise_for_status()
    key.write_text(response.text, encoding="utf-8")
    time.sleep(delay)          # only sleep when we really hit the network
    return response.text


def parse_ships(html: str) -> list[dict]:
    """Pull the ship records out of one page."""
    soup = BeautifulSoup(html, "html.parser")
    ships = []
    for item in soup.select("li.ship"):
        name = item.select_one(".name")
        price = item.select_one(".price")
        if not name or not price:
            continue          # the page changed; skip rather than crash
        ships.append({
            "id": item.get("data-id"),
            "name": name.get_text(strip=True),
            "price": price.get_text(strip=True),
        })
    return ships


def scrape_all(start_url: str, max_pages: int = 5) -> list[dict]:
    """Follow 'Next' links, politely, up to a hard limit."""
    results = []
    url = start_url

    with requests.Session() as session:
        session.headers.update(HEADERS)
        for _ in range(max_pages):
            html = get_page(url, session)
            results.extend(parse_ships(html))

            soup = BeautifulSoup(html, "html.parser")
            next_link = soup.select_one("a.next")
            if not next_link:
                break
            url = requests.compat.urljoin(url, next_link["href"])

    return results''',
          run=False, verify="compile")}

    {voice("PARANOIA", "Medium: Success",
           "Note the hard limit on pages and the skip-rather-than-crash when a field is "
           "missing. Both exist because scrapers run unattended against pages that change "
           "without warning.",
           "A scraper with no page limit that follows links is a program that can crawl an "
           "entire site, or loop forever between two pages that link to each other. Put a "
           "ceiling on anything that follows links it did not choose.")}

    <h2>When the content is not in the HTML</h2>
    <p>
      Fetch a modern site and find an almost empty page: the content is loaded by JavaScript
      after the page arrives, and <code>requests</code> does not run JavaScript. Three options,
      in order of preference:
    </p>
    <ol>
      <li><strong>Find the underlying API.</strong> Open your browser's developer tools,
      Network tab, and reload. The page is almost certainly fetching JSON from an endpoint you
      can call directly. This is faster and more stable than parsing HTML, and it is what
      experienced scrapers do first.</li>
      <li><strong>Look for embedded data.</strong> Many pages ship their data inside a
      <code>&lt;script type="application/json"&gt;</code> tag.</li>
      <li><strong>Drive a real browser</strong> with
      {link("Playwright", "https://playwright.dev/python/")} or Selenium. Powerful, slow,
      fragile, and a much heavier commitment.</li>
    </ol>

    <h2>Tables, the easy case</h2>
    {code('''import pandas as pd      # pip install pandas lxml

tables = pd.read_html("https://en.wikipedia.org/wiki/List_of_programming_languages")
print(len(tables), "tables found")
print(tables[0].head())''',
          run=False, verify="compile")}
    <p>
      If the data you want is already in an HTML <code>&lt;table&gt;</code>, one pandas call
      turns every table on the page into a dataframe. It is worth checking for this before
      writing any parsing code at all.
    </p>

    {exercise(1, "Extract structured data",
              "<p>Parse this fragment with the standard library only and produce a list of "
              "dictionaries.</p>"
              + code('''<div class="book"><span class="t">Dune</span><span class="y">1965</span></div>
<div class="book"><span class="t">Neuromancer</span><span class="y">1984</span></div>''',
                     run=False, verify="skip"),
              code('''from html.parser import HTMLParser


class BookParser(HTMLParser):
    """Collect book titles and years without any third-party packages."""

    def __init__(self):
        super().__init__()
        self.books = []
        self.current = {}
        self.field = None

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "")
        if tag == "div" and "book" in classes:
            self.current = {}
        elif tag == "span" and classes in ("t", "y"):
            self.field = "title" if classes == "t" else "year"

    def handle_data(self, data):
        if self.field:
            self.current[self.field] = data.strip()
            self.field = None

    def handle_endtag(self, tag):
        if tag == "div" and self.current:
            self.books.append(self.current)
            self.current = {}


parser = BookParser()
parser.feed("""
<div class="book"><span class="t">Dune</span><span class="y">1965</span></div>
<div class="book"><span class="t">Neuromancer</span><span class="y">1984</span></div>
""")

for book in parser.books:
    print(f"{book['title']:12} ({book['year']})")''',
                   expect="""Dune         (1965)
Neuromancer  (1984)""")
              + "<p>This is a state machine: it remembers what it is currently inside. That is "
              "why <code>BeautifulSoup</code> exists, and why it is worth the install for "
              "anything beyond a simple document.</p>")}

    {exercise(2, "Would you scrape it?",
              "<p>For each, decide: scrape, use an API, or do not touch it.</p>"
              "<ol><li>Product prices from a shop that has a public API.</li>"
              "<li>Your own posts from a forum you belong to.</li>"
              "<li>Email addresses from a member directory.</li>"
              "<li>Public weather data from a government site.</li>"
              "<li>Every article from a news site, to train a model.</li></ol>",
              "<ol><li><strong>Use the API.</strong> Faster, allowed, and it will not break "
              "when they change their CSS.</li>"
              "<li><strong>Fine,</strong> and check whether there is an export feature first. "
              "Your own data is the easiest case there is.</li>"
              "<li><strong>Do not.</strong> Harvesting personal contact details is a data "
              "protection problem in most jurisdictions and a spam problem "
              "everywhere.</li>"
              "<li><strong>Usually fine,</strong> and often explicitly encouraged. Check for a "
              "bulk download; government sites frequently publish the whole dataset.</li>"
              "<li><strong>Careful.</strong> Copyright applies to the articles, terms of "
              "service usually forbid it, and this is the subject of active litigation. At "
              "minimum, read the terms and prefer licensed datasets.</li></ol>")}

    {exercise(3, "Make a scraper survive a redesign",
              "<p>Your scraper breaks every time the site changes. List four things that make "
              "one more durable.</p>",
              "<ul>"
              "<li><strong>Select on meaning, not on layout.</strong> "
              "<code>[data-product-id]</code> or a semantic class survives a redesign; "
              "<code>div &gt; div &gt; div:nth-child(3)</code> does not.</li>"
              "<li><strong>Fail loudly on structure, quietly on content.</strong> If zero "
              "items parse, raise: the page has changed. If one item is missing a field, log "
              "it and continue.</li>"
              "<li><strong>Cache raw HTML.</strong> When parsing breaks you can then debug "
              "against the exact page that failed, without hitting the site again.</li>"
              "<li><strong>Write a test with a saved page.</strong> A stored HTML fixture plus "
              "an expected result turns 'it broke' into a failing test that shows you "
              "where.</li>"
              "</ul>"
              "<p>And the honest one: scrapers rot. Anything built on someone else's HTML is "
              "borrowed time, which is the strongest argument for checking one more time "
              "whether an API exists.</p>")}
""",
)

# ---------------------------------------------------------------- 44
_add(
    level=5,
    num="44",
    slug="44-web-apps",
    id="py-44-web-apps",
    card="Serve your own pages and your own API, with the standard library and then with FastAPI.",
    title="Building a Web App",
    emoji="🚀",
    desc="A web server from the standard library, then Flask and FastAPI, routing, templates, and deployment.",
    lede="""You have been calling other people's servers. Now you write one, and the whole
    thing stops being mysterious.""",
    body=f"""
    <h2>A real web server, no packages</h2>
    {code('''from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.respond(200, "text/html", "<h1>Ahoy from Python</h1>")
        elif self.path == "/api/crew":
            body = json.dumps([{"name": "Guybrush"}, {"name": "Elaine"}])
            self.respond(200, "application/json", body)
        else:
            self.respond(404, "text/plain", "Not found")

    def respond(self, status, content_type, body):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type + "; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *args):
        pass          # quiet


if __name__ == "__main__":
    HTTPServer(("localhost", 8000), Handler).serve_forever()''',
          run=False, verify="compile")}
    <p>
      That is a genuinely working web server in thirty lines, with nothing installed. Run it,
      visit <code>http://localhost:8000</code>, and you have served a page. The Rusty School
      next door is served by a Rust program of exactly this shape, which is
      <a href="../../build/09-server.html">the capstone project over there</a>.
    </p>
    <p>
      It is also not something you would deploy: no routing to speak of, one request at a
      time, no templates, no security. Which is what frameworks are for.
    </p>

    <h2>Flask: the small one</h2>
    {code('''from flask import Flask, request, jsonify, render_template_string      # pip install flask

app = Flask(__name__)

CREW = [
    {"id": 1, "name": "Guybrush", "role": "captain"},
    {"id": 2, "name": "Elaine", "role": "governor"},
]

PAGE = """
<!doctype html>
<title>Crew</title>
<h1>The crew of the {{ ship }}</h1>
<ul>{% for member in crew %}<li>{{ member.name }} ({{ member.role }})</li>{% endfor %}</ul>
"""


@app.route("/")
def index():
    return render_template_string(PAGE, ship="Sea Monkey", crew=CREW)


@app.route("/api/crew")
def list_crew():
    return jsonify(CREW)


@app.route("/api/crew/<int:member_id>")
def get_member(member_id):
    for member in CREW:
        if member["id"] == member_id:
            return jsonify(member)
    return jsonify({"error": "no such crew member"}), 404


@app.route("/api/crew", methods=["POST"])
def add_member():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name is required"}), 400
    member = {"id": max(m["id"] for m in CREW) + 1, "name": data["name"],
              "role": data.get("role", "deckhand")}
    CREW.append(member)
    return jsonify(member), 201


if __name__ == "__main__":
    app.run(debug=True)''',
          run=False, verify="compile")}
    <p>
      The <code>@app.route</code> decorator should look familiar now: Lesson 35 explained
      exactly what it is doing, which is registering your function in a lookup table of paths.
      Nothing here is magic any more.
    </p>

    <h2>FastAPI: the modern one</h2>
    {code('''from fastapi import FastAPI, HTTPException      # pip install "fastapi[standard]"
from pydantic import BaseModel

app = FastAPI(title="Crew API")


class Member(BaseModel):
    """The type hints are the validation, the docs and the parsing."""
    name: str
    role: str = "deckhand"
    insults: int = 0


CREW: dict[int, Member] = {1: Member(name="Guybrush", role="captain", insults=8)}


@app.get("/api/crew")
def list_crew() -> list[Member]:
    return list(CREW.values())


@app.get("/api/crew/{member_id}")
def get_member(member_id: int) -> Member:
    if member_id not in CREW:
        raise HTTPException(status_code=404, detail="no such crew member")
    return CREW[member_id]


@app.post("/api/crew", status_code=201)
def add_member(member: Member) -> Member:
    new_id = max(CREW) + 1
    CREW[new_id] = member
    return member''',
          run=False, verify="compile")}
    {term("""$ fastapi dev main.py

INFO  Uvicorn running on http://127.0.0.1:8000
INFO  Application startup complete.

# and for free, at http://127.0.0.1:8000/docs :
# a complete interactive API documentation page, generated from your type hints""")}

    {voice("INTERFACING", "Formidable: Success",
           "Look at what those type hints just bought. FastAPI reads them and generates "
           "request parsing, validation with proper error messages, JSON serialisation, and a "
           "full interactive documentation site.",
           "Send it {\\\"name\\\": 42} and it replies with a precise 422 explaining that name "
           "must be a string, without you writing a line of validation. This is the strongest "
           "practical argument for Lesson 38 that exists.")}

    <h2>Choosing</h2>
    {table(
        ["Framework", "Best for", "Trade"],
        [["<code>http.server</code>", "Learning, tiny internal tools", "You write everything"],
         ["<strong>Flask</strong>", "Small apps, HTML pages, huge ecosystem", "Synchronous by default; validation is manual"],
         ["<strong>FastAPI</strong>", "JSON APIs, async, automatic docs", "Newer; more concepts to learn"],
         ["<strong>Django</strong>", "Full products: admin, auth, ORM, migrations", "Large and opinionated; overkill for an API"],
         ["<strong>Litestar</strong>, <strong>Starlette</strong>", "Alternatives worth knowing about", ""]],
    )}
    <p>
      A reasonable default in 2026: FastAPI if you are serving JSON, Django if you are building
      a product with users and an admin panel, Flask if you want something small that renders
      HTML.
    </p>

    <h2>Templates: HTML with holes in it</h2>
    {code('''from jinja2 import Template      # ships with Flask; pip install jinja2 otherwise

template = Template("""
<h1>{{ ship }}</h1>
<ul>
{% for member in crew %}
  <li>{{ member.name }}{% if member.captain %} (captain){% endif %}</li>
{% endfor %}
</ul>
<p>{{ crew | length }} aboard.</p>
""")

print(template.render(
    ship="Sea Monkey",
    crew=[{"name": "Guybrush", "captain": True}, {"name": "Otis", "captain": False}],
))''',
          run=False, verify="compile")}
    {callout("danger", "🛡️ Jinja escapes HTML for you. Do not switch it off.",
             "<p>If a user's name is <code>&lt;script&gt;steal()&lt;/script&gt;</code> and you "
             "insert it into a page unescaped, you have a cross-site scripting hole. Jinja "
             "escapes by default in Flask; the <code>|safe</code> filter turns that off and "
             "should be treated as a loaded weapon. Never build HTML with f-strings and user "
             "input.</p>")}

    <h2>Where the danger actually is</h2>
    <ul>
      <li><strong>SQL injection.</strong> Never build queries with f-strings. Lesson 45 shows
      the parameterised form.</li>
      <li><strong>Cross-site scripting.</strong> Use a template engine and leave escaping
      on.</li>
      <li><strong>Secrets in code.</strong> Environment variables, as in Lesson 42.</li>
      <li><strong><code>debug=True</code> in production.</strong> Flask's debugger lets anyone
      who triggers an error run arbitrary Python on your server. It is off by default for a
      reason.</li>
      <li><strong>Trusting any input.</strong> Validate at the boundary. Pydantic does this for
      you, which is most of why FastAPI exists.</li>
    </ul>

    <h2>Getting it online</h2>
    {term("""# development
fastapi dev main.py

# production: a real server process, several workers
pip install "uvicorn[standard]"
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# in front of it, nginx or Caddy for TLS and static files""")}
    {table(
        ["Where", "Good for", "Cost"],
        [["A small VPS", "Full control, learning how it all fits", "A few pounds a month, and you patch it"],
         ["Fly.io, Railway, Render", "Push and it deploys", "Free tiers exist; they sleep when idle"],
         ["A serverless platform", "Bursty traffic, no servers to run", "Cold starts, and a different mental model"],
         ["Cloudflare Pages / Workers", "Static sites and edge functions", "Free tier, and how this school is hosted"]],
    )}
    {callout("info", "🏫 This school as the example",
             "<p>The site you are reading is static HTML on Cloudflare Pages, with a handful of "
             "small serverless functions for progress sync and the anonymous completion "
             "counter. Free tier, no server to patch, and the whole thing is in a public "
             "repository you can read. Static-first with a small dynamic edge is a genuinely "
             "good default for a personal project.</p>")}

    {exercise(1, "A JSON API from the standard library",
              "<p>Extend the plain <code>http.server</code> example with a "
              "<code>/api/time</code> endpoint returning JSON, and a 404 that is also JSON.</p>",
              code('''import json
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer

ROUTES = {}


def route(path):
    """A tiny decorator, exactly like Flask's, so you can see there is no magic."""
    def register(func):
        ROUTES[path] = func
        return func
    return register


@route("/api/time")
def current_time():
    return {"utc": datetime.now(timezone.utc).isoformat(), "ok": True}


@route("/api/crew")
def crew():
    return {"crew": ["Guybrush", "Elaine"]}


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        handler = ROUTES.get(self.path)
        status = 200 if handler else 404
        body = handler() if handler else {"error": "not found", "path": self.path}
        encoded = json.dumps(body).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def log_message(self, *args):
        pass


# Proving the routing works without starting a server:
print(json.dumps(ROUTES["/api/crew"]()))
print(sorted(ROUTES))''',
                   expect="""{"crew": ["Guybrush", "Elaine"]}
['/api/crew', '/api/time']""")
              + "<p>Writing your own <code>@route</code> decorator is the moment Flask stops "
              "being magic. It is a dictionary from paths to functions, and that is genuinely "
              "all a router is.</p>")}

    {exercise(2, "Find the security holes",
              "<p>Three serious problems. Name them.</p>"
              + code('''from flask import Flask, request
import sqlite3

app = Flask(__name__)


@app.route("/search")
def search():
    term = request.args.get("q")
    conn = sqlite3.connect("shop.db")
    rows = conn.execute(f"SELECT * FROM products WHERE name LIKE '%{term}%'").fetchall()
    return f"<h1>Results for {term}</h1>" + "".join(f"<p>{r}</p>" for r in rows)


app.run(debug=True, host="0.0.0.0")''', run=False, verify="compile"),
              "<ol><li><strong>SQL injection.</strong> The query is built with an f-string, so "
              "<code>?q=' OR 1=1 --</code> returns the whole table and worse is possible. Use "
              "<code>conn.execute(\"... LIKE ?\", (f\"%{{term}}%\",))</code>.</li>"
              "<li><strong>Cross-site scripting.</strong> <code>term</code> goes straight into "
              "the HTML, so <code>?q=&lt;script&gt;...&lt;/script&gt;</code> executes in every "
              "visitor's browser. Render a template and let it escape.</li>"
              "<li><strong><code>debug=True</code> on <code>0.0.0.0</code>.</strong> That "
              "exposes an interactive Python console to the entire network. This is a remote "
              "code execution hole, deliberately, for development only.</li></ol>"
              "<p>Bonus: the connection is never closed, and there is no error handling if the "
              "database file is missing.</p>")}

    {exercise(3, "Design the endpoints",
              "<p>Design a REST API for a to-do list, before writing code. What paths, what "
              "methods, what status codes?</p>",
              out("""GET    /api/tasks              200  list all, supports ?done=true&limit=20
POST   /api/tasks              201  create one, returns it with its new id
                               400  if the body is invalid

GET    /api/tasks/{id}         200  one task
                               404  if there is no such id
PUT    /api/tasks/{id}         200  replace it entirely
PATCH  /api/tasks/{id}         200  change some fields, eg {"done": true}
DELETE /api/tasks/{id}         204  deleted, no body to return
                               404  if it was not there""")
              + "<p>The conventions worth absorbing: plural nouns for collections, the id in "
              "the path rather than a query parameter, the method carries the verb so the URL "
              "never contains <code>/deleteTask</code>, 201 for creation with the new object "
              "in the body, and 204 for a successful delete with nothing to say. Following "
              "them means other developers can guess your API correctly.</p>")}
""",
)

# ---------------------------------------------------------------- 45
_add(
    level=5,
    num="45",
    slug="45-databases",
    id="py-45-databases",
    card="SQLite is built in, is a real database, and is enough for far more than you think.",
    title="Databases with SQLite",
    emoji="🗄️",
    desc="SQL basics, sqlite3 from the standard library, parameterised queries, transactions and when to use a database.",
    lede="""A real SQL database ships with Python, lives in a single file, and needs no server.
    It is the most under-used tool in the standard library.""",
    body=f"""
    <h2>When a file is not enough</h2>
    <p>Reach for a database when you need any of:</p>
    <ul>
      <li>to find things by criteria without loading everything into memory;</li>
      <li>relationships between kinds of thing (orders belong to customers);</li>
      <li>more data than fits comfortably in RAM;</li>
      <li>several things writing at once without corrupting each other;</li>
      <li>a guarantee that a half-finished update never survives a crash.</li>
    </ul>
    <p>
      SQLite gives you all of that in a file, with no server to install or administer. It is
      in your phone, your browser, and on most aircraft. The
      {link("official docs", "https://www.sqlite.org/whentouse.html")} claim it is the most
      widely deployed database engine in the world, and that is probably true.
    </p>

    <h2>Creating and inserting</h2>
    {code('''import sqlite3

conn = sqlite3.connect("ship.db")
conn.execute("""
    CREATE TABLE IF NOT EXISTS crew (
        id       INTEGER PRIMARY KEY,
        name     TEXT NOT NULL,
        role     TEXT NOT NULL DEFAULT 'deckhand',
        pay      INTEGER NOT NULL CHECK (pay >= 0),
        joined   TEXT NOT NULL
    )
""")

conn.execute(
    "INSERT INTO crew (name, role, pay, joined) VALUES (?, ?, ?, ?)",
    ("Guybrush", "captain", 100, "1990-10-15"),
)
conn.executemany(
    "INSERT INTO crew (name, role, pay, joined) VALUES (?, ?, ?, ?)",
    [
        ("Elaine", "governor", 250, "1990-10-15"),
        ("Otis", "lookout", 40, "1991-01-03"),
        ("Meathook", "lookout", 45, "1991-06-20"),
    ],
)
conn.commit()

print(conn.execute("SELECT COUNT(*) FROM crew").fetchone()[0], "crew")
conn.close()''',
          expect="4 crew")}

    {callout("danger", "💉 The question marks are not optional",
             "<p>Never build SQL with f-strings. <code>f\"... WHERE name = '{{name}}'\"</code> "
             "with <code>name</code> set to <code>' OR 1=1 --</code> returns your whole table, "
             "and worse inputs can drop it. Passing values as a separate tuple means the "
             "database treats them strictly as data, never as code. This is the single most "
             "famous vulnerability in web software and it is entirely preventable by typing "
             "<code>?</code>.</p>")}
    {code('''import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT)")
conn.execute("INSERT INTO users VALUES ('Guybrush')")
conn.execute("INSERT INTO users VALUES ('Elaine')")

attack = "' OR '1'='1"

# The safe way: the input is data, so it simply matches nothing
safe = conn.execute("SELECT * FROM users WHERE name = ?", (attack,)).fetchall()
print("parameterised:", safe)

# The unsafe way, shown once so you recognise it
unsafe = conn.execute(f"SELECT * FROM users WHERE name = '{attack}'").fetchall()
print("f-string:     ", unsafe)''',
          expect="""parameterised: []
f-string:      [('Guybrush',), ('Elaine',)]""")}
    <p>
      The second query returned every row, because the input closed the quote and added its
      own condition. That is SQL injection, demonstrated in four lines.
    </p>

    <h2>Querying</h2>
    {code('''import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE crew (id INTEGER PRIMARY KEY, name TEXT, role TEXT, pay INTEGER)")
conn.executemany("INSERT INTO crew (name, role, pay) VALUES (?, ?, ?)", [
    ("Guybrush", "captain", 100),
    ("Elaine", "governor", 250),
    ("Otis", "lookout", 40),
    ("Meathook", "lookout", 45),
])

for row in conn.execute("SELECT name, pay FROM crew WHERE pay > ? ORDER BY pay DESC", (50,)):
    print(f"{row[0]:10} {row[1]}")

print("---")
print(conn.execute("SELECT COUNT(*), SUM(pay), AVG(pay) FROM crew").fetchone())

print("---")
for role, count, total in conn.execute(
    "SELECT role, COUNT(*), SUM(pay) FROM crew GROUP BY role ORDER BY SUM(pay) DESC"
):
    print(f"{role:10} {count} people, {total} total")''',
          expect="""Elaine     250
Guybrush   100
---
(4, 435, 108.75)
---
governor   1 people, 250 total
captain    1 people, 100 total
lookout    2 people, 85 total""")}

    <h2>Rows as dictionaries, which is far nicer</h2>
    {code('''import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row          # the one line worth remembering
conn.execute("CREATE TABLE crew (name TEXT, role TEXT, pay INTEGER)")
conn.execute("INSERT INTO crew VALUES ('Guybrush', 'captain', 100)")

row = conn.execute("SELECT * FROM crew").fetchone()

print(row["name"], row["pay"])
print(dict(row))
print(row.keys())''',
          expect="""Guybrush 100
{'name': 'Guybrush', 'role': 'captain', 'pay': 100}
['name', 'role', 'pay']""")}

    <h2>Relationships: the actual point of SQL</h2>
    {code('''import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")      # SQLite needs asking, every connection

conn.executescript("""
    CREATE TABLE ships (
        id   INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    CREATE TABLE crew (
        id      INTEGER PRIMARY KEY,
        name    TEXT NOT NULL,
        ship_id INTEGER REFERENCES ships(id) ON DELETE CASCADE
    );
    INSERT INTO ships (name) VALUES ('Sea Monkey'), ('Flying Dutchman');
    INSERT INTO crew (name, ship_id) VALUES
        ('Guybrush', 1), ('Otis', 1), ('LeChuck', 2);
""")

for row in conn.execute("""
    SELECT ships.name AS ship, COUNT(crew.id) AS crew_count
    FROM ships
    LEFT JOIN crew ON crew.ship_id = ships.id
    GROUP BY ships.id
    ORDER BY crew_count DESC
"""):
    print(f"{row['ship']:16} {row['crew_count']} crew")

print("---")
for row in conn.execute("""
    SELECT crew.name, ships.name AS ship
    FROM crew JOIN ships ON crew.ship_id = ships.id
    WHERE ships.name = ?
""", ("Sea Monkey",)):
    print(f"{row['name']} sails the {row['ship']}")''',
          expect="""Sea Monkey       2 crew
Flying Dutchman  1 crew
---
Guybrush sails the Sea Monkey
Otis sails the Sea Monkey""")}
    <p>
      A <code>JOIN</code> answers a question that would otherwise be two loops and a
      dictionary in Python, and the database does it with an index instead of scanning. This is
      what SQL is for, and it is why "just use a JSON file" stops working around a few thousand
      records.
    </p>

    <h2>Transactions: all or nothing</h2>
    {code('''import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE accounts (name TEXT PRIMARY KEY, balance INTEGER)")
conn.executemany("INSERT INTO accounts VALUES (?, ?)",
                 [("Guybrush", 100), ("Elaine", 250)])
conn.commit()


def transfer(conn, sender, recipient, amount):
    """Move money. Either both sides happen or neither does."""
    try:
        with conn:          # commits on success, rolls back on any exception
            balance = conn.execute(
                "SELECT balance FROM accounts WHERE name = ?", (sender,)
            ).fetchone()[0]
            if balance < amount:
                raise ValueError(f"{sender} has only {balance}")
            conn.execute("UPDATE accounts SET balance = balance - ? WHERE name = ?",
                         (amount, sender))
            conn.execute("UPDATE accounts SET balance = balance + ? WHERE name = ?",
                         (amount, recipient))
        return "ok"
    except ValueError as err:
        return f"refused: {err}"


print(transfer(conn, "Guybrush", "Elaine", 50))
print(transfer(conn, "Guybrush", "Elaine", 500))
print(dict(conn.execute("SELECT name, balance FROM accounts ORDER BY name").fetchall()))''',
          expect="""ok
refused: Guybrush has only 50
{'Elaine': 300, 'Guybrush': 50}""")}
    <p>
      <code>with conn:</code> is a transaction. If anything inside raises, every change is
      undone. Without it, a crash between the two UPDATE statements would destroy money, which
      is the classic illustration of why databases have transactions at all.
    </p>

    <h2>Indexes: the difference between instant and unusable</h2>
    {code('''import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE events (id INTEGER PRIMARY KEY, user_id INTEGER, action TEXT)")
conn.executemany("INSERT INTO events (user_id, action) VALUES (?, ?)",
                 [(i % 100, "click") for i in range(20000)])

plan_before = conn.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM events WHERE user_id = 42"
).fetchone()[-1]

conn.execute("CREATE INDEX idx_events_user ON events(user_id)")

plan_after = conn.execute(
    "EXPLAIN QUERY PLAN SELECT * FROM events WHERE user_id = 42"
).fetchone()[-1]

print("before:", plan_before)
print("after: ", plan_after)''',
          expect="""before: SCAN events
after:  SEARCH events USING INDEX idx_events_user (user_id=?)""")}
    <p>
      SCAN means it read every row. SEARCH USING INDEX means it jumped straight there. On
      twenty thousand rows the difference is small; on twenty million it is the difference
      between a page that loads and a page that times out. Index the columns you filter and
      join on, and <code>EXPLAIN QUERY PLAN</code> tells you whether it worked.
    </p>

    <h2>Beyond SQLite</h2>
    {table(
        ["Tool", "Use when"],
        [["<strong>SQLite</strong>", "One machine, one writer at a time, up to many gigabytes. Most personal projects, forever"],
         ["<strong>PostgreSQL</strong>", "Several writers, a network, real users. The default serious choice"],
         ["<strong>MySQL / MariaDB</strong>", "Similar; often what a host gives you"],
         ["<strong>An ORM</strong> (SQLAlchemy, Django, SQLModel)", "You want Python objects instead of SQL strings, and migrations"],
         ["<strong>Redis</strong>", "Caching and ephemeral data, not durable storage"]],
    )}
    {callout("info", "🧭 On ORMs",
             "<p>An object-relational mapper lets you write <code>session.query(Crew).filter"
             "(Crew.pay &gt; 50)</code> instead of SQL. They are genuinely useful for large "
             "applications and they hide what the database is doing, which is fine until it is "
             "not. Learn enough SQL to read what your ORM generates: the "
             "<a href='https://docs.sqlalchemy.org' target='_blank' rel='noopener'>SQLAlchemy</a> "
             "docs are excellent, and every serious backend job expects SQL literacy.</p>")}

    {exercise(1, "Build a small library database",
              "<p>Two tables, authors and books, with a foreign key. Insert a few rows and "
              "produce a report of each author with their book count.</p>",
              code('''import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = ON")

conn.executescript("""
    CREATE TABLE authors (
        id   INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE
    );
    CREATE TABLE books (
        id        INTEGER PRIMARY KEY,
        title     TEXT NOT NULL,
        year      INTEGER,
        author_id INTEGER NOT NULL REFERENCES authors(id)
    );
""")

conn.executemany("INSERT INTO authors (name) VALUES (?)",
                 [("Herbert",), ("Gibson",), ("Unpublished",)])
conn.executemany("INSERT INTO books (title, year, author_id) VALUES (?, ?, ?)", [
    ("Dune", 1965, 1),
    ("Dune Messiah", 1969, 1),
    ("Neuromancer", 1984, 2),
])
conn.commit()

for row in conn.execute("""
    SELECT authors.name, COUNT(books.id) AS n, MIN(books.year) AS first
    FROM authors
    LEFT JOIN books ON books.author_id = authors.id
    GROUP BY authors.id
    ORDER BY n DESC, authors.name
"""):
    first = row["first"] or "-"
    print(f"{row['name']:12} {row['n']} books, first {first}")''',
                   expect="""Herbert      2 books, first 1965
Gibson       1 books, first 1984
Unpublished  0 books, first -""")
              + "<p>The <code>LEFT JOIN</code> is what includes the author with no books. A "
              "plain <code>JOIN</code> would silently drop them, which is one of the most "
              "common reporting bugs there is.</p>")}

    {exercise(2, "Fix the injection",
              "<p>Rewrite this safely, and explain what an attacker could do with it.</p>"
              + code('''def find_user(conn, username):
    return conn.execute(
        f"SELECT * FROM users WHERE username = '{username}'"
    ).fetchall()''', run=False, verify="compile"),
              code('''def find_user(conn, username):
    """Find a user by name. The value is passed as data, never as SQL."""
    return conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchall()''', run=False, verify="compile")
              + "<p>With the original, <code>username</code> set to <code>' OR '1'='1</code> "
              "returns every user. Set to <code>'; DROP TABLE users; --</code> it would try to "
              "delete the table (SQLite's <code>execute</code> blocks multiple statements, "
              "which is a lucky accident rather than a defence; most database drivers do "
              "not).</p>"
              "<p>The habit to build: if a value came from outside your program, it goes in "
              "the tuple, never in the string. There is no exception to this rule.</p>")}

    {exercise(3, "When would you not use SQLite?",
              "<p>Name three situations where SQLite is the wrong choice, and what you would "
              "use instead.</p>",
              "<ol><li><strong>Several servers writing at once.</strong> SQLite allows one "
              "writer at a time and the file must be on local disk; on a network filesystem "
              "the locking is unreliable. Use PostgreSQL.</li>"
              "<li><strong>You need per-user access control inside the database.</strong> "
              "SQLite has no users or permissions: anyone who can read the file has "
              "everything.</li>"
              "<li><strong>Very high concurrent write throughput,</strong> such as thousands "
              "of writes a second from many clients. WAL mode helps a lot, but this is what "
              "client-server databases are built for.</li></ol>"
              "<p>What is <em>not</em> a good reason: 'it is only a toy database'. It handles "
              "hundreds of gigabytes, it is used in production by enormous companies, and for "
              "a single-machine application it is often the better engineering choice, because "
              "there is no server to secure, back up or keep running.</p>")}
""",
)

# ---------------------------------------------------------------- 46
_add(
    level=5,
    num="46",
    slug="46-data",
    id="py-46-data",
    card="NumPy and pandas: the tools that made Python the language of science.",
    title="Data Analysis",
    emoji="📊",
    desc="NumPy arrays, pandas DataFrames, loading and cleaning data, grouping, and honest analysis.",
    lede="""This is why physicists, economists and machine learning researchers all ended up
    writing Python. Two libraries, and a spreadsheet stops being big enough to matter.""",
    body=f"""
    <h2>Why not just use lists?</h2>
    {code('''# Pure Python: a loop, and a new list
prices = [10.0, 24.99, 3.25, 8.75]
with_vat = [p * 1.2 for p in prices]
print([round(p, 2) for p in with_vat])
print(round(sum(prices) / len(prices), 2))''',
          expect="""[12.0, 29.99, 3.9, 10.5]
11.75""")}
    {code('''import numpy as np      # pip install numpy

prices = np.array([10.0, 24.99, 3.25, 8.75])

print(np.round(prices * 1.2, 2))      # no loop: applies to everything at once
print(prices.mean(), prices.std().round(2))
print(prices[prices > 9])''',
          run=False, verify="compile")}
    <p>
      Three differences that matter. The syntax is shorter. The operation applies to the whole
      array at once, which is called <strong>vectorisation</strong>. And it runs perhaps fifty
      times faster, because the loop happens in compiled C over a contiguous block of memory
      rather than in Python over a list of separate objects.
    </p>

    {voice("ENCYCLOPEDIA", "Medium: Success",
           "This is the resolution of the 'Python is slow' argument from Base Camp 4. NumPy is "
           "not really Python: it is a thin, friendly skin over decades of highly optimised C "
           "and Fortran, including LAPACK, which physicists have been tuning since the 1970s.",
           "You write the experiment in a language designed for thinking, and the arithmetic "
           "runs in a language designed for speed. That trade is the whole reason scientific "
           "computing settled here.")}

    <h2>pandas: a spreadsheet you can program</h2>
    {code('''import pandas as pd      # pip install pandas

crew = pd.DataFrame([
    {"name": "Guybrush", "role": "captain", "pay": 100, "joined": "1990-10-15"},
    {"name": "Elaine", "role": "governor", "pay": 250, "joined": "1990-10-15"},
    {"name": "Otis", "role": "lookout", "pay": 40, "joined": "1991-01-03"},
    {"name": "Meathook", "role": "lookout", "pay": 45, "joined": "1991-06-20"},
])

print(crew.head())
print(crew.shape)
print(crew.dtypes)
print(crew["pay"].describe())''',
          run=False, verify="compile")}
    {out("""       name      role  pay      joined
0  Guybrush   captain  100  1990-10-15
1    Elaine  governor  250  1990-10-15
2      Otis   lookout   40  1991-01-03
3  Meathook   lookout   45  1991-06-20

(4, 4)

name      object
role      object
pay        int64
joined    object
dtype: object

count      4.000000
mean     108.750000
std      100.041658
min       40.000000
25%       43.750000
50%       72.500000
75%      137.500000
max      250.000000
Name: pay, dtype: float64""")}
    <p>
      A <code>DataFrame</code> is a table with named columns, each column a typed array.
      <code>.describe()</code> on a numeric column is usually the first thing you run on
      unfamiliar data, and it will often tell you immediately that something is wrong.
    </p>

    <h2>Loading real data</h2>
    {code('''import pandas as pd

df = pd.read_csv("sales.csv")
df = pd.read_json("data.json")
df = pd.read_excel("report.xlsx")           # needs openpyxl
df = pd.read_sql("SELECT * FROM crew", conn)
df = pd.read_html("https://example.com/table")[0]

df.to_csv("clean.csv", index=False)
df.to_json("clean.json", orient="records", indent=2)''',
          run=False, verify="compile")}
    <p>
      That list is most of why pandas won: whatever the data is in, one line loads it, and one
      line writes it back out as something else.
    </p>

    <h2>Selecting, filtering, sorting</h2>
    {code('''import pandas as pd

crew = pd.DataFrame({
    "name": ["Guybrush", "Elaine", "Otis", "Meathook"],
    "role": ["captain", "governor", "lookout", "lookout"],
    "pay": [100, 250, 40, 45],
})

print(crew["pay"].sum())
print(crew[crew["pay"] > 50])
print(crew[(crew["role"] == "lookout") & (crew["pay"] > 42)])
print(crew.sort_values("pay", ascending=False).head(2))
print(crew.loc[crew["name"] == "Otis", "pay"])''',
          run=False, verify="compile")}
    {callout("warn", "🪤 & and |, not and and or",
             "<p>pandas filters compare whole columns at once, so Python's <code>and</code> "
             "(which wants a single true or false) raises <code>ValueError: The truth value of "
             "a Series is ambiguous</code>. Use <code>&amp;</code> and <code>|</code>, and put "
             "brackets around each condition, because they bind more tightly than "
             "<code>==</code>.</p>")}

    <h2>Grouping: the operation you will use most</h2>
    {code('''import pandas as pd

sales = pd.DataFrame({
    "region": ["North", "South", "North", "South", "East"],
    "seller": ["Elaine", "Otis", "Guybrush", "Meathook", "Stan"],
    "amount": [1200, 340, 890, 1150, 4200],
})

print(sales.groupby("region")["amount"].sum().sort_values(ascending=False))
print(sales.groupby("region").agg(
    total=("amount", "sum"),
    average=("amount", "mean"),
    sellers=("seller", "count"),
))''',
          run=False, verify="compile")}
    {out("""region
East     4200
North    2090
South    1490
Name: amount, dtype: int64

        total  average  sellers
region
East     4200   4200.0        1
North    2090   1045.0        2
South    1490    745.0        2""")}
    <p>
      Split by a key, apply a calculation, combine the results. It is the same idea as SQL's
      GROUP BY and as the dictionary-of-lists grouping you wrote by hand in Lesson 15, and it
      is the single most useful data operation there is.
    </p>

    <h2>Cleaning: where the real time goes</h2>
    {code('''import pandas as pd
import numpy as np

messy = pd.DataFrame({
    "name": ["  Guybrush ", "ELAINE", None, "Otis"],
    "pay": ["100", "250", "40", "not recorded"],
    "joined": ["1990-10-15", "15/10/1990", None, "1991-01-03"],
})

clean = messy.copy()
clean["name"] = clean["name"].str.strip().str.title()
clean["pay"] = pd.to_numeric(clean["pay"], errors="coerce")
clean["joined"] = pd.to_datetime(clean["joined"], format="mixed", errors="coerce")

print(clean)
print(clean.isna().sum())
print(clean.dropna(subset=["name", "pay"]))''',
          run=False, verify="compile")}
    <p>
      <code>errors="coerce"</code> turns anything unparseable into <code>NaN</code> rather than
      raising, which lets you see the whole extent of the mess before deciding what to do about
      it. <code>.isna().sum()</code> counts the gaps per column and is the second thing you
      should run on any new dataset.
    </p>

    {callout("danger", "🧭 Deciding what to do with missing data is analysis, not cleanup",
             "<p>Dropping rows with gaps can silently bias your result, because the rows with "
             "missing data are often not a random sample. Filling them with the mean invents "
             "data that was never observed. Both are sometimes right. Neither is a default, "
             "and whichever you choose belongs in your write-up.</p>")}

    <h2>An honest worked example</h2>
    {code('''import pandas as pd

df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "sales": [100, 120, 118, 135, 150, 900],
})

print(f"mean:   {df['sales'].mean():.1f}")
print(f"median: {df['sales'].median():.1f}")

# a rough outlier check before believing either number
q1, q3 = df["sales"].quantile([0.25, 0.75])
iqr = q3 - q1
outliers = df[(df["sales"] < q1 - 1.5 * iqr) | (df["sales"] > q3 + 1.5 * iqr)]
print(outliers)''',
          run=False, verify="compile")}
    {out("""mean:   253.8
median: 127.5

  month  sales
5   Jun    900""")}
    <p>
      The mean says business more than doubled. The median says it grew steadily. One
      exceptional June is dragging the mean, and reporting it without saying so would be
      technically true and actively misleading. Always look at the distribution before quoting
      an average, and say which one you used.
    </p>

    <h2>The wider ecosystem</h2>
    {table(
        ["Tool", "For"],
        [["<strong>NumPy</strong>", "Arrays and numerical computing. The foundation everything else sits on"],
         ["<strong>pandas</strong>", "Tables, cleaning, grouping, time series"],
         ["<strong>Polars</strong>", "A faster pandas alternative, written in Rust, excellent for large data"],
         ["<strong>matplotlib</strong> / <strong>seaborn</strong>", "Charts (Lesson 47)"],
         ["<strong>scikit-learn</strong>", "Classical machine learning: regression, clustering, classification"],
         ["<strong>SciPy</strong>", "Statistics, optimisation, signal processing"],
         ["<strong>Jupyter</strong>", "Notebooks: code, output and prose interleaved. The standard workspace"],
         ["<strong>DuckDB</strong>", "SQL directly over CSV and Parquet files, extremely fast"]],
    )}

    {exercise(1, "Do it without pandas first",
              "<p>Using only the standard library, load this CSV, compute the total and mean "
              "per region, and print a sorted report. Then note how many lines pandas would "
              "have taken.</p>",
              code('''import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

Path("sales.csv").write_text("""region,seller,amount
North,Elaine,1200
South,Otis,340
North,Guybrush,890
South,Meathook,1150
East,Stan,4200
""", encoding="utf-8")

amounts = defaultdict(list)
with open("sales.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        amounts[row["region"]].append(int(row["amount"]))

for region, values in sorted(amounts.items(), key=lambda kv: sum(kv[1]), reverse=True):
    print(f"{region:6} total {sum(values):5,}  mean {mean(values):7,.1f}  n={len(values)}")''',
                   expect="""East   total 4,200  mean 4,200.0  n=1
North  total 2,090  mean 1,045.0  n=2
South  total 1,490  mean   745.0  n=2""")
              + "<p>In pandas that is two lines: <code>pd.read_csv(...)</code> then "
              "<code>.groupby('region')['amount'].agg(['sum','mean','count'])</code>. Both are "
              "correct. Knowing the long version means you know what the short one is doing, "
              "and it means you can still work on a machine where you cannot install "
              "anything.</p>")}

    {exercise(2, "Spot the misleading analysis",
              "<p>A report says: 'average customer spend rose from £40 to £95, a 137% "
              "increase.' What would you ask before believing it?</p>",
              "<ul>"
              "<li><strong>Mean or median?</strong> One enterprise customer can move a mean and "
              "leave the typical customer untouched.</li>"
              "<li><strong>Did the denominator change?</strong> If you dropped your cheapest "
              "tier, average spend rises while revenue falls.</li>"
              "<li><strong>Same population?</strong> Comparing all customers against active "
              "customers only is a different question.</li>"
              "<li><strong>How many customers?</strong> A jump from 3 to 5 customers is not a "
              "trend.</li>"
              "<li><strong>What is the distribution?</strong> Plot it. Two numbers cannot "
              "describe a shape.</li>"
              "<li><strong>Inflation, seasonality, currency?</strong> Compare like with "
              "like.</li>"
              "</ul>"
              "<p>Every one of those is a question about the data, not about Python. The "
              "library will happily compute a beautifully precise wrong answer, and noticing "
              "that is the actual skill.</p>")}

    {exercise(3, "Install and explore",
              "<p>On your own machine, install pandas and load something real: a CSV export "
              "from your bank, a spreadsheet, or an open dataset. Run these five lines before "
              "anything else.</p>",
              code('''import pandas as pd

df = pd.read_csv("your-data.csv")

print(df.shape)            # how much is there
print(df.dtypes)           # did anything numeric load as text
print(df.head())           # what does a row look like
print(df.isna().sum())     # where are the gaps
print(df.describe())       # ranges, and any impossible values''',
                   run=False, verify="compile")
              + "<p>That is the standard first contact with any dataset, and it routinely "
              "finds problems before you waste an hour analysing them: a date column loaded as "
              "text, a price column with a currency symbol making it a string, negative ages, "
              "or a column that is 90% empty.</p>")}
""",
)

# ---------------------------------------------------------------- 47
_add(
    level=5,
    num="47",
    slug="47-charts",
    id="py-47-charts",
    card="Turning numbers into pictures, and not lying with them.",
    title="Charts and Visualisation",
    emoji="📈",
    desc="matplotlib basics, choosing the right chart, labelling properly, and the ways charts mislead.",
    lede="""A chart is an argument. This lesson covers how to draw one in Python, and how to
    make sure the argument it makes is true.""",
    body=f"""
    <h2>The simplest chart</h2>
    {code('''import matplotlib      # pip install matplotlib
matplotlib.use("Agg")           # render to a file, no window needed
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
sales = [100, 120, 118, 135, 150, 162]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(months, sales, marker="o")
ax.set_title("Monthly sales, 2026")
ax.set_xlabel("Month")
ax.set_ylabel("Sales (£000s)")
ax.grid(alpha=0.3)

fig.tight_layout()
fig.savefig("sales.png", dpi=150)
print("written to sales.png")''',
          run=False, verify="compile")}
    <p>
      The pattern is always the same: make a figure and axes, draw on the axes, label
      everything, save or show. <code>matplotlib.use("Agg")</code> tells it to render to a file
      rather than open a window, which is what you want on a server or in a script.
    </p>

    <h2>Choosing the right chart</h2>
    {table(
        ["Question", "Chart", "Notes"],
        [["How has this changed over time?", "Line", "Time on the x-axis, always"],
         ["How do these categories compare?", "Bar", "Horizontal if the labels are long"],
         ["What is the distribution?", "Histogram", "The one people forget, and often the most informative"],
         ["Are these two things related?", "Scatter", "Correlation, not causation. Say so"],
         ["What are the parts of a whole?", "Stacked bar", "Not a pie chart. See below"],
         ["Where are the outliers?", "Box plot", "Shows median, quartiles and stragglers at once"]],
    )}
    {callout("warn", "🥧 On pie charts",
             "<p>Humans compare angles badly and lengths well. A pie chart with more than about "
             "four slices is harder to read than the bar chart of the same data, and two pie "
             "charts side by side are nearly impossible to compare. Use a bar chart. If someone "
             "insists on a pie, sort the slices and never explode them.</p>")}

    <h2>Several charts at once</h2>
    {code('''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

rng = np.random.default_rng(seed=42)
data = rng.normal(loc=100, scale=15, size=500)

fig, axes = plt.subplots(1, 3, figsize=(14, 4))

axes[0].hist(data, bins=30, edgecolor="white")
axes[0].set_title("Distribution")

axes[1].boxplot(data, vert=False)
axes[1].set_title("Spread and outliers")

axes[2].scatter(data[:-1], data[1:], alpha=0.4, s=12)
axes[2].set_title("Each value against the next")

for ax in axes:
    ax.grid(alpha=0.3)

fig.suptitle("Three views of the same 500 numbers")
fig.tight_layout()
fig.savefig("three-views.png", dpi=150)
print("saved")''',
          run=False, verify="compile")}
    <p>
      Note the seeded random generator: <code>default_rng(seed=42)</code> makes the figure
      reproducible, which matters as much for a chart in a report as it does for a test.
    </p>

    <h2>The chart nobody labels properly</h2>
    {code('''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

regions = ["East", "North", "South", "West"]
totals = [4200, 2090, 1490, 980]

fig, ax = plt.subplots(figsize=(8, 4.5))
bars = ax.barh(regions, totals, color="#4584b6")

ax.set_title("Total sales by region, Q2 2026")
ax.set_xlabel("Sales (£)")
ax.bar_label(bars, fmt="£{:,.0f}", padding=4)
ax.set_xlim(0, max(totals) * 1.15)
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
fig.savefig("regions.png", dpi=150)
print("saved")''',
          run=False, verify="compile")}
    <p>A chart is finished when it has:</p>
    <ul>
      <li>a title that states the finding, not just the subject;</li>
      <li>axis labels <strong>with units</strong>;</li>
      <li>a source and a date, if anyone else will see it;</li>
      <li>no more ink than the data needs. Remove gridlines, borders and legends that earn
      nothing.</li>
    </ul>

    <h2>How charts lie</h2>
    {code('''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

months = ["Jan", "Feb", "Mar", "Apr"]
values = [100, 102, 101, 104]

fig, (left, right) = plt.subplots(1, 2, figsize=(11, 4))

left.bar(months, values, color="#c92a2a")
left.set_ylim(99, 105)
left.set_title("'Explosive growth!'")

right.bar(months, values, color="#4584b6")
right.set_ylim(0, 120)
right.set_title("The same data, honest axis")

fig.tight_layout()
fig.savefig("truncated.png", dpi=150)
print("saved")''',
          run=False, verify="compile")}

    {voice("RHETORIC", "Formidable: Success",
           "The left chart is not false. Every number on it is correct. It is simply drawn so "
           "that a four percent change fills the frame and reads as a quadrupling.",
           "Truncating a bar chart's y-axis is the most common deception in business "
           "presentations, and it is usually not malice: it is someone letting the plotting "
           "library pick the limits. Bar charts must start at zero, because the bar's length is "
           "the message. Line charts may not, because the slope is the message.")}

    <p>The other reliable ways to mislead, in case you meet them:</p>
    <ul>
      <li><strong>Cherry-picked ranges.</strong> Any trend can be reversed by choosing the
      start date.</li>
      <li><strong>Two y-axes.</strong> Almost always used to imply a relationship between
      unrelated series, and the scales can be tuned until the lines agree.</li>
      <li><strong>Area for a single number.</strong> Doubling a circle's radius quadruples its
      area, so the reader sees a 4x change in a 2x quantity.</li>
      <li><strong>Correlation presented as cause.</strong> Ice cream sales and drownings rise
      together. Neither causes the other; summer causes both.</li>
    </ul>

    <h2>Other tools</h2>
    {table(
        ["Tool", "Good for"],
        [["<strong>matplotlib</strong>", "Everything, eventually. Verbose but total control"],
         ["<strong>seaborn</strong>", "Statistical charts in one line, sensible defaults"],
         ["<strong>plotly</strong>", "Interactive charts for web pages"],
         ["<strong>pandas .plot()</strong>", "Quick looks straight from a DataFrame"],
         ["<strong>Altair</strong>", "Declarative: you describe the mapping, it draws it"]],
    )}
    {code('''import pandas as pd

df = pd.DataFrame({"month": ["Jan", "Feb", "Mar"], "sales": [100, 120, 118]})

# the fastest possible look at some data
ax = df.plot(x="month", y="sales", kind="bar", title="Sales", figsize=(6, 3))
ax.figure.savefig("quick.png")''',
          run=False, verify="compile")}

    {exercise(1, "Draw a distribution",
              "<p>Generate 1,000 dice-roll totals for two dice, plot them as a histogram, and "
              "label it properly. Seed the generator so it is reproducible.</p>",
              code('''import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import random

random.seed(42)
totals = [random.randint(1, 6) + random.randint(1, 6) for _ in range(1000)]

fig, ax = plt.subplots(figsize=(8, 4.5))
ax.hist(totals, bins=range(2, 14), align="left", rwidth=0.85, color="#4584b6")

ax.set_title("Two dice, 1,000 rolls: seven is the most likely total")
ax.set_xlabel("Total of both dice")
ax.set_ylabel("Number of rolls")
ax.set_xticks(range(2, 13))
ax.spines[["top", "right"]].set_visible(False)

fig.tight_layout()
fig.savefig("dice.png", dpi=150)
print("saved dice.png")''',
                   run=False, verify="compile")
              + "<p>The title states the finding rather than naming the chart. That single "
              "habit improves reports more than any styling.</p>")}

    {exercise(2, "Fix the misleading chart",
              "<p>A colleague sends a chart showing 'a 300% increase in engagement'. The y-axis "
              "runs from 4.0 to 4.3 and the x-axis covers eleven days. What do you say?</p>",
              "<p>Something like: <em>the axis starts at 4.0, so a 0.3 change fills the whole "
              "frame. In absolute terms this is a 7% move, not 300%, and the 300% figure "
              "appears to be the change relative to the truncated baseline rather than to "
              "zero. Eleven days is also short enough that normal weekly variation could "
              "explain it. Could we see it from zero, over a quarter, with the weekly cycle "
              "visible?</em></p>"
              "<p>Note the tone. The chart is nearly always an honest mistake by someone who "
              "let the library choose the limits. Asking to see it differently gets a better "
              "chart; accusing someone of lying gets a defensive colleague.</p>")}

    {exercise(3, "Chart selection",
              "<p>Which chart for each?</p>"
              "<ol><li>Website visitors per day for a year.</li>"
              "<li>Revenue from five product lines this quarter.</li>"
              "<li>How long users spend on a page.</li>"
              "<li>Whether taller people earn more.</li>"
              "<li>The share of traffic from four sources, compared across three months.</li></ol>",
              "<ol><li><strong>Line.</strong> Time series. Consider a seven-day rolling average "
              "to reveal the trend under the weekly cycle.</li>"
              "<li><strong>Bar,</strong> horizontal if the product names are long, sorted by "
              "value.</li>"
              "<li><strong>Histogram.</strong> The mean is nearly useless here: this "
              "distribution will be heavily skewed by a few very long sessions.</li>"
              "<li><strong>Scatter,</strong> with a note that any correlation is not "
              "causation, and that confounders like age and occupation are doing much of the "
              "work.</li>"
              "<li><strong>Stacked bar,</strong> three bars side by side. Three pie charts "
              "would make the comparison nearly impossible.</li></ol>")}
""",
)

# ---------------------------------------------------------------- 48
_add(
    level=5,
    num="48",
    slug="48-games",
    id="py-48-games",
    card="The game loop, and a playable game in under a hundred lines with pygame.",
    title="Making Games",
    emoji="🎮",
    desc="The game loop, pygame basics, sprites, collision, input handling, and text adventures with no libraries.",
    lede="""Games are the best way to learn programming, because the feedback is instant and
    the bugs are funny. Here is the loop that every game ever written is built on.""",
    body=f"""
    <h2>Every game, ever</h2>
    {code('''def game_loop():
    """The structure under Doom, Tetris and Elden Ring alike."""
    running = True
    while running:
        # 1. handle input      what did the player just do?
        # 2. update state      move everything, apply rules, check collisions
        # 3. draw              paint the current state
        # 4. wait              hold a steady frame rate
        running = False
    return "game over"


print(game_loop())''',
          expect="game over")}
    <p>
      That is it. Sixty times a second, forever. Everything else is detail, and the detail is
      where the fun is.
    </p>

    <h2>A complete text adventure, no libraries</h2>
    {code('''ROOMS = {
    "beach": {
        "description": "A beach. A rubber chicken lies in the sand.",
        "exits": {"north": "jungle"},
        "items": ["rubber chicken"],
    },
    "jungle": {
        "description": "Thick jungle. Something rustles.",
        "exits": {"south": "beach", "east": "clearing"},
        "items": [],
    },
    "clearing": {
        "description": "A clearing with a locked chest.",
        "exits": {"west": "jungle"},
        "items": ["chest"],
    },
}


def play(commands):
    """Run a scripted game so the example is reproducible."""
    here = "beach"
    carrying = []
    output = []

    for command in commands:
        room = ROOMS[here]
        match command.lower().split():
            case ["look"]:
                output.append(room["description"])
                if room["items"]:
                    output.append("You see: " + ", ".join(room["items"]))
            case ["go", direction] if direction in room["exits"]:
                here = room["exits"][direction]
                output.append(f"You go {direction}. {ROOMS[here]['description']}")
            case ["go", direction]:
                output.append(f"You cannot go {direction} from here.")
            case ["take", *words] if " ".join(words) in room["items"]:
                item = " ".join(words)
                room["items"].remove(item)
                carrying.append(item)
                output.append(f"Taken: {item}.")
            case ["inventory"] | ["i"]:
                output.append("Carrying: " + (", ".join(carrying) or "nothing"))
            case _:
                output.append(f"I do not understand {command!r}.")

    return output


for line in play(["look", "take rubber chicken", "inventory", "go north", "go up", "look"]):
    print(line)''',
          expect="""A beach. A rubber chicken lies in the sand.
You see: rubber chicken
Taken: rubber chicken.
Carrying: rubber chicken
You go north. Thick jungle. Something rustles.
You cannot go up from here.
Thick jungle. Something rustles.""")}
    <p>
      Dictionaries for the world, <code>match</code> for the parser, a list for the inventory.
      Every technique in there came from Levels 2 and 4, and this is a real game. The workshop
      builds it out properly with saving, locked doors and a win condition.
    </p>

    <h2>pygame: actual graphics</h2>
    {code('''import pygame      # pip install pygame-ce

WIDTH, HEIGHT = 640, 480
PLAYER_SPEED = 300      # pixels per second, not per frame


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Escape from Melee Island")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 28)

    player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 32, 32)
    treasure = pygame.Rect(500, 100, 24, 24)
    score = 0
    running = True

    while running:
        delta = clock.tick(60) / 1000        # seconds since the last frame

        # 1. input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * PLAYER_SPEED * delta
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * PLAYER_SPEED * delta

        # 2. update
        player.x = max(0, min(WIDTH - player.width, player.x + int(dx)))
        player.y = max(0, min(HEIGHT - player.height, player.y + int(dy)))

        if player.colliderect(treasure):
            score += 1
            treasure.topleft = (
                (treasure.x * 7 + 113) % (WIDTH - 24),
                (treasure.y * 5 + 71) % (HEIGHT - 24),
            )

        # 3. draw
        screen.fill((18, 22, 27))
        pygame.draw.rect(screen, (255, 222, 87), treasure)
        pygame.draw.rect(screen, (69, 132, 182), player)
        screen.blit(font.render(f"Treasure: {score}", True, (233, 238, 244)), (10, 10))
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()''',
          run=False, verify="compile")}

    {callout("tip", "⏱️ Multiply movement by delta time",
             "<p><code>player.x += 5</code> moves five pixels per <em>frame</em>, so the game "
             "runs at double speed on a 120Hz monitor. <code>speed * delta</code> moves a fixed "
             "distance per <em>second</em>, so it behaves identically everywhere. This is the "
             "single most common beginner bug in game programming, and it is why old PC games "
             "become unplayable on modern hardware.</p>")}

    <h2>Sprites and groups</h2>
    {code('''import pygame


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 16))
        self.image.fill((255, 222, 87))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.bob = 0.0

    def update(self, delta):
        self.bob += delta
        self.rect.y += int(2 * (self.bob % 1 < 0.5) - 1)


coins = pygame.sprite.Group(Coin(100, 100), Coin(200, 150))

# in the loop:
#   coins.update(delta)
#   coins.draw(screen)
#   collected = pygame.sprite.spritecollide(player_sprite, coins, dokill=True)''',
          run=False, verify="compile")}
    <p>
      <code>Sprite</code> and <code>Group</code> are pygame's answer to "I now have four
      hundred coins". A group updates and draws everything in one call, and
      <code>spritecollide</code> handles the collisions. This is the point where the classes
      from Lesson 31 stop being an exercise and start being load-bearing.
    </p>

    <h2>The wider landscape</h2>
    {table(
        ["Tool", "Best for", "Note"],
        [["<strong>pygame-ce</strong>", "2D games, learning, jams", "The maintained community fork. Use this, not the original pygame"],
         ["<strong>Arcade</strong>", "2D with a more modern API", "Built on OpenGL, nice sprite handling"],
         ["<strong>Pyxel</strong>", "Tiny retro games", "16 colours, 4 channels, delightful constraints"],
         ["<strong>Ren'Py</strong>", "Visual novels", "A whole engine, and genuinely popular commercially"],
         ["<strong>Godot</strong>", "Serious 2D and 3D", "GDScript is Python-like; a real engine with an editor"],
         ["<strong>Bevy</strong> (Rust)", "Performance-critical games", "The <a href='../../learn/index.html'>sister school</a> covers it"]],
    )}

    {voice("DRAMA", "Medium: Success",
           "Let us be honest with the student. Nobody ships a commercial 3D game in Python, and "
           "pretending otherwise would be a disservice.",
           "But Python is arguably the best language in existence for <em>learning</em> game "
           "programming, and for game jams, prototypes and tools. Every studio has Python "
           "somewhere in its pipeline. And a finished small game teaches more than an "
           "unfinished large one, in any language.")}

    <h2>Finishing a game is the hard part</h2>
    <ul>
      <li><strong>Make the smallest playable thing first.</strong> One screen, one mechanic. If
      it is not fun with rectangles, art will not save it.</li>
      <li><strong>Playtest early on someone else.</strong> Watch without helping. Everything
      they struggle with is your bug, not theirs.</li>
      <li><strong>Scope down twice.</strong> Then again. Almost every unfinished hobby game
      died of ambition.</li>
      <li><strong>Ship it.</strong> A tiny finished game beats a magnificent unfinished one,
      every single time.</li>
    </ul>

    {exercise(1, "Add a feature to the adventure",
              "<p>Add a locked chest that opens only if the player is carrying a key, with a "
              "key hidden in the jungle.</p>",
              code('''ROOMS = {
    "jungle": {"description": "Thick jungle.", "exits": {"east": "clearing"},
               "items": ["rusty key"]},
    "clearing": {"description": "A clearing with a locked chest.", "exits": {"west": "jungle"},
                 "items": []},
}

CHEST_OPEN = False


def play(commands):
    global CHEST_OPEN
    here = "jungle"
    carrying = []
    output = []

    for command in commands:
        room = ROOMS[here]
        match command.lower().split():
            case ["take", *words] if " ".join(words) in room["items"]:
                item = " ".join(words)
                room["items"].remove(item)
                carrying.append(item)
                output.append(f"Taken: {item}.")
            case ["go", direction] if direction in room["exits"]:
                here = room["exits"][direction]
                output.append(f"You go {direction}.")
            case ["open", "chest"] if here != "clearing":
                output.append("There is no chest here.")
            case ["open", "chest"] if "rusty key" not in carrying:
                output.append("The chest is locked. You have no key.")
            case ["open", "chest"]:
                CHEST_OPEN = True
                output.append("The key turns. Inside: the Secret of Monkey Island.")
            case _:
                output.append(f"You cannot do that.")

    return output


for line in play(["open chest", "go east", "open chest", "go west",
                  "take rusty key", "go east", "open chest"]):
    print(line)''',
                   expect="""There is no chest here.
You go east.
The chest is locked. You have no key.
You go west.
Taken: rusty key.
You go east.
The key turns. Inside: the Secret of Monkey Island.""")
              + "<p>Note the order of the <code>case</code> clauses: the most specific guard "
              "first. Put the unguarded <code>open chest</code> earlier and it would swallow "
              "the other two, which is the same ordering trap as FizzBuzz in Lesson 7.</p>")}

    {exercise(2, "Design a game loop on paper",
              "<p>For a game of Pong, write out what happens in each of the four loop phases.</p>",
              out("""1. INPUT
   read up/down keys for player 1 and player 2 (or read the AI's decision)
   check for quit and pause

2. UPDATE
   move paddles by speed * delta, clamped to the screen
   move ball by velocity * delta
   if ball hits top or bottom wall: invert vertical velocity
   if ball overlaps a paddle: invert horizontal velocity, add spin from
       paddle movement, increase speed slightly
   if ball passes the left or right edge: award a point, reset to centre,
       serve towards the player who conceded
   if either score reaches 11: state = game over

3. DRAW
   clear the screen
   draw both paddles, the ball, the centre line, both scores
   if game over: draw the winner and 'press space'
   flip the buffer

4. WAIT
   clock.tick(60), and capture delta for the next frame""")
              + "<p>Writing this out before coding is worth twenty minutes. Nearly every "
              "difficult game bug is really an ordering problem: collision checked before "
              "movement, or the score checked after the reset.</p>")}

    {exercise(3, "Fix the frame-rate bug",
              "<p>This game is unplayably fast on one machine and sluggish on another.</p>"
              + code('''while running:
    clock.tick(60)
    player.x += 5
    enemy.y += 2''', run=False, verify="skip"),
              code('''while running:
    delta = clock.tick(60) / 1000        # seconds since the last frame

    player.x += PLAYER_SPEED * delta     # pixels per second
    enemy.y += ENEMY_SPEED * delta''', run=False, verify="skip")
              + "<p><code>clock.tick(60)</code> caps the frame rate but cannot guarantee it: a "
              "slow machine drops to 30fps and everything moves at half speed, while an "
              "uncapped 144Hz display runs at more than double. Multiplying by elapsed time "
              "makes movement depend on the clock rather than on the hardware.</p>"
              "<p>The same principle applies to every animation, physics step and timer in any "
              "real-time program, not just games.</p>")}
""",
)

# ---------------------------------------------------------------- 49
_add(
    level=5,
    num="49",
    slug="49-desktop",
    id="py-49-desktop",
    card="Windows, buttons and menus with tkinter, which is already installed.",
    title="Desktop Applications",
    emoji="🖥️",
    desc="Building GUIs with tkinter, event-driven programming, widgets, layout, and keeping the interface responsive.",
    lede="""Not everything should be a command line. tkinter ships with Python, works on every
    operating system, and will get a small tool into a non-programmer's hands today.""",
    body=f"""
    <h2>Event-driven programming</h2>
    <p>
      A command-line program runs top to bottom and stops. A GUI program sets up a window,
      registers what should happen when things are clicked, and then hands control to a loop
      that waits for the user. Your code becomes a set of responses rather than a sequence.
    </p>
    {code('''import tkinter as tk

root = tk.Tk()
root.title("Ahoy")

count = 0


def on_click():
    """This runs when the button is pressed. Not before."""
    global count
    count += 1
    label.config(text=f"Insults learned: {count}")


label = tk.Label(root, text="Insults learned: 0", font=("Helvetica", 16))
label.pack(padx=40, pady=20)

tk.Button(root, text="Learn an insult", command=on_click).pack(pady=(0, 20))

root.mainloop()          # hands control to tkinter. Nothing after this runs until the window closes''',
          run=False, verify="compile")}
    <p>
      <code>mainloop()</code> is the equivalent of the game loop from Lesson 48: it waits for
      events and dispatches them to your functions. Everything you write is a callback.
    </p>

    <h2>The widgets you will actually use</h2>
    {code('''import tkinter as tk
from tkinter import ttk          # themed widgets: they look native

root = tk.Tk()
root.title("Crew manager")
root.geometry("420x360")

name = tk.StringVar(value="Guybrush")
role = tk.StringVar(value="captain")
active = tk.BooleanVar(value=True)

frame = ttk.Frame(root, padding=16)
frame.pack(fill="both", expand=True)

ttk.Label(frame, text="Name").grid(row=0, column=0, sticky="w", pady=4)
ttk.Entry(frame, textvariable=name, width=24).grid(row=0, column=1, pady=4)

ttk.Label(frame, text="Role").grid(row=1, column=0, sticky="w", pady=4)
ttk.Combobox(frame, textvariable=role, values=["captain", "lookout", "cook"],
             state="readonly").grid(row=1, column=1, pady=4)

ttk.Checkbutton(frame, text="Currently aboard", variable=active).grid(
    row=2, column=0, columnspan=2, sticky="w", pady=8)

listbox = tk.Listbox(frame, height=6)
listbox.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=8)
frame.rowconfigure(3, weight=1)
frame.columnconfigure(1, weight=1)


def add_member():
    status = "aboard" if active.get() else "ashore"
    listbox.insert("end", f"{name.get()} ({role.get()}, {status})")
    name.set("")


ttk.Button(frame, text="Add to crew", command=add_member).grid(
    row=4, column=0, columnspan=2, pady=4)

root.mainloop()''',
          run=False, verify="compile")}
    {table(
        ["Widget", "For"],
        [["<code>Label</code>", "Text you display"],
         ["<code>Entry</code>", "One line of typed input"],
         ["<code>Text</code>", "Multi-line editing"],
         ["<code>Button</code>", "Doing something"],
         ["<code>Checkbutton</code> / <code>Radiobutton</code>", "Choices"],
         ["<code>Combobox</code>", "A dropdown"],
         ["<code>Listbox</code> / <code>Treeview</code>", "Lists and tables"],
         ["<code>Frame</code>", "Grouping, and the key to sane layout"],
         ["<code>Canvas</code>", "Drawing anything you like"]],
    )}

    <h2>Layout: pick one and stick to it</h2>
    {table(
        ["Manager", "Idea", "Use for"],
        [["<code>.pack()</code>", "Stack things in a direction", "Simple vertical or horizontal layouts"],
         ["<code>.grid()</code>", "Rows and columns", "Forms. Almost always the right choice"],
         ["<code>.place()</code>", "Exact pixel positions", "Almost never"]],
    )}
    {callout("danger", "🪤 Never mix pack and grid in the same container",
             "<p>tkinter will hang forever with no error while the two managers argue about "
             "the size of the container. It is a silent freeze, not a crash, and it is the "
             "single most confusing tkinter bug. Different containers may use different "
             "managers; one container must pick one.</p>")}

    <h2>Dialogs and files</h2>
    {code('''import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

root = tk.Tk()
root.withdraw()          # hide the main window; we only want dialogs


def open_and_count():
    path = filedialog.askopenfilename(
        title="Choose a text file",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
    )
    if not path:
        return          # the user cancelled, which is not an error

    try:
        words = len(Path(path).read_text(encoding="utf-8").split())
    except UnicodeDecodeError:
        messagebox.showerror("Cannot read", "That does not look like a text file.")
        return

    if messagebox.askyesno("Result", f"{words} words. Save a report?"):
        target = filedialog.asksaveasfilename(defaultextension=".txt")
        if target:
            Path(target).write_text(f"{words} words\\n", encoding="utf-8")''',
          run=False, verify="compile")}
    <p>
      Note that cancelling returns an empty string, not an exception. Handling the cancel case
      is the most commonly forgotten branch in GUI code, and it produces the classic "the app
      crashed when I pressed cancel".
    </p>

    <h2>The rule that keeps a GUI usable</h2>
    {code('''import threading
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
status = ttk.Label(root, text="Ready")
status.pack(padx=20, pady=20)


def slow_work():
    """Runs on a background thread, so the window keeps repainting."""
    import time
    time.sleep(3)
    # Never touch widgets from another thread. Schedule it on the main one:
    root.after(0, lambda: status.config(text="Done"))


def start():
    status.config(text="Working...")
    threading.Thread(target=slow_work, daemon=True).start()


ttk.Button(root, text="Start", command=start).pack(pady=(0, 20))
root.mainloop()''',
          run=False, verify="compile")}

    {voice("PARANOIA", "Formidable: Success",
           "Anything slow on the main thread freezes the window. No repainting, no response to "
           "clicks, and after a few seconds the operating system helpfully offers to kill your "
           "application.",
           "So: slow work on a thread, and results back to the main thread via root.after. "
           "tkinter is not thread-safe, and updating a widget from a background thread will "
           "corrupt it in ways that look like haunting rather than like a bug.")}

    <h2>Other options</h2>
    {table(
        ["Toolkit", "Trade"],
        [["<strong>tkinter</strong>", "Built in, everywhere, a bit dated. Perfect for small tools"],
         ["<strong>PySide6</strong> / <strong>PyQt</strong>", "Professional and vast. Qt licensing matters for PyQt; PySide6 is LGPL"],
         ["<strong>Kivy</strong>", "Touch and mobile, custom look"],
         ["<strong>Flet</strong>", "Flutter-based, modern-looking, quite new"],
         ["<strong>A local web app</strong>", "Honestly often the best answer: FastAPI plus a browser page (Lesson 44)"]],
    )}
    {callout("info", "📦 Shipping a desktop app to someone who has no Python",
             "<p>This is Python's weakest spot, and Base Camp 4 said so. The tools are "
             "<a href='https://pyinstaller.org' target='_blank' rel='noopener'>PyInstaller</a> "
             "and <a href='https://briefcase.readthedocs.io' target='_blank' rel='noopener'>Briefcase</a>: "
             "they bundle the interpreter and your code into one executable. Expect a 30 to "
             "80MB file, some antivirus false positives, and a genuinely fiddly first attempt. "
             "It works, but a compiled language earns its keep here.</p>")}

    {exercise(1, "A unit converter",
              "<p>Build a window with an entry, a dropdown of conversions, and a result label. "
              "Handle bad input without crashing.</p>",
              code('''import tkinter as tk
from tkinter import ttk

CONVERSIONS = {
    "Celsius to Fahrenheit": lambda c: c * 9 / 5 + 32,
    "Fahrenheit to Celsius": lambda f: (f - 32) * 5 / 9,
    "Kilometres to Miles": lambda km: km * 0.621371,
    "Miles to Kilometres": lambda mi: mi / 0.621371,
}

root = tk.Tk()
root.title("Converter")

value = tk.StringVar()
choice = tk.StringVar(value=list(CONVERSIONS)[0])
result = tk.StringVar(value="-")

frame = ttk.Frame(root, padding=16)
frame.grid(sticky="nsew")

ttk.Entry(frame, textvariable=value, width=16).grid(row=0, column=0, padx=4)
ttk.Combobox(frame, textvariable=choice, values=list(CONVERSIONS),
             state="readonly", width=24).grid(row=0, column=1, padx=4)
ttk.Label(frame, textvariable=result, font=("Helvetica", 16)).grid(
    row=1, column=0, columnspan=2, pady=12)


def convert(*_):
    try:
        number = float(value.get())
    except ValueError:
        result.set("Enter a number" if value.get() else "-")
        return
    result.set(f"{CONVERSIONS[choice.get()](number):.2f}")


value.trace_add("write", convert)      # convert as they type
choice.trace_add("write", convert)

root.mainloop()''',
                   run=False, verify="compile")
              + "<p><code>trace_add</code> reacts to the variable changing, so the result "
              "updates live with no Convert button at all. Removing a button is usually better "
              "interface design than adding one.</p>")}

    {exercise(2, "Why did it freeze?",
              "<p>A user clicks Download and the window goes white and stops responding. What "
              "happened, and what are the two fixes?</p>",
              "<p>The download is running on the main thread, so <code>mainloop()</code> never "
              "gets a chance to process events, including 'repaint yourself'. The operating "
              "system sees an application that has not responded and greys it out.</p>"
              "<p><strong>Fix one:</strong> run the work on a background thread and send "
              "results back with <code>root.after(0, ...)</code>, as in the example above. "
              "This is right for network and disk work.</p>"
              "<p><strong>Fix two:</strong> break the work into small chunks and schedule each "
              "with <code>root.after(10, next_chunk)</code>, so the loop runs between pieces. "
              "This suits work you can naturally divide, and avoids threads entirely.</p>"
              "<p>Either way, show progress. A frozen window and a slow window look identical "
              "to the user; a progress bar is the difference between 'broken' and "
              "'working'.</p>")}

    {exercise(3, "CLI, GUI or web?",
              "<p>For each, which interface would you build, and why?</p>"
              "<ol><li>A tool you run every morning to tidy your downloads.</li>"
              "<li>A tool for your non-technical colleague to rename photo batches.</li>"
              "<li>A dashboard the whole team needs to see.</li>"
              "<li>A step in an automated build pipeline.</li></ol>",
              "<ol><li><strong>CLI.</strong> You can schedule it (Lesson 41), and it needs no "
              "clicking.</li>"
              "<li><strong>GUI.</strong> Asking a non-programmer to open a terminal is asking "
              "them not to use your tool. tkinter, one window, a folder picker and a big "
              "button.</li>"
              "<li><strong>Web.</strong> No installation, works on any device, one deployment "
              "to update. Lesson 44.</li>"
              "<li><strong>CLI,</strong> with proper exit codes (Lesson 27). A pipeline cannot "
              "click anything.</li></ol>"
              "<p>The underlying question is always 'who is holding the mouse, and where are "
              "they'. Choosing the interface before writing the logic saves rewriting the "
              "logic.</p>")}
""",
)

# ---------------------------------------------------------------- 50
_add(
    level=5,
    num="50",
    slug="50-packaging",
    id="py-50-packaging",
    card="Turn your code into something other people can install, with tests running automatically.",
    title="Packaging and Shipping",
    emoji="📦",
    desc="pyproject.toml, building a package, publishing to PyPI, semantic versioning and GitHub Actions.",
    lede="""The final step from 'a folder of scripts' to 'a thing that exists in the world and
    someone else can pip install'.""",
    body=f"""
    <h2>The shape of a package</h2>
    {out("""crew-manager/
├── pyproject.toml          the one config file that matters
├── README.md               what it is, shown on PyPI
├── LICENSE                 without one, nobody may legally use it
├── .gitignore
├── src/
│   └── crew_manager/
│       ├── __init__.py     makes it a package; holds the version
│       ├── core.py
│       └── cli.py
└── tests/
    ├── test_core.py
    └── test_cli.py""")}
    {callout("tip", "📁 Why src/",
             "<p>Putting the package inside <code>src/</code> means your tests cannot "
             "accidentally import the local folder instead of the installed package. That "
             "sounds pedantic until the day your tests pass locally and the published package "
             "is missing a file nobody noticed. This is called the src layout and it is the "
             "current recommendation.</p>")}

    <h2>pyproject.toml</h2>
    {code('''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "crew-manager"
version = "0.1.0"
description = "Manage a pirate crew from the command line."
readme = "README.md"
requires-python = ">=3.11"
license = "MIT"
authors = [{ name = "Your Name" }]
keywords = ["cli", "pirates"]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
dependencies = [
    "rich>=13.0",
]

[project.optional-dependencies]
dev = ["pytest>=8.0", "ruff>=0.6", "mypy>=1.10"]

[project.scripts]
crew = "crew_manager.cli:main"

[project.urls]
Homepage = "https://github.com/you/crew-manager"
Issues = "https://github.com/you/crew-manager/issues"''',
          run=False, verify="skip")}
    <p>
      That <code>[project.scripts]</code> line is the good bit: after installing, the user gets
      a <code>crew</code> command on their PATH that calls your <code>main</code> function. It
      is how <code>pytest</code>, <code>ruff</code> and <code>pip</code> itself are installed.
    </p>

    <h2>Installing your own package while you work on it</h2>
    {term("""$ python3 -m venv .venv && source .venv/bin/activate
$ pip install -e ".[dev]"

Successfully installed crew-manager-0.1.0 (editable)

$ crew --help
usage: crew [-h] {add,list,remove} ...""")}
    <p>
      <code>-e</code> means editable: the package is installed as a link to your source, so
      your edits take effect immediately with no reinstall. <code>.[dev]</code> also pulls in
      the optional development dependencies. This is the first command to run in any Python
      project you clone.
    </p>

    <h2>Building and publishing</h2>
    {term("""$ pip install build twine
$ python -m build

Successfully built crew_manager-0.1.0.tar.gz and
                   crew_manager-0.1.0-py3-none-any.whl

# ALWAYS publish to the test index first
$ twine upload --repository testpypi dist/*
$ pip install --index-url https://test.pypi.org/simple/ crew-manager

# then, when you are sure
$ twine upload dist/*""")}
    {table(
        ["File", "What it is"],
        [["<code>.whl</code> (wheel)", "The built package. Fast to install: it is just unpacked"],
         ["<code>.tar.gz</code> (sdist)", "The source. A fallback when a wheel does not fit the platform"]],
    )}
    {callout("danger", "🔒 Use a token, not your password",
             "<p>Create a PyPI API token scoped to the single project, and store it in "
             "<code>~/.pypirc</code> or a CI secret. Better still, use "
             "<a href='https://docs.pypi.org/trusted-publishers/' target='_blank' rel='noopener'>trusted publishing</a>, "
             "which lets GitHub Actions publish with no long-lived secret at all.</p>"
             "<p>And note: <strong>a version once published can never be replaced.</strong> "
             "You can only yank it and publish a new number. Test on TestPyPI first, every "
             "time.</p>")}

    <h2>Version numbers mean something</h2>
    {table(
        ["Change", "Bump", "Example"],
        [["Broke something that used to work", "<strong>MAJOR</strong>", "1.4.2 → 2.0.0"],
         ["Added something, nothing broke", "<strong>MINOR</strong>", "1.4.2 → 1.5.0"],
         ["Fixed a bug, no interface change", "<strong>PATCH</strong>", "1.4.2 → 1.4.3"],
         ["Still working it out", "0.x", "0.1.0. Anything may change"]],
    )}
    <p>
      This is {link("semantic versioning", "https://semver.org")}, and it is a promise to the
      people installing your package. Breaking it, by changing behaviour in a patch release, is
      the fastest way to lose users' trust, because their code broke while they were doing
      nothing wrong.
    </p>

    <h2>Automating the checks</h2>
    {code('''# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12", "3.13"]

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install
        run: pip install -e ".[dev]"

      - name: Lint
        run: ruff check .

      - name: Format check
        run: ruff format --check .

      - name: Type check
        run: mypy src

      - name: Test
        run: pytest -v''',
          run=False, verify="skip")}
    <p>
      Every push now runs your tests on three Python versions, on a clean machine, before you
      can merge. That last part is the real value: it catches "works on my machine" the moment
      it happens, and it proves your package installs from scratch.
    </p>

    {voice("VOLITION", "Formidable: Success",
           "Publishing something, even something small, changes how you write code. You "
           "suddenly care about the interface, because changing it will inconvenience "
           "strangers.",
           "It is also a rite of passage. Your name on a package that anyone in the world can "
           "install is a genuinely different feeling from a folder of scripts, and it is worth "
           "doing once even if nobody but you ever installs it.")}

    <h2>Before you publish anything</h2>
    <ul class="checklist">
      <li>A README that shows installation and one working example in the first screen</li>
      <li>A LICENSE file. Without one, the legal default is that nobody may use it</li>
      <li>Tests that pass on a clean machine, not just yours</li>
      <li>A name nobody has taken, checked on PyPI</li>
      <li><code>requires-python</code> set honestly</li>
      <li>Version 0.1.0, not 1.0.0, unless you mean it</li>
      <li>No secrets, no API keys, no personal paths in the source</li>
      <li>Uploaded to TestPyPI and installed from there successfully</li>
    </ul>

    {exercise(1, "Package something you have written",
              "<p>Take any script from this course, give it the layout above, and install it "
              "editable with a console command.</p>",
              code('''# src/wordtools/__init__.py
"""Small text statistics helpers."""

__version__ = "0.1.0"

from .core import word_count, most_common

__all__ = ["word_count", "most_common"]''', run=False, verify="compile")
              + code('''# src/wordtools/cli.py
"""Command-line entry point."""

import argparse
import sys
from pathlib import Path

from .core import most_common, word_count


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="wordtools")
    parser.add_argument("file", type=Path)
    parser.add_argument("-n", "--top", type=int, default=3)
    args = parser.parse_args(argv)

    try:
        text = args.file.read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"wordtools: no such file: {args.file}", file=sys.stderr)
        return 1

    print(f"{word_count(text)} words")
    for word, count in most_common(text, args.top):
        print(f"  {count:4}  {word}")
    return 0


if __name__ == "__main__":
    sys.exit(main())''', run=False, verify="compile")
              + term("""pip install -e ".[dev]"
wordtools README.md --top 5""")
              + "<p>With <code>[project.scripts] wordtools = \"wordtools.cli:main\"</code> in "
              "pyproject.toml, that command now exists on your PATH. You have built a real "
              "tool.</p>")}

    {exercise(2, "Which version number?",
              "<p>You are at 2.3.1. What is the next version for each change?</p>"
              "<ol><li>Fixed a crash on empty input.</li>"
              "<li>Added an optional <code>--verbose</code> flag.</li>"
              "<li>Renamed a function everyone uses.</li>"
              "<li>Made an argument required that used to be optional.</li>"
              "<li>Rewrote the internals, identical behaviour, three times faster.</li></ol>",
              "<ol><li><strong>2.3.2.</strong> Patch.</li>"
              "<li><strong>2.4.0.</strong> Minor: new feature, nothing broken.</li>"
              "<li><strong>3.0.0.</strong> Major. Even with an alias left behind, it is a "
              "breaking change to the documented interface.</li>"
              "<li><strong>3.0.0.</strong> Major. Every existing call now fails, which is the "
              "definition of breaking.</li>"
              "<li><strong>2.3.2.</strong> Patch, arguably 2.4.0 if the speed is a headline "
              "feature. Users' code does not change either way.</li></ol>"
              "<p>The test is always the same: could someone else's working code break if they "
              "upgrade without reading anything?</p>")}

    {exercise(3, "Read a package's manifest",
              "<p>Look at any package you use on PyPI and find: its licence, its minimum "
              "Python, its dependencies, when it was last released, and whether the source "
              "repository is linked and active. Then say whether you would depend on it.</p>",
              "<p>The signals that matter, roughly in order:</p>"
              "<ul><li><strong>Recent releases</strong> or recent commits. Two years of silence "
              "means you will be maintaining it.</li>"
              "<li><strong>A permissive licence</strong> (MIT, BSD, Apache) unless you have "
              "checked that a copyleft one suits your use.</li>"
              "<li><strong>Few dependencies of its own.</strong> Every one is a package you are "
              "also trusting, transitively.</li>"
              "<li><strong>Issues being answered,</strong> even if not always fixed.</li>"
              "<li><strong>A name that is not one typo away</strong> from a much more popular "
              "package (Lesson 26).</li></ul>"
              "<p>Adding a dependency is a decision with a maintenance cost, not a free win. "
              "The standard library remains the safest dependency you will ever have.</p>")}
""",
)

# ---------------------------------------------------------------- 51
_add(
    level=5,
    num="51",
    slug="51-performance",
    id="py-51-performance",
    card="Measure first, then fix the right thing, and know when to call Rust.",
    title="Making Python Fast",
    emoji="⚡",
    desc="Profiling with timeit and cProfile, algorithmic complexity, practical speedups, and calling Rust from Python.",
    lede="""Python is slow, in the way a bicycle is slow. Most of the time the route matters
    more than the vehicle, and this lesson is about finding the route.""",
    body=f"""
    <h2>The rule: measure, do not guess</h2>
    {code('''import timeit

setup = "data = list(range(1000))"

loop = timeit.timeit("total = 0\\nfor n in data: total += n", setup=setup, number=1000)
builtin = timeit.timeit("total = sum(data)", setup=setup, number=1000)

print(f"explicit loop faster than sum? {loop < builtin}")
print(f"sum is at least twice as fast: {loop / builtin > 2}")''',
          expect="""explicit loop faster than sum? False
sum is at least twice as fast: True""")}
    <p>
      Note what is being asserted there: a direction, not a number. The exact ratio depends on
      your machine, your Python version and what else is running, so a lesson that promised
      "4.7 times faster" would be wrong for most readers. Benchmarks you publish should claim
      only what they can defend.
    </p>

    {voice("LOGIC", "Formidable: Success",
           "Programmers are famously bad at guessing where time goes. Decades of experience "
           "produce confident, wrong answers, because the bottleneck is nearly always "
           "somewhere unglamorous: a repeated lookup, an accidental quadratic, a call inside a "
           "loop that could be outside it.",
           "Donald Knuth's line about premature optimisation is usually quoted as a joke about "
           "laziness. The full sentence is an argument for measurement: he says we should "
           "forget small efficiencies about 97% of the time, and then adds that we should not "
           "pass up the critical 3%. Finding the 3% requires a profiler.")}

    <h2>cProfile: where the time actually goes</h2>
    {code('''import cProfile
import io
import pstats


def slow_lookup(names, targets):
    """Deliberately quadratic: a list scan inside a loop."""
    return [name for name in targets if name in names]


def fast_lookup(names, targets):
    lookup = set(names)
    return [name for name in targets if name in lookup]


names = [f"pirate{i}" for i in range(4000)]
targets = [f"pirate{i}" for i in range(0, 4000, 4)]

profiler = cProfile.Profile()
profiler.enable()
slow = slow_lookup(names, targets)
fast = fast_lookup(names, targets)
profiler.disable()

buffer = io.StringIO()
pstats.Stats(profiler, stream=buffer).sort_stats("cumulative").print_stats(0)

print("same answer:", slow == fast)
print("matched:", len(fast))''',
          expect="""same answer: True
matched: 1000""")}
    {term("""$ python -m cProfile -s cumulative myscript.py | head -15

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    2.417    2.417 myscript.py:1(<module>)
        1    2.301    2.301    2.301    2.301 myscript.py:4(slow_lookup)
        1    0.004    0.004    0.004    0.004 myscript.py:9(fast_lookup)""")}
    <p>
      <code>tottime</code> is time inside that function alone; <code>cumtime</code> includes
      everything it called. Sort by cumulative to find the expensive branch, then by tottime to
      find the expensive line. One command, and the guessing stops.
    </p>

    <h2>Algorithms beat micro-optimisation, always</h2>
    {code('''import time

names = [f"pirate{i}" for i in range(20000)]
targets = [f"pirate{i}" for i in range(0, 20000, 2)]

start = time.perf_counter()
slow = [n for n in targets if n in names]          # list: scans every time
slow_time = time.perf_counter() - start

lookup = set(names)
start = time.perf_counter()
fast = [n for n in targets if n in lookup]         # set: instant
fast_time = time.perf_counter() - start

print(f"same result: {slow == fast}")
print(f"set version at least 20x faster: {slow_time / fast_time > 20}")''',
          expect="""same result: True
set version at least 20x faster: True""")}
    {table(
        ["Operation", "list", "set / dict"],
        [["<code>x in collection</code>", "O(n): checks every item", "O(1): effectively instant"],
         ["append / add", "O(1)", "O(1)"],
         ["<code>collection[i]</code>", "O(1)", "n/a (dict by key is O(1))"],
         ["insert at the front", "O(n)", "use <code>collections.deque</code>"]],
    )}
    <p>
      That table is worth more than every micro-optimisation in this lesson combined. A loop
      inside a loop over the same data is the accidental quadratic, and it is the single most
      common cause of "it was fine in testing and unusable in production".
    </p>

    <h2>The practical speedups, in order of value</h2>
    {code('''import time

# 1. Do less work: move invariant things out of the loop
data = list(range(20000))

start = time.perf_counter()
result_bad = [x * len(data) for x in data]           # len() every iteration
bad = time.perf_counter() - start

start = time.perf_counter()
size = len(data)
result_good = [x * size for x in data]
good = time.perf_counter() - start

print("same:", result_bad == result_good)

# 2. Build strings with join, not +=
start = time.perf_counter()
text = ""
for i in range(20000):
    text += str(i)            # a new string every time
concat = time.perf_counter() - start

start = time.perf_counter()
joined = "".join(str(i) for i in range(20000))
join = time.perf_counter() - start

print("same text:", text == joined)
print("join at least as fast:", join <= concat * 1.5)''',
          expect="""same: True
same text: True
join at least as fast: True""")}
    <ol>
      <li><strong>Pick the right data structure.</strong> Sets and dicts for lookup. Usually a
      100x win or more.</li>
      <li><strong>Do less.</strong> Cache with <code>functools.lru_cache</code>, hoist
      invariants out of loops, and stop computing things nobody reads.</li>
      <li><strong>Use the built-ins.</strong> <code>sum</code>, <code>min</code>,
      <code>sorted</code>, <code>any</code> and <code>str.join</code> run in C.</li>
      <li><strong>Use generators</strong> when you do not need the whole list (Lesson 34).</li>
      <li><strong>Reach for NumPy</strong> for numeric arrays. Often 50x, sometimes far more
      (Lesson 46).</li>
      <li><strong>Then consider concurrency</strong> (Lessons 39 and 40), which helps waiting,
      not computing.</li>
      <li><strong>Then a faster language</strong> for the one function that matters.</li>
    </ol>

    <h2>Free speed from newer Pythons</h2>
    <p>
      Python has been getting substantially faster. The
      {link("Faster CPython", "https://github.com/faster-cpython")} project delivered large
      gains in 3.11, more in 3.12 and 3.13, and 3.14 continues. Upgrading is often the cheapest
      performance work available: no code changes, and a benchmark suite you did not have to
      write.
    </p>
    {term("""$ python3.11 bench.py
2.41s

$ python3.13 bench.py
1.52s

# the same code, no changes""")}

    <h2>When Python genuinely is not enough</h2>
    {table(
        ["Option", "Effort", "Typical gain"],
        [["Upgrade Python", "Minutes", "10 to 60%"],
         ["<code>functools.cache</code>", "One line", "Unbounded, if there is repetition"],
         ["NumPy for arrays", "A rewrite of that section", "10 to 100x"],
         ["<a href='https://docs.python.org/3/library/multiprocessing.html'>multiprocessing</a>", "Moderate", "Up to the number of cores"],
         ["<a href='https://cython.org' target='_blank' rel='noopener'>Cython</a>", "Annotate a hot function", "10 to 100x"],
         ["<a href='https://numba.pydata.org' target='_blank' rel='noopener'>Numba</a>", "One decorator, numeric code only", "10 to 100x"],
         ["Rewrite the hot function in Rust", "A day, plus learning", "10 to 200x"]],
    )}

    <h2>Calling Rust from Python</h2>
    <p>
      This is the pattern behind the fastest tools in the Python ecosystem, and it is much more
      approachable than it sounds. You write the 5% that is slow in Rust and import it as an
      ordinary Python module.
    </p>
    {code('''// src/lib.rs
use pyo3::prelude::*;

/// Count how many numbers below `limit` are prime.
#[pyfunction]
fn count_primes(limit: u64) -> u64 {
    (2..limit)
        .filter(|n| (2..=(*n as f64).sqrt() as u64).all(|d| n % d != 0))
        .count() as u64
}

#[pymodule]
fn fastmath(m: &Bound<\'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(count_primes, m)?)?;
    Ok(())
}''', run=False, verify="skip")}
    {code('''# and then, from Python
import fastmath

print(fastmath.count_primes(1_000_000))      # the same answer, dramatically faster''',
          run=False, verify="compile")}
    {term("""$ pip install maturin
$ maturin init --bindings pyo3
$ maturin develop          # builds the Rust and installs it into your venv""")}
    {callout("info", "🦀 This is not a hypothetical",
             "<p><a href='https://github.com/astral-sh/ruff' target='_blank' rel='noopener'>ruff</a> "
             "replaced a stack of Python linters and is 10 to 100 times faster. "
             "<a href='https://github.com/astral-sh/uv' target='_blank' rel='noopener'>uv</a> "
             "did the same to pip. "
             "<a href='https://pola.rs' target='_blank' rel='noopener'>Polars</a> is doing it to "
             "pandas. <a href='https://docs.pydantic.dev' target='_blank' rel='noopener'>Pydantic</a> "
             "moved its core to Rust in version 2. All of them are used from Python, by Python "
             "programmers, who mostly never look at the Rust.</p>"
             "<p>If that appeals, the <a href='../../learn/index.html'>Rusty School</a> is next "
             "door and teaches Rust from the same starting point as this course. Python plus "
             "Rust is an unusually strong pair of languages to know.</p>")}

    {exercise(1, "Find the bottleneck",
              "<p>This function is slow. Profile it mentally, then fix it, then prove the "
              "fix.</p>"
              + code('''def find_duplicates(records):
    duplicates = []
    for record in records:
        count = 0
        for other in records:
            if record["id"] == other["id"]:
                count += 1
        if count > 1 and record["id"] not in [d["id"] for d in duplicates]:
            duplicates.append(record)
    return duplicates''', run=False, verify="compile"),
              "<p>Three nested scans: the inner loop over all records, and a third scan of "
              "<code>duplicates</code> rebuilt on every iteration. That is O(n²) at best.</p>"
              + code('''from collections import Counter
import time


def find_duplicates_fast(records):
    """One pass to count, one pass to collect. O(n)."""
    counts = Counter(r["id"] for r in records)
    seen = set()
    result = []
    for record in records:
        if counts[record["id"]] > 1 and record["id"] not in seen:
            seen.add(record["id"])
            result.append(record)
    return result


records = [{"id": i % 500, "name": f"r{i}"} for i in range(4000)]

start = time.perf_counter()
fast = find_duplicates_fast(records)
elapsed = time.perf_counter() - start

print(f"{len(fast)} duplicate ids found")
print(f"fast enough: {elapsed < 0.1}")''',
                     expect="""500 duplicate ids found
fast enough: True""")
              + "<p>The shape to recognise: any time you write a loop inside a loop over the "
              "same data, ask whether a <code>Counter</code>, a <code>set</code> or a "
              "<code>dict</code> would let you do it in one pass.</p>")}

    {exercise(2, "Cache the expensive call",
              "<p>Use <code>functools.cache</code> to make a repeated calculation instant, and "
              "prove it worked.</p>",
              code('''import functools
import time


@functools.cache
def expensive(n):
    """Pretend this is a slow API call or a heavy computation."""
    total = sum(i * i for i in range(n))
    return total


start = time.perf_counter()
first = expensive(200_000)
first_time = time.perf_counter() - start

start = time.perf_counter()
second = expensive(200_000)
second_time = time.perf_counter() - start

print(f"same answer: {first == second}")
print(f"second call much faster: {second_time < first_time / 10}")
print(expensive.cache_info().hits, "cache hit")''',
                   expect="""same answer: True
second call much faster: True
1 cache hit""")
              + "<p>The caveats matter: arguments must be hashable, the function must be pure "
              "(Lesson 37), and an unbounded cache is a memory leak with good manners. Use "
              "<code>lru_cache(maxsize=1000)</code> when the input space is large.</p>")}

    {exercise(3, "Decide whether to optimise",
              "<p>A report takes 45 seconds. Should you optimise it? What do you need to know "
              "first?</p>",
              "<ul>"
              "<li><strong>How often does it run?</strong> Once a month at 3am: leave it. Forty "
              "times a day while a person waits: fix it.</li>"
              "<li><strong>Where do the 45 seconds go?</strong> Profile. If 43 of them are "
              "waiting on a database, no amount of Python tuning will help; the query or its "
              "indexes are the problem (Lesson 45).</li>"
              "<li><strong>Is it blocking anyone?</strong> A background job that nobody waits "
              "for has a very different cost than a page load.</li>"
              "<li><strong>What would the fix cost?</strong> Two days of work and permanent "
              "extra complexity, to save a person four seconds a week, is a bad trade and "
              "worth saying out loud.</li>"
              "<li><strong>Is there a free win?</strong> A newer Python, one index, or one "
              "<code>@cache</code> is worth trying before a rewrite.</li>"
              "</ul>"
              "<p>Optimisation is an engineering decision, not a reflex. The correct answer is "
              "often 'no, and here is the measurement that says so'.</p>")}
""",
)

# ---------------------------------------------------------------- 52
_add(
    level=5,
    num="52",
    slug="52-security",
    id="py-52-security",
    card="Secrets, hashing, injection, pickle, and the supply chain. The things that actually bite.",
    title="Security Basics",
    emoji="🔐",
    desc="Handling secrets, hashing passwords properly, avoiding injection, the dangers of pickle and eval, and dependency risk.",
    lede="""You do not need to be a security expert. You do need to not make the six mistakes
    that account for most of the damage, and they are all avoidable in one line each.""",
    body=f"""
    <h2>1. Secrets never go in code</h2>
    {code('''# WRONG, and it is now in your git history forever
API_KEY = "sk-abc123realkeyhere"''', run=False, verify="skip")}
    {code('''import os

# right: from the environment, and it fails loudly if missing
API_KEY = os.environ["OPENAI_API_KEY"]

# or with a default and a clear error
key = os.environ.get("OPENAI_API_KEY")
if not key:
    raise SystemExit("Set OPENAI_API_KEY. See README.")''',
          run=False, verify="compile")}
    {callout("danger", "🚨 git history is forever",
             "<p>Deleting a key in a later commit does not remove it: it is still in the "
             "history, and on every clone. If you push a secret, <strong>revoke it "
             "immediately</strong>, then clean the history if you must. Bots scan public "
             "commits within seconds, and cloud keys have produced five-figure bills "
             "overnight.</p>")}
    {code('''# .gitignore, from the very first commit
.env
*.key
*.pem
secrets.json
.venv/''', run=False, verify="skip")}

    <h2>2. Never store passwords, store hashes</h2>
    {code('''import hashlib
import secrets

# WRONG in three different ways
def terrible(password):
    return password                                   # plain text
def bad(password):
    return hashlib.md5(password.encode()).hexdigest() # broken, and unsalted
def still_wrong(password):
    return hashlib.sha256(password.encode()).hexdigest()  # fast, so brute-forceable


# Acceptable with the standard library only:
def hash_password(password, iterations=600_000):
    """PBKDF2 with a random salt. Slow on purpose."""
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"


def verify_password(password, stored):
    """Check a password against a stored hash, in constant time."""
    algorithm, iterations, salt_hex, digest_hex = stored.split("$")
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations)
    )
    return secrets.compare_digest(digest.hex(), digest_hex)


stored = hash_password("swordfish")
algorithm, iterations, salt, digest = stored.split("$")
print(algorithm, iterations, f"salt={len(salt)} hex chars", f"hash={len(digest)} hex chars")
print(verify_password("swordfish", stored))
print(verify_password("Swordfish", stored))''',
          expect="""pbkdf2_sha256 600000 salt=32 hex chars hash=64 hex chars
True
False""")}
    <p>Three ideas are doing the work there:</p>
    <ul>
      <li><strong>A salt.</strong> Random per password, so identical passwords produce
      different hashes and precomputed rainbow tables are useless.</li>
      <li><strong>Slowness on purpose.</strong> 600,000 iterations costs you a few
      milliseconds and costs an attacker with a stolen database everything.</li>
      <li><strong><code>compare_digest</code>.</strong> Comparing with <code>==</code> returns
      early on the first differing byte, and the timing difference can leak the answer one
      character at a time. This is a real, practical attack.</li>
    </ul>
    {callout("tip", "🔑 In production, use a library",
             "<p><code>argon2-cffi</code> or <code>bcrypt</code>. Argon2 won the Password "
             "Hashing Competition and is memory-hard, which resists GPU cracking in a way "
             "PBKDF2 does not. The code above is correct and is the best you can do without "
             "installing anything; a library is better.</p>")}

    <h2>3. Injection: never build commands from input</h2>
    {code('''import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE users (name TEXT, admin INTEGER)")
conn.execute("INSERT INTO users VALUES ('Guybrush', 0)")

user_input = "' OR '1'='1"

unsafe = conn.execute(f"SELECT * FROM users WHERE name = '{user_input}'").fetchall()
safe = conn.execute("SELECT * FROM users WHERE name = ?", (user_input,)).fetchall()

print("unsafe returned:", len(unsafe), "rows")
print("safe returned:  ", len(safe), "rows")''',
          expect="""unsafe returned: 1 rows
safe returned:   0 rows""")}
    <p>The same rule, in three places:</p>
    {code('''import subprocess

filename = "report.txt; rm -rf ~"

# WRONG: shell=True with interpolated input runs whatever they typed
# subprocess.run(f"cat {filename}", shell=True)

# right: a list of arguments, no shell involved
result = subprocess.run(["echo", filename], capture_output=True, text=True)
print(result.stdout.strip())''',
          expect="report.txt; rm -rf ~")}
    <p>
      Passing a list means the operating system runs <code>echo</code> with one argument that
      happens to contain a semicolon. There is no shell to interpret it, so there is nothing to
      inject into.
    </p>

    <h2>4. eval, exec and pickle are code execution</h2>
    {code('''# Never do this with anything a user can influence
user_input = "2 + 2"
# print(eval(user_input))        # fine here, catastrophic with hostile input

# because this also "works":
# eval("__import__('os').system('rm -rf ~')")

# The safe way to evaluate a literal:
import ast
print(ast.literal_eval("[1, 2, {'a': 3}]"))

try:
    ast.literal_eval("__import__('os')")
except ValueError as err:
    print("refused:", type(err).__name__)''',
          expect="""[1, 2, {'a': 3}]
refused: ValueError""")}
    {callout("danger", "🥒 pickle is not a data format, it is a program format",
             "<p>Unpickling data executes code contained in it. Loading a pickle from an "
             "untrusted source is equivalent to running a script from that source. The official "
             "documentation says so in a red box. Use JSON for anything crossing a trust "
             "boundary, and reserve pickle for data your own program wrote and only your own "
             "program reads.</p>")}
    {code('''import json

# JSON can only describe data, so parsing it can never execute anything
print(json.loads('{"name": "Guybrush", "insults": 8}'))

try:
    json.loads("__import__('os')")
except json.JSONDecodeError:
    print("JSON refuses to parse code. That is the feature.")''',
          expect="""{'name': 'Guybrush', 'insults': 8}
JSON refuses to parse code. That is the feature.""")}

    <h2>5. Randomness: the right module matters</h2>
    {code('''import random
import secrets

random.seed(42)
print("predictable:", random.randint(1000, 9999))
random.seed(42)
print("predictable:", random.randint(1000, 9999))      # same again

print("token:", len(secrets.token_urlsafe(32)))
print("choice from a set:", secrets.choice(["a", "b", "c"]) in {"a", "b", "c"})''',
          expect="""predictable: 2824
predictable: 2824
token: 43
choice from a set: True""")}
    <p>
      <code>random</code> is a Mersenne Twister: excellent statistically, and completely
      predictable once you have seen enough output. Its own documentation says it must not be
      used for security. Password reset tokens, session ids, API keys and one-time codes all
      need <code>secrets</code>.
    </p>

    <h2>6. Your dependencies are your attack surface</h2>
    {term("""# check what you have installed against known vulnerabilities
$ pip install pip-audit
$ pip-audit

Found 2 known vulnerabilities in 1 package
Name    Version  ID                  Fix Versions
------- -------- ------------------- ------------
requests 2.19.1  GHSA-x84v-xcm2-53pg 2.31.0""")}
    <ul>
      <li><strong>Pin versions</strong> so an upgrade cannot happen without you noticing.</li>
      <li><strong>Audit regularly.</strong> <code>pip-audit</code> is free and takes seconds;
      GitHub's Dependabot does it automatically on a repository.</li>
      <li><strong>Check names character by character.</strong> Typosquatted packages on PyPI
      are a real and ongoing attack.</li>
      <li><strong>Fewer dependencies is fewer risks.</strong> The standard library is the
      safest dependency you have.</li>
    </ul>

    {voice("PARANOIA", "Medium: Success",
           "You will notice none of this required cryptography knowledge. Six habits: secrets "
           "in the environment, hashes not passwords, parameters not string building, JSON not "
           "pickle, secrets not random, and audited dependencies.",
           "That is not everything. It is the part that accounts for most of the damage done to "
           "small projects, and every one of them is a single line of difference.")}

    <h2>The checklist</h2>
    <ul class="checklist">
      <li>No secrets in code, and <code>.env</code> in <code>.gitignore</code> from commit one</li>
      <li>Passwords hashed with argon2, bcrypt or PBKDF2, never stored or reversibly encrypted</li>
      <li>Parameterised queries everywhere; no SQL built with f-strings</li>
      <li><code>subprocess</code> with a list, never <code>shell=True</code> with user input</li>
      <li>No <code>eval</code>, <code>exec</code> or <code>pickle</code> on untrusted data</li>
      <li><code>secrets</code>, not <code>random</code>, for anything security-related</li>
      <li>Template escaping left on; no HTML built from user input by hand</li>
      <li>Dependencies pinned and audited</li>
      <li>Errors logged, not shown to users with a full traceback</li>
      <li>HTTPS everywhere, and certificate verification never disabled</li>
    </ul>

    {exercise(1, "Audit this login code",
              "<p>Find five problems.</p>"
              + code('''import hashlib

USERS = {"guybrush": "5f4dcc3b5aa765d61d8327deb882cf99"}


def login(username, password):
    hashed = hashlib.md5(password.encode()).hexdigest()
    if username in USERS and USERS[username] == hashed:
        return True
    print(f"Failed login for {username} with password {password}")
    return False''', run=False, verify="compile"),
              "<ol><li><strong>MD5.</strong> Cryptographically broken, and far too fast for "
              "password hashing regardless.</li>"
              "<li><strong>No salt.</strong> That hash is the well-known MD5 of 'password'; "
              "identical passwords produce identical hashes across every user and every "
              "site.</li>"
              "<li><strong>The password is logged in plain text</strong> on failure. Now your "
              "log file is a credential dump, and users type their real password into the wrong "
              "box constantly.</li>"
              "<li><strong><code>==</code> for hash comparison</strong> is not constant time. "
              "Use <code>secrets.compare_digest</code>.</li>"
              "<li><strong>The error distinguishes cases</strong> if you extend it: 'no such "
              "user' versus 'wrong password' tells an attacker which usernames exist. Say "
              "'invalid username or password' for both.</li></ol>"
              "<p>Bonus: no rate limiting, so an attacker may try as fast as the network "
              "allows.</p>")}

    {exercise(2, "Make the config loader safe",
              "<p>This reads a config file. Make it safe against hostile input while keeping "
              "the feature.</p>"
              + code('''def load_config(path):
    with open(path) as f:
        return eval(f.read())''', run=False, verify="compile"),
              code('''import ast
import json
from pathlib import Path


def load_config(path):
    """Load a config file. JSON first, then a Python literal, never eval."""
    text = Path(path).read_text(encoding="utf-8")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    try:
        return ast.literal_eval(text)      # data only: no calls, no imports
    except (ValueError, SyntaxError) as err:
        raise ValueError(f"{path} is not valid JSON or a Python literal") from err


Path("config.json").write_text('{"ship": "Sea Monkey", "crew": 12}', encoding="utf-8")
Path("config.py").write_text("{'ship': 'Sea Monkey', 'crew': 12}", encoding="utf-8")

print(load_config("config.json"))
print(load_config("config.py"))

Path("evil.py").write_text("__import__('os').getcwd()", encoding="utf-8")
try:
    load_config("evil.py")
except ValueError as err:
    print("refused:", err)''',
                   expect="""{'ship': 'Sea Monkey', 'crew': 12}
{'ship': 'Sea Monkey', 'crew': 12}
refused: evil.py is not valid JSON or a Python literal""")
              + "<p><code>ast.literal_eval</code> parses the same syntax but only permits "
              "literals: strings, numbers, tuples, lists, dicts, sets, booleans and None. There "
              "is no way to express a function call, so there is nothing to exploit.</p>")}

    {exercise(3, "Threat model a small app",
              "<p>You built a web app where users upload a CSV and get a chart back. List what "
              "could go wrong.</p>",
              "<ul>"
              "<li><strong>A 10GB upload</strong> fills the disk. Limit the size before "
              "reading.</li>"
              "<li><strong>A zip bomb or a CSV with a billion columns</strong> exhausts memory. "
              "Stream, and cap rows and columns.</li>"
              "<li><strong>A filename like <code>../../etc/passwd</code></strong> escapes your "
              "upload folder. Never trust an uploaded filename: generate your own.</li>"
              "<li><strong>CSV injection.</strong> A cell starting with <code>=</code> becomes "
              "a formula when the output is opened in Excel, and can exfiltrate data. Prefix "
              "suspicious cells with an apostrophe on export.</li>"
              "<li><strong>Slow requests as a denial of service.</strong> One user uploading "
              "large files repeatedly starves everyone. Rate limit, and process out of "
              "band.</li>"
              "<li><strong>Uploaded data left on disk</strong> containing someone's personal "
              "information. Delete it, and know your retention obligations.</li>"
              "<li><strong>Errors leaking tracebacks</strong> with file paths and library "
              "versions. Log the detail, show the user a reference number.</li>"
              "</ul>"
              "<p>This exercise is threat modelling, and it is mostly just asking 'what does "
              "the worst possible user do here' for each input. Doing it on paper for ten "
              "minutes finds more real issues than any scanner.</p>")}

    {callout("info", "🎉 That is Level 5",
             "<p>Automation, HTTP, scraping, web apps, databases, data, charts, games, desktop "
             "apps, packaging, performance and security. You have now seen the whole landscape "
             "of what Python is used for. Level 6 builds one thing properly with all of it: "
             "your own AI assistant.</p>")}
""",
)
