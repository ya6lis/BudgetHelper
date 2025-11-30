# -*- coding: utf-8 -*-
"""
Форматери для відображення даних користувачу.
Працюють з моделями Income та Expense.
"""

from typing import Dict, List
from locales import get_text, translate_category_name
from models import Income, Expense


def format_income_list(data: dict, period_name: str, user_id: int = None) -> str:
    """
    Форматує список доходів для відображення.
    
    Args:
        data: Словник з агрегованими доходами
        period_name: Назва періоду для відображення
        user_id: ID користувача для локалізації
    
    Returns:
        str: Відформатований текст
    """
    from utils.currency_converter import get_currency_symbol, convert_currency
    
    msg = get_text('view_incomes_title', user_id=user_id).format(period_name)
    
    aggregated_by_category_currency = data.get('aggregated_by_category_currency', {})
    total = data.get('total', 0.0)
    currency = data.get('currency', 'UAH')
    currency_symbol = get_currency_symbol(currency)
    by_currency = data.get('by_currency', {})
    
    # Показуємо категорії з оригінальними валютами
    for category_name, currencies in aggregated_by_category_currency.items():
        category_display = translate_category_name(category_name, user_id=user_id)
        
        # Якщо є кілька валют або валюта не дефолтна, показуємо кожну окремо
        if len(currencies) > 1 or currency not in currencies:
            msg += f"\n💰 {category_display}:\n"
            for curr, amount in sorted(currencies.items()):
                curr_symbol = get_currency_symbol(curr)
                if curr != currency:
                    converted = convert_currency(amount, curr, currency)
                    msg += f"  • {amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {currency_symbol})</i>\n"
                else:
                    msg += f"  • {amount:.2f} {curr_symbol}\n"
        else:
            # Одна валюта (дефолтна) - старий стиль
            curr = list(currencies.keys())[0]
            amount = currencies[curr]
            curr_symbol = get_currency_symbol(curr)
            msg += f"• {category_display}: {amount:.2f} {curr_symbol}\n"
    
    # Якщо є кілька валют АБО валюта відрізняється від дефолтної, показуємо що це приблизна сума після конвертації
    has_single_non_default_currency = (len(by_currency) == 1 and currency not in by_currency)
    
    if len(by_currency) > 1 or has_single_non_default_currency:
        msg += "\n" + get_text('approximate_income_after_conversion', user_id=user_id).format(f"{total:.2f}", currency_symbol)
    else:
        msg += get_text('view_incomes_total', user_id=user_id).format(f"{total:.2f} {currency_symbol}")
    
    return msg


def format_expense_list(data: dict, period_name: str, user_id: int = None) -> str:
    """
    Форматує список витрат для відображення.
    
    Args:
        data: Словник з агрегованими витратами
        period_name: Назва періоду для відображення
        user_id: ID користувача для локалізації
    
    Returns:
        str: Відформатований текст
    """
    from utils.currency_converter import get_currency_symbol, convert_currency
    
    msg = get_text('view_expenses_title', user_id=user_id).format(period_name)
    
    aggregated_by_category_currency = data.get('aggregated_by_category_currency', {})
    total = data.get('total', 0.0)
    currency = data.get('currency', 'UAH')
    currency_symbol = get_currency_symbol(currency)
    by_currency = data.get('by_currency', {})
    
    # Показуємо категорії з оригінальними валютами
    for category_name, currencies in aggregated_by_category_currency.items():
        category_display = translate_category_name(category_name, user_id=user_id)
        
        # Якщо є кілька валют або валюта не дефолтна, показуємо кожну окремо
        if len(currencies) > 1 or currency not in currencies:
            msg += f"\n💸 {category_display}:\n"
            for curr, amount in sorted(currencies.items()):
                curr_symbol = get_currency_symbol(curr)
                if curr != currency:
                    converted = convert_currency(amount, curr, currency)
                    msg += f"  • {amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {currency_symbol})</i>\n"
                else:
                    msg += f"  • {amount:.2f} {curr_symbol}\n"
        else:
            # Одна валюта (дефолтна) - старий стиль
            curr = list(currencies.keys())[0]
            amount = currencies[curr]
            curr_symbol = get_currency_symbol(curr)
            msg += f"• {category_display}: {amount:.2f} {curr_symbol}\n"
    
    # Якщо є кілька валют АБО валюта відрізняється від дефолтної, показуємо що це приблизна сума після конвертації
    has_single_non_default_currency = (len(by_currency) == 1 and currency not in by_currency)
    
    if len(by_currency) > 1 or has_single_non_default_currency:
        msg += "\n" + get_text('approximate_expense_after_conversion', user_id=user_id).format(f"{total:.2f}", currency_symbol)
    else:
        msg += get_text('view_expenses_total', user_id=user_id).format(f"{total:.2f} {currency_symbol}")
    
    return msg


