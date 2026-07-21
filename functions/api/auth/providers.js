// GET /api/auth/providers
// Tells the account page which sign-in buttons to show. A provider is
// available once its client id and secret are configured in the Pages
// project settings.

import { json } from "../_lib.js";

export async function onRequestGet(context) {
  const { env } = context;
  return json({
    github: Boolean(env.GITHUB_CLIENT_ID && env.GITHUB_CLIENT_SECRET),
    google: Boolean(env.GOOGLE_CLIENT_ID && env.GOOGLE_CLIENT_SECRET),
  });
}
