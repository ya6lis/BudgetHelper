# -*- coding: utf-8 -*-
from keyboards import finance_submenu, create_timeframe_keyboard, create_period_with_back_keyboard
from database import get_incomes_aggregated, get_expenses_aggregated, ensure_user_exists
from locales import get_text
from utils import send_main_menu, answer_callback, format_income_list, format_expense_list
from config.callbacks import (
    CALLBACK_MY_FINANCES,
    CALLBACK_VIEW_INCOMES,
    CALLBACK_VIEW_EXPENSES,
    CALLBACK_VIEW_GENERAL,
    CALLBACK_ANOTHER_PERIOD,
    CALLBACK_BACK_TO_FINANCES,
    CALLBACK_BACK_TO_VIEW_EXPENSES,
    CALLBACK_BACK_TO_VIEW_INCOMES,
    CALLBACK_TO_PERIOD,
)

def register_handlers(bot):
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_MY_FINANCES)
    def finance_start(call):
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        bot.edit_message_text(get_text('finance_menu_info', user_id=user_id), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=finance_submenu(user_id=user_id))
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_VIEW_INCOMES)
    def view_incomes_start(call):
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        bot.edit_message_text(get_text('view_incomes_select_period', user_id=user_id), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_timeframe_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_FINANCES))
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_VIEW_EXPENSES)
    def view_expenses_start(call):
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        bot.edit_message_text(get_text('view_expenses_select_period', user_id=user_id), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_timeframe_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_FINANCES))
    
    @bot.callback_query_handler(func=lambda call: call.data in CALLBACK_TO_PERIOD)
    def show_data_for_period(call):
        answer_callback(bot, call)
        period = CALLBACK_TO_PERIOD.get(call.data)
        if not period:
            return
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        message_text = call.message.text
        if 'дох' in message_text.lower() or 'income' in message_text.lower():
            data = get_incomes_aggregated(user_id, period)
            if not data or not data.get('incomes'):
                bot.edit_message_text(get_text('view_incomes_no_data', user_id=user_id), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_period_with_back_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_VIEW_INCOMES))
                return
            period_name = get_text(f'period_{period}', user_id=user_id)
            msg = format_income_list(data, period_name, user_id=user_id)
            back_callback = CALLBACK_BACK_TO_VIEW_INCOMES
        else:
            data = get_expenses_aggregated(user_id, period)
            if not data or not data.get('expenses'):
                bot.edit_message_text(get_text('view_expenses_no_data', user_id=user_id), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_period_with_back_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_VIEW_EXPENSES))
                return
            period_name = get_text(f'period_{period}', user_id=user_id)
            msg = format_expense_list(data, period_name, user_id=user_id)
            back_callback = CALLBACK_BACK_TO_VIEW_EXPENSES
        bot.edit_message_text(msg, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_period_with_back_keyboard(user_id=user_id, back_callback=back_callback))
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_ANOTHER_PERIOD)
    def another_period(call):
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        message_text = call.message.text
        if 'дох' in message_text.lower() or 'income' in message_text.lower():
            text = get_text('view_incomes_select_another', user_id=user_id)
            back_callback = CALLBACK_BACK_TO_FINANCES
        else:
            text = get_text('view_expenses_select_another', user_id=user_id)
            back_callback = CALLBACK_BACK_TO_FINANCES
        bot.edit_message_text(text, chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_timeframe_keyboard(user_id=user_id, back_callback=back_callback))
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_BACK_TO_FINANCES)
    def back_to_finances(call):
        """Повернення до меню фінансів."""
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        bot.edit_message_text(get_text('finance_menu_info', user_id=user_id), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=finance_submenu(user_id=user_id))
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_BACK_TO_VIEW_EXPENSES)
    def back_to_view_expenses(call):
        """Повернення до вибору періоду витрат."""
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        bot.edit_message_text(get_text('view_expenses_select_period', user_id=user_id), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_timeframe_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_FINANCES))
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_BACK_TO_VIEW_INCOMES)
    def back_to_view_incomes(call):
        """Повернення до вибору періоду доходів."""
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        bot.edit_message_text(get_text('view_incomes_select_period', user_id=user_id), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=create_timeframe_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_FINANCES))
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_VIEW_GENERAL)
    def view_general_finances(call):
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        answer_callback(bot, call, text=get_text('feature_not_ready', user_id=user_id))
