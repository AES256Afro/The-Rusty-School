// PUT /api/progress
// Saves the signed-in student's merged progress. The client merges local
// and remote before calling; the server validates and stores.

import { json, getSession, safeParseProgress } from "./_lib.js";

export async function onRequestPut(context) {
  const { request, env } = context;
  const session = await getSession(request, env);
  if (!session) return json({ error: "not signed in" }, 401);

  const raw = await request.text();
  if (raw.length > 8192) return json({ error: "progress too large" }, 413);

  const progress = safeParseProgress(raw);
  await env.DB.prepare("UPDATE users SET progress = ?1 WHERE id = ?2")
    .bind(JSON.stringify(progress), session.user.id)
    .run();

  return json({ ok: true, progress });
}
