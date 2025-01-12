import sqlite3
from datetime import datetime

def add_salary():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    # Input salary amount
    while True:
        amount_input = input("Enter biweekly salary amount: ")
        try:
            amount = float(amount_input.replace(",", ""))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the salary amount.")
    
    # Input next payment date
    while True:
        next_payment_date = input("Enter next payment date (MM/DD/YYYY): ")
        try:
            valid_date = datetime.strptime(next_payment_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in MM/DD/YYYY format.")
    
    try:
        cursor.execute("""
            INSERT INTO salary (amount, frequency, next_payment_date)
            VALUES (?, ?, ?)
        """, (amount, 'biweekly', valid_date))
        connection.commit()
        print(f"Biweekly salary of ${amount:.2f} added. Next payment date: {next_payment_date}.")
    except sqlite3.Error as e:
        print("Error adding salary:", e)
    finally:
        connection.close()
