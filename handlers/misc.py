# -*- coding: utf-8 -*-
"""
Handler для кнопки "Назад" та інших службових callback'ів.
"""

from utils import send_main_menu, answer_callback
from locales import get_text
from config.callbacks import CALLBACK_BACK_TO_MAIN, CALLBACK_REPORT
from database import ensure_user_exists
from keyboards.main_keyboards import create_report_menu


def register_handlers(bot):
    """Реєструє обробники для службових callback'ів."""
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_BACK_TO_MAIN)
    def handle_back_to_main(call):
        """Обробка натискання кнопки 'Назад до головного меню'."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        username = call.from_user.username
        ensure_user_exists(user_id, username)
        
        # Видаляємо HTML звіт якщо він існує
        from handlers.report import html_report_messages
        if user_id in html_report_messages:
            try:
                bot.delete_message(call.message.chat.id, html_report_messages[user_id])
                del html_report_messages[user_id]
            except Exception as e:
                print(f"[DEBUG] Could not delete HTML report on back to main: {e}")
        
        send_main_menu(
            bot,
            call.message.chat.id,
            text_or_key='main_menu_info',
            message_id=call.message.message_id,
            user_id=user_id
        )
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_REPORT)
    def handle_report(call):
        """Обробка натискання кнопки 'Звіт / Аналіз бюджету'."""
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        text = get_text('report_menu', user_id=user_id)
        markup = create_report_menu(user_id)
        answer_callback(bot, call)
        bot.edit_message_text(
            text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )

