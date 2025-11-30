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
    CALLBACK_REPORT_DETAILED,
    CALLBACK_REPORT_QUICK,
    CALLBACK_BACK_TO_REPORT_MENU,
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


def create_income_types_keyboard(user_id=None, back_callback=CALLBACK_BACK_TO_MAIN):
    """Клавіатура вибору типу доходу."""
    from database import CategoryRepository
    from locales import translate_category_name
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Отримуємо категорії з бази (дефолтні + кастомні)
    categories = CategoryRepository.get_categories_by_type(user_id, 'income')
    
    buttons = []
    for cat in categories:
        # Перекладаємо назву категорії
        translated_name = translate_category_name(cat.name, user_id=user_id)
        buttons.append(
            types.InlineKeyboardButton(
                translated_name,
                callback_data=f'income_cat_{cat.id}'
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


def create_expense_types_keyboard(user_id=None, back_callback=CALLBACK_BACK_TO_MAIN):
    """Клавіатура вибору типу витрати."""
    from database import CategoryRepository
    from locales import translate_category_name
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    # Отримуємо категорії з бази (дефолтні + кастомні)
    categories = CategoryRepository.get_categories_by_type(user_id, 'expense')
    
    buttons = []
    for cat in categories:
        # Перекладаємо назву категорії
        translated_name = translate_category_name(cat.name, user_id=user_id)
        buttons.append(
            types.InlineKeyboardButton(
                translated_name,
                callback_data=f'expense_cat_{cat.id}'
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
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton(
            get_text('settings_change_language', user_id=user_id),
            callback_data=CALLBACK_SETTINGS_LANGUAGE
        ),
        types.InlineKeyboardButton(
            get_text('settings_manage_categories', user_id=user_id),
            callback_data='category_management'
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


def create_category_management_menu(user_id=None):
    """Меню управління категоріями."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(
        types.InlineKeyboardButton(
            get_text('add_category', user_id=user_id),
            callback_data='category_add_type_select'
        ),
        types.InlineKeyboardButton(
            get_text('view_categories', user_id=user_id),
            callback_data='category_view_type_select'
        )
    )
    markup.row(
        types.InlineKeyboardButton(
            get_text('menu_main', user_id=user_id),
            callback_data=CALLBACK_BACK_TO_MAIN
        ),
        types.InlineKeyboardButton(
            get_text('menu_back', user_id=user_id),
            callback_data=CALLBACK_BACK_TO_SETTINGS
        )
    )
    return markup


def create_category_type_selection(user_id=None, action='add'):
    """Вибір типу категорії (доходи/витрати)."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    callback_prefix = f'category_{action}_'
    
    markup.add(
        types.InlineKeyboardButton(
            get_text('income_categories', user_id=user_id),
            callback_data=f'{callback_prefix}income'
        ),
        types.InlineKeyboardButton(
            get_text('expense_categories', user_id=user_id),
            callback_data=f'{callback_prefix}expense'
        )
    )
    markup.row(
        types.InlineKeyboardButton(
            get_text('menu_main', user_id=user_id),
            callback_data=CALLBACK_BACK_TO_MAIN
        ),
        types.InlineKeyboardButton(
            get_text('menu_back', user_id=user_id),
            callback_data='category_management'
        )
    )
    return markup


def create_categories_list(user_id=None, categories=None, category_type='income'):
    """Список категорій з кнопками видалення."""
    from locales import translate_category_name
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    if categories:
        for cat in categories:
            # Перекладаємо назву категорії
            translated_name = translate_category_name(cat.name, user_id=user_id)
            markup.add(
                types.InlineKeyboardButton(
                    f"❌ {translated_name}",
                    callback_data=f'category_delete_{cat.id}'
                )
            )
    
    markup.add(
        types.InlineKeyboardButton(
            get_text('add_category', user_id=user_id),
            callback_data=f'category_add_{category_type}'
        )
    )
    markup.row(
        types.InlineKeyboardButton(
            get_text('menu_main', user_id=user_id),
            callback_data=CALLBACK_BACK_TO_MAIN
        ),
        types.InlineKeyboardButton(
            get_text('menu_back', user_id=user_id),
            callback_data='category_view_type_select'
        )
    )
    return markup


def create_report_menu(user_id=None):
    """Меню вибору періоду для звіту."""
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(
            get_text('period_today', user_id=user_id),
            callback_data='detailed_today'
        ),
        types.InlineKeyboardButton(
            get_text('period_week', user_id=user_id),
            callback_data='detailed_week'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            get_text('period_month', user_id=user_id),
            callback_data='detailed_month'
        ),
        types.InlineKeyboardButton(
            get_text('period_year', user_id=user_id),
            callback_data='detailed_year'
        )
    )
    markup.add(
        types.InlineKeyboardButton(
            get_text('menu_back', user_id=user_id),
            callback_data=CALLBACK_BACK_TO_MAIN
        )
    )
    return markup
