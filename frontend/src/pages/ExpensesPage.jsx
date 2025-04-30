import React, { useEffect, useState } from "react";
import api from "../services/api";

const ExpensesPage = () => {
  const [expenses, setExpenses] = useState([]);
  const [category, setCategory] = useState("");
  const [frequency, setFrequency] = useState("");
  const [amount, setAmount] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editCategory, setEditCategory] = useState("");
  const [editFrequency, setEditFrequency] = useState("");
  const [editAmount, setEditAmount] = useState("");

  useEffect(() => {
    fetchExpenses();
  }, []);

  const fetchExpenses = () => {
    api.get("/expenses")
      .then(res => setExpenses(res.data))
      .catch(err => console.error("Error fetching expenses:", err));
  };

  const handleAdd = (e) => {
    e.preventDefault();
    api.post("/expenses", {
      category,
      frequency,
      amount: parseFloat(amount)
    })
    .then(() => {
      setCategory("");
      setFrequency("");
      setAmount("");
      fetchExpenses();
    })
    .catch(err => console.error("Error adding expense:", err));
  };

  const handleDelete = (id) => {
    if (window.confirm("Delete this expense?")) {
      api.delete(`/expenses/${id}`)
        .then(() => fetchExpenses())
        .catch(err => console.error("Error deleting expense:", err));
    }
  };

  const startEdit = (expense) => {
    setEditingId(expense.expense_id);
    setEditCategory(expense.category);
    setEditFrequency(expense.frequency);
    setEditAmount(expense.amount);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditCategory("");
    setEditFrequency("");
    setEditAmount("");
  };

  const saveEdit = (id) => {
    api.put(`/expenses/${id}`, {
      category: editCategory,
      frequency: editFrequency,
      amount: parseFloat(editAmount)
    })
    .then(() => {
      cancelEdit();
      fetchExpenses();
    })
    .catch(err => console.error("Error updating expense:", err));
  };

  return (
    <div>
      <h1>Expenses</h1>

      {/* Add Expense Form */}
      <form onSubmit={handleAdd} style={{ marginBottom: "2rem" }}>
        <input
          type="text"
          placeholder="Category (e.g., Rent)"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <input
          type="text"
          placeholder="Frequency (e.g., Monthly)"
          value={frequency}
          onChange={(e) => setFrequency(e.target.value)}
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
        <button type="submit">Add Expense</button>
      </form>

      {/* Expenses Table */}
      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Category</th>
            <th>Frequency</th>
            <th>Amount</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map((expense) => (
            <tr key={expense.expense_id}>
              <td>{editingId === expense.expense_id ? (
                <input
                  value={editCategory}
                  onChange={(e) => setEditCategory(e.target.value)}
                />
              ) : expense.category}</td>

              <td>{editingId === expense.expense_id ? (
                <input
                  value={editFrequency}
                  onChange={(e) => setEditFrequency(e.target.value)}
                />
              ) : expense.frequency}</td>

              <td>{editingId === expense.expense_id ? (
                <input
                  type="number"
                  value={editAmount}
                  onChange={(e) => setEditAmount(e.target.value)}
                />
              ) : `$${expense.amount}`}</td>

              <td>
                {editingId === expense.expense_id ? (
                  <>
                    <button onClick={() => saveEdit(expense.expense_id)}>Save</button>
                    <button onClick={cancelEdit}>Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => startEdit(expense)}>Edit</button>
                    <button onClick={() => handleDelete(expense.expense_id)}>Delete</button>
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

export default ExpensesPage;
