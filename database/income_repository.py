# -*- coding: utf-8 -*-
"""
Репозиторій для роботи з доходами в базі даних.
Використовує модель Income для представлення даних.
"""

from datetime import datetime
from threading import Lock
from typing import List, Optional
from .db_manager import get_connection, ensure_user
from .utils import get_date_range_for_period
from models import Income
from config.constants import DEFAULT_CURRENCY

_lock = Lock()


def add_income(user_id: int, amount: float, description: str, currency: str = DEFAULT_CURRENCY) -> Income:
    """
    Додати новий дохід для користувача.
    
    Args:
        user_id: ID користувача Telegram
        amount: Сума доходу
        description: Опис/категорія доходу
        currency: Валюта (за замовчуванням UAH)
    
    Returns:
        Income: Створений об'єкт Income з ID
    """
    income = Income(
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
                INSERT INTO incomes (user_id, amount, description, currency, add_date, update_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (income.user_id, income.amount, income.description, 
                  income.currency, income.add_date, income.update_date))
            conn.commit()
            income.id = cursor.lastrowid
    
    return income


def get_income_by_id(income_id: int) -> Optional[Income]:
    """
    Отримати дохід за ID.
    
    Args:
        income_id: ID доходу
    
    Returns:
        Income або None
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, user_id, amount, description, currency, add_date, update_date
                FROM incomes WHERE id = ?
            ''', (income_id,))
            row = cursor.fetchone()
            
            if row:
                return Income.from_dict({
                    'id': row[0],
                    'user_id': row[1],
                    'amount': row[2],
                    'description': row[3],
                    'currency': row[4],
                    'add_date': row[5],
                    'update_date': row[6]
                })
            return None


def get_all_incomes(user_id: int) -> List[Income]:
    """
    Отримати всі доходи користувача.
    
    Args:
        user_id: ID користувача
    
    Returns:
        List[Income]: Список об'єктів Income
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, user_id, amount, description, currency, add_date, update_date
                FROM incomes WHERE user_id = ?
                ORDER BY add_date DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            
            return [Income.from_dict({
                'id': row[0],
                'user_id': row[1],
                'amount': row[2],
                'description': row[3],
                'currency': row[4],
                'add_date': row[5],
                'update_date': row[6]
            }) for row in rows]


def get_incomes_aggregated(user_id: int, period: str) -> dict:
    """
    Отримати агреговані доходи за період.
    
    Args:
        user_id: ID користувача
        period: Період ('today', 'week', 'month', 'year')
    
    Returns:
        dict: Словник з агрегованими даними та списком Income
    """
    start, end = get_date_range_for_period(period)
    
    # Використовуємо однаковий запит для всіх періодів
    query = '''
        SELECT id, user_id, amount, description, currency, add_date, update_date
        FROM incomes
        WHERE user_id = ? AND add_date BETWEEN ? AND ?
        ORDER BY add_date DESC
    '''
    params = (user_id, start.strftime('%Y-%m-%d %H:%M:%S'), end.strftime('%Y-%m-%d %H:%M:%S'))

    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            incomes = [Income.from_dict({
                'id': row[0],
                'user_id': row[1],
                'amount': row[2],
                'description': row[3],
                'currency': row[4],
                'add_date': row[5],
                'update_date': row[6]
            }) for row in rows]
            
            # Агрегування по категоріях
            aggregated = {}
            total = 0.0
            for income in incomes:
                if income.description not in aggregated:
                    aggregated[income.description] = 0.0
                aggregated[income.description] += income.amount
                total += income.amount
            
            return {
                'incomes': incomes,
                'aggregated': aggregated,
                'total': total
            }


def update_income(income: Income) -> bool:
    """
    Оновити існуючий дохід.
    
    Args:
        income: Об'єкт Income з оновленими даними
    
    Returns:
        bool: True якщо успішно оновлено
    """
    income.update()
    
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE incomes
                SET amount = ?, description = ?, currency = ?, update_date = ?
                WHERE id = ?
            ''', (income.amount, income.description, income.currency, 
                  income.update_date, income.id))
            conn.commit()
            return cursor.rowcount > 0


def delete_income(income_id: int) -> bool:
    """
    Видалити дохід за ID.
    
    Args:
        income_id: ID доходу
    
    Returns:
        bool: True якщо успішно видалено
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM incomes WHERE id = ?', (income_id,))
            conn.commit()
            return cursor.rowcount > 0
