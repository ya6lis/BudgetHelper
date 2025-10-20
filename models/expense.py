# -*- coding: utf-8 -*-
"""
Expense model для представлення витрат користувача.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Expense:
    """
    Модель витрати користувача.
    
    Attributes:
        user_id: ID користувача
        amount: Сума витрати
        description: Опис/категорія витрати (Їжа, Транспорт, тощо)
        currency: Валюта (UAH, USD, EUR)
        add_date: Дата додавання запису
        update_date: Дата останнього оновлення
        id: Унікальний ідентифікатор запису (генерується БД)
    """
    user_id: int
    amount: float
    description: str
    currency: str = 'UAH'
    add_date: Optional[str] = None
    update_date: Optional[str] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Ініціалізація дат при створенні об'єкта."""
        if self.add_date is None:
            self.add_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if self.update_date is None:
            self.update_date = self.add_date
    
    def to_dict(self) -> dict:
        """Конвертує модель у словник для зберігання в БД."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'amount': self.amount,
            'description': self.description,
            'currency': self.currency,
            'add_date': self.add_date,
            'update_date': self.update_date
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Expense':
        """Створює модель з словника даних з БД."""
        return Expense(
            id=data.get('id'),
            user_id=data['user_id'],
            amount=data['amount'],
            description=data['description'],
            currency=data.get('currency', 'UAH'),
            add_date=data.get('add_date'),
            update_date=data.get('update_date')
        )
    
    def update(self):
        """Оновлює дату останньої модифікації."""
        self.update_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def __repr__(self) -> str:
        return (f"Expense(id={self.id}, user_id={self.user_id}, "
                f"amount={self.amount}, description='{self.description}', "
                f"currency={self.currency}, add_date={self.add_date})")
