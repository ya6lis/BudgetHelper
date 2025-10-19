# -*- coding: utf-8 -*-
"""
Репозиторій для роботи з витратами в базі даних.
"""

from datetime import datetime, timezone
from threading import Lock
from .db_manager import get_connection, ensure_user
from .utils import get_date_range_for_period

_lock = Lock()


def add_expense(user_id, amount, description):
    """
    Додати витрату для користувача.
    
    Args:
        user_id (int): ID користувача Telegram
        amount (float): Сума витрати
        description (str): Опис витрати
    """
    now = datetime.now(timezone.utc).isoformat()
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            ensure_user(cursor, user_id)
            cursor.execute('''
                INSERT INTO expenses (user_id, amount, description, add_date, update_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, amount, description, now, now))
            conn.commit()


def get_expenses_aggregated(user_id, period):
    """
    Отримати агреговані витрати за період.
    
    Args:
        user_id (int): ID користувача
        period (str): Період ('today', 'week', 'month', 'year')
    
    Returns:
        list: Список словників з витратами
    """
    start, end = get_date_range_for_period(period)
    
    if period == 'today':
        query = '''
            SELECT amount, description FROM expenses
            WHERE user_id = ? AND date(add_date) = date('now')
        '''
        params = (user_id,)
        aggregate = False
    else:
        query = '''
            SELECT description, SUM(amount) as total_amount FROM expenses
            WHERE user_id = ? AND add_date BETWEEN ? AND ?
            GROUP BY description
        '''
        params = (user_id, start.isoformat(), end.isoformat())
        aggregate = True

    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            if aggregate:
                return [{"description": row[0], "total_amount": row[1]} for row in rows]
            else:
                return [{"amount": row[0], "description": row[1]} for row in rows]
