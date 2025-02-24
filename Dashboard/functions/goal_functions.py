import sqlite3  # Importing SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def add_financial_goal():
    """
    Add a new financial goal entry with validated input.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid target net worth goal
        target_net_worth = get_valid_float("Enter your target net worth goal: ")
        if target_net_worth is None:
            return  # User chose to cancel

        # Get valid target date
        target_date = get_valid_date("Enter the target date to achieve this goal (MM/DD/YYYY): ")
        if target_date is None:
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO goals (net_worth_target, target_date)
            VALUES (?, ?)
        """, (target_net_worth, target_date))
        connection.commit()
        print(f"Goal of ${target_net_worth:.2f} by {target_date} added successfully!")

    except sqlite3.Error as e:
        print("Error adding goal:", e)
    finally:
        connection.close()

def edit_financial_goal():
    """
    Edit an existing financial goal entry with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT goal_id, net_worth_target, target_date FROM goals")
        goals = cursor.fetchall()
        if not goals:
            print("\nNo financial goals found. Add one before editing.")
            return

        print("\n===== Financial Goals =====")
        for goal_id, net_worth_target, target_date in goals:
            print(f"ID: {goal_id}, Target Net Worth: ${net_worth_target:.2f}, Target Date: {target_date}")

        # Get valid goal ID
        goal_id = get_valid_id("\nEnter the ID of the goal to edit (or type 'cancel' to go back): ", "goals", "goal_id")
        if goal_id is None:
            return

        # Get new values
        new_target = get_valid_float("Enter new target net worth: ")
        if new_target is None:
            return

        new_date = get_valid_date("Enter new target date (MM/DD/YYYY): ")
        if new_date is None:
            return

        cursor.execute("""
            UPDATE goals SET net_worth_target = ?, target_date = ? WHERE goal_id = ?
        """, (new_target, new_date, goal_id))
        connection.commit()
        print("Financial goal updated successfully!")

    except sqlite3.Error as e:
        print("Error updating financial goal:", e)
    finally:
        connection.close()


def delete_financial_goal():
    """
    Delete a financial goal entry by its ID with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT goal_id, net_worth_target, target_date FROM goals")
        goals = cursor.fetchall()
        if not goals:
            print("\nNo financial goals found. Add one before deleting.")
            return

        print("\n===== Financial Goals =====")
        for goal_id, net_worth_target, target_date in goals:
            print(f"ID: {goal_id}, Target Net Worth: ${net_worth_target:.2f}, Target Date: {target_date}")

        # Get valid goal ID
        goal_id = get_valid_id("\nEnter the ID of the goal to delete (or type 'cancel' to go back): ", "goals", "goal_id")
        if goal_id is None:
            return

        cursor.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))
        connection.commit()
        print("Financial goal deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting financial goal:", e)
    finally:
        connection.close()