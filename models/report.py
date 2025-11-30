# -*- coding: utf-8 -*-
"""
Report models для представлення даних звітів та аналізу бюджету.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from .income import Income
from .expense import Expense


@dataclass
class ReportData:
    """
    Основна модель даних звіту.
    
    Attributes:
        user_id: ID користувача
        period_name: Назва періоду (За місяць, За тиждень, тощо)
        start_date: Початок періоду
        end_date: Кінець періоду
        incomes: Список об'єктів Income
        expenses: Список об'єктів Expense
        total_income: Загальна сума доходів
        total_expense: Загальна сума витрат
        net_balance: Чистий баланс (доходи - витрати)
        income_by_category: Доходи згруповані по категоріях
        expense_by_category: Витрати згруповані по категоріях
        avg_income: Середній дохід
        avg_expense: Середня витрата
        income_count: Кількість записів доходів
        expense_count: Кількість записів витрат
        transaction_count: Загальна кількість транзакцій
        previous_period: Порівняння з попереднім періодом (опціонально)
    """
    user_id: int
    period_name: str
    start_date: str
    end_date: str
    
    incomes: List[Income]
    expenses: List[Expense]
    
    total_income: float
    total_expense: float
    net_balance: float
    
    income_by_category: Dict[str, float]
    expense_by_category: Dict[str, float]
    
    avg_income: float
    avg_expense: float
    income_count: int
    expense_count: int
    transaction_count: int
    
    currency: str = 'UAH'  # Валюта звіту
    income_by_currency: Optional[Dict[str, float]] = None  # Розбивка доходів по валютах
    expense_by_currency: Optional[Dict[str, float]] = None  # Розбивка витрат по валютах
    income_by_category_currency: Optional[Dict[str, Dict[str, float]]] = None  # {category: {currency: amount}}
    expense_by_category_currency: Optional[Dict[str, Dict[str, float]]] = None  # {category: {currency: amount}}
    previous_period: Optional['PeriodComparison'] = None
    
    def to_dict(self) -> dict:
        """Конвертує модель у словник."""
        return {
            'user_id': self.user_id,
            'period_name': self.period_name,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'total_income': self.total_income,
            'total_expense': self.total_expense,
            'net_balance': self.net_balance,
            'income_by_category': self.income_by_category,
            'expense_by_category': self.expense_by_category,
            'avg_income': self.avg_income,
            'avg_expense': self.avg_expense,
            'income_count': self.income_count,
            'expense_count': self.expense_count,
            'transaction_count': self.transaction_count,
        }


@dataclass
class PeriodComparison:
    """
    Порівняння поточного періоду з попереднім.
    
    Attributes:
        prev_total_income: Загальний дохід попереднього періоду
        prev_total_expense: Загальні витрати попереднього періоду
        prev_net_balance: Баланс попереднього періоду
        income_change: Абсолютна зміна доходів
        income_change_percent: Процентна зміна доходів
        expense_change: Абсолютна зміна витрат
        expense_change_percent: Процентна зміна витрат
        balance_change: Абсолютна зміна балансу
        balance_change_percent: Процентна зміна балансу
    """
    prev_total_income: float
    prev_total_expense: float
    prev_net_balance: float
    
    income_change: float
    income_change_percent: float
    expense_change: float
    expense_change_percent: float
    balance_change: float
    balance_change_percent: float
    
    def to_dict(self) -> dict:
        """Конвертує модель у словник."""
        return {
            'prev_total_income': self.prev_total_income,
            'prev_total_expense': self.prev_total_expense,
            'prev_net_balance': self.prev_net_balance,
            'income_change': self.income_change,
            'income_change_percent': self.income_change_percent,
            'expense_change': self.expense_change,
            'expense_change_percent': self.expense_change_percent,
            'balance_change': self.balance_change,
            'balance_change_percent': self.balance_change_percent,
        }
