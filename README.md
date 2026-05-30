# ⚡ FileStore Web — Vercel Frontend

A beautiful Next.js frontend for your Telegram File Store Bot, deployed on Vercel's global CDN — completely separate from your bot server.

## Why Vercel?

| Without Vercel | With Vercel |
|---------------|-------------|
| Bot server handles UI + streaming | Bot server handles only streaming |
| Single server region | CDN in 100+ regions globally |
| Bot restarts take down the site | Site stays up independently |
| No caching | Static assets cached at the edge |

---

## 🚀 Deploy to Vercel in 2 minutes

### Option A — One-click (Recommended)

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. Push this `filestore-web/` folder to a GitHub repo.
2. Go to vercel.com → **New Project** → import your repo.
3. Vercel auto-detects Next.js — just set environment variables:

| Variable | Value |
|----------|-------|
| `BOT_BACKEND_URL` | Your bot URL, e.g. `https://mybot.onrender.com` |
| `NEXT_PUBLIC_BOT_USERNAME` | Your bot's Telegram username (no @) |
| `NEXT_PUBLIC_SITE_NAME` | Your site name, e.g. `FileStore` |
| `NEXT_PUBLIC_SITE_TAGLINE` | Tagline shown in hero |

4. Click **Deploy**. Done! 🎉

### Option B — CLI

```bash
npm install -g vercel
cd filestore-web
cp .env.example .env.local   # fill in values
vercel                        # deploy
```

---

## 🔗 How the Frontend Connects to Your Bot

```
User browser ──► Vercel Edge ──► /api/stream/:token  ──► Bot Backend /watch/:token
                              ──► /api/download/:token ──► Bot Backend /download/:token
                              ──► /api/file-info?token ──► Bot Backend /file-info/:token
```

The Next.js API routes act as a **transparent proxy** — they forward stream/download requests to your bot backend and pass the chunked response back. This means:
- Vercel handles the UI globally (fast)
- Your bot handles only the heavy streaming (focused)
- CORS issues are eliminated (same origin for the browser)

---

## 🌗 Dark / Light Mode

Theme is saved in `localStorage` under `fs-theme`. Users' preference persists across visits.
- Default: **Dark**
- Toggle button in the top-right navbar

---

## 📁 Project Structure

```
filestore-web/
├── pages/
│   ├── index.js              ← Homepage: hero, features, how it works
│   ├── watch/[token].js      ← File viewer: video/audio/image player
│   ├── _app.js               ← Theme provider
│   ├── _document.js          ← HTML head, fonts
│   └── api/
│       └── file-info.js      ← Proxy: GET file metadata from bot
├── components/
│   ├── Navbar.js             ← Navigation + theme toggle
│   └── Footer.js
├── styles/
│   ├── globals.css           ← CSS variables (dark/light tokens), animations
│   ├── Home.module.css
│   ├── Watch.module.css
│   ├── Navbar.module.css
│   └── Footer.module.css
├── public/
│   └── favicon.svg
├── next.config.js            ← Rewrites: /api/stream → bot backend
├── vercel.json               ← Vercel deployment config
└── .env.example
```

---

## 🤖 Required Bot Backend Endpoint

Your bot needs one extra endpoint added (already included in the updated `stream_routes.py`):

```
GET /file-info/:token
→ { file_name, file_size, mime_type }
```

This powers the file metadata display (name, size, type) on the watch page.

---

## Local Development

```bash
npm install
cp .env.example .env.local
# fill in BOT_BACKEND_URL pointing to your locally running bot
npm run dev
# open http://localhost:3000
```
