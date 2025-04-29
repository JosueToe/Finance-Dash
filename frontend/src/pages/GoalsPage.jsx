import React, { useEffect, useState } from "react";
import api from "../services/api";

const GoalsPage = () => {
  const [goals, setGoals] = useState([]);
  const [netWorthTarget, setNetWorthTarget] = useState("");
  const [targetDate, setTargetDate] = useState("");

  const [editingId, setEditingId] = useState(null);
  const [editNetWorthTarget, setEditNetWorthTarget] = useState("");
  const [editTargetDate, setEditTargetDate] = useState("");

  useEffect(() => {
    fetchGoals();
  }, []);

  const fetchGoals = () => {
    api.get("/goals")
      .then(res => setGoals(res.data))
      .catch(err => console.error("Error fetching goals:", err));
  };

  const handleAdd = (e) => {
    e.preventDefault();
    api.post("/goals", {
      net_worth_target: parseFloat(netWorthTarget),
      target_date: targetDate
    })
    .then(() => {
      setNetWorthTarget("");
      setTargetDate("");
      fetchGoals();
    })
    .catch(err => console.error("Error adding goal:", err));
  };

  const handleDelete = (id) => {
    if (window.confirm("Delete this goal?")) {
      api.delete(`/goals/${id}`)
        .then(() => fetchGoals())
        .catch(err => console.error("Error deleting goal:", err));
    }
  };

  const startEdit = (goal) => {
    setEditingId(goal.goal_id);
    setEditNetWorthTarget(goal.net_worth_target);
    setEditTargetDate(goal.target_date);
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditNetWorthTarget("");
    setEditTargetDate("");
  };

  const saveEdit = (id) => {
    api.put(`/goals/${id}`, {
      net_worth_target: parseFloat(editNetWorthTarget),
      target_date: editTargetDate
    })
    .then(() => {
      cancelEdit();
      fetchGoals();
    })
    .catch(err => console.error("Error updating goal:", err));
  };

  return (
    <div>
      <h1>Financial Goals</h1>

      <form onSubmit={handleAdd} style={{ marginBottom: "2rem" }}>
        <input
          type="number"
          placeholder="Net Worth Target"
          value={netWorthTarget}
          onChange={(e) => setNetWorthTarget(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <input
          type="date"
          placeholder="Target Date"
          value={targetDate}
          onChange={(e) => setTargetDate(e.target.value)}
          required
          style={{ marginRight: "1rem" }}
        />
        <button type="submit">Add Goal</button>
      </form>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>Goal ID</th>
            <th>Net Worth Target ($)</th>
            <th>Target Date</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {goals.map((goal) => (
            <tr key={goal.goal_id}>
              <td>{goal.goal_id}</td>

              <td>{editingId === goal.goal_id ? (
                <input
                  type="number"
                  value={editNetWorthTarget}
                  onChange={(e) => setEditNetWorthTarget(e.target.value)}
                />
              ) : `$${goal.net_worth_target}`}</td>

              <td>{editingId === goal.goal_id ? (
                <input
                  type="date"
                  value={editTargetDate}
                  onChange={(e) => setEditTargetDate(e.target.value)}
                />
              ) : goal.target_date}</td>

              <td>
                {editingId === goal.goal_id ? (
                  <>
                    <button onClick={() => saveEdit(goal.goal_id)}>Save</button>
                    <button onClick={cancelEdit}>Cancel</button>
                  </>
                ) : (
                  <>
                    <button onClick={() => startEdit(goal)}>Edit</button>
                    <button onClick={() => handleDelete(goal.goal_id)}>Delete</button>
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

export default GoalsPage;
