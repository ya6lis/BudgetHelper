# -*- coding: utf-8 -*-

from datetime import datetime, timezone
from threading import Lock
from .db_manager import get_connection, ensure_user
from .utils import get_date_range_for_period
from config.constants import DEFAULT_CURRENCY

_lock = Lock()


def add_income(user_id, amount, description, currency=DEFAULT_CURRENCY):
    now = datetime.now(timezone.utc).isoformat()
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            ensure_user(cursor, user_id)
            cursor.execute('''
                INSERT INTO incomes (user_id, amount, description, currency, add_date, update_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, amount, description, currency, now, now))
            conn.commit()


def get_incomes_aggregated(user_id, period):
    start, end = get_date_range_for_period(period)
    
    if period == 'today':
        query = '''
            SELECT amount, description FROM incomes
            WHERE user_id = ? AND date(add_date) = date('now')
        '''
        params = (user_id,)
        aggregate = False
    else:
        query = '''
            SELECT description, SUM(amount) as total_amount FROM incomes
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
