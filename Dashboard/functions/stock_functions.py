import sqlite3  # Import SQLite library
from functions.validate_functions import (
    get_valid_id, get_valid_float, get_valid_int, 
    get_valid_text, get_valid_frequency, get_valid_date
)

def add_stock():
    """
    Add a new stock entry with validated input.
    """
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        # Get valid stock name
        stock_name = get_valid_text("Enter stock name: ")
        if stock_name is None:
            return  # User chose to cancel

        # Get valid number of shares
        shares = get_valid_float("Enter number of shares: ")
        if shares is None:
            return

        # Get valid current value per share
        current_value = get_valid_float("Enter current value per share: ")
        if current_value is None:
            return

        # Insert into database
        cursor.execute("""
            INSERT INTO stocks (stock_name, shares, current_value)
            VALUES (?, ?, ?)
        """, (stock_name, shares, current_value))
        connection.commit()
        print(f"Added {shares} shares of {stock_name} at ${current_value:.2f} per share.")

    except sqlite3.Error as e:
        print("Error adding stock:", e)
    finally:
        connection.close()

def edit_stock():
    connection = sqlite3.connect('database/finance_dashboard.db')
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT stock_id, stock_name, shares, current_value FROM stocks")
        stocks = cursor.fetchall()
        print("\n===== Stocks =====")
        for stock_id, stock_name, shares, current_value in stocks:
            print(f"ID: {stock_id}, Name: {stock_name}, Shares: {shares:.2f}, Value: ${current_value:.2f}")

        stock_id = get_valid_id("\nEnter the ID of the stock to edit (or type 'cancel' to go back): ", "stocks", "stock_id")
        if stock_id is None:
            return

        new_name = get_valid_text("Enter new stock name: ")
        if new_name is None:
            return

        new_shares = get_valid_float("Enter new number of shares: ")
        if new_shares is None:
            return

        new_value = get_valid_float("Enter new current value per share: ")
        if new_value is None:
            return

        cursor.execute("""
            UPDATE stocks SET stock_name = ?, shares = ?, current_value = ? WHERE stock_id = ?
        """, (new_name, new_shares, new_value, stock_id))
        connection.commit()
        print("Stock updated successfully!")

    except sqlite3.Error as e:
        print("Error updating stock:", e)
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