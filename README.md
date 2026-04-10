# 🚀 SMS Bomber Telegram Bot

Fast Mode SMS Bomber — 28 APIs, ~140 SMS per run.

---

## 📁 File Structure

```
├── bot.py               # Main bot logic + all 28 API services
├── api/
│   └── webhook.py       # Vercel serverless webhook handler
├── set_webhook.py       # One-time webhook registration script
├── requirements.txt     # Python dependencies
├── vercel.json          # Vercel deployment config
└── README.md
```

---

## 🤖 Step 1 — Create a Telegram Bot

1. Open Telegram → search **@BotFather**
2. Send `/newbot`
3. Give it a name and username
4. Copy the **API Token** — e.g. `123456789:ABCdef...`

---

## ☁️ Step 2 — Deploy to Vercel

### Option A — Vercel CLI (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy (from project folder)
vercel --prod
```

When prompted:
- **Set up and deploy?** → Yes
- **Which scope?** → Your account
- **Link to existing project?** → No
- **Project name?** → sms-bomber-bot (or anything)
- **In which directory?** → ./

### Option B — Vercel Dashboard

1. Go to [vercel.com](https://vercel.com) → New Project
2. Import your GitHub repo (push this folder to GitHub first)
3. Framework Preset: **Other**
4. Click **Deploy**

---

## 🔐 Step 3 — Set Environment Variables on Vercel

Go to your project → **Settings** → **Environment Variables** → Add:

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | Your Telegram bot token |

Click **Save** then **Redeploy**.

---

## 🔗 Step 4 — Register Webhook (One-Time)

After deploying, run this **once** on your local machine:

```bash
BOT_TOKEN="your_bot_token" VERCEL_URL="https://your-app.vercel.app" python set_webhook.py
```

Or open this URL in your browser (replace values):

```
https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://your-app.vercel.app/webhook
```

---

## ✅ Step 5 — Test the Bot

1. Open Telegram → find your bot
2. Send `/start`
3. Click **🚀 Start Attack**
4. Enter target number: `017XXXXXXXX`
5. Bot will bomb and show results!

---

## 🔘 Bot Buttons

| Button | Action |
|--------|--------|
| 🚀 Start Attack | Ask for number → start bombing |
| 📞 Support | Show admin & developer contacts |

---

## 📊 APIs Used (Fast Mode — 28 APIs)

| # | Service | Requests |
|---|---------|----------|
| 1 | BTCL MyBTCL | 5 |
| 2 | BTCL PhoneBill | 5 |
| 3 | BTCL BDIA | 5 |
| 4 | Bioscope Plus | 5 |
| 5 | BD Tickets | 5 |
| 6 | Apex4U | 5 |
| 7 | Swap.com.bd | 5 |
| 8 | Ilyn Global | 5 |
| 9 | Arogga | 5 |
| 10 | Fundesh | 5 |
| 11 | Garibook | 5 |
| 12 | Sheba | 5 |
| 13 | AppLink | 5 |
| 14 | MyGP Cinematic | 5 |
| 15 | GP Web Login | 5 |
| 16 | Ghoori Learning | 5 |
| 17 | Deepto Play | 5 |
| 18 | Sailor Clothing | 5 |
| 19 | MedEasy | 5 |
| 20 | Osudpotro | 5 |
| 21 | TheClinicall | 5 |
| 22 | Care Box | 5 |
| 23 | Renix Care | 5 |
| 24 | PKLuck2 Register | 5 |
| 25 | PKLuck2 NoLogin | 5 |
| 26 | GP Flexiplan | 5 |
| 27 | GP FWA | 5 |
| 28 | Priyoshikkhaloy | 5 |

**Total: ~140 SMS per run**

---

## 👨‍💻 Credits

- Admin: @parvesbrand420
- Developer: @codex_haseb

---

## ⚠️ Vercel Free Plan Note

Vercel free plan allows **10 seconds** max execution per serverless function.
The bot runs all 28 APIs **concurrently** so it finishes within the limit.
If it times out, reduce the number of APIs in `bot.py` → `run_fast()`.