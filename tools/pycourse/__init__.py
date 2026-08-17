"""The Python School: curriculum registry and page assembly.

Lesson content lives in level_0.py through level_6.py. Everything else
(home page, setup lab, playground, quizzes, the Snake Pit, the Insult
Compiler, the workshop) lives in pages.py, pit.py, insults.py,
quizzes.py, workshop.py, glossary.py and cheatsheets.py.

This file's only job is to stitch them together and hand pybuild.py a
list of (path, html) pairs.
"""

from __future__ import annotations

import importlib

from .kit import SITE, page

LEVELS = {
    0: ("Level 0 · Base Camp", "l0", "Base Camp",
        "Never written a line of code? Start here. No Python yet, and that is on purpose."),
    1: ("Level 1 · First Words", "l1", "Lesson",
        "The whole language in miniature: values, names, decisions, repetition."),
    2: ("Level 2 · The Toolbox", "l2", "Lesson",
        "Lists, dictionaries and functions: where Python starts feeling like a superpower."),
    3: ("Level 3 · Real Programs", "l3", "Lesson",
        "Files, errors, testing, packaging: the difference between a script and software."),
    4: ("Level 4 · Pythonic", "l4", "Lesson",
        "Objects, generators, decorators: the idioms that make Python code look like Python."),
    5: ("Level 5 · In the Wild", "l5", "Lesson",
        "Automation, the web, data, games, hardware: what people actually build."),
    6: ("Level 6 · Build Your Own Jarvis", "l6", "Lesson",
        "The capstone track: assemble a private AI assistant you own end to end."),
}

LEVEL_MODULES = [
    "level_0", "level_1", "level_2", "level_3", "level_4", "level_5", "level_6",
]


def load_lessons() -> list[dict]:
    """Collect every lesson, in curriculum order, filling in defaults."""
    lessons: list[dict] = []
    for mod_name in LEVEL_MODULES:
        try:
            mod = importlib.import_module(f".{mod_name}", package=__name__)
        except ModuleNotFoundError:
            continue  # a level still being written
        lessons.extend(getattr(mod, "LESSONS", []))

    numbered = [l for l in lessons if l["level"] > 0]
    for i, lesson in enumerate(lessons):
        level_label, level_class, noun, _ = LEVELS[lesson["level"]]
        lesson.setdefault("level_label", level_label)
        lesson.setdefault("level_class", level_class)
        lesson.setdefault("nav_label", f"{noun} {lesson['num']}: {lesson['title']}")
        if lesson["level"] == 0:
            lesson.setdefault("counter", f"Base Camp {lesson['num']} of "
                                         f"{sum(1 for x in lessons if x['level'] == 0)}")
        else:
            lesson.setdefault("counter", f"Lesson {lesson['num']} of {len(numbered)}")
    return lessons


def build_all() -> list[tuple[str, str]]:
    from . import cheatsheets, glossary, insults, pages, pit, quizzes, workshop
    from .kit import lesson_page

    lessons = load_lessons()
    out: list[tuple[str, str]] = []

    # lesson pages, chained prev/next through the whole curriculum
    for i, lesson in enumerate(lessons):
        prev = lessons[i - 1] if i > 0 else None
        nxt = lessons[i + 1] if i + 1 < len(lessons) else None
        out.append((f"learn/{lesson['slug']}.html", lesson_page(lesson, prev, nxt)))

    out.append(("learn/index.html", pages.curriculum(lessons, LEVELS)))
    out.append(("index.html", pages.home(lessons)))
    out.append(("setup.html", pages.setup()))
    out.append(("playground.html", pages.playground()))
    out.append(("achievements.html", pages.achievements()))
    out.append(("pit.html", pit.build()))
    out.append(("insults.html", insults.build()))
    out.append(("quiz.html", quizzes.build()))
    out.append(("glossary.html", glossary.build()))
    out.append(("cheatsheets.html", cheatsheets.build()))
    out.extend(workshop.build())
    return out
