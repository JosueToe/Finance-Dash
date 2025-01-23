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
