# -*- coding: utf-8 -*-

# Ключі категорій (мовно-незалежні)
INCOME_CATEGORY_KEYS = ['salary', 'bonus', 'gift', 'other']
EXPENSE_CATEGORY_KEYS = ['food', 'transport', 'utilities', 'entertainment', 'health', 'clothing', 'other']

# Переклади категорій доходів
INCOME_TYPES = {
    'uk': ['Зарплата', 'Премія', 'Подарунок', 'Інші'],
    'en': ['Salary', 'Bonus', 'Gift', 'Other'],
}

# Переклади категорій витрат
EXPENSE_TYPES = {
    'uk': ['Їжа', 'Транспорт', 'Комунальні послуги', 'Розваги', 'Здоров\'я', 'Одяг', 'Інші'],
    'en': ['Food', 'Transport', 'Utilities', 'Entertainment', 'Health', 'Clothing', 'Other'],
}

# Мапінг ключів на переклади
INCOME_CATEGORY_TRANSLATIONS = {
    'salary': {'uk': 'Зарплата', 'en': 'Salary'},
    'bonus': {'uk': 'Премія', 'en': 'Bonus'},
    'gift': {'uk': 'Подарунок', 'en': 'Gift'},
    'other': {'uk': 'Інші', 'en': 'Other'},
}

EXPENSE_CATEGORY_TRANSLATIONS = {
    'food': {'uk': 'Їжа', 'en': 'Food'},
    'transport': {'uk': 'Транспорт', 'en': 'Transport'},
    'utilities': {'uk': 'Комунальні послуги', 'en': 'Utilities'},
    'entertainment': {'uk': 'Розваги', 'en': 'Entertainment'},
    'health': {'uk': 'Здоров\'я', 'en': 'Health'},
    'clothing': {'uk': 'Одяг', 'en': 'Clothing'},
    'other': {'uk': 'Інші', 'en': 'Other'},
}

TIME_PERIODS = {
    'today': 'За сьогодні',
    'week': 'За тиждень',
    'month': 'За місяць',
    'year': 'За рік',
}

# Доступні валюти
AVAILABLE_CURRENCIES = ['UAH', 'USD', 'EUR']
DEFAULT_CURRENCY = 'UAH'
DB_FILE = 'budget_helper.db'
DEFAULT_LANGUAGE = 'uk'
AVAILABLE_LANGUAGES = ['uk', 'en']
