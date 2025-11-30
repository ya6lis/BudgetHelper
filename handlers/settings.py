# -*- coding: utf-8 -*-
"""
Handler для налаштувань користувача.
Використовує inline-клавіатури, модель User та локалізацію.
"""

from utils import send_main_menu, answer_callback
from locales import get_text, set_language
from database import ensure_user_exists, update_user_language, update_user_currency
from keyboards import create_settings_keyboard, create_language_keyboard, create_currency_keyboard
from utils.currency_converter import get_rate_info
from config.callbacks import (
    CALLBACK_SETTINGS,
    CALLBACK_SETTINGS_LANGUAGE,
    CALLBACK_SETTINGS_CURRENCY,
    CALLBACK_LANGUAGE_UK,
    CALLBACK_LANGUAGE_EN,
    CALLBACK_CURRENCY_UAH,
    CALLBACK_CURRENCY_USD,
    CALLBACK_CURRENCY_EUR,
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
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_SETTINGS_CURRENCY)
    def change_currency_menu(call):
        """Меню вибору валюти."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        # Отримуємо актуальні курси валют
        rate_info = get_rate_info(user_id=user_id)
        
        keyboard = create_currency_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_SETTINGS)
        bot.edit_message_text(
            get_text('settings_select_currency', user_id=user_id).format(rate_info),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
    
    @bot.callback_query_handler(func=lambda call: call.data in [CALLBACK_CURRENCY_UAH, CALLBACK_CURRENCY_USD, CALLBACK_CURRENCY_EUR])
    def process_currency_selection(call):
        """Обробка вибору валюти."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        
        if call.data == CALLBACK_CURRENCY_UAH:
            selected_currency = 'UAH'
        elif call.data == CALLBACK_CURRENCY_USD:
            selected_currency = 'USD'
        elif call.data == CALLBACK_CURRENCY_EUR:
            selected_currency = 'EUR'
        else:
            return
        
        update_user_currency(user_id, selected_currency)
        
        success_msg = get_text('settings_currency_changed', user_id=user_id).format(selected_currency)
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
