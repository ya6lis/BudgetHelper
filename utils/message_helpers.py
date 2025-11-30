# -*- coding: utf-8 -*-
"""
Helper функції для роботи з повідомленнями та inline-клавіатурами.
"""

import logging
from telebot import types
from telebot.apihelper import ApiTelegramException
from keyboards import main_menu, back_button
from locales import get_text

logger = logging.getLogger(__name__)

# Константи для обробки помилок
MESSAGE_NOT_MODIFIED = "message is not modified"


def send_main_menu(bot, chat_id, text_or_key='back_to_main', message_id=None, user_id=None):
    """
    Відправити головне меню.
    
    Args:
        bot: TeleBot instance
        chat_id: ID чату
        text_or_key: Текст або ключ локалізації
        message_id: ID повідомлення для редагування (опціонально)
        user_id: ID користувача для отримання його мови
    """
    if any(text_or_key.startswith(emoji) for emoji in ['✅', '⬅️', '👋', '⚠️', '📊', '💰', '💸', '🔙']):
        text = text_or_key
    else:
        text = get_text(text_or_key, user_id=user_id)
    
    markup = main_menu(user_id=user_id)
    
    if message_id:
        try:
            bot.edit_message_text(
                text,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=markup
            )
        except ApiTelegramException as e:
            if MESSAGE_NOT_MODIFIED not in str(e).lower():
                logger.warning(f"Failed to edit message in send_main_menu: {e}")
            bot.send_message(chat_id, text, reply_markup=markup)
    else:
        bot.send_message(chat_id, text, reply_markup=markup)


def send_back_button(bot, chat_id, text, message_id=None):
    """
    Відправити повідомлення з кнопкою назад.
    
    Args:
        bot: TeleBot instance
        chat_id: ID чату
        text: Текст повідомлення
        message_id: ID повідомлення для редагування (опціонально)
    """
    markup = back_button()
    
    if message_id:
        try:
            bot.edit_message_text(
                text,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=markup
            )
        except ApiTelegramException as e:
            if MESSAGE_NOT_MODIFIED not in str(e).lower():
                logger.warning(f"Failed to edit message in send_back_button: {e}")
            bot.send_message(chat_id, text, reply_markup=markup)
    else:
        bot.send_message(chat_id, text, reply_markup=markup)


def send_with_keyboard(bot, chat_id, text, keyboard, message_id=None):
    """
    Відправити повідомлення з кастомною клавіатурою.
    
    Args:
        bot: TeleBot instance
        chat_id: ID чату
        text: Текст повідомлення
        keyboard: InlineKeyboardMarkup
        message_id: ID повідомлення для редагування (опціонально)
    """
    if message_id:
        try:
            bot.edit_message_text(
                text,
                chat_id=chat_id,
                message_id=message_id,
                reply_markup=keyboard
            )
        except ApiTelegramException as e:
            if MESSAGE_NOT_MODIFIED not in str(e).lower():
                logger.warning(f"Failed to edit message: {e}")
            bot.send_message(chat_id, text, reply_markup=keyboard)
    else:
        bot.send_message(chat_id, text, reply_markup=keyboard)


def answer_callback(bot, callback_query, text=None, show_alert=False):
    """
    Відповісти на callback query.
    
    Args:
        bot: TeleBot instance
        callback_query: CallbackQuery object
        text: Текст відповіді (опціонально)
        show_alert: Показати як alert (True) чи toast (False)
    """
    bot.answer_callback_query(
        callback_query.id,
        text=text,
        show_alert=show_alert
    )


def create_inline_keyboard_from_dict(items_dict, row_width=2, add_back=True):
    """
    Створити inline-клавіатуру зі словника.
    
    Args:
        items_dict: Словник {текст: callback_data}
        row_width: Кількість кнопок в ряду
        add_back: Додати кнопку назад
    
    Returns:
        InlineKeyboardMarkup
    """
    from config.callbacks import CALLBACK_BACK_TO_MAIN
    
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    buttons = [
        types.InlineKeyboardButton(text, callback_data=callback_data)
        for text, callback_data in items_dict.items()
    ]
    
    # Додаємо кнопки
    for i in range(0, len(buttons), row_width):
        row_buttons = buttons[i:i + row_width]
        markup.add(*row_buttons)
    
    if add_back:
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back'),
                callback_data=CALLBACK_BACK_TO_MAIN
            )
        )
    
    return markup


def edit_or_send_message(bot, chat_id, message_id, text, reply_markup=None):
    """
    Редагувати існуюче повідомлення або відправити нове.
    
    Args:
        bot: TeleBot instance
        chat_id: ID чату
        message_id: ID повідомлення для редагування
        text: Текст повідомлення
        reply_markup: Клавіатура (опціонально)
    """
    try:
        bot.edit_message_text(
            text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=reply_markup
        )
    except ApiTelegramException as e:
        if MESSAGE_NOT_MODIFIED not in str(e).lower():
            logger.warning(f"Failed to edit message in edit_or_send_message: {e}")
        bot.send_message(chat_id, text, reply_markup=reply_markup)
