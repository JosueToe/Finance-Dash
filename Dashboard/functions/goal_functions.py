import sqlite3  # Importing SQLite library
from functions.validate_functions import get_valid_float, get_valid_date

def add_financial_goal():
    """
    Add a new financial goal entry with validated input.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid target net worth goal
        target_net_worth = get_valid_float("Enter your target net worth goal: ")
        if target_net_worth is None:
            return  # User chose to cancel

        # Get valid target date
        target_date = get_valid_date("Enter the target date to achieve this goal (MM/DD/YYYY): ")
        if target_date is None:
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO goals (net_worth_target, target_date)
            VALUES (?, ?)
        """, (target_net_worth, target_date))
        connection.commit()
        print(f"Goal of ${target_net_worth:.2f} by {target_date} added successfully!")

    except sqlite3.Error as e:
        print("Error adding goal:", e)
    finally:
        connection.close()