def format_amount(amount: float, currency: str = 'UAH') -> str:
    """
    Форматує суму з валютою.
    
    Args:
        amount: Сума
        currency: Валюта (за замовчуванням UAH)
    
    Returns:
        str: Відформатована сума
    """
    return f"{amount:.2f} {currency}"


def calculate_balance(incomes: float, expenses: float) -> float:
    """
    Обчислює баланс (доходи - витрати).
    
    Args:
        incomes: Сума доходів
        expenses: Сума витрат
    
    Returns:
        float: Баланс
    """
    return incomes - expenses


def format_income_model(income: Income) -> str:
    """
    Форматує модель Income для відображення.
    
    Args:
        income: Об'єкт Income
    
    Returns:
        str: Відформатований текст
    """
    return (f"💰 {income.description}: {income.amount:.2f} {income.currency}\n"
            f"📅 {income.add_date}")


def format_expense_model(expense: Expense) -> str:
    """
    Форматує модель Expense для відображення.
    
    Args:
        expense: Об'єкт Expense
    
    Returns:
        str: Відформатований текст
    """
    return (f"💸 {expense.description}: {expense.amount:.2f} {expense.currency}\n"
            f"📅 {expense.add_date}")


def _format_currency_amounts(by_currency: dict) -> str:
    """Форматує суми по валютах у вигляді 'amount ₴ + amount $'"""
    from utils.currency_converter import get_currency_symbol
    
    if not by_currency:
        return ""
    
    parts = [f"{amount:.2f} {get_currency_symbol(curr)}" for curr, amount in by_currency.items()]
    return " + ".join(parts)


def _calculate_balance_with_conversion(income_by_currency: dict, expense_by_currency: dict, user_currency: str) -> tuple:
    """
    Розраховує баланс по кожній валюті та загальний конвертований баланс.
    
    Returns:
        tuple: (balance_text, total_balance_converted)
    """
    from utils.currency_converter import get_currency_symbol, convert_currency
    
    all_currencies = set(list(income_by_currency.keys()) + list(expense_by_currency.keys()))
    balance_parts = []
    total_balance_converted = 0.0
    
    for curr in sorted(all_currencies):
        income_in_curr = income_by_currency.get(curr, 0.0)
        expense_in_curr = expense_by_currency.get(curr, 0.0)
        balance_in_curr = income_in_curr - expense_in_curr
        
        curr_symbol = get_currency_symbol(curr)
        sign = "+" if balance_in_curr >= 0 else ""
        balance_parts.append(f"{sign}{balance_in_curr:.2f} {curr_symbol}")
        
        # Конвертуємо для орієнтовного підрахунку
        converted = convert_currency(balance_in_curr, curr, user_currency) if curr != user_currency else balance_in_curr
        total_balance_converted += converted
    
    return " ".join(balance_parts), total_balance_converted


