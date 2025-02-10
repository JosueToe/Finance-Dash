import sqlite3

def add_crypto():
    """
    Add a new cryptocurrency entry.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        coin_name = input("Enter the cryptocurrency name (e.g., Bitcoin): ").capitalize()
        coins = input("Enter the number of coins you own: ").replace(",", "")
        current_value = input("Enter the current value per coin: ").replace(",", "")

        # Convert inputs to floats after removing commas
        coins = float(coins)
        current_value = float(current_value)

        cursor.execute("""
            INSERT INTO cryptos (coin_name, coins, current_value)
            VALUES (?, ?, ?)
        """, (coin_name, coins, current_value))
        connection.commit()
        print(f"{coin_name} added successfully!")
    except ValueError:
        print("Invalid input. Please enter valid numeric values.")
    except sqlite3.Error as e:
        print("Error adding cryptocurrency:", e)
    finally:
        connection.close()
