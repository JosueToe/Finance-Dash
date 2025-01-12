import sqlite3

def add_stock():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    # Input stock name
    stock_name = input("Enter stock name: ")
    
    # Input number of shares
    while True:
        shares_input = input("Enter number of shares: ")
        try:
            shares = float(shares_input.replace(",", ""))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for shares.")
    
    # Input current value per share
    while True:
        current_value_input = input("Enter current value per share: ")
        try:
            current_value = float(current_value_input.replace(",", ""))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the current value per share.")
    
    try:
        cursor.execute("""
            INSERT INTO stocks (stock_name, shares, current_value)
            VALUES (?, ?, ?)
        """, (stock_name, shares, current_value))
        connection.commit()
        print(f"Added {shares} shares of {stock_name} at ${current_value:.2f} per share.")
    except sqlite3.Error as e:
        print("Error adding stock:", e)
    finally:
        connection.close()
