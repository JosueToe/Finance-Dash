import sqlite3  # Importing SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def add_financial_goal():
    import sqlite3
    from datetime import datetime

    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()
    steps = ['net_worth_target', 'target_date']
    data = {}
    step_index = 0

    try:
        while step_index < len(steps):
            step = steps[step_index]
            if step == 'net_worth_target':
                user_input = input("Enter your target net worth (or type 'back'/'cancel'): ").replace(",", "").strip().lower()
                if user_input == 'cancel':
                    print("❌ Operation cancelled.")
                    return
                if user_input == 'back':
                    print("🔙 Nothing to go back to.")
                    continue
                try:
                    data['net_worth_target'] = float(user_input)
                    step_index += 1
                except ValueError:
                    print("❌ Invalid number.")
            elif step == 'target_date':
                user_input = input("Enter target date (MM/DD/YYYY) or 'back'/'cancel': ").strip().lower()
                if user_input == 'cancel':
                    print("❌ Operation cancelled.")
                    return
                if user_input == 'back':
                    step_index -= 1
                    continue
                try:
                    date_obj = datetime.strptime(user_input, "%m/%d/%Y")
                    data['target_date'] = date_obj.strftime("%Y-%m-%d")
                    step_index += 1
                except ValueError:
                    print("❌ Invalid date format.")

        cursor.execute("INSERT INTO goals (net_worth_target, target_date) VALUES (?, ?)",
                       (data['net_worth_target'], data['target_date']))
        connection.commit()
        print(f"✅ Goal of ${data['net_worth_target']:.2f} by {data['target_date']} added.")

    except sqlite3.Error as e:
        print("❌ Error:", e)
    finally:
        connection.close()


def edit_financial_goal():
    import sqlite3
    from datetime import datetime

    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:
            cursor.execute("SELECT goal_id, net_worth_target, target_date FROM goals")
            goals = cursor.fetchall()
            if not goals:
                print("❌ No goals found.")
                return

            print("\n===== Financial Goals =====")
            for goal_id, net_worth_target, target_date in goals:
                print(f"ID: {goal_id}, Target: ${net_worth_target:.2f}, Date: {target_date}")

            goal_id_input = input("Enter ID to edit (or type 'back'/'cancel'): ").lower().strip()
            if goal_id_input == 'cancel':
                print("Returning to main menu...")
                return
            if goal_id_input == 'back':
                continue
            if not goal_id_input.isdigit():
                print("❌ Invalid input.")
                continue

            goal_id = int(goal_id_input)
            cursor.execute("SELECT * FROM goals WHERE goal_id = ?", (goal_id,))
            if not cursor.fetchone():
                print("❌ No goal with that ID.")
                continue

            step_index = 0
            steps = ['net_worth_target', 'target_date']
            data = {}

            while step_index < len(steps):
                step = steps[step_index]
                if step == 'net_worth_target':
                    user_input = input("Enter new net worth (or 'back'/'cancel'): ").replace(",", "").strip().lower()
                    if user_input == 'cancel':
                        return
                    if user_input == 'back':
                        print("🔙 Going back to ID selection...")
                        break
                    try:
                        data['net_worth_target'] = float(user_input)
                        step_index += 1
                    except ValueError:
                        print("❌ Invalid number.")
                elif step == 'target_date':
                    user_input = input("Enter new target date (MM/DD/YYYY) or 'back'/'cancel': ").strip().lower()
                    if user_input == 'cancel':
                        return
                    if user_input == 'back':
                        step_index -= 1
                        continue
                    try:
                        date_obj = datetime.strptime(user_input, "%m/%d/%Y")
                        data['target_date'] = date_obj.strftime("%Y-%m-%d")
                        step_index += 1
                    except ValueError:
                        print("❌ Invalid date format.")

            if len(data) == 2:
                cursor.execute("UPDATE goals SET net_worth_target = ?, target_date = ? WHERE goal_id = ?",
                               (data['net_worth_target'], data['target_date'], goal_id))
                connection.commit()
                print("✅ Goal updated successfully.")
                return

    except sqlite3.Error as e:
        print("❌ Error updating goal:", e)
    finally:
        connection.close()



def delete_financial_goal():
    import sqlite3

    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:
            cursor.execute("SELECT goal_id, net_worth_target, target_date FROM goals")
            goals = cursor.fetchall()
            if not goals:
                print("❌ No goals to delete.")
                return

            print("\n===== Financial Goals =====")
            for goal_id, net_worth_target, target_date in goals:
                print(f"ID: {goal_id}, Target: ${net_worth_target:.2f}, Date: {target_date}")

            goal_id_input = input("Enter ID to delete (or 'back'/'cancel'): ").strip().lower()
            if goal_id_input == 'cancel':
                return
            if goal_id_input == 'back':
                continue
            if not goal_id_input.isdigit():
                print("❌ Invalid ID.")
                continue

            goal_id = int(goal_id_input)
            cursor.execute("SELECT * FROM goals WHERE goal_id = ?", (goal_id,))
            if not cursor.fetchone():
                print("❌ No goal found with that ID.")
                continue

            confirm = input(f"Delete goal ID {goal_id}? (yes/no/back): ").strip().lower()
            if confirm == 'cancel':
                return
            if confirm == 'back':
                continue
            if confirm != 'yes':
                print("❌ Deletion cancelled.")
                continue

            cursor.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))
            connection.commit()
            print(f"✅ Goal ID {goal_id} deleted.")
            return

    except sqlite3.Error as e:
        print("❌ Error deleting goal:", e)
    finally:
        connection.close()
