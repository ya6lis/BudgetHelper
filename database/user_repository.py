# -*- coding: utf-8 -*-
"""
Репозиторій для роботи з користувачами в базі даних.
Використовує модель User для представлення даних.
"""

from threading import Lock
from typing import Optional
from .db_manager import get_connection
from models import User

_lock = Lock()


def get_user(user_id: int) -> Optional[User]:
    """
    Отримати користувача за ID.
    
    Args:
        user_id: ID користувача Telegram
    
    Returns:
        User або None
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT user_id, language, username
                FROM users WHERE user_id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            
            if row:
                return User(
                    user_id=row[0],
                    language=row[1] if row[1] else 'uk',
                    username=row[2]
                )
            return None


def create_user(user_id: int, language: str = 'uk', username: str = None) -> User:
    """
    Створити нового користувача.
    
    Args:
        user_id: ID користувача Telegram
        language: Мова інтерфейсу (за замовчуванням 'uk')
        username: Ім'я користувача в Telegram
    
    Returns:
        User: Створений об'єкт User
    """
    user = User(user_id=user_id, language=language, username=username)
    
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, language, username)
                VALUES (?, ?, ?)
            ''', (user.user_id, user.language, user.username))
            conn.commit()
    
    return user


def update_user_language(user_id: int, language: str) -> bool:
    """
    Оновити мову користувача.
    
    Args:
        user_id: ID користувача
        language: Нова мова ('uk', 'en')
    
    Returns:
        bool: True якщо успішно оновлено
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users SET language = ? WHERE user_id = ?
            ''', (language, user_id))
            conn.commit()
            return cursor.rowcount > 0


def get_user_language(user_id: int) -> Optional[str]:
    """
    Отримати мову користувача з бази даних.
    
    Args:
        user_id: ID користувача
    
    Returns:
        Optional[str]: Мова користувача ('uk', 'en') або None
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT language FROM users WHERE user_id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            return row[0] if row else None


def get_all_user_ids():
    """
    Отримати список всіх user_id з бази даних.
    
    Returns:
        list: Список ID користувачів
    """
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT user_id FROM users')
            return [row[0] for row in cursor.fetchall()]


def ensure_user_exists(user_id: int, username: str = None) -> User:
    """
    Перевірити чи існує користувач, якщо ні - створити.
    Також встановлює мову користувача з БД в locale_manager.
    
    Args:
        user_id: ID користувача Telegram
        username: Ім'я користувача в Telegram
    
    Returns:
        User: Об'єкт User
    """
    from locales import set_language
    
    user = get_user(user_id)
    if user is None:
        user = create_user(user_id, username=username)
    
    # Встановлюємо мову користувача з БД
    set_language(user_id, user.language)
    
    return user
