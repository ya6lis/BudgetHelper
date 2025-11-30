# -*- coding: utf-8 -*-

import sqlite3
import uuid
from threading import Lock
from config.constants import DB_FILE

_lock = Lock()


def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def generate_uuid():
    """Генерувати UUID як рядок."""
    return str(uuid.uuid4())


def init_db():
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                language TEXT DEFAULT 'uk',
                username TEXT
            );
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS bot_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                message_id INTEGER,
                add_date TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS incomes (
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                category_id TEXT,
                description TEXT,
                currency TEXT DEFAULT 'UAH',
                add_date TEXT,
                update_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
            );
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                category_id TEXT,
                description TEXT,
                add_date TEXT,
                update_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT
            );
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                is_default INTEGER DEFAULT 0,
                user_id INTEGER,
                add_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(name, type, user_id)
            );
            ''')
            
            # Додаємо дефолтні категорії доходів (тільки якщо їх ще немає)
            default_income_categories = [
                ('Зарплата', 'income'),
                ('Премія', 'income'),
                ('Подарунок', 'income'),
                ('Інвестиції', 'income'),
                ('Інше', 'income')
            ]
            
            for name, cat_type in default_income_categories:
                # Перевіряємо чи існує дефолтна категорія
                cursor.execute('''
                    SELECT COUNT(*) FROM categories 
                    WHERE name = ? AND type = ? AND is_default = 1 AND user_id IS NULL
                ''', (name, cat_type))
                
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO categories (id, name, type, is_default, add_date)
                        VALUES (?, ?, ?, 1, datetime('now'))
                    ''', (generate_uuid(), name, cat_type))
            
            # Додаємо дефолтні категорії витрат (тільки якщо їх ще немає)
            default_expense_categories = [
                ('Їжа', 'expense'),
                ('Транспорт', 'expense'),
                ('Здоров\'я', 'expense'),
                ('Розваги', 'expense'),
                ('Інше', 'expense')
            ]
            
            for name, cat_type in default_expense_categories:
                # Перевіряємо чи існує дефолтна категорія
                cursor.execute('''
                    SELECT COUNT(*) FROM categories 
                    WHERE name = ? AND type = ? AND is_default = 1 AND user_id IS NULL
                ''', (name, cat_type))
                
                if cursor.fetchone()[0] == 0:
                    cursor.execute('''
                        INSERT INTO categories (id, name, type, is_default, add_date)
                        VALUES (?, ?, ?, 1, datetime('now'))
                    ''', (generate_uuid(), name, cat_type))
            
            conn.commit()
    
    print("[OK] Database initialized successfully!", flush=True)


def ensure_user(cursor, user_id):
    cursor.execute('INSERT OR IGNORE INTO users(user_id) VALUES (?)', (user_id,))


def save_bot_message(user_id: int, message_id: int):
    """Зберігає message_id повідомлення відправленого ботом."""
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO bot_messages (user_id, message_id)
                VALUES (?, ?)
            ''', (user_id, message_id))
            conn.commit()


def get_user_bot_messages(user_id: int):
    """Отримує всі message_id для користувача."""
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT message_id FROM bot_messages 
                WHERE user_id = ?
                ORDER BY id DESC
                LIMIT 100
            ''', (user_id,))
            return [row[0] for row in cursor.fetchall()]


def clear_user_bot_messages(user_id: int):
    """Видаляє всі збережені message_id для користувача."""
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bot_messages WHERE user_id = ?', (user_id,))
            conn.commit()


def delete_bot_message(user_id: int, message_id: int):
    """Видаляє конкретний message_id з бази даних."""
    with _lock:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM bot_messages WHERE user_id = ? AND message_id = ?', (user_id, message_id))
            conn.commit()
