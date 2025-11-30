# -*- coding: utf-8 -*-
"""
Category model для представлення категорій доходів/витрат.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Category:
    """
    Модель категорії.
    
    Attributes:
        name: Назва категорії
        type: Тип ('income' або 'expense')
        is_default: Чи є категорія дефолтною (системною)
        user_id: ID користувача (None для дефолтних категорій)
        add_date: Дата додавання запису
        id: Унікальний ідентифікатор запису (генерується БД)
    """
    name: str
    type: str  # 'income' або 'expense'
    is_default: bool = False
    user_id: Optional[int] = None
    add_date: Optional[str] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Ініціалізація дат при створенні об'єкта."""
        if self.add_date is None:
            self.add_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self) -> dict:
        """Конвертує модель у словник для зберігання в БД."""
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'is_default': 1 if self.is_default else 0,
            'user_id': self.user_id,
            'add_date': self.add_date
        }
    
    @staticmethod
    def from_db_row(row: tuple):
        """Створює об'єкт Category з рядка БД."""
        return Category(
            id=row[0],
            name=row[1],
            type=row[2],
            is_default=bool(row[3]),
            user_id=row[4],
            add_date=row[5]
        )
