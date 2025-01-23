import sqlite3  # Importing SQLite library to interact with the database.
from datetime import datetime  # Importing datetime to work with dates.

def add_financial_goal():
    # Connect to the database where the finance data is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()  # Cursor is used to execute SQL commands.

    # Loop until the user provides a valid numeric target net worth.
    while True:
        target_input = input("Enter your target net worth goal: ")  # Prompt for the goal amount.
        try:
            # Convert the target input to a float, removing commas if present.
            target_net_worth = float(target_input.replace(",", ""))
            break  # Exit the loop if input is valid.
        except ValueError:
            # Show an error message for invalid input.
            print("Invalid input. Please enter a numeric value for the goal.")

    # Loop until the user provides a valid date in MM/DD/YYYY format.
    while True:
        target_date = input("Enter the target date to achieve this goal (MM/DD/YYYY): ")
        try:
            # Convert the date string to the correct format (YYYY-MM-DD) for database storage.
            valid_date = datetime.strptime(target_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            break  # Exit the loop if input is valid.
        except ValueError:
            # Show an error message for invalid date format.
            print("Invalid date format. Please enter the date in MM/DD/YYYY format.")

    try:
        # Insert the goal data (net worth and target date) into the "goals" table in the database.
        cursor.execute("""
            INSERT INTO goals (net_worth_target, target_date)
            VALUES (?, ?)
        """, (target_net_worth, valid_date))
        connection.commit()  # Save changes to the database.
        # Confirm that the goal was successfully added.
        print(f"Goal of ${target_net_worth:.2f} by {target_date} added successfully!")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error adding goal:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()