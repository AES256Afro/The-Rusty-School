// GET /api/me/export
// One-click download of every byte we store about the signed-in student.
// If this file looks small, that is the feature.

import { getSession, json } from "../_lib.js";

export async function onRequestGet(context) {
  const { request, env } = context;
  const session = await getSession(request, env);
  if (!session) return json({ error: "not signed in" }, 401);

  const { user } = session;
  const body = JSON.stringify(
    {
      exported_at: new Date().toISOString(),
      provider: user.provider,
      name: user.name,
      avatar: user.avatar,
      progress: user.progress,
      note: "This is the complete record The Rusty School stores about you.",
    },
    null,
    2
  );

  return new Response(body, {
    status: 200,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Content-Disposition": 'attachment; filename="rusty-school-data.json"',
    },
  });
}
