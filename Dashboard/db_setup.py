import sqlite3
import os

def create_database():
    # Ensure the 'database' folder exists
    if not os.path.exists('database'):
        os.makedirs('database')

    # Connect to the database
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank_accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_name TEXT NOT NULL,
        shares REAL NOT NULL,
        current_value REAL NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        frequency TEXT NOT NULL,
        next_payment_date DATE NOT NULL
    )
    """)

    cursor.execute("""
CREATE TABLE IF NOT EXISTS goals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    net_worth_target REAL NOT NULL,
    target_date DATE NOT NULL
)
""")


    # Replace the subscriptions table with an expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,    -- e.g., 'rent', 'utilities', 'subscription'
        frequency TEXT NOT NULL,   -- 'weekly', 'biweekly', 'monthly'
        amount REAL NOT NULL
    )
    """)

    connection.commit()
    print("Database initialized successfully!")
    connection.close()

if __name__ == "__main__":
    create_database()
