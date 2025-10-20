# -*- coding: utf-8 -*-

from datetime import datetime, timedelta


def get_date_range_for_period(period):
    now = datetime.now()  # Використовуємо локальний час, як в моделях
    
    if period == 'today':
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == 'week':
        start = (now - timedelta(days=now.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end = now
    elif period == 'month':
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    elif period == 'year':
        start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now
    else:
        start = None
        end = None
    
    return start, end
