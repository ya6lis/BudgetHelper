# -*- coding: utf-8 -*-

from utils import (
    send_main_menu,
    send_back_button,
    create_keyboard_from_list,
    validate_amount,
    is_back_command,
)
from database import add_income
from locales import get_text, get_income_types

temp_income_types = {}


def register_handlers(bot):
    @bot.message_handler(func=lambda m: m.text == get_text('menu_add_income'))
    def income_start(message):
        income_types = get_income_types()
        markup = create_keyboard_from_list(income_types)
        bot.send_message(message.chat.id, get_text('income_select_type'), reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == get_text('menu_back'))
    def go_back(message):
        send_main_menu(bot, message.chat.id)

    @bot.message_handler(func=lambda m: m.text in get_income_types())
    def input_income_amount_standard(message):
        user_id = message.from_user.id
        income_type = message.text
        temp_income_types[user_id] = income_type
        send_back_button(bot, message.chat.id, get_text('income_enter_amount').format(income_type))
        bot.register_next_step_handler(message, process_income_amount, bot)


def process_income_amount(message, bot):
    user_id = message.from_user.id
    text = message.text.strip()
    income_types = get_income_types()
    income_type = temp_income_types.get(user_id, income_types[-1])

    if is_back_command(text):
        markup = create_keyboard_from_list(income_types)
        bot.send_message(message.chat.id, get_text('income_select_type'), reply_markup=markup)
        return

    is_valid, amount = validate_amount(text)
    
    if is_valid:
        add_income(user_id, amount, income_type)
        temp_income_types.pop(user_id, None)
        success_msg = get_text('income_added').format(amount, income_type)
        send_main_menu(bot, message.chat.id, success_msg)
    else:
        bot.send_message(message.chat.id, get_text('income_invalid_amount'))
        bot.register_next_step_handler(message, process_income_amount, bot)
