import sqlite3
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)


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

def edit_crypto():
    """
    Edit an existing cryptocurrency entry with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT crypto_id, coin_name, coins, current_value FROM cryptos")
        cryptos = cursor.fetchall()
        if not cryptos:
            print("\nNo cryptocurrencies found. Add one before editing.")
            return

        print("\n===== Cryptocurrencies =====")
        for crypto_id, coin_name, coins, current_value in cryptos:
            print(f"ID: {crypto_id}, Coin: {coin_name}, Coins: {coins:.4f}, Value: ${current_value:.2f}")

        # Get valid crypto ID
        crypto_id = get_valid_id("\nEnter the ID of the cryptocurrency to edit (or type 'cancel' to go back): ", "cryptos", "crypto_id")
        if crypto_id is None:
            return

        # Get new values
        new_name = get_valid_text("Enter new cryptocurrency name: ")
        if new_name is None:
            return

        new_coins = get_valid_float("Enter new number of coins: ")
        if new_coins is None:
            return

        new_value = get_valid_float("Enter new current value per coin: ")
        if new_value is None:
            return

        cursor.execute("""
            UPDATE cryptos SET coin_name = ?, coins = ?, current_value = ? WHERE crypto_id = ?
        """, (new_name, new_coins, new_value, crypto_id))
        connection.commit()
        print("Cryptocurrency updated successfully!")

    except sqlite3.Error as e:
        print("Error updating cryptocurrency:", e)
    finally:
        connection.close()


def delete_crypto():
    """
    Delete a cryptocurrency entry by its ID with validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT crypto_id, coin_name, coins, current_value FROM cryptos")
        cryptos = cursor.fetchall()
        if not cryptos:
            print("\nNo cryptocurrencies found. Add one before deleting.")
            return

        print("\n===== Cryptocurrencies =====")
        for crypto_id, coin_name, coins, current_value in cryptos:
            print(f"ID: {crypto_id}, Coin: {coin_name}, Coins: {coins:.4f}, Value: ${current_value:.2f}")

        # Get valid crypto ID
        crypto_id = get_valid_id("\nEnter the ID of the cryptocurrency to delete (or type 'cancel' to go back): ", "cryptos", "crypto_id")
        if crypto_id is None:
            return

        cursor.execute("DELETE FROM cryptos WHERE crypto_id = ?", (crypto_id,))
        connection.commit()
        print("Cryptocurrency deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting cryptocurrency:", e)
    finally:
        connection.close()