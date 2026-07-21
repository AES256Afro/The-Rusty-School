/* ============================================================
   The Rusty School: site scripts
   Theme toggle · mobile nav · Rust syntax highlighting ·
   copy buttons · lesson progress · quiz engine · confetti
   ============================================================ */
(function () {
  "use strict";

  /* ---------------- theme ---------------- */
  const root = document.documentElement;

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

  /* ---------------- mobile nav ---------------- */
  function initNav() {
    const burger = document.querySelector(".nav-burger");
    const nav = document.querySelector(".main-nav");
    if (burger && nav) {
      burger.addEventListener("click", () => nav.classList.toggle("open"));
    }
    // Account link in the nav and Privacy link in the footer are injected
    // here so all thirty-odd static pages pick them up from one place.
    const inSubfolder = location.pathname.includes("/learn/") ||
                        location.pathname.includes("/build/");
    const prefix = inSubfolder ? "../" : "";
    // Some pages already ship a hard-coded link (workshop pages link to
    // "index.html" relatively), so match on the rendered label rather than
    // on any particular href spelling.
    const navLabels = [...nav.querySelectorAll("a")].map((a) => a.textContent.trim());
    if (nav && !navLabels.includes("Build")) {
      const build = document.createElement("a");
      build.href = prefix + "build/index.html";
      build.textContent = "Build";
      const learn = nav.querySelector('a[href$="learn/index.html"]');
      if (learn) learn.insertAdjacentElement("afterend", build);
      else nav.insertBefore(build, nav.querySelector(".theme-toggle"));
    }
    if (nav && !navLabels.includes("Dojo")) {
      const dojo = document.createElement("a");
      dojo.href = prefix + "dojo.html";
      dojo.textContent = "Dojo";
      const buildLink = [...nav.querySelectorAll("a")].find((a) => a.textContent.trim() === "Build");
      if (buildLink) buildLink.insertAdjacentElement("afterend", dojo);
      else nav.insertBefore(dojo, nav.querySelector(".theme-toggle"));
    }
    if (nav && !nav.querySelector('a[href$="playground.html"]')) {
      const pg = document.createElement("a");
      pg.href = prefix + "playground.html";
      pg.textContent = "Playground";
      nav.insertBefore(pg, nav.querySelector(".theme-toggle"));
    }
    if (nav && !nav.querySelector('a[href$="account.html"]')) {
      const acct = document.createElement("a");
      acct.href = prefix + "account.html";
      acct.textContent = "Account";
      nav.insertBefore(acct, nav.querySelector(".theme-toggle"));
    }
    const footList = document.querySelector(".site-footer .cols ul");
    if (footList && !footList.querySelector('a[href$="glossary.html"]')) {
      const li = document.createElement("li");
      li.innerHTML = '<a href="' + prefix + 'glossary.html">Glossary</a>';
      footList.appendChild(li);
    }
    if (footList && !footList.querySelector('a[href$="privacy.html"]')) {
      const li = document.createElement("li");
      li.innerHTML = '<a href="' + prefix + 'privacy.html">Privacy</a>';
      footList.appendChild(li);
    }
    // License line at the very bottom of every footer, from one place.
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
    // highlight the current page in the nav
    const here = location.pathname.replace(/\/index\.html$/, "/");
    document.querySelectorAll(".main-nav a").forEach((a) => {
      const href = a.getAttribute("href");
      if (!href || href.startsWith("http")) return;
      const target = new URL(href, location.href).pathname.replace(/\/index\.html$/, "/");
      if (target === here || (target.endsWith("/learn/") && here.includes("/learn/"))) {
        a.classList.add("active");
      }
    });
  }

  /* ---------------- Rust syntax highlighting ---------------- */
  const KEYWORDS =
    "fn|let|mut|const|static|if|else|match|for|while|loop|in|return|use|mod|pub|" +
    "struct|enum|trait|impl|self|Self|super|crate|where|async|await|move|dyn|ref|" +
    "break|continue|unsafe|type|as|true|false";
  const PRIMITIVES = "i8|i16|i32|i64|i128|isize|u8|u16|u32|u64|u128|usize|f32|f64|bool|str|char";

  const TOKEN_RE = new RegExp(
    [
      "(#!?\\[[^\\]\\n]*\\])",                          // 1 attribute
      "(\\/\\/[^\\n]*)",                                 // 2 comment
      '("(?:[^"\\\\]|\\\\[\\s\\S])*")',                  // 3 string
      "('(?:\\\\.|[^'\\\\])')",                          // 4 char literal
      "('[A-Za-z_][A-Za-z0-9_]*)",                       // 5 lifetime
      "(\\b[a-z_][A-Za-z0-9_]*!)",                       // 6 macro
      "(\\b(?:" + KEYWORDS + ")\\b)",                    // 7 keyword
      "(\\b(?:" + PRIMITIVES + ")\\b)",                  // 8 primitive type
      "(\\b[A-Z][A-Za-z0-9_]*\\b)",                      // 9 Type name
      "(\\b\\d[\\d_]*(?:\\.\\d[\\d_]*)?(?:[iuf](?:8|16|32|64|128|size)?)?\\b)", // 10 number
      "(\\b[a-z_][a-z0-9_]*(?=\\s*\\())",                // 11 function call
    ].join("|"),
    "g"
  );
  const TOKEN_CLASS = [null, "tok-attr", "tok-com", "tok-str", "tok-str", "tok-life",
    "tok-mac", "tok-kw", "tok-typ", "tok-typ", "tok-num", "tok-fn"];

  function escapeHtml(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function highlightRust(source) {
    let out = "";
    let last = 0;
    let m;
    TOKEN_RE.lastIndex = 0;
    while ((m = TOKEN_RE.exec(source)) !== null) {
      out += escapeHtml(source.slice(last, m.index));
      let cls = null;
      for (let g = 1; g < TOKEN_CLASS.length; g++) {
        if (m[g] !== undefined) { cls = TOKEN_CLASS[g]; break; }
      }
      out += cls ? '<span class="' + cls + '">' + escapeHtml(m[0]) + "</span>" : escapeHtml(m[0]);
      last = m.index + m[0].length;
    }
    out += escapeHtml(source.slice(last));
    return out;
  }

  function initCode() {
    document.querySelectorAll("pre > code").forEach((code) => {
      const pre = code.parentElement;
      const skip = pre.classList.contains("term") ||
                   pre.classList.contains("compiler") ||
                   code.classList.contains("nohl");
      if (!skip) code.innerHTML = highlightRust(code.textContent);

      // copy button on every code block
      const btn = document.createElement("button");
      btn.className = "copy-btn";
      btn.type = "button";
      btn.textContent = "copy";
      btn.addEventListener("click", () => {
        navigator.clipboard.writeText(code.textContent).then(() => {
          btn.textContent = "copied ✓";
          btn.classList.add("copied");
          setTimeout(() => {
            btn.textContent = "copy";
            btn.classList.remove("copied");
          }, 1600);
        });
      });
      pre.appendChild(btn);

      // runnable examples (anything with fn main) get a ▶ run button that
      // executes right here in the page via the playground proxy
      if (!skip && code.textContent.includes("fn main(")) {
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
          executeRust(code.textContent, out, runBtn);
        });
        pre.appendChild(runBtn);
      }
    });
  }

  /* ---------------- lesson progress ---------------- */
  function getDone() {
    try { return new Set(JSON.parse(localStorage.getItem("rusty-done") || "[]")); }
    catch { return new Set(); }
  }
  function saveDone(set) {
    localStorage.setItem("rusty-done", JSON.stringify([...set]));
  }

  function initProgress() {
    const done = getDone();

    // "Mark lesson complete" button on lesson pages
    document.querySelectorAll(".complete-btn[data-lesson]").forEach((btn) => {
      const id = btn.dataset.lesson;
      const render = () => {
        const isDone = getDone().has(id);
        btn.classList.toggle("done", isDone);
        btn.textContent = isDone ? "✓ Lesson complete. Nice work!" : "Mark lesson complete";
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
        }
        saveDone(set);
        render();
        pushProgress();
      });
    });

    // checkmarks + progress bar on the curriculum page
    const cards = document.querySelectorAll(".lesson-card[data-lesson]");
    if (cards.length) {
      let doneCount = 0;
      cards.forEach((card) => {
        if (done.has(card.dataset.lesson)) { card.classList.add("done"); doneCount++; }
      });
      const fill = document.getElementById("progress-fill");
      const label = document.getElementById("progress-label");
      if (fill) fill.style.width = Math.round((doneCount / cards.length) * 100) + "%";
      if (label) {
        const noun = location.pathname.includes("/build/") ? "projects" : "lessons";
        const one = noun === "projects" ? "project" : "lesson";
        label.textContent = doneCount === 0
          ? "0 of " + cards.length + " " + noun + " complete. Your journey starts here 🦀"
          : doneCount === cards.length
          ? "All " + cards.length + " " + noun + " complete. You did it! 🎓🦀"
          : doneCount + " of " + cards.length + " " +
            (doneCount === 1 ? one : noun) + " complete. Keep going!";
      }
    }
  }

  /* ---------------- impact counter (anonymous) ----------------
     When a lesson is completed for the first time in this browser, ping
     the stats API once. No cookies, no identifiers, and users with
     Do Not Track enabled are never counted. The home page banner reads
     the public total back. Everything fails silently when the API is
     absent (for example on the local Rust dev server). */
  function dntEnabled() {
    return navigator.doNotTrack === "1" || window.doNotTrack === "1";
  }

  function reportCompletion(id) {
    if (dntEnabled()) return;
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

  function initImpactBanner() {
    const el = document.getElementById("impact-banner");
    if (!el) return;
    fetch("/api/stats")
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (data && data.total > 0) {
          el.querySelector(".n").textContent = data.total.toLocaleString();
          const lbl = el.querySelector(".lbl");
          if (lbl) lbl.textContent = data.total === 1 ? "lesson completed" : "lessons completed";
          el.hidden = false;
        }
      })
      .catch(() => {});
  }

  /* ---------------- confetti ---------------- */
  const CONFETTI = ["🦀", "🎉", "⭐", "🧡", "✨"];
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

  /* ---------------- quiz engine ----------------
     quiz.html defines window.RUSTY_QUIZZES = [{id, title, level,
     levelClass, blurb, questions: [{q, code?, options[], answer, explain}]}]
     and includes <div id="quiz-root"></div>. */
  function bestScores() {
    try { return JSON.parse(localStorage.getItem("rusty-quiz-best") || "{}"); }
    catch { return {}; }
  }

  function initQuizzes() {
    const rootEl = document.getElementById("quiz-root");
    if (!rootEl || !window.RUSTY_QUIZZES) return;
    renderQuizMenu(rootEl);
  }

  function renderQuizMenu(rootEl) {
    const best = bestScores();
    rootEl.innerHTML = "";
    const grid = document.createElement("div");
    grid.className = "grid cols-3";
    window.RUSTY_QUIZZES.forEach((quiz) => {
      const card = document.createElement("div");
      card.className = "card";
      const bestLine = best[quiz.id] !== undefined
        ? '<p class="best-score">Best score: ' + best[quiz.id] + "/" + quiz.questions.length + "</p>"
        : '<p class="best-score">Not attempted yet</p>';
      card.innerHTML =
        '<span class="badge ' + quiz.levelClass + '">' + quiz.level + "</span>" +
        "<h3>" + quiz.title + "</h3>" +
        "<p>" + quiz.blurb + "</p>" + bestLine;
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
        (q.code ? "<pre><code>" + highlightRust(q.code) + "</code></pre>" : "");
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
        pushProgress();
      }
      const pct = score / total;
      const verdict =
        pct === 1 ? "Perfect score! Ferris is doing a happy dance. 🦀💃"
        : pct >= 0.7 ? "Great work! You clearly know your stuff. 🎉"
        : pct >= 0.4 ? "Good start! A re-read of the lessons will lock it in. 📖"
        : "No worries: wrong answers are how brains learn. Try again! 💪";

      rootEl.innerHTML = "";
      const card = document.createElement("div");
      card.className = "card quiz-card quiz-score";
      card.innerHTML =
        "<h3>" + quiz.title + ": results</h3>" +
        '<div class="big">' + score + " / " + total + "</div>" +
        "<p>" + verdict + "</p>";
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

  /* ---------------- tabs (setup page) ---------------- */
  function initTabs() {
    const tabs = document.querySelectorAll(".tab-btn[data-tab]");
    if (!tabs.length) return;
    function activate(id, updateHash) {
      tabs.forEach((t) => t.classList.toggle("active", t.dataset.tab === id));
      document.querySelectorAll(".tab-panel").forEach((p) =>
        p.classList.toggle("active", p.id === "tab-" + id)
      );
      if (updateHash) history.replaceState(null, "", "#" + id);
    }
    tabs.forEach((t) =>
      t.addEventListener("click", () => activate(t.dataset.tab, true))
    );
    const fromHash = location.hash.slice(1);
    if (fromHash && document.getElementById("tab-" + fromHash)) activate(fromHash, false);
  }

  /* ---------------- glossary filter ---------------- */
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
        countEl.textContent = q
          ? shown + " of " + total + " terms"
          : total + " terms, all of them defined in a lesson";
      }
      if (emptyEl) emptyEl.hidden = shown !== 0;
    }

    input.addEventListener("input", apply);
    apply();
  }

  /* ---------------- the Rust Dojo ----------------
     36 verified puzzles in 6 belts. Puzzle data is embedded in dojo.html
     (window.RUSTY_DOJO); every snippet was compiled and run before
     publishing. Solved state shares the rusty-done set with lessons,
     using dojo- prefixed ids, so it syncs to accounts like everything
     else. Dojo puzzles deliberately do NOT ping the public counter:
     the home page banner counts lessons only, and stays honest. */
  const DOJO_BELTS = [
    ["white",  "White Belt",  "first stances: variables, printing, loops"],
    ["yellow", "Yellow Belt", "functions and flow"],
    ["orange", "Orange Belt", "the ownership trials"],
    ["green",  "Green Belt",  "structs, enums, collections"],
    ["brown",  "Brown Belt",  "errors, traits, iterators"],
    ["black",  "Black Belt",  "lifetimes, closures, threads"],
  ];
  const DOJO_TYPE = {
    predict: "🔮 Predict the output",
    fix: "🔧 Fix it",
    bug: "🐛 Find the bug",
  };

  function dojoOpenInPlayground(code) {
    localStorage.setItem("pg-pending", code);
    location.href = "playground.html";
  }

  function initDojo() {
    const rootEl = document.getElementById("dojo-root");
    if (!rootEl || !window.RUSTY_DOJO) return;
    const puzzles = window.RUSTY_DOJO;

    DOJO_BELTS.forEach(([key, name, subtitle]) => {
      const mine = puzzles.filter((p) => p.belt === key);
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
        card.dataset.puzzle = "dojo-" + p.id;

        const head = document.createElement("div");
        head.className = "dojo-head";
        head.innerHTML =
          '<span class="dojo-type">' + (DOJO_TYPE[p.type] || p.type) + "</span>" +
          "<h3>" + p.title + "</h3>";
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

        if (p.type !== "predict") {
          const train = document.createElement("button");
          train.type = "button";
          train.className = "btn btn-ghost btn-small";
          train.textContent = "🥋 Train in the Playground";
          train.addEventListener("click", () => dojoOpenInPlayground(p.code));
          actions.appendChild(train);
        }

        const hint = document.createElement("details");
        hint.className = "hint";
        hint.innerHTML =
          "<summary>Hint</summary>" +
          '<div class="hint-body"><p></p></div>';
        hint.querySelector("p").textContent = p.hint;
        actions.appendChild(hint);

        const sol = document.createElement("details");
        sol.className = "hint dojo-solution";
        const solLabel = p.type === "predict" ? "Reveal the answer" : "Reveal the solution";
        sol.innerHTML = "<summary>" + solLabel + "</summary>" +
          '<div class="hint-body"></div>';
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
        opre.className = "term";
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
          if (set.has(id)) {
            set.delete(id);
          } else {
            set.add(id);
            confetti(e.clientX, e.clientY);
          }
          saveDone(set);
          pushProgress();
          refreshDojo();
        });
        actions.appendChild(solved);

        card.appendChild(actions);
        section.appendChild(card);
      });

      rootEl.appendChild(section);
    });

    function refreshDojo() {
      const done = getDone();
      let total = 0;
      let solvedCount = 0;
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
        const earnedNow = solvedHere === cards.length;
        if (earnedNow && !badge.classList.contains("earned")) {
          badge.classList.add("earned");
        } else if (!earnedNow) {
          badge.classList.remove("earned");
        }
      });
      const fill = document.getElementById("dojo-fill");
      const label = document.getElementById("dojo-label");
      if (fill) fill.style.width = Math.round((solvedCount / total) * 100) + "%";
      if (label) {
        label.textContent = solvedCount === total
          ? "All " + total + " puzzles solved. Black belt. Bow to the crab. 🥋🦀"
          : solvedCount + " of " + total + " puzzles solved";
      }
    }

    refreshDojo();
  }

  /* ---------------- running code (The Rusty Playground) ----------------
     Snippets execute on the official Rust Playground via our /api/run
     proxy. Boilerplate cargo lines are trimmed from stderr so beginners
     see their output and real errors, not the build chatter. */
  const BOILERPLATE = /^(\s+Compiling playground|\s+Finished `|\s+Running `)/;

  function renderRunResult(el, result) {
    el.innerHTML = "";
    if (result.error) {
      el.appendChild(runLine("⚠️ " + result.error, "run-err"));
      return;
    }
    const stderr = (result.stderr || "")
      .split("\n")
      .filter((l) => !BOILERPLATE.test(l))
      .join("\n")
      .trim();
    if (result.success) {
      const out = (result.stdout || "").replace(/\s+$/, "");
      el.appendChild(runLine(out.length ? out : "(the program ran, with no output)", "run-ok"));
      if (stderr) el.appendChild(runLine(stderr, "run-warn"));
    } else {
      el.appendChild(runLine(stderr || "compilation failed", "run-err"));
      const hint = document.createElement("div");
      hint.className = "run-hint";
      hint.textContent = "Compiler errors are directions, not punishments. Read from the top. 🦀";
      el.appendChild(hint);
    }
  }

  function runLine(text, cls) {
    const span = document.createElement("span");
    span.className = cls;
    span.textContent = text;
    return span;
  }

  async function executeRust(code, outEl, button) {
    outEl.innerHTML = "";
    outEl.appendChild(runLine("⏳ Compiling on the Rust Playground…", "run-warn"));
    if (button) button.disabled = true;
    try {
      const resp = await fetch("/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code, edition: "2024" }),
      });
      const result = await resp.json().catch(() => ({ error: "unreadable response" }));
      renderRunResult(outEl, result);
    } catch {
      renderRunResult(outEl, {
        error: "Couldn't reach the playground. On the local dev server, running " +
          "code needs the live site: rustyschool.com",
      });
    } finally {
      if (button) button.disabled = false;
    }
  }

  const PG_EXAMPLES = {
    hello: 'fn main() {\n    println!("Hello, world! 🦀");\n}\n',
    variables:
      'fn main() {\n    let crabs = 10;          // immutable\n    let mut snacks = 3;      // mutable\n    snacks += 1;\n\n    let crabs = crabs * 2;   // shadowing: a brand-new binding\n    println!("{crabs} crabs sharing {snacks} snacks");\n}\n',
    fizzbuzz:
      'fn main() {\n    for n in 1..=20 {\n        if n % 15 == 0 {\n            println!("FizzBuzz");\n        } else if n % 3 == 0 {\n            println!("Fizz");\n        } else if n % 5 == 0 {\n            println!("Buzz");\n        } else {\n            println!("{n}");\n        }\n    }\n}\n',
    ownership:
      'fn main() {\n    let s1 = String::from("hello");\n    let s2 = s1;              // ownership MOVES to s2\n\n    // println!("{s1}");      // uncomment me and read the error!\n    println!("{s2}");\n\n    let s3 = s2.clone();      // a real copy: both stay valid\n    println!("{s2} and {s3}");\n}\n',
    match:
      'enum Weather {\n    Sunny,\n    Rainy,\n    Windy(u32),  // wind speed in km/h\n}\n\nfn main() {\n    let today = Weather::Windy(95);\n\n    match today {\n        Weather::Sunny => println!("Sunscreen. You are a crab."),\n        Weather::Rainy => println!("You live in water. Proceed."),\n        Weather::Windy(s) if s > 80 => println!("GRIP THE ROCK ({s} km/h)"),\n        Weather::Windy(s) => println!("Breezy at {s} km/h."),\n    }\n}\n',
    iterators:
      'fn main() {\n    let catch_g = vec![12, 7, 30, 5, 18];\n\n    let keepers: Vec<i32> = catch_g\n        .iter()\n        .filter(|w| **w >= 10)\n        .map(|w| w * 2)\n        .collect();\n\n    println!("{keepers:?}");\n}\n',
    threads:
      'use std::sync::mpsc;\nuse std::thread;\n\nfn main() {\n    let (tx, rx) = mpsc::channel();\n\n    for worker in 0..3 {\n        let tx = tx.clone();\n        thread::spawn(move || {\n            tx.send(format!("worker {worker} reporting in")).unwrap();\n        });\n    }\n    drop(tx);\n\n    for message in rx {\n        println!("📨 {message}");\n    }\n}\n',
  };

  function initPlayground() {
    const editor = document.getElementById("pg-editor");
    if (!editor) return;
    const output = document.getElementById("pg-output");
    const runBtn = document.getElementById("pg-run");
    const picker = document.getElementById("pg-example");

    // A dojo puzzle may have sent code over for repair.
    const pending = localStorage.getItem("pg-pending");
    if (pending) {
      editor.value = pending;
      localStorage.removeItem("pg-pending");
    } else {
      editor.value = PG_EXAMPLES.hello;
    }
    picker.addEventListener("change", () => {
      editor.value = PG_EXAMPLES[picker.value] || PG_EXAMPLES.hello;
      editor.focus();
    });

    // Tab inserts spaces instead of leaving the editor.
    editor.addEventListener("keydown", (e) => {
      if (e.key === "Tab") {
        e.preventDefault();
        const s = editor.selectionStart;
        editor.setRangeText("    ", s, editor.selectionEnd, "end");
      }
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        executeRust(editor.value, output, runBtn);
      }
    });

    runBtn.addEventListener("click", () => executeRust(editor.value, output, runBtn));
  }

  /* ---------------- accounts & progress sync ----------------
     Optional sign-in (GitHub/Google) syncs progress across devices.
     Everything here degrades gracefully: with no API (local dev server)
     or no session, the site behaves exactly as before, localStorage only. */
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

  // Fetch the session; if signed in, merge remote and local progress
  // (union of completions, best of quiz scores) in both directions.
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
      if (JSON.stringify(merged) !== JSON.stringify(me.progress)) {
        pushProgress();
      }
      me.progress = merged;
      return me;
    } catch {
      return null;
    }
  }

  /* ---------------- account page ---------------- */
  const AUTH_ERRORS = {
    "state-mismatch": "The sign-in attempt expired or was tampered with. Please try again.",
    "token-exchange-failed": "The provider rejected the sign-in. Please try again.",
    "profile-fetch-failed": "We couldn't read your public profile. Please try again.",
    "github-not-configured": "GitHub sign-in isn't switched on yet.",
    "google-not-configured": "Google sign-in isn't switched on yet.",
  };

  function initAccount(me) {
    const root = document.getElementById("account-root");
    if (!root) return;

    if (me && me.signedIn) {
      const tpl = document.getElementById("tpl-signed-in");
      root.innerHTML = "";
      root.appendChild(tpl.content.cloneNode(true));
      const avatar = document.getElementById("acct-avatar");
      if (me.avatar) avatar.src = me.avatar; else avatar.style.display = "none";
      document.getElementById("acct-name").textContent = me.name || "Rustacean";
      document.getElementById("acct-provider").textContent = me.provider;
      const allDone = (me.progress && me.progress.done) || [];
      const lessonCount = allDone.filter((d) => !d.startsWith("dojo-")).length;
      const puzzleCount = allDone.filter((d) => d.startsWith("dojo-")).length;
      let summary = "📚 <strong>" + lessonCount + " lesson" + (lessonCount === 1 ? "" : "s") + "</strong>";
      if (puzzleCount > 0) {
        summary += " and <strong>" + puzzleCount + " dojo puzzle" + (puzzleCount === 1 ? "" : "s") + "</strong>";
      }
      document.getElementById("acct-progress").innerHTML = summary + " synced to your account.";
      document.getElementById("acct-sync-note").textContent =
        "Progress syncs automatically whenever you complete a lesson or quiz on any signed-in device.";

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

    // Signed out: show whichever provider buttons are actually configured.
    const tpl = document.getElementById("tpl-signed-out");
    root.innerHTML = "";
    root.appendChild(tpl.content.cloneNode(true));

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
            '<a class="btn btn-primary" href="/api/auth/github">Sign in with GitHub</a>');
        }
        if (providers.google) {
          any = true;
          row.insertAdjacentHTML("beforeend",
            '<a class="btn btn-ghost" href="/api/auth/google">Sign in with Google</a>');
        }
        if (!any) note.hidden = false;
      });
  }

  /* ---------------- boot ---------------- */
  document.addEventListener("DOMContentLoaded", async () => {
    initTheme();
    initNav();
    initDojo();   // before initCode, so generated puzzles get highlighting and run buttons
    initCode();
    initTabs();
    const themeBtn = document.querySelector(".theme-toggle");
    if (themeBtn) themeBtn.addEventListener("click", toggleTheme);

    // Sync before rendering progress so checkmarks reflect merged state.
    const me = await syncProgress(1500);
    initProgress();
    initQuizzes();
    initImpactBanner();
    initAccount(me);
    initPlayground();
    initGlossary();
  });
})();
