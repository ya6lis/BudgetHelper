# -*- coding: utf-8 -*-

import math
from locales import get_text


def validate_amount(text):
    """
    Валідація суми грошей.
    
    Перевіряє:
    - Чи можна конвертувати в число
    - Чи не є NaN, Inf, -Inf
    - Чи більше 0
    - Чи не перевищує максимальне значення
    
    Args:
        text: Текст для валідації
        
    Returns:
        tuple: (is_valid: bool, amount: float|None)
    """
    # Перевірка на порожній або невалідний вхід
    if not text or not isinstance(text, str):
        return False, None
    
    text = text.strip().lower()
    
    # Замінюємо кому на крапку для підтримки обох форматів
    text = text.replace(',', '.')
    
    # Перевірка на заборонені текстові значення
    forbidden_values = ['nan', 'inf', 'infinity', '-inf', '-infinity', '+inf', '+infinity']
    if text in forbidden_values:
        return False, None
    
    try:
        amount = float(text)
        
        # Перевірка на NaN
        if math.isnan(amount):
            return False, None
        
        # Перевірка на нескінченність
        if math.isinf(amount):
            return False, None
        
        # Перевірка на від'ємне або нульове значення
        if amount <= 0:
            return False, None
        
        # Перевірка на занадто велике значення (більше 1 трильйона)
        if amount > 1_000_000_000_000:
            return False, None
        
        # Перевірка на занадто мале значення (менше 0.001)
        if amount < 0.001:
            return False, None
        
        # Округлення до 2 знаків після коми
        amount = round(amount, 2)
        
        return True, amount
        
    except (ValueError, AttributeError, OverflowError):
        return False, None


def is_back_command(text):
    return text == get_text('menu_back')


def is_valid_text_input(text, min_length=1, max_length=500):
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    return min_length <= len(text) <= max_length
