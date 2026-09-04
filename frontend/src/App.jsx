import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import AppShell from './components/layout/AppShell';
import ErrorBoundary from './components/common/ErrorBoundary';

import Overview from './pages/Overview';
import Pipeline from './pages/Pipeline';
import Opportunities from './pages/Opportunities';
import Priorities from './pages/Priorities';
import WorkQueue from './pages/WorkQueue';
import Accounts from './pages/Accounts';
import AccountDetail from './pages/AccountDetail';
import Agents from './pages/Agents';
import AgentDetail from './pages/AgentDetail';
import Managers from './pages/Managers';
import ManagerDetail from './pages/ManagerDetail';
import Products from './pages/Products';
import ProductDetail from './pages/ProductDetail';
import Aging from './pages/Aging';
import Performance from './pages/Performance';
import Settings from './pages/Settings';
import HelpDocs from './pages/HelpDocs';
import Login from './pages/Login';

export function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />

          {/* Main App Layout */}
          <Route element={<AppShell />}>
            <Route path="/" element={<Overview />} />
            <Route path="/overview" element={<Overview />} />
            <Route path="/pipeline" element={<Pipeline />} />
            <Route path="/opportunities" element={<Opportunities />} />
            <Route path="/priorities" element={<Priorities />} />
            <Route path="/workqueue" element={<WorkQueue />} />
            <Route path="/accounts" element={<Accounts />} />
            <Route path="/accounts/:id" element={<AccountDetail />} />
            <Route path="/agents" element={<Agents />} />
            <Route path="/agents/:name" element={<AgentDetail />} />
            <Route path="/managers" element={<Managers />} />
            <Route path="/managers/:name" element={<ManagerDetail />} />
            <Route path="/products" element={<Products />} />
            <Route path="/products/:name" element={<ProductDetail />} />
            <Route path="/aging" element={<Aging />} />
            <Route path="/performance" element={<Performance />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/help-docs" element={<HelpDocs />} />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
