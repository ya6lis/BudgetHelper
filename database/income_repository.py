# -*- coding: utf-8 -*-
"""
Репозиторій для роботи з доходами в базі даних.
Використовує модель Income для представлення даних.
"""

from datetime import datetime
from threading import Lock
from typing import List, Optional
from .db_manager import get_connection, ensure_user, generate_uuid
from .utils import get_date_range_for_period
from models import Income
from config.constants import DEFAULT_CURRENCY
from locales import translate_category_name

_lock = Lock()


def add_income(user_id: int, amount: float, category_id: int, description: str = None, currency: str = DEFAULT_CURRENCY, add_date: str = None) -> Income:
    """
    Додати новий дохід для користувача.
    
    Args:
        user_id: ID користувача Telegram
        amount: Сума доходу
        category_id: ID категорії
        description: Опис (опціонально)
        currency: Валюта (за замовчуванням UAH)
        add_date: Дата додавання (опціонально, за замовчуванням - поточна)
    
    Returns:
        Income: Створений об'єкт Income з ID
    """
    income = Income(
        user_id=user_id,
        amount=amount,
        category_id=category_id,
        description=description,
        currency=currency
    )
    
    # Якщо передана дата, використовуємо її
    if add_date:
        income.add_date = add_date
        income.update_date = add_date
    
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            ensure_user(cursor, user_id)
            income.id = generate_uuid()
            cursor.execute('''
                INSERT INTO incomes (id, user_id, amount, category_id, description, currency, add_date, update_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (income.id, income.user_id, income.amount, income.category_id, income.description,
                  income.currency, income.add_date, income.update_date))
            conn.commit()
    
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
                SELECT id, user_id, amount, category_id, description, currency, add_date, update_date
                FROM incomes WHERE id = ?
            ''', (income_id,))
            row = cursor.fetchone()
            
            if row:
                return Income.from_dict({
                    'id': row[0],
                    'user_id': row[1],
                    'amount': row[2],
                    'category_id': row[3],
                    'description': row[4],
                    'currency': row[5],
                    'add_date': row[6],
                    'update_date': row[7]
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
                SELECT id, user_id, amount, category_id, description, currency, add_date, update_date
                FROM incomes WHERE user_id = ?
                ORDER BY add_date DESC
            ''', (user_id,))
            rows = cursor.fetchall()
            
            return [Income.from_dict({
                'id': row[0],
                'user_id': row[1],
                'amount': row[2],
                'category_id': row[3],
                'description': row[4],
                'currency': row[5],
                'add_date': row[6],
                'update_date': row[7]
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
        SELECT id, user_id, amount, category_id, description, currency, add_date, update_date
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
                'category_id': row[3],
                'description': row[4],
                'currency': row[5],
                'add_date': row[6],
                'update_date': row[7]
            }) for row in rows]
            
            # Отримуємо категорії для агрегування
            from database import CategoryRepository
            
            # Агрегування по категоріях
            aggregated = {}
            total = 0.0
            for income in incomes:
                category = CategoryRepository.get_category_by_id(income.category_id)
                category_name = category.name if category else 'Інше'
                # Не перекладаємо назви в aggregated - переклад буде в formatters
                # Зберігаємо оригінальні назви з БД
                if category_name not in aggregated:
                    aggregated[category_name] = 0.0
                aggregated[category_name] = round(aggregated[category_name] + income.amount, 2)
                total = round(total + income.amount, 2)
            
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
