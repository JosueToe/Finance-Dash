import sqlite3
import requests
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def get_crypto_price(crypto_name):
    """
    Fetches the live crypto price using CoinGecko API.
    Returns the price if successful, otherwise None.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name.lower()}&vs_currencies=usd"
    response = requests.get(url).json()
    return response.get(crypto_name.lower(), {}).get("usd")

def add_crypto():
    """
    Add a new cryptocurrency entry with validation and a cancel option.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Ask for cryptocurrency name
        coin_name = get_valid_text("Enter the cryptocurrency name (or type 'cancel' to exit): ")
        if coin_name is None:
            print("Returning to main menu...")
            return

        # Fetch live crypto price
        current_value = get_crypto_price(coin_name)
        if current_value is None:
            print("❌ Error: Invalid cryptocurrency. Please try again.")
            return

        # Ask for the number of coins
        coins = get_valid_float("Enter the number of coins you own (or type 'cancel' to exit): ")
        if coins is None:
            print("Returning to main menu...")
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO cryptos (coin_name, coins, current_value)
            VALUES (?, ?, ?)
        """, (coin_name, coins, current_value))
        connection.commit()
        print(f"✅ {coin_name} added successfully with {coins} coins at ${current_value:.2f} per coin.")

    except sqlite3.Error as e:
        print("❌ Error adding cryptocurrency:", e)
    finally:
        connection.close()



def edit_crypto():
    """
    Edit an existing cryptocurrency entry with live price validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing cryptocurrencies
        cursor.execute("SELECT crypto_id, coin_name, coins FROM cryptos")
        cryptos = cursor.fetchall()
        print("\n===== Cryptocurrencies =====")
        for crypto_id, coin_name, coins in cryptos:
            print(f"ID: {crypto_id}, Coin: {coin_name}, Coins: {coins:.2f}")

        # Select crypto to edit
        crypto_id = get_valid_id("\nEnter the ID of the cryptocurrency to edit (or type 'cancel' to go back): ", "cryptos", "crypto_id")
        if crypto_id is None:
            return  # User canceled

        # Retrieve existing crypto name
        cursor.execute("SELECT coin_name FROM cryptos WHERE crypto_id = ?", (crypto_id,))
        coin_name = cursor.fetchone()[0]

        # Get latest price
        new_value = get_crypto_price(coin_name)
        if new_value is None:
            print("❌ Error fetching live price. Please try again later.")
            return

        # Get valid number of coins
        new_coins = get_valid_float("Enter new number of coins: ")
        if new_coins is None:
            return

        # Update crypto details
        cursor.execute("""
            UPDATE cryptos
            SET coins = ?, current_value = ?
            WHERE crypto_id = ?
        """, (new_coins, new_value, crypto_id))
        connection.commit()
        print(f"✅ Updated {coin_name}: {new_coins} coins at ${new_value:.2f} per coin.")

    except sqlite3.Error as e:
        print("❌ Error updating cryptocurrency:", e)
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