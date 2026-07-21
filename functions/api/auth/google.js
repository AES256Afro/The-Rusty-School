// GET /api/auth/google
// Step one of "Sign in with Google". Scope is "openid profile" only:
// we do not request the email address. Minimal data, on purpose.

import { json, redirect, randomToken, cookieHeader, STATE_COOKIE } from "../_lib.js";

export async function onRequestGet(context) {
  const { request, env } = context;
  if (!env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET) {
    return json({ error: "Google sign-in is not configured yet" }, 503);
  }

  const origin = new URL(request.url).origin;
  const state = randomToken();

  const url = new URL("https://accounts.google.com/o/oauth2/v2/auth");
  url.searchParams.set("client_id", env.GOOGLE_CLIENT_ID);
  url.searchParams.set("redirect_uri", origin + "/api/auth/callback/google");
  url.searchParams.set("response_type", "code");
  url.searchParams.set("scope", "openid profile");
  url.searchParams.set("state", state);

  return redirect(url.toString(), {
    "Set-Cookie": cookieHeader(STATE_COOKIE, state, 600, "/api/auth"),
  });
}
