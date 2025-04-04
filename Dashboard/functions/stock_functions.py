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

def get_stock_price(ticker):
    import yfinance as yf
    try:
        stock = yf.Ticker(ticker.upper())
        data = stock.history(period="1d")
        if not data.empty:
            return float(data["Close"].iloc[-1])
        return None
    except Exception as e:
        print(f"❌ [DEBUG] Error fetching price for {ticker}: {e}")
        return None

    
def add_stock():
    """
    Add a new stock entry with full back/cancel support and ticker validation.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    steps = ['ticker', 'shares']
    data = {}
    step_index = 0

    try:
        while step_index < len(steps):
            step = steps[step_index]

            if step == 'ticker':
                ticker_input = input("Enter stock ticker (e.g., AAPL, TSLA) or 'back'/'cancel': ").strip().upper()

                if ticker_input.lower() == 'cancel':
                    print("❌ Operation cancelled. Returning to main menu...")
                    return
                if ticker_input.lower() == 'back':
                    print("🔙 Nothing to go back to.")
                    continue

                stock = yf.Ticker(ticker_input)
                try:
                    stock_info = stock.info
                    current_price = stock.history(period="1d")["Close"].iloc[-1]

                    if not stock_info or 'shortName' not in stock_info or current_price is None:
                        raise ValueError

                    data['stock_ticker'] = ticker_input
                    data['stock_name'] = stock_info['shortName']
                    data['current_value'] = float(current_price)
                    print(f"✅ Validated {data['stock_name']} at ${data['current_value']:.2f} per share.")
                    step_index += 1
                except Exception:
                    print("❌ Invalid stock ticker. Please enter a valid symbol.")

            elif step == 'shares':
                shares_input = input("Enter number of shares (decimals allowed) or 'back'/'cancel': ").replace(",", "").strip()

                if shares_input.lower() == 'cancel':
                    print("❌ Operation cancelled. Returning to main menu...")
                    return
                if shares_input.lower() == 'back':
                    step_index -= 1
                    continue

                try:
                    data['shares'] = float(shares_input)
                    step_index += 1
                except ValueError:
                    print("❌ Invalid input. Please enter a valid number.")

        # Insert into the database
        cursor.execute("""
            INSERT INTO stocks (stock_name, stock_ticker, shares, current_value)
            VALUES (?, ?, ?, ?)
        """, (data['stock_name'], data['stock_ticker'], data['shares'], data['current_value']))
        connection.commit()
        print(f"✅ {data['stock_name']} ({data['stock_ticker']}) added successfully with {data['shares']} shares at ${data['current_value']:.2f} per share.")

    except sqlite3.Error as e:
        print("❌ Error adding stock:", e)
    finally:
        connection.close()

def edit_stock():
    """
    Edit an existing stock entry with full 'back' and 'cancel' navigation support.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:
            # Display all stocks
            cursor.execute("SELECT stock_id, stock_ticker, shares, current_value FROM stocks")
            stocks = cursor.fetchall()
            print("\n===== Stocks =====")
            for stock_id, stock_ticker, shares, current_value in stocks:
                print(f"ID: {stock_id}, Ticker: {stock_ticker.upper()}, Shares: {shares:.2f}, Price: ${current_value:.2f}")

            stock_id_input = input("Enter ID of stock to edit (or type 'back'/'cancel'): ").strip().lower()
            if stock_id_input == "cancel":
                print("Returning to main menu...")
                return
            if stock_id_input == "back":
                continue
            if not stock_id_input.isdigit():
                print("❌ Invalid input. Please enter a numeric ID.")
                continue

            stock_id = int(stock_id_input)
            cursor.execute("SELECT stock_ticker FROM stocks WHERE stock_id = ?", (stock_id,))
            result = cursor.fetchone()
            if not result:
                print("❌ Invalid stock ID.")
                continue

            original_ticker = result[0].upper()

            # Fetch the new live price first, before asking for shares
            new_price = get_stock_price(original_ticker)
            if not new_price:
                print(f"❌ Failed to fetch latest stock price for {original_ticker}. Try again later.")
                return

            while True:
                new_shares_input = input("Enter new number of shares or 'back'/'cancel': ").strip().lower()
                if new_shares_input == "cancel":
                    print("Operation cancelled.")
                    return
                if new_shares_input == "back":
                    break  # go back to ID selection

                try:
                    new_shares = float(new_shares_input)
                    break
                except ValueError:
                    print("❌ Invalid input. Please enter a number.")

            # If user typed "back", skip the update logic
            if new_shares_input == "back":
                continue

            # Update database
            cursor.execute("""
                UPDATE stocks SET shares = ?, current_value = ?
                WHERE stock_id = ?
            """, (new_shares, new_price, stock_id))
            connection.commit()
            print(f"✅ Stock updated successfully! New price for {original_ticker}: ${new_price:.2f}")
            return

    except sqlite3.Error as e:
        print("❌ Error updating stock:", e)
    finally:
        connection.close()


def delete_stock():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        while True:
            cursor.execute("SELECT stock_id, stock_ticker, shares FROM stocks")
            stocks = cursor.fetchall()
            print("\n===== Stocks =====")
            for stock_id, ticker, shares in stocks:
                print(f"ID: {stock_id}, Ticker: {ticker}, Shares: {shares:.2f}")

            stock_id = input("Enter stock ID to delete (or 'back'/'cancel'): ").strip().lower()
            if stock_id == 'cancel':
                print("❌ Operation cancelled.")
                return
            if stock_id == 'back':
                continue
            if not stock_id.isdigit():
                print("❌ Invalid input. Please enter a numeric ID.")
                continue

            stock_id = int(stock_id)
            cursor.execute("SELECT * FROM stocks WHERE stock_id = ?", (stock_id,))
            if not cursor.fetchone():
                print("❌ Stock ID not found.")
                continue

            confirm = input(f"Are you sure you want to delete stock ID {stock_id}? (yes/no/back): ").lower().strip()
            if confirm == 'back':
                continue
            if confirm != 'yes':
                print("❌ Deletion cancelled.")
                continue

            cursor.execute("DELETE FROM stocks WHERE stock_id = ?", (stock_id,))
            connection.commit()
            print(f"✅ Stock ID {stock_id} deleted.")
            break

    except sqlite3.Error as e:
        print("❌ Error deleting stock:", e)
    finally:
        connection.close()
