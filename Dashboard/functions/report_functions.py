import sqlite3

def expense_breakdown():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        expenses = cursor.fetchall()

        print("\n===== Expense Breakdown =====")
        for category, total in expenses:
            print(f"{category.capitalize()}: ${total:.2f}")
        print("=============================")
    except sqlite3.Error as e:
        print("Error generating expense breakdown:", e)
    finally:
        connection.close()

def cash_flow_report():
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
