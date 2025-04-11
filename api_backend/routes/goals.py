# api_backend/routes/goals.py

from flask import Blueprint, jsonify, request
import sqlite3
import os

goals_bp = Blueprint('goals', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# GET all goals
@goals_bp.route('/goals', methods=['GET'])
def get_goals():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT goal_id, net_worth_target, target_date FROM goals")
        rows = cursor.fetchall()
        conn.close()

        goals = [
            {"goal_id": row[0], "net_worth_target": row[1], "target_date": row[2]}
            for row in rows
        ]
        return jsonify(goals), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST - Add goal
@goals_bp.route('/goals', methods=['POST'])
def add_goal():
    try:
        data = request.get_json()
        required_fields = ['net_worth_target', 'target_date']

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO goals (net_worth_target, target_date)
            VALUES (?, ?)
        """, (
            data['net_worth_target'],
            data['target_date']
        ))
        conn.commit()
        conn.close()

        return jsonify({"message": "Goal added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT - Update goal
@goals_bp.route('/goals/<int:goal_id>', methods=['PUT'])
def update_goal(goal_id):
    try:
        data = request.get_json()
        fields = ['net_worth_target', 'target_date']
        updates = [f"{field} = ?" for field in fields if field in data]

        if not updates:
            return jsonify({"error": "No valid fields provided for update"}), 400

        values = [data[field] for field in fields if field in data]
        values.append(goal_id)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE goals
            SET {', '.join(updates)}
            WHERE goal_id = ?
        """, values)
        conn.commit()
        conn.close()

        return jsonify({"message": "Goal updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE - Delete goal
@goals_bp.route('/goals/<int:goal_id>', methods=['DELETE'])
def delete_goal(goal_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Goal deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
