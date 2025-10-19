# -*- coding: utf-8 -*-

INCOME_TYPES = {
    'uk': ['Зарплата', 'Премія', 'Подарунок', 'Інші'],
    'en': ['Salary', 'Bonus', 'Gift', 'Other'],
}

EXPENSE_TYPES = {
    'uk': ['Їжа', 'Транспорт', 'Комунальні послуги', 'Розваги', 'Здоров\'я', 'Одяг', 'Інші'],
    'en': ['Food', 'Transport', 'Utilities', 'Entertainment', 'Health', 'Clothing', 'Other'],
}

TIME_PERIODS = {
    'today': 'За сьогодні',
    'week': 'За тиждень',
    'month': 'За місяць',
    'year': 'За рік',
}

DEFAULT_CURRENCY = 'UAH'
DB_FILE = 'budget_helper.db'
DEFAULT_LANGUAGE = 'uk'
AVAILABLE_LANGUAGES = ['uk', 'en']
