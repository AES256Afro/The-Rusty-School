/* ============================================================
   The Python School: site scripts

   Deliberately standalone (the Rusty School's app.js is Rust-flavoured
   down to its syntax highlighter), but it shares the campus storage
   keys so one account carries progress across both schools.

   Contents
     theme + nav          shared with the Rusty School
     highlightPython      a small hand-rolled tokenizer
     Pyodide runner       real CPython 3.14, in your browser, no server
     progress + XP        ranks, levels, achievements, toasts
     quiz engine          same shape as the Rusty School's
     the Snake Pit        puzzle renderer
     the Insult Compiler  error-message swordfighting
   ============================================================ */
(function () {
  "use strict";

  const root = document.documentElement;
  const IN_SUB = /\/python\/(learn|build)\//.test(location.pathname);
  const UP = IN_SUB ? "../" : "";
  const campus = UP + "../";      // from any python page up to the campus (docs) root

  /* ================= theme (shared across the campus) ================= */
  function initTheme() {
    const stored = localStorage.getItem("rusty-theme");
    if (stored) {
      root.dataset.theme = stored;
    } else if (window.matchMedia("(prefers-color-scheme: light)").matches) {
      root.dataset.theme = "light";
    }
    updateThemeButton();
  }
  function updateThemeButton() {
    const btn = document.querySelector(".theme-toggle");
    if (btn) btn.textContent = root.dataset.theme === "light" ? "🌙" : "☀️";
  }
  function toggleTheme() {
    const next = root.dataset.theme === "light" ? "dark" : "light";
    root.dataset.theme = next;
    localStorage.setItem("rusty-theme", next);
    updateThemeButton();
  }

  /* ================= nav ================= */
  function initNav() {
    const burger = document.querySelector(".nav-burger");
    const nav = document.querySelector(".main-nav");
    if (burger && nav) burger.addEventListener("click", () => nav.classList.toggle("open"));

    // Campus cross-link: a Rust School link on every Python page, mirroring
    // the Python link the Rust school injects. The campus goes both ways.
    if (nav && !nav.querySelector('a.nav-campus')) {
      const rust = document.createElement("a");
      rust.href = campus + "index.html";
      rust.textContent = "🦀 Rust";
      rust.className = "nav-campus";
      nav.insertBefore(rust, nav.querySelector(".theme-toggle"));
    }

    const footList = document.querySelector(".site-footer .cols ul");
    if (footList && !footList.querySelector('a[href$="roadmap.html"]')) {
      const li = document.createElement("li");
      li.innerHTML = '<a href="' + campus + 'roadmap.html">Roadmap</a>';
      footList.appendChild(li);
    }
    if (footList && !footList.querySelector('a[href$="privacy.html"]')) {
      const li = document.createElement("li");
      li.innerHTML = '<a href="' + campus + 'privacy.html">Privacy</a>';
      footList.appendChild(li);
    }
    const footer = document.querySelector(".site-footer");
    if (footer && !footer.querySelector(".license-line")) {
      const wrap = document.createElement("div");
      wrap.className = "container";
      wrap.innerHTML =
        '<p class="license-line">Code ' +
        '<a href="https://github.com/AES256Afro/The-Rusty-School/blob/main/LICENSE-MIT" target="_blank" rel="noopener">MIT</a> OR ' +
        '<a href="https://github.com/AES256Afro/The-Rusty-School/blob/main/LICENSE-APACHE" target="_blank" rel="noopener">Apache-2.0</a>' +
        ' · Course content ' +
        '<a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a>' +
        ' · Code examples in lessons are MIT/Apache too, so copy away.</p>';
      footer.appendChild(wrap);
    }

    const here = location.pathname.replace(/\/index\.html$/, "/");
    document.querySelectorAll(".main-nav a").forEach((a) => {
      const href = a.getAttribute("href");
      if (!href || href.startsWith("http")) return;
      const target = new URL(href, location.href).pathname.replace(/\/index\.html$/, "/");
      if (target === here || (target.endsWith("/learn/") && here.includes("/python/learn/"))) {
        a.classList.add("active");
      }
    });
  }

  /* ================= Python syntax highlighting ================= */
  const KEYWORDS =
    "False|None|True|and|as|assert|async|await|break|class|continue|def|del|elif|" +
    "else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|" +
    "pass|raise|return|try|while|with|yield|match|case";
  const BUILTINS =
    "abs|all|any|ascii|bin|bool|bytearray|bytes|callable|chr|classmethod|compile|" +
    "complex|dict|dir|divmod|enumerate|eval|exec|filter|float|format|frozenset|" +
    "getattr|globals|hasattr|hash|help|hex|id|input|int|isinstance|issubclass|iter|" +
    "len|list|locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|" +
    "property|range|repr|reversed|round|set|setattr|slice|sorted|staticmethod|str|" +
    "sum|super|tuple|type|vars|zip|Exception|ValueError|TypeError|KeyError|" +
    "IndexError|NameError|ZeroDivisionError|FileNotFoundError|AttributeError|" +
    "RuntimeError|StopIteration|ImportError|OSError|EOFError|KeyboardInterrupt";

  const PY_RE = new RegExp(
    [
      '("""[\\s\\S]*?"""|\'\'\'[\\s\\S]*?\'\'\')',                       // 1 triple string
      "(#[^\\n]*)",                                                        // 2 comment
      "([fFbBrRuU]{0,2}\"(?:[^\"\\\\\\n]|\\\\.)*\"|[fFbBrRuU]{0,2}'(?:[^'\\\\\\n]|\\\\.)*')", // 3 string
      "(@[A-Za-z_][A-Za-z0-9_.]*)",                                        // 4 decorator
      "(\\b__[a-z_]+__\\b)",                                               // 5 dunder
      "(\\b(?:" + KEYWORDS + ")\\b)",                                      // 6 keyword
      "(\\b(?:self|cls)\\b)",                                              // 7 self
      "(\\b(?:" + BUILTINS + ")\\b)",                                      // 8 builtin
      "(\\b[A-Z][A-Za-z0-9_]*\\b)",                                        // 9 class name
      "(\\b\\d[\\d_]*(?:\\.\\d[\\d_]*)?(?:[eE][-+]?\\d+)?[jJ]?\\b)",       // 10 number
      "(\\b[a-z_][a-z0-9_]*(?=\\s*\\())",                                  // 11 call
    ].join("|"),
    "g"
  );
  const PY_CLASS = [null, "tok-str", "tok-com", "tok-str", "tok-dec", "tok-attr",
    "tok-kw", "tok-self", "tok-typ", "tok-typ", "tok-num", "tok-fn"];

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightPython(source) {
    let out = "";
    let last = 0;
    let m;
    PY_RE.lastIndex = 0;
    while ((m = PY_RE.exec(source)) !== null) {
      out += escapeHtml(source.slice(last, m.index));
      let cls = null;
      for (let g = 1; g < PY_CLASS.length; g++) {
        if (m[g] !== undefined) { cls = PY_CLASS[g]; break; }
      }
      out += cls ? '<span class="' + cls + '">' + escapeHtml(m[0]) + "</span>" : escapeHtml(m[0]);
      last = m.index + m[0].length;
    }
    out += escapeHtml(source.slice(last));
    return out;
  }

  /* ================= code blocks: highlight, copy, run ================= */
  function initCode() {
    document.querySelectorAll("pre > code").forEach((code) => {
      const pre = code.parentElement;
      const plain = pre.classList.contains("term") || pre.classList.contains("out") ||
                    pre.classList.contains("traceback") || pre.classList.contains("repl") ||
                    code.classList.contains("nohl");
      if (!plain) code.innerHTML = highlightPython(code.textContent);

      const btn = document.createElement("button");
      btn.className = "copy-btn";
      btn.type = "button";
      btn.textContent = "copy";
      btn.addEventListener("click", () => {
        navigator.clipboard.writeText(code.textContent).then(() => {
          btn.textContent = "copied ✓";
          btn.classList.add("copied");
          setTimeout(() => { btn.textContent = "copy"; btn.classList.remove("copied"); }, 1600);
        });
      });
      pre.appendChild(btn);

      if (pre.classList.contains("run")) {
        const runBtn = document.createElement("button");
        runBtn.className = "copy-btn run-btn";
        runBtn.type = "button";
        runBtn.textContent = "▶ run";
        runBtn.addEventListener("click", () => {
          let out = pre.nextElementSibling;
          if (!out || !out.classList.contains("run-out")) {
            out = document.createElement("div");
            out.className = "run-out";
            pre.insertAdjacentElement("afterend", out);
          }
          executePython(code.textContent, out, runBtn, pre.dataset.stdin || "");
        });
        pre.appendChild(runBtn);
      }
    });
  }

  /* ================= the Python engine (Pyodide) =================
     Real CPython compiled to WebAssembly, downloaded from a CDN the
     first time you press run and cached by your browser afterwards.
     Nothing you type here ever leaves your machine: there is no server
     to send it to. That is a genuinely different bargain from the
     Rusty School's playground, which has to ship your Rust off to a
     compiler farm. */
  const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v314.0.5/full/";
  let pyodidePromise = null;

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = () => reject(new Error("could not load " + src));
      document.head.appendChild(s);
    });
  }

  function getPyodide(onProgress) {
    if (pyodidePromise) return pyodidePromise;
    pyodidePromise = (async () => {
      if (onProgress) onProgress("Downloading Python (about 12 MB, once)…");
      if (!window.loadPyodide) await loadScript(PYODIDE_URL + "pyodide.js");
      if (onProgress) onProgress("Starting the interpreter…");
      const py = await window.loadPyodide({ indexURL: PYODIDE_URL });
      return py;
    })().catch((err) => {
      pyodidePromise = null;
      throw err;
    });
    return pyodidePromise;
  }

  /* The harness that runs your code.

     It captures stdout and stderr into one buffer (so print order is
     preserved), fakes input() with a browser prompt or a canned answer
     list, and installs a watchdog so an accidental infinite loop gives
     you a friendly message instead of a frozen tab. */
  const HARNESS = `
import sys, io, time, builtins, traceback

_buf = io.StringIO()
_saved = (sys.stdout, sys.stderr, builtins.input)
sys.stdout = _buf
sys.stderr = _buf

_lines = list(_stdin_lines)

def _input(prompt=""):
    text = str(prompt)
    _buf.write(text)
    if _lines:
        answer = _lines.pop(0)
    else:
        from js import window
        answer = window.prompt(text or "Your program is asking for input:")
        if answer is None:
            raise EOFError("input() was cancelled")
    answer = str(answer)
    _buf.write(answer + "\\n")
    return answer

builtins.input = _input

_deadline = time.time() + 20.0
_ticks = 0

def _watchdog(frame, event, arg):
    global _ticks
    _ticks += 1
    if _ticks % 4000 == 0 and time.time() > _deadline:
        raise TimeoutError(
            "This program ran for more than 20 seconds, so the school stopped it. "
            "Nine times out of ten that means a loop with no way out."
        )
    return _watchdog

_ok = True
try:
    _compiled = compile(_user_code, "your_program.py", "exec")
except SyntaxError as _e:
    _ok = False
    _buf.write("".join(traceback.format_exception_only(type(_e), _e)))
else:
    try:
        sys.settrace(_watchdog)
        exec(_compiled, {"__name__": "__main__", "__file__": "your_program.py"})
    except SystemExit:
        pass
    except BaseException as _e:
        _ok = False
        sys.settrace(None)
        # tb_next drops this harness's own frame, so a student only ever
        # sees line numbers from the code they actually wrote
        _tb = _e.__traceback__
        _buf.write("".join(traceback.format_exception(
            type(_e), _e, _tb.tb_next if _tb is not None and _tb.tb_next else _tb)))
    finally:
        sys.settrace(None)
sys.stdout, sys.stderr, builtins.input = _saved

_result = _buf.getvalue()
_failed = not _ok
`;

  function runLine(text, cls) {
    const span = document.createElement("span");
    span.className = cls;
    span.textContent = text;
    return span;
  }

  async function executePython(code, outEl, button, stdin) {
    outEl.innerHTML = "";
    const status = runLine("⏳ Waking the snake…", "run-warn");
    outEl.appendChild(status);
    if (button) button.disabled = true;
    try {
      const py = await getPyodide((msg) => { status.textContent = "⏳ " + msg; });
      status.textContent = "⏳ Running…";
      py.globals.set("_user_code", code);
      py.globals.set("_stdin_lines", stdin ? stdin.split("\n") : []);
      await py.runPythonAsync(HARNESS);
      const result = py.globals.get("_result");
      const failed = py.globals.get("_failed");
      outEl.innerHTML = "";
      const text = (result || "").replace(/\s+$/, "");
      if (failed) {
        outEl.appendChild(runLine(text || "something went wrong", "run-err"));
        outEl.appendChild(runLine(
          "Read a traceback from the BOTTOM up: the last line names the problem.",
          "run-hint"));
      } else {
        outEl.appendChild(runLine(
          text.length ? text : "(the program ran, and printed nothing at all)", "run-ok"));
      }
      flag("ran-code");
    } catch (err) {
      outEl.innerHTML = "";
      outEl.appendChild(runLine(
        "⚠️ Could not start Python in your browser. " +
        "Check your connection and try again. (" + (err && err.message ? err.message : err) + ")",
        "run-err"));
    } finally {
      if (button) button.disabled = false;
    }
  }

  /* ================= progress, XP and ranks ================= */
  const XP_LESSON = 100;
  const XP_PUZZLE = 60;
  const XP_PROJECT = 250;
  const XP_QUIZ_Q = 20;

  const RANKS = [
    [0, "Stowaway", "🥚"],
    [300, "Deck Swabber", "🧽"],
    [700, "Grog Taster", "🍺"],
    [1200, "Rubber Chicken Owner", "🐔"],
    [1900, "Cartographer", "🗺️"],
    [2800, "Insult Duelist", "⚔️"],
    [3900, "Quartermaster", "📦"],
    [5200, "Ship's Navigator", "🧭"],
    [6800, "First Mate", "🦜"],
    [8600, "Snake Charmer", "🐍"],
    [10600, "Mighty Programmer", "🏴‍☠️"],
    [12800, "Harbourmaster of the Interpreter", "🌟"],
  ];

  function getDone() {
    try { return new Set(JSON.parse(localStorage.getItem("rusty-done") || "[]")); }
    catch { return new Set(); }
  }
  function saveDone(set) {
    localStorage.setItem("rusty-done", JSON.stringify([...set]));
  }
  function bestScores() {
    try { return JSON.parse(localStorage.getItem("rusty-quiz-best") || "{}"); }
    catch { return {}; }
  }
  function getFlags() {
    try { return JSON.parse(localStorage.getItem("py-flags") || "{}"); }
    catch { return {}; }
  }
  function flag(name, value) {
    const f = getFlags();
    if (f[name] === (value === undefined ? true : value)) return;
    f[name] = value === undefined ? true : value;
    localStorage.setItem("py-flags", JSON.stringify(f));
  }

  function countDone(prefix) {
    let n = 0;
    getDone().forEach((id) => { if (id.startsWith(prefix)) n++; });
    return n;
  }

  function totalXp() {
    const done = getDone();
    let xp = 0;
    done.forEach((id) => {
      if (id.startsWith("pypit-")) xp += XP_PUZZLE;
      else if (id.startsWith("pybuild-")) xp += XP_PROJECT;
      else if (id.startsWith("py-")) xp += XP_LESSON;
    });
    const best = bestScores();
    Object.keys(best).forEach((k) => { if (k.startsWith("py-")) xp += best[k] * XP_QUIZ_Q; });
    xp += unlockedAchievements().reduce((sum, a) => sum + (a.xp || 0), 0);
    return xp;
  }

  function rankFor(xp) {
    let i = 0;
    for (let k = 0; k < RANKS.length; k++) if (xp >= RANKS[k][0]) i = k;
    const [floor, name, icon] = RANKS[i];
    const next = RANKS[i + 1] || null;
    return {
      index: i + 1, name, icon, floor,
      nextAt: next ? next[0] : null,
      nextName: next ? next[1] : null,
      pct: next ? Math.min(100, Math.round(((xp - floor) / (next[0] - floor)) * 100)) : 100,
    };
  }

  function renderXp() {
    const wrap = document.getElementById("xp-wrap");
    if (!wrap) return;
    const xp = totalXp();
    const r = rankFor(xp);
    wrap.querySelector(".rank-num").textContent = r.index;
    wrap.querySelector(".rank-name").textContent = r.icon + " " + r.name;
    wrap.querySelector(".xp-nums").innerHTML =
      "<strong>" + xp.toLocaleString() + " XP</strong>" +
      (r.nextAt ? " · " + (r.nextAt - xp).toLocaleString() + " to " + r.nextName
                : " · maximum rank, you magnificent creature");
    wrap.querySelector(".xp-fill").style.width = r.pct + "%";
  }

  /* ---- achievements ----
     Every test below reads window.PY_COURSE (assets/course.js), which
     ships on every page. It used to read page-scoped globals such as
     PY_LESSONS, which exist only on the curriculum page: away from that
     one page the level achievements silently evaluated to false, and
     because checkNewAchievements() then wrote the shrunken list back to
     storage, already-earned achievements were re-announced later. One
     shared index fixes the whole family of bugs. */
  function courseLessons() {
    return (window.PY_COURSE && window.PY_COURSE.lessons) || window.PY_LESSONS || [];
  }
  function quizSizes() {
    return (window.PY_COURSE && window.PY_COURSE.quizSizes) || window.PY_QUIZ_SIZES || {};
  }
  function pitTotal() {
    return (window.PY_COURSE && window.PY_COURSE.pitTotal) || window.PY_PIT_TOTAL || 0;
  }
  function buildTotal() {
    return (window.PY_COURSE && window.PY_COURSE.projects.length) || window.PY_BUILD_TOTAL || 0;
  }

  function lessonIdsForLevel(level) {
    return courseLessons().filter((l) => l.level === level).map((l) => l.id);
  }
  function allComplete(ids) {
    if (!ids.length) return false;
    const done = getDone();
    return ids.every((id) => done.has(id));
  }

  const ACHIEVEMENTS = [
    { id: "hatchling", icon: "🐣", name: "Hatchling", xp: 25,
      how: "Complete your first Python lesson.",
      test: () => countDone("py-") > 0 },
    { id: "hello", icon: "👋", name: "Certified Greeter", xp: 25,
      how: "Finish Lesson 1 and greet the world.",
      test: () => getDone().has("py-01-hello") },
    { id: "indent", icon: "📐", name: "Indentation Whisperer", xp: 100,
      how: "Complete every Level 1 lesson.",
      test: () => allComplete(lessonIdsForLevel(1)) },
    { id: "collector", icon: "🧰", name: "The Collector", xp: 100,
      how: "Complete every Level 2 lesson.",
      test: () => allComplete(lessonIdsForLevel(2)) },
    { id: "shipwright", icon: "🛠️", name: "Shipwright", xp: 100,
      how: "Complete every Level 3 lesson.",
      test: () => allComplete(lessonIdsForLevel(3)) },
    { id: "decorated", icon: "🎩", name: "Decorated", xp: 100,
      how: "Complete every Level 4 lesson.",
      test: () => allComplete(lessonIdsForLevel(4)) },
    { id: "fieldagent", icon: "🌍", name: "Field Agent", xp: 100,
      how: "Complete every Level 5 lesson.",
      test: () => allComplete(lessonIdsForLevel(5)) },
    { id: "alive", icon: "🤖", name: "It's Alive", xp: 200,
      how: "Complete the whole Jarvis track.",
      test: () => allComplete(lessonIdsForLevel(6)) },
    { id: "graduate", icon: "🎓", name: "Graduate", xp: 400,
      how: "Complete every lesson in the school.",
      test: () => allComplete(courseLessons().map((l) => l.id)) },
    { id: "labrat", icon: "🧪", name: "Lab Rat", xp: 25,
      how: "Run Python in your browser at least once.",
      test: () => !!getFlags()["ran-code"] },
    { id: "duelist", icon: "⚔️", name: "Insult Duelist", xp: 75,
      how: "Win a bout in the Insult Compiler.",
      test: () => !!getFlags()["duel-won"] },
    { id: "swordmaster", icon: "🗡️", name: "Sword Master", xp: 150,
      how: "Win the Insult Compiler without taking a single hit.",
      test: () => !!getFlags()["duel-flawless"] },
    { id: "pitfighter", icon: "🐍", name: "Pit Fighter", xp: 75,
      how: "Solve ten puzzles in the Snake Pit.",
      test: () => countDone("pypit-") >= 10 },
    { id: "basilisk", icon: "🏆", name: "Basilisk Slayer", xp: 200,
      how: "Solve every puzzle in the Snake Pit.",
      test: () => pitTotal() > 0 && countDone("pypit-") >= pitTotal() },
    { id: "bookworm", icon: "📚", name: "Bookworm", xp: 50,
      how: "Score full marks on any quiz.",
      test: () => {
        const best = bestScores();
        const quizzes = quizSizes();
        return Object.keys(quizzes).some((k) => best[k] === quizzes[k]);
      } },
    { id: "straightas", icon: "💯", name: "Straight A's", xp: 200,
      how: "Score full marks on every quiz.",
      test: () => {
        const best = bestScores();
        const quizzes = quizSizes();
        const keys = Object.keys(quizzes);
        return keys.length > 0 && keys.every((k) => best[k] === quizzes[k]);
      } },
    { id: "builder", icon: "🔨", name: "Builder", xp: 75,
      how: "Finish one project in the workshop.",
      test: () => countDone("pybuild-") > 0 },
    { id: "shipped", icon: "🚢", name: "Shipped It", xp: 300,
      how: "Finish every project in the workshop.",
      test: () => buildTotal() > 0 && countDone("pybuild-") >= buildTotal() },
    { id: "bilingual", icon: "🦀", name: "Bilingual", xp: 100,
      how: "Complete lessons at both the Python School and the Rusty School.",
      test: () => {
        let rust = 0;
        getDone().forEach((id) => {
          if (!id.startsWith("py-") && !id.startsWith("pypit-") &&
              !id.startsWith("pybuild-") && !id.startsWith("dojo-")) rust++;
        });
        return rust > 0 && countDone("py-") > 0;
      } },
    { id: "nightowl", icon: "🌙", name: "Night Owl", xp: 25,
      how: "Complete a lesson between midnight and 5am. We are not judging.",
      test: () => !!getFlags()["night-owl"] },
    { id: "caffeine", icon: "☕", name: "Caffeinated", xp: 50,
      how: "Complete three lessons in a single day.",
      test: () => (getFlags()["day-best"] || 0) >= 3 },
  ];

  function unlockedAchievements() {
    return ACHIEVEMENTS.filter((a) => {
      try { return a.test(); } catch { return false; }
    });
  }

  function checkNewAchievements() {
    const seen = getFlags()["ach"] || [];
    const now = unlockedAchievements().map((a) => a.id);
    const fresh = now.filter((id) => !seen.includes(id));
    if (fresh.length) {
      flag("ach", now);
      const a = ACHIEVEMENTS.find((x) => x.id === fresh[0]);
      toast("🏅 Achievement unlocked: " + a.icon + " " + a.name,
            a.how + (fresh.length > 1 ? " (and " + (fresh.length - 1) + " more)" : ""));
    } else if (seen.length !== now.length) {
      flag("ach", now);
    }
  }

  function toast(title, body) {
    const el = document.createElement("div");
    el.className = "toast";
    el.innerHTML = '<span class="t-title"></span><span class="t-body"></span>';
    el.querySelector(".t-title").textContent = title;
    el.querySelector(".t-body").textContent = body || "";
    // Finishing a level can earn an achievement and a milestone at the
    // same instant. Stack them rather than letting one hide the other.
    const stacked = document.querySelectorAll(".toast").length;
    if (stacked) el.style.bottom = 26 + stacked * 104 + "px";
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 5200);
  }

  function noteDailyStreak() {
    const now = new Date();
    if (now.getHours() < 5) flag("night-owl");
    const key = now.getFullYear() + "-" + (now.getMonth() + 1) + "-" + now.getDate();
    const f = getFlags();
    const day = f["day"] === key ? (f["day-count"] || 0) + 1 : 1;
    flag("day", key);
    flag("day-count", day);
    if (day > (f["day-best"] || 0)) flag("day-best", day);
  }

  /* ---- lesson complete buttons + curriculum bars ---- */
  function initProgress() {
    document.querySelectorAll(".complete-btn[data-lesson]").forEach((btn) => {
      const id = btn.dataset.lesson;
      const label = btn.dataset.label || "Mark lesson complete";
      const doneLabel = btn.dataset.doneLabel || "✓ Lesson complete. Monty approves.";
      const render = () => {
        const isDone = getDone().has(id);
        btn.classList.toggle("done", isDone);
        btn.textContent = isDone ? doneLabel : label;
      };
      render();
      btn.addEventListener("click", (e) => {
        const set = getDone();
        if (set.has(id)) {
          set.delete(id);
        } else {
          set.add(id);
          confetti(e.clientX, e.clientY);
          reportCompletion(id);
          noteDailyStreak();
        }
        saveDone(set);
        render();
        renderXp();
        checkNewAchievements();
        refreshGuidance(true);
        pushProgress();
      });
    });

    const cards = document.querySelectorAll(".lesson-card[data-lesson]");
    if (cards.length) {
      const done = getDone();
      let doneCount = 0;
      cards.forEach((card) => {
        if (done.has(card.dataset.lesson)) { card.classList.add("done"); doneCount++; }
      });
      const fill = document.getElementById("progress-fill");
      const label = document.getElementById("progress-label");
      if (fill) fill.style.width = Math.round((doneCount / cards.length) * 100) + "%";
      if (label) {
        const noun = document.body.dataset.noun || "lessons";
        const one = noun.replace(/s$/, "");
        label.textContent = doneCount === 0
          ? "0 of " + cards.length + " " + noun + " complete. Every expert started exactly here 🐍"
          : doneCount === cards.length
          ? "All " + cards.length + " " + noun + " complete. You did it! 🎓🐍"
          : doneCount + " of " + cards.length + " " +
            (doneCount === 1 ? one : noun) + " complete. Keep going!";
      }
    }
  }

  /* ---- the public counter (anonymous, DNT-respecting) ---- */
  function dntEnabled() {
    return navigator.doNotTrack === "1" || window.doNotTrack === "1";
  }
  function reportCompletion(id) {
    if (dntEnabled()) return;
    if (id.startsWith("pypit-")) return; // puzzles stay private, like the dojo
    let counted;
    try { counted = new Set(JSON.parse(localStorage.getItem("rusty-counted") || "[]")); }
    catch { counted = new Set(); }
    if (counted.has(id)) return;
    counted.add(id);
    localStorage.setItem("rusty-counted", JSON.stringify([...counted]));
    fetch("/api/complete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lesson: id }),
      keepalive: true,
    }).catch(() => {});
  }

  /* ================= confetti ================= */
  const CONFETTI = ["🐍", "🎉", "⭐", "💛", "✨"];
  function confetti(x, y) {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    for (let i = 0; i < 14; i++) {
      const piece = document.createElement("span");
      piece.className = "confetti-piece";
      piece.textContent = CONFETTI[i % CONFETTI.length];
      piece.style.left = x + (Math.random() * 160 - 80) + "px";
      piece.style.top = y - 10 + "px";
      piece.style.animationDelay = Math.random() * 0.25 + "s";
      document.body.appendChild(piece);
      setTimeout(() => piece.remove(), 1800);
    }
  }

  /* ================= achievements page ================= */
  function initAchievements() {
    const rootEl = document.getElementById("ach-root");
    if (!rootEl) return;
    const unlocked = new Set(unlockedAchievements().map((a) => a.id));
    rootEl.innerHTML = "";
    const grid = document.createElement("div");
    grid.className = "ach-grid";
    ACHIEVEMENTS.forEach((a) => {
      const card = document.createElement("div");
      card.className = "ach" + (unlocked.has(a.id) ? " unlocked" : "");
      card.innerHTML =
        '<div class="ach-icon">' + a.icon + "</div>" +
        "<div><h3></h3><p></p>" +
        '<span class="ach-state"></span></div>';
      card.querySelector("h3").textContent = a.name;
      card.querySelector("p").textContent = a.how;
      card.querySelector(".ach-state").textContent =
        (unlocked.has(a.id) ? "Unlocked · +" : "Locked · +") + a.xp + " XP";
      grid.appendChild(card);
    });
    rootEl.appendChild(grid);
    const count = document.getElementById("ach-count");
    if (count) {
      count.textContent = unlocked.size + " of " + ACHIEVEMENTS.length + " unlocked";
    }
  }

  /* ================= milestones and what to do next =================
     Achievements are wide: twenty-one scattered rewards for doing
     interesting things. Milestones are the opposite shape, and answer a
     different question. They are the single road through the school,
     and each one names what you can DO now rather than how much is
     left. Both matter; neither replaces the other.

     Alongside them sits the question beginners ask most often and
     tutorials answer worst: what should I do next? The engine below
     names one concrete action with a reason.

     Course order comes from assets/course.js, generated by pybuild.py,
     so this never drifts from the curriculum. */
  function course() {
    return window.PY_COURSE || { levels: [], lessons: [], projects: [], pitTotal: 0 };
  }
  function lessonsOfLevel(n) {
    return course().lessons.filter((l) => l.level === n);
  }
  function countDoneIn(ids) {
    const done = getDone();
    return ids.filter((id) => done.has(id)).length;
  }
  function levelProgress(n) {
    const ids = lessonsOfLevel(n).map((l) => l.id);
    return [countDoneIn(ids), ids.length];
  }
  function lessonsDoneCount() {
    return countDoneIn(course().lessons.map((l) => l.id));
  }
  function projectsDoneCount() {
    return countDoneIn(course().projects.map((p) => p.id));
  }

  const MILESTONES = [
    { id: "camp", icon: "🏕️", name: "Camp Struck",
      blurb: "Base Camp done. You know what a program is, what an interpreter does, and why any of this works. No Python required.",
      need: () => levelProgress(0) },
    { id: "firstwords", icon: "👋", name: "First Words",
      blurb: "You have written and run real Python. The gap between zero and one is the widest one there is, and it is behind you.",
      need: () => [countDoneIn(["py-01-hello"]), 1] },
    { id: "fledgling", icon: "🐣", name: "Fledgling",
      blurb: "Values, names, decisions, loops. The whole language in miniature: you can already write programs that think.",
      need: () => levelProgress(1) },
    { id: "toolbox", icon: "🧰", name: "Toolbox Open",
      blurb: "Lists, dictionaries, functions. This is the point where Python stops being a toy and starts being a superpower.",
      need: () => levelProgress(2) },
    { id: "builder", icon: "🔨", name: "Builder",
      blurb: "One workshop project finished, built from a spec rather than copied. That is the cure for tutorial hell.",
      need: () => [Math.min(projectsDoneCount(), 1), 1] },
    { id: "pit", icon: "🐍", name: "Pit Fighter",
      blurb: "Ten Snake Pit puzzles solved. Reading broken code is a separate skill from writing new code, and a rarer one.",
      need: () => [Math.min(countDone("pypit-"), 10), 10] },
    { id: "software", icon: "🛠️", name: "Software, Not Scripts",
      blurb: "Files, errors, testing, packaging. The difference between something that ran once and something other people can use.",
      need: () => levelProgress(3) },
    { id: "pythonic", icon: "🎩", name: "Pythonic",
      blurb: "Objects, generators, decorators. Your code has stopped looking like translated Java and started looking like Python.",
      need: () => levelProgress(4) },
    { id: "wild", icon: "🌍", name: "In the Wild",
      blurb: "Automation, the web, data, games, hardware. You have seen what people actually build for a living.",
      need: () => levelProgress(5) },
    { id: "jarvis", icon: "🤖", name: "Jarvis Online",
      blurb: "The capstone track complete: a private AI assistant you built, own, and understand end to end.",
      need: () => levelProgress(6) },
    { id: "shipped", icon: "🚢", name: "Shipped It",
      blurb: "Every workshop project finished. You have a folder of programs that are yours.",
      need: () => [projectsDoneCount(), course().projects.length] },
    { id: "graduate", icon: "🎓", name: "Graduate",
      blurb: "Every lesson in the school complete. Now go and teach somebody, which is the only way to find out what you really know.",
      need: () => [lessonsDoneCount(), course().lessons.length] },
  ];

  function milestoneState() {
    const list = MILESTONES.map((m) => {
      const [have, total] = m.need();
      return { m, have, total, reached: total > 0 && have >= total };
    });
    return {
      list,
      current: list.find((x) => !x.reached) || null,
      reached: list.filter((x) => x.reached).length,
    };
  }

  function suggestNext() {
    const done = getDone();
    const c = course();
    const out = [];
    const anyLesson = c.lessons.some((l) => done.has(l.id));

    const nextLesson = c.lessons.find((l) => !done.has(l.id));
    if (nextLesson) {
      const lvl = c.levels[nextLesson.level] || { icon: "", name: "" };
      out.push({
        icon: anyLesson ? "📖" : "🚀",
        title: nextLesson.title,
        why: anyLesson
          ? "The next lesson on the path, in " + lvl.icon + " " + lvl.name + "."
          : "Everybody starts here, including people who have never opened a terminal.",
        href: UP + nextLesson.href,
        cta: anyLesson ? "Continue" : "Start at the beginning",
      });
    }

    const best = bestScores();
    for (let i = c.levels.length - 1; i >= 0; i--) {
      const [have, total] = levelProgress(i);
      if (total > 0 && have >= total && best[c.levels[i].quiz] === undefined) {
        out.push({
          icon: "🧠",
          title: c.levels[i].name + " quiz",
          why: "You finished the level. Ten minutes of testing yourself beats an hour of re-reading.",
          href: UP + "quiz.html",
          cta: "Take the quiz",
        });
        break;
      }
    }

    const [l1have, l1total] = levelProgress(1);
    if (l1total > 0 && l1have >= l1total) {
      const nextProject = c.projects.find((p) => !done.has(p.id));
      if (nextProject) {
        out.push({
          icon: "🔨",
          title: nextProject.title,
          why: projectsDoneCount() === 0
            ? "Lessons teach the language. Projects teach programming. The gap between them is the whole job."
            : "The next build in the workshop.",
          href: UP + nextProject.href,
          cta: "Open the spec",
        });
      }
    }

    if (anyLesson && countDone("pypit-") < c.pitTotal && lessonsDoneCount() >= 5) {
      out.push({
        icon: "🐍",
        title: "The Snake Pit",
        why: countDone("pypit-") === 0
          ? "Broken and baffling programs, ranked from Egg to Basilisk. Predict, fix, and find the bug."
          : countDone("pypit-") + " of " + c.pitTotal + " puzzles solved so far.",
        href: UP + "pit.html",
        cta: "Enter the pit",
      });
    }

    if (anyLesson && !getFlags()["duel-won"]) {
      out.push({
        icon: "⚔️",
        title: "The Insult Compiler",
        why: "Error messages are the thing beginners fear most, so we turned reading them into a swordfight.",
        href: UP + "insults.html",
        cta: "Fight",
      });
    }

    if (!nextLesson) {
      out.push({
        icon: "🦀",
        title: "The Rusty School",
        why: "You have finished Python. The sister school starts from zero again, and the contrast teaches you more about Python than another Python course would.",
        href: campus + "index.html",
        cta: "Visit the Rusty School",
      });
    }

    return out;
  }

  function renderMilestones(mount) {
    const state = milestoneState();
    mount.innerHTML = "";
    const head = document.createElement("div");
    head.className = "ms-head";
    head.innerHTML = "<h2>Milestones</h2><span class='ms-count'></span>";
    head.querySelector(".ms-count").textContent =
      state.reached + " of " + MILESTONES.length + " reached";
    mount.appendChild(head);

    const track = document.createElement("div");
    track.className = "ms-track";
    state.list.forEach((x) => {
      const isCurrent = state.current === x;
      const el = document.createElement("div");
      el.className = "ms" + (x.reached ? " reached" : isCurrent ? " current" : " locked");
      const icon = document.createElement("span");
      icon.className = "ms-icon";
      icon.textContent = x.m.icon;
      const body = document.createElement("div");
      body.className = "ms-body";
      const name = document.createElement("span");
      name.className = "ms-name";
      name.textContent = x.m.name;
      const meta = document.createElement("span");
      meta.className = "ms-meta";
      meta.textContent = x.reached ? "reached" : x.have + " of " + x.total;
      body.appendChild(name);
      body.appendChild(meta);
      if (isCurrent || x.reached) {
        const blurb = document.createElement("p");
        blurb.className = "ms-blurb";
        blurb.textContent = x.m.blurb;
        body.appendChild(blurb);
      }
      el.appendChild(icon);
      el.appendChild(body);
      track.appendChild(el);
    });
    mount.appendChild(track);
  }

  function renderNextStep(mount) {
    const picks = suggestNext();
    if (!picks.length) return false;
    const primary = picks[0];
    mount.innerHTML = "";

    const card = document.createElement("div");
    card.className = "next-step";
    const kicker = document.createElement("span");
    kicker.className = "ns-kicker";
    kicker.textContent = "What to do next";
    card.appendChild(kicker);

    const row = document.createElement("div");
    row.className = "ns-row";
    const icon = document.createElement("span");
    icon.className = "ns-icon";
    icon.textContent = primary.icon;
    const text = document.createElement("div");
    text.className = "ns-text";
    const h3 = document.createElement("h3");
    h3.textContent = primary.title;
    const why = document.createElement("p");
    why.textContent = primary.why;
    text.appendChild(h3);
    text.appendChild(why);
    const go = document.createElement("a");
    go.className = "btn btn-primary btn-small";
    go.href = primary.href;
    go.textContent = primary.cta + " →";
    row.appendChild(icon);
    row.appendChild(text);
    row.appendChild(go);
    card.appendChild(row);

    if (picks.length > 1) {
      const also = document.createElement("div");
      also.className = "ns-also";
      also.appendChild(document.createTextNode("Or: "));
      picks.slice(1, 3).forEach((s, i) => {
        if (i) also.appendChild(document.createTextNode(" · "));
        const a = document.createElement("a");
        a.href = s.href;
        a.textContent = s.icon + " " + s.title;
        also.appendChild(a);
      });
      card.appendChild(also);
    }

    mount.appendChild(card);
    return true;
  }

  function checkMilestones(announce) {
    const now = milestoneState().list.filter((x) => x.reached).map((x) => x.m.id);
    let seen;
    try { seen = JSON.parse(localStorage.getItem("py-milestones") || "[]"); }
    catch { seen = []; }
    const fresh = now.filter((id) => !seen.includes(id));
    localStorage.setItem("py-milestones", JSON.stringify(now));
    if (announce && fresh.length) {
      const m = MILESTONES.find((x) => x.id === fresh[0]);
      toast("🏁 Milestone reached: " + m.icon + " " + m.name, m.blurb);
    }
  }

  function refreshGuidance(announce) {
    const msMount = document.getElementById("milestones");
    if (msMount) renderMilestones(msMount);
    const nsMount = document.getElementById("next-step");
    if (nsMount) renderNextStep(nsMount);
    const cont = document.getElementById("continue");
    if (cont) {
      const started = lessonsDoneCount() > 0 || projectsDoneCount() > 0 ||
                      countDone("pypit-") > 0;
      const body = cont.querySelector(".continue-body");
      if (started && body && renderNextStep(body)) cont.hidden = false;
      else cont.hidden = true;
    }
    checkMilestones(announce);
  }

  function initGuidance() {
    const wrap = document.querySelector(".progress-wrap");
    if (wrap && !document.getElementById("next-step")) {
      const ns = document.createElement("div");
      ns.id = "next-step";
      wrap.insertAdjacentElement("afterend", ns);
      // The milestone spine belongs to the curriculum. The workshop and
      // the pit already have their own progress shapes.
      if (/\/python\/learn\//.test(location.pathname)) {
        const ms = document.createElement("section");
        ms.id = "milestones";
        ms.className = "section ms-section";
        ns.insertAdjacentElement("afterend", ms);
      }
    }
    refreshGuidance(false);
  }

  /* ================= quiz engine ================= */
  function initQuizzes() {
    const rootEl = document.getElementById("quiz-root");
    if (!rootEl || !window.PY_QUIZZES) return;
    renderQuizMenu(rootEl);
  }

  function renderQuizMenu(rootEl) {
    const best = bestScores();
    rootEl.innerHTML = "";
    const grid = document.createElement("div");
    grid.className = "grid cols-3";
    window.PY_QUIZZES.forEach((quiz) => {
      const card = document.createElement("div");
      card.className = "card";
      const bestLine = best[quiz.id] !== undefined
        ? '<p class="best-score">Best score: ' + best[quiz.id] + "/" + quiz.questions.length + "</p>"
        : '<p class="best-score">Not attempted yet</p>';
      card.innerHTML =
        '<span class="badge ' + quiz.levelClass + '">' + quiz.level + "</span>" +
        "<h3>" + quiz.title + "</h3><p>" + quiz.blurb + "</p>" + bestLine;
      const btn = document.createElement("button");
      btn.className = "btn btn-primary btn-small";
      btn.style.marginTop = "12px";
      btn.textContent = "Start quiz →";
      btn.addEventListener("click", () => runQuiz(rootEl, quiz));
      card.appendChild(btn);
      grid.appendChild(card);
    });
    rootEl.appendChild(grid);
  }

  function runQuiz(rootEl, quiz) {
    let index = 0;
    let score = 0;

    function showQuestion() {
      const q = quiz.questions[index];
      rootEl.innerHTML = "";
      const card = document.createElement("div");
      card.className = "card quiz-card";
      card.innerHTML =
        '<div class="quiz-meta"><span>' + quiz.title + "</span><span>Question " +
        (index + 1) + " of " + quiz.questions.length + " · Score " + score + "</span></div>" +
        '<div class="quiz-q">' + q.q + "</div>" +
        (q.code ? "<pre><code>" + highlightPython(q.code) + "</code></pre>" : "");
      const opts = document.createElement("div");
      opts.className = "quiz-opts";
      q.options.forEach((text, i) => {
        const opt = document.createElement("button");
        opt.className = "quiz-opt";
        opt.type = "button";
        opt.innerHTML = text;
        opt.addEventListener("click", (e) => {
          [...opts.children].forEach((b) => (b.disabled = true));
          const right = i === q.answer;
          opt.classList.add(right ? "correct" : "wrong");
          opts.children[q.answer].classList.add("correct");
          if (right) { score++; confetti(e.clientX, e.clientY); }
          const explain = document.createElement("div");
          explain.className = "quiz-explain";
          explain.innerHTML = "<strong>" + (right ? "Correct! " : "Not quite. ") + "</strong>" + q.explain;
          card.appendChild(explain);
          const next = document.createElement("button");
          next.className = "btn btn-primary btn-small";
          next.style.marginTop = "14px";
          next.textContent = index + 1 < quiz.questions.length ? "Next question →" : "See my score →";
          next.addEventListener("click", () => {
            index++;
            if (index < quiz.questions.length) showQuestion();
            else showScore();
          });
          card.appendChild(next);
        });
        opts.appendChild(opt);
      });
      card.appendChild(opts);
      rootEl.appendChild(card);
      card.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }

    function showScore() {
      const total = quiz.questions.length;
      const best = bestScores();
      if (score > (best[quiz.id] || 0)) {
        best[quiz.id] = score;
        localStorage.setItem("rusty-quiz-best", JSON.stringify(best));
        renderXp();
        checkNewAchievements();
        pushProgress();
      }
      const pct = score / total;
      const verdict =
        pct === 1 ? "Perfect score. Monty is speechless, which for a snake is normal, but still. 🐍"
        : pct >= 0.7 ? "Strong work. You clearly read the lessons instead of skimming them. 🎉"
        : pct >= 0.4 ? "Decent start. One re-read and this will click. 📖"
        : "Wrong answers are the raw material of learning. Go again. 💪";
      rootEl.innerHTML = "";
      const card = document.createElement("div");
      card.className = "card quiz-card quiz-score";
      card.innerHTML = "<h3>" + quiz.title + ": results</h3>" +
        '<div class="big">' + score + " / " + total + "</div><p>" + verdict + "</p>";
      const actions = document.createElement("div");
      actions.className = "quiz-actions";
      const again = document.createElement("button");
      again.className = "btn btn-primary btn-small";
      again.textContent = "Try again";
      again.addEventListener("click", () => runQuiz(rootEl, quiz));
      const menu = document.createElement("button");
      menu.className = "btn btn-ghost btn-small";
      menu.textContent = "All quizzes";
      menu.addEventListener("click", () => renderQuizMenu(rootEl));
      actions.appendChild(again);
      actions.appendChild(menu);
      card.appendChild(actions);
      rootEl.appendChild(card);
      if (pct >= 0.7) confetti(window.innerWidth / 2, 160);
    }

    showQuestion();
  }

  /* ================= the Snake Pit ================= */
  const PIT_TIERS = [
    ["egg", "Egg", "you have not hatched yet: printing, names, arithmetic"],
    ["garter", "Garter Snake", "strings, conditions, loops that end"],
    ["rattler", "Rattler", "lists, dicts, and the mutation traps"],
    ["boa", "Boa", "functions, scope, arguments that bite"],
    ["cobra", "Cobra", "comprehensions, classes, iterators"],
    ["basilisk", "Basilisk", "closures, decorators, references, the deep magic"],
  ];
  const PIT_TYPE = {
    predict: "🔮 Predict the output",
    fix: "🔧 Fix it",
    bug: "🐛 Find the bug",
  };

  function initPit() {
    const rootEl = document.getElementById("pit-root");
    if (!rootEl || !window.PY_PIT) return;
    const puzzles = window.PY_PIT;
    window.PY_PIT_TOTAL = puzzles.length;

    PIT_TIERS.forEach(([key, name, subtitle]) => {
      const mine = puzzles.filter((p) => p.tier === key);
      if (!mine.length) return;
      const section = document.createElement("section");
      section.className = "section belt-section";
      section.dataset.belt = key;
      const h2 = document.createElement("h2");
      h2.innerHTML =
        '<span class="belt-badge belt-' + key + '">' + name + "</span> " +
        '<span class="muted small">' + subtitle + "</span> " +
        '<span class="belt-count muted small"></span>';
      section.appendChild(h2);

      mine.forEach((p) => {
        const card = document.createElement("article");
        card.className = "card dojo-card";
        card.dataset.puzzle = "pypit-" + p.id;
        const head = document.createElement("div");
        head.className = "dojo-head";
        head.innerHTML = '<span class="dojo-type">' + (PIT_TYPE[p.type] || p.type) + "</span>";
        const h3 = document.createElement("h3");
        h3.textContent = p.title;
        head.appendChild(h3);
        card.appendChild(head);

        const task = document.createElement("p");
        task.className = "muted dojo-task";
        task.textContent = p.task;
        card.appendChild(task);

        const pre = document.createElement("pre");
        const code = document.createElement("code");
        code.textContent = p.code;
        pre.appendChild(code);
        card.appendChild(pre);

        const actions = document.createElement("div");
        actions.className = "dojo-actions";
        const train = document.createElement("button");
        train.type = "button";
        train.className = "btn btn-ghost btn-small";
        train.textContent = "🐍 Open in the Playground";
        train.addEventListener("click", () => {
          localStorage.setItem("py-pg-pending", p.code);
          location.href = (IN_SUB ? "../" : "") + "playground.html";
        });
        actions.appendChild(train);

        const hint = document.createElement("details");
        hint.className = "hint";
        hint.innerHTML = "<summary>Hint</summary><div class=\"hint-body\"><p></p></div>";
        hint.querySelector("p").textContent = p.hint;
        actions.appendChild(hint);

        const sol = document.createElement("details");
        sol.className = "hint dojo-solution";
        sol.innerHTML = "<summary>" +
          (p.type === "predict" ? "Reveal the answer" : "Reveal the solution") +
          "</summary><div class=\"hint-body\"></div>";
        const body = sol.querySelector(".hint-body");
        if (p.solution) {
          const spre = document.createElement("pre");
          const scode = document.createElement("code");
          scode.textContent = p.solution;
          spre.appendChild(scode);
          body.appendChild(spre);
        }
        const outLabel = document.createElement("p");
        outLabel.className = "muted small";
        outLabel.textContent = p.type === "predict" ? "It prints:" : "The fixed version prints:";
        body.appendChild(outLabel);
        const opre = document.createElement("pre");
        opre.className = "out";
        const ocode = document.createElement("code");
        ocode.className = "nohl";
        ocode.textContent = p.expected;
        opre.appendChild(ocode);
        body.appendChild(opre);
        const expl = document.createElement("p");
        expl.textContent = p.explain;
        body.appendChild(expl);
        actions.appendChild(sol);

        const solved = document.createElement("button");
        solved.type = "button";
        solved.className = "btn btn-ghost btn-small dojo-solved-btn";
        solved.addEventListener("click", (e) => {
          const set = getDone();
          const id = card.dataset.puzzle;
          if (set.has(id)) set.delete(id);
          else { set.add(id); confetti(e.clientX, e.clientY); }
          saveDone(set);
          renderXp();
          checkNewAchievements();
          pushProgress();
          refreshPit();
          refreshGuidance(true);
        });
        actions.appendChild(solved);
        card.appendChild(actions);
        section.appendChild(card);
      });
      rootEl.appendChild(section);
    });

    function refreshPit() {
      const done = getDone();
      let total = 0, solvedCount = 0;
      document.querySelectorAll(".dojo-card").forEach((card) => {
        total++;
        const isDone = done.has(card.dataset.puzzle);
        if (isDone) solvedCount++;
        card.classList.toggle("solved", isDone);
        const btn = card.querySelector(".dojo-solved-btn");
        btn.textContent = isDone ? "✓ Solved" : "Mark solved";
        btn.classList.toggle("is-solved", isDone);
      });
      document.querySelectorAll(".belt-section").forEach((section) => {
        const cards = section.querySelectorAll(".dojo-card");
        const solvedHere = [...cards].filter((c) => done.has(c.dataset.puzzle)).length;
        section.querySelector(".belt-count").textContent = solvedHere + " of " + cards.length + " solved";
        const badge = section.querySelector(".belt-badge");
        badge.classList.toggle("earned", solvedHere === cards.length);
      });
      const fill = document.getElementById("pit-fill");
      const label = document.getElementById("pit-label");
      if (fill) fill.style.width = Math.round((solvedCount / total) * 100) + "%";
      if (label) {
        label.textContent = solvedCount === total
          ? "All " + total + " puzzles solved. The Basilisk blinks first. 🏆"
          : solvedCount + " of " + total + " puzzles solved";
      }
    }
    refreshPit();
  }

  /* ================= the Insult Compiler =================
     Swordfighting, but the insults are Python error messages and the
     comebacks are the fixes. Get the right riposte and you land a hit.
     Error-message literacy is the single most useful beginner skill
     there is, so we made it a duel. */
  function initDuel() {
    const rootEl = document.getElementById("duel-root");
    if (!rootEl || !window.PY_INSULTS) return;
    startDuel(rootEl);
  }

  function shuffle(arr) {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  }

  function startDuel(rootEl) {
    const rounds = shuffle(window.PY_INSULTS).slice(0, 10);
    let i = 0, hp = 5, theirHp = rounds.length, flawless = true;

    function draw() {
      const round = rounds[i];
      rootEl.innerHTML = "";
      const box = document.createElement("div");
      box.className = "duel";
      box.innerHTML =
        '<div class="duel-hp">' +
        '<div class="you"><span>You · ' + hp + " pride left</span>" +
        '<div class="hp-bar"><div class="hp-fill" style="width:' + (hp / 5) * 100 + '%"></div></div></div>' +
        '<div class="them"><span>Your opponent · ' + theirHp + " insults left</span>" +
        '<div class="hp-bar"><div class="hp-fill" style="width:' + (theirHp / rounds.length) * 100 + '%"></div></div></div>' +
        "</div>" +
        '<p class="taunt-said">The swordfighter sneers and reads from your terminal:</p>' +
        '<pre class="taunt"></pre>' +
        "<p><strong>Your riposte?</strong> Pick the comeback that actually fixes it.</p>";
      box.querySelector(".taunt").textContent = round.error;
      const list = document.createElement("div");
      list.className = "riposte-list";

      const options = shuffle(round.options.map((text, idx) => ({ text, idx })));
      options.forEach((opt) => {
        const b = document.createElement("button");
        b.type = "button";
        b.className = "riposte";
        b.textContent = opt.text;
        b.addEventListener("click", (e) => {
          [...list.children].forEach((x) => (x.disabled = true));
          const right = opt.idx === round.answer;
          b.classList.add(right ? "hit" : "miss");
          if (right) { theirHp--; confetti(e.clientX, e.clientY); }
          else {
            hp--; flawless = false;
            [...list.children].forEach((x) => {
              if (x.textContent === round.options[round.answer]) x.classList.add("hit");
            });
          }
          const verdict = document.createElement("div");
          verdict.className = "duel-verdict";
          verdict.innerHTML = "<strong>" +
            (right ? "A palpable hit! " : "You flail wildly. ") + "</strong>" + round.explain;
          box.appendChild(verdict);
          const next = document.createElement("button");
          next.className = "btn btn-primary btn-small";
          next.style.marginTop = "14px";
          i++;
          next.textContent = (hp <= 0 || i >= rounds.length) ? "See how you did →" : "Next insult →";
          next.addEventListener("click", () => {
            if (hp <= 0 || i >= rounds.length) finish();
            else draw();
          });
          box.appendChild(next);
        });
        list.appendChild(b);
      });
      box.appendChild(list);
      rootEl.appendChild(box);
    }

    function finish() {
      const won = theirHp <= 0 || (hp > 0 && i >= rounds.length);
      if (won) {
        flag("duel-won");
        if (flawless) flag("duel-flawless");
        checkNewAchievements();
        pushProgress();
      }
      rootEl.innerHTML = "";
      const card = document.createElement("div");
      card.className = "card duel-score";
      const landed = rounds.length - theirHp;
      card.innerHTML =
        "<h3>" + (won ? "You win the duel" : "You are laughed off the beach") + "</h3>" +
        '<div class="big">' + landed + " / " + rounds.length + "</div>" +
        "<p>" + (flawless && won
          ? "Flawless. Not one wild swing. The swordmaster asks where you trained."
          : won
          ? "Victory, with a couple of scratches. That is how everybody wins their first duel."
          : "Your opponent bows insincerely. Read the tracebacks again and come back for them.") +
        "</p>";
      const actions = document.createElement("div");
      actions.className = "quiz-actions";
      const again = document.createElement("button");
      again.className = "btn btn-primary btn-small";
      again.textContent = "Fight again";
      again.addEventListener("click", () => startDuel(rootEl));
      actions.appendChild(again);
      card.appendChild(actions);
      rootEl.appendChild(card);
      if (won) confetti(window.innerWidth / 2, 160);
      renderXp();
    }

    draw();
  }

  /* ================= playground page ================= */
  const PG_EXAMPLES = {
    hello: 'print("Hello, world!")\nprint("I am a snake and I am fine. 🐍")\n',
    variables:
      'name = "Guybrush"\nyears_at_sea = 3\ngrog_level = 7.5\n\nprint(f"{name} has sailed for {years_at_sea} years.")\nprint(f"Grog level: {grog_level} out of 10")\n\nyears_at_sea = years_at_sea + 1\nprint(f"A year passes. Now {years_at_sea}.")\n',
    fizzbuzz:
      'for n in range(1, 21):\n    if n % 15 == 0:\n        print("FizzBuzz")\n    elif n % 3 == 0:\n        print("Fizz")\n    elif n % 5 == 0:\n        print("Buzz")\n    else:\n        print(n)\n',
    lists:
      'inventory = ["rubber chicken", "map", "grog", "sword"]\n\ninventory.append("mints")\ninventory.remove("grog")\n\nfor i, item in enumerate(inventory, start=1):\n    print(f"{i}. {item}")\n\nprint(f"You carry {len(inventory)} things.")\n',
    dicts:
      'crew = {"Guybrush": "captain", "Elaine": "governor", "Otis": "prisoner"}\n\nfor name, job in crew.items():\n    print(f"{name:10} -> {job}")\n\ncrew["Meathook"] = "first mate"\nprint("Roster size:", len(crew))\nprint("Is Otis aboard?", "Otis" in crew)\n',
    input:
      'name = input("What is your name? ")\nprint(f"Nice to meet you, {name}.")\n\nage = input("How many years have you programmed? ")\nyears = int(age)\nprint(f"In ten years that will be {years + 10}.")\n',
    classes:
      'class Pirate:\n    def __init__(self, name, insults=0):\n        self.name = name\n        self.insults = insults\n\n    def learn(self, insult):\n        self.insults += 1\n        print(f"{self.name} learns: {insult!r}")\n\n    def __repr__(self):\n        return f"Pirate({self.name!r}, insults={self.insults})"\n\n\nguy = Pirate("Guybrush")\nguy.learn("You fight like a dairy farmer!")\nguy.learn("I have spoken to apes more polite than you.")\nprint(guy)\n',
    errors:
      '# Every line here is broken on purpose. Fix them one at a time\n# and press run after each fix. Read the LAST line of the error.\n\nnumbers = [1, 2, 3]\nprint(numbers[5])\n\n# print("unclosed string)\n# print(1 + "one")\n# print(undefined_name)\n',
  };

  function initPlayground() {
    const editor = document.getElementById("pg-editor");
    if (!editor) return;
    const output = document.getElementById("pg-output");
    const runBtn = document.getElementById("pg-run");
    const picker = document.getElementById("pg-example");
    const status = document.getElementById("pg-status");

    const pending = localStorage.getItem("py-pg-pending");
    if (pending) {
      editor.value = pending;
      localStorage.removeItem("py-pg-pending");
    } else {
      editor.value = localStorage.getItem("py-pg-draft") || PG_EXAMPLES.hello;
    }
    editor.addEventListener("input", () => {
      try { localStorage.setItem("py-pg-draft", editor.value); } catch {}
    });

    if (picker) {
      picker.addEventListener("change", () => {
        editor.value = PG_EXAMPLES[picker.value] || PG_EXAMPLES.hello;
        editor.focus();
      });
    }

    editor.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        e.preventDefault();
        const s = editor.selectionStart;
        editor.setRangeText("    ", s, editor.selectionEnd, "end");
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        run();
      }
    });

    function run() {
      if (status) { status.textContent = "running…"; status.className = "pg-status busy"; }
      executePython(editor.value, output, runBtn, "").then(() => {
        if (status) { status.textContent = "ready"; status.className = "pg-status ready"; }
      });
    }
    runBtn.addEventListener("click", run);

    // Warm the interpreter up in the background so the first run feels instant.
    if (navigator.connection && navigator.connection.saveData) return;
    setTimeout(() => {
      getPyodide((msg) => { if (status) status.textContent = msg.toLowerCase(); })
        .then(() => { if (status) { status.textContent = "python 3.14 ready"; status.className = "pg-status ready"; } })
        .catch(() => {});
    }, 600);
  }

  /* ================= glossary filter ================= */
  function initGlossary() {
    const input = document.getElementById("gloss-filter");
    const list = document.getElementById("gloss-list");
    if (!input || !list) return;
    const terms = [];
    let dt = null;
    [...list.children].forEach((el) => {
      if (el.tagName === "DT") {
        dt = { term: el, defs: [], text: el.textContent.toLowerCase() };
        terms.push(dt);
      } else if (el.tagName === "DD" && dt) {
        dt.defs.push(el);
        dt.text += " " + el.textContent.toLowerCase();
      }
    });
    const countEl = document.getElementById("gloss-count");
    const emptyEl = document.getElementById("gloss-empty");
    const total = terms.length;
    function apply() {
      const q = input.value.trim().toLowerCase();
      let shown = 0;
      terms.forEach((t) => {
        const match = !q || t.text.includes(q);
        t.term.hidden = !match;
        t.defs.forEach((d) => (d.hidden = !match));
        if (match) shown++;
      });
      if (countEl) {
        countEl.textContent = q ? shown + " of " + total + " terms"
                                : total + " terms, every one of them defined in a lesson";
      }
      if (emptyEl) emptyEl.hidden = shown !== 0;
    }
    input.addEventListener("input", apply);
    apply();
  }

  /* ================= tabs ================= */
  function initTabs() {
    const tabs = document.querySelectorAll(".tab-btn[data-tab]");
    if (!tabs.length) return;
    function activate(id, updateHash) {
      tabs.forEach((t) => t.classList.toggle("active", t.dataset.tab === id));
      document.querySelectorAll(".tab-panel").forEach((p) =>
        p.classList.toggle("active", p.id === "tab-" + id));
      if (updateHash) history.replaceState(null, "", "#" + id);
    }
    tabs.forEach((t) => t.addEventListener("click", () => activate(t.dataset.tab, true)));
    const fromHash = location.hash.slice(1);
    if (fromHash && document.getElementById("tab-" + fromHash)) activate(fromHash, false);
  }

  /* ================= account sync (shared with the Rusty School) ================= */
  let signedIn = false;
  function readJson(key, fallback) {
    try { return JSON.parse(localStorage.getItem(key) || fallback); }
    catch { return JSON.parse(fallback); }
  }
  function localProgress() {
    return {
      done: readJson("rusty-done", "[]"),
      counted: readJson("rusty-counted", "[]"),
      quizBest: readJson("rusty-quiz-best", "{}"),
    };
  }
  function mergeProgress(a, b) {
    const done = [...new Set([...(a.done || []), ...(b.done || [])])];
    const counted = [...new Set([...(a.counted || []), ...(b.counted || [])])];
    const quizBest = {};
    const keys = new Set([...Object.keys(a.quizBest || {}), ...Object.keys(b.quizBest || {})]);
    keys.forEach((k) => {
      quizBest[k] = Math.max((a.quizBest || {})[k] || 0, (b.quizBest || {})[k] || 0);
    });
    return { done, counted, quizBest };
  }
  function saveLocalProgress(p) {
    localStorage.setItem("rusty-done", JSON.stringify(p.done));
    localStorage.setItem("rusty-counted", JSON.stringify(p.counted));
    localStorage.setItem("rusty-quiz-best", JSON.stringify(p.quizBest));
  }
  function pushProgress() {
    if (!signedIn) return;
    fetch("/api/progress", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(localProgress()),
      keepalive: true,
    }).catch(() => {});
  }
  async function syncProgress(timeoutMs) {
    try {
      const ctrl = new AbortController();
      const timer = setTimeout(() => ctrl.abort(), timeoutMs || 1500);
      const resp = await fetch("/api/me", { signal: ctrl.signal });
      clearTimeout(timer);
      if (!resp.ok) return null;
      const me = await resp.json();
      if (!me.signedIn) return me;
      signedIn = true;
      const merged = mergeProgress(localProgress(), me.progress || {});
      saveLocalProgress(merged);
      if (JSON.stringify(merged) !== JSON.stringify(me.progress)) pushProgress();
      me.progress = merged;
      return me;
    } catch {
      return null;
    }
  }

  /* ================= account page =================
     The same session, the same database row and the same API as the
     Rusty School: one campus, one account. The only Python-specific
     part is `?from=python` on the sign-in links, which the OAuth
     callback uses to send you back to this page instead of the other
     school's. */
  const AUTH_ERRORS = {
    "state-mismatch": "The sign-in attempt expired or was tampered with. Please try again.",
    "token-exchange-failed": "The provider rejected the sign-in. Please try again.",
    "profile-fetch-failed": "We couldn't read your public profile. Please try again.",
    "github-not-configured": "GitHub sign-in isn't switched on yet.",
    "google-not-configured": "Google sign-in isn't switched on yet.",
  };

  function progressSummary(done) {
    const py = done.filter((d) => d.startsWith("py-") && !d.startsWith("py-quiz")).length;
    const pit = done.filter((d) => d.startsWith("pypit-")).length;
    const build = done.filter((d) => d.startsWith("pybuild-")).length;
    const rust = done.filter((d) =>
      !d.startsWith("py-") && !d.startsWith("pypit-") && !d.startsWith("pybuild-")).length;
    const bits = [];
    const plural = (n, one, many) => n + " " + (n === 1 ? one : many);
    if (py) bits.push("📚 <strong>" + plural(py, "Python lesson", "Python lessons") + "</strong>");
    if (pit) bits.push("🐍 <strong>" + plural(pit, "pit puzzle", "pit puzzles") + "</strong>");
    if (build) bits.push("🔨 <strong>" + plural(build, "project", "projects") + "</strong>");
    if (rust) bits.push("🦀 <strong>" + plural(rust, "Rusty School item", "Rusty School items") + "</strong>");
    if (!bits.length) return "Nothing synced yet. Finish a lesson and it appears here.";
    const last = bits.pop();
    return (bits.length ? bits.join(", ") + " and " + last : last) + " synced to your account.";
  }

  function initAccount(me) {
    const root = document.getElementById("account-root");
    if (!root) return;

    if (me && me.signedIn) {
      root.innerHTML = "";
      root.appendChild(document.getElementById("tpl-signed-in").content.cloneNode(true));
      const avatar = document.getElementById("acct-avatar");
      if (me.avatar) avatar.src = me.avatar; else avatar.style.display = "none";
      document.getElementById("acct-name").textContent = me.name || "Programmer";
      document.getElementById("acct-provider").textContent = me.provider;
      document.getElementById("acct-progress").innerHTML =
        progressSummary((me.progress && me.progress.done) || []);
      document.getElementById("acct-sync-note").textContent =
        "Progress syncs automatically whenever you finish a lesson, puzzle or quiz on any " +
        "signed-in device, at either school.";

      document.getElementById("btn-signout").addEventListener("click", () => {
        fetch("/api/auth/logout", { method: "POST" }).finally(() => location.reload());
      });
      document.getElementById("btn-delete").addEventListener("click", () => {
        const sure = confirm(
          "Delete your account? Your name, picture, and synced progress will be " +
          "erased from our database immediately and permanently."
        );
        if (!sure) return;
        fetch("/api/me", { method: "DELETE" }).finally(() => {
          location.href = "account.html";
        });
      });
      return;
    }

    root.innerHTML = "";
    root.appendChild(document.getElementById("tpl-signed-out").content.cloneNode(true));

    const params = new URLSearchParams(location.search);
    const err = params.get("error");
    if (err) {
      const el = document.getElementById("auth-error");
      let msg = "⚠️ " + (AUTH_ERRORS[err] || "Sign-in failed. Please try again.");
      const from = params.get("from");
      const detail = params.get("detail");
      if (from) msg += " [" + from + (detail ? ": " + detail : "") + "]";
      el.textContent = msg;
      el.hidden = false;
    }

    fetch("/api/auth/providers")
      .then((r) => (r.ok ? r.json() : {}))
      .catch(() => ({}))
      .then((providers) => {
        const row = document.getElementById("provider-buttons");
        const note = document.getElementById("provider-note");
        let any = false;
        if (providers.github) {
          any = true;
          row.insertAdjacentHTML("beforeend",
            '<a class="btn btn-primary" href="/api/auth/github?from=python">Sign in with GitHub</a>');
        }
        if (providers.google) {
          any = true;
          row.insertAdjacentHTML("beforeend",
            '<a class="btn btn-ghost" href="/api/auth/google?from=python">Sign in with Google</a>');
        }
        if (!any) note.hidden = false;
      });
  }

  /* ================= campus search =================
     The very same overlay the Rusty School uses, living at the campus
     root and searching both schools at once. */
  function initSearch() {
    if (document.querySelector("script[data-campus-search]")) return;
    const s = document.createElement("script");
    s.src = campus + "assets/search.js";
    s.defer = true;
    s.setAttribute("data-campus-search", "");
    document.head.appendChild(s);
  }

  /* ================= boot ================= */
  document.addEventListener("DOMContentLoaded", async () => {
    initTheme();
    initNav();
    initSearch();
    initPit();
    initCode();
    initTabs();
    const themeBtn = document.querySelector(".theme-toggle");
    if (themeBtn) themeBtn.addEventListener("click", toggleTheme);

    const me = await syncProgress(1500);
    initProgress();
    renderXp();
    initGuidance();
    initAccount(me);
    initAchievements();
    initQuizzes();
    initDuel();
    initPlayground();
    initGlossary();
    checkNewAchievements();
  });
})();
