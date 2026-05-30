/**
 * GET /api/file-info?token=xxx
 * Proxies a metadata request to the bot backend.
 * The bot backend exposes GET /file-info/:token returning JSON.
 */
export default async function handler(req, res) {
  const { token } = req.query;
  if (!token) return res.status(400).json({ error: "Missing token" });

  const BOT_BACKEND = process.env.BOT_BACKEND_URL || "http://localhost:8080";

  try {
    const upstream = await fetch(`${BOT_BACKEND}/file-info/${token}`, {
      headers: { "Accept": "application/json" },
      signal: AbortSignal.timeout(8000),
    });

    if (!upstream.ok) {
      return res.status(upstream.status).json({ error: "File not found" });
    }

    const data = await upstream.json();
    return res.status(200).json(data);
  } catch (err) {
    console.error("file-info proxy error:", err);
    return res.status(502).json({ error: "Backend unavailable. Please try again." });
  }
}
