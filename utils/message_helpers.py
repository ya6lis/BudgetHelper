# -*- coding: utf-8 -*-

from telebot import types
from keyboards import main_menu, back_button
from locales import get_text


def send_main_menu(bot, chat_id, text_or_key='back_to_main'):
    if any(text_or_key.startswith(emoji) for emoji in ['✅', '⬅️', '👋', '⚠️', '📊', '💰', '💸', '🔙']):
        text = text_or_key
    else:
        text = get_text(text_or_key)
    bot.send_message(chat_id, text, reply_markup=main_menu())


def send_back_button(bot, chat_id, text):
    bot.send_message(chat_id, text, reply_markup=back_button())


def send_with_keyboard(bot, chat_id, text, keyboard):
    bot.send_message(chat_id, text, reply_markup=keyboard)


def create_keyboard_from_list(items, add_back=True, row_width=2):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    buttons = [types.KeyboardButton(item) for item in items]
    
    if add_back:
        buttons.append(types.KeyboardButton(get_text('menu_back')))
    
    markup.add(*buttons)
    return markup


def create_menu_keyboard(items, row_width=1):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    for item in items:
        markup.add(types.KeyboardButton(item))
    return markup
