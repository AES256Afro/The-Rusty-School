"""Missions aboard the UES Magnanimous.

One module per season. Each mission carries a shared briefing and, per
language, four things: a stub, a reference solution (verified), a checker
(appended to learner code, prints BRIDGE| lines), and objective labels.

The helpers module explains the wire format and the generated checkers;
seasons that need stateful or concurrent checks write theirs by hand.
"""

from __future__ import annotations

from .helpers import MISSIONS  # noqa: F401  (the registry the seasons fill)
from . import s1, s2, s3, s4, s5, s6  # noqa: F401,E402

__all__ = ["MISSIONS"]
