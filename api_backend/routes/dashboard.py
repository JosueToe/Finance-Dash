# api_backend/routes/dashboard.py

from flask import Blueprint, jsonify
import sqlite3
import os

dashboard_bp = Blueprint('dashboard', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

def get_monthly_multiplier(freq):
    return {
        "weekly": 4.33,
        "biweekly": 2.16,
        "monthly": 1,
        "annually": 1/12
    }.get(freq.lower(), 1)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard_summary():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Net Worth = bank + crypto + stocks
        cursor.execute("SELECT SUM(balance) FROM bank_accounts")
        bank_total = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(shares * current_value) FROM stocks")
        stocks_total = cursor.fetchone()[0] or 0

        cursor.execute("SELECT SUM(coins * current_value) FROM cryptos")
        crypto_total = cursor.fetchone()[0] or 0

        total_net_worth = bank_total + stocks_total + crypto_total

        # Monthly Income from salaries
        cursor.execute("SELECT amount, frequency FROM salary")
        salary_rows = cursor.fetchall()
        total_monthly_income = sum(
            amount * get_monthly_multiplier(freq)
            for amount, freq in salary_rows
        )

        # Monthly Expenses
        cursor.execute("SELECT amount, frequency FROM expenses")
        expense_rows = cursor.fetchall()
        total_monthly_expenses = sum(
            amount * get_monthly_multiplier(freq)
            for amount, freq in expense_rows
        )

        # Goal progress (based on the first goal in table)
        cursor.execute("SELECT net_worth_target FROM goals LIMIT 1")
        goal_target_row = cursor.fetchone()
        if goal_target_row:
            goal_target = goal_target_row[0]
            goal_progress = round((total_net_worth / goal_target) * 100, 2)
        else:
            goal_target = None
            goal_progress = None

        conn.close()

        return jsonify({
            "total_net_worth": round(total_net_worth, 2),
            "total_monthly_income": round(total_monthly_income, 2),
            "total_monthly_expenses": round(total_monthly_expenses, 2),
            "goal_target": goal_target,
            "goal_progress": goal_progress
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
