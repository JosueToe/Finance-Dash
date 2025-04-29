from flask import Blueprint, request, jsonify
import sqlite3
import os

debts_bp = Blueprint('debts', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# ✅ Get all debts
@debts_bp.route('/debts', methods=['GET'])
def get_debts():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT debt_id, creditor, balance, minimum_payment, due_date FROM debts")
        rows = cursor.fetchall()
        conn.close()

        debts = [
            {
                "debt_id": row[0],
                "creditor": row[1],
                "balance": row[2],
                "minimum_payment": row[3],
                "due_date": row[4]
            }
            for row in rows
        ]
        return jsonify(debts), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Add a new debt
@debts_bp.route('/debts', methods=['POST'])
def add_debt():
    try:
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO debts (creditor, balance, minimum_payment, due_date)
            VALUES (?, ?, ?, ?)
        """, (
            data['creditor'],
            data['balance'],
            data['minimum_payment'],
            data['due_date']
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Debt added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Update a debt
@debts_bp.route('/debts/<int:debt_id>', methods=['PUT'])
def update_debt(debt_id):
    try:
        data = request.get_json()
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE debts
            SET creditor = ?, balance = ?, minimum_payment = ?, due_date = ?
            WHERE debt_id = ?
        """, (
            data['creditor'],
            data['balance'],
            data['minimum_payment'],
            data['due_date'],
            debt_id
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Debt updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Delete a debt
@debts_bp.route('/debts/<int:debt_id>', methods=['DELETE'])
def delete_debt(debt_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM debts WHERE debt_id = ?", (debt_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Debt deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
