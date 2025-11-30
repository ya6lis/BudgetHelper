# -*- coding: utf-8 -*-
"""
Репозиторій для роботи з витратами в базі даних.
Використовує модель Expense для представлення даних.
"""

from datetime import datetime
from threading import Lock
from typing import List, Optional
from .db_manager import get_connection, ensure_user, generate_uuid
from .utils import get_date_range_for_period
from models import Expense
from config.constants import DEFAULT_CURRENCY
from locales import translate_category_name

_lock = Lock()


def add_expense(user_id: int, amount: float, category_id: int, description: str = None, add_date: str = None) -> Expense:
    """
    Додати нову витрату для користувача.
    
    Args:
        user_id: ID користувача Telegram
        amount: Сума витрати
        category_id: ID категорії
        description: Опис (опціонально)
        add_date: Дата додавання (опціонально, за замовчуванням - поточна)
    
    Returns:
        Expense: Створений об'єкт Expense з ID
    """
    expense = Expense(
        user_id=user_id,
        amount=amount,
        category_id=category_id,
        description=description
    )
    
    # Якщо передана дата, використовуємо її
    if add_date:
        expense.add_date = add_date
        expense.update_date = add_date
    
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            ensure_user(cursor, user_id)
            expense.id = generate_uuid()
            cursor.execute('''
                INSERT INTO expenses (id, user_id, amount, category_id, description, add_date, update_date)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (expense.id, expense.user_id, expense.amount, expense.category_id, expense.description,
                  expense.add_date, expense.update_date))
            conn.commit()
    
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
                SELECT id, user_id, amount, category_id, description, add_date, update_date
                FROM expenses WHERE id = ?
            ''', (expense_id,))
            row = cursor.fetchone()
            
            if row:
                return Expense.from_dict({
                    'id': row[0],
                    'user_id': row[1],
                    'amount': row[2],
                    'category_id': row[3],
                    'description': row[4],
                    'add_date': row[5],
                    'update_date': row[6]
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
                SELECT id, user_id, amount, category_id, description, add_date, update_date
                FROM expenses WHERE user_id = ?
                ORDER BY add_date DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            
            return [Expense.from_dict({
                'id': row[0],
                'user_id': row[1],
                'amount': row[2],
                'category_id': row[3],
                'description': row[4],
                'add_date': row[5],
                'update_date': row[6]
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
        SELECT id, user_id, amount, category_id, description, add_date, update_date
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
                'category_id': row[3],
                'description': row[4],
                'add_date': row[5],
                'update_date': row[6]
            }) for row in rows]
            
            # Отримуємо категорії для агрегування
            from database import CategoryRepository
            
            # Агрегування по категоріях
            aggregated = {}
            total = 0.0
            for expense in expenses:
                category = CategoryRepository.get_category_by_id(expense.category_id)
                category_name = category.name if category else 'Інше'
                if category_name not in aggregated:
                    aggregated[category_name] = 0.0
                aggregated[category_name] = round(aggregated[category_name] + expense.amount, 2)
                total = round(total + expense.amount, 2)
            
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
