// GET /api/auth/github
// Step one of "Sign in with GitHub": redirect to GitHub's consent page.
// We request no scopes at all, which grants read access to the public
// profile only. A random state value guards against CSRF.

import { json, redirect, randomToken, cookieHeader, STATE_COOKIE } from "../_lib.js";

export async function onRequestGet(context) {
  const { request, env } = context;
  if (!env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET) {
    return json({ error: "GitHub sign-in is not configured yet" }, 503);
  }

  const origin = new URL(request.url).origin;
  const state = randomToken();

  const url = new URL("https://github.com/login/oauth/authorize");
  url.searchParams.set("client_id", env.GITHUB_CLIENT_ID);
  url.searchParams.set("redirect_uri", origin + "/api/auth/callback/github");
  url.searchParams.set("state", state);

  return redirect(url.toString(), {
    "Set-Cookie": cookieHeader(STATE_COOKIE, state, 600, "/api/auth"),
  });
}
