# api_backend/app.py

from flask import Flask
from flask_cors import CORS
from routes.stocks import stocks_bp  # Import your stocks blueprint
from routes.crypto import crypto_bp
from routes.bank import bank_bp
from routes.salary import salary_bp
from routes.expenses import expenses_bp
from routes.goals import goals_bp
from routes.dashboard import dashboard_bp
from routes.income import income_bp
from routes.debts import debts_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(stocks_bp)
app.register_blueprint(crypto_bp)
app.register_blueprint(bank_bp)
app.register_blueprint(salary_bp)
app.register_blueprint(expenses_bp)
app.register_blueprint(goals_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(income_bp)
app.register_blueprint(debts_bp)

if __name__ == '__main__':
    app.run(debug=True)
