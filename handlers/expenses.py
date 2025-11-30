# -*- coding: utf-8 -*-
"""
Handler для обробки витрат користувача.
Використовує inline-клавіатури, моделі та локалізацію.
"""

from telebot.apihelper import ApiTelegramException
from utils import send_main_menu, answer_callback, validate_amount
from database import add_expense, ensure_user_exists, CategoryRepository, get_user
from locales import get_text, get_current_language, translate_category_name
from keyboards import create_expense_types_keyboard, back_button, create_transaction_currency_keyboard
from utils.currency_converter import convert_currency, format_amount_with_currency, get_currency_symbol
from config.callbacks import (
    CALLBACK_ADD_EXPENSE,
    CALLBACK_BACK_TO_MAIN,
    CALLBACK_BACK_TO_ADD_EXPENSE,
    CALLBACK_SKIP_DESCRIPTION,
    CALLBACK_EXPENSE_CURRENCY_PREFIX,
)

user_states = {}
user_message_history = {}


def register_handlers(bot):
    """Реєструє обробники повідомлень для витрат."""
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_ADD_EXPENSE)
    def expense_start(call):
        """Початок процесу додавання витрати."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        if user_id not in user_message_history:
            user_message_history[user_id] = []
        
        keyboard = create_expense_types_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_MAIN)
        bot.edit_message_text(
            get_text('expense_select_type', user_id=user_id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
        user_message_history[user_id].append(call.message.message_id)
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith('expense_cat_'))
    def expense_type_selected(call):
        """Обробка вибору типу витрати."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        # Отримуємо category_id з callback (тепер це UUID - текст)
        category_id = call.data.replace('expense_cat_', '')
        
        # Отримуємо категорію з бази
        category = CategoryRepository.get_category_by_id(category_id)
        
        if not category:
            send_main_menu(bot, call.message.chat.id, 'error', call.message.message_id)
            return
        
        user_states[user_id] = {
            'action': 'waiting_expense_amount',
            'expense_category_id': category_id,
            'message_id': call.message.message_id
        }
        
        translated_category_name = translate_category_name(category.name, user_id=user_id)
        bot.edit_message_text(
            get_text('expense_enter_amount', user_id=user_id).format(translated_category_name),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button(user_id=user_id, back_callback=CALLBACK_BACK_TO_ADD_EXPENSE)
        )
    
    @bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('action') == 'waiting_expense_amount')
    def process_expense_amount(message):
        """Обробка введеної суми витрати."""
        user_id = message.from_user.id
        ensure_user_exists(user_id, message.from_user.username)
        
        text = message.text.strip()
        state = user_states.get(user_id, {})
        category_id = state.get('expense_category_id')
        
        if not category_id:
            send_main_menu(bot, message.chat.id, 'error', user_id=user_id)
            user_states.pop(user_id, None)
            return
        
        is_valid, amount = validate_amount(text)
        
        if is_valid:
            # Зберігаємо суму і переходимо до запиту опису
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                pass
            
            error_msg_id = state.get('error_message_id')
            if error_msg_id:
                try:
                    bot.delete_message(message.chat.id, error_msg_id)
                except Exception:
                    pass
            
            user_states[user_id]['action'] = 'waiting_expense_currency'
            user_states[user_id]['expense_amount'] = amount
            
            # Show currency selection keyboard
            keyboard = create_transaction_currency_keyboard(user_id, transaction_type='expense', back_callback=CALLBACK_BACK_TO_ADD_EXPENSE)
            
            prompt_msg_id = state.get('message_id')
            if prompt_msg_id:
                try:
                    bot.edit_message_text(
                        get_text('select_transaction_currency', user_id=user_id),
                        chat_id=message.chat.id,
                        message_id=prompt_msg_id,
                        reply_markup=keyboard
                    )
                except Exception:
                    # Якщо не вдалося редагувати, створюємо нове повідомлення
                    msg = bot.send_message(
                        message.chat.id,
                        get_text('select_transaction_currency', user_id=user_id),
                        reply_markup=keyboard
                    )
                    user_states[user_id]['message_id'] = msg.message_id
            else:
                msg = bot.send_message(
                    message.chat.id,
                    get_text('select_transaction_currency', user_id=user_id),
                    reply_markup=keyboard
                )
                user_states[user_id]['message_id'] = msg.message_id
        else:
            try:
                bot.delete_message(message.chat.id, message.message_id)
            except Exception:
                pass
            
            error_msg_id = state.get('error_message_id')
            if error_msg_id:
                try:
                    bot.delete_message(message.chat.id, error_msg_id)
                except Exception:
                    pass
            
            error_msg = bot.send_message(
                message.chat.id,
                get_text('expense_invalid_amount', user_id=user_id),
                reply_markup=back_button(user_id=user_id, back_callback=CALLBACK_BACK_TO_ADD_EXPENSE)
            )
            user_states[user_id]['error_message_id'] = error_msg.message_id
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith(CALLBACK_EXPENSE_CURRENCY_PREFIX))
    def process_expense_currency_selection(call):
        """Обробка вибору валюти для витрати."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        state = user_states.get(user_id, {})
        if state.get('action') != 'waiting_expense_currency':
            return
        
        # Extract currency from callback data
        currency = call.data.replace(CALLBACK_EXPENSE_CURRENCY_PREFIX, '').upper()
        state['expense_currency'] = currency
        state['action'] = 'waiting_expense_description'
        
        # Створюємо клавіатуру з кнопкою "Пропустити"
        from telebot import types
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton(
            get_text('expense_skip_description', user_id=user_id),
            callback_data=CALLBACK_SKIP_DESCRIPTION
        ))
        
        # Show conversion info if currency differs from default
        user = get_user(user_id)
        amount = state.get('expense_amount')
        conversion_text = ""
        
        if currency != user.default_currency and amount:
            converted_amount = convert_currency(amount, currency, user.default_currency)
            if converted_amount:
                converted_formatted = format_amount_with_currency(converted_amount, user.default_currency)
                currency_symbol = get_currency_symbol(user.default_currency)
                conversion_text = "\n\n" + get_text('currency_conversion_info', user_id=user_id).format(
                    currency_symbol,
                    converted_formatted
                )
        
        try:
            bot.edit_message_text(
                get_text('expense_enter_description', user_id=user_id) + conversion_text,
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                reply_markup=markup
            )
        except Exception:
            pass
    
    @bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('action') == 'waiting_expense_description')
    def process_expense_description(message):
        """Обробка введеного опису витрати."""
        user_id = message.from_user.id
        ensure_user_exists(user_id, message.from_user.username)
        
        state = user_states.get(user_id, {})
        category_id = state.get('expense_category_id')
        amount = state.get('expense_amount')
        currency = state.get('expense_currency', 'UAH')
        
        if not category_id or not amount:
            send_main_menu(bot, message.chat.id, 'error', user_id=user_id)
            user_states.pop(user_id, None)
            return
        
        description = message.text.strip() if message.text else None
        
        # Створюємо витрату з описом
        expense = add_expense(user_id, amount, category_id, description=description, currency=currency)
        
        # Видаляємо повідомлення
        message_ids_to_delete = user_message_history.get(user_id, [])
        for msg_id in message_ids_to_delete:
            try:
                bot.delete_message(message.chat.id, msg_id)
            except Exception:
                pass
        
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except Exception:
            pass
        
        prompt_msg_id = state.get('message_id')
        if prompt_msg_id:
            try:
                bot.delete_message(message.chat.id, prompt_msg_id)
            except Exception:
                pass
        
        user_message_history.pop(user_id, None)
        user_states.pop(user_id, None)
        
        # Отримуємо категорію з бази
        category = CategoryRepository.get_category_by_id(category_id)
        category_display = category.name if category else "Витрата"
        
        # Format amount with currency
        amount_text = format_amount_with_currency(expense.amount, expense.currency)
        
        # Вибираємо повідомлення залежно від того, чи є опис
        if description:
            success_msg = get_text('expense_added_with_description', user_id=user_id).format(
                amount_text,
                category_display,
                description
            )
        else:
            success_msg = get_text('expense_added', user_id=user_id).format(
                amount_text,
                category_display
            )
        
        send_main_menu(bot, message.chat.id, success_msg, user_id=user_id)
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_SKIP_DESCRIPTION and user_states.get(call.from_user.id, {}).get('action') == 'waiting_expense_description')
    def skip_expense_description(call):
        """Пропуск введення опису витрати."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        state = user_states.get(user_id, {})
        category_id = state.get('expense_category_id')
        amount = state.get('expense_amount')
        currency = state.get('expense_currency', 'UAH')
        
        if not category_id or not amount:
            send_main_menu(bot, call.message.chat.id, 'error', call.message.message_id, user_id=user_id)
            user_states.pop(user_id, None)
            return
        
        # Створюємо витрату без опису
        expense = add_expense(user_id, amount, category_id, description=None, currency=currency)
        
        # Видаляємо повідомлення
        message_ids_to_delete = user_message_history.get(user_id, [])
        for msg_id in message_ids_to_delete:
            try:
                bot.delete_message(call.message.chat.id, msg_id)
            except Exception:
                pass
        
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        
        user_message_history.pop(user_id, None)
        user_states.pop(user_id, None)
        
        # Отримуємо категорію з бази
        category = CategoryRepository.get_category_by_id(category_id)
        category_display = category.name if category else get_text('expense_fallback', user_id=user_id)
        
        # Format amount with currency
        amount_text = format_amount_with_currency(expense.amount, expense.currency)
        
        success_msg = get_text('expense_added', user_id=user_id).format(
            amount_text,
            category_display
        )
        send_main_menu(bot, call.message.chat.id, success_msg, user_id=user_id)
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_BACK_TO_ADD_EXPENSE)
    def back_to_add_expense(call):
        """Повернення до вибору типу витрати."""
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        user_states.pop(user_id, None)
        
        keyboard = create_expense_types_keyboard(user_id=user_id, back_callback=CALLBACK_BACK_TO_MAIN)
        bot.edit_message_text(
            get_text('expense_select_type', user_id=user_id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )

