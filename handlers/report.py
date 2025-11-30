# -*- coding: utf-8 -*-
"""
Обробники для звітів та аналізу бюджету.
Підтримує детальні та швидкі звіти за різні періоди.
"""

import os
from telebot import TeleBot, types
from locales import get_text, get_current_language
from keyboards.main_keyboards import (
    create_report_menu,
    back_button
)
from database import generate_user_report
from utils import format_detailed_report, format_compact_report, generate_html_report
from config.callbacks import (
    CALLBACK_REPORT_DETAILED,
    CALLBACK_REPORT_QUICK,
    CALLBACK_BACK_TO_REPORT_MENU,
    CALLBACK_BACK_TO_MAIN,
)
from utils.message_helpers import answer_callback

# Словник для збереження message_id файлів HTML звітів {user_id: message_id}
html_report_messages = {}


def report_menu(call: types.CallbackQuery, bot: TeleBot):
    """Показує меню вибору періоду для звіту."""
    user_id = call.from_user.id
    
    # Видаляємо попереднє повідомлення з HTML файлом, якщо воно існує
    if user_id in html_report_messages:
        try:
            bot.delete_message(call.message.chat.id, html_report_messages[user_id])
            del html_report_messages[user_id]
        except Exception as e:
            print(f"[DEBUG] Could not delete HTML report in menu: {e}")
    
    text = get_text('report_select_period', user_id=user_id)
    markup = create_report_menu(user_id)
    
    answer_callback(bot, call)
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


def show_detailed_report(call: types.CallbackQuery, bot: TeleBot, period: str):
    """Генерує та показує детальний звіт за вказаний період."""
    user_id = call.from_user.id
    
    # Генеруємо звіт з порівнянням
    report_data = generate_user_report(user_id, period, include_comparison=True)
    
    if report_data is None:
        text = get_text('report_no_data', user_id=user_id)
        markup = back_button(user_id, back_callback=CALLBACK_BACK_TO_REPORT_MENU)
        answer_callback(bot, call)
        bot.edit_message_text(
            text,
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
        return
    
    # Форматуємо детальний звіт
    text = format_detailed_report(report_data, user_id)
    
    # Створюємо клавіатуру з кнопкою для завантаження HTML
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            text=get_text('view_online_report', user_id=user_id),
            callback_data=f'html_detailed_{period}'
        )
    )
    markup.row(
        types.InlineKeyboardButton(
            text=get_text('menu_main', user_id=user_id),
            callback_data=CALLBACK_BACK_TO_MAIN
        ),
        types.InlineKeyboardButton(
            text=get_text('menu_back', user_id=user_id),
            callback_data=CALLBACK_BACK_TO_REPORT_MENU
        )
    )
    
    answer_callback(bot, call)
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup,
        parse_mode='HTML'
    )


def show_quick_report(call: types.CallbackQuery, bot: TeleBot, period: str):
    """Генерує та показує швидкий звіт за вказаний період (не використовується)."""
    # Функція залишена для зворотної сумісності з HTML генератором
    pass


def back_to_report_menu(call: types.CallbackQuery, bot: TeleBot):
    """Повертає до вибору періоду звіту."""
    user_id = call.from_user.id
    
    # Видаляємо попереднє повідомлення з HTML файлом, якщо воно існує
    if user_id in html_report_messages:
        try:
            bot.delete_message(call.message.chat.id, html_report_messages[user_id])
            del html_report_messages[user_id]
        except Exception as e:
            print(f"[DEBUG] Could not delete HTML report message on back: {e}")
    
    report_menu(call, bot)


def handle_report_period_callback(call: types.CallbackQuery, bot: TeleBot):
    """Обробляє вибір періоду для звіту."""
    callback_data = call.data
    
    # Визначаємо період (завжди детальний звіт)
    if callback_data.startswith('detailed_'):
        period = callback_data.replace('detailed_', '')
        show_detailed_report(call, bot, period)


