import sqlite3

# Connect to the database
connection = sqlite3.connect('database/finance_dashboard.db')
cursor = connection.cursor()

try:
    # Drop the old 'goals' table if it exists
    cursor.execute("DROP TABLE IF EXISTS goals")

    # Recreate the 'goals' table with the correct schema
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS goals (
        goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
        net_worth_target REAL NOT NULL,
        target_date DATE NOT NULL
    )
    """)

    print("Table 'goals' updated successfully!")
except sqlite3.Error as e:
    print("Error updating schema:", e)
finally:
    connection.commit()
    connection.close()
