"""Placeholder for cheatsheets; real content lands in a later pass."""
from __future__ import annotations
from .kit import SCHOOL, SITE, page


def build() -> str:
    return page(
        path="cheatsheets.html",
        title="cheatsheets - " + SCHOOL,
        description="Coming very soon.",
        body="<section class='lesson-header'><h1>Under construction</h1></section>",
        canonical=SITE + "/python/cheatsheets",
    )
