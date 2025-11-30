# -*- coding: utf-8 -*-
"""
Пакет для роботи з базою даних.
Включає repositories для роботи з моделями User, Income, Expense.
"""

from .db_manager import (
    init_db,
    get_connection,
    ensure_user,
    save_bot_message,
    get_user_bot_messages,
    clear_user_bot_messages,
    delete_bot_message,
)
from .user_repository import (
    get_user,
    create_user,
    update_user_language,
    update_user_currency,
    get_user_language,
    ensure_user_exists,
    get_all_user_ids,
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
from .report_repository import (
    generate_user_report,
    compare_with_previous_period,
)
from .category_repository import CategoryRepository

__all__ = [
    # DB Manager
    'init_db',
    'get_connection',
    'ensure_user',
    'save_bot_message',
    'get_user_bot_messages',
    'clear_user_bot_messages',
    'delete_bot_message',
    
    # User Repository
    'get_user',
    'create_user',
    'update_user_language',
    'update_user_currency',
    'get_user_language',
    'ensure_user_exists',
    'get_all_user_ids',
    
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
    
    # Report Repository
    'generate_user_report',
    'compare_with_previous_period',
    
    # Category Repository
    'CategoryRepository',
]

