# -*- coding: utf-8 -*-
"""
Inline-клавіатури для Budget Helper бота.
Використовує InlineKeyboardMarkup з callback_query.
"""

from telebot import types
from locales import get_text, get_income_types, get_expense_types
from config.callbacks import (
    CALLBACK_MY_FINANCES,
    CALLBACK_ADD_INCOME,
    CALLBACK_ADD_EXPENSE,
    CALLBACK_REPORT,
    CALLBACK_SETTINGS,
    CALLBACK_VIEW_INCOMES,
    CALLBACK_VIEW_EXPENSES,
    CALLBACK_VIEW_GENERAL,
    CALLBACK_BACK_TO_MAIN,
    CALLBACK_BACK_TO_FINANCES,
    CALLBACK_BACK_TO_VIEW_EXPENSES,
    CALLBACK_BACK_TO_VIEW_INCOMES,
    CALLBACK_BACK_TO_ADD_INCOME,
    CALLBACK_BACK_TO_ADD_EXPENSE,
    CALLBACK_BACK_TO_SETTINGS,
    CALLBACK_PERIOD_TODAY,
    CALLBACK_PERIOD_WEEK,
    CALLBACK_PERIOD_MONTH,
    CALLBACK_PERIOD_YEAR,
    CALLBACK_ANOTHER_PERIOD,
    CALLBACK_BACK,
    INCOME_TYPE_CALLBACKS,
    EXPENSE_TYPE_CALLBACKS,
    CALLBACK_SETTINGS_LANGUAGE,
    CALLBACK_LANGUAGE_UK,
    CALLBACK_LANGUAGE_EN,
)


def main_menu(user_id=None):
    """Головне меню з inline-кнопками."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_my_finances', user_id=user_id),
            callback_data=CALLBACK_MY_FINANCES
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_add_income', user_id=user_id),
            callback_data=CALLBACK_ADD_INCOME
        ),
        types.InlineKeyboardButton(
            get_text('menu_add_expense', user_id=user_id),
            callback_data=CALLBACK_ADD_EXPENSE
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_report', user_id=user_id),
            callback_data=CALLBACK_REPORT
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_settings', user_id=user_id),
            callback_data=CALLBACK_SETTINGS
        )
    )
    return markup


def finance_submenu(user_id=None):
    """Підменю фінансів."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_view_incomes', user_id=user_id),
            callback_data=CALLBACK_VIEW_INCOMES
        ),
        types.InlineKeyboardButton(
            get_text('menu_view_expenses', user_id=user_id),
            callback_data=CALLBACK_VIEW_EXPENSES
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_view_general_finances', user_id=user_id),
            callback_data=CALLBACK_VIEW_GENERAL
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_back', user_id=user_id),
            callback_data=CALLBACK_BACK_TO_MAIN
        )
    )
    return markup


def back_button(user_id=None, back_callback=CALLBACK_BACK_TO_MAIN, show_main_menu=True):
    """Кнопка назад з опціональною кнопкою головного меню."""
    markup = types.InlineKeyboardMarkup()
    if show_main_menu and back_callback != CALLBACK_BACK_TO_MAIN:
        markup.row(
            types.InlineKeyboardButton(
                get_text('menu_main', user_id=user_id),
                callback_data=CALLBACK_BACK_TO_MAIN
            ),
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    else:
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    return markup


def create_timeframe_keyboard(user_id=None, back_callback=CALLBACK_BACK_TO_MAIN):
    """Клавіатура вибору періоду часу."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            get_text('period_today', user_id=user_id),
            callback_data=CALLBACK_PERIOD_TODAY
        ),
        types.InlineKeyboardButton(
            get_text('period_week', user_id=user_id),
            callback_data=CALLBACK_PERIOD_WEEK
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            get_text('period_month', user_id=user_id),
            callback_data=CALLBACK_PERIOD_MONTH
        ),
        types.InlineKeyboardButton(
            get_text('period_year', user_id=user_id),
            callback_data=CALLBACK_PERIOD_YEAR
        )
    )
    if back_callback != CALLBACK_BACK_TO_MAIN:
        markup.row(
            types.InlineKeyboardButton(
                get_text('menu_main', user_id=user_id),
                callback_data=CALLBACK_BACK_TO_MAIN
            ),
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    else:
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    return markup


def create_income_types_keyboard(lang='uk', back_callback=CALLBACK_BACK_TO_MAIN):
    """Клавіатура вибору типу доходу."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    income_types = get_income_types(lang)
    callbacks = INCOME_TYPE_CALLBACKS.get(lang, INCOME_TYPE_CALLBACKS['uk'])
    
    buttons = []
    for income_type in income_types:
        callback_data = callbacks.get(income_type, CALLBACK_BACK)
        buttons.append(
            types.InlineKeyboardButton(
                income_type,
                callback_data=callback_data
            )
        )
    
    # Додаємо кнопки по 2 в ряд
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i + 1])
        else:
            markup.add(buttons[i])
    
    if back_callback != CALLBACK_BACK_TO_MAIN:
        markup.row(
            types.InlineKeyboardButton(
                get_text('menu_main'),
                callback_data=CALLBACK_BACK_TO_MAIN
            ),
            types.InlineKeyboardButton(
                get_text('menu_back'),
                callback_data=back_callback
            )
        )
    else:
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back'),
                callback_data=back_callback
            )
        )
    return markup


