import sqlite3

def display_dashboard():
    """
    Display the financial dashboard with total balances, stocks, crypto, and net worth.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Initialize the dashboard data dictionary
        dashboard_data = {}

        # Fetch total bank balances
        cursor.execute("SELECT SUM(balance) FROM bank_accounts")
        dashboard_data['total_bank'] = cursor.fetchone()[0] or 0.0

        # Fetch total stock value
        cursor.execute("SELECT SUM(shares * current_value) FROM stocks")
        dashboard_data['total_stocks'] = cursor.fetchone()[0] or 0.0

        # Fetch total cryptocurrency value
        cursor.execute("SELECT SUM(coins * current_value) FROM cryptos")
        dashboard_data['total_crypto'] = cursor.fetchone()[0] or 0.0

        # Fetch monthly income
        cursor.execute("SELECT SUM(amount) FROM salary")
        dashboard_data['total_monthly_income'] = (cursor.fetchone()[0] or 0.0) * 2  # Assuming biweekly salary

        # Fetch monthly expenses
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
        dashboard_data['total_monthly_expenses'] = total_monthly_expenses

        # Fetch financial goal
        cursor.execute("SELECT net_worth_target, target_date FROM goals LIMIT 1")
        goal = cursor.fetchone()
        if goal:
            net_worth_target, target_date = goal
            dashboard_data['net_worth_target'] = net_worth_target

            # Calculate progress and remaining days
            total_net_worth = dashboard_data['total_bank'] + dashboard_data['total_stocks'] + dashboard_data['total_crypto']
            dashboard_data['total_net_worth'] = total_net_worth
            dashboard_data['progress_percentage'] = (total_net_worth / net_worth_target) * 100

            from datetime import datetime
            today = datetime.today().date()
            target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            days_remaining = (target_date - today).days
            dashboard_data['days_remaining'] = days_remaining
        else:
            dashboard_data['net_worth_target'] = None
            dashboard_data['total_net_worth'] = dashboard_data['total_bank'] + dashboard_data['total_stocks'] + dashboard_data['total_crypto']

        # Display the dashboard
        print("\n===== Financial Dashboard =====")
        print(f"Total Bank Balances: ${dashboard_data['total_bank']:.2f}")
        print(f"Total Stock Value: ${dashboard_data['total_stocks']:.2f}")
        print(f"Total Cryptocurrency Value: ${dashboard_data['total_crypto']:.2f}")  
        print(f"Total Net Worth: ${dashboard_data['total_net_worth']:.2f}")
        print(f"Total Monthly Income: ${dashboard_data['total_monthly_income']:.2f}")
        print(f"Total Monthly Expenses: ${dashboard_data['total_monthly_expenses']:.2f}")
        print(f"Net Monthly Cash Flow: ${dashboard_data['total_monthly_income'] - dashboard_data['total_monthly_expenses']:.2f}")

        # Display financial goal progress if set
        if dashboard_data['net_worth_target'] is not None:
            print("\nFinancial Goal:")
            print(f"  Target Net Worth: ${dashboard_data['net_worth_target']:.2f}")
            print(f"  Current Progress: {dashboard_data['progress_percentage']:.2f}%")
            print(f"  Days Remaining: {dashboard_data['days_remaining']} days")
            print("===============================")
        else:
            print("\nNo financial goals set.")

    except sqlite3.Error as e:
        print("Error displaying dashboard:", e)

    finally:
        connection.close()
