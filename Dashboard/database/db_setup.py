import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('finance_dashboard.db')
cursor = connection.cursor()

try:
    # Bank accounts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank_accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL
    )
    """)

    # Stocks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_name TEXT NOT NULL,
        shares REAL NOT NULL,
        current_value REAL NOT NULL,
        last_updated TEXT DEFAULT NULL
    )
    """)

    # Salary
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        frequency TEXT DEFAULT 'biweekly',
        next_payment_date DATE NOT NULL
    )
    """)

    # Goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        net_worth_target REAL NOT NULL,
        target_date DATE NOT NULL
    )
    """)

    cursor.execute("DROP TABLE IF EXISTS expenses")

    cursor.execute("""
    CREATE TABLE expenses (
    expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    frequency TEXT NOT NULL,
    amount REAL NOT NULL
    )
    """)

    # Net worth history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS net_worth_history (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        net_worth REAL NOT NULL,
        recorded_date DATE DEFAULT CURRENT_DATE
    )
    """)

    # Cryptos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cryptos (
        crypto_id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin_name TEXT NOT NULL,
        coins REAL NOT NULL,
        current_value REAL NOT NULL,
        last_updated TEXT DEFAULT NULL
    )
    """)

    # Income
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS income (
        income_id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT DEFAULT 'General',
        amount REAL NOT NULL,
        frequency TEXT NOT NULL
    )
    """)

    # Debts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS debts (
        debt_id INTEGER PRIMARY KEY AUTOINCREMENT,
        creditor TEXT NOT NULL,
        balance REAL NOT NULL,
        minimum_payment REAL NOT NULL,
        due_date DATE NOT NULL
    )
    """)

    # Check if stock_ticker column exists
    cursor.execute("PRAGMA table_info(stocks);")
    columns = [row[1] for row in cursor.fetchall()]

    if "stock_ticker" not in columns:
        print("Adding missing column: stock_ticker to stocks table...")
        cursor.execute("ALTER TABLE stocks ADD COLUMN stock_ticker TEXT;")
        connection.commit()
        print("Column 'stock_ticker' added successfully.")

    print("All tables created/updated successfully.")

except sqlite3.Error as e:
    print("Error creating tables:", e)

finally:
    connection.commit()
    connection.close()