def generate_and_send_html_report(call: types.CallbackQuery, bot: TeleBot):
    """Генерує HTML звіт та відправляє користувачу."""
    from database import save_bot_message, delete_bot_message
    
    user_id = call.from_user.id
    callback_data = call.data
    
    # Визначаємо період з callback_data
    if callback_data.startswith('html_detailed_'):
        period = callback_data.replace('html_detailed_', '')
        include_comparison = True
    elif callback_data.startswith('html_quick_'):
        period = callback_data.replace('html_quick_', '')
        include_comparison = False
    else:
        return
    
    answer_callback(bot, call)
    
    # Видаляємо попереднє повідомлення з файлом, якщо воно існує
    if user_id in html_report_messages:
        try:
            bot.delete_message(call.message.chat.id, html_report_messages[user_id])
            # Видаляємо його також з бази даних
            delete_bot_message(user_id, html_report_messages[user_id])
            del html_report_messages[user_id]
        except Exception as e:
            print(f"[DEBUG] Could not delete previous HTML report message: {e}")
    
    # Показуємо повідомлення про генерацію
    status_msg = bot.send_message(
        call.message.chat.id,
        get_text('generating_html_report', user_id=user_id)
    )
    
    # Зберігаємо message_id статусного повідомлення в БД
    save_bot_message(user_id, status_msg.message_id)
    
    try:
        # Генеруємо дані звіту
        report_data = generate_user_report(user_id, period, include_comparison=include_comparison)
        
        if report_data is None:
            bot.edit_message_text(
                get_text('report_no_data', user_id=user_id),
                chat_id=call.message.chat.id,
                message_id=status_msg.message_id
            )
            return
        
        # Отримуємо мову користувача
        lang = get_current_language(user_id)
        
        # Генеруємо HTML файл
        html_filepath = generate_html_report(report_data, user_id, lang)
        
        # Видаляємо статусне повідомлення
        bot.delete_message(call.message.chat.id, status_msg.message_id)
        # Видаляємо його також з бази даних
        delete_bot_message(user_id, status_msg.message_id)
        
        # Відправляємо HTML файл
        with open(html_filepath, 'rb') as file:
            sent_msg = bot.send_document(
                call.message.chat.id,
                file,
                caption=get_text('online_report_generated', user_id=user_id),
                visible_file_name=f'budget_report_{period}.html'
            )
        
        # Зберігаємо message_id відправленого файлу
        html_report_messages[user_id] = sent_msg.message_id
        
        # Зберігаємо message_id в базі даних для очищення при перезапуску
        save_bot_message(user_id, sent_msg.message_id)
        
        # Видаляємо файл після відправки
        try:
            os.remove(html_filepath)
        except Exception as e:
            print(f"[DEBUG] Could not remove HTML file: {e}")
        
    except Exception as e:
        print(f"[ERROR] Failed to generate HTML report: {e}")
        import traceback
        traceback.print_exc()
        
        bot.edit_message_text(
            get_text('report_generation_error', user_id=user_id),
            chat_id=call.message.chat.id,
            message_id=status_msg.message_id
        )


def register_handlers(bot: TeleBot):
    """Реєструє всі обробники звітів."""
    
    # Головне меню звітів (показує вибір періоду)
    @bot.callback_query_handler(func=lambda call: call.data == 'main_report')
    def callback_report_menu(call):
        report_menu(call, bot)
    
    # Генерація HTML звіту (має бути перед іншими, щоб спрацював першим)
    @bot.callback_query_handler(func=lambda call: call.data.startswith('html_'))
    def callback_html_report(call):
        generate_and_send_html_report(call, bot)
    
    # Вибір періоду для звіту (тепер тільки detailed_)
    @bot.callback_query_handler(func=lambda call: call.data.startswith('detailed_'))
    def callback_report_period(call):
        handle_report_period_callback(call, bot)
    
    # Навігація назад (більше не потрібен, але залишаємо для сумісності)
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_BACK_TO_REPORT_MENU)
    def callback_back_to_menu(call):
        back_to_report_menu(call, bot)
