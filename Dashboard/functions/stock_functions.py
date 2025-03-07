import sqlite3  # Import SQLite library
import yfinance as yf
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def get_valid_stock_ticker():
    """
    Ensures the user enters a valid stock ticker that exists in Yahoo Finance.
    Prevents invalid tickers from being entered.
    """
    while True:
        stock_ticker = input("Enter stock ticker (e.g., AAPL, TSLA): ").strip().upper()

        if stock_ticker.lower() == 'cancel':
            return None  # Allow canceling

        try:
            stock = yf.Ticker(stock_ticker)
            stock_info = stock.history(period="1d")  # Fetch stock history
            
            if not stock_info.empty:
                return stock_ticker  # Ticker is valid
            else:
                print("❌ Invalid stock ticker. Please enter a valid ticker symbol.")

        except Exception:
            print("❌ Invalid stock ticker. Please enter a valid ticker symbol.")

def get_stock_price(ticker):
    """
    Fetches the latest stock price using Yahoo Finance.
    Returns the price if successful, otherwise asks for user retry.
    """
    while True:
        try:
            stock = yf.Ticker(ticker)
            price_data = stock.history(period="1d")["Close"]

            if not price_data.empty:
                return price_data.iloc[-1]  # Return latest closing price
            else:
                print("❌ Could not retrieve stock price. Please try again.")
                retry = input("Would you like to retry? (yes/no): ").strip().lower()
                if retry != "yes":
                    return None  # Allow user to cancel
            
        except Exception:
            print("❌ Error fetching stock price. Please enter a valid stock ticker.")
            return None

def add_stock():
    """
    Add a new stock entry with live price validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid stock ticker
        while True:
            stock_ticker = get_valid_stock_ticker()
            if stock_ticker is None:
                print("❌ Stock addition canceled.")
                return  # User chose to cancel
            
            # Get stock price
            stock_price = get_stock_price(stock_ticker)
            if stock_price is not None:
                break  # Exit loop if price is valid
            else:
                print("❌ Unable to fetch stock price. Please enter a different stock.")

        # Get valid number of shares
        shares = get_valid_float("Enter number of shares: ")
        if shares is None:
            print("❌ Stock addition canceled.")
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO stocks (stock_name, stock_ticker, shares, current_value)
            VALUES (?, ?, ?, ?)
        """, (stock_ticker, stock_ticker, shares, stock_price))
        connection.commit()
        print(f"✅ Added {shares} shares of {stock_ticker} at ${stock_price:.2f} per share.")

    except sqlite3.Error as e:
        print("❌ Error adding stock:", e)
    finally:
        connection.close()


def edit_stock():
    """
    Edit an existing stock entry with live price validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Display existing stocks
        cursor.execute("SELECT stock_id, stock_ticker, shares FROM stocks")
        stocks = cursor.fetchall()
        print("\n===== Stocks =====")
        for stock_id, stock_ticker, shares in stocks:
            print(f"ID: {stock_id}, Ticker: {stock_ticker}, Shares: {shares:.2f}")

        # Select stock to edit
        stock_id = get_valid_id("\nEnter the ID of the stock to edit (or type 'cancel' to go back): ", "stocks", "stock_id")
        if stock_id is None:
            return  # User canceled

        # Retrieve existing ticker
        cursor.execute("SELECT stock_ticker FROM stocks WHERE stock_id = ?", (stock_id,))
        stock_ticker = cursor.fetchone()[0]

        # Get latest price
        new_value = get_stock_price(stock_ticker)
        if new_value is None:
            print("❌ Error fetching live price. Please try again later.")
            return

        # Get valid number of shares
        new_shares = get_valid_float("Enter new number of shares: ")
        if new_shares is None:
            return

        # Update stock details
        cursor.execute("""
            UPDATE stocks
            SET shares = ?, current_value = ?
            WHERE stock_id = ?
        """, (new_shares, new_value, stock_id))
        connection.commit()
        print(f"✅ Updated {stock_ticker}: {new_shares} shares at ${new_value:.2f} per share.")

    except sqlite3.Error as e:
        print("❌ Error updating stock:", e)
    finally:
        connection.close()

def delete_stock():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT stock_id, stock_name, shares, current_value FROM stocks")
        stocks = cursor.fetchall()
        print("\n===== Stocks =====")
        for stock_id, stock_name, shares, current_value in stocks:
            print(f"ID: {stock_id}, Name: {stock_name}, Shares: {shares:.2f}, Value: ${current_value:.2f}")

        stock_id = get_valid_id("\nEnter the ID of the stock to delete (or type 'cancel' to go back): ", "stocks", "stock_id")
        if stock_id is None:
            return

        cursor.execute("DELETE FROM stocks WHERE stock_id = ?", (stock_id,))
        connection.commit()
        print("Stock deleted successfully!")

    except sqlite3.Error as e:
        print("Error deleting stock:", e)
    finally:
        connection.close()