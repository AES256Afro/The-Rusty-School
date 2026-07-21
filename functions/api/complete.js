// POST /api/complete
// Counts one lesson completion. Anonymous by design: no cookies, no IPs
// stored, no user identifiers. The browser sends {"lesson": "06-ownership"}
// exactly once per lesson (the site remembers what it already reported),
// and users with Do Not Track enabled are never counted.

const LESSON_ID = /^[a-z0-9][a-z0-9-]{1,39}$/;

function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...headers },
  });
}

export async function onRequestPost(context) {
  const { request, env } = context;

  if (!env.DB) {
    return json({ error: "stats not configured" }, 503);
  }

  // Honor Do Not Track on the server side as well as the client.
  if ((request.headers.get("DNT") || "") === "1") {
    return json({ ok: true, counted: false });
  }

  let lesson = null;
  try {
    const body = await request.json();
    lesson = body && body.lesson;
  } catch {
    // fall through to validation below
  }
  if (typeof lesson !== "string" || !LESSON_ID.test(lesson)) {
    return json({ error: "bad lesson id" }, 400);
  }

  // Atomic upsert increments: one for the global total, one per lesson.
  const upsert = env.DB.prepare(
    "INSERT INTO stats (key, value) VALUES (?1, 1) " +
      "ON CONFLICT(key) DO UPDATE SET value = value + 1"
  );
  await env.DB.batch([upsert.bind("total"), upsert.bind("lesson:" + lesson)]);

  return json({ ok: true, counted: true });
}
