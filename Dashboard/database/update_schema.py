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


import sqlite3

DB_PATH = "finance_dashboard.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(cryptos)")
columns = [row[1] for row in cursor.fetchall()]

if "coin_id" not in columns:
    print("🔧 Adding column 'coin_id' to cryptos...")
    cursor.execute("ALTER TABLE cryptos ADD COLUMN coin_id TEXT")
    conn.commit()
    print("✅ Column 'coin_id' added successfully.")
else:
    print("✅ Column 'coin_id' already exists.")

conn.close()
