"""Page shell for The Bridge.

The Bridge is campus-level rather than living inside either school, so it
gets its own template: its own mascot (the ship), its own stylesheet, and
a nav that points back at both schools. It still loads the campus
style.css, so themes, buttons and code blocks look like everywhere else.
"""

from __future__ import annotations

SITE = "https://rustyschool.com"
NAME = "The Bridge"
CAMPUS = "The Rusty School"
THEME_COLOR = "#f74c00"
OG_IMAGE = SITE + "/assets/og-image.png"
OG_ALT = "The Rusty School: learn Rust or Python from zero"

NL = chr(10)

# (scope, href, label). "bridge" is relative to docs/bridge/, "campus"
# is relative to docs/. Guessing the scope from a "../" prefix is how the
# first version of this file shipped every asset path one level too deep.
NAV = [
    ("bridge", "index.html", "The Bridge"),
    ("campus", "learn/index.html", "🦀 Rust"),
    ("campus", "python/index.html", "🐍 Python"),
]


def esc(text: str) -> str:
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def page(
    *,
    path: str,
    title: str,
    description: str,
    body: str,
    canonical: str,
    main_class: str = "container",
    body_attrs: str = "",
) -> str:
    """Render one Bridge page. `path` is relative to docs/."""
    # `path` always starts "bridge/", so its first slash is the Bridge root
    # itself and does not count as nesting. bridge/index.html sits AT the
    # root (up = ""), bridge/s1/x.html is one below it (up = "../").
    depth = path.count("/") - 1
    up = "../" * depth              # up to docs/bridge/
    campus = "../" * (depth + 1)    # up to docs/

    nav_items = NL.join(
        f'      <a href="{(up if scope == "bridge" else campus) + href}">{label}</a>'
        for scope, href, label in NAV
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{CAMPUS}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{OG_IMAGE}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{OG_ALT}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{OG_IMAGE}">
<meta name="theme-color" content="{THEME_COLOR}">
<link rel="icon" type="image/svg+xml" href="{up}assets/ship.svg">
<link rel="stylesheet" href="{campus}assets/style.css">
<link rel="stylesheet" href="{up}assets/bridge.css">
<script>try{{var t=localStorage.getItem("rusty-theme");if(t)document.documentElement.dataset.theme=t}}catch(e){{}}</script>
<script defer src="{campus}assets/app.js"></script>
<script defer src="{up}assets/missions.js"></script>
<script defer src="{up}assets/bridge.js"></script>
</head>
<body{body_attrs}>

<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="container">
    <a class="logo" href="{up}index.html"><img src="{up}assets/ship.svg" alt="The UES Magnanimous">The <span class="crate">Bridge</span></a>
    <button class="nav-burger" aria-label="Open menu">☰</button>
    <nav class="main-nav">
{nav_items}
      <button class="theme-toggle" aria-label="Toggle light/dark theme">☀️</button>
    </nav>
  </div>
</header>

<main id="main" tabindex="-1" class="{main_class}">
{body}
</main>

<footer class="site-footer">
  <div class="container cols">
    <div>
      <h4>The Bridge</h4>
      <ul>
        <li><a href="{up}index.html">Mission board</a></li>
        <li><a href="{campus}roadmap.html">Roadmap</a></li>
      </ul>
    </div>
    <div>
      <h4>The campus</h4>
      <ul>
        <li><a href="{campus}index.html">🦀 The Rusty School</a></li>
        <li><a href="{campus}python/index.html">🐍 The Python School</a></li>
        <li><a href="{campus}privacy.html">Privacy</a></li>
      </ul>
    </div>
    <div>
      <h4>The small print</h4>
      <p class="muted small">The UES Magnanimous, her crew and ARCHIE are original to
      this school. Starships, warp cores and away teams are stock science fiction and
      belong to everybody.</p>
    </div>
  </div>
</footer>

</body>
</html>
"""
