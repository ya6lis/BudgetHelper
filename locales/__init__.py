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
)

__all__ = [
    'get_text',
    'set_language',
    'get_available_languages',
    'get_income_types',
    'get_expense_types',
    'get_time_frames',
]
