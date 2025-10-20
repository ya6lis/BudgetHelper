# -*- coding: utf-8 -*-

import sqlite3
from threading import Lock
from config.constants import DB_FILE

_lock = Lock()


def get_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


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
            CREATE TABLE IF NOT EXISTS incomes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                description TEXT,
                currency TEXT DEFAULT 'UAH',
                add_date TEXT,
                update_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            ''')
            
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount REAL,
                description TEXT,
                add_date TEXT,
                update_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
            );
            ''')
            
            conn.commit()
    
    print("[OK] Database initialized successfully!", flush=True)


def ensure_user(cursor, user_id):
    cursor.execute('INSERT OR IGNORE INTO users(user_id) VALUES (?)', (user_id,))
