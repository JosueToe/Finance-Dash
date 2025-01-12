import sqlite3

def add_expense():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    # Input expense name
    name = input("Enter expense name (e.g., 'Rent', 'Electricity Bill'): ")
    
    # Input expense category
    category = input("Enter category (e.g., 'rent', 'utilities', 'subscription'): ").lower()
    
    # Input expense frequency
    while True:
        frequency = input("Enter frequency (weekly/biweekly/monthly): ").lower()
        if frequency in ["weekly", "biweekly", "monthly"]:
            break
        print("Invalid frequency. Please enter 'weekly', 'biweekly', or 'monthly'.")
    
    # Input expense amount
    while True:
        amount_input = input("Enter the amount: ")
        try:
            amount = float(amount_input.replace(",", ""))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the amount.")
    
    try:
        cursor.execute("""
            INSERT INTO expenses (name, category, frequency, amount)
            VALUES (?, ?, ?, ?)
        """, (name, category, frequency, amount))
        connection.commit()
        print(f"Expense '{name}' of ${amount:.2f} ({frequency}) added successfully!")
    except sqlite3.Error as e:
        print("Error adding expense:", e)
    finally:
        connection.close()
