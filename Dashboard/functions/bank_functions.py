import sqlite3  # Import SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

import sqlite3

def add_bank_account():
    """
    Add a new bank account with full back navigation support.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    steps = ['account_type', 'balance']
    data = {}

    try:
        step_index = 0
        while step_index < len(steps):
            step = steps[step_index]

            if step == 'account_type':
                user_input = input("Enter account type (savings/checking) or type 'back' or 'cancel': ").lower()
                if user_input == 'cancel':
                    print("❌ Operation cancelled. Returning to main menu...")
                    return
                if user_input == 'back':
                    print("🔙 Going back... (nothing to go back to)")
                    continue
                if user_input in ['savings', 'checking']:
                    data['account_type'] = user_input
                    step_index += 1
                else:
                    print("❌ Invalid input. Please enter 'savings' or 'checking'.")

            elif step == 'balance':
                user_input = input("Enter account balance or type 'back' or 'cancel': ").replace(",", "").strip()
                if user_input.lower() == 'cancel':
                    print("❌ Operation cancelled. Returning to main menu...")
                    return
                if user_input.lower() == 'back':
                    step_index -= 1
                    continue
                try:
                    data['balance'] = float(user_input)
                    step_index += 1
                except ValueError:
                    print("❌ Invalid input. Please enter a valid number.")

        # Insert into DB
        cursor.execute("""
            INSERT INTO bank_accounts (account_type, balance)
            VALUES (?, ?)
        """, (data['account_type'], data['balance']))
        connection.commit()
        print(f"✅ {data['account_type'].capitalize()} account added successfully with balance ${data['balance']:.2f}.")

    except sqlite3.Error as e:
        print("❌ Error adding bank account:", e)
    finally:
        connection.close()



def edit_bank_account():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:  # Allow reselecting ID if user enters "back"
            cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
            accounts = cursor.fetchall()
            print("\n===== Bank Accounts =====")
            for account_id, account_type, balance in accounts:
                print(f"ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

            account_id = input("\nEnter the ID of the account to edit (or type 'back' to return, 'cancel' to exit): ").strip().lower()
            if account_id == "cancel":
                print("Returning to main menu...")
                return
            elif account_id == "back":
                continue  # Reload account list to allow re-selection

            if not account_id.isdigit():
                print("❌ Invalid input. Please enter a valid numeric ID.")
                continue

            account_id = int(account_id)

            cursor.execute("SELECT * FROM bank_accounts WHERE account_id = ?", (account_id,))
            if not cursor.fetchone():
                print("❌ Invalid ID. Please select a valid account ID.")
                continue  # Re-ask for input

            while True:
                new_type = input("Enter new account type (savings/checking) or 'back' to reselect ID: ").strip().lower()
                if new_type == "back":
                    break  # Go back to reselecting account ID
                elif new_type not in ["savings", "checking"]:
                    print("❌ Invalid input. Please enter 'savings' or 'checking'.")
                    continue

                while True:
                    new_balance = input("Enter new account balance or 'back' to reselect account type: ").strip().lower()
                    if new_balance == "back":
                        break  # Go back to account type selection

                    try:
                        new_balance = float(new_balance)
                        cursor.execute("""
                            UPDATE bank_accounts SET account_type = ?, balance = ? WHERE account_id = ?
                        """, (new_type, new_balance, account_id))
                        connection.commit()
                        print("✅ Bank account updated successfully!")
                        return  # Exit function after successful update
                    except ValueError:
                        print("❌ Invalid input. Please enter a valid number.")
                        continue  # Stay in balance input step

    except sqlite3.Error as e:
        print("❌ Error updating bank account:", e)
    finally:
        connection.close()



import sqlite3
from functions.validate_functions import get_valid_id

def delete_bank_account():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:
            # Show available accounts
            cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
            accounts = cursor.fetchall()
            print("\n===== Bank Accounts =====")
            for account_id, account_type, balance in accounts:
                print(f"ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

            # Ask for ID to delete
            account_id = input("\nEnter the ID of the account to delete (or type 'back' to return, 'cancel' to exit): ").lower().strip()

            if account_id == 'cancel':
                print("Returning to main menu...")
                return
            elif account_id == 'back':
                continue
            elif not account_id.isdigit():
                print("❌ Invalid input. Please enter a valid numeric ID.")
                continue

            # Check if account exists
            cursor.execute("SELECT * FROM bank_accounts WHERE account_id = ?", (account_id,))
            result = cursor.fetchone()

            if not result:
                print("❌ No account found with that ID.")
                continue

            # Confirm deletion
            confirm = input(f"Are you sure you want to delete account ID {account_id}? (yes/no/back): ").strip().lower()
            if confirm == 'cancel':
                print("Returning to main menu...")
                return
            elif confirm == 'back':
                continue
            elif confirm != 'yes':
                print("❌ Deletion cancelled.")
                continue

            # Delete and confirm
            cursor.execute("DELETE FROM bank_accounts WHERE account_id = ?", (account_id,))
            connection.commit()
            print(f"✅ Account ID {account_id} deleted successfully.")
            break

    except sqlite3.Error as e:
        print("❌ Error deleting bank account:", e)

    finally:
        connection.close()

