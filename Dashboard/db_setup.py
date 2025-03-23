import sqlite3  # Import SQLite library to interact with the database.

# Connect to SQLite database
connection = sqlite3.connect('database/finance_dashboard.db')  # Creates or opens the database file.
cursor = connection.cursor()  # Cursor is used to execute SQL commands.

# Create tables
try:
    # Table for bank accounts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bank_accounts (
        account_id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique identifier for each account.
        account_type TEXT NOT NULL,  -- savings or checking
        balance REAL NOT NULL  # Current balance in the account.
    )
    """)

    # Table for stocks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        stock_id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique identifier for each stock.
        stock_name TEXT NOT NULL,  # Name of the stock (e.g., Apple, Google).
        shares REAL NOT NULL,  # Number of shares owned.
        current_value REAL NOT NULL  # Current value per share.
    )
    """)

    # Table for salary
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS salary (
        salary_id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique identifier for each salary entry.
        amount REAL NOT NULL,  # Amount of the salary (biweekly by default).
        frequency TEXT DEFAULT 'biweekly',  -- biweekly or other frequencies
        next_payment_date DATE NOT NULL  # Date of the next salary payment.
    )
    """)

    # Table for financial goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique identifier for each financial goal.
        net_worth_target REAL NOT NULL,  # Target net worth to achieve.
        target_date DATE NOT NULL  # Deadline to achieve the financial goal.
    )
    """)

    # Table for expenses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        expense_id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique identifier for each expense.
        name TEXT NOT NULL,  -- e.g., rent, utilities
        category TEXT NOT NULL,  -- e.g., housing, transportation
        frequency TEXT NOT NULL,  -- weekly, biweekly, or monthly
        amount REAL NOT NULL  # Amount of the expense.
    )
    """)

    # Table for net worth history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS net_worth_history (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,  # Unique identifier for each record.
        net_worth REAL NOT NULL,  # Net worth value recorded.
        recorded_date DATE DEFAULT CURRENT_DATE  # Date when the record was added (default is the current date).
    )
    """)

    print("All tables created successfully.")  # Confirm successful table creation.
except sqlite3.Error as e:
    # Handle and print any errors that occur during table creation.
    print("Error creating tables:", e)
finally:
    # Commit changes to save the database schema.
    connection.commit()
    # Close the database connection to free resources.
    connection.close()
