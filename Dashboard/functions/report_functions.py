import sqlite3
from datetime import datetime


def expense_breakdown():
    """
    Display a breakdown of expenses grouped by category.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        expenses = cursor.fetchall()

        print("\n===== Expense Breakdown =====")
        if not expenses:
            print("No expenses recorded.")
        else:
            for category, total in expenses:
                print(f"{category.capitalize()}: ${total:.2f}")
        print("=============================")
    except sqlite3.Error as e:
        print("Error generating expense breakdown:", e)
    finally:
        connection.close()


def cash_flow_report():
    """
    Display the user's total monthly income, expenses, and net cash flow.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Total monthly income
        cursor.execute("SELECT amount FROM salary")
        salaries = cursor.fetchall()
        total_monthly_income = sum([salary[0] * 2 for salary in salaries])  # Assuming biweekly salary

        # Total monthly expenses
        cursor.execute("SELECT frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        total_monthly_expenses = 0.0
        for frequency, amount in expenses:
            if frequency == 'weekly':
                total_monthly_expenses += amount * 4  # Approximate 4 weeks in a month
            elif frequency == 'biweekly':
                total_monthly_expenses += amount * 2  # Approximate 2 biweeks in a month
            elif frequency == 'monthly':
                total_monthly_expenses += amount

        # Net monthly cash flow
        net_cash_flow = total_monthly_income - total_monthly_expenses

        print("\n===== Cash Flow Report =====")
        print(f"Total Monthly Income: ${total_monthly_income:.2f}")
        print(f"Total Monthly Expenses: ${total_monthly_expenses:.2f}")
        print(f"Net Monthly Cash Flow: ${net_cash_flow:.2f}")
        print("===========================")
    except sqlite3.Error as e:
        print("Error generating cash flow report:", e)
    finally:
        connection.close()


def record_net_worth():

    """
    Record the user's current net worth as a snapshot in the database.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Calculate total bank balances
        cursor.execute("SELECT SUM(balance) FROM bank_accounts")
        total_bank = cursor.fetchone()[0] or 0.0

        # Calculate total stock value
        cursor.execute("SELECT SUM(shares * current_value) FROM stocks")
        total_stocks = cursor.fetchone()[0] or 0.0

        # Calculate total monthly expenses
        cursor.execute("SELECT frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        total_monthly_expenses = 0.0
        for frequency, amount in expenses:
            if frequency == 'weekly':
                total_monthly_expenses += amount * 4  # Approximate 4 weeks in a month
            elif frequency == 'biweekly':
                total_monthly_expenses += amount * 2  # Approximate 2 biweeks in a month
            elif frequency == 'monthly':
                total_monthly_expenses += amount

        # Calculate net worth
        net_worth = total_bank + total_stocks - total_monthly_expenses

        # Insert net worth into the history table
        cursor.execute("""
            INSERT INTO net_worth_history (net_worth)
            VALUES (?)
        """, (net_worth,))
        connection.commit()
        print(f"Net worth recorded: ${net_worth:.2f} on {datetime.today().strftime('%Y-%m-%d')}")
    except sqlite3.Error as e:
        print("Error recording net worth:", e)
    finally:
        connection.close()



def net_worth_trend():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT recorded_date, net_worth FROM net_worth_history ORDER BY recorded_date ASC")
        records = cursor.fetchall()

        print("\n===== Net Worth Trend =====")
        if not records:
            print("No net worth records found. Please record your net worth first.")
        else:
            for record_date, net_worth in records:
                print(f"{record_date}: ${net_worth:.2f}")
        print("===========================")
    except sqlite3.Error as e:
        print("Error generating net worth trend:", e)
    finally:
        connection.close()
