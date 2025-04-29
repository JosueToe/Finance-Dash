import React, { useEffect, useState } from "react";
import api from "../services/api";

const IncomePage = () => {
  const [incomes, setIncomes] = useState([]);
  const [source, setSource] = useState("");
  const [amount, setAmount] = useState("");
  const [frequency, setFrequency] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editSource, setEditSource] = useState("");
  const [editAmount, setEditAmount] = useState("");
  const [editFrequency, setEditFrequency] = useState("");

  useEffect(() => {
    fetchIncome();
  }, []);

  const fetchIncome = () => {
    api.get("/income")
      .then(res => setIncomes(res.data))
      .catch(err => console.error("Error fetching income:", err));
  };

  const handleAdd = (e) => {
    e.preventDefault();
    api.post("/income", {
      source,
      amount: parseFloat(amount),
      frequency
    })
    .then(() => {
      setSource("");
      setAmount("");
      setFrequency("");
      fetchIncome();
    })
    .catch(err => console.error("Error adding income:", err));
  };

  const handleDelete = (id) => {
    if (window.confirm("Delete this income entry?")) {
      api.delete(`/income/${id}`)
        .then(() => fetchIncome())
        .catch(err => console.error("Error deleting income:", err));
    }
  };

  const startEdit = (income) => {
    setEditingId(income.income_id);
    setEditSource(income.source);
    setEditAmount(income.amount);
    setEditFrequency(income.frequency);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditSource("");
    setEditAmount("");
    setEditFrequency("");
  };

  const saveEdit = (id) => {
    api.put(`/income/${id}`, {
      source: editSource,
      amount: parseFloat(editAmount),
      frequency: editFrequency
    })
    .then(() => {
      cancelEdit();
      fetchIncome();
    })
    .catch(err => console.error("Error updating income:", err));
  };

  return (
    <div>
      <h1>Income Sources</h1>

      {/* Add Income Form */}
      <form onSubmit={handleAdd} style={{ marginBottom: "2rem" }}>
        <input
          type="text"
          placeholder="Source (e.g., Freelance)"
          value={source}
          onChange={(e) => setSource(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <input
          type="number"
          placeholder="Amount"
          value={amount}
          onChange={(e) => setAmount(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <input
          type="text"
          placeholder="Frequency (Monthly, Weekly)"
          value={frequency}
          onChange={(e) => setFrequency(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <button type="submit">Add Income</button>
      </form>

      {/* Income Table */}
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Income ID</th>
            <th>Source</th>
            <th>Amount</th>
            <th>Frequency</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {incomes.map((income) => (
            <tr key={income.income_id}>
              <td>{income.income_id}</td>

              <td>{editingId === income.income_id ? (
                <input
                  value={editSource}
                  onChange={(e) => setEditSource(e.target.value)}
                />
              ) : income.source}</td>

              <td>{editingId === income.income_id ? (
                <input
                  type="number"
                  value={editAmount}
                  onChange={(e) => setEditAmount(e.target.value)}
                />
              ) : `$${income.amount}`}</td>

              <td>{editingId === income.income_id ? (
                <input
                  value={editFrequency}
                  onChange={(e) => setEditFrequency(e.target.value)}
                />
              ) : income.frequency}</td>

              <td>
                {editingId === income.income_id ? (
                  <>
                    <button onClick={() => saveEdit(income.income_id)}>Save</button>
                    <button onClick={cancelEdit}>Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => startEdit(income)}>Edit</button>
                    <button onClick={() => handleDelete(income.income_id)}>Delete</button>
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

export default IncomePage;
