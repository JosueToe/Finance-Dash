import React, { useEffect, useState } from "react";
import api from "../services/api";

const BankPage = () => {
  const [accounts, setAccounts] = useState([]);
  const [newAccountType, setNewAccountType] = useState("");
  const [newBalance, setNewBalance] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editedAccountType, setEditedAccountType] = useState("");
  const [editedBalance, setEditedBalance] = useState("");

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = () => {
    api.get("/bank")
      .then(response => {
        setAccounts(response.data);
      })
      .catch(error => {
        console.error("Error fetching bank accounts:", error);
      });
  };

  const handleAddAccount = (e) => {
    e.preventDefault();
    api.post("/bank", {
      account_type: newAccountType,
      balance: parseFloat(newBalance)
    })
    .then(() => {
      setNewAccountType("");
      setNewBalance("");
      fetchAccounts();
    })
    .catch(error => {
      console.error("Error adding account:", error);
    });
  };

  const handleDelete = (id) => {
    if (window.confirm("Are you sure you want to delete this account?")) {
      api.delete(`/bank/${id}`)
        .then(() => {
          fetchAccounts();
        })
        .catch(error => {
          console.error("Error deleting account:", error);
        });
    }
  };

  const startEditing = (account) => {
    setEditingId(account.account_id);
    setEditedAccountType(account.account_type);
    setEditedBalance(account.balance);
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditedAccountType("");
    setEditedBalance("");
  };

  const handleSaveEdit = (id) => {
    api.put(`/bank/${id}`, {
      account_type: editedAccountType,
      balance: parseFloat(editedBalance)
    })
    .then(() => {
      setEditingId(null);
      fetchAccounts();
    })
    .catch(error => {
      console.error("Error updating account:", error);
    });
  };

  return (
    <div>
      <h1>Bank Accounts</h1>

      <form onSubmit={handleAddAccount} style={{ marginBottom: "2rem" }}>
        <input
          type="text"
          placeholder="Account Type"
          value={newAccountType}
          onChange={(e) => setNewAccountType(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <input
          type="number"
          placeholder="Balance"
          value={newBalance}
          onChange={(e) => setNewBalance(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <button type="submit">Add Account</button>
      </form>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Account ID</th>
            <th>Account Type</th>
            <th>Balance</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {accounts.map((account) => (
            <tr key={account.account_id}>
              <td>{account.account_id}</td>

              <td>
                {editingId === account.account_id ? (
                  <input
                    type="text"
                    value={editedAccountType}
                    onChange={(e) => setEditedAccountType(e.target.value)}
                  />
                ) : (
                  account.account_type
                )}
              </td>

              <td>
                {editingId === account.account_id ? (
                  <input
                    type="number"
                    value={editedBalance}
                    onChange={(e) => setEditedBalance(e.target.value)}
                  />
                ) : (
                  `$${account.balance}`
                )}
              </td>

              <td>
                {editingId === account.account_id ? (
                  <>
                    <button onClick={() => handleSaveEdit(account.account_id)}>Save</button>
                    <button onClick={cancelEditing}>Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => startEditing(account)}>Edit</button>
                    <button onClick={() => handleDelete(account.account_id)} style={{ marginLeft: "0.5rem" }}>Delete</button>
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

export default BankPage;
