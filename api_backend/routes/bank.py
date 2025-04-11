# api_backend/routes/bank.py

from flask import Blueprint, jsonify, request
import sqlite3
import os

bank_bp = Blueprint('bank', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# GET all bank accounts
@bank_bp.route('/bank', methods=['GET'])
def get_bank_accounts():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT account_id, account_type, balance FROM bank_accounts")
        rows = cursor.fetchall()
        conn.close()

        accounts = [
            {"account_id": row[0], "account_type": row[1], "balance": row[2]}
            for row in rows
        ]
        return jsonify(accounts), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST - Add a new bank account
@bank_bp.route('/bank', methods=['POST'])
def add_bank_account():
    try:
        data = request.get_json()
        required_fields = ['account_type', 'balance']

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO bank_accounts (account_type, balance)
            VALUES (?, ?)
        """, (data['account_type'], data['balance']))
        conn.commit()
        conn.close()

        return jsonify({"message": "Bank account added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT - Update bank account
@bank_bp.route('/bank/<int:account_id>', methods=['PUT'])
def update_bank_account(account_id):
    try:
        data = request.get_json()
        fields = ['account_type', 'balance']
        updates = [f"{field} = ?" for field in fields if field in data]

        if not updates:
            return jsonify({"error": "No valid fields provided for update"}), 400

        values = [data[field] for field in fields if field in data]
        values.append(account_id)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE bank_accounts
            SET {', '.join(updates)}
            WHERE account_id = ?
        """, values)
        conn.commit()
        conn.close()

        return jsonify({"message": "Bank account updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE - Remove a bank account
@bank_bp.route('/bank/<int:account_id>', methods=['DELETE'])
def delete_bank_account(account_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bank_accounts WHERE account_id = ?", (account_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Bank account deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
