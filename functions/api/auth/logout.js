// POST /api/auth/logout
// Ends the current session for real: the row is deleted from the
// database, so the cookie is useless even if it lingers somewhere.

import { json, getSession, clearCookieHeader, SESSION_COOKIE } from "../_lib.js";

export async function onRequestPost(context) {
  const { request, env } = context;
  const session = await getSession(request, env);
  if (session) {
    await env.DB.prepare("DELETE FROM sessions WHERE token_hash = ?1")
      .bind(session.tokenHash)
      .run();
  }
  return json({ ok: true }, 200, {
    "Set-Cookie": clearCookieHeader(SESSION_COOKIE),
  });
}
