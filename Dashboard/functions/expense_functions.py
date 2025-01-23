import sqlite3  # Importing the SQLite library to interact with the database.

def add_expense():
    # Connect to the database where the finance data is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()  # Cursor is used to execute SQL commands.

    # Prompt the user to input the name of the expense (e.g., "Rent").
    name = input("Enter expense name (e.g., 'Rent', 'Electricity Bill'): ")
    
    # Prompt the user to input the category of the expense (e.g., "rent", "utilities").
    category = input("Enter category (e.g., 'rent', 'utilities', 'subscription'): ").lower()
    
    # Loop until the user provides a valid frequency.
    while True:
        frequency = input("Enter frequency (weekly/biweekly/monthly): ").lower()
        # Check if the frequency is one of the allowed options.
        if frequency in ["weekly", "biweekly", "monthly"]:
            break
        # Display an error message for invalid input.
        print("Invalid frequency. Please enter 'weekly', 'biweekly', or 'monthly'.")
    
    # Loop until the user provides a valid numeric amount.
    while True:
        amount_input = input("Enter the amount: ")
        try:
            # Convert the amount to a float and remove commas if present.
            amount = float(amount_input.replace(",", ""))
            break
        except ValueError:
            # Display an error message if the input is not a valid number.
            print("Invalid input. Please enter a numeric value for the amount.")
    
    try:
        # Insert the new expense into the "expenses" table in the database.
        cursor.execute("""
            INSERT INTO expenses (name, category, frequency, amount)
            VALUES (?, ?, ?, ?)
        """, (name, category, frequency, amount))
        connection.commit()  # Save changes to the database.
        # Confirm the addition of the expense to the user.
        print(f"Expense '{name}' of ${amount:.2f} ({frequency}) added successfully!")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error adding expense:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()
