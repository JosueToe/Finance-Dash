import sqlite3  # Import SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

from datetime import datetime
import sqlite3

def add_salary():
    """
    Add salary with back navigation across amount, frequency, and date.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    steps = ['amount', 'frequency', 'date']
    data = {}
    step_index = 0

    try:
        while step_index < len(steps):
            step = steps[step_index]

            if step == 'amount':
                user_input = input("Enter biweekly salary amount (or type 'back' or 'cancel'): ").replace(",", "").strip()
                if user_input.lower() == 'cancel':
                    print("❌ Operation cancelled. Returning to main menu...")
                    return
                if user_input.lower() == 'back':
                    print("🔙 Nothing to go back to.")
                    continue
                try:
                    data['amount'] = float(user_input)
                    step_index += 1
                except ValueError:
                    print("❌ Invalid input. Please enter a valid number.")

            elif step == 'frequency':
                user_input = input("Enter salary frequency (biweekly/monthly) or 'back'/'cancel': ").lower()
                if user_input == 'cancel':
                    print("❌ Operation cancelled. Returning to main menu...")
                    return
                if user_input == 'back':
                    step_index -= 1
                    continue
                if user_input in ['biweekly', 'monthly']:
                    data['frequency'] = user_input
                    step_index += 1
                else:
                    print("❌ Invalid frequency. Use 'biweekly' or 'monthly'.")

            elif step == 'date':
                user_input = input("Enter next payment date (MM/DD/YYYY) or 'back'/'cancel': ")
                if user_input.lower() == 'cancel':
                    print("❌ Operation cancelled. Returning to main menu...")
                    return
                if user_input.lower() == 'back':
                    step_index -= 1
                    continue
                try:
                    parsed_date = datetime.strptime(user_input, "%m/%d/%Y").strftime("%Y-%m-%d")
                    data['next_payment_date'] = parsed_date
                    step_index += 1
                except ValueError:
                    print("❌ Invalid date format. Use MM/DD/YYYY.")

        cursor.execute("""
            INSERT INTO salary (amount, frequency, next_payment_date)
            VALUES (?, ?, ?)
        """, (data['amount'], data['frequency'], data['next_payment_date']))
        connection.commit()
        print(f"✅ Salary added: ${data['amount']:.2f} ({data['frequency']}, next on {data['next_payment_date']}).")

    except sqlite3.Error as e:
        print("❌ Error adding salary:", e)
    finally:
        connection.close()

    

def edit_salary():
    """
    Edit an existing salary entry with full back functionality between steps.
    """
    import sqlite3
    from functions.validate_functions import get_valid_float, get_valid_frequency, get_valid_date

    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing salaries
        cursor.execute("SELECT salary_id, amount, frequency, next_payment_date FROM salary")
        salaries = cursor.fetchall()
        if not salaries:
            print("No salary records found.")
            return

        print("\n===== Salaries =====")
        for salary_id, amount, frequency, next_payment_date in salaries:
            print(f"ID: {salary_id}, Amount: ${amount:.2f}, Frequency: {frequency}, Next Payment: {next_payment_date}")

        # Step 1: Select ID
        while True:
            user_input = input("\nEnter the ID of the salary to edit (or type 'back' to return, 'cancel' to exit): ").lower().strip()
            if user_input == 'cancel':
                print("Returning to main menu...")
                return
            if user_input == 'back':
                return

            if user_input.isdigit():
                salary_id = int(user_input)
                cursor.execute("SELECT * FROM salary WHERE salary_id = ?", (salary_id,))
                existing = cursor.fetchone()
                if existing:
                    break
                else:
                    print("❌ No salary found with that ID.")
            else:
                print("Invalid input. Please enter a valid numeric ID.")

        # Step-by-step editing with back support
        step = 1
        new_amount = None
        new_frequency = None
        new_date = None

        while step <= 3:
            if step == 1:
                temp = input("Enter new salary amount (or type 'back' or 'cancel'): ").replace(",", "").strip().lower()
                if temp == 'cancel':
                    print("Returning to main menu...")
                    return
                if temp == 'back':
                    print("Returning to ID selection...\n")
                    return edit_salary()
                try:
                    new_amount = float(temp)
                    step += 1
                except ValueError:
                    print("Invalid input. Please enter a valid number (decimals allowed).")

            elif step == 2:
                temp = input("Enter new frequency (biweekly/monthly) or 'back' to return: ").lower().strip()
                if temp == 'cancel':
                    print("Returning to main menu...")
                    return
                if temp == 'back':
                    step -= 1
                    continue
                if temp in ['weekly', 'biweekly', 'monthly']:
                    new_frequency = temp
                    step += 1
                else:
                    print("Invalid choice. Please enter one of the following: weekly, biweekly, monthly.")

            elif step == 3:
                temp = input("Enter new next payment date (MM/DD/YYYY) or 'back': ").lower().strip()
                if temp == 'cancel':
                    print("Returning to main menu...")
                    return
                if temp == 'back':
                    step -= 1
                    continue
                from datetime import datetime
                try:
                    valid_date = datetime.strptime(temp, "%m/%d/%Y").date()
                    new_date = valid_date.strftime("%Y-%m-%d")
                    step += 1
                except ValueError:
                    print("Invalid date format. Please enter the date in MM/DD/YYYY format.")

        # Final update
        cursor.execute("""
            UPDATE salary SET amount = ?, frequency = ?, next_payment_date = ?
            WHERE salary_id = ?
        """, (new_amount, new_frequency, new_date, salary_id))
        connection.commit()
        print("✅ Salary entry updated successfully.")

    except sqlite3.Error as e:
        print("Error updating salary:", e)
    finally:
        connection.close()






def delete_salary():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:
            cursor.execute("SELECT salary_id, amount, frequency, next_payment_date FROM salary")
            salaries = cursor.fetchall()
            print("\n===== Salaries =====")
            for salary_id, amount, frequency, next_payment_date in salaries:
                print(f"ID: {salary_id}, Amount: ${amount:.2f}, Frequency: {frequency}, Next Payment: {next_payment_date}")

            salary_id = input("\nEnter the ID of the salary to delete (or type 'back' to return, 'cancel' to exit): ").lower().strip()

            if salary_id == 'cancel':
                print("Returning to main menu...")
                return
            elif salary_id == 'back':
                continue
            elif not salary_id.isdigit():
                print("❌ Invalid input. Please enter a valid numeric ID.")
                continue

            cursor.execute("SELECT * FROM salary WHERE salary_id = ?", (salary_id,))
            result = cursor.fetchone()
            if not result:
                print("❌ No salary found with that ID.")
                continue

            confirm = input(f"Are you sure you want to delete salary ID {salary_id}? (yes/no/back): ").lower().strip()
            if confirm == 'cancel':
                print("Returning to main menu...")
                return
            elif confirm == 'back':
                continue
            elif confirm != 'yes':
                print("❌ Deletion cancelled.")
                continue

            cursor.execute("DELETE FROM salary WHERE salary_id = ?", (salary_id,))
            connection.commit()
            print(f"✅ Salary ID {salary_id} deleted successfully.")
            break

    except sqlite3.Error as e:
        print("❌ Error deleting salary:", e)
    finally:
        connection.close()
