import sqlite3  # Importing SQLite library
from functions.validate_functions import (
    get_valid_text, get_valid_frequency, get_valid_float
)

def add_expense():
    """
    Add a new expense entry with validated input.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid expense name
        name = get_valid_text("Enter expense name (e.g., 'Rent', 'Electricity Bill'): ")
        if name is None:
            return  # User chose to cancel

        # Get valid category
        category = get_valid_text("Enter category (e.g., 'rent', 'utilities', 'subscription'): ")
        if category is None:
            return

        # Get valid frequency
        frequency = get_valid_frequency("Enter frequency (weekly/biweekly/monthly): ")
        if frequency is None:
            return

        # Get valid amount
        amount = get_valid_float("Enter the amount: ")
        if amount is None:
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO expenses (name, category, frequency, amount)
            VALUES (?, ?, ?, ?)
        """, (name, category, frequency, amount))
        connection.commit()
        print(f"Expense '{name}' of ${amount:.2f} ({frequency}) added successfully!")

    except sqlite3.Error as e:
        print("Error adding expense:", e)
    finally:
        connection.close()
