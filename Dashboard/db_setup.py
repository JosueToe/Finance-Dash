import sqlite3

# Connect to SQLite database
connection = sqlite3.connect('database/finance_dashboard.db')
cursor = connection.cursor()

# Create tables
try:
    # Table for bank accounts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank_accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_type TEXT NOT NULL, -- savings or checking
        balance REAL NOT NULL
    )
    """)

    # Table for stocks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_name TEXT NOT NULL,
        shares REAL NOT NULL,
        current_value REAL NOT NULL
    )
    """)

    # Table for salary
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        frequency TEXT DEFAULT 'biweekly', -- biweekly or other frequencies
        next_payment_date DATE NOT NULL
    )
    """)

    # Table for financial goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        net_worth_target REAL NOT NULL,
        target_date DATE NOT NULL
    )
    """)

    # Table for expenses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL, -- e.g., rent, utilities
        category TEXT NOT NULL, -- e.g., housing, transportation
        frequency TEXT NOT NULL, -- weekly, biweekly, or monthly
        amount REAL NOT NULL
    )
    """)

    # Table for net worth history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS net_worth_history (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        net_worth REAL NOT NULL,
        recorded_date DATE DEFAULT CURRENT_DATE
    )
    """)

    print("All tables created successfully.")
except sqlite3.Error as e:
    print("Error creating tables:", e)
finally:
    # Commit changes and close connection
    connection.commit()
    connection.close()

    connection.commit()
    print("Database initialized successfully!")
    connection.close()

if __name__ == "__main__":
    create_database()
