#!/usr/bin/env python3
"""
Run this script ONCE after deploying to Vercel to register the webhook.
Usage: BOT_TOKEN=xxx VERCEL_URL=https://your-app.vercel.app python set_webhook.py
"""

import urllib.request
import urllib.parse
import json
import os

BOT_TOKEN  = os.environ.get("BOT_TOKEN",  "8787428715:AAGP9FBh0gX5q8TO-d5u_6Ghvj3Zs-LTR4w")
VERCEL_URL = os.environ.get("VERCEL_URL", "https://your-app.vercel.app")

WEBHOOK_URL = f"{VERCEL_URL}/webhook"
API_URL     = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"

data = urllib.parse.urlencode({"url": WEBHOOK_URL}).encode()
req  = urllib.request.Request(API_URL, data=data)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())

if result.get("ok"):
    print(f"✅ Webhook set successfully!")
    print(f"   URL: {WEBHOOK_URL}")
else:
    print(f"❌ Failed: {result}")