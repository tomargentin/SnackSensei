import sqlite3


def create_database():
    conn = sqlite3.connect('prices.db')
    c = conn.cursor()

    # Create table for Aldi
    c.execute('''
        CREATE TABLE IF NOT EXISTS aldi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            quantity FLOAT NOT NULL
        )
    ''')

    # Create table for Kaufland
    c.execute('''
        CREATE TABLE IF NOT EXISTS kaufland (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            quantity FLOAT NOT NULL
        )
    ''')

    # Create table for abc
    c.execute('''
        CREATE TABLE IF NOT EXISTS abc (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            quantity FLOAT NOT NULL
        )
    ''')

    # Create table for pqr
    c.execute('''
        CREATE TABLE IF NOT EXISTS pqr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            quantity FLOAT NOT NULL
        )
    ''')

    # Create table for std
    c.execute('''
        CREATE TABLE IF NOT EXISTS std (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT NOT NULL,
            price REAL NOT NULL,
            quantity FLOAT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()
