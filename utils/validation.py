# -*- coding: utf-8 -*-

from locales import get_text


def validate_amount(text):
    try:
        amount = float(text.strip())
        if amount <= 0:
            return False, None
        return True, amount
    except (ValueError, AttributeError):
        return False, None


def is_back_command(text):
    return text == get_text('menu_back')


def is_valid_text_input(text, min_length=1, max_length=500):
    if not text or not isinstance(text, str):
        return False
    
    text = text.strip()
    return min_length <= len(text) <= max_length
