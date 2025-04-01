import sqlite3  # Importing SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

import sqlite3
from functions.validate_functions import get_valid_float

def add_expense():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    steps = ['name', 'category', 'frequency', 'amount']
    data = {}

    try:
        step_index = 0
        while step_index < len(steps):
            step = steps[step_index]

            if step == 'name':
                name = input("Enter expense name (or 'back'/'cancel'): ").strip()
                if name.lower() == 'cancel':
                    print("❌ Operation cancelled.")
                    return
                if name.lower() == 'back':
                    print("🔙 Nothing to go back to.")
                    continue
                if name:
                    data['name'] = name.capitalize()
                    step_index += 1
                else:
                    print("❌ Name cannot be empty.")

            elif step == 'category':
                category = input("Enter expense category (or 'back'/'cancel'): ").strip()
                if category.lower() == 'cancel':
                    print("❌ Operation cancelled.")
                    return
                if category.lower() == 'back':
                    step_index -= 1
                    continue
                if category:
                    data['category'] = category.capitalize()
                    step_index += 1
                else:
                    print("❌ Category cannot be empty.")

            elif step == 'frequency':
                frequency = input("Enter frequency (weekly/biweekly/monthly) or 'back'/'cancel': ").strip().lower()
                if frequency == 'cancel':
                    print("❌ Operation cancelled.")
                    return
                if frequency == 'back':
                    step_index -= 1
                    continue
                if frequency in ['weekly', 'biweekly', 'monthly']:
                    data['frequency'] = frequency
                    step_index += 1
                else:
                    print("❌ Invalid frequency. Choose from weekly, biweekly, or monthly.")

            elif step == 'amount':
                amount_input = input("Enter amount or 'back'/'cancel': ").replace(",", "").strip()
                if amount_input.lower() == 'cancel':
                    print("❌ Operation cancelled.")
                    return
                if amount_input.lower() == 'back':
                    step_index -= 1
                    continue
                try:
                    data['amount'] = float(amount_input)
                    step_index += 1
                except ValueError:
                    print("❌ Invalid number. Please enter a valid amount.")

        cursor.execute("""
            INSERT INTO expenses (name, category, frequency, amount)
            VALUES (?, ?, ?, ?)
        """, (data['name'], data['category'], data['frequency'], data['amount']))
        connection.commit()
        print(f"✅ Expense '{data['name']}' added successfully!")

    except sqlite3.Error as e:
        print("❌ Error adding expense:", e)
    finally:
        connection.close()


import sqlite3
from functions.validate_functions import get_valid_id

def edit_expense():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:
            # Show current expenses
            cursor.execute("SELECT expense_id, name, category, frequency, amount FROM expenses")
            expenses = cursor.fetchall()
            print("\n===== Expenses =====")
            for expense_id, name, category, frequency, amount in expenses:
                print(f"ID: {expense_id}, Name: {name}, Category: {category}, Frequency: {frequency}, Amount: ${amount:.2f}")

            expense_id_input = input("\nEnter the ID of the expense to edit (or type 'back'/'cancel'): ").strip().lower()
            if expense_id_input == 'cancel':
                print("Returning to main menu...")
                return
            if expense_id_input == 'back':
                continue
            if not expense_id_input.isdigit():
                print("❌ Invalid input. Please enter a numeric ID.")
                continue

            expense_id = int(expense_id_input)
            cursor.execute("SELECT * FROM expenses WHERE expense_id = ?", (expense_id,))
            if not cursor.fetchone():
                print("❌ No expense found with that ID.")
                continue

            steps = ['name', 'category', 'frequency', 'amount']
            data = {}
            index = 0

            while index < len(steps):
                step = steps[index]

                if step == 'name':
                    user_input = input("Enter new expense name or 'back': ").strip()
                    if user_input.lower() == 'back':
                        print("Returning to ID selection...")
                        break
                    data['name'] = user_input.capitalize()
                    index += 1

                elif step == 'category':
                    user_input = input("Enter new category or 'back': ").strip()
                    if user_input.lower() == 'back':
                        index -= 1
                        continue
                    data['category'] = user_input.capitalize()
                    index += 1

                elif step == 'frequency':
                    user_input = input("Enter new frequency (weekly/biweekly/monthly) or 'back': ").strip().lower()
                    if user_input == 'back':
                        index -= 1
                        continue
                    if user_input not in ['weekly', 'biweekly', 'monthly']:
                        print("❌ Invalid frequency. Please choose from weekly, biweekly, monthly.")
                        continue
                    data['frequency'] = user_input
                    index += 1

                elif step == 'amount':
                    user_input = input("Enter new amount or 'back': ").strip().lower()
                    if user_input == 'back':
                        index -= 1
                        continue
                    try:
                        data['amount'] = float(user_input.replace(',', ''))
                        index += 1
                    except ValueError:
                        print("❌ Invalid amount.")
                        continue

            if len(data) == 4:
                cursor.execute("""
                    UPDATE expenses
                    SET name = ?, category = ?, frequency = ?, amount = ?
                    WHERE expense_id = ?
                """, (data['name'], data['category'], data['frequency'], data['amount'], expense_id))
                connection.commit()
                print("✅ Expense updated successfully!")
                return

    except sqlite3.Error as e:
        print("❌ Error updating expense:", e)
    finally:
        connection.close()



def delete_expense():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:
            cursor.execute("SELECT expense_id, name, category, frequency, amount FROM expenses")
            expenses = cursor.fetchall()
            print("\n===== Expenses =====")
            for expense_id, name, category, frequency, amount in expenses:
                print(f"ID: {expense_id}, Name: {name}, Category: {category}, Frequency: {frequency}, Amount: ${amount:.2f}")

            expense_id = input("\nEnter the ID of the expense to delete (or 'back'/'cancel'): ").strip().lower()
            if expense_id == 'cancel':
                print("Returning to main menu...")
                return
            if expense_id == 'back':
                continue
            if not expense_id.isdigit():
                print("❌ Invalid ID.")
                continue

            expense_id = int(expense_id)
            cursor.execute("SELECT * FROM expenses WHERE expense_id = ?", (expense_id,))
            if not cursor.fetchone():
                print("❌ No expense found with that ID.")
                continue

            confirm = input(f"Are you sure you want to delete expense ID {expense_id}? (yes/no/back): ").strip().lower()
            if confirm == 'cancel':
                print("Returning to main menu...")
                return
            if confirm == 'back':
                continue
            if confirm != 'yes':
                print("❌ Deletion cancelled.")
                continue

            cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
            connection.commit()
            print("✅ Expense deleted successfully.")
            break

    except sqlite3.Error as e:
        print("❌ Error deleting expense:", e)
    finally:
        connection.close()
