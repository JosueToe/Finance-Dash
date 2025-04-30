from flask import Blueprint, jsonify, request
import sqlite3
import os

expenses_bp = Blueprint('expenses', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# GET all expenses
@expenses_bp.route('/expenses', methods=['GET'])
def get_expenses():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT expense_id, category, frequency, amount FROM expenses")
        rows = cursor.fetchall()
        conn.close()

        expenses = [
            {
                "expense_id": row[0],
                "category": row[1],
                "frequency": row[2],
                "amount": row[3]
            }
            for row in rows
        ]
        return jsonify(expenses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST - Add an expense
@expenses_bp.route('/expenses', methods=['POST'])
def add_expense():
    try:
        data = request.get_json()
        required_fields = ['category', 'frequency', 'amount']

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (category, frequency, amount)
            VALUES (?, ?, ?)
        """, (
            data['category'],
            data['frequency'],
            data['amount']
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Expense added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT - Update an expense
@expenses_bp.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    try:
        data = request.get_json()
        fields = ['category', 'frequency', 'amount']
        updates = [f"{field} = ?" for field in fields if field in data]

        if not updates:
            return jsonify({"error": "No valid fields provided for update"}), 400

        values = [data[field] for field in fields if field in data]
        values.append(expense_id)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE expenses
            SET {', '.join(updates)}
            WHERE expense_id = ?
        """, values)
        conn.commit()
        conn.close()

        return jsonify({"message": "Expense updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE - Remove an expense
@expenses_bp.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE expense_id = ?", (expense_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Expense deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