def create_expense_types_keyboard(lang='uk', back_callback=CALLBACK_BACK_TO_MAIN):
    """Клавіатура вибору типу витрати."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    expense_types = get_expense_types(lang)
    callbacks = EXPENSE_TYPE_CALLBACKS.get(lang, EXPENSE_TYPE_CALLBACKS['uk'])
    
    buttons = []
    for expense_type in expense_types:
        callback_data = callbacks.get(expense_type, CALLBACK_BACK)
        buttons.append(
            types.InlineKeyboardButton(
                expense_type,
                callback_data=callback_data
            )
        )
    
    # Додаємо кнопки по 2 в ряд
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i + 1])
        else:
            markup.add(buttons[i])
    
    if back_callback != CALLBACK_BACK_TO_MAIN:
        markup.row(
            types.InlineKeyboardButton(
                get_text('menu_main'),
                callback_data=CALLBACK_BACK_TO_MAIN
            ),
            types.InlineKeyboardButton(
                get_text('menu_back'),
                callback_data=back_callback
            )
        )
    else:
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back'),
                callback_data=back_callback
            )
        )
    return markup


def create_period_with_back_keyboard(user_id=None, back_callback=CALLBACK_BACK_TO_MAIN):
    """Клавіатура періоду з кнопкою 'Інший період' та 'Назад'."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_another_period', user_id=user_id),
            callback_data=CALLBACK_ANOTHER_PERIOD
        )
    )
    if back_callback != CALLBACK_BACK_TO_MAIN:
        markup.row(
            types.InlineKeyboardButton(
                get_text('menu_main', user_id=user_id),
                callback_data=CALLBACK_BACK_TO_MAIN
            ),
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    else:
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    return markup


def create_language_keyboard(user_id=None, back_callback=CALLBACK_BACK_TO_MAIN):
    """Клавіатура вибору мови."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            '🇺🇦 Українська',
            callback_data=CALLBACK_LANGUAGE_UK
        ),
        types.InlineKeyboardButton(
            '🇬🇧 English',
            callback_data=CALLBACK_LANGUAGE_EN
        )
    )
    if back_callback != CALLBACK_BACK_TO_MAIN:
        markup.row(
            types.InlineKeyboardButton(
                get_text('menu_main', user_id=user_id),
                callback_data=CALLBACK_BACK_TO_MAIN
            ),
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    else:
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    return markup


def create_settings_keyboard(user_id=None, back_callback=CALLBACK_BACK_TO_MAIN):
    """Клавіатура налаштувань."""
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(
            get_text('settings_change_language', user_id=user_id),
            callback_data=CALLBACK_SETTINGS_LANGUAGE
        )
    )
    if back_callback != CALLBACK_BACK_TO_MAIN:
        markup.row(
            types.InlineKeyboardButton(
                get_text('menu_main', user_id=user_id),
                callback_data=CALLBACK_BACK_TO_MAIN
            ),
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    else:
        markup.add(
            types.InlineKeyboardButton(
                get_text('menu_back', user_id=user_id),
                callback_data=back_callback
            )
        )
    return markup
