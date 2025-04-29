from flask import Blueprint, request, jsonify
import sqlite3
import os
import requests

crypto_bp = Blueprint('crypto', __name__)

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Dashboard/database/finance_dashboard.db'))

# 🧠 Coin ID aliases (common symbols → CoinGecko IDs)
coin_id_aliases = {
    "btc": "bitcoin",
    "bitcoin": "bitcoin",

    "eth": "ethereum",
    "ethereum": "ethereum",

    "xrp": "ripple",
    "ripple": "ripple",

    "doge": "dogecoin",
    "dogecoin": "dogecoin",

    "ada": "cardano",
    "cardano": "cardano",

    "sol": "solana",
    "solana": "solana",

    "dot": "polkadot",
    "polkadot": "polkadot",

    "ltc": "litecoin",
    "litecoin": "litecoin",

    "bch": "bitcoin-cash",
    "bitcoin cash": "bitcoin-cash",
    "bitcoin-cash": "bitcoin-cash",

    "matic": "matic-network",
    "polygon": "matic-network",

    "shib": "shiba-inu",
    "shiba": "shiba-inu",
    "shiba inu": "shiba-inu",

    "avax": "avalanche-2",
    "avalanche": "avalanche-2",

    "uni": "uniswap",
    "uniswap": "uniswap",

    "link": "chainlink",
    "chainlink": "chainlink"
}

# 🔧 Get live price
def get_crypto_price(coin_id):
    try:
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd')
        if response.status_code == 200:
            return response.json()[coin_id]["usd"]
        else:
            return 0.0
    except Exception:
        return 0.0

# ✅ Get all cryptos
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

# ✅ Add new crypto
@crypto_bp.route('/cryptos', methods=['POST'])
def add_crypto():
    try:
        data = request.get_json()
        user_input = data['coin_id'].lower()
        coin_id = coin_id_aliases.get(user_input, user_input)

        response = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin_id}')
        if response.status_code != 200:
            return jsonify({"error": f"Coin ID '{coin_id}' not found."}), 400

        coin_name = response.json().get("name", "Unknown")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cryptos (coin_name, coins, current_value, coin_id)
            VALUES (?, ?, ?, ?)
        """, (
            coin_name,
            data['coins'],
            get_crypto_price(coin_id),
            coin_id
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Crypto added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Update existing crypto
@crypto_bp.route('/cryptos/<int:crypto_id>', methods=['PUT'])
def update_crypto(crypto_id):
    try:
        data = request.get_json()
        user_input = data['coin_id'].lower()
        coin_id = coin_id_aliases.get(user_input, user_input)

        response = requests.get(f'https://api.coingecko.com/api/v3/coins/{coin_id}')
        if response.status_code != 200:
            return jsonify({"error": f"Coin ID '{coin_id}' not found."}), 400

        coin_name = response.json().get("name", "Unknown")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE cryptos
            SET coin_name = ?, coin_id = ?, coins = ?, current_value = ?
            WHERE crypto_id = ?
        """, (
            coin_name,
            coin_id,
            data['coins'],
            get_crypto_price(coin_id),
            crypto_id
        ))
        conn.commit()
        conn.close()
        return jsonify({"message": "Crypto updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ✅ Delete crypto
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
