import React, { useEffect, useState } from "react";
import api from "../services/api";

const StocksPage = () => {
  const [stocks, setStocks] = useState([]);
  const [ticker, setTicker] = useState("");
  const [shares, setShares] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editTicker, setEditTicker] = useState("");
  const [editShares, setEditShares] = useState("");

  useEffect(() => {
    fetchStocks();
  }, []);

  const fetchStocks = () => {
    api.get("/stocks")
      .then(res => setStocks(res.data))
      .catch(err => console.error("Error fetching stocks:", err));
  };

  const handleAdd = (e) => {
    e.preventDefault();
    api.post("/stocks", {
      stock_name: ticker.toUpperCase(), // Force uppercase
      shares: parseFloat(shares)
    })
    .then(() => {
      setTicker("");
      setShares("");
      fetchStocks();
    })
    .catch(err => console.error("Error adding stock:", err));
  };

  const handleDelete = (id) => {
    if (window.confirm("Delete this stock?")) {
      api.delete(`/stocks/${id}`)
        .then(() => fetchStocks())
        .catch(err => console.error("Error deleting stock:", err));
    }
  };

  const startEdit = (stock) => {
    setEditingId(stock.stock_id);
    setEditTicker(stock.stock_name);
    setEditShares(stock.shares);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditTicker("");
    setEditShares("");
  };

  const saveEdit = (id) => {
    api.put(`/stocks/${id}`, {
      stock_name: editTicker.toUpperCase(), // Force uppercase
      shares: parseFloat(editShares)
    })
    .then(() => {
      cancelEdit();
      fetchStocks();
    })
    .catch(err => console.error("Error saving stock:", err));
  };

  return (
    <div>
      <h1>Stock Holdings</h1>

      <form onSubmit={handleAdd} style={{ marginBottom: "2rem" }}>
        <input
          type="text"
          placeholder="Stock Ticker (e.g. AAPL)"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <input
          type="number"
          placeholder="Shares"
          value={shares}
          onChange={(e) => setShares(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <button type="submit">Add Stock</button>
      </form>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Ticker</th>
            <th>Shares</th>
            <th>Current Price</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {stocks.map((stock) => (
            <tr key={stock.stock_id}>
              <td>{editingId === stock.stock_id ? (
                <input value={editTicker} onChange={(e) => setEditTicker(e.target.value)} />
              ) : stock.stock_name}</td>

              <td>{editingId === stock.stock_id ? (
                <input
                  type="number"
                  value={editShares}
                  onChange={(e) => setEditShares(e.target.value)}
                />
              ) : stock.shares}</td>

              <td>${stock.current_value}</td>

              <td>
                {editingId === stock.stock_id ? (
                  <>
                    <button onClick={() => saveEdit(stock.stock_id)}>Save</button>
                    <button onClick={cancelEdit}>Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => startEdit(stock)}>Edit</button>
                    <button onClick={() => handleDelete(stock.stock_id)}>Delete</button>
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

export default StocksPage;
