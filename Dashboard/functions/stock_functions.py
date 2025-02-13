import sqlite3  # Import SQLite library
from functions.validate_functions import get_valid_text, get_valid_float

def add_stock():
    """
    Add a new stock entry with validated input.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid stock name
        stock_name = get_valid_text("Enter stock name: ")
        if stock_name is None:
            return  # User chose to cancel

        # Get valid number of shares
        shares = get_valid_float("Enter number of shares: ")
        if shares is None:
            return

        # Get valid current value per share
        current_value = get_valid_float("Enter current value per share: ")
        if current_value is None:
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO stocks (stock_name, shares, current_value)
            VALUES (?, ?, ?)
        """, (stock_name, shares, current_value))
        connection.commit()
        print(f"Added {shares} shares of {stock_name} at ${current_value:.2f} per share.")

    except sqlite3.Error as e:
        print("Error adding stock:", e)
    finally:
        connection.close()
