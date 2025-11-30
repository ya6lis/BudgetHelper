# -*- coding: utf-8 -*-
"""
Пакет для локалізації (перекладів).
"""

from .locale_manager import (
    get_text,
    set_language,
    get_available_languages,
    get_income_types,
    get_expense_types,
    get_time_frames,
    get_current_language,
    translate_income_category,
    translate_expense_category,
    translate_category_name,
    get_period_name,
    get_category_key_from_callback,
)

__all__ = [
    'get_text',
    'set_language',
    'get_available_languages',
    'get_income_types',
    'get_expense_types',
    'get_time_frames',
    'get_current_language',
    'translate_income_category',
    'translate_expense_category',
    'translate_category_name',
    'get_period_name',
    'get_category_key_from_callback',
]
