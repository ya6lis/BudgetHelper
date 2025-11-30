# -*- coding: utf-8 -*-
"""
Repository для роботи з категоріями доходів/витрат.
"""

import logging
from typing import List, Optional
from models.category import Category
from database.db_manager import get_connection, ensure_user, generate_uuid, _lock

logger = logging.getLogger(__name__)


class CategoryRepository:
    """Репозиторій для роботи з категоріями."""
    
    @staticmethod
    def get_categories_by_type(user_id: int, category_type: str) -> List[Category]:
        """
        Отримати всі категорії (дефолтні + кастомні користувача) за типом.
        
        Args:
            user_id: ID користувача
            category_type: 'income' або 'expense'
        
        Returns:
            List[Category]: Список категорій
        """
        with _lock:
            with get_connection() as conn:
                cursor = conn.cursor()
                ensure_user(cursor, user_id)
                
                # Отримуємо дефолтні категорії та кастомні користувача
                cursor.execute('''
                    SELECT DISTINCT id, name, type, is_default, user_id, add_date
                    FROM categories
                    WHERE type = ? AND (is_default = 1 OR user_id = ?)
                    ORDER BY is_default DESC, name ASC
                ''', (category_type, user_id))
                
                rows = cursor.fetchall()
                return [Category.from_db_row(row) for row in rows]
    
    @staticmethod
    def add_custom_category(user_id: int, name: str, category_type: str) -> Optional[int]:
        """
        Додати кастомну категорію користувача.
        
        Args:
            user_id: ID користувача
            name: Назва категорії
            category_type: 'income' або 'expense'
        
        Returns:
            Optional[int]: ID створеної категорії або None якщо помилка
        """
        with _lock:
            with get_connection() as conn:
                cursor = conn.cursor()
                ensure_user(cursor, user_id)
                
                try:
                    new_id = generate_uuid()
                    cursor.execute('''
                        INSERT INTO categories (id, name, type, is_default, user_id, add_date)
                        VALUES (?, ?, ?, 0, ?, datetime('now'))
                    ''', (new_id, name, category_type, user_id))
                    
                    conn.commit()
                    return new_id
                except Exception as e:
                    logger.error(f"Failed to add custom category: {e}")
                    return None
    
    @staticmethod
    def delete_custom_category(user_id: int, category_id: int) -> bool:
        """
        Видалити кастомну категорію користувача.
        
        Args:
            user_id: ID користувача
            category_id: ID категорії
        
        Returns:
            bool: True якщо успішно, False якщо помилка
        """
        with _lock:
            with get_connection() as conn:
                cursor = conn.cursor()
                
                try:
                    # Видаляємо тільки кастомні категорії користувача
                    cursor.execute('''
                        DELETE FROM categories
                        WHERE id = ? AND user_id = ? AND is_default = 0
                    ''', (category_id, user_id))
                    
                    conn.commit()
                    return cursor.rowcount > 0
                except Exception as e:
                    logger.error(f"Failed to delete custom category: {e}")
                    return False
    
    @staticmethod
    def get_category_by_id(category_id: int) -> Optional[Category]:
        """
        Отримати категорію за ID.
        
        Args:
            category_id: ID категорії
        
        Returns:
            Optional[Category]: Об'єкт категорії або None
        """
        with _lock:
            with get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT id, name, type, is_default, user_id, add_date
                    FROM categories
                    WHERE id = ?
                ''', (category_id,))
                
                row = cursor.fetchone()
                return Category.from_db_row(row) if row else None
    
    @staticmethod
    def category_exists(user_id: int, name: str, category_type: str) -> bool:
        """
        Перевірити чи існує категорія з такою назвою.
        
        Args:
            user_id: ID користувача
            name: Назва категорії
            category_type: 'income' або 'expense'
        
        Returns:
            bool: True якщо існує
        """
        with _lock:
            with get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM categories
                    WHERE name = ? AND type = ? AND (is_default = 1 OR user_id = ?)
                ''', (name, category_type, user_id))
                
                count = cursor.fetchone()[0]
                return count > 0
