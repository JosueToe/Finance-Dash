from flask import Blueprint, request, jsonify
import sqlite3
import os
import yfinance as yf

stocks_bp = Blueprint('stocks', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# 🔧 Helper: Fetch live stock price
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        price = stock.history(period="1d")['Close'].iloc[-1]
        return float(price)
    except Exception:
        return 0.0

# ✅ Get all stocks
@stocks_bp.route('/stocks', methods=['GET'])
def get_stocks():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT stock_id, stock_name, shares, current_value FROM stocks")
        rows = cursor.fetchall()
        conn.close()

        stocks = [
            {
                "stock_id": row[0],
                "stock_name": row[1],
                "shares": row[2],
                "current_value": row[3]
            }
            for row in rows
        ]
        return jsonify(stocks), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Add a new stock
@stocks_bp.route('/stocks', methods=['POST'])
def add_stock():
    try:
        data = request.get_json()
        stock_name = data['stock_name'].upper()  # Force uppercase
        shares = data['shares']

        current_price = get_stock_price(stock_name)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stocks (stock_name, shares, current_value)
            VALUES (?, ?, ?)
        """, (stock_name, shares, current_price))
        conn.commit()
        conn.close()

        return jsonify({"message": "Stock added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Update a stock
@stocks_bp.route('/stocks/<int:stock_id>', methods=['PUT'])
def update_stock(stock_id):
    try:
        data = request.get_json()
        stock_name = data['stock_name'].upper()  # Force uppercase
        shares = data['shares']

        current_price = get_stock_price(stock_name)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE stocks
            SET stock_name = ?, shares = ?, current_value = ?
            WHERE stock_id = ?
        """, (stock_name, shares, current_price, stock_id))
        conn.commit()
        conn.close()

        return jsonify({"message": "Stock updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Delete a stock
@stocks_bp.route('/stocks/<int:stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM stocks WHERE stock_id = ?", (stock_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Stock deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
