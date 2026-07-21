// GET /api/auth/callback/github
// Step two: GitHub redirects back here with a one-time code. We exchange
// it for an access token, read the public profile, create the account if
// needed, and open a session.

import {
  redirect,
  parseCookies,
  clearCookieHeader,
  signIn,
  STATE_COOKIE,
} from "../../_lib.js";

function fail(reason, detail) {
  const params = new URLSearchParams({ error: reason, from: "github" });
  if (detail) {
    params.set("detail", String(detail).replace(/[^a-zA-Z0-9_-]/g, "").slice(0, 40));
  }
  return redirect("/account.html?" + params.toString(), {
    "Set-Cookie": clearCookieHeader(STATE_COOKIE, "/api/auth"),
  });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  if (!env.DB || !env.GITHUB_CLIENT_ID || !env.GITHUB_CLIENT_SECRET) {
    return fail("github-not-configured");
  }

  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const expected = parseCookies(request)[STATE_COOKIE];
  if (!code || !state || !expected || state !== expected) {
    return fail("state-mismatch");
  }

  const tokenResp = await fetch("https://github.com/login/oauth/access_token", {
    method: "POST",
    headers: { "Content-Type": "application/json", Accept: "application/json" },
    body: JSON.stringify({
      client_id: env.GITHUB_CLIENT_ID,
      client_secret: env.GITHUB_CLIENT_SECRET,
      code,
      redirect_uri: url.origin + "/api/auth/callback/github",
    }),
  });
  const tokenData = await tokenResp.json().catch(() => ({}));
  if (!tokenData.access_token) {
    return fail("token-exchange-failed", tokenData.error || tokenResp.status);
  }

  const profileResp = await fetch("https://api.github.com/user", {
    headers: {
      Authorization: "Bearer " + tokenData.access_token,
      Accept: "application/vnd.github+json",
      "User-Agent": "the-rusty-school",
    },
  });
  const profile = await profileResp.json().catch(() => ({}));
  if (!profile.id) return fail("profile-fetch-failed");

  const sessionCookie = await signIn(
    env,
    "github",
    profile.id,
    profile.name || profile.login || "Rustacean",
    profile.avatar_url || ""
  );

  return new Response(null, {
    status: 302,
    headers: [
      ["Location", "/account.html?welcome=1"],
      ["Set-Cookie", sessionCookie],
      ["Set-Cookie", clearCookieHeader(STATE_COOKIE, "/api/auth")],
    ],
  });
}
