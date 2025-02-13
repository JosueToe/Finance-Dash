import sqlite3  # Importing SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)


def edit_bank_account():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
        accounts = cursor.fetchall()
        print("\n===== Bank Accounts =====")
        for account_id, account_type, balance in accounts:
            print(f"ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

        account_id = get_valid_id("\nEnter the ID of the account to edit (or type 'cancel' to go back): ", "bank_accounts", "account_id")
        if account_id is None:
            return

        new_type = get_valid_text("Enter new account type (savings/checking): ").lower()
        if new_type not in ["savings", "checking"]:
            print("Invalid account type. Please enter 'savings' or 'checking'.")
            return

        new_balance = get_valid_float("Enter new account balance: ")
        if new_balance is None:
            return

        cursor.execute("""
            UPDATE bank_accounts SET account_type = ?, balance = ? WHERE account_id = ?
        """, (new_type, new_balance, account_id))
        connection.commit()
        print("Bank account updated successfully!")

    except sqlite3.Error as e:
        print("Error updating bank account:", e)
    finally:
        connection.close()


def delete_bank_account():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
        accounts = cursor.fetchall()
        print("\n===== Bank Accounts =====")
        for account_id, account_type, balance in accounts:
            print(f"ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

        account_id = get_valid_id("\nEnter the ID of the account to delete (or type 'cancel' to go back): ", "bank_accounts", "account_id")
        if account_id is None:
            return

        cursor.execute("DELETE FROM bank_accounts WHERE account_id = ?", (account_id,))
        connection.commit()
        print("Bank account deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting bank account:", e)
    finally:
        connection.close()

def edit_stock():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT stock_id, stock_name, shares, current_value FROM stocks")
        stocks = cursor.fetchall()
        print("\n===== Stocks =====")
        for stock_id, stock_name, shares, current_value in stocks:
            print(f"ID: {stock_id}, Name: {stock_name}, Shares: {shares:.2f}, Value: ${current_value:.2f}")

        stock_id = get_valid_id("\nEnter the ID of the stock to edit (or type 'cancel' to go back): ", "stocks", "stock_id")
        if stock_id is None:
            return

        new_name = get_valid_text("Enter new stock name: ")
        if new_name is None:
            return

        new_shares = get_valid_float("Enter new number of shares: ")
        if new_shares is None:
            return

        new_value = get_valid_float("Enter new current value per share: ")
        if new_value is None:
            return

        cursor.execute("""
            UPDATE stocks SET stock_name = ?, shares = ?, current_value = ? WHERE stock_id = ?
        """, (new_name, new_shares, new_value, stock_id))
        connection.commit()
        print("Stock updated successfully!")

    except sqlite3.Error as e:
        print("Error updating stock:", e)
    finally:
        connection.close()

def delete_stock():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT stock_id, stock_name, shares, current_value FROM stocks")
        stocks = cursor.fetchall()
        print("\n===== Stocks =====")
        for stock_id, stock_name, shares, current_value in stocks:
            print(f"ID: {stock_id}, Name: {stock_name}, Shares: {shares:.2f}, Value: ${current_value:.2f}")

        stock_id = get_valid_id("\nEnter the ID of the stock to delete (or type 'cancel' to go back): ", "stocks", "stock_id")
        if stock_id is None:
            return

        cursor.execute("DELETE FROM stocks WHERE stock_id = ?", (stock_id,))
        connection.commit()
        print("Stock deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting stock:", e)
    finally:
        connection.close()

def edit_expense():
    """
    Edit an existing expense entry with proper validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing expenses
        cursor.execute("SELECT expense_id, name, category, frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        if not expenses:
            print("\nNo expenses found. Add one before editing.")
            return

        print("\n===== Expenses =====")
        for expense_id, name, category, frequency, amount in expenses:
            print(f"ID: {expense_id}, Name: {name}, Category: {category}, Frequency: {frequency}, Amount: ${amount:.2f}")

        # Select valid expense ID to edit
        expense_id = get_valid_id("\nEnter the ID of the expense to edit (or type 'cancel' to go back): ", "expenses", "expense_id")
        if expense_id is None:
            return

        # Get new details
        new_name = get_valid_text("Enter new expense name: ")
        if new_name is None:
            return

        new_category = get_valid_text("Enter new category: ")
        if new_category is None:
            return

        new_frequency = get_valid_frequency("Enter new frequency (weekly/biweekly/monthly): ")
        if new_frequency is None:
            return

        new_amount = get_valid_float("Enter new amount: ")
        if new_amount is None:
            return

        # Update the expense in the database
        cursor.execute("""
            UPDATE expenses
            SET name = ?, category = ?, frequency = ?, amount = ?
            WHERE expense_id = ?
        """, (new_name, new_category, new_frequency, new_amount, expense_id))
        connection.commit()
        print("Expense updated successfully!")

    except sqlite3.Error as e:
        print("Error updating expense:", e)
    finally:
        connection.close()


def delete_expense():
    """
    Delete an expense entry by its ID with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing expenses
        cursor.execute("SELECT expense_id, name, category, frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        if not expenses:
            print("\nNo expenses found. Add one before deleting.")
            return

        print("\n===== Expenses =====")
        for expense_id, name, category, frequency, amount in expenses:
            print(f"ID: {expense_id}, Name: {name}, Category: {category}, Frequency: {frequency}, Amount: ${amount:.2f}")

        # Select valid expense ID to delete
        expense_id = get_valid_id("\nEnter the ID of the expense to delete (or type 'cancel' to go back): ", "expenses", "expense_id")
        if expense_id is None:
            return

        # Delete the selected expense
        cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
        connection.commit()
        print("Expense deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting expense:", e)
    finally:
        connection.close()


def edit_salary():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT salary_id, amount, frequency, next_payment_date FROM salary")
        salaries = cursor.fetchall()
        print("\n===== Salaries =====")
        for salary_id, amount, frequency, next_payment_date in salaries:
            print(f"ID: {salary_id}, Amount: ${amount:.2f}, Frequency: {frequency}, Next Payment: {next_payment_date}")

        salary_id = get_valid_id("\nEnter the ID of the salary to edit (or type 'cancel' to go back): ", "salary", "salary_id")
        if salary_id is None:
            return

        new_amount = get_valid_float("Enter new salary amount: ")
        if new_amount is None:
            return

        new_frequency = get_valid_frequency("Enter new frequency (biweekly/monthly): ")
        if new_frequency is None:
            return

        new_date = get_valid_date("Enter new next payment date (MM/DD/YYYY): ")
        if new_date is None:
            return

        cursor.execute("""
            UPDATE salary SET amount = ?, frequency = ?, next_payment_date = ? WHERE salary_id = ?
        """, (new_amount, new_frequency, new_date, salary_id))
        connection.commit()
        print("Salary updated successfully!")

    except sqlite3.Error as e:
        print("Error updating salary:", e)
    finally:
        connection.close()


def delete_salary():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT salary_id, amount, frequency, next_payment_date FROM salary")
        salaries = cursor.fetchall()
        print("\n===== Salaries =====")
        for salary_id, amount, frequency, next_payment_date in salaries:
            print(f"ID: {salary_id}, Amount: ${amount:.2f}, Frequency: {frequency}, Next Payment: {next_payment_date}")

        salary_id = get_valid_id("\nEnter the ID of the salary to delete (or type 'cancel' to go back): ", "salary", "salary_id")
        if salary_id is None:
            return

        cursor.execute("DELETE FROM salary WHERE salary_id = ?", (salary_id,))
        connection.commit()
        print("Salary deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting salary:", e)
    finally:
        connection.close()

def edit_financial_goal():
    """
    Edit an existing financial goal entry with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT goal_id, net_worth_target, target_date FROM goals")
        goals = cursor.fetchall()
        if not goals:
            print("\nNo financial goals found. Add one before editing.")
            return

        print("\n===== Financial Goals =====")
        for goal_id, net_worth_target, target_date in goals:
            print(f"ID: {goal_id}, Target Net Worth: ${net_worth_target:.2f}, Target Date: {target_date}")

        # Get valid goal ID
        goal_id = get_valid_id("\nEnter the ID of the goal to edit (or type 'cancel' to go back): ", "goals", "goal_id")
        if goal_id is None:
            return

        # Get new values
        new_target = get_valid_float("Enter new target net worth: ")
        if new_target is None:
            return

        new_date = get_valid_date("Enter new target date (MM/DD/YYYY): ")
        if new_date is None:
            return

        cursor.execute("""
            UPDATE goals SET net_worth_target = ?, target_date = ? WHERE goal_id = ?
        """, (new_target, new_date, goal_id))
        connection.commit()
        print("Financial goal updated successfully!")

    except sqlite3.Error as e:
        print("Error updating financial goal:", e)
    finally:
        connection.close()


def delete_financial_goal():
    """
    Delete a financial goal entry by its ID with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT goal_id, net_worth_target, target_date FROM goals")
        goals = cursor.fetchall()
        if not goals:
            print("\nNo financial goals found. Add one before deleting.")
            return

        print("\n===== Financial Goals =====")
        for goal_id, net_worth_target, target_date in goals:
            print(f"ID: {goal_id}, Target Net Worth: ${net_worth_target:.2f}, Target Date: {target_date}")

        # Get valid goal ID
        goal_id = get_valid_id("\nEnter the ID of the goal to delete (or type 'cancel' to go back): ", "goals", "goal_id")
        if goal_id is None:
            return

        cursor.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))
        connection.commit()
        print("Financial goal deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting financial goal:", e)
    finally:
        connection.close()

def edit_crypto():
    """
    Edit an existing cryptocurrency entry with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT crypto_id, coin_name, coins, current_value FROM cryptos")
        cryptos = cursor.fetchall()
        if not cryptos:
            print("\nNo cryptocurrencies found. Add one before editing.")
            return

        print("\n===== Cryptocurrencies =====")
        for crypto_id, coin_name, coins, current_value in cryptos:
            print(f"ID: {crypto_id}, Coin: {coin_name}, Coins: {coins:.4f}, Value: ${current_value:.2f}")

        # Get valid crypto ID
        crypto_id = get_valid_id("\nEnter the ID of the cryptocurrency to edit (or type 'cancel' to go back): ", "cryptos", "crypto_id")
        if crypto_id is None:
            return

        # Get new values
        new_name = get_valid_text("Enter new cryptocurrency name: ")
        if new_name is None:
            return

        new_coins = get_valid_float("Enter new number of coins: ")
        if new_coins is None:
            return

        new_value = get_valid_float("Enter new current value per coin: ")
        if new_value is None:
            return

        cursor.execute("""
            UPDATE cryptos SET coin_name = ?, coins = ?, current_value = ? WHERE crypto_id = ?
        """, (new_name, new_coins, new_value, crypto_id))
        connection.commit()
        print("Cryptocurrency updated successfully!")

    except sqlite3.Error as e:
        print("Error updating cryptocurrency:", e)
    finally:
        connection.close()


def delete_crypto():
    """
    Delete a cryptocurrency entry by its ID with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT crypto_id, coin_name, coins, current_value FROM cryptos")
        cryptos = cursor.fetchall()
        if not cryptos:
            print("\nNo cryptocurrencies found. Add one before deleting.")
            return

        print("\n===== Cryptocurrencies =====")
        for crypto_id, coin_name, coins, current_value in cryptos:
            print(f"ID: {crypto_id}, Coin: {coin_name}, Coins: {coins:.4f}, Value: ${current_value:.2f}")

        # Get valid crypto ID
        crypto_id = get_valid_id("\nEnter the ID of the cryptocurrency to delete (or type 'cancel' to go back): ", "cryptos", "crypto_id")
        if crypto_id is None:
            return

        cursor.execute("DELETE FROM cryptos WHERE crypto_id = ?", (crypto_id,))
        connection.commit()
        print("Cryptocurrency deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting cryptocurrency:", e)
    finally:
        connection.close()
