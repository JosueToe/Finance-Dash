import sqlite3  # Import SQLite library to interact with the database.
from datetime import datetime  # Import datetime to work with date-related operations.
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)





def expense_breakdown():
    """
    Display a breakdown of expenses grouped by category.
    """
    # Connect to the database where the expense data is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()  # Cursor is used to execute SQL commands.

    try:
        # Retrieve the total expenses grouped by category from the "expenses" table.
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        expenses = cursor.fetchall()  # Fetch all rows from the query result.

        # Print the breakdown of expenses.
        print("\n===== Expense Breakdown =====")
        if not expenses:  # Check if there are no recorded expenses.
            print("No expenses recorded.")
        else:
            # Iterate through each category and its total expense, printing the details.
            for category, total in expenses:
                print(f"{category.capitalize()}: ${total:.2f}")
        print("=============================")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error generating expense breakdown:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()

def cash_flow_report():
    """
    Display the user's total monthly income, expenses, and net cash flow.
    """
    # Connect to the database to retrieve income and expense data.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Calculate the total monthly income by retrieving all salary records.
        cursor.execute("SELECT amount FROM salary")
        salaries = cursor.fetchall()  # Fetch all salary amounts.
        total_monthly_income = sum([salary[0] * 2 for salary in salaries])  # Assuming biweekly salary.

        # Calculate the total monthly expenses based on frequency and amount.
        cursor.execute("SELECT frequency, amount FROM expenses")
        expenses = cursor.fetchall()  # Fetch all expense records.
        total_monthly_expenses = 0.0
        for frequency, amount in expenses:
            if frequency == 'weekly':
                total_monthly_expenses += amount * 4  # Multiply by 4 for weekly expenses.
            elif frequency == 'biweekly':
                total_monthly_expenses += amount * 2  # Multiply by 2 for biweekly expenses.
            elif frequency == 'monthly':
                total_monthly_expenses += amount  # Use the amount directly for monthly expenses.

        # Calculate the net cash flow (income minus expenses).
        net_cash_flow = total_monthly_income - total_monthly_expenses

        # Print the cash flow report.
        print("\n===== Cash Flow Report =====")
        print(f"Total Monthly Income: ${total_monthly_income:.2f}")
        print(f"Total Monthly Expenses: ${total_monthly_expenses:.2f}")
        print(f"Net Monthly Cash Flow: ${net_cash_flow:.2f}")
        print("===========================")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error generating cash flow report:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()

def record_net_worth():
    """
    Record the user's current net worth as a snapshot in the database.
    """
    # Connect to the database where financial data is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Calculate the total bank balances by summing up the "balance" column in "bank_accounts".
        cursor.execute("SELECT SUM(balance) FROM bank_accounts")
        total_bank = cursor.fetchone()[0] or 0.0  # Default to 0 if no records are found.

        # Calculate the total stock value using the formula: shares * current_value.
        cursor.execute("SELECT SUM(shares * current_value) FROM stocks")
        total_stocks = cursor.fetchone()[0] or 0.0  # Default to 0 if no records are found.

        # Calculate the total monthly expenses using their frequency.
        cursor.execute("SELECT frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        total_monthly_expenses = 0.0
        for frequency, amount in expenses:
            if frequency == 'weekly':
                total_monthly_expenses += amount * 4  # Multiply by 4 for weekly expenses.
            elif frequency == 'biweekly':
                total_monthly_expenses += amount * 2  # Multiply by 2 for biweekly expenses.
            elif frequency == 'monthly':
                total_monthly_expenses += amount  # Use the amount directly for monthly expenses.

        # Calculate net worth by adding total bank balances and stock value, then subtracting expenses.
        net_worth = total_bank + total_stocks - total_monthly_expenses

        # Insert the calculated net worth into the "net_worth_history" table.
        cursor.execute("""
            INSERT INTO net_worth_history (net_worth)
            VALUES (?)
        """, (net_worth,))
        connection.commit()  # Save changes to the database.
        # Confirm that the net worth has been recorded.
        print(f"Net worth recorded: ${net_worth:.2f} on {datetime.today().strftime('%Y-%m-%d')}")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error recording net worth:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()

def net_worth_trend():
    """
    Display a trend of the user's net worth over time.
    """
    # Connect to the database where the net worth history is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Retrieve all net worth records, ordered by their recorded date.
        cursor.execute("SELECT recorded_date, net_worth FROM net_worth_history ORDER BY recorded_date ASC")
        records = cursor.fetchall()  # Fetch all rows from the query result.

        # Print the trend of net worth over time.
        print("\n===== Net Worth Trend =====")
        if not records:  # Check if there are no recorded net worth entries.
            print("No net worth records found. Please record your net worth first.")
        else:
            # Iterate through each record and display the date and net worth.
            for record_date, net_worth in records:
                print(f"{record_date}: ${net_worth:.2f}")
        print("===========================")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error generating net worth trend:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()
