import sqlite3
import requests
import yfinance as yf
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def get_crypto_price(crypto_name):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name.lower()}&vs_currencies=usd"
        response = requests.get(url).json()
        return response.get(crypto_name.lower(), {}).get("usd")
    except Exception:
        return None


def add_crypto():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()
    steps = ['name', 'coins']
    data = {}
    step_index = 0

    try:
        while step_index < len(steps):
            step = steps[step_index]

            if step == 'name':
                name_input = input("Enter the cryptocurrency name (e.g., bitcoin) or 'back'/'cancel': ").strip().lower()
                if name_input == 'cancel':
                    print("❌ Operation cancelled. Returning to main menu...")
                    return
                if name_input == 'back':
                    print("🔙 Nothing to go back to.")
                    continue

                price = get_crypto_price(name_input)
                if price is None:
                    print("❌ Error: Invalid cryptocurrency. Please try again.")
                else:
                    data['name'] = name_input
                    data['price'] = price
                    step_index += 1

            elif step == 'coins':
                coins_input = input("Enter the number of coins (or 'back'/'cancel'): ").replace(",", "").strip()
                if coins_input.lower() == 'cancel':
                    print("❌ Operation cancelled.")
                    return
                if coins_input.lower() == 'back':
                    step_index -= 1
                    continue
                try:
                    data['coins'] = float(coins_input)
                    step_index += 1
                except ValueError:
                    print("❌ Invalid input. Please enter a numeric value.")

        cursor.execute("""
            INSERT INTO cryptos (coin_name, coins, current_value)
            VALUES (?, ?, ?)
        """, (data['name'], data['coins'], data['price']))
        connection.commit()
        print(f"✅ {data['name'].capitalize()} added successfully with {data['coins']} coins at ${data['price']:.2f}.")

    except sqlite3.Error as e:
        print("❌ Error adding cryptocurrency:", e)
    finally:
        connection.close()


def edit_crypto():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT crypto_id, coin_name, coins, current_value FROM cryptos")
        cryptos = cursor.fetchall()

        if not cryptos:
            print("⚠️ No cryptocurrency records found.")
            return

        print("\n===== Cryptocurrencies =====")
        for crypto_id, coin_name, coins, current_value in cryptos:
            print(f"ID: {crypto_id}, Coin: {coin_name}, Coins: {coins:.2f}, Value: ${current_value:.2f}")

        while True:
            user_input = input("\nEnter the ID of the crypto to edit (or 'back'/'cancel'): ").strip().lower()
            if user_input == 'cancel':
                return
            if user_input == 'back':
                print("🔙 Nothing to go back to.")
                continue
            if user_input.isdigit():
                crypto_id = int(user_input)
                cursor.execute("SELECT * FROM cryptos WHERE crypto_id = ?", (crypto_id,))
                if cursor.fetchone():
                    break
                else:
                    print("❌ Invalid ID. Try again.")
            else:
                print("❌ Please enter a valid numeric ID.")

        steps = ['name', 'coins']
        data = {}
        step_index = 0

        while step_index < len(steps):
            step = steps[step_index]

            if step == 'name':
                name_input = input("Enter new cryptocurrency name (e.g., bitcoin) or 'back'/'cancel': ").strip().lower()
                if name_input == 'cancel':
                    print("❌ Operation cancelled.")
                    return
                if name_input == 'back':
                    print("🔙 Nothing to go back to.")
                    continue

                price = get_crypto_price(name_input)
                if price is None:
                    print("❌ Error: Invalid name. Try again.")
                else:
                    data['name'] = name_input
                    data['price'] = price
                    step_index += 1

            elif step == 'coins':
                coins_input = input("Enter new number of coins (or 'back'/'cancel'): ").replace(",", "").strip()
                if coins_input.lower() == 'cancel':
                    return
                if coins_input.lower() == 'back':
                    step_index -= 1
                    continue
                try:
                    data['coins'] = float(coins_input)
                    step_index += 1
                except ValueError:
                    print("❌ Invalid number. Please enter digits only.")

        cursor.execute("""
            UPDATE cryptos SET coin_name = ?, coins = ?, current_value = ?
            WHERE crypto_id = ?
        """, (data['name'], data['coins'], data['price'], crypto_id))
        connection.commit()
        print("✅ Cryptocurrency updated successfully!")

    except sqlite3.Error as e:
        print("❌ Error editing cryptocurrency:", e)
    finally:
        connection.close()


def delete_crypto():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT crypto_id, coin_name, coins, current_value FROM cryptos")
        cryptos = cursor.fetchall()

        if not cryptos:
            print("⚠️ No cryptocurrencies found.")
            return

        print("\n===== Cryptocurrencies =====")
        for crypto_id, coin_name, coins, current_value in cryptos:
            print(f"ID: {crypto_id}, Coin: {coin_name}, Coins: {coins:.2f}, Value: ${current_value:.2f}")

        while True:
            user_input = input("\nEnter the ID of the crypto to delete (or 'back'/'cancel'): ").strip().lower()
            if user_input == 'cancel':
                return
            if user_input == 'back':
                print("🔙 Nothing to go back to.")
                continue
            if user_input.isdigit():
                crypto_id = int(user_input)
                cursor.execute("SELECT * FROM cryptos WHERE crypto_id = ?", (crypto_id,))
                if cursor.fetchone():
                    break
                else:
                    print("❌ Invalid ID.")
            else:
                print("❌ Enter a numeric ID.")

        confirm = input(f"Are you sure you want to delete crypto ID {crypto_id}? (yes/no): ").strip().lower()
        if confirm == 'yes':
            cursor.execute("DELETE FROM cryptos WHERE crypto_id = ?", (crypto_id,))
            connection.commit()
            print("✅ Cryptocurrency deleted successfully.")
        else:
            print("❌ Deletion cancelled.")

    except sqlite3.Error as e:
        print("❌ Error deleting cryptocurrency:", e)
    finally:
        connection.close()
