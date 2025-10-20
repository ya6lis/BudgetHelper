# -*- coding: utf-8 -*-
"""
Handler для обробки доходів користувача.
Використовує inline-клавіатури, моделі та локалізацію.
"""

from utils import (
    send_main_menu,
    answer_callback,
    validate_amount,
)
from database import add_income, ensure_user_exists
from locales import get_text, get_current_language, translate_income_category, get_category_key_from_callback
from keyboards import create_income_types_keyboard, back_button
from config.callbacks import (
    CALLBACK_ADD_INCOME,
    CALLBACK_BACK_TO_MAIN,
    CALLBACK_BACK_TO_ADD_INCOME,
    CALLBACK_INCOME_TYPE_PREFIX,
)

user_states = {}
user_message_history = {}


def register_handlers(bot):
    """Реєструє обробники повідомлень для доходів."""
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_ADD_INCOME)
    def income_start(call):
        """Початок процесу додавання доходу."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        if user_id not in user_message_history:
            user_message_history[user_id] = []
        
        keyboard = create_income_types_keyboard(lang=get_current_language(user_id), back_callback=CALLBACK_BACK_TO_MAIN)
        bot.edit_message_text(
            get_text('income_select_type', user_id=user_id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
        user_message_history[user_id].append(call.message.message_id)
    
    @bot.callback_query_handler(func=lambda call: call.data.startswith(CALLBACK_INCOME_TYPE_PREFIX))
    def income_type_selected(call):
        """Обробка вибору типу доходу."""
        answer_callback(bot, call)
        
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        callback_data = call.data
        
        category_key = get_category_key_from_callback(callback_data)
        
        if not category_key:
            send_main_menu(bot, call.message.chat.id, 'error', call.message.message_id)
            return
        
        income_type_display = translate_income_category(category_key, user_id=user_id)
        
        user_states[user_id] = {
            'action': 'waiting_income_amount',
            'income_category_key': category_key,
            'message_id': call.message.message_id
        }
        
        bot.edit_message_text(
            get_text('income_enter_amount', user_id=user_id).format(income_type_display),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=back_button(user_id=user_id, back_callback=CALLBACK_BACK_TO_ADD_INCOME)
        )
    
    @bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get('action') == 'waiting_income_amount')
    def process_income_amount(message):
        """Обробка введеної суми доходу."""
        user_id = message.from_user.id
        ensure_user_exists(user_id, message.from_user.username)
        
        text = message.text.strip()
        state = user_states.get(user_id, {})
        category_key = state.get('income_category_key')
        
        if not category_key:
            send_main_menu(bot, message.chat.id, 'error', user_id=user_id)
            user_states.pop(user_id, None)
            return
        
        is_valid, amount = validate_amount(text)
        
        if is_valid:
            income = add_income(user_id, amount, category_key)
            
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
            
            error_msg_id = state.get('error_message_id')
            if error_msg_id:
                try:
                    bot.delete_message(message.chat.id, error_msg_id)
                except Exception:
                    pass
            
            user_message_history.pop(user_id, None)
            user_states.pop(user_id, None)
            
            category_display = translate_income_category(category_key, user_id=user_id)
            success_msg = get_text('income_added', user_id=user_id).format(
                income.amount,
                category_display
            )
            send_main_menu(bot, message.chat.id, success_msg, user_id=user_id)
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
                get_text('income_invalid_amount', user_id=user_id),
                reply_markup=back_button(user_id=user_id, back_callback=CALLBACK_BACK_TO_ADD_INCOME)
            )
            user_states[user_id]['error_message_id'] = error_msg.message_id
    
    @bot.callback_query_handler(func=lambda call: call.data == CALLBACK_BACK_TO_ADD_INCOME)
    def back_to_add_income(call):
        """Повернення до вибору типу доходу."""
        answer_callback(bot, call)
        user_id = call.from_user.id
        ensure_user_exists(user_id, call.from_user.username)
        
        user_states.pop(user_id, None)
        
        keyboard = create_income_types_keyboard(lang=get_current_language(user_id), back_callback=CALLBACK_BACK_TO_MAIN)
        bot.edit_message_text(
            get_text('income_select_type', user_id=user_id),
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )


