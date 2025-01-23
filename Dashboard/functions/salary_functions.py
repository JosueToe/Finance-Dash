import sqlite3  # Import SQLite library to interact with the database.
from datetime import datetime  # Import datetime to work with date-related operations.

def add_salary():
    # Connect to the database where the salary data is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()  # Cursor is used to execute SQL commands.

    # Loop until the user provides a valid biweekly salary amount.
    while True:
        amount_input = input("Enter biweekly salary amount: ")  # Prompt for the salary amount.
        try:
            # Convert the input to a float and remove commas if present.
            amount = float(amount_input.replace(",", ""))
            break  # Exit the loop if input is valid.
        except ValueError:
            # Show an error message for invalid input.
            print("Invalid input. Please enter a numeric value for the salary amount.")

    # Loop until the user provides a valid date for the next payment.
    while True:
        next_payment_date = input("Enter next payment date (MM/DD/YYYY): ")  # Prompt for the date.
        try:
            # Convert the input date to the format YYYY-MM-DD for database storage.
            valid_date = datetime.strptime(next_payment_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            break  # Exit the loop if input is valid.
        except ValueError:
            # Show an error message for invalid date format.
            print("Invalid date format. Please enter the date in MM/DD/YYYY format.")

    try:
        # Insert the salary data (amount, frequency, and next payment date) into the "salary" table.
        cursor.execute("""
            INSERT INTO salary (amount, frequency, next_payment_date)
            VALUES (?, ?, ?)
        """, (amount, 'biweekly', valid_date))
        connection.commit()  # Save changes to the database.
        # Confirm that the salary was successfully added.
        print(f"Biweekly salary of ${amount:.2f} added. Next payment date: {next_payment_date}.")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error adding salary:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()