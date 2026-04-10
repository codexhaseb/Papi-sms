#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vercel Serverless Webhook Handler for Telegram Bot
"""

import json
import os
import asyncio
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)

# Import handlers from bot.py
from bot import (
    start,
    button_handler,
    receive_number,
    cancel,
    WAITING_FOR_NUMBER,
    BOT_TOKEN,
)

# Build application once
_app = None

def get_app():
    global _app
    if _app is None:
        _app = Application.builder().token(BOT_TOKEN).build()

        conv_handler = ConversationHandler(
            entry_points=[CallbackQueryHandler(button_handler, pattern="^start_attack$")],
            states={
                WAITING_FOR_NUMBER: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, receive_number)
                ],
            },
            fallbacks=[CommandHandler("cancel", cancel)],
            per_message=False,
        )

        _app.add_handler(CommandHandler("start", start))
        _app.add_handler(conv_handler)
        _app.add_handler(CallbackQueryHandler(button_handler))
    return _app


async def process_update(body: dict):
    app = get_app()
    await app.initialize()
    update = Update.de_json(body, app.bot)
    await app.process_update(update)


def handler(request, response):
    """Vercel serverless function handler"""
    if request.method == "POST":
        try:
            body = request.body
            if isinstance(body, bytes):
                body = body.decode("utf-8")
            data = json.loads(body)
            asyncio.run(process_update(data))
            response.status_code = 200
            response.body = json.dumps({"ok": True})
        except Exception as e:
            response.status_code = 500
            response.body = json.dumps({"ok": False, "error": str(e)})
    else:
        response.status_code = 200
        response.body = json.dumps({"status": "SMS Bomber Bot is running!"})
    return response