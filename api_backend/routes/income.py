from flask import Blueprint, request, jsonify
import sqlite3
import os

income_bp = Blueprint('income', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# ✅ Get all income entries
@income_bp.route('/income', methods=['GET'])
def get_income():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT income_id, source, amount, frequency FROM income")
        rows = cursor.fetchall()
        conn.close()

        incomes = [
            {
                "income_id": row[0],
                "source": row[1],
                "amount": row[2],
                "frequency": row[3]
            }
            for row in rows
        ]
        return jsonify(incomes), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Add a new income
@income_bp.route('/income', methods=['POST'])
def add_income():
    try:
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO income (source, amount, frequency)
            VALUES (?, ?, ?)
        """, (
            data['source'],
            data['amount'],
            data['frequency']
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Income added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Update an income
@income_bp.route('/income/<int:income_id>', methods=['PUT'])
def update_income(income_id):
    try:
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE income
            SET source = ?, amount = ?, frequency = ?
            WHERE income_id = ?
        """, (
            data['source'],
            data['amount'],
            data['frequency'],
            income_id
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Income updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Delete an income
@income_bp.route('/income/<int:income_id>', methods=['DELETE'])
def delete_income(income_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM income WHERE income_id = ?", (income_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Income deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
