# -*- coding: utf-8 -*-
"""
Migration script to add currency support to existing database.
Adds:
- currency column to expenses table (if not exists)
- default_currency column to users table (if not exists)
"""

import sqlite3
import os
from config.constants import DB_FILE, DEFAULT_CURRENCY


def migrate_add_currency():
    """Add currency columns to expenses and users tables."""
    
    db_path = DB_FILE
    if not os.path.exists(db_path):
        print(f"[!] Database file '{db_path}' not found. No migration needed.")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("[*] Starting currency migration...")
        
        # Check if expenses table has currency column
        cursor.execute("PRAGMA table_info(expenses)")
        expenses_columns = [col[1] for col in cursor.fetchall()]
        
        if 'currency' not in expenses_columns:
            print("[*] Adding 'currency' column to expenses table...")
            cursor.execute(f'''
                ALTER TABLE expenses 
                ADD COLUMN currency TEXT DEFAULT '{DEFAULT_CURRENCY}'
            ''')
            # Update existing records to have default currency
            cursor.execute(f'''
                UPDATE expenses 
                SET currency = '{DEFAULT_CURRENCY}' 
                WHERE currency IS NULL
            ''')
            print("[OK] Added 'currency' column to expenses table")
        else:
            print("[*] 'currency' column already exists in expenses table")
        
        # Check if users table has default_currency column
        cursor.execute("PRAGMA table_info(users)")
        users_columns = [col[1] for col in cursor.fetchall()]
        
        if 'default_currency' not in users_columns:
            print("[*] Adding 'default_currency' column to users table...")
            cursor.execute(f'''
                ALTER TABLE users 
                ADD COLUMN default_currency TEXT DEFAULT '{DEFAULT_CURRENCY}'
            ''')
            # Update existing records to have default currency
            cursor.execute(f'''
                UPDATE users 
                SET default_currency = '{DEFAULT_CURRENCY}' 
                WHERE default_currency IS NULL
            ''')
            print("[OK] Added 'default_currency' column to users table")
        else:
            print("[*] 'default_currency' column already exists in users table")
        
        conn.commit()
        print("[OK] Currency migration completed successfully!")
        
    except Exception as e:
        print(f"[ERROR] Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    migrate_add_currency()
