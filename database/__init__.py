# -*- coding: utf-8 -*-
"""
Пакет для роботи з базою даних.
Включає repositories для роботи з моделями User, Income, Expense.
"""

from .db_manager import (
    init_db,
    get_connection,
    ensure_user,
)
from .user_repository import (
    get_user,
    create_user,
    update_user_language,
    ensure_user_exists,
)
from .income_repository import (
    add_income,
    get_income_by_id,
    get_all_incomes,
    get_incomes_aggregated,
    update_income,
    delete_income,
)
from .expense_repository import (
    add_expense,
    get_expense_by_id,
    get_all_expenses,
    get_expenses_aggregated,
    update_expense,
    delete_expense,
)

__all__ = [
    # DB Manager
    'init_db',
    'get_connection',
    'ensure_user',
    
    # User Repository
    'get_user',
    'create_user',
    'update_user_language',
    'ensure_user_exists',
    
    # Income Repository
    'add_income',
    'get_income_by_id',
    'get_all_incomes',
    'get_incomes_aggregated',
    'update_income',
    'delete_income',
    
    # Expense Repository
    'add_expense',
    'get_expense_by_id',
    'get_all_expenses',
    'get_expenses_aggregated',
    'update_expense',
    'delete_expense',
]

