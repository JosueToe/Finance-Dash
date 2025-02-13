import sqlite3
import re
from datetime import datetime

# ---- Validate Numeric IDs (Whole Numbers Only) ----
def get_valid_id(prompt, table_name, id_column):
    """
    Repeatedly asks the user for a valid ID from a given table.
    Ensures the ID exists before proceeding.
    Allows 'cancel' option to exit.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    while True:
        user_input = input(prompt).strip().lower()

        if user_input == 'cancel':
            connection.close()
            return None  # Allows the user to exit

        if not user_input.isdigit():  # Ensures it's a whole number
            print("Invalid input. Please enter a valid numeric ID (whole number).")
            continue  # Ask again

        cursor.execute(f"SELECT {id_column} FROM {table_name} WHERE {id_column} = ?", (user_input,))
        result = cursor.fetchone()

        if result:
            connection.close()
            return int(user_input)  # Valid ID found, return it
        else:
            print(f"Invalid ID. Please enter an existing ID from the {table_name} list.")

# ---- Validate Float Inputs (Allows Decimals) ----
def get_valid_float(prompt):
    """
    Repeatedly asks the user for a valid float input.
    Allows numeric values with commas and decimals.
    """
    while True:
        user_input = input(prompt).replace(",", "").strip()
        if user_input.lower() == 'cancel':
            return None  # Allows the user to exit

        try:
            return float(user_input)  # Convert to float if valid
        except ValueError:
            print("Invalid input. Please enter a valid number (decimals allowed).")

# ---- Validate Integer Inputs (Whole Numbers Only) ----
def get_valid_int(prompt):
    """
    Ensures that the user inputs a valid integer (no decimals allowed).
    """
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'cancel':
            return None

        if user_input.isdigit():  # Ensures only whole numbers
            return int(user_input)
        else:
            print("Invalid input. Please enter a whole number (no decimals).")

# ---- Validate Text Inputs (No Numbers Allowed) ----
def get_valid_text(prompt):
    """
    Ensures the user enters a valid text input without numbers.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'cancel':
            return None

        if re.match("^[a-zA-Z ]+$", user_input):  # Only letters and spaces allowed
            return user_input.capitalize()
        else:
            print("Invalid input. Please enter a valid name (letters only).")

# ---- Validate Frequency Choices ----
def get_valid_frequency(prompt):
    """
    Ensures that the user selects a valid frequency option.
    """
    valid_choices = ["weekly", "biweekly", "monthly"]
    
    while True:
        user_input = input(prompt).strip().lower()
        if user_input == 'cancel':
            return None

        if user_input in valid_choices:
            return user_input
        print(f"Invalid choice. Please enter one of the following: {', '.join(valid_choices)}.")

# ---- Validate Date Input (MM/DD/YYYY) ----
def get_valid_date(prompt):
    """
    Ensures the user enters a date in MM/DD/YYYY format.
    """
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'cancel':
            return None

        try:
            valid_date = datetime.strptime(user_input, "%m/%d/%Y").date()
            return valid_date.strftime("%Y-%m-%d")  # Convert to correct format
        except ValueError:
            print("Invalid date format. Please enter the date in MM/DD/YYYY format.")
