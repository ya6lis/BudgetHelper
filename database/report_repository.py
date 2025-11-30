# -*- coding: utf-8 -*-
"""
Report repository - агрегація даних для звітів та аналізу бюджету.
"""

from datetime import datetime, timedelta
from threading import Lock
from typing import Dict, Optional
from .db_manager import get_connection
from .utils import get_date_range_for_period
from .income_repository import get_incomes_aggregated
from .expense_repository import get_expenses_aggregated
from models import ReportData, PeriodComparison, Income, Expense
from locales import get_period_name

_lock = Lock()


def generate_user_report(
    user_id: int,
    period: str = 'month',
    include_comparison: bool = False
) -> ReportData:
    """
    Генерує повний звіт для користувача за вказаний період.
    
    Args:
        user_id: ID користувача
        period: Період ('today', 'week', 'month', 'year')
        include_comparison: Чи включати порівняння з попереднім періодом
    
    Returns:
        ReportData: Повний звіт з усіма даними
    """
    # Отримуємо діапазон дат
    start, end = get_date_range_for_period(period)
    
    # Отримуємо агреговані дані
    incomes_data = get_incomes_aggregated(user_id, period)
    expenses_data = get_expenses_aggregated(user_id, period)
    
    # Списки транзакцій
    incomes = incomes_data.get('incomes', [])
    expenses = expenses_data.get('expenses', [])
    
    # Загальні суми
    total_income = round(incomes_data.get('total', 0.0), 2)
    total_expense = round(expenses_data.get('total', 0.0), 2)
    net_balance = round(total_income - total_expense, 2)
    
    # Категорії
    income_by_category = incomes_data.get('aggregated', {})
    expense_by_category = expenses_data.get('aggregated', {})
    
    # Статистика
    income_count = len(incomes)
    expense_count = len(expenses)
    transaction_count = income_count + expense_count
    
    avg_income = round(total_income / income_count, 2) if income_count > 0 else 0.0
    avg_expense = round(total_expense / expense_count, 2) if expense_count > 0 else 0.0
    
    # Отримуємо перекладену назву періоду
    period_name = get_period_name(period, user_id=user_id)
    
    # Створюємо об'єкт звіту
    report = ReportData(
        user_id=user_id,
        period_name=period_name,
        start_date=start.strftime('%d.%m.%Y'),
        end_date=end.strftime('%d.%m.%Y'),
        incomes=incomes,
        expenses=expenses,
        total_income=total_income,
        total_expense=total_expense,
        net_balance=net_balance,
        income_by_category=income_by_category,
        expense_by_category=expense_by_category,
        avg_income=avg_income,
        avg_expense=avg_expense,
        income_count=income_count,
        expense_count=expense_count,
        transaction_count=transaction_count,
    )
    
    # Додаємо порівняння з попереднім періодом (опціонально)
    if include_comparison and transaction_count > 0:
        report.previous_period = compare_with_previous_period(
            user_id, start, end, total_income, total_expense, net_balance
        )
    
    return report


def compare_with_previous_period(
    user_id: int,
    current_start: datetime,
    current_end: datetime,
    current_income: float,
    current_expense: float,
    current_balance: float
) -> Optional[PeriodComparison]:
    """
    Порівнює поточний період з попереднім.
    
    Args:
        user_id: ID користувача
        current_start: Початок поточного періоду
        current_end: Кінець поточного періоду
        current_income: Поточний дохід
        current_expense: Поточні витрати
        current_balance: Поточний баланс
    
    Returns:
        PeriodComparison або None якщо попередніх даних немає
    """
    # Обчислюємо попередній період
    period_length = current_end - current_start
    prev_end = current_start - timedelta(seconds=1)
    prev_start = prev_end - period_length
    
    # Отримуємо дані попереднього періоду
    prev_incomes = _get_period_totals(user_id, prev_start, prev_end, 'incomes')
    prev_expenses = _get_period_totals(user_id, prev_start, prev_end, 'expenses')
    prev_balance = prev_incomes - prev_expenses
    
    # Якщо попередній період порожній, не повертаємо порівняння
    if prev_incomes == 0 and prev_expenses == 0:
        return None
    
    # Обчислюємо зміни
    income_change = round(current_income - prev_incomes, 2)
    income_change_percent = round((income_change / prev_incomes * 100) if prev_incomes > 0 else 0.0, 2)
    
    expense_change = round(current_expense - prev_expenses, 2)
    expense_change_percent = round((expense_change / prev_expenses * 100) if prev_expenses > 0 else 0.0, 2)
    
    balance_change = round(current_balance - prev_balance, 2)
    balance_change_percent = round((balance_change / abs(prev_balance) * 100) if prev_balance != 0 else 0.0, 2)
    
    return PeriodComparison(
        prev_total_income=prev_incomes,
        prev_total_expense=prev_expenses,
        prev_net_balance=prev_balance,
        income_change=income_change,
        income_change_percent=income_change_percent,
        expense_change=expense_change,
        expense_change_percent=expense_change_percent,
        balance_change=balance_change,
        balance_change_percent=balance_change_percent,
    )


def _get_period_totals(
    user_id: int,
    start: datetime,
    end: datetime,
    table: str
) -> float:
    """
    Отримує загальну суму для періоду з вказаної таблиці.
    
    Args:
        user_id: ID користувача
        start: Початок періоду
        end: Кінець періоду
        table: Назва таблиці ('incomes' або 'expenses')
    
    Returns:
        float: Загальна сума
    """
    query = f'''
        SELECT COALESCE(SUM(amount), 0.0)
        FROM {table}
        WHERE user_id = ? AND add_date BETWEEN ? AND ?
    '''
    
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                query,
                (user_id, start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'))
            )
            result = cursor.fetchone()
            return result[0] if result else 0.0
