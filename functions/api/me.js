// /api/me
// GET: who am I, and what progress is stored for me?
// DELETE: erase my account and everything attached to it, immediately.

import { json, getSession, clearCookieHeader, SESSION_COOKIE } from "./_lib.js";

export async function onRequestGet(context) {
  const { request, env } = context;
  if (!env.DB) return json({ signedIn: false, error: "not configured" });

  const session = await getSession(request, env);
  if (!session) return json({ signedIn: false });

  const { user } = session;
  return json({
    signedIn: true,
    provider: user.provider,
    name: user.name,
    avatar: user.avatar,
    progress: user.progress,
  });
}

export async function onRequestDelete(context) {
  const { request, env } = context;
  const session = await getSession(request, env);
  if (!session) return json({ error: "not signed in" }, 401);

  // Sessions first, then the user row. Nothing else exists to delete:
  // that is the whole point of storing so little.
  await env.DB.prepare("DELETE FROM sessions WHERE user_id = ?1")
    .bind(session.user.id)
    .run();
  await env.DB.prepare("DELETE FROM users WHERE id = ?1")
    .bind(session.user.id)
    .run();

  return json({ ok: true, deleted: true }, 200, {
    "Set-Cookie": clearCookieHeader(SESSION_COOKIE),
  });
}
