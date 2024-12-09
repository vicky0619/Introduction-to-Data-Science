import sqlite3

DB_FILE = "user_data.db"

def initialize_database():
    """創建資料庫和表"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food_name TEXT,
            quantity INTEGER,
            calories REAL,
            protein REAL,
            fats REAL,
            carbs REAL
        )
    ''')
    conn.commit()
    conn.close()

def insert_user_record(date, food_name, quantity, calories, protein, fats, carbs):
    """插入用戶記錄"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO user_records (date, food_name, quantity, calories, protein, fats, carbs)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (date, food_name, quantity, calories, protein, fats, carbs))
    conn.commit()
    conn.close()

def fetch_user_records():
    """獲取所有用戶記錄"""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_records")
    records = cursor.fetchall()
    conn.close()
    return records
