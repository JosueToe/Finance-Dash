import sqlite3

# Connect to the database
import os
db_path = os.path.join(os.path.dirname(__file__), "finance_dashboard.db")
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

try:
    # Add last_updated column to stocks table if it doesn't exist
    cursor.execute("PRAGMA table_info(stocks)")
    columns = [col[1] for col in cursor.fetchall()]
    if "last_updated" not in columns:
        cursor.execute("ALTER TABLE stocks ADD COLUMN last_updated TEXT DEFAULT NULL")
        print("✅ Added last_updated column to stocks table.")

    # Add last_updated column to cryptos table if it doesn't exist
    cursor.execute("PRAGMA table_info(cryptos)")
    columns = [col[1] for col in cursor.fetchall()]
    if "last_updated" not in columns:
        cursor.execute("ALTER TABLE cryptos ADD COLUMN last_updated TEXT DEFAULT NULL")
        print("✅ Added last_updated column to cryptos table.")

    connection.commit()
    print("✅ Database schema updated successfully.")

except sqlite3.Error as e:
    print("❌ Error updating database schema:", e)

finally:
    connection.close()
