import sqlite3

def add_bank_account():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()
    
    # Input account type
    while True:
        account_type = input("Enter account type (savings/checking): ").lower()
        if account_type in ['savings', 'checking']:
            break
        print("Invalid account type. Please enter 'savings' or 'checking'.")
    
    # Input account balance
    while True:
        balance_input = input("Enter account balance: ")
        try:
            balance = float(balance_input.replace(",", ""))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the balance.")
    
    try:
        cursor.execute("""
            INSERT INTO bank_accounts (account_type, balance)
            VALUES (?, ?)
        """, (account_type, balance))
        connection.commit()
        print(f"{account_type.capitalize()} account added successfully with balance ${balance:.2f}.")
    except sqlite3.Error as e:
        print("Error adding bank account:", e)
    finally:
        connection.close()
