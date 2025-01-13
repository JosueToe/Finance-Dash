import sqlite3
from datetime import datetime

def calculate_net_worth():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Total bank balances
        cursor.execute("SELECT SUM(balance) FROM bank_accounts")
        total_bank = cursor.fetchone()[0] or 0.0

        # Total stock value
        cursor.execute("SELECT SUM(shares * current_value) FROM stocks")
        total_stocks = cursor.fetchone()[0] or 0.0

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

        # Total monthly income
        cursor.execute("SELECT amount FROM salary")
        salaries = cursor.fetchall()
        total_monthly_income = sum([salary[0] * 2 for salary in salaries])  # Assuming biweekly salary

        # Net worth calculation
        total_net_worth = total_bank + total_stocks - total_monthly_expenses

        # Financial goal progress
        cursor.execute("SELECT net_worth_target, target_date FROM goals ORDER BY goal_id DESC LIMIT 1")
        goal = cursor.fetchone()
        if goal:
            net_worth_target, target_date = goal
            progress_percentage = (total_net_worth / net_worth_target) * 100 if net_worth_target else 0
            days_remaining = (datetime.strptime(target_date, "%Y-%m-%d").date() - datetime.today().date()).days
        else:
            net_worth_target = None
            progress_percentage = None
            days_remaining = None

        # Return data as a dictionary
        return {
            "total_bank": total_bank,
            "total_stocks": total_stocks,
            "total_net_worth": total_net_worth,
            "total_monthly_income": total_monthly_income,
            "total_monthly_expenses": total_monthly_expenses,
            "net_worth_target": net_worth_target,
            "progress_percentage": progress_percentage,
            "days_remaining": days_remaining,
        }

    except sqlite3.Error as e:
        print("Error retrieving dashboard data:", e)
        return None
    finally:
        connection.close()


def display_dashboard():
    dashboard_data = calculate_net_worth()
    if dashboard_data is None:
        print("Unable to display dashboard due to an error.")
        return

    print("\n===== Financial Dashboard =====")
    print(f"Total Bank Balances: ${dashboard_data['total_bank']:.2f}")
    print(f"Total Stock Value: ${dashboard_data['total_stocks']:.2f}")
    print(f"Total Net Worth: ${dashboard_data['total_net_worth']:.2f}")
    print(f"Total Monthly Income: ${dashboard_data['total_monthly_income']:.2f}")
    print(f"Total Monthly Expenses: ${dashboard_data['total_monthly_expenses']:.2f}")
    print(f"Net Monthly Cash Flow: ${dashboard_data['total_monthly_income'] - dashboard_data['total_monthly_expenses']:.2f}")

    if dashboard_data['net_worth_target'] is not None:
        print("\nFinancial Goal:")
        print(f"  Target Net Worth: ${dashboard_data['net_worth_target']:.2f}")
        print(f"  Current Progress: {dashboard_data['progress_percentage']:.2f}%")
        print(f"  Days Remaining: {dashboard_data['days_remaining']} days")
    else:
        print("\nNo financial goals set.")

    print("===============================")
