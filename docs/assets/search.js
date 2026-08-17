/* ============================================================
   Campus search: one overlay, both schools.

   Loaded on demand by app.js (Rust) and py.js (Python), so neither
   school's hand-written or generated pages need a script tag.

   The index (assets/search-index.json, built by
   tools/build-search-index.py) is fetched the first time somebody
   actually opens search, never on page load. Nothing is sent anywhere:
   the matching all happens in this file, on your machine.
   ============================================================ */
(function () {
  "use strict";
  if (window.__campusSearch) return;
  window.__campusSearch = true;

  // Depth back to the campus root, so search behaves the same from /,
  // /learn/, /python/ and /python/build/.
  const ROOT = (function () {
    let p = location.pathname;
    if (!p.endsWith("/")) p = p.slice(0, p.lastIndexOf("/") + 1);
    const parts = p.split("/").filter(Boolean).length;
    return parts ? "../".repeat(parts) : "./";
  })();

  const KIND_ICON = { lesson: "📖", project: "🔨", puzzles: "🧩", page: "📄" };
  const SCHOOL_ICON = { rust: "🦀", python: "🐍" };

  let index = null;
  let loading = null;
  let overlay = null;
  let input = null;
  let listEl = null;
  let statusEl = null;
  let results = [];
  let active = 0;
  let filter = "all";

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    loading = fetch(ROOT + "assets/search-index.json")
      .then((r) => (r.ok ? r.json() : []))
      .then((data) => {
        index = data.map((p) => {
          // Precompute one lowercase haystack per page. Doing it once
          // here keeps every keystroke afterwards cheap.
          const heads = (p.h || []).join(" ");
          return {
            u: p.u, t: p.t, s: p.s, k: p.k, l: p.l || "", d: p.d || "",
            heads,
            lt: p.t.toLowerCase(),
            lh: heads.toLowerCase(),
            lb: ((p.d || "") + " " + (p.b || "")).toLowerCase(),
          };
        });
        return index;
      })
      .catch(() => (index = []));
    return loading;
  }

  /* A very small stemmer, so "dictionary" finds "Dictionaries" and
     "lifetimes" finds "Lifetime". It only ever shortens a word, which
     means matching can stay a plain substring test on the raw text.
     Not linguistics, just the handful of endings English actually
     throws at a search box. */
  function stem(w) {
    if (w.length > 5 && w.endsWith("ies")) return w.slice(0, -3);
    if (w.length > 4 && w.endsWith("y")) return w.slice(0, -1);
    if (w.length > 5 && w.endsWith("ing")) return w.slice(0, -3);
    if (w.length > 4 && w.endsWith("es")) return w.slice(0, -2);
    if (w.length > 3 && w.endsWith("s")) return w.slice(0, -1);
    return w;
  }

  /* ---- scoring ----
     Deliberately simple and explainable: a hit in the title beats a hit
     in a heading, which beats a hit in the body. Every word of the query
     must appear somewhere, so "borrow checker" does not match a page
     that merely says "checker". */
  function score(page, words, phrase) {
    let total = 0;
    for (const w of words) {
      let s = 0;
      const ti = page.lt.indexOf(w);
      if (ti === 0) s += 120;
      else if (ti > 0) s += page.lt[ti - 1] === " " ? 90 : 55;
      if (page.lh.includes(w)) s += 30;
      const bi = page.lb.indexOf(w);
      if (bi >= 0) s += 12;
      if (s === 0) return 0; // every word must land somewhere
      total += s;
    }
    // Whole-phrase hits are worth a lot: "list comprehension" should beat
    // a page that happens to say "list" in one place and "comprehension"
    // in another.
    if (words.length > 1) {
      if (page.lt.includes(phrase)) total += 200;
      else if (page.lh.includes(phrase)) total += 80;
      else if (page.lb.includes(phrase)) total += 40;
    }
    if (page.k === "lesson") total += 8; // ties fall towards teaching material
    return total;
  }

  function search(query) {
    const q = query.trim().toLowerCase();
    if (!q || !index) return [];
    const words = q.split(/\s+/).filter(Boolean).map(stem);
    const pool = filter === "all" ? index : index.filter((p) => p.s === filter);
    return pool
      .map((p) => ({ p, n: score(p, words, q) }))
      .filter((x) => x.n > 0)
      .sort((a, b) => b.n - a.n || a.p.t.length - b.p.t.length)
      .slice(0, 24)
      .map((x) => x.p);
  }

  /* A short piece of the page around the first match, so a result shows
     why it matched rather than just asserting that it did. */
  function snippet(page, q) {
    const hay = page.d + " " + (page.heads || "");
    const i = hay.toLowerCase().indexOf(q.split(/\s+/)[0]);
    if (i < 0) return page.d.slice(0, 120);
    const start = Math.max(0, i - 40);
    return (start ? "…" : "") + hay.slice(start, start + 130).trim();
  }

  function mark(text, words) {
    const frag = document.createDocumentFragment();
    if (!words.length) { frag.appendChild(document.createTextNode(text)); return frag; }
    const re = new RegExp("(" + words.map(escapeRe).join("|") + ")", "ig");
    let last = 0, m;
    while ((m = re.exec(text)) !== null) {
      if (m.index > last) frag.appendChild(document.createTextNode(text.slice(last, m.index)));
      const el = document.createElement("mark");
      el.textContent = m[0];
      frag.appendChild(el);
      last = m.index + m[0].length;
      if (m[0].length === 0) re.lastIndex++;
    }
    if (last < text.length) frag.appendChild(document.createTextNode(text.slice(last)));
    return frag;
  }
  function escapeRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

  function render() {
    const q = input.value.trim();
    // Highlight the stems, so searching "dictionary" still lights up the
    // "Dictionar" inside "Dictionaries".
    const words = q.toLowerCase().split(/\s+/).filter(Boolean).map(stem);
    results = search(q);
    active = 0;
    listEl.innerHTML = "";

    if (!q) {
      statusEl.textContent = index
        ? "Search " + index.length + " pages across both schools."
        : "Loading the index…";
      return;
    }
    if (!results.length) {
      statusEl.textContent = 'Nothing matched "' + q + '". Try a single word, or a topic like "ownership" or "dictionary".';
      return;
    }
    statusEl.textContent = results.length + (results.length === 1 ? " result" : " results");

    results.forEach((p, i) => {
      const a = document.createElement("a");
      a.className = "cs-hit" + (i === 0 ? " active" : "");
      a.href = ROOT.replace(/\/$/, "") + p.u;
      a.setAttribute("role", "option");
      a.setAttribute("aria-selected", i === 0 ? "true" : "false");
      a.id = "cs-hit-" + i;

      const icon = document.createElement("span");
      icon.className = "cs-icon";
      icon.textContent = KIND_ICON[p.k] || "📄";

      const body = document.createElement("span");
      body.className = "cs-body";
      const title = document.createElement("span");
      title.className = "cs-title";
      title.appendChild(mark(p.t, words));
      const meta = document.createElement("span");
      meta.className = "cs-meta";
      meta.textContent = (SCHOOL_ICON[p.s] || "") + " " +
        (p.s === "python" ? "Python School" : "Rusty School") +
        (p.l ? " · " + p.l : "");
      const desc = document.createElement("span");
      desc.className = "cs-desc";
      desc.appendChild(mark(snippet(p, q.toLowerCase()), words));

      body.appendChild(title);
      body.appendChild(meta);
      body.appendChild(desc);
      a.appendChild(icon);
      a.appendChild(body);
      a.addEventListener("mouseenter", () => setActive(i));
      listEl.appendChild(a);
    });
    input.setAttribute("aria-activedescendant", "cs-hit-0");
  }

  function setActive(i) {
    const hits = listEl.querySelectorAll(".cs-hit");
    if (!hits.length) return;
    active = (i + hits.length) % hits.length;
    hits.forEach((h, n) => {
      const on = n === active;
      h.classList.toggle("active", on);
      h.setAttribute("aria-selected", on ? "true" : "false");
    });
    hits[active].scrollIntoView({ block: "nearest" });
    input.setAttribute("aria-activedescendant", "cs-hit-" + active);
  }

  function build() {
    overlay = document.createElement("div");
    overlay.className = "cs-overlay";
    overlay.hidden = true;
    overlay.innerHTML =
      '<div class="cs-panel" role="dialog" aria-modal="true" aria-label="Search the campus">' +
        '<div class="cs-top">' +
          '<span class="cs-glass" aria-hidden="true">🔍</span>' +
          '<input type="search" class="cs-input" autocomplete="off" spellcheck="false" ' +
            'placeholder="Search lessons, projects and puzzles…" aria-label="Search the campus" ' +
            'role="combobox" aria-expanded="true" aria-controls="cs-list">' +
          '<button type="button" class="cs-close" aria-label="Close search">esc</button>' +
        "</div>" +
        '<div class="cs-filters" role="group" aria-label="Filter by school">' +
          '<button type="button" class="cs-chip active" data-f="all">Both schools</button>' +
          '<button type="button" class="cs-chip" data-f="rust">🦀 Rust</button>' +
          '<button type="button" class="cs-chip" data-f="python">🐍 Python</button>' +
        "</div>" +
        '<p class="cs-status" id="cs-status" aria-live="polite"></p>' +
        '<div class="cs-list" id="cs-list" role="listbox" aria-label="Search results"></div>' +
        '<div class="cs-foot"><kbd>↑</kbd><kbd>↓</kbd> to move · <kbd>enter</kbd> to open · ' +
          "<kbd>esc</kbd> to close</div>" +
      "</div>";
    document.body.appendChild(overlay);

    input = overlay.querySelector(".cs-input");
    listEl = overlay.querySelector(".cs-list");
    statusEl = overlay.querySelector(".cs-status");

    overlay.addEventListener("mousedown", (e) => { if (e.target === overlay) close(); });
    overlay.querySelector(".cs-close").addEventListener("click", close);
    input.addEventListener("input", render);
    overlay.querySelectorAll(".cs-chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        filter = chip.dataset.f;
        overlay.querySelectorAll(".cs-chip").forEach((c) => c.classList.toggle("active", c === chip));
        render();
        input.focus();
      });
    });

    input.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown") { e.preventDefault(); setActive(active + 1); }
      else if (e.key === "ArrowUp") { e.preventDefault(); setActive(active - 1); }
      else if (e.key === "Enter") {
        const hit = listEl.querySelectorAll(".cs-hit")[active];
        if (hit) { e.preventDefault(); location.href = hit.href; }
      } else if (e.key === "Escape") { e.preventDefault(); close(); }
    });

    // Keep tab focus inside the dialog while it is open.
    overlay.addEventListener("keydown", (e) => {
      if (e.key !== "Tab") return;
      const focusable = overlay.querySelectorAll("button, input, a");
      if (!focusable.length) return;
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    });
  }

  let lastFocus = null;

  function open(prefill) {
    if (!overlay) build();
    lastFocus = document.activeElement;
    overlay.hidden = false;
    document.body.classList.add("cs-open");
    if (prefill) input.value = prefill;
    input.focus();
    input.select();
    render();
    loadIndex().then(render);
  }

  function close() {
    if (!overlay || overlay.hidden) return;
    overlay.hidden = true;
    document.body.classList.remove("cs-open");
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  function isTyping(el) {
    if (!el) return false;
    const tag = el.tagName;
    return tag === "INPUT" || tag === "TEXTAREA" || tag === "SELECT" || el.isContentEditable;
  }

  document.addEventListener("keydown", (e) => {
    const open_ = overlay && !overlay.hidden;
    // "/" is the convention people already know from GitHub and friends.
    if (!open_ && e.key === "/" && !isTyping(document.activeElement) &&
        !e.metaKey && !e.ctrlKey && !e.altKey) {
      e.preventDefault();
      open();
    } else if (!open_ && (e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
      e.preventDefault();
      open();
    } else if (open_ && e.key === "Escape") {
      close();
    }
  });

  // A visible entry point in the nav, because a keyboard shortcut nobody
  // can see is a feature only power users get.
  function addNavButton() {
    const nav = document.querySelector(".main-nav");
    if (!nav || nav.querySelector(".cs-nav-btn")) return;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "cs-nav-btn";
    btn.innerHTML = '<span aria-hidden="true">🔍</span><span class="cs-nav-label">Search</span>';
    btn.setAttribute("aria-label", "Search the campus");
    btn.addEventListener("click", () => open());
    const toggle = nav.querySelector(".theme-toggle");
    if (toggle) nav.insertBefore(btn, toggle);
    else nav.appendChild(btn);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addNavButton);
  } else {
    addNavButton();
  }

  window.campusSearch = { open, close };
})();
