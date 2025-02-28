import sqlite3
import yfinance as yf
import requests
import time

def get_stock_price(ticker):
    """
    Fetches the latest stock price using Yahoo Finance.
    Returns the price if successful, otherwise None.
    """
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]  # Get the latest closing price
        return price if not price.empty else None
    except Exception:
        return None

def get_crypto_price(crypto_name):
    """
    Fetches the latest cryptocurrency price using CoinGecko API.
    Returns the price if successful, otherwise None.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name.lower()}&vs_currencies=usd"
    response = requests.get(url).json()
    return response.get(crypto_name.lower(), {}).get("usd")

def update_prices():
    """
    Updates stock and cryptocurrency prices in the database.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Update stock prices
        cursor.execute("SELECT stock_id, stock_ticker FROM stocks")
        stocks = cursor.fetchall()
        for stock_id, stock_ticker in stocks:
            price = get_stock_price(stock_ticker)
            if price:
                cursor.execute("UPDATE stocks SET current_value = ? WHERE stock_id = ?", (price, stock_id))
                print(f"Updated {stock_ticker} to ${price:.2f}")

        # Update crypto prices
        cursor.execute("SELECT crypto_id, coin_name FROM cryptos")
        cryptos = cursor.fetchall()
        for crypto_id, coin_name in cryptos:
            price = get_crypto_price(coin_name)
            if price:
                cursor.execute("UPDATE cryptos SET current_value = ? WHERE crypto_id = ?", (price, crypto_id))
                print(f"Updated {coin_name.capitalize()} to ${price:.2f}")

        connection.commit()
    except sqlite3.Error as e:
        print("Error updating prices:", e)
    finally:
        connection.close()

def auto_update_prices(interval=300):
    """
    Automatically updates stock & crypto prices every X seconds.
    Default interval is 5 minutes (300 seconds).
    """
    while True:
        print("\n🔄 Updating stock and crypto prices...")
        update_prices()
        print("✅ Update complete. Waiting for next update...\n")
        time.sleep(interval)  # Wait before the next update
