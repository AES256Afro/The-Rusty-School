"""The Bridge: a starship simulator for people learning to code."""

from __future__ import annotations


def build_all() -> list[tuple[str, str]]:
    from . import render
    return render.build()
