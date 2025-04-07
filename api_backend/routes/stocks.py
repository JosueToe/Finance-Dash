# api_backend/routes/stocks.py

from flask import Blueprint, jsonify
import sqlite3
import os

stocks_bp = Blueprint('stocks', __name__)

# Define path to your existing database
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# api_backend/routes/stocks.py

@stocks_bp.route('/stocks', methods=['GET'])
def get_stocks():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT stock_id, stock_name, shares, current_value, stock_ticker FROM stocks")
        rows = cursor.fetchall()
        conn.close()

        stocks = [
            {
                "stock_id": row[0],
                "stock_name": row[1],
                "shares": row[2],
                "current_value": row[3],
                "stock_ticker": row[4]
            }
            for row in rows
        ]

        return jsonify(stocks), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import request  # Add this at the top if not already

@stocks_bp.route('/stocks', methods=['POST'])
def add_stock():
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ['stock_name', 'shares', 'current_value', 'stock_ticker']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO stocks (stock_name, shares, current_value, stock_ticker)
            VALUES (?, ?, ?, ?)
        """, (
            data['stock_name'],
            data['shares'],
            data['current_value'],
            data['stock_ticker']
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Stock added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@stocks_bp.route('/stocks/<int:stock_id>', methods=['PUT'])
def update_stock(stock_id):
    try:
        data = request.get_json()

        fields = ['stock_name', 'shares', 'current_value', 'stock_ticker']
        updates = [f"{field} = ?" for field in fields if field in data]

        if not updates:
            return jsonify({"error": "No valid fields provided for update"}), 400

        values = [data[field] for field in fields if field in data]
        values.append(stock_id)  # Add stock_id for WHERE clause

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE stocks
            SET {', '.join(updates)}
            WHERE stock_id = ?
        """, values)

        conn.commit()
        conn.close()

        return jsonify({"message": "Stock updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
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
