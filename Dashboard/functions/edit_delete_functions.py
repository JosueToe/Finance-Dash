import sqlite3  # Importing the SQLite library to interact with the database.

def edit_bank_account():
    # Connect to the database where the finance data is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()  # Cursor is used to execute SQL commands.

    try:
        # Fetch and display all existing bank accounts.
        cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
        accounts = cursor.fetchall()  # Fetch all rows from the query result.
        print("\n===== Bank Accounts =====")
        for account_id, account_type, balance in accounts:
            print(f"ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

        # Ask the user for the ID of the account they want to edit.
        account_id = input("\nEnter the ID of the account to edit (or type 'cancel' to go back): ")
        if account_id.lower() == 'cancel':  # Allow the user to cancel the action.
            return

        # Collect new details for the selected bank account.
        new_type = input("Enter new account type (savings/checking): ").lower()
        new_balance = input("Enter new account balance: ")

        # Update the bank account details in the database.
        cursor.execute("""
            UPDATE bank_accounts
            SET account_type = ?, balance = ?
            WHERE account_id = ?
        """, (new_type, float(new_balance.replace(",", "")), account_id))  # Replace commas in numbers before conversion.
        connection.commit()  # Save changes to the database.
        print("Bank account updated successfully!")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error updating bank account:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()

def delete_bank_account():
    # Connect to the database where the finance data is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()  # Cursor is used to execute SQL commands.

    try:
        # Fetch and display all existing bank accounts.
        cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
        accounts = cursor.fetchall()  # Fetch all rows from the query result.
        print("\n===== Bank Accounts =====")
        for account_id, account_type, balance in accounts:
            print(f"ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

        # Ask the user for the ID of the account they want to delete.
        account_id = input("\nEnter the ID of the account to delete (or type 'cancel' to go back): ")
        if account_id.lower() == 'cancel':  # Allow the user to cancel the action.
            return

        # Delete the selected bank account from the database.
        cursor.execute("DELETE FROM bank_accounts WHERE account_id = ?", (account_id,))
        connection.commit()  # Save changes to the database.
        print("Bank account deleted successfully!")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error deleting bank account:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()

def edit_stock():
    """
    Edit an existing stock entry.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing stocks
        cursor.execute("SELECT stock_id, stock_name, shares, current_value FROM stocks")
        stocks = cursor.fetchall()
        print("\n===== Stocks =====")
        for stock_id, stock_name, shares, current_value in stocks:
            print(f"ID: {stock_id}, Name: {stock_name}, Shares: {shares:.2f}, Value: ${current_value:.2f}")

        # Select stock to edit
        stock_id = input("\nEnter the ID of the stock to edit (or type 'cancel' to go back): ")
        if stock_id.lower() == 'cancel':
            return

        # Update stock details
        new_name = input("Enter new stock name: ").capitalize()
        new_shares = input("Enter new number of shares: ")
        new_value = input("Enter new current value per share: ")

        cursor.execute("""
            UPDATE stocks
            SET stock_name = ?, shares = ?, current_value = ?
            WHERE stock_id = ?
        """, (new_name, float(new_shares), float(new_value), stock_id))
        connection.commit()
        print("Stock updated successfully!")
    except sqlite3.Error as e:
        print("Error updating stock:", e)
    finally:
        connection.close()


def delete_stock():
    """
    Delete a stock entry by its ID.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing stocks
        cursor.execute("SELECT stock_id, stock_name, shares, current_value FROM stocks")
        stocks = cursor.fetchall()
        print("\n===== Stocks =====")
        for stock_id, stock_name, shares, current_value in stocks:
            print(f"ID: {stock_id}, Name: {stock_name}, Shares: {shares:.2f}, Value: ${current_value:.2f}")

        # Select stock to delete
        stock_id = input("\nEnter the ID of the stock to delete (or type 'cancel' to go back): ")
        if stock_id.lower() == 'cancel':
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
    Edit an existing expense entry.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing expenses
        cursor.execute("SELECT expense_id, name, category, frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        print("\n===== Expenses =====")
        for expense_id, name, category, frequency, amount in expenses:
            print(f"ID: {expense_id}, Name: {name}, Category: {category}, Frequency: {frequency}, Amount: ${amount:.2f}")

        # Select expense to edit
        expense_id = input("\nEnter the ID of the expense to edit (or type 'cancel' to go back): ")
        if expense_id.lower() == 'cancel':
            return

        # Update expense details
        new_name = input("Enter new expense name: ").capitalize()
        new_category = input("Enter new category: ").capitalize()
        new_frequency = input("Enter new frequency (weekly/biweekly/monthly): ").lower()
        new_amount = input("Enter new amount: ")

        cursor.execute("""
            UPDATE expenses
            SET name = ?, category = ?, frequency = ?, amount = ?
            WHERE expense_id = ?
        """, (new_name, new_category, new_frequency, float(new_amount), expense_id))
        connection.commit()
        print("Expense updated successfully!")
    except sqlite3.Error as e:
        print("Error updating expense:", e)
    finally:
        connection.close()


def delete_expense():
    """
    Delete an expense entry by its ID.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing expenses
        cursor.execute("SELECT expense_id, name, category, frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        print("\n===== Expenses =====")
        for expense_id, name, category, frequency, amount in expenses:
            print(f"ID: {expense_id}, Name: {name}, Category: {category}, Frequency: {frequency}, Amount: ${amount:.2f}")

        # Select expense to delete
        expense_id = input("\nEnter the ID of the expense to delete (or type 'cancel' to go back): ")
        if expense_id.lower() == 'cancel':
            return

        cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
        connection.commit()
        print("Expense deleted successfully!")
    except sqlite3.Error as e:
        print("Error deleting expense:", e)
    finally:
        connection.close()

def edit_salary():
    """
    Edit an existing salary entry.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing salaries
        cursor.execute("SELECT salary_id, amount, frequency, next_payment_date FROM salary")
        salaries = cursor.fetchall()
        print("\n===== Salaries =====")
        for salary_id, amount, frequency, next_payment_date in salaries:
            print(f"ID: {salary_id}, Amount: ${amount:.2f}, Frequency: {frequency}, Next Payment: {next_payment_date}")

        # Select salary to edit
        salary_id = input("\nEnter the ID of the salary to edit (or type 'cancel' to go back): ")
        if salary_id.lower() == 'cancel':
            return

        # Update salary details
        new_amount = input("Enter new salary amount: ")
        new_frequency = input("Enter new frequency (biweekly/monthly): ").lower()
        new_date = input("Enter new next payment date (YYYY-MM-DD): ")

        cursor.execute("""
            UPDATE salary
            SET amount = ?, frequency = ?, next_payment_date = ?
            WHERE salary_id = ?
        """, (float(new_amount), new_frequency, new_date, salary_id))
        connection.commit()
        print("Salary updated successfully!")
    except sqlite3.Error as e:
        print("Error updating salary:", e)
    finally:
        connection.close()


def delete_salary():
    """
    Delete a salary entry by its ID.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing salaries
        cursor.execute("SELECT salary_id, amount, frequency, next_payment_date FROM salary")
        salaries = cursor.fetchall()
        print("\n===== Salaries =====")
        for salary_id, amount, frequency, next_payment_date in salaries:
            print(f"ID: {salary_id}, Amount: ${amount:.2f}, Frequency: {frequency}, Next Payment: {next_payment_date}")

        # Select salary to delete
        salary_id = input("\nEnter the ID of the salary to delete (or type 'cancel' to go back): ")
        if salary_id.lower() == 'cancel':
            return

        cursor.execute("DELETE FROM salary WHERE salary_id = ?", (salary_id,))
        connection.commit()
        print("Salary deleted successfully!")
    except sqlite3.Error as e:
        print("Error deleting salary:", e)
    finally:
        connection.close()

import sqlite3

def edit_financial_goal():
    """
    Edit an existing financial goal entry.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing goals
        cursor.execute("SELECT goal_id, net_worth_target, target_date FROM goals")
        goals = cursor.fetchall()
        print("\n===== Financial Goals =====")
        for goal_id, net_worth_target, target_date in goals:
            print(f"ID: {goal_id}, Target Net Worth: ${net_worth_target:.2f}, Target Date: {target_date}")

        # Select goal to edit
        goal_id = input("\nEnter the ID of the goal to edit (or type 'cancel' to go back): ")
        if goal_id.lower() == 'cancel':
            return

        # Update goal details
        new_target = input("Enter new target net worth: ").replace(",", "")
        new_date = input("Enter new target date (YYYY-MM-DD): ")

        cursor.execute("""
            UPDATE goals
            SET net_worth_target = ?, target_date = ?
            WHERE goal_id = ?
        """, (float(new_target), new_date, goal_id))
        connection.commit()
        print("Financial goal updated successfully!")
    except ValueError:
        print("Invalid input. Please enter a valid number for the target net worth.")
    except sqlite3.Error as e:
        print("Error updating financial goal:", e)
    finally:
        connection.close()



def delete_financial_goal():
    """
    Delete a financial goal entry by its ID.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing goals
        cursor.execute("SELECT goal_id, net_worth_target, target_date FROM goals")
        goals = cursor.fetchall()
        print("\n===== Financial Goals =====")
        for goal_id, net_worth_target, target_date in goals:
            print(f"ID: {goal_id}, Target Net Worth: ${net_worth_target:.2f}, Target Date: {target_date}")

        # Select goal to delete
        goal_id = input("\nEnter the ID of the goal to delete (or type 'cancel' to go back): ")
        if goal_id.lower() == 'cancel':
            return

        cursor.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))
        connection.commit()
        print("Financial goal deleted successfully!")
    except sqlite3.Error as e:
        print("Error deleting financial goal:", e)
    finally:
        connection.close()


import sqlite3

def edit_crypto():
    """
    Edit an existing cryptocurrency entry.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing cryptocurrencies
        cursor.execute("SELECT crypto_id, coin_name, coins, current_value FROM cryptos")
        cryptos = cursor.fetchall()
        print("\n===== Cryptocurrencies =====")
        for crypto_id, coin_name, coins, current_value in cryptos:
            print(f"ID: {crypto_id}, Coin: {coin_name}, Coins: {coins:.2f}, Value: ${current_value:.2f}")

        # Select crypto to edit
        crypto_id = input("\nEnter the ID of the cryptocurrency to edit (or type 'cancel' to go back): ")
        if crypto_id.lower() == 'cancel':
            return

        # Get new values from the user
        new_name = input("Enter new cryptocurrency name: ").capitalize()
        new_coins = input("Enter new number of coins: ").replace(",", "")
        new_value = input("Enter new current value per coin: ").replace(",", "")

        # Convert inputs to floats after removing commas
        new_coins = float(new_coins)
        new_value = float(new_value)

        cursor.execute("""
            UPDATE cryptos
            SET coin_name = ?, coins = ?, current_value = ?
            WHERE crypto_id = ?
        """, (new_name, new_coins, new_value, crypto_id))
        connection.commit()
        print("Cryptocurrency updated successfully!")
    except ValueError:
        print("Invalid input. Please enter valid numeric values.")
    except sqlite3.Error as e:
        print("Error updating cryptocurrency:", e)
    finally:
        connection.close()




def delete_crypto():
    """
    Delete a cryptocurrency entry by its ID.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing cryptocurrencies
        cursor.execute("SELECT crypto_id, coin_name, coins, current_value FROM cryptos")
        cryptos = cursor.fetchall()
        print("\n===== Cryptocurrencies =====")
        for crypto_id, coin_name, coins, current_value in cryptos:
            print(f"ID: {crypto_id}, Coin: {coin_name}, Coins: {coins:.2f}, Value: ${current_value:.2f}")

        # Select crypto to delete
        crypto_id = input("\nEnter the ID of the cryptocurrency to delete (or type 'cancel' to go back): ")
        if crypto_id.lower() == 'cancel':
            return

        cursor.execute("DELETE FROM cryptos WHERE crypto_id = ?", (crypto_id,))
        connection.commit()
        print("Cryptocurrency deleted successfully!")
    except sqlite3.Error as e:
        print("Error deleting cryptocurrency:", e)
    finally:
        connection.close()
