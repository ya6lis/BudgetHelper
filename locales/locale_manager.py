# -*- coding: utf-8 -*-

from .uk import TEXTS_UK
from .en import TEXTS_EN
from config.constants import INCOME_TYPES, EXPENSE_TYPES, DEFAULT_LANGUAGE

CURRENT_LANGUAGE = DEFAULT_LANGUAGE

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


def get_text(key, lang=None):
    language = lang or CURRENT_LANGUAGE
    texts = LANGUAGES.get(language, TEXTS_UK)
    return texts.get(key, key)


def set_language(lang):
    global CURRENT_LANGUAGE
    if lang in LANGUAGES:
        CURRENT_LANGUAGE = lang
    else:
        raise ValueError(f"Language '{lang}' is not supported")


def get_available_languages():
    return list(LANGUAGES.keys())


def get_income_types(lang=None):
    language = lang or CURRENT_LANGUAGE
    return INCOME_TYPES.get(language, INCOME_TYPES['uk'])


def get_expense_types(lang=None):
    language = lang or CURRENT_LANGUAGE
    return EXPENSE_TYPES.get(language, EXPENSE_TYPES['uk'])


def get_time_frames(lang=None):
    language = lang or CURRENT_LANGUAGE
    return TIME_FRAMES.get(language, TIME_FRAMES['uk'])
