import sqlite3  # Importing SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def add_expense():
    """
    Add a new expense entry with validated input.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid expense name
        name = get_valid_text("Enter expense name (e.g., 'Rent', 'Electricity Bill'): ")
        if name is None:
            return  # User chose to cancel

        # Get valid category
        category = get_valid_text("Enter category (e.g., 'rent', 'utilities', 'subscription'): ")
        if category is None:
            return

        # Get valid frequency
        frequency = get_valid_frequency("Enter frequency (weekly/biweekly/monthly): ")
        if frequency is None:
            return

        # Get valid amount
        amount = get_valid_float("Enter the amount: ")
        if amount is None:
            return

        # Insert into database
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

def edit_expense():
    """
    Edit an existing expense entry with proper validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing expenses
        cursor.execute("SELECT expense_id, name, category, frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        if not expenses:
            print("\nNo expenses found. Add one before editing.")
            return

        print("\n===== Expenses =====")
        for expense_id, name, category, frequency, amount in expenses:
            print(f"ID: {expense_id}, Name: {name}, Category: {category}, Frequency: {frequency}, Amount: ${amount:.2f}")

        # Select valid expense ID to edit
        expense_id = get_valid_id("\nEnter the ID of the expense to edit (or type 'cancel' to go back): ", "expenses", "expense_id")
        if expense_id is None:
            return

        # Get new details
        new_name = get_valid_text("Enter new expense name: ")
        if new_name is None:
            return

        new_category = get_valid_text("Enter new category: ")
        if new_category is None:
            return

        new_frequency = get_valid_frequency("Enter new frequency (weekly/biweekly/monthly): ")
        if new_frequency is None:
            return

        new_amount = get_valid_float("Enter new amount: ")
        if new_amount is None:
            return

        # Update the expense in the database
        cursor.execute("""
            UPDATE expenses
            SET name = ?, category = ?, frequency = ?, amount = ?
            WHERE expense_id = ?
        """, (new_name, new_category, new_frequency, new_amount, expense_id))
        connection.commit()
        print("Expense updated successfully!")

    except sqlite3.Error as e:
        print("Error updating expense:", e)
    finally:
        connection.close()


def delete_expense():
    """
    Delete an expense entry by its ID with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing expenses
        cursor.execute("SELECT expense_id, name, category, frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        if not expenses:
            print("\nNo expenses found. Add one before deleting.")
            return

        print("\n===== Expenses =====")
        for expense_id, name, category, frequency, amount in expenses:
            print(f"ID: {expense_id}, Name: {name}, Category: {category}, Frequency: {frequency}, Amount: ${amount:.2f}")

        # Select valid expense ID to delete
        expense_id = get_valid_id("\nEnter the ID of the expense to delete (or type 'cancel' to go back): ", "expenses", "expense_id")
        if expense_id is None:
            return

        # Delete the selected expense
        cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
        connection.commit()
        print("Expense deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting expense:", e)
    finally:
        connection.close()