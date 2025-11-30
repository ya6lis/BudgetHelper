# -*- coding: utf-8 -*-
"""
User model для представлення користувача системи.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """
    Модель користувача Telegram бота.
    
    Attributes:
        user_id: Унікальний ідентифікатор користувача Telegram
        language: Мова інтерфейсу (uk, en)
        username: Ім'я користувача в Telegram (опціонально)
        default_currency: Валюта за замовчуванням (UAH, USD, EUR)
    """
    user_id: int
    language: str = 'uk'
    username: Optional[str] = None
    default_currency: str = 'UAH'
    
    def to_dict(self) -> dict:
        """Конвертує модель у словник для зберігання в БД."""
        return {
            'user_id': self.user_id,
            'language': self.language,
            'username': self.username,
            'default_currency': self.default_currency
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'User':
        """Створює модель з словника даних з БД."""
        return User(
            user_id=data.get('user_id'),
            language=data.get('language', 'uk'),
            username=data.get('username'),
            default_currency=data.get('default_currency', 'UAH')
        )
    
    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, language={self.language}, username={self.username}, default_currency={self.default_currency})"
