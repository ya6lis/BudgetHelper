# -*- coding: utf-8 -*-

import sys
import io
import os

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

os.environ['PYTHONUNBUFFERED'] = '1'

from database import init_db, get_all_user_ids, get_user_bot_messages, clear_user_bot_messages
from bot import bot, init_bot


def clear_chat_history():
    """Очищує історію чату для всіх користувачів."""
    try:
        print("[*] Clearing chat history for all users...", flush=True)
        user_ids = get_all_user_ids()
        
        for user_id in user_ids:
            try:
                # Отримуємо всі збережені message_id для цього користувача
                message_ids = get_user_bot_messages(user_id)
                
                # Видаляємо всі повідомлення
                deleted_count = 0
                for msg_id in message_ids:
                    try:
                        bot.delete_message(user_id, msg_id)
                        deleted_count += 1
                    except Exception:
                        # Ігноруємо помилки (повідомлення вже видалено або недоступно)
                        pass
                
                # Очищаємо список збережених повідомлень
                clear_user_bot_messages(user_id)
                
                if deleted_count > 0:
                    print(f"[OK] Deleted {deleted_count} messages for user {user_id}", flush=True)
                
            except Exception as e:
                print(f"[WARNING] Could not process user {user_id}: {e}", flush=True)
        
        print(f"[OK] Processed {len(user_ids)} users", flush=True)
    except Exception as e:
        print(f"[WARNING] Could not clear chat history: {e}", flush=True)


def main():
    try:
        print("[*] Initializing database...", flush=True)
        init_db()
        
        print("[*] Initializing bot and registering handlers...", flush=True)
        init_bot()
        
        # Очищаємо історію чату та відправляємо /start всім користувачам
        clear_chat_history()
        
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
