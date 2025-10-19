# -*- coding: utf-8 -*-

from telebot import types
from locales import get_text, get_time_frames


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(get_text('menu_my_finances')))
    markup.add(
        types.KeyboardButton(get_text('menu_add_expense')),
        types.KeyboardButton(get_text('menu_add_income'))
    )
    markup.add(types.KeyboardButton(get_text('menu_report')))
    markup.add(types.KeyboardButton(get_text('menu_settings')))
    return markup


def finance_submenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(get_text('menu_view_expenses')),
        types.KeyboardButton(get_text('menu_view_incomes'))
    )
    markup.add(types.KeyboardButton(get_text('menu_back')))
    return markup


def back_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.KeyboardButton(get_text('menu_back')))
    return markup


def create_timeframe_keyboard():
    time_frames = get_time_frames()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(period) for period in time_frames.keys()]
    buttons.append(types.KeyboardButton(get_text('menu_back')))
    markup.add(*buttons)
    return markup
