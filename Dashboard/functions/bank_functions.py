import sqlite3  # Import SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def add_bank_account():
    """
    Add a new bank account with a cancel option.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get account type
        account_type = input("Enter account type (savings/checking) or type 'cancel' to exit: ").lower()
        if account_type == 'cancel':
            print("Returning to main menu...")
            return

        while account_type not in ['savings', 'checking']:
            print("❌ Invalid input. Please enter 'savings' or 'checking'.")
            account_type = input("Enter account type (savings/checking): ").lower()
            if account_type == 'cancel':
                print("Returning to main menu...")
                return

        # Get balance
        balance = get_valid_float("Enter account balance (or type 'cancel' to exit): ")
        if balance is None:
            print("Returning to main menu...")
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO bank_accounts (account_type, balance)
            VALUES (?, ?)
        """, (account_type, balance))
        connection.commit()
        print(f"✅ {account_type.capitalize()} account added successfully with balance ${balance:.2f}.")

    except sqlite3.Error as e:
        print("❌ Error adding bank account:", e)
    finally:
        connection.close()


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