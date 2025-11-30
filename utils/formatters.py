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
    msg = get_text('view_incomes_title', user_id=user_id).format(period_name)
    
    aggregated = data.get('aggregated', {})
    total = data.get('total', 0.0)
    
    for category_name, amount in aggregated.items():
        # Перекладаємо назву категорії з БД
        category_display = translate_category_name(category_name, user_id=user_id)
        msg += f"— {category_display} : {amount:.2f} UAH\n"
    
    msg += get_text('view_incomes_total', user_id=user_id).format(total)
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
    msg = get_text('view_expenses_title', user_id=user_id).format(period_name)
    
    aggregated = data.get('aggregated', {})
    total = data.get('total', 0.0)
    
    for category_name, amount in aggregated.items():
        # Перекладаємо назву категорії з БД
        category_display = translate_category_name(category_name, user_id=user_id)
        msg += f"— {category_display} : {amount:.2f} UAH\n"
    
    msg += get_text('view_expenses_total', user_id=user_id).format(total)
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
    total_income = incomes_data.get('total', 0.0)
    total_expense = expenses_data.get('total', 0.0)
    balance = calculate_balance(total_income, total_expense)
    
    msg = get_text('view_general_title', user_id=user_id).format(period_name)
    msg += get_text('view_general_income', user_id=user_id).format(total_income) + '\n'
    msg += get_text('view_general_expense', user_id=user_id).format(total_expense)
    
    if balance > 0:
        msg += get_text('view_general_balance_positive', user_id=user_id).format(balance)
    elif balance < 0:
        msg += get_text('view_general_balance_negative', user_id=user_id).format(balance)
    else:
        msg += get_text('view_general_balance_zero', user_id=user_id)
    
    return msg

