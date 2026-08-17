"""Placeholder for the workshop; real content lands in a later pass."""
from __future__ import annotations
from .kit import SCHOOL, SITE, page


def build() -> list[tuple[str, str]]:
    return [("build/index.html", page(
        path="build/index.html",
        title="Workshop - " + SCHOOL,
        description="Coming very soon.",
        body="<section class='lesson-header'><h1>Under construction</h1></section>",
        canonical=SITE + "/python/build/",
    ))]
