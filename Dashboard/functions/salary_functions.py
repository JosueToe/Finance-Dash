import sqlite3  # Import SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def add_salary():
    """
    Add a new salary entry with validated input.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid biweekly salary amount
        amount = get_valid_float("Enter biweekly salary amount: ")
        if amount is None:
            return  # User chose to cancel

        # Get valid next payment date
        next_payment_date = get_valid_date("Enter next payment date (MM/DD/YYYY): ")
        if next_payment_date is None:
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO salary (amount, frequency, next_payment_date)
            VALUES (?, ?, ?)
        """, (amount, 'biweekly', next_payment_date))
        connection.commit()
        print(f"Biweekly salary of ${amount:.2f} added. Next payment date: {next_payment_date}.")

    except sqlite3.Error as e:
        print("Error adding salary:", e)
    finally:
        connection.close()


def edit_salary():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT salary_id, amount, frequency, next_payment_date FROM salary")
        salaries = cursor.fetchall()
        print("\n===== Salaries =====")
        for salary_id, amount, frequency, next_payment_date in salaries:
            print(f"ID: {salary_id}, Amount: ${amount:.2f}, Frequency: {frequency}, Next Payment: {next_payment_date}")

        salary_id = get_valid_id("\nEnter the ID of the salary to edit (or type 'cancel' to go back): ", "salary", "salary_id")
        if salary_id is None:
            return

        new_amount = get_valid_float("Enter new salary amount: ")
        if new_amount is None:
            return

        new_frequency = get_valid_frequency("Enter new frequency (biweekly/monthly): ")
        if new_frequency is None:
            return

        new_date = get_valid_date("Enter new next payment date (MM/DD/YYYY): ")
        if new_date is None:
            return

        cursor.execute("""
            UPDATE salary SET amount = ?, frequency = ?, next_payment_date = ? WHERE salary_id = ?
        """, (new_amount, new_frequency, new_date, salary_id))
        connection.commit()
        print("Salary updated successfully!")

    except sqlite3.Error as e:
        print("Error updating salary:", e)
    finally:
        connection.close()


def delete_salary():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT salary_id, amount, frequency, next_payment_date FROM salary")
        salaries = cursor.fetchall()
        print("\n===== Salaries =====")
        for salary_id, amount, frequency, next_payment_date in salaries:
            print(f"ID: {salary_id}, Amount: ${amount:.2f}, Frequency: {frequency}, Next Payment: {next_payment_date}")

        salary_id = get_valid_id("\nEnter the ID of the salary to delete (or type 'cancel' to go back): ", "salary", "salary_id")
        if salary_id is None:
            return

        cursor.execute("DELETE FROM salary WHERE salary_id = ?", (salary_id,))
        connection.commit()
        print("Salary deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting salary:", e)
    finally:
        connection.close()