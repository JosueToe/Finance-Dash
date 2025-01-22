import sqlite3

def edit_bank_account():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing accounts
        cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
        accounts = cursor.fetchall()
        print("\n===== Bank Accounts =====")
        for account_id, account_type, balance in accounts:
            print(f"ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

        # Select account to edit
        account_id = input("\nEnter the ID of the account to edit (or type 'cancel' to go back): ")
        if account_id.lower() == 'cancel':
            return

        # Update account details
        new_type = input("Enter new account type (savings/checking): ").lower()
        new_balance = input("Enter new account balance: ")

        cursor.execute("""
            UPDATE bank_accounts
            SET account_type = ?, balance = ?
            WHERE account_id = ?
        """, (new_type, float(new_balance.replace(",", "")), account_id))
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
        # Display existing accounts
        cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
        accounts = cursor.fetchall()
        print("\n===== Bank Accounts =====")
        for account_id, account_type, balance in accounts:
            print(f"ID: {account_id}, Type: {account_type}, Balance: ${balance:.2f}")

        # Select account to delete
        account_id = input("\nEnter the ID of the account to delete (or type 'cancel' to go back): ")
        if account_id.lower() == 'cancel':
            return

        cursor.execute("DELETE FROM bank_accounts WHERE account_id = ?", (account_id,))
        connection.commit()
        print("Bank account deleted successfully!")
    except sqlite3.Error as e:
        print("Error deleting bank account:", e)
    finally:
        connection.close()
