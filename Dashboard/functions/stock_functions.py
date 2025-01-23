import sqlite3  # Import SQLite library to interact with the database.

def add_stock():
    # Connect to the database where stock data is stored.
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()  # Cursor is used to execute SQL commands.

    # Prompt the user to input the stock name (e.g., "Apple").
    stock_name = input("Enter stock name: ")

    # Loop until the user provides a valid number of shares.
    while True:
        shares_input = input("Enter number of shares: ")  # Prompt for the number of shares.
        try:
            # Convert the input to a float, removing commas if present.
            shares = float(shares_input.replace(",", ""))
            break  # Exit the loop if input is valid.
        except ValueError:
            # Show an error message for invalid input.
            print("Invalid input. Please enter a numeric value for shares.")

    # Loop until the user provides a valid current value per share.
    while True:
        current_value_input = input("Enter current value per share: ")  # Prompt for the share value.
        try:
            # Convert the input to a float, removing commas if present.
            current_value = float(current_value_input.replace(",", ""))
            break  # Exit the loop if input is valid.
        except ValueError:
            # Show an error message for invalid input.
            print("Invalid input. Please enter a numeric value for the current value per share.")

    try:
        # Insert the stock data (name, shares, and current value) into the "stocks" table in the database.
        cursor.execute("""
            INSERT INTO stocks (stock_name, shares, current_value)
            VALUES (?, ?, ?)
        """, (stock_name, shares, current_value))
        connection.commit()  # Save changes to the database.
        # Confirm that the stock was successfully added.
        print(f"Added {shares} shares of {stock_name} at ${current_value:.2f} per share.")
    except sqlite3.Error as e:
        # Handle and print any database-related errors.
        print("Error adding stock:", e)
    finally:
        # Ensure the database connection is always closed.
        connection.close()
