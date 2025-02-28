import sqlite3
import yfinance as yf
import requests
from datetime import datetime
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

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

def update_stock_prices():
    """
    Updates stock prices in the database before displaying the dashboard.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT stock_id, stock_ticker FROM stocks")
        stocks = cursor.fetchall()
        for stock_id, stock_ticker in stocks:
            price = get_stock_price(stock_ticker)
            if price:
                cursor.execute("UPDATE stocks SET current_value = ? WHERE stock_id = ?", (price, stock_id))
        connection.commit()
    except sqlite3.Error as e:
        print("Error updating stock prices:", e)
    finally:
        connection.close()

def update_crypto_prices():
    """
    Updates cryptocurrency prices in the database before displaying the dashboard.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT crypto_id, coin_name FROM cryptos")
        cryptos = cursor.fetchall()
        for crypto_id, coin_name in cryptos:
            price = get_crypto_price(coin_name)
            if price:
                cursor.execute("UPDATE cryptos SET current_value = ? WHERE crypto_id = ?", (price, crypto_id))
        connection.commit()
    except sqlite3.Error as e:
        print("Error updating cryptocurrency prices:", e)
    finally:
        connection.close()

def display_dashboard():
    """
    Display the financial dashboard with real-time stock & crypto prices, net worth, and financial goals.
    """
    # Ensure stock & crypto prices are updated before displaying
    print("\n🔄 Fetching live stock & cryptocurrency prices...")
    update_stock_prices()
    update_crypto_prices()

    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Initialize the dashboard data dictionary
        dashboard_data = {}

        # Fetch total bank balances
        cursor.execute("SELECT SUM(balance) FROM bank_accounts")
        dashboard_data['total_bank'] = cursor.fetchone()[0] or 0.0

        # Fetch total stock value (after updating prices)
        cursor.execute("SELECT SUM(shares * current_value) FROM stocks")
        dashboard_data['total_stocks'] = cursor.fetchone()[0] or 0.0

        # Fetch total cryptocurrency value (after updating prices)
        cursor.execute("SELECT SUM(coins * current_value) FROM cryptos")
        dashboard_data['total_crypto'] = cursor.fetchone()[0] or 0.0

        # Fetch monthly income
        cursor.execute("SELECT SUM(amount) FROM salary")
        dashboard_data['total_monthly_income'] = (cursor.fetchone()[0] or 0.0) * 2  # Assuming biweekly salary

        # Fetch monthly expenses
        cursor.execute("SELECT frequency, amount FROM expenses")
        expenses = cursor.fetchall()
        total_monthly_expenses = 0.0
        for frequency, amount in expenses:
            if frequency == 'weekly':
                total_monthly_expenses += amount * 4  # Approximate 4 weeks in a month
            elif frequency == 'biweekly':
                total_monthly_expenses += amount * 2  # Approximate 2 biweeks in a month
            elif frequency == 'monthly':
                total_monthly_expenses += amount
        dashboard_data['total_monthly_expenses'] = total_monthly_expenses

        # Fetch financial goal
        cursor.execute("SELECT net_worth_target, target_date FROM goals LIMIT 1")
        goal = cursor.fetchone()
        if goal:
            net_worth_target, target_date = goal
            dashboard_data['net_worth_target'] = net_worth_target

            # Calculate progress and remaining days
            total_net_worth = dashboard_data['total_bank'] + dashboard_data['total_stocks'] + dashboard_data['total_crypto']
            dashboard_data['total_net_worth'] = total_net_worth
            dashboard_data['progress_percentage'] = (total_net_worth / net_worth_target) * 100

            today = datetime.today().date()
            target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
            days_remaining = (target_date - today).days
            dashboard_data['days_remaining'] = days_remaining
        else:
            dashboard_data['net_worth_target'] = None
            dashboard_data['total_net_worth'] = dashboard_data['total_bank'] + dashboard_data['total_stocks'] + dashboard_data['total_crypto']

        # Display the dashboard
        print("\n===== 📊 Financial Dashboard =====")
        print(f"🏦 Total Bank Balances: ${dashboard_data['total_bank']:.2f}")
        print(f"📈 Total Stock Value: ${dashboard_data['total_stocks']:.2f} (Updated)")
        print(f"🪙 Total Cryptocurrency Value: ${dashboard_data['total_crypto']:.2f} (Updated)")
        print(f"💰 Total Net Worth: ${dashboard_data['total_net_worth']:.2f}")
        print(f"📥 Total Monthly Income: ${dashboard_data['total_monthly_income']:.2f}")
        print(f"📤 Total Monthly Expenses: ${dashboard_data['total_monthly_expenses']:.2f}")
        print(f"📊 Net Monthly Cash Flow: ${dashboard_data['total_monthly_income'] - dashboard_data['total_monthly_expenses']:.2f}")

        # Display financial goal progress if set
        if dashboard_data['net_worth_target'] is not None:
            print("\n🎯 Financial Goal:")
            print(f"  Target Net Worth: ${dashboard_data['net_worth_target']:.2f}")
            print(f"  Current Progress: {dashboard_data['progress_percentage']:.2f}%")
            print(f"  Days Remaining: {dashboard_data['days_remaining']} days")
            print("===============================")
        else:
            print("\n❌ No financial goals set.")

    except sqlite3.Error as e:
        print("Error displaying dashboard:", e)

    finally:
        connection.close()
