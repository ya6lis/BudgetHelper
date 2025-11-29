# -*- coding: utf-8 -*-
"""
Константи для callback_data в inline-клавіатурах.
"""

# Головне меню
CALLBACK_MY_FINANCES = 'main_finances'
CALLBACK_ADD_INCOME = 'main_add_income'
CALLBACK_ADD_EXPENSE = 'main_add_expense'
CALLBACK_REPORT = 'main_report'
CALLBACK_SETTINGS = 'main_settings'

# Фінанси - підменю
CALLBACK_VIEW_INCOMES = 'finance_view_incomes'
CALLBACK_VIEW_EXPENSES = 'finance_view_expenses'
CALLBACK_VIEW_GENERAL = 'finance_view_general'
CALLBACK_BACK_TO_MAIN = 'back_to_main'

# Періоди часу
CALLBACK_PERIOD_TODAY = 'period_today'
CALLBACK_PERIOD_WEEK = 'period_week'
CALLBACK_PERIOD_MONTH = 'period_month'
CALLBACK_PERIOD_YEAR = 'period_year'
CALLBACK_ANOTHER_PERIOD = 'another_period'

# Типи доходів (префікси)
CALLBACK_INCOME_TYPE_PREFIX = 'income_type_'
CALLBACK_INCOME_SALARY = 'income_type_salary'
CALLBACK_INCOME_BONUS = 'income_type_bonus'
CALLBACK_INCOME_GIFT = 'income_type_gift'
CALLBACK_INCOME_OTHER = 'income_type_other'

# Типи витрат (префікси)
CALLBACK_EXPENSE_TYPE_PREFIX = 'expense_type_'
CALLBACK_EXPENSE_FOOD = 'expense_type_food'
CALLBACK_EXPENSE_TRANSPORT = 'expense_type_transport'
CALLBACK_EXPENSE_UTILITIES = 'expense_type_utilities'
CALLBACK_EXPENSE_ENTERTAINMENT = 'expense_type_entertainment'
CALLBACK_EXPENSE_HEALTH = 'expense_type_health'
CALLBACK_EXPENSE_CLOTHING = 'expense_type_clothing'
CALLBACK_EXPENSE_OTHER = 'expense_type_other'

# Налаштування
CALLBACK_SETTINGS_LANGUAGE = 'settings_language'
CALLBACK_LANGUAGE_UK = 'lang_uk'
CALLBACK_LANGUAGE_EN = 'lang_en'

# Навігація
CALLBACK_BACK = 'back'
CALLBACK_CANCEL = 'cancel'
CALLBACK_BACK_TO_FINANCES = 'back_to_finances'
CALLBACK_BACK_TO_VIEW_EXPENSES = 'back_to_view_expenses'
CALLBACK_BACK_TO_VIEW_INCOMES = 'back_to_view_incomes'
CALLBACK_BACK_TO_VIEW_GENERAL = 'back_to_view_general'
CALLBACK_BACK_TO_ADD_INCOME = 'back_to_add_income'
CALLBACK_BACK_TO_ADD_EXPENSE = 'back_to_add_expense'
CALLBACK_BACK_TO_SETTINGS = 'back_to_settings'

# Мапінг типів доходів на callback_data
INCOME_TYPE_CALLBACKS = {
    'uk': {
        'Зарплата': CALLBACK_INCOME_SALARY,
        'Премія': CALLBACK_INCOME_BONUS,
        'Подарунок': CALLBACK_INCOME_GIFT,
        'Інші': CALLBACK_INCOME_OTHER,
    },
    'en': {
        'Salary': CALLBACK_INCOME_SALARY,
        'Bonus': CALLBACK_INCOME_BONUS,
        'Gift': CALLBACK_INCOME_GIFT,
        'Other': CALLBACK_INCOME_OTHER,
    }
}

# Мапінг типів витрат на callback_data
EXPENSE_TYPE_CALLBACKS = {
    'uk': {
        'Їжа': CALLBACK_EXPENSE_FOOD,
        'Транспорт': CALLBACK_EXPENSE_TRANSPORT,
        'Комунальні послуги': CALLBACK_EXPENSE_UTILITIES,
        'Розваги': CALLBACK_EXPENSE_ENTERTAINMENT,
        'Здоров\'я': CALLBACK_EXPENSE_HEALTH,
        'Одяг': CALLBACK_EXPENSE_CLOTHING,
        'Інші': CALLBACK_EXPENSE_OTHER,
    },
    'en': {
        'Food': CALLBACK_EXPENSE_FOOD,
        'Transport': CALLBACK_EXPENSE_TRANSPORT,
        'Utilities': CALLBACK_EXPENSE_UTILITIES,
        'Entertainment': CALLBACK_EXPENSE_ENTERTAINMENT,
        'Health': CALLBACK_EXPENSE_HEALTH,
        'Clothing': CALLBACK_EXPENSE_CLOTHING,
        'Other': CALLBACK_EXPENSE_OTHER,
    }
}

# Зворотний мапінг callback_data на типи
CALLBACK_TO_INCOME_TYPE = {
    'uk': {v: k for k, v in INCOME_TYPE_CALLBACKS['uk'].items()},
    'en': {v: k for k, v in INCOME_TYPE_CALLBACKS['en'].items()},
}

CALLBACK_TO_EXPENSE_TYPE = {
    'uk': {v: k for k, v in EXPENSE_TYPE_CALLBACKS['uk'].items()},
    'en': {v: k for k, v in EXPENSE_TYPE_CALLBACKS['en'].items()},
}

# Мапінг періодів
PERIOD_CALLBACKS = {
    'today': CALLBACK_PERIOD_TODAY,
    'week': CALLBACK_PERIOD_WEEK,
    'month': CALLBACK_PERIOD_MONTH,
    'year': CALLBACK_PERIOD_YEAR,
}

CALLBACK_TO_PERIOD = {v: k for k, v in PERIOD_CALLBACKS.items()}
