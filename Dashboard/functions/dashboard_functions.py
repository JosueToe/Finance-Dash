import sqlite3
import yfinance as yf
import requests
from datetime import datetime, timedelta
from functions.validate_functions import get_valid_text

def get_stock_price(ticker):
    """
    Fetches the latest stock price using Yahoo Finance.
    If the API fails, returns None.
    """
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")["Close"].iloc[-1]  # Get latest closing price
        return price if not price.empty else None
    except Exception:
        return None

def get_crypto_price(crypto_name):
    """
    Fetches the latest cryptocurrency price using CoinGecko API.
    If the API fails, returns None.
    """
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_name.lower()}&vs_currencies=usd"
    response = requests.get(url).json()
    return response.get(crypto_name.lower(), {}).get("usd")

def should_update(last_updated_time):
    """
    Checks if more than 10 minutes have passed since the last update.
    Returns True if update is needed, otherwise False.
    """
    if not last_updated_time:
        return True  # If no timestamp, force an update
    
    last_update = datetime.strptime(last_updated_time, "%Y-%m-%d %H:%M:%S")
    return datetime.now() - last_update > timedelta(minutes=10)  # Update only if >10 min

def update_stock_prices():
    """
    Updates stock prices in the database only if the last update was more than 10 minutes ago.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT stock_id, stock_ticker, last_updated FROM stocks")
        stocks = cursor.fetchall()

        for stock_id, stock_ticker, last_updated in stocks:
            if should_update(last_updated):
                price = get_stock_price(stock_ticker)
                if price:
                    cursor.execute("UPDATE stocks SET current_value = ?, last_updated = CURRENT_TIMESTAMP WHERE stock_id = ?", (price, stock_id))
        
        connection.commit()
    except sqlite3.Error as e:
        print("❌ Error updating stock prices:", e)
    finally:
        connection.close()

def update_crypto_prices():
    """
    Updates cryptocurrency prices in the database only if the last update was more than 10 minutes ago.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT crypto_id, coin_name, last_updated FROM cryptos")
        cryptos = cursor.fetchall()

        for crypto_id, coin_name, last_updated in cryptos:
            if should_update(last_updated):
                price = get_crypto_price(coin_name)
                if price:
                    cursor.execute("UPDATE cryptos SET current_value = ?, last_updated = CURRENT_TIMESTAMP WHERE crypto_id = ?", (price, crypto_id))

        connection.commit()
    except sqlite3.Error as e:
        print("❌ Error updating cryptocurrency prices:", e)
    finally:
        connection.close()

def display_dashboard():
    """
    Display the financial dashboard with optimized stock & crypto updates.
    """
    print("\n🔄 Checking if stock & crypto prices need updates...")
    update_stock_prices()
    update_crypto_prices()

    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Fetch total bank balances
        cursor.execute("SELECT SUM(balance) FROM bank_accounts")
        total_bank = cursor.fetchone()[0] or 0.0

        # Fetch total stock value
        cursor.execute("SELECT SUM(shares * current_value) FROM stocks")
        total_stocks = cursor.fetchone()[0] or 0.0

        # Fetch total cryptocurrency value
        cursor.execute("SELECT SUM(coins * current_value) FROM cryptos")
        total_crypto = cursor.fetchone()[0] or 0.0

        # Fetch monthly income
        cursor.execute("SELECT SUM(amount) FROM salary")
        total_monthly_income = (cursor.fetchone()[0] or 0.0) * 2  # Assuming biweekly salary

        # Fetch monthly expenses
        cursor.execute("SELECT frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        total_monthly_expenses = 0.0
        for frequency, amount in expenses:
            if frequency == 'weekly':
                total_monthly_expenses += amount * 4
            elif frequency == 'biweekly':
                total_monthly_expenses += amount * 2
            elif frequency == 'monthly':
                total_monthly_expenses += amount
        total_net_worth = total_bank + total_stocks + total_crypto

        # Fetch financial goal
        cursor.execute("SELECT net_worth_target, target_date FROM goals LIMIT 1")
        goal = cursor.fetchone()

        print("\n===== 📊 Financial Dashboard =====")
        print(f"🏦 Total Bank Balances: ${total_bank:.2f}")
        print(f"📈 Total Stock Value: ${total_stocks:.2f} (Updated)")
        print(f"🪙 Total Cryptocurrency Value: ${total_crypto:.2f} (Updated)")
        print(f"💰 Total Net Worth: ${total_net_worth:.2f}")
        print(f"📥 Total Monthly Income: ${total_monthly_income:.2f}")
        print(f"📤 Total Monthly Expenses: ${total_monthly_expenses:.2f}")
        print(f"📊 Net Monthly Cash Flow: ${total_monthly_income - total_monthly_expenses:.2f}")

        # Display financial goal progress if set
        if goal:
            net_worth_target, target_date = goal
            progress_percentage = (total_net_worth / net_worth_target) * 100
            today = datetime.today().date()
            target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            days_remaining = (target_date - today).days
            print("\n🎯 Financial Goal:")
            print(f"  Target Net Worth: ${net_worth_target:.2f}")
            print(f"  Current Progress: {progress_percentage:.2f}%")
            print(f"  Days Remaining: {days_remaining} days")
            print("===============================")
        else:
            print("\n❌ No financial goals set.")

    except sqlite3.Error as e:
        print("❌ Error displaying dashboard:", e)

    finally:
        connection.close()
