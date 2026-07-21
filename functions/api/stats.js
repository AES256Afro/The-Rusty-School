// GET /api/stats
// Returns the public, anonymous counters shown on the home page banner.
// Cached for a minute at the edge to keep database reads tiny.

function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...headers },
  });
}

export async function onRequestGet(context) {
  const { env } = context;

  if (!env.DB) {
    return json({ error: "stats not configured" }, 503);
  }

  const row = await env.DB.prepare(
    "SELECT value FROM stats WHERE key = 'total'"
  ).first();

  return json(
    { total: (row && row.value) || 0 },
    200,
    { "Cache-Control": "public, max-age=60" }
  );
}
