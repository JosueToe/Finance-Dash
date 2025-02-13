import sqlite3  # Import SQLite library
from functions.validate_functions import get_valid_float, get_valid_date

def add_salary():
    """
    Add a new salary entry with validated input.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid biweekly salary amount
        amount = get_valid_float("Enter biweekly salary amount: ")
        if amount is None:
            return  # User chose to cancel

        # Get valid next payment date
        next_payment_date = get_valid_date("Enter next payment date (MM/DD/YYYY): ")
        if next_payment_date is None:
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO salary (amount, frequency, next_payment_date)
            VALUES (?, ?, ?)
        """, (amount, 'biweekly', next_payment_date))
        connection.commit()
        print(f"Biweekly salary of ${amount:.2f} added. Next payment date: {next_payment_date}.")

    except sqlite3.Error as e:
        print("Error adding salary:", e)
    finally:
        connection.close()
