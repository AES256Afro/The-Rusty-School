// GET /api/auth/google
// Step one of "Sign in with Google". Scope is "openid profile" only:
// we do not request the email address. Minimal data, on purpose.

import {
  json, redirect, randomToken, cookieHeader,
  STATE_COOKIE, RETURN_COOKIE, returnKey,
} from "../_lib.js";

export async function onRequestGet(context) {
  const { request, env } = context;
  if (!env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET) {
    return json({ error: "Google sign-in is not configured yet" }, 503);
  }

  const requestUrl = new URL(request.url);
  const origin = requestUrl.origin;
  const state = randomToken();
  // Remember which school sent them here, so they come back to it.
  const from = returnKey(requestUrl.searchParams.get("from"));

  const url = new URL("https://accounts.google.com/o/oauth2/v2/auth");
  url.searchParams.set("client_id", env.GOOGLE_CLIENT_ID);
  url.searchParams.set("redirect_uri", origin + "/api/auth/callback/google");
  url.searchParams.set("response_type", "code");
  url.searchParams.set("scope", "openid profile");
  url.searchParams.set("state", state);

  const headers = new Headers({ Location: url.toString() });
  headers.append("Set-Cookie", cookieHeader(STATE_COOKIE, state, 600, "/api/auth"));
  headers.append("Set-Cookie", cookieHeader(RETURN_COOKIE, from, 600, "/api/auth"));
  return new Response(null, { status: 302, headers });
}
