import sqlite3
from datetime import datetime

def add_financial_goal():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    # Input target net worth
    while True:
        target_input = input("Enter your target net worth goal: ")
        try:
            target_net_worth = float(target_input.replace(",", ""))
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value for the goal.")
    
    # Input target date
    while True:
        target_date = input("Enter the target date to achieve this goal (MM/DD/YYYY): ")
        try:
            valid_date = datetime.strptime(target_date, "%m/%d/%Y").strftime("%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date format. Please enter the date in MM/DD/YYYY format.")
    
    try:
        cursor.execute("""
            INSERT INTO goals (net_worth_target, target_date)
            VALUES (?, ?)
        """, (target_net_worth, valid_date))
        connection.commit()
        print(f"Goal of ${target_net_worth:.2f} by {target_date} added successfully!")
    except sqlite3.Error as e:
        print("Error adding goal:", e)
    finally:
        connection.close()
