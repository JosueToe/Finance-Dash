import React, { useEffect, useState } from "react";
import api from "../services/api";

const DashboardPage = () => {
  const [dashboardData, setDashboardData] = useState({
    totalNetWorth: 0,
    totalIncome: 0,
    totalExpenses: 0,
    totalBankBalance: 0,
    totalStockValue: 0,
    totalCryptoValue: 0,
    totalSalary: 0,
    totalDebt: 0,
    goalTarget: null,
    goalProgress: null
  });

  useEffect(() => {
    api.get("/dashboard")
      .then(res => setDashboardData(res.data))
      .catch(err => console.error("Error loading dashboard:", err));
  }, []);

  return (
    <div>
      <h1>Finance Dashboard</h1>

      <h2>Total Net Worth: ${dashboardData.total_net_worth}</h2>
<p>Total Monthly Income: ${dashboardData.total_monthly_income}</p>
<p>Total Monthly Expenses: ${dashboardData.total_monthly_expenses}</p>
<p>Bank Balance: ${dashboardData.bank_balance}</p>
<p>Investments: ${dashboardData.investments}</p>
<p>Goal Target: ${dashboardData.goal_target ?? "No goal set"}</p>
<p>Goal Progress: {dashboardData.goal_progress ?? "No goal"}%</p>

    </div>
  );
};

export default DashboardPage;
