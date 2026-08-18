/* ============================================================
   The Bridge: mission runner and auto-grading

   The campus already knew how to RUN learner code. What it could not do
   was CHECK it: the Dojo and the Snake Pit both end with "Mark solved",
   which takes the learner's word for it. This file is the difference.

   How grading works, in both languages:

     1. Take what the learner wrote.
     2. Append the mission's checker, which exercises their function and
        prints one line per objective in the wire format
            BRIDGE|<index>|<PASS or FAIL>|<detail>
     3. Run the combined program.
          Python  Pyodide, in this browser, no server, no cost
          Rust    POST /api/run, the same playground proxy the lessons use
     4. Split the output: BRIDGE| lines drive the objective list, and
        everything else is shown back as the learner's own output, so
        print-debugging still works inside a graded mission.

   The checker runs AFTER the learner's code in the same program, which is
   the whole trick and also the one thing to be careful about: a learner
   who defines main() in Rust, or calls exit() in Python, breaks it. Both
   cases are detected and explained rather than reported as a mystery.
   ============================================================ */
(function () {
  "use strict";

  const PYODIDE_URL = "https://cdn.jsdelivr.net/pyodide/v314.0.5/full/";
  const WIRE = /^BRIDGE\|(\d+)\|(PASS|FAIL)\|([\s\S]*)$/;

  /* ---------------- shared progress (campus keys) ---------------- */
  function getDone() {
    try { return new Set(JSON.parse(localStorage.getItem("rusty-done") || "[]")); }
    catch { return new Set(); }
  }
  function saveDone(set) {
    localStorage.setItem("rusty-done", JSON.stringify([...set]));
  }
  function markCleared(id) {
    const set = getDone();
    if (set.has(id)) return false;
    set.add(id);
    saveDone(set);
    // The campus sync in app.js pushes on its own triggers; nudge it here
    // so a cleared mission is not lost if the tab closes.
    fetch("/api/progress", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        done: [...set],
        counted: JSON.parse(localStorage.getItem("rusty-counted") || "[]"),
        quizBest: JSON.parse(localStorage.getItem("rusty-quiz-best") || "{}"),
      }),
      keepalive: true,
    }).catch(() => {});
    return true;
  }

  /* ---------------- draft persistence ----------------
     Losing half an hour of work to an accidental refresh is the fastest
     way to make somebody stop using a thing. */
  function draftKey(mission, lang) { return "bridge-draft-" + mission + "-" + lang; }
  function saveDraft(mission, lang, code) {
    try { localStorage.setItem(draftKey(mission, lang), code); } catch {}
  }
  function loadDraft(mission, lang) {
    try { return localStorage.getItem(draftKey(mission, lang)); } catch { return null; }
  }

  /* ================= the Python engine (Pyodide) ================= */
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
      if (onProgress) onProgress("downloading Python (about 12 MB, once)");
      if (!window.loadPyodide) await loadScript(PYODIDE_URL + "pyodide.js");
      if (onProgress) onProgress("starting the interpreter");
      return await window.loadPyodide({ indexURL: PYODIDE_URL });
    })().catch((err) => { pyodidePromise = null; throw err; });
    return pyodidePromise;
  }

  // Runs learner code then checker, capturing everything printed.
  // A learner exception during their own definitions is reported as a
  // setup failure rather than silently failing all five objectives.
  const PY_HARNESS = `
import sys, io, traceback, builtins

_buf = io.StringIO()
_saved_out, _saved_err = sys.stdout, sys.stderr
sys.stdout = _buf
sys.stderr = _buf
_setup_error = ""

try:
    exec(compile(_user_code, "your_console.py", "exec"), globals())
except SystemExit:
    _setup_error = ("Your code called exit(), which stops the program before ARCHIE "
                    "can test anything. Remove it.")
except BaseException as _e:
    _tb = _e.__traceback__
    _setup_error = "".join(traceback.format_exception(
        type(_e), _e, _tb.tb_next if _tb is not None and _tb.tb_next else _tb))
else:
    try:
        exec(compile(_checker_code, "archie_checker.py", "exec"), globals())
    except BaseException as _e:
        _setup_error = "The checker could not run: " + repr(_e)

sys.stdout, sys.stderr = _saved_out, _saved_err
_output = _buf.getvalue()
`;

  async function runPython(userCode, checker, onStatus) {
    const py = await getPyodide(onStatus);
    if (onStatus) onStatus("running diagnostics");
    py.globals.set("_user_code", userCode);
    py.globals.set("_checker_code", checker);
    await py.runPythonAsync(PY_HARNESS);
    return {
      output: py.globals.get("_output") || "",
      setupError: py.globals.get("_setup_error") || "",
    };
  }

  /* ================= the Rust engine (playground proxy) ================= */
  async function runRust(userCode, checker, onStatus) {
    if (/fn\s+main\s*\(/.test(userCode)) {
      return {
        output: "",
        setupError:
          "Your code defines main(). ARCHIE supplies main() for the objectives, so " +
          "two of them collide and nothing compiles. Write the function only.",
      };
    }
    if (onStatus) onStatus("compiling on the playground");
    const resp = await fetch("/api/run", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ code: userCode + "\n" + checker, edition: "2021" }),
    });
    const result = await resp.json().catch(() => ({ error: "unreadable response" }));
    if (result.error) return { output: "", setupError: "⚠️ " + result.error };
    if (!result.success) {
      return { output: result.stdout || "", setupError: cleanRustErrors(result.stderr || "") };
    }
    return { output: (result.stdout || "") + (result.stderr || ""), setupError: "" };
  }

  // The playground's stderr is mostly cargo chatter. Keep the diagnostics.
  const RUST_NOISE = /^(\s+Compiling|\s+Finished|\s+Running|error: could not compile|warning: unused)/;
  function cleanRustErrors(stderr) {
    return stderr
      .split("\n")
      .filter((l) => !RUST_NOISE.test(l))
      .join("\n")
      .trim();
  }

  /* ================= grading ================= */
  function parseResults(output, count) {
    const results = new Array(count).fill(null);
    const leftovers = [];
    output.split("\n").forEach((line) => {
      const m = WIRE.exec(line.trim());
      if (!m) {
        if (line.trim()) leftovers.push(line);
        return;
      }
      const idx = Number(m[1]);
      if (idx >= 0 && idx < count) {
        results[idx] = { pass: m[2] === "PASS", detail: m[3] };
      }
    });
    return { results, output: leftovers.join("\n") };
  }

  /* ================= wiring one mission page ================= */
  function initMission() {
    const missionId = window.BRIDGE_MISSION;
    const data = (window.BRIDGE_MISSIONS || {})[missionId];
    if (!missionId || !data) return;

    const objectivesEl = document.querySelector('[data-role="objectives"]');
    const debriefEl = document.querySelector('[data-role="debrief"]');
    const tabs = [...document.querySelectorAll(".lang-tab")];
    const panels = [...document.querySelectorAll(".lang-panel")];

    // Remember the language the learner last used, campus-wide.
    let active = localStorage.getItem("bridge-lang") || "py";
    if (!data[active]) active = "py";

    function showLang(lang) {
      active = lang;
      localStorage.setItem("bridge-lang", lang);
      tabs.forEach((t) => t.classList.toggle("active", t.dataset.lang === lang));
      panels.forEach((p) => (p.hidden = p.dataset.lang !== lang));
      resetObjectives();
    }
    tabs.forEach((t) => t.addEventListener("click", () => showLang(t.dataset.lang)));

    function resetObjectives() {
      objectivesEl.querySelectorAll("li").forEach((li) => {
        li.className = "";
        li.querySelector(".obj-state").textContent = "•";
        li.querySelector(".obj-detail").textContent = "";
      });
    }

    panels.forEach((panel) => {
      const lang = panel.dataset.lang;
      const spec = data[lang];
      const editor = panel.querySelector(".console-editor");
      const runBtn = panel.querySelector('[data-role="run"]');
      const resetBtn = panel.querySelector('[data-role="reset"]');
      const status = panel.querySelector('[data-role="status"]');
      const archie = panel.querySelector('[data-role="archie"] .archie-body');

      editor.value = loadDraft(missionId, lang) || spec.stub;
      editor.addEventListener("input", () => saveDraft(missionId, lang, editor.value));

      // Tab indents instead of escaping the editor, which is the single
      // most annoying thing about a plain textarea.
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

      resetBtn.addEventListener("click", () => {
        if (!confirm("Put the console back to the starting code? Your version is lost.")) return;
        editor.value = spec.stub;
        saveDraft(missionId, lang, editor.value);
        resetObjectives();
        archie.innerHTML = '<p class="muted">Console reset. Standing by.</p>';
      });

      runBtn.addEventListener("click", run);

      async function run() {
        runBtn.disabled = true;
        status.textContent = "working";
        status.className = "console-status busy";
        archie.innerHTML = '<p class="muted">Running diagnostics…</p>';
        resetObjectives();

        const setStatus = (msg) => { status.textContent = msg; };
        let res;
        try {
          res = lang === "py"
            ? await runPython(editor.value, spec.checker, setStatus)
            : await runRust(editor.value, spec.checker, setStatus);
        } catch (err) {
          res = { output: "", setupError: String((err && err.message) || err) };
        }

        status.textContent = "ready";
        status.className = "console-status ready";
        runBtn.disabled = false;

        if (res.setupError) return reportSetupFailure(archie, res.setupError, lang);
        const parsed = parseResults(res.output, data.objectives.length);
        reportResults(archie, parsed, data, missionId, lang, debriefEl, objectivesEl);
      }
    });

    showLang(active);
    renderMissionState(missionId, objectivesEl, debriefEl);
  }

  function reportSetupFailure(archie, message, lang) {
    archie.innerHTML =
      '<p class="archie-line">Your code did not get as far as the objectives. ' +
      "Here is what stopped it.</p><pre class=\"archie-err\"></pre>" +
      (lang === "py"
        ? '<p class="muted small">Read a traceback from the bottom up: the last line names the problem.</p>'
        : '<p class="muted small">Read the first error first. The ones after it are often knock-on effects.</p>');
    archie.querySelector(".archie-err").textContent = message;
  }

  function reportResults(archie, parsed, data, missionId, lang, debriefEl, objectivesEl) {
    const { results, output } = parsed;
    const total = results.length;
    const passed = results.filter((r) => r && r.pass).length;
    const missing = results.some((r) => r === null);

    objectivesEl.querySelectorAll("li").forEach((li, i) => {
      const r = results[i];
      const state = li.querySelector(".obj-state");
      const detail = li.querySelector(".obj-detail");
      if (!r) {
        li.className = "obj-unknown";
        state.textContent = "?";
        detail.textContent = "no result reported";
        return;
      }
      li.className = r.pass ? "obj-pass" : "obj-fail";
      state.textContent = r.pass ? "✓" : "✗";
      detail.textContent = r.pass ? "" : r.detail;
    });

    let line;
    if (missing) {
      line = "Some objectives reported nothing at all. That usually means your code " +
             "stopped early, or printed something that swallowed my output.";
    } else if (passed === total) {
      line = pickPass(lang);
    } else if (passed === 0) {
      line = "None of the objectives passed. Look at the first one: the failures after " +
             "it are often the same mistake wearing a different hat.";
    } else {
      line = passed + " of " + total + " objectives met. The failures below show the " +
             "input I used and what came back.";
    }

    archie.innerHTML =
      '<p class="archie-line"></p>' +
      '<div class="archie-score"><strong></strong> objectives met</div>' +
      (output ? '<div class="archie-output"><span class="muted small">Your own output</span><pre></pre></div>' : "");
    archie.querySelector(".archie-line").textContent = line;
    archie.querySelector(".archie-score strong").textContent = passed + " / " + total;
    if (output) archie.querySelector(".archie-output pre").textContent = output;

    if (passed === total && !missing) {
      const before = campaignState().rank;
      const langId = missionId + "-" + lang;
      const firstTime = markCleared(langId);
      markCleared(missionId);
      if (debriefEl) debriefEl.hidden = false;
      if (firstTime) confetti();
      renderMissionState(missionId, objectivesEl, debriefEl);
      const after = campaignState();
      if (after.rank[0] > before[0]) {
        setTimeout(() => toast(after.rank[2] + " Promoted to " + after.rank[1],
          "New stations may have opened. Check the mission board."), 900);
      }
    }
  }

  const PASS_LINES = {
    py: [
      "All objectives met. The replicator is behaving and the Captain is telling people about it.",
      "Every objective passed. I have logged this as a success and Ensign Tannenbaum as a lesson.",
    ],
    rs: [
      "All objectives met, and it compiled, which is two achievements in one.",
      "Every objective passed. The borrow checker raised no complaint, which from it is warm praise.",
    ],
  };
  function pickPass(lang) {
    const lines = PASS_LINES[lang] || PASS_LINES.py;
    return lines[Math.floor(Math.random() * lines.length)];
  }

  function renderMissionState(missionId, objectivesEl, debriefEl) {
    const done = getDone();
    const cleared = done.has(missionId);
    if (cleared && debriefEl) debriefEl.hidden = false;
    document.querySelectorAll(".lang-tab").forEach((t) => {
      const langDone = done.has(missionId + "-" + t.dataset.lang);
      t.classList.toggle("cleared", langDone);
      if (langDone && !t.querySelector(".tab-check")) {
        const tick = document.createElement("span");
        tick.className = "tab-check";
        tick.textContent = " ✓";
        t.appendChild(tick);
      }
    });
  }

  /* ================= the campaign layer =================
     Ranks are earned by missions cleared (in either language). Rank gates
     open STATIONS and SEASONS, never difficulty: a Cadet has two places
     to fail, a Commander has six. Nothing in the main campaign is ever
     locked behind the timed mode. */
  const RANKS = [
    [0,  "Cadet",          "🎖️"],
    [6,  "Ensign",         "⭐"],
    [14, "Lieutenant JG",  "🌟"],
    [22, "Lieutenant",     "✨"],
    [30, "Lt. Commander",  "🏅"],
    [36, "Commander",      "🎗️"],
    [44, "Captain",        "👑"],
  ];
  // Minimum missions cleared before a station is open.
  const STATION_OPENS = { helm: 0, ops: 0, science: 6, tactical: 14, engineering: 22, sickbay: 30 };
  // Minimum missions cleared before a season is open.
  const SEASON_OPENS = { 1: 0, 2: 0, 3: 6, 4: 14, 5: 22, 6: 36 };

  function rankNameFor(threshold) {
    for (const r of RANKS) if (r[0] === threshold) return r[1];
    return "a higher rank";
  }

  function campaignState() {
    const done = getDone();
    const all = window.BRIDGE_MISSIONS || {};
    const ids = Object.keys(all);
    let cleared = 0;
    const clearedIds = new Set();
    ids.forEach((id) => {
      if (done.has(id) || done.has(id + "-py") || done.has(id + "-rs")) {
        cleared++;
        clearedIds.add(id);
      }
    });
    let rank = RANKS[0];
    for (const r of RANKS) if (cleared >= r[0]) rank = r;
    const next = RANKS[RANKS.indexOf(rank) + 1] || null;
    return { done, all, cleared, clearedIds, rank, next, total: ids.length };
  }

  function isLocked(mission, cleared) {
    const stationAt = STATION_OPENS[mission.station] || 0;
    const seasonAt = SEASON_OPENS[mission.season] || 0;
    const need = Math.max(stationAt, seasonAt);
    return cleared < need ? need : 0;
  }

  function renderRank(state) {
    const wrap = document.getElementById("rank-wrap");
    if (!wrap) return;
    const { cleared, rank, next } = state;
    wrap.querySelector(".rank-icon").textContent = rank[2];
    wrap.querySelector(".rank-name").textContent = rank[1];
    wrap.querySelector(".rank-nums").textContent =
      cleared + " mission" + (cleared === 1 ? "" : "s") + " cleared";
    const fill = document.getElementById("rank-fill");
    if (fill) {
      const span = next ? next[0] - rank[0] : 1;
      const into = next ? cleared - rank[0] : 1;
      fill.style.width = Math.min(100, Math.round((into / span) * 100)) + "%";
    }
    const nextEl = document.getElementById("rank-next");
    if (nextEl) {
      nextEl.textContent = next
        ? (next[0] - cleared) + " more to " + next[1] + " " + next[2]
        : "Full commission. The dedication plaque has your name on it.";
    }
  }

  function initBoard() {
    if (!document.getElementById("rank-wrap")) return;
    const state = campaignState();
    const { done, cleared } = state;
    renderRank(state);

    document.querySelectorAll(".mission-card[data-mission]").forEach((card) => {
      const id = card.dataset.mission;
      const m = state.all[id] || { station: card.dataset.station, season: Number(card.dataset.season) };
      const py = done.has(id + "-py");
      const rs = done.has(id + "-rs");
      const flags = card.querySelector(".mission-flags");
      const need = isLocked(m, cleared);
      if (need) {
        card.classList.add("locked");
        card.setAttribute("aria-disabled", "true");
        card.addEventListener("click", (e) => {
          e.preventDefault();
          toast("🔒 Requires " + rankNameFor(need),
                "Clear " + (need - cleared) + " more mission" + (need - cleared === 1 ? "" : "s") + " first.");
        });
        if (flags) flags.innerHTML = '<span class="flag lock">🔒 requires ' + rankNameFor(need) + "</span>";
        return;
      }
      if (py || rs) card.classList.add("cleared");
      if (flags) {
        flags.innerHTML =
          '<span class="flag' + (py ? " on" : "") + '">🐍 ' + (py ? "cleared" : "open") + "</span>" +
          '<span class="flag' + (rs ? " on" : "") + '">🦀 ' + (rs ? "cleared" : "open") + "</span>";
      }
    });

    // Per-season counts.
    document.querySelectorAll(".season[data-season]").forEach((sec) => {
      const cards = [...sec.querySelectorAll(".mission-card")];
      const n = cards.filter((c) => c.classList.contains("cleared")).length;
      const el = sec.querySelector('[data-role="season-count"]');
      if (el && cards.length) el.textContent = n + " of " + cards.length + " cleared";
      const need = SEASON_OPENS[Number(sec.dataset.season)] || 0;
      if (cleared < need) sec.classList.add("season-gated");
    });

    // Station list: open or locked, with what it takes.
    document.querySelectorAll(".station-list li[data-station]").forEach((li) => {
      const need = STATION_OPENS[li.dataset.station] || 0;
      const lock = li.querySelector(".st-lock");
      if (cleared >= need) {
        li.classList.add("open");
        if (lock) lock.textContent = "open";
      } else {
        li.classList.add("shut");
        if (lock) lock.textContent = "🔒 opens at " + rankNameFor(need);
      }
    });
  }

  /* ================= the crew roster ================= */
  function initCrew() {
    const cards = document.querySelectorAll(".crew-card[data-crew]");
    if (!cards.length) return;
    const state = campaignState();
    let met = 0;
    cards.forEach((card) => {
      const id = card.dataset.crew;
      let known = card.dataset.always === "1";
      if (!known && card.dataset.unlock) {
        known = state.clearedIds.has(card.dataset.unlock);
      } else if (!known) {
        known = Object.keys(state.all).some((mid) =>
          state.clearedIds.has(mid) && (state.all[mid].crew || []).includes(id));
      }
      card.classList.toggle("met", known);
      if (known) met++;
    });
    const count = document.getElementById("crew-count");
    if (count) count.textContent = met + " of " + cards.length + " personnel files open.";
  }

  /* ================= toasts (campus style) ================= */
  function toast(title, body) {
    const el = document.createElement("div");
    el.className = "toast";
    el.innerHTML = '<span class="t-title"></span><span class="t-body"></span>';
    el.querySelector(".t-title").textContent = title;
    el.querySelector(".t-body").textContent = body || "";
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 4200);
  }

  /* ================= confetti (campus style) ================= */
  const PIECES = ["🖖", "🎉", "⭐", "🛸", "✨"];
  function confetti() {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const x = window.innerWidth / 2;
    for (let i = 0; i < 16; i++) {
      const piece = document.createElement("span");
      piece.className = "confetti-piece";
      piece.textContent = PIECES[i % PIECES.length];
      piece.style.left = x + (Math.random() * 220 - 110) + "px";
      piece.style.top = "180px";
      piece.style.animationDelay = Math.random() * 0.25 + "s";
      document.body.appendChild(piece);
      setTimeout(() => piece.remove(), 1800);
    }
  }

  document.addEventListener("DOMContentLoaded", () => {
    initMission();
    initBoard();
    initCrew();
  });
})();
