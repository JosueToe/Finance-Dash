import React, { useEffect, useState } from "react";
import api from "../services/api";

const DashboardPage = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    api.get("/dashboard")
      .then((response) => {
        setData(response.data);
      })
      .catch((error) => {
        console.error("Error fetching dashboard data:", error);
      });
  }, []);

  if (!data) return <div>Loading...</div>;

  return (
    <div style={{ padding: "2rem" }}>
      <h1>Finance Dashboard</h1>
      <p><strong>Total Net Worth:</strong> ${data.total_net_worth}</p>
      <p><strong>Total Monthly Income:</strong> ${data.total_monthly_income}</p>
      <p><strong>Total Monthly Expenses:</strong> ${data.total_monthly_expenses}</p>
      <p><strong>Goal Target:</strong> ${data.goal_target || "No goal set"}</p>
      <p><strong>Goal Progress:</strong> {data.goal_progress ? `${data.goal_progress}%` : "No goal"}</p>
    </div>
  );
};

export default DashboardPage;
