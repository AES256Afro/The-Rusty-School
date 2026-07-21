// POST /api/run
// Compiles and runs a Rust snippet by forwarding it to the official Rust
// Playground (play.rust-lang.org), whose generous public API also powers
// the run buttons in Rust's own documentation. Thanks, Rust infra team!
//
// Why a proxy instead of calling it straight from the browser: the client
// stays same-origin, we send a proper User-Agent, and if this school ever
// outgrows polite use of the shared service we can point this one file at
// a self-hosted playground backend without touching any page.

function json(body, status = 200) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8" },
  });
}

const MAX_CODE_BYTES = 25000;
const EDITIONS = new Set(["2015", "2018", "2021", "2024"]);

export async function onRequestPost(context) {
  const { request } = context;

  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: "expected a JSON body" }, 400);
  }

  const code = typeof body.code === "string" ? body.code : "";
  if (!code.trim()) return json({ error: "no code to run" }, 400);
  if (code.length > MAX_CODE_BYTES) {
    return json({ error: "that program is too long for the playground" }, 413);
  }
  const edition = EDITIONS.has(String(body.edition)) ? String(body.edition) : "2024";

  let upstream;
  try {
    upstream = await fetch("https://play.rust-lang.org/execute", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "User-Agent": "the-rusty-school (https://rustyschool.com)",
      },
      body: JSON.stringify({
        channel: "stable",
        mode: "debug",
        edition,
        crateType: "bin",
        tests: false,
        code,
        backtrace: false,
      }),
    });
  } catch {
    return json({ error: "could not reach the Rust Playground" }, 502);
  }

  if (upstream.status === 429) {
    return json(
      { error: "the playground is rate limiting; wait a moment and try again" },
      429
    );
  }
  if (!upstream.ok) {
    return json({ error: "playground error (" + upstream.status + ")" }, 502);
  }

  const result = await upstream.json().catch(() => null);
  if (!result) return json({ error: "unreadable playground response" }, 502);

  return json({
    success: Boolean(result.success),
    stdout: String(result.stdout || ""),
    stderr: String(result.stderr || ""),
  });
}
