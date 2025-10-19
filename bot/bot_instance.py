# -*- coding: utf-8 -*-

from telebot import TeleBot
from config.config import TOKEN

print("[*] Creating bot instance...", flush=True)
bot = TeleBot(TOKEN, parse_mode='HTML')

try:
    bot_info = bot.get_me()
    print(f"[OK] Bot instance created: @{bot_info.username}", flush=True)
except Exception as e:
    print(f"[ERROR] Cannot connect to Telegram API: {e}", flush=True)
    print("[!] Please check your internet connection and TOKEN", flush=True)
    raise


def init_bot():
    try:
        print("[*] Importing handlers...", flush=True)
        from handlers import start, income, finance, misc
        
        print("[*] Registering handlers...", flush=True)
        start.register_handlers(bot)
        income.register_handlers(bot)
        finance.register_handlers(bot)
        misc.register_handlers(bot)
        
        print("[OK] Bot initialized successfully!", flush=True)
        print("[OK] Registered handlers: start, income, finance, misc", flush=True)
        return bot
        
    except Exception as e:
        print(f"[ERROR] Failed to initialize bot: {e}", flush=True)
        raise
