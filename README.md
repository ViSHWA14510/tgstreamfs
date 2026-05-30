# 📁 Telegram File Store & Stream Bot

A robust Telegram bot that stores files in a private channel, generates shareable links, and streams/downloads files over HTTP. Built with **Pyrogram** + **Aiohttp** + **MongoDB**.

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 📨 **File Store Link** | Shareable `t.me/BotName?start=file_xxx` link — delivers file natively inside Telegram |
| 🎬 **Stream Link** | Browser/VLC streamable HTTP link with Range request support (seeking works) |
| ⬇️ **Download Link** | Direct HTTP file download link |
| 🔒 **Force Subscribe** | Gate file access behind channel membership |
| 📢 **Broadcast** | Admin command to message all users |
| 📊 **Stats** | User count, file count, banned users |
| 🚫 **Ban/Unban** | Restrict specific users |
| 🐳 **Docker** | One-command deployment via Docker or Render/Heroku |

---

## 🚀 Quick Setup

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/telegram-file-stream-bot.git
cd telegram-file-stream-bot
```

### 2. Configure environment
```bash
cp .env.example .env
nano .env   # Fill in your values
```

**Required values in `.env`:**

| Variable | Description |
|----------|-------------|
| `API_ID` | From https://my.telegram.org |
| `API_HASH` | From https://my.telegram.org |
| `BOT_TOKEN` | From @BotFather |
| `DATABASE_URL` | MongoDB Atlas URI or local MongoDB |
| `BIN_CHANNEL` | Private channel ID (bot must be admin) |
| `FQDN` | Your public domain (e.g. `https://mybot.onrender.com`) |

**Optional:**

| Variable | Description |
|----------|-------------|
| `FORCE_SUB_CHANNEL` | `@username` or `-100xxx` — leave empty to disable |
| `ADMIN_USER_IDS` | Comma-separated Telegram user IDs |
| `PORT` | Defaults to `8080` |

### 3. Create the Bin Channel
1. Create a **private** Telegram channel.
2. Add your bot as **Admin** (with "Post Messages" permission).
3. Get the channel ID (forward a message from it to @userinfobot or @RawDataBot).
4. Set `BIN_CHANNEL=-100xxxxxxxxxx` in your `.env`.

### 4. Run locally
```bash
pip install -r requirements.txt
python bot.py
```

Or with Docker:
```bash
docker-compose up --build
```

---

## ☁️ Deployment

### Render (Recommended — Free Tier Available)
1. Push your repo to GitHub.
2. Go to https://render.com → New → **Web Service**.
3. Connect your repo.
4. Set **Start Command**: `python bot.py`
5. Add all environment variables from `.env.example` in the Render dashboard.
6. Render will auto-set `PORT`. Set `FQDN` to your Render URL (e.g. `https://mybot.onrender.com`).

### Heroku
1. Install Heroku CLI and login.
```bash
heroku create your-app-name
heroku config:set API_ID=xxx API_HASH=xxx BOT_TOKEN=xxx ...
git push heroku main
```

### VPS (Ubuntu)
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone and configure
git clone ... && cd telegram-file-stream-bot
cp .env.example .env && nano .env

# Run
docker-compose up -d
```

---

## 🔗 How File Store Links Work

When a user sends a file to the bot:
1. The bot **forwards the file** to your private `BIN_CHANNEL` (permanent storage).
2. A unique token is generated from the MongoDB document ID.
3. Three links are returned:

```
📨 File Store Link:  https://t.me/YourBot?start=file_<token>
🎬 Stream Link:      https://your-domain.com/watch/<token>
⬇️ Download Link:    https://your-domain.com/download/<token>
```

When someone clicks the **File Store Link**:
- If Force Subscribe is ON → checks channel membership → shows join prompt if not subscribed.
- Once verified → bot sends the file directly in Telegram chat.

---

## 🔒 Force Subscribe Flow

```
User clicks File Store Link
       ↓
Bot checks channel membership
       ↓
  Not subscribed?         Subscribed?
       ↓                      ↓
Show Join + Try Again    Send file directly
button
       ↓
User joins → clicks Try Again
       ↓
Bot re-checks → sends file
```

---

## 🤖 Admin Commands

| Command | Description |
|---------|-------------|
| `/stats` | View user count, file count, banned count |
| `/broadcast` | Reply to a message with this to broadcast it |
| `/ban <user_id>` | Ban a user from the bot |
| `/unban <user_id>` | Unban a user |
| `/ban_check <user_id>` | Check if a user is banned |

---

## 📂 Project Structure

```
telegram-file-stream-bot/
├── bot.py                  ← Entry point (starts bot + web server)
├── config.py               ← All env variables
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── Procfile                ← Heroku
├── .env.example
├── bot/
│   ├── clients.py          ← Pyrogram client init
│   └── plugins/
│       ├── start.py        ← /start, file store link, force-sub
│       ├── handlers.py     ← File receiving + link generation
│       └── admin.py        ← Admin commands
├── server/
│   ├── app.py              ← Aiohttp app setup
│   └── stream_routes.py    ← /watch and /download endpoints
├── database/
│   └── mongo.py            ← MongoDB helpers
└── utils/
    ├── custom_filters.py   ← Pyrogram filters (admin check)
    └── helpers.py          ← Encoding, size formatting
```

---

## ⚡ Multi-Bot Support (Explained)

> **Your bot is configured as single-bot only.** This section explains what multi-bot support does, in case you want to add it later.

### What is the Multi-Bot Speed Limit Problem?

Telegram enforces a **download speed cap per bot token** when streaming files from its servers. In practice, each bot token is rate-limited to roughly **50 MB/s** of concurrent download throughput. When many users stream simultaneously, they all share this bandwidth — causing slowdowns and buffering.

### How Multi-Bot Bypasses This

Multi-bot support means creating **2–5 extra bot tokens** (via @BotFather) and loading them all as separate Pyrogram clients. When a stream request comes in, the system picks a bot using **round-robin** or **least-loaded** selection:

```
User 1 request → Bot Token A (streaming)
User 2 request → Bot Token B (streaming)
User 3 request → Bot Token C (streaming)
User 4 request → Bot Token A again (round-robin)
```

Each token gets its own independent rate limit, so with 4 bots you effectively get **4× the bandwidth**.

### Requirements for Multi-Bot
- All extra bots must be **admins** in your `BIN_CHANNEL`.
- A load-balancer function in `clients.py` to rotate between them.
- Extra `BOT_TOKEN_2`, `BOT_TOKEN_3` env variables.

### When Do You Need It?
- **Single bot is fine** for personal use or low traffic (< 20 concurrent users).
- Add multi-bot when you notice buffering or slow downloads under heavy load.

---

## 📄 License

MIT
