import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import DashboardPage from './pages/DashboardPage';
import BankPage from './pages/BankPage';
import CryptoPage from './pages/CryptoPage';
import StocksPage from './pages/StocksPage';
import ExpensesPage from './pages/ExpensesPage';
import GoalsPage from './pages/GoalsPage';

function App() {
  return (
    <Router>
      <nav style={{ padding: "1rem", backgroundColor: "#f5f5f5" }}>
        <Link to="/" style={{ marginRight: "1rem" }}>Dashboard</Link>
        <Link to="/bank" style={{ marginRight: "1rem" }}>Bank</Link>
        <Link to="/crypto" style={{ marginRight: "1rem" }}>Crypto</Link>
        <Link to="/stocks" style={{ marginRight: "1rem" }}>Stocks</Link>
        <Link to="/expenses" style={{ marginRight: "1rem" }}>Expenses</Link>
        <Link to="/goals">Goals</Link>
      </nav>

      <div style={{ padding: "2rem" }}>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/bank" element={<BankPage />} />
          <Route path="/crypto" element={<CryptoPage />} />
          <Route path="/stocks" element={<StocksPage />} />
          <Route path="/expenses" element={<ExpensesPage />} />
          <Route path="/goals" element={<GoalsPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
