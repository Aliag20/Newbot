import sqlite3

conn = sqlite3.connect('bot_data.db', check_same_thread=False)
c = conn.cursor()

def setup_db():
    # جدول الردود
    c.execute('CREATE TABLE IF NOT EXISTS responses (trigger TEXT PRIMARY KEY, reply TEXT)')
    # جدول الرتب (0: مستخدم، 1: آدمن، 2: مطور)
    c.execute('CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, rank INTEGER DEFAULT 0)')
    conn.commit()

def set_rank(user_id, rank):
    c.execute('INSERT OR REPLACE INTO users (user_id, rank) VALUES (?, ?)', (user_id, rank))
    conn.commit()

def get_rank(user_id):
    c.execute('SELECT rank FROM users WHERE user_id = ?', (user_id,))
    res = c.fetchone()
    return res[0] if res else 0

def add_response(trigger, reply):
    c.execute('INSERT OR REPLACE INTO responses (trigger, reply) VALUES (?, ?)', (trigger, reply))
    conn.commit()
