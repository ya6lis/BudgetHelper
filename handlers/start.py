# -*- coding: utf-8 -*-
"""
Handler для стартових команд.
Використовує inline-клавіатури та локалізацію.
"""

from utils import send_main_menu
from locales import get_text
from database import ensure_user_exists


def register_handlers(bot):
    """Реєструє обробники стартових команд."""
    
    @bot.message_handler(commands=['start', 'help'])
    def welcome(message):
        """Обробка команд /start та /help."""
        user_id = message.from_user.id
        username = message.from_user.username
        
        ensure_user_exists(user_id, username)
        send_main_menu(bot, message.chat.id, 'welcome', user_id=user_id)