def format_general_finances(incomes_data: dict, expenses_data: dict, period_name: str, user_id: int = None) -> str:
    """
    Форматує загальні фінанси для відображення.
    
    Args:
        incomes_data: Словник з агрегованими доходами
        expenses_data: Словник з агрегованими витратами
        period_name: Назва періоду для відображення
        user_id: ID користувача для локалізації
    
    Returns:
        str: Відформатований текст
    """
    from utils.currency_converter import get_currency_symbol, convert_currency
    
    # Розбивка по валютах (оригінальні суми)
    income_by_currency = incomes_data.get('by_currency', {})
    expense_by_currency = expenses_data.get('by_currency', {})
    
    # Валюта користувача для орієнтовного підрахунку
    user_currency = incomes_data.get('currency', 'UAH')
    user_currency_symbol = get_currency_symbol(user_currency)
    
    msg = get_text('view_general_title', user_id=user_id).format(period_name)
    
    # Перевіряємо чи є кілька валют
    all_currencies = set(list(income_by_currency.keys()) + list(expense_by_currency.keys()))
    has_multiple_currencies = len(all_currencies) > 1 or (len(all_currencies) == 1 and user_currency not in all_currencies)
    
    # Доходи
    if has_multiple_currencies and income_by_currency:
        msg += "\n" + get_text('incomes_header', user_id=user_id) + "\n"
        for curr in sorted(income_by_currency.keys()):
            amount = income_by_currency[curr]
            curr_symbol = get_currency_symbol(curr)
            if curr != user_currency:
                converted = convert_currency(amount, curr, user_currency)
                msg += f"  • {amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {user_currency_symbol})</i>\n"
            else:
                msg += f"  • {amount:.2f} {curr_symbol}\n"
    else:
        income_text = _format_currency_amounts(income_by_currency)
        if income_text:
            msg += get_text('view_general_income', user_id=user_id).format(income_text) + '\n'
        else:
            msg += get_text('view_general_income', user_id=user_id).format(f"0.00 {user_currency_symbol}") + '\n'
    
    # Витрати
    if has_multiple_currencies and expense_by_currency:
        msg += "\n" + get_text('expenses_header', user_id=user_id) + "\n"
        for curr in sorted(expense_by_currency.keys()):
            amount = expense_by_currency[curr]
            curr_symbol = get_currency_symbol(curr)
            if curr != user_currency:
                converted = convert_currency(amount, curr, user_currency)
                msg += f"  • {amount:.2f} {curr_symbol} <i>(≈ {converted:.2f} {user_currency_symbol})</i>\n"
            else:
                msg += f"  • {amount:.2f} {curr_symbol}\n"
    else:
        expense_text = _format_currency_amounts(expense_by_currency)
        if expense_text:
            msg += get_text('view_general_expense', user_id=user_id).format(expense_text) + '\n'
        else:
            msg += get_text('view_general_expense', user_id=user_id).format(f"0.00 {user_currency_symbol}") + '\n'
    
    # Баланс по кожній валюті окремо
    if all_currencies:
        balance_text, total_balance_converted = _calculate_balance_with_conversion(
            income_by_currency, expense_by_currency, user_currency
        )
        
        if has_multiple_currencies:
            # Показуємо баланс по кожній валюті окремо
            msg += "\n" + get_text('balance_header', user_id=user_id) + "\n"
            for curr in sorted(all_currencies):
                income_in_curr = income_by_currency.get(curr, 0.0)
                expense_in_curr = expense_by_currency.get(curr, 0.0)
                balance_in_curr = income_in_curr - expense_in_curr
                curr_symbol = get_currency_symbol(curr)
                sign = "+" if balance_in_curr >= 0 else ""
                
                if curr != user_currency:
                    converted = convert_currency(balance_in_curr, curr, user_currency)
                    msg += f"  • {sign}{balance_in_curr:.2f} {curr_symbol} <i>(≈ {converted:+.2f} {user_currency_symbol})</i>\n"
                else:
                    msg += f"  • {sign}{balance_in_curr:.2f} {curr_symbol}\n"
            
            # Показуємо орієнтовний баланс в дефолтній валюті
            msg += f"\n{get_text('currency_conversion_info', user_id=user_id).format(user_currency_symbol, f'{total_balance_converted:+.2f} {user_currency_symbol}')}"
        else:
            # Простий баланс для однієї валюти
            approx_text = f"\n{get_text('currency_conversion_info', user_id=user_id).format(user_currency_symbol, f'{total_balance_converted:+.2f} {user_currency_symbol}')}"
            if total_balance_converted >= 0:
                msg += "\n" + get_text('balance_positive', user_id=user_id).format(balance_text)
                if user_currency not in all_currencies:
                    msg += approx_text
            else:
                msg += "\n" + get_text('balance_negative', user_id=user_id).format(balance_text)
                if user_currency not in all_currencies:
                    msg += approx_text
        
        # Повідомлення про стан фінансів
        if total_balance_converted >= 0:
            msg += "\n\n" + get_text('finances_positive', user_id=user_id)
        else:
            msg += "\n\n" + get_text('finances_negative', user_id=user_id)
    else:
        msg += get_text('view_general_balance_zero', user_id=user_id)
    
    return msg

