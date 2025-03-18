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

            # Account selection is confirmed, move to editing
            while True:
                new_type = input("Enter new account type (savings/checking) or 'back' to reselect account: ").strip().lower()
                if new_type == "back":
                    break  # Go back to reselecting account ID
                elif new_type not in ["savings", "checking"]:
                    print("❌ Invalid input. Please enter 'savings' or 'checking'.")
                    continue

                new_balance = input("Enter new account balance or 'back' to reselect account: ").strip().lower()
                if new_balance == "back":
                    break  # Go back to reselecting account ID

                try:
                    new_balance = float(new_balance)
                except ValueError:
                    print("❌ Invalid input. Please enter a valid number.")
                    continue

                # Update in database
                cursor.execute("""
                    UPDATE bank_accounts SET account_type = ?, balance = ? WHERE account_id = ?
                """, (new_type, new_balance, account_id))
                connection.commit()
                print("✅ Bank account updated successfully!")
                return  # Exit function after successful update

    except sqlite3.Error as e:
        print("❌ Error updating bank account:", e)
    finally:
        connection.close()


def delete_bank_account():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:  # Allow reselecting ID if user enters "back"
            cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
            accounts = cursor.fetchall()
            print("\n===== Bank Accounts =====")
            for account_id, account_type, balance in accounts:
                print(f"ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

            account_id = input("\nEnter the ID of the account to delete (or type 'back' to return, 'cancel' to exit): ").strip().lower()
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
                confirm = input(f"Are you sure you want to delete account ID {account_id}? (yes/no/back): ").strip().lower()
                if confirm == "back":
                    break  # Go back to reselecting account ID
                elif confirm == "yes":
                    cursor.execute("DELETE FROM bank_accounts WHERE account_id = ?", (account_id,))
                    connection.commit()
                    print("✅ Bank account deleted successfully!")
                    return  # Exit function after successful deletion
                elif confirm == "no":
                    print("❌ Deletion cancelled.")
                    break  # Return to account selection menu
                else:
                    print("❌ Invalid choice. Please type 'yes', 'no', or 'back'.")

    except sqlite3.Error as e:
        print("❌ Error deleting bank account:", e)
    finally:
        connection.close()
