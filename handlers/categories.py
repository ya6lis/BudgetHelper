# -*- coding: utf-8 -*-
"""
Обробники для управління категоріями.
"""

from typing import Optional
from telebot import TeleBot, types
from telebot.apihelper import ApiTelegramException
from locales import get_text
from locales.locale_manager import translate_category_name
from keyboards.main_keyboards import (
    create_category_management_menu,
    create_category_type_selection,
    create_categories_list,
    back_button
)
from database import CategoryRepository
from config.callbacks import CALLBACK_BACK_TO_SETTINGS
from utils.message_helpers import answer_callback


# Словник для зберігання стану додавання категорії {user_id: {'type': 'income/expense', 'step': 'name'}}
category_creation_state = {}


def category_management_menu(call: types.CallbackQuery, bot: TeleBot):
    """Показує меню управління категоріями."""
    user_id = call.from_user.id
    
    text = get_text('category_management_menu', user_id=user_id)
    markup = create_category_management_menu(user_id)
    
    answer_callback(bot, call)
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


def add_category_select_type(call: types.CallbackQuery, bot: TeleBot):
    """Вибір типу категорії для додавання."""
    user_id = call.from_user.id
    
    text = get_text('select_category_type_to_add', user_id=user_id)
    markup = create_category_type_selection(user_id, action='add')
    
    answer_callback(bot, call)
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


def add_category_start(call: types.CallbackQuery, bot: TeleBot, category_type: str):
    """Початок процесу додавання категорії."""
    user_id = call.from_user.id
    
    # Зберігаємо стан
    category_creation_state[user_id] = {
        'type': category_type,
        'step': 'name',
        'message_id': call.message.message_id,
        'chat_id': call.message.chat.id
    }
    
    type_name = get_text('income_type_label' if category_type == 'income' else 'expense_type_label', user_id=user_id)
    text = get_text('enter_category_name', user_id=user_id).format(type_name)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_back', user_id=user_id),
            callback_data='category_add_type_select'
        )
    )
    
    answer_callback(bot, call)
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


def handle_category_name_input(message: types.Message, bot: TeleBot):
    """Обробка введення назви категорії."""
    user_id = message.from_user.id
    
    if user_id not in category_creation_state:
        return
    
    state = category_creation_state[user_id]
    if state['step'] != 'name':
        return
    
    # Видаляємо повідомлення користувача
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except ApiTelegramException:
        pass
    
    category_name = message.text.strip()
    
    # Перевірка на порожню назву
    if not category_name:
        text = get_text('category_name_empty', user_id=user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data='category_add_type_select'
            )
        )
        bot.edit_message_text(
            text,
            chat_id=state['chat_id'],
            message_id=state['message_id'],
            reply_markup=markup
        )
        return
    
    # Перевірка на довжину
    if len(category_name) > 50:
        text = get_text('category_name_too_long', user_id=user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data='category_add_type_select'
            )
        )
        bot.edit_message_text(
            text,
            chat_id=state['chat_id'],
            message_id=state['message_id'],
            reply_markup=markup
        )
        return
    
    # Перевірка чи існує категорія
    if CategoryRepository.category_exists(user_id, category_name, state['type']):
        text = get_text('category_already_exists', user_id=user_id).format(category_name)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data='category_add_type_select'
            )
        )
        bot.edit_message_text(
            text,
            chat_id=state['chat_id'],
            message_id=state['message_id'],
            reply_markup=markup
        )
        return
    
    # Створюємо категорію
    create_category_and_notify(user_id, category_name, state['type'], bot, state['chat_id'], state['message_id'])





def create_category_and_notify(user_id: int, name: str, category_type: str, bot: TeleBot, chat_id: int, message_id: int):
    """Створює категорію і відправляє повідомлення."""
    cat_id = CategoryRepository.add_custom_category(user_id, name, category_type)
    
    if cat_id:
        text = get_text('category_created_success', user_id=user_id).format(name)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                get_text('add_another_category', user_id=user_id),
                callback_data='category_add_type_select'
            )
        )
        markup.row(
            types.InlineKeyboardButton(
                get_text('menu_main', user_id=user_id),
                callback_data='back_to_main'
            ),
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data='category_management'
            )
        )
        
        bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=markup)
    else:
        text = get_text('category_creation_failed', user_id=user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data='category_management'
            )
        )
        bot.edit_message_text(text, chat_id=chat_id, message_id=message_id, reply_markup=markup)
    
    # Очищаємо стан
    if user_id in category_creation_state:
        del category_creation_state[user_id]


def view_categories_select_type(call: types.CallbackQuery, bot: TeleBot):
    """Вибір типу категорії для перегляду."""
    user_id = call.from_user.id
    
    text = get_text('select_category_type_to_view', user_id=user_id)
    markup = create_category_type_selection(user_id, action='view')
    
    answer_callback(bot, call)
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


