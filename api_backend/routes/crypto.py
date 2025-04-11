# api_backend/routes/crypto.py

from flask import Blueprint, jsonify, request
import sqlite3
import os
import requests

def fetch_crypto_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get(coin_id, {}).get('usd', None)
    except:
        return None


crypto_bp = Blueprint('crypto', __name__)

# Path to the shared database
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# ✅ GET /cryptos - Retrieve all crypto entries
@crypto_bp.route('/cryptos', methods=['GET'])
def get_cryptos():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT crypto_id, coin_name, coins, current_value, coin_id FROM cryptos")
        rows = cursor.fetchall()
        conn.close()

        cryptos = [
            {
                "crypto_id": row[0],
                "coin_name": row[1],
                "coins": row[2],
                "current_value": row[3],
                "coin_id": row[4]
            }
            for row in rows
        ]

        return jsonify(cryptos), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ POST /cryptos - Add a new crypto
@crypto_bp.route('/cryptos', methods=['POST'])
def add_crypto():
    try:
        data = request.get_json()
        required_fields = ['coin_name', 'coins', 'coin_id']

        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Fetch live price
        live_price = fetch_crypto_price(data['coin_id'])
        if live_price is None:
            return jsonify({"error": "Failed to fetch live price from CoinGecko"}), 500

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO cryptos (coin_name, coins, current_value, coin_id)
            VALUES (?, ?, ?, ?)
        """, (
            data['coin_name'],
            data['coins'],
            live_price,
            data['coin_id']
        ))

        conn.commit()
        conn.close()

        return jsonify({"message": "Crypto added with live price!", "price": live_price}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ PUT /cryptos/<crypto_id> - Update a crypto entry
@crypto_bp.route('/cryptos/<int:crypto_id>', methods=['PUT'])
def update_crypto(crypto_id):
    try:
        data = request.get_json()
        fields = ['coin_name', 'coins', 'coin_id']
        updates = []
        values = []

        if 'coin_id' in data:
            live_price = fetch_crypto_price(data['coin_id'])
            if live_price is None:
                return jsonify({"error": "Failed to fetch live price from CoinGecko"}), 500
            updates.append("current_value = ?")
            values.append(live_price)

        for field in fields:
            if field in data:
                updates.append(f"{field} = ?")
                values.append(data[field])

        if not updates:
            return jsonify({"error": "No valid fields provided for update"}), 400

        values.append(crypto_id)

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(f"""
            UPDATE cryptos
            SET {', '.join(updates)}
            WHERE crypto_id = ?
        """, values)

        conn.commit()
        conn.close()

        return jsonify({"message": "Crypto updated successfully", "price": live_price if 'coin_id' in data else "unchanged"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ✅ DELETE /cryptos/<crypto_id> - Delete a crypto entry
@crypto_bp.route('/cryptos/<int:crypto_id>', methods=['DELETE'])
def delete_crypto(crypto_id):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cryptos WHERE crypto_id = ?", (crypto_id,))
        conn.commit()
        conn.close()

        return jsonify({"message": "Crypto deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
