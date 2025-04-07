# api_backend/app.py

from flask import Flask
from flask_cors import CORS
from routes.stocks import stocks_bp  # Import your stocks blueprint
from routes.crypto import crypto_bp



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Register blueprints
app.register_blueprint(stocks_bp)
app.register_blueprint(crypto_bp)

if __name__ == '__main__':
    app.run(debug=True)
