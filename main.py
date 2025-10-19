# -*- coding: utf-8 -*-

import sys
import io
import os

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

os.environ['PYTHONUNBUFFERED'] = '1'

from database import init_db
from bot import bot, init_bot


def main():
    try:
        print("[*] Initializing database...", flush=True)
        init_db()
        
        print("[*] Initializing bot and registering handlers...", flush=True)
        init_bot()
        
        print("[*] Bot is running...", flush=True)
        print("[*] Press Ctrl+C to stop", flush=True)
        print("[*] Waiting for messages...", flush=True)
        
        import telebot
        telebot.logger.setLevel('DEBUG')
        
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
        
    except KeyboardInterrupt:
        print("\n[*] Bot stopped by user", flush=True)
    except Exception as e:
        print(f"[ERROR] Failed to start bot: {e}", flush=True)
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
