import sqlite3  # Import SQLite library to interact with the database.

def add_bank_account():
    # Connect to the database where bank account data is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()  # Cursor is used to execute SQL commands.

    # Loop until the user provides a valid account type (savings or checking).
    while True:
        account_type = input("Enter account type (savings/checking): ").lower()  # Prompt for the account type.
        if account_type in ['savings', 'checking']:  # Check if the input is valid.
            break  # Exit the loop if input is valid.
        # Show an error message for invalid input.
        print("Invalid account type. Please enter 'savings' or 'checking'.")

    # Loop until the user provides a valid numeric value for the account balance.
    while True:
        balance_input = input("Enter account balance: ")  # Prompt for the account balance.
        try:
            # Convert the input to a float, removing commas if present.
            balance = float(balance_input.replace(",", ""))
            break  # Exit the loop if input is valid.
        except ValueError:
            # Show an error message for invalid input.
            print("Invalid input. Please enter a numeric value for the balance.")

    try:
        # Insert the bank account data (type and balance) into the "bank_accounts" table in the database.
        cursor.execute("""
            INSERT INTO bank_accounts (account_type, balance)
            VALUES (?, ?)
        """, (account_type, balance))
        connection.commit()  # Save changes to the database.
        # Confirm that the bank account was successfully added.
        print(f"{account_type.capitalize()} account added successfully with balance ${balance:.2f}.")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error adding bank account:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()