# -*- coding: utf-8 -*-

from .uk import TEXTS_UK
from .en import TEXTS_EN
from config.constants import (
    INCOME_TYPES, EXPENSE_TYPES, DEFAULT_LANGUAGE,
    INCOME_CATEGORY_TRANSLATIONS, EXPENSE_CATEGORY_TRANSLATIONS
)

# Словник для зберігання мови кожного користувача
USER_LANGUAGES = {}

LANGUAGES = {
    'uk': TEXTS_UK,
    'en': TEXTS_EN,
}

TIME_FRAMES = {
    'uk': {
        'За сьогодні': 'today',
        'За тиждень': 'week',
        'За місяць': 'month',
        'За рік': 'year',
    },
    'en': {
        'Today': 'today',
        'This Week': 'week',
        'This Month': 'month',
        'This Year': 'year',
    },
}


def get_text(key, lang=None, user_id=None):
    """
    Отримати текст для ключа.
    Пріоритет: lang > user_id мова > DEFAULT_LANGUAGE
    """
    if lang:
        language = lang
    elif user_id and user_id in USER_LANGUAGES:
        language = USER_LANGUAGES[user_id]
    else:
        language = DEFAULT_LANGUAGE
    
    texts = LANGUAGES.get(language, TEXTS_UK)
    return texts.get(key, key)


def set_language(user_id, lang):
    """Встановити мову для конкретного користувача."""
    if lang in LANGUAGES:
        USER_LANGUAGES[user_id] = lang
    else:
        raise ValueError(f"Language '{lang}' is not supported")


def get_current_language(user_id=None):
    """Отримати мову користувача або мову за замовчуванням."""
    if user_id and user_id in USER_LANGUAGES:
        return USER_LANGUAGES[user_id]
    return DEFAULT_LANGUAGE


def get_available_languages():
    return list(LANGUAGES.keys())


def get_income_types(lang=None, user_id=None):
    """Отримати типи доходів для мови користувача."""
    if lang:
        language = lang
    elif user_id and user_id in USER_LANGUAGES:
        language = USER_LANGUAGES[user_id]
    else:
        language = DEFAULT_LANGUAGE
    
    return INCOME_TYPES.get(language, INCOME_TYPES['uk'])


def get_expense_types(lang=None, user_id=None):
    """Отримати типи витрат для мови користувача."""
    if lang:
        language = lang
    elif user_id and user_id in USER_LANGUAGES:
        language = USER_LANGUAGES[user_id]
    else:
        language = DEFAULT_LANGUAGE
    
    return EXPENSE_TYPES.get(language, EXPENSE_TYPES['uk'])


def get_time_frames(lang=None, user_id=None):
    """Отримати часові рамки для мови користувача."""
    if lang:
        language = lang
    elif user_id and user_id in USER_LANGUAGES:
        language = USER_LANGUAGES[user_id]
    else:
        language = DEFAULT_LANGUAGE
    
    return TIME_FRAMES.get(language, TIME_FRAMES['uk'])


def translate_income_category(category_key, lang=None, user_id=None):
    """
    Перекласти ключ категорії доходу на поточну мову.
    
    Args:
        category_key: Ключ категорії (наприклад 'salary')
        lang: Мова (опціонально)
        user_id: ID користувача (опціонально)
    
    Returns:
        str: Переклад категорії або сам ключ якщо переклад не знайдено
    """
    if lang:
        language = lang
    elif user_id and user_id in USER_LANGUAGES:
        language = USER_LANGUAGES[user_id]
    else:
        language = DEFAULT_LANGUAGE
    
    return INCOME_CATEGORY_TRANSLATIONS.get(category_key, {}).get(language, category_key)


def translate_expense_category(category_key, lang=None, user_id=None):
    """
    Перекласти ключ категорії витрати на поточну мову.
    
    Args:
        category_key: Ключ категорії (наприклад 'food')
        lang: Мова (опціонально)
        user_id: ID користувача (опціонально)
    
    Returns:
        str: Переклад категорії або сам ключ якщо переклад не знайдено
    """
    if lang:
        language = lang
    elif user_id and user_id in USER_LANGUAGES:
        language = USER_LANGUAGES[user_id]
    else:
        language = DEFAULT_LANGUAGE
    
    return EXPENSE_CATEGORY_TRANSLATIONS.get(category_key, {}).get(language, category_key)


def get_category_key_from_callback(callback_data):
    """
    Отримати ключ категорії з callback_data.
    
    Args:
        callback_data: Дані callback (наприклад 'expense_type_food')
    
    Returns:
        str: Ключ категорії (наприклад 'food') або None
    """
    if callback_data.startswith('income_type_'):
        return callback_data.replace('income_type_', '')
    elif callback_data.startswith('expense_type_'):
        return callback_data.replace('expense_type_', '')
    return None
