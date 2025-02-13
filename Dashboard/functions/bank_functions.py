import sqlite3  # Import SQLite library
from functions.validate_functions import get_valid_text, get_valid_float

def add_bank_account():
    """
    Add a new bank account entry with validated input.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid account type
        while True:
            account_type = get_valid_text("Enter account type (savings/checking): ").lower()
            if account_type is None:
                return  # User chose to cancel
            if account_type in ["savings", "checking"]:
                break
            print("Invalid account type. Please enter 'savings' or 'checking'.")

        # Get valid account balance
        balance = get_valid_float("Enter account balance: ")
        if balance is None:
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO bank_accounts (account_type, balance)
            VALUES (?, ?)
        """, (account_type, balance))
        connection.commit()
        print(f"{account_type.capitalize()} account added successfully with balance ${balance:.2f}.")

    except sqlite3.Error as e:
        print("Error adding bank account:", e)
    finally:
        connection.close()
