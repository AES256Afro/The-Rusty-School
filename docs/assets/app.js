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
        label.textContent = doneCount === 0
          ? "0 of " + cards.length + " lessons complete. Your journey starts here 🦀"
          : doneCount === cards.length
          ? "All " + cards.length + " lessons complete. You did it! 🎓🦀"
          : doneCount + " of " + cards.length + " lessons complete. Keep going!";
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

  /* ---------------- boot ---------------- */
  document.addEventListener("DOMContentLoaded", () => {
    initTheme();
    initNav();
    initCode();
    initProgress();
    initQuizzes();
    initTabs();
    initImpactBanner();
    const themeBtn = document.querySelector(".theme-toggle");
    if (themeBtn) themeBtn.addEventListener("click", toggleTheme);
  });
})();
