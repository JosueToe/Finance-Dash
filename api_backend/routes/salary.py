# api_backend/routes/salary.py

from flask import Blueprint, jsonify, request
import sqlite3
import os

salary_bp = Blueprint('salary', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# GET all salaries
@salary_bp.route('/salary', methods=['GET'])
def get_salaries():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT salary_id, amount, frequency, next_payment_date FROM salary")
        rows = cursor.fetchall()
        conn.close()

        salaries = [
            {"salary_id": row[0], "amount": row[1], "frequency": row[2], "next_payment_date": row[3]}
            for row in rows
        ]
        return jsonify(salaries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST - Add a salary
@salary_bp.route('/salary', methods=['POST'])
def add_salary():
    try:
        data = request.get_json()
        required_fields = ['amount', 'frequency', 'next_payment_date']

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO salary (amount, frequency, next_payment_date)
            VALUES (?, ?, ?)
        """, (
            data['amount'],
            data['frequency'],
            data['next_payment_date']
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Salary added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT - Update salary
@salary_bp.route('/salary/<int:salary_id>', methods=['PUT'])
def update_salary(salary_id):
    try:
        data = request.get_json()
        fields = ['amount', 'frequency', 'next_payment_date']
        updates = [f"{field} = ?" for field in fields if field in data]

        if not updates:
            return jsonify({"error": "No valid fields provided for update"}), 400

        values = [data[field] for field in fields if field in data]
        values.append(salary_id)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE salary
            SET {', '.join(updates)}
            WHERE salary_id = ?
        """, values)
        conn.commit()
        conn.close()

        return jsonify({"message": "Salary updated!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE - Remove salary
@salary_bp.route('/salary/<int:salary_id>', methods=['DELETE'])
def delete_salary(salary_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM salary WHERE salary_id = ?", (salary_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Salary deleted!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
