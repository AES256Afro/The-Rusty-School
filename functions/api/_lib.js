// Shared helpers for The Rusty School's account API.
// Files starting with an underscore are not routed by Pages Functions.
//
// Design notes, for students reading the source:
// - Sessions live in the database, not in signed cookies. The cookie holds a
//   random token; only a SHA-256 hash of it is stored. Stealing the database
//   does not yield usable sessions, and sign-out truly revokes.
// - We store the absolute minimum: provider, provider id, display name,
//   avatar URL, and a progress JSON. No emails, no IPs, no analytics.

export const LESSON_ID = /^[a-z0-9][a-z0-9-]{1,39}$/;
export const SESSION_COOKIE = "rusty_session";
export const STATE_COOKIE = "rusty_oauth_state";
export const SESSION_DAYS = 90;

export function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json; charset=utf-8", ...headers },
  });
}

export function redirect(location, extraHeaders = {}) {
  return new Response(null, {
    status: 302,
    headers: { Location: location, ...extraHeaders },
  });
}

export function parseCookies(request) {
  const out = {};
  const raw = request.headers.get("Cookie") || "";
  for (const part of raw.split(";")) {
    const i = part.indexOf("=");
    if (i > 0) out[part.slice(0, i).trim()] = part.slice(i + 1).trim();
  }
  return out;
}

export function randomToken() {
  const bytes = new Uint8Array(32);
  crypto.getRandomValues(bytes);
  let s = "";
  for (const b of bytes) s += String.fromCharCode(b);
  return btoa(s).replaceAll("+", "-").replaceAll("/", "_").replaceAll("=", "");
}

export async function sha256hex(text) {
  const digest = await crypto.subtle.digest(
    "SHA-256",
    new TextEncoder().encode(text)
  );
  return [...new Uint8Array(digest)]
    .map((b) => b.toString(16).padStart(2, "0"))
    .join("");
}

export function cookieHeader(name, value, maxAgeSeconds, path = "/") {
  return (
    name + "=" + value +
    "; Max-Age=" + maxAgeSeconds +
    "; Path=" + path +
    "; HttpOnly; Secure; SameSite=Lax"
  );
}

export function clearCookieHeader(name, path = "/") {
  return name + "=; Max-Age=0; Path=" + path + "; HttpOnly; Secure; SameSite=Lax";
}

export async function createSession(env, userId) {
  const token = randomToken();
  const hash = await sha256hex(token);
  const expires = new Date(Date.now() + SESSION_DAYS * 86400 * 1000).toISOString();
  await env.DB.prepare(
    "INSERT INTO sessions (token_hash, user_id, expires_at) VALUES (?1, ?2, ?3)"
  ).bind(hash, userId, expires).run();
  return token;
}

// Returns { user, tokenHash } for a valid session, else null.
export async function getSession(request, env) {
  const token = parseCookies(request)[SESSION_COOKIE];
  if (!token || !env.DB) return null;
  const hash = await sha256hex(token);
  const row = await env.DB.prepare(
    "SELECT s.token_hash, s.expires_at, u.id, u.provider, u.name, u.avatar, u.progress " +
      "FROM sessions s JOIN users u ON u.id = s.user_id WHERE s.token_hash = ?1"
  ).bind(hash).first();
  if (!row) return null;
  if (new Date(row.expires_at).getTime() < Date.now()) {
    await env.DB.prepare("DELETE FROM sessions WHERE token_hash = ?1").bind(hash).run();
    return null;
  }
  return {
    tokenHash: row.token_hash,
    user: {
      id: row.id,
      provider: row.provider,
      name: row.name,
      avatar: row.avatar,
      progress: safeParseProgress(row.progress),
    },
  };
}

export function safeParseProgress(text) {
  try {
    const p = JSON.parse(text || "{}");
    return {
      done: Array.isArray(p.done) ? p.done.filter((x) => LESSON_ID.test(String(x))).slice(0, 200) : [],
      counted: Array.isArray(p.counted) ? p.counted.filter((x) => LESSON_ID.test(String(x))).slice(0, 200) : [],
      quizBest: sanitizeQuizBest(p.quizBest),
    };
  } catch {
    return { done: [], counted: [], quizBest: {} };
  }
}

export function sanitizeQuizBest(obj) {
  const out = {};
  if (obj && typeof obj === "object") {
    for (const k of Object.keys(obj).slice(0, 50)) {
      const v = obj[k];
      if (/^[a-z0-9-]{1,40}$/.test(k) && Number.isInteger(v) && v >= 0 && v <= 1000) {
        out[k] = v;
      }
    }
  }
  return out;
}

// Find or create a user for an OAuth identity, then open a session.
// Returns the Set-Cookie header value for the new session.
export async function signIn(env, provider, providerId, name, avatar) {
  const existing = await env.DB.prepare(
    "SELECT id FROM users WHERE provider = ?1 AND provider_id = ?2"
  ).bind(provider, String(providerId)).first();

  let userId;
  if (existing) {
    userId = existing.id;
    await env.DB.prepare(
      "UPDATE users SET name = ?1, avatar = ?2 WHERE id = ?3"
    ).bind(name, avatar, userId).run();
  } else {
    const inserted = await env.DB.prepare(
      "INSERT INTO users (provider, provider_id, name, avatar, progress) " +
        "VALUES (?1, ?2, ?3, ?4, '{}') RETURNING id"
    ).bind(provider, String(providerId), name, avatar).first();
    userId = inserted.id;
  }

  const token = await createSession(env, userId);
  return cookieHeader(SESSION_COOKIE, token, SESSION_DAYS * 86400);
}
