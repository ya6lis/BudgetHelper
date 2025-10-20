# -*- coding: utf-8 -*-
"""
Handler для налаштувань користувача.
Використовує inline-клавіатури, модель User та локалізацію.
"""

from utils import send_main_menu, answer_callback
from locales import get_text, set_language
from database import ensure_user_exists, update_user_language
from keyboards import create_settings_keyboard, create_language_keyboard
from config.callbacks import (
    CALLBACK_SETTINGS,
    CALLBACK_SETTINGS_LANGUAGE,
    CALLBACK_LANGUAGE_UK,
    CALLBACK_LANGUAGE_EN,
    CALLBACK_BACK_TO_MAIN,
    CALLBACK_BACK_TO_SETTINGS,
)


def register_handlers(bot):
    """Реєструє обробники повідомлень для налаштувань."""
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_SETTINGS)
    def settings_menu(call):
        """Меню налаштувань."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        username = call.from_user.username
        ensure_user_exists(user_id, username)
        
        keyboard = create_settings_keyboard(user_id=user_id)
        bot.edit_message_text(
            get_text('settings_menu', user_id=user_id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_SETTINGS_LANGUAGE)
    def change_language_menu(call):
        """Меню вибору мови."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        keyboard = create_language_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_SETTINGS)
        bot.edit_message_text(
            get_text('settings_select_language', user_id=user_id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
    
    @bot.callback_query_handler(func=lambda call: call.data in [CALLBACK_LANGUAGE_UK, CALLBACK_LANGUAGE_EN])
    def process_language_selection(call):
        """Обробка вибору мови."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        
        if call.data == CALLBACK_LANGUAGE_UK:
            selected_lang = 'uk'
        elif call.data == CALLBACK_LANGUAGE_EN:
            selected_lang = 'en'
        else:
            return
        
        update_user_language(user_id, selected_lang)
        set_language(user_id, selected_lang)
        
        success_msg = get_text('settings_language_changed', user_id=user_id)
        send_main_menu(
            bot,
            call.message.chat.id,
            success_msg,
            call.message.message_id,
            user_id=user_id
        )
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_BACK_TO_SETTINGS)
    def back_to_settings(call):
        """Повернення до меню налаштувань."""
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        keyboard = create_settings_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_MAIN)
        bot.edit_message_text(
            get_text('settings_menu', user_id=user_id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
