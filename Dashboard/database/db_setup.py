import sqlite3

# Connect to the SQLite database
connection = sqlite3.connect('database/finance_dashboard.db')
cursor = connection.cursor()

try:
    # Create bank accounts table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank_accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,
        account_type TEXT NOT NULL,
        balance REAL NOT NULL
    )
    """)

    # Create stocks table (initial structure)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_name TEXT NOT NULL,
        shares REAL NOT NULL,
        current_value REAL NOT NULL
    )
    """)

    # Create salary table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        frequency TEXT DEFAULT 'biweekly',
        next_payment_date DATE NOT NULL
    )
    """)

    # Create goals table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        net_worth_target REAL NOT NULL,
        target_date DATE NOT NULL
    )
    """)

    # Create expenses table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        frequency TEXT NOT NULL,
        amount REAL NOT NULL
    )
    """)

    # Create net worth history table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS net_worth_history (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        net_worth REAL NOT NULL,
        recorded_date DATE DEFAULT CURRENT_DATE
    )
    """)

    # Create cryptos table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cryptos (
        crypto_id INTEGER PRIMARY KEY AUTOINCREMENT,
        coin_name TEXT NOT NULL,
        coins REAL NOT NULL,
        current_value REAL NOT NULL
    )
    """)

    # 🛠️ Check if the 'stock_ticker' column exists in the stocks table
    cursor.execute("PRAGMA table_info(stocks);")
    columns = [row[1] for row in cursor.fetchall()]
    
    if "stock_ticker" not in columns:
        print("🔧 Adding missing column: stock_ticker to stocks table...")
        cursor.execute("ALTER TABLE stocks ADD COLUMN stock_ticker TEXT;")
        connection.commit()
        print("✅ Column 'stock_ticker' added successfully.")

    print("✅ All tables created/updated successfully.")
except sqlite3.Error as e:
    print("❌ Error creating/updating tables:", e)
finally:
    connection.commit()
    connection.close()
