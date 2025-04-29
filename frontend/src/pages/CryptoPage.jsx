import React, { useEffect, useState } from "react";
import api from "../services/api";

const CryptoPage = () => {
  const [cryptos, setCryptos] = useState([]);
  const [coinId, setCoinId] = useState("");
  const [coins, setCoins] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editCoinId, setEditCoinId] = useState("");
  const [editCoins, setEditCoins] = useState("");

  useEffect(() => {
    fetchCryptos();
  }, []);

  const fetchCryptos = () => {
    api.get("/cryptos")
      .then(res => setCryptos(res.data))
      .catch(err => console.error("Error fetching cryptos:", err));
  };

  const handleAdd = (e) => {
    e.preventDefault();
    api.post("/cryptos", {
      coin_id: coinId,
      coins: parseFloat(coins)
    })
    .then(() => {
      setCoinId("");
      setCoins("");
      fetchCryptos();
    })
    .catch(err => console.error("Error adding crypto:", err));
  };

  const handleDelete = (id) => {
    if (window.confirm("Delete this crypto?")) {
      api.delete(`/cryptos/${id}`)
        .then(() => fetchCryptos())
        .catch(err => console.error("Error deleting:", err));
    }
  };

  const startEdit = (crypto) => {
    setEditingId(crypto.crypto_id);
    setEditCoinId(crypto.coin_id);
    setEditCoins(crypto.coins);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditCoinId("");
    setEditCoins("");
  };

  const saveEdit = (id) => {
    api.put(`/cryptos/${id}`, {
      coin_id: editCoinId,
      coins: parseFloat(editCoins)
    })
    .then(() => {
      cancelEdit();
      fetchCryptos();
    })
    .catch(err => console.error("Error saving:", err));
  };

  return (
    <div>
      <h1>Crypto Holdings</h1>

      <form onSubmit={handleAdd} style={{ marginBottom: "2rem" }}>
        <input
          type="text"
          placeholder="Coin ID (e.g. ethereum)"
          value={coinId}
          onChange={(e) => setCoinId(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <input
          type="number"
          placeholder="Amount of coins"
          value={coins}
          onChange={(e) => setCoins(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <button type="submit">Add</button>
      </form>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Coin ID</th>
            <th>Coin Name</th>
            <th>Coins</th>
            <th>Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {cryptos.map((c) => (
            <tr key={c.crypto_id}>
              <td>{editingId === c.crypto_id ? (
                <input value={editCoinId} onChange={(e) => setEditCoinId(e.target.value)} />
              ) : c.coin_id}</td>

              <td>{c.coin_name}</td>

              <td>{editingId === c.crypto_id ? (
                <input
                  type="number"
                  value={editCoins}
                  onChange={(e) => setEditCoins(e.target.value)}
                />
              ) : c.coins}</td>

              <td>${c.current_value}</td>

              <td>
                {editingId === c.crypto_id ? (
                  <>
                    <button onClick={() => saveEdit(c.crypto_id)}>Save</button>
                    <button onClick={cancelEdit}>Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => startEdit(c)}>Edit</button>
                    <button onClick={() => handleDelete(c.crypto_id)}>Delete</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CryptoPage;
