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
    """
    user_id: int
    language: str = 'uk'
    username: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Конвертує модель у словник для зберігання в БД."""
        return {
            'user_id': self.user_id,
            'language': self.language,
            'username': self.username
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'User':
        """Створює модель з словника даних з БД."""
        return User(
            user_id=data.get('user_id'),
            language=data.get('language', 'uk'),
            username=data.get('username')
        )
    
    def __repr__(self) -> str:
        return f"User(user_id={self.user_id}, language={self.language}, username={self.username})"