def view_categories_list(call: types.CallbackQuery, bot: TeleBot, category_type: str):
    """Показує список категорій."""
    user_id = call.from_user.id
    
    categories = CategoryRepository.get_categories_by_type(user_id, category_type)
    
    type_name = get_text('income_type_label' if category_type == 'income' else 'expense_type_label', user_id=user_id)
    text = get_text('categories_list_title', user_id=user_id).format(type_name) + '\n\n'
    
    default_cats = [cat for cat in categories if cat.is_default]
    custom_cats = [cat for cat in categories if not cat.is_default]
    
    if default_cats:
        text += get_text('default_categories', user_id=user_id) + '\n'
        for cat in default_cats:
            # Перекладаємо дефолтні категорії
            translated_name = translate_category_name(cat.name, user_id=user_id)
            text += f"  • {translated_name}\n"
        text += '\n'
    
    if custom_cats:
        text += get_text('custom_categories', user_id=user_id) + '\n'
        for cat in custom_cats:
            text += f"  • {cat.name}\n"
    else:
        text += get_text('no_custom_categories', user_id=user_id)
    
    markup = create_categories_list(user_id, custom_cats, category_type)
    
    answer_callback(bot, call)
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


def delete_category_confirm(call: types.CallbackQuery, bot: TeleBot, category_id: int):
    """Підтвердження видалення категорії."""
    user_id = call.from_user.id
    
    category = CategoryRepository.get_category_by_id(category_id)
    
    if not category or category.user_id != user_id:
        answer_callback(bot, call, get_text('category_not_found', user_id=user_id))
        return
    
    text = get_text('confirm_delete_category', user_id=user_id).format(category.name)
    
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton(
            get_text('confirm_delete', user_id=user_id),
            callback_data=f'category_delete_confirmed_{category_id}'
        ),
        types.InlineKeyboardButton(
            get_text('menu_back', user_id=user_id),
            callback_data=f'category_view_{category.type}'
        )
    )
    
    answer_callback(bot, call)
    bot.edit_message_text(
        text,
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=markup
    )


def delete_category_execute(call: types.CallbackQuery, bot: TeleBot, category_id: int):
    """Виконує видалення категорії."""
    user_id = call.from_user.id
    
    category = CategoryRepository.get_category_by_id(category_id)
    category_type = category.type if category else 'income'
    
    if CategoryRepository.delete_custom_category(user_id, category_id):
        answer_callback(bot, call, get_text('category_deleted_success', user_id=user_id))
    else:
        answer_callback(bot, call, get_text('category_deletion_failed', user_id=user_id))
    
    # Повертаємось до списку категорій
    view_categories_list(call, bot, category_type)


def register_handlers(bot: TeleBot):
    """Реєструє всі обробники категорій."""
    
    # Головне меню управління категоріями
    @bot.callback_query_handler(func=lambda call: call.data == 'category_management')
    def callback_category_menu(call):
        category_management_menu(call, bot)
    
    # Додавання категорії - вибір типу
    @bot.callback_query_handler(func=lambda call: call.data == 'category_add_type_select')
    def callback_add_type_select(call):
        add_category_select_type(call, bot)
    
    # Додавання категорії - початок
    @bot.callback_query_handler(func=lambda call: call.data.startswith('category_add_'))
    def callback_add_category(call):
        category_type = call.data.replace('category_add_', '')
        if category_type in ['income', 'expense']:
            add_category_start(call, bot, category_type)
    
    # Перегляд категорій - вибір типу
    @bot.callback_query_handler(func=lambda call: call.data == 'category_view_type_select')
    def callback_view_type_select(call):
        view_categories_select_type(call, bot)
    
    # Перегляд категорій - список
    @bot.callback_query_handler(func=lambda call: call.data.startswith('category_view_'))
    def callback_view_categories(call):
        category_type = call.data.replace('category_view_', '')
        if category_type in ['income', 'expense']:
            view_categories_list(call, bot, category_type)
    
    # Видалення категорії - підтвердження
    @bot.callback_query_handler(func=lambda call: call.data.startswith('category_delete_'))
    def callback_delete_category(call):
        if call.data.startswith('category_delete_confirmed_'):
            category_id = call.data.replace('category_delete_confirmed_', '')
            delete_category_execute(call, bot, category_id)
        else:
            category_id = call.data.replace('category_delete_', '')
            delete_category_confirm(call, bot, category_id)
    
    # Обробка текстових повідомлень для створення категорії
    @bot.message_handler(func=lambda message: message.from_user.id in category_creation_state and category_creation_state[message.from_user.id]['step'] == 'name')
    def handle_name(message):
        handle_category_name_input(message, bot)
