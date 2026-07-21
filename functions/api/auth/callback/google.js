// GET /api/auth/callback/google
// Step two of Google sign-in: exchange the code, read the basic profile
// (name and picture; we never request the email), and open a session.

import {
  redirect,
  parseCookies,
  clearCookieHeader,
  signIn,
  STATE_COOKIE,
} from "../../_lib.js";

function fail(reason, detail) {
  const params = new URLSearchParams({ error: reason, from: "google" });
  if (detail) {
    params.set("detail", String(detail).replace(/[^a-zA-Z0-9_-]/g, "").slice(0, 40));
  }
  return redirect("/account.html?" + params.toString(), {
    "Set-Cookie": clearCookieHeader(STATE_COOKIE, "/api/auth"),
  });
}

export async function onRequestGet(context) {
  const { request, env } = context;
  if (!env.DB || !env.GOOGLE_CLIENT_ID || !env.GOOGLE_CLIENT_SECRET) {
    return fail("google-not-configured");
  }

  const url = new URL(request.url);
  const code = url.searchParams.get("code");
  const state = url.searchParams.get("state");
  const expected = parseCookies(request)[STATE_COOKIE];
  if (!code || !state || !expected || state !== expected) {
    return fail("state-mismatch");
  }

  const tokenResp = await fetch("https://oauth2.googleapis.com/token", {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      client_id: env.GOOGLE_CLIENT_ID,
      client_secret: env.GOOGLE_CLIENT_SECRET,
      code,
      redirect_uri: url.origin + "/api/auth/callback/google",
      grant_type: "authorization_code",
    }),
  });
  const tokenData = await tokenResp.json().catch(() => ({}));
  if (!tokenData.access_token) {
    return fail("token-exchange-failed", tokenData.error || tokenResp.status);
  }

  const profileResp = await fetch(
    "https://www.googleapis.com/oauth2/v3/userinfo",
    { headers: { Authorization: "Bearer " + tokenData.access_token } }
  );
  const profile = await profileResp.json().catch(() => ({}));
  if (!profile.sub) return fail("profile-fetch-failed");

  const sessionCookie = await signIn(
    env,
    "google",
    profile.sub,
    profile.name || "Rustacean",
    profile.picture || ""
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
