# -*- coding: utf-8 -*-
"""
Міграція бази даних: зміна INTEGER ID на UUID.
УВАГА: Створює бекап перед міграцією!
"""

import sqlite3
import uuid
import shutil
from datetime import datetime
from pathlib import Path
from config.constants import DB_FILE

def backup_database():
    """Створити бекап БД перед міграцією."""
    backup_path = f"{DB_FILE}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(DB_FILE, backup_path)
    print(f"✅ Бекап створено: {backup_path}")
    return backup_path

def migrate_to_uuid():
    """Міграція БД з INTEGER ID на UUID."""
    
    if not Path(DB_FILE).exists():
        print("❌ База даних не знайдена!")
        return False
    
    print("🔄 Починаємо міграцію до UUID...")
    backup_path = backup_database()
    
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.execute('PRAGMA foreign_keys = OFF')
        cursor = conn.cursor()
        
        # 1. Міграція categories
        print("\n📂 Міграція таблиці categories...")
        
        # Створюємо мапінг старих ID на нові UUID
        cursor.execute('SELECT id, name, type, is_default, user_id, add_date FROM categories')
        categories = cursor.fetchall()
        category_mapping = {}
        
        # Створюємо нову таблицю
        cursor.execute('''
            CREATE TABLE categories_new (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('income', 'expense')),
                is_default INTEGER DEFAULT 0,
                user_id INTEGER,
                add_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                UNIQUE(name, type, user_id)
            )
        ''')
        
        # Копіюємо дані з новими UUID
        for old_id, name, cat_type, is_default, user_id, add_date in categories:
            new_id = str(uuid.uuid4())
            category_mapping[old_id] = new_id
            cursor.execute('''
                INSERT INTO categories_new (id, name, type, is_default, user_id, add_date)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (new_id, name, cat_type, is_default, user_id, add_date))
        
        print(f"  ✅ Змігровано {len(categories)} категорій")
        
        # 2. Міграція incomes
        print("\n💰 Міграція таблиці incomes...")
        
        cursor.execute('SELECT id, user_id, amount, category_id, description, currency, add_date, update_date FROM incomes')
        incomes = cursor.fetchall()
        
        cursor.execute('''
            CREATE TABLE incomes_new (
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                category_id TEXT,
                description TEXT,
                currency TEXT DEFAULT 'UAH',
                add_date TEXT,
                update_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories_new(id) ON DELETE RESTRICT
            )
        ''')
        
        for old_id, user_id, amount, old_category_id, description, currency, add_date, update_date in incomes:
            new_id = str(uuid.uuid4())
            new_category_id = category_mapping.get(old_category_id)
            if new_category_id:
                cursor.execute('''
                    INSERT INTO incomes_new (id, user_id, amount, category_id, description, currency, add_date, update_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (new_id, user_id, amount, new_category_id, description, currency, add_date, update_date))
        
        print(f"  ✅ Змігровано {len(incomes)} доходів")
        
        # 3. Міграція expenses
        print("\n💸 Міграція таблиці expenses...")
        
        cursor.execute('SELECT id, user_id, amount, category_id, description, add_date, update_date FROM expenses')
        expenses = cursor.fetchall()
        
        cursor.execute('''
            CREATE TABLE expenses_new (
                id TEXT PRIMARY KEY,
                user_id INTEGER,
                amount REAL,
                category_id TEXT,
                description TEXT,
                add_date TEXT,
                update_date TEXT,
                FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
                FOREIGN KEY (category_id) REFERENCES categories_new(id) ON DELETE RESTRICT
            )
        ''')
        
        for old_id, user_id, amount, old_category_id, description, add_date, update_date in expenses:
            new_id = str(uuid.uuid4())
            new_category_id = category_mapping.get(old_category_id)
            if new_category_id:
                cursor.execute('''
                    INSERT INTO expenses_new (id, user_id, amount, category_id, description, add_date, update_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (new_id, user_id, amount, new_category_id, description, add_date, update_date))
        
        print(f"  ✅ Змігровано {len(expenses)} витрат")
        
        # 4. Видаляємо старі таблиці та перейменовуємо нові
        print("\n🔄 Заміна таблиць...")
        cursor.execute('DROP TABLE incomes')
        cursor.execute('DROP TABLE expenses')
        cursor.execute('DROP TABLE categories')
        
        cursor.execute('ALTER TABLE categories_new RENAME TO categories')
        cursor.execute('ALTER TABLE incomes_new RENAME TO incomes')
        cursor.execute('ALTER TABLE expenses_new RENAME TO expenses')
        
        conn.execute('PRAGMA foreign_keys = ON')
        conn.commit()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ Міграція завершена успішно!")
        print(f"📊 Категорій: {len(categories)}")
        print(f"💰 Доходів: {len(incomes)}")
        print(f"💸 Витрат: {len(expenses)}")
        print(f"💾 Бекап збережено: {backup_path}")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Помилка під час міграції: {e}")
        print(f"💾 Відновіть БД з бекапу: {backup_path}")
        return False

def main():
    """Головна функція."""
    print("="*60)
    print("⚠️  МІГРАЦІЯ БАЗИ ДАНИХ: INTEGER → UUID")
    print("="*60)
    print("\nЦей скрипт:")
    print("  1. Створить бекап поточної БД")
    print("  2. Змінить всі ID з INTEGER на UUID")
    print("  3. Оновить всі зв'язки між таблицями")
    print("\n⚠️  УВАГА: Процес незворотній!")
    print("\nНатисніть Enter щоб продовжити або Ctrl+C для скасування...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\n❌ Міграцію скасовано")
        return
    
    migrate_to_uuid()

if __name__ == '__main__':
    main()
