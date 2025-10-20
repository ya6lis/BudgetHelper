# -*- coding: utf-8 -*-
"""
Репозиторій для роботи з витратами в базі даних.
Використовує модель Expense для представлення даних.
"""

from datetime import datetime
from threading import Lock
from typing import List, Optional
from .db_manager import get_connection, ensure_user
from .utils import get_date_range_for_period
from models import Expense
from config.constants import DEFAULT_CURRENCY

_lock = Lock()


def add_expense(user_id: int, amount: float, description: str, currency: str = DEFAULT_CURRENCY) -> Expense:
    """
    Додати нову витрату для користувача.
    
    Args:
        user_id: ID користувача Telegram
        amount: Сума витрати
        description: Опис/категорія витрати
        currency: Валюта (за замовчуванням UAH)
    
    Returns:
        Expense: Створений об'єкт Expense з ID
    """
    expense = Expense(
        user_id=user_id,
        amount=amount,
        description=description,
        currency=currency
    )
    
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            ensure_user(cursor, user_id)
            cursor.execute('''
                INSERT INTO expenses (user_id, amount, description, add_date, update_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (expense.user_id, expense.amount, expense.description,
                  expense.add_date, expense.update_date))
            conn.commit()
            expense.id = cursor.lastrowid
    
    return expense


def get_expense_by_id(expense_id: int) -> Optional[Expense]:
    """
    Отримати витрату за ID.
    
    Args:
        expense_id: ID витрати
    
    Returns:
        Expense або None
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, user_id, amount, description, add_date, update_date
                FROM expenses WHERE id = ?
            ''', (expense_id,))
            row = cursor.fetchone()
            
            if row:
                return Expense.from_dict({
                    'id': row[0],
                    'user_id': row[1],
                    'amount': row[2],
                    'description': row[3],
                    'currency': DEFAULT_CURRENCY,
                    'add_date': row[4],
                    'update_date': row[5]
                })
            return None


def get_all_expenses(user_id: int) -> List[Expense]:
    """
    Отримати всі витрати користувача.
    
    Args:
        user_id: ID користувача
    
    Returns:
        List[Expense]: Список об'єктів Expense
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, user_id, amount, description, add_date, update_date
                FROM expenses WHERE user_id = ?
                ORDER BY add_date DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            
            return [Expense.from_dict({
                'id': row[0],
                'user_id': row[1],
                'amount': row[2],
                'description': row[3],
                'currency': DEFAULT_CURRENCY,
                'add_date': row[4],
                'update_date': row[5]
            }) for row in rows]


def get_expenses_aggregated(user_id: int, period: str) -> dict:
    """
    Отримати агреговані витрати за період.
    
    Args:
        user_id: ID користувача
        period: Період ('today', 'week', 'month', 'year')
    
    Returns:
        dict: Словник з агрегованими даними та списком Expense
    """
    start, end = get_date_range_for_period(period)
    
    # Використовуємо однаковий запит для всіх періодів
    query = '''
        SELECT id, user_id, amount, description, add_date, update_date
        FROM expenses
        WHERE user_id = ? AND add_date BETWEEN ? AND ?
        ORDER BY add_date DESC
    '''
    params = (user_id, start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'))

    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            expenses = [Expense.from_dict({
                'id': row[0],
                'user_id': row[1],
                'amount': row[2],
                'description': row[3],
                'currency': DEFAULT_CURRENCY,
                'add_date': row[4],
                'update_date': row[5]
            }) for row in rows]
            
            # Агрегування по категоріях
            aggregated = {}
            total = 0.0
            for expense in expenses:
                if expense.description not in aggregated:
                    aggregated[expense.description] = 0.0
                aggregated[expense.description] += expense.amount
                total += expense.amount
            
            return {
                'expenses': expenses,
                'aggregated': aggregated,
                'total': total
            }


def update_expense(expense: Expense) -> bool:
    """
    Оновити існуючу витрату.
    
    Args:
        expense: Об'єкт Expense з оновленими даними
    
    Returns:
        bool: True якщо успішно оновлено
    """
    expense.update()
    
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE expenses
                SET amount = ?, description = ?, update_date = ?
                WHERE id = ?
            ''', (expense.amount, expense.description, expense.update_date, expense.id))
            conn.commit()
            return cursor.rowcount > 0


def delete_expense(expense_id: int) -> bool:
    """
    Видалити витрату за ID.
    
    Args:
        expense_id: ID витрати
    
    Returns:
        bool: True якщо успішно видалено
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
            conn.commit()
            return cursor.rowcount > 0
