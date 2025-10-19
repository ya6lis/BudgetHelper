# -*- coding: utf-8 -*-

from telebot import types
from keyboards import create_timeframe_keyboard
from database import get_incomes_aggregated, get_expenses_aggregated
from locales import get_text, get_time_frames
from utils import (
    send_main_menu,
    send_back_button,
    create_menu_keyboard,
    format_income_list,
)


def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == get_text('menu_my_finances'))
    def finance_start(message):
        items = [
            get_text('menu_view_expenses'),
            get_text('menu_view_incomes'),
            get_text('menu_view_general_finances'),
            get_text('menu_back')
        ]
        markup = create_menu_keyboard(items)
        bot.send_message(message.chat.id, get_text('finance_select_option'), reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == get_text('menu_view_incomes'))
    def show_incomes_menu(message):
        bot.send_message(
            message.chat.id,
            get_text('view_incomes_select_period'),
            reply_markup=create_timeframe_keyboard()
        )
        bot.register_next_step_handler(message, incomes_menu_next_step)

    def incomes_menu_next_step(message):
        time_frames = get_time_frames()
        if message.text == get_text('menu_back'):
            send_main_menu(bot, message.chat.id)
        elif message.text in time_frames:
            show_incomes_filtered(message)
        else:
            bot.send_message(message.chat.id, get_text('view_incomes_invalid_choice'))
            show_incomes_menu(message)

    def show_incomes_filtered(message):
        user_id = message.from_user.id
        time_frames = get_time_frames()
        period = time_frames.get(message.text)

        if not period:
            bot.send_message(message.chat.id, get_text('view_incomes_period_error'))
            show_incomes_menu(message)
            return

        incomes = get_incomes_aggregated(user_id, period)

        if not incomes:
            send_back_button(bot, message.chat.id, get_text('view_incomes_no_data'))
            return

        msg = format_income_list(incomes, period, message.text)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        markup.add(
            types.KeyboardButton(get_text('menu_another_period')),
            types.KeyboardButton(get_text('menu_back'))
        )

        bot.send_message(message.chat.id, msg, reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == get_text('menu_back'))
    def back_to_main(message):
        send_main_menu(bot, message.chat.id)

    @bot.message_handler(func=lambda m: m.text == get_text('menu_another_period'))
    def period_back_to_incomes(message):
        bot.send_message(
            message.chat.id,
            get_text('view_incomes_select_another'),
            reply_markup=create_timeframe_keyboard()
        )
        bot.register_next_step_handler(message, incomes_menu_next_step)
