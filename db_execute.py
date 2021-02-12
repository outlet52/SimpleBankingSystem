import sqlite3


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0);""")
conn.commit()
cur.execute('''SELECT * FROM card''')
database_info = cur.fetchall()
