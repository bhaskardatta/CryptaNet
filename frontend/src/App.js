import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import CssBaseline from '@mui/material/CssBaseline';
import { useDispatch, useSelector } from 'react-redux';

// Theme
import { CustomThemeProvider } from './theme/ThemeContext';

// Layout components
import Layout from './components/layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import SupplyChainData from './pages/SupplyChainData';
import AnomalyDetection from './pages/AnomalyDetection';
import Explainability from './pages/Explainability';
import Settings from './pages/Settings';
import BlockchainPrivacy from './components/blockchain/BlockchainPrivacy';
import SystemHealthDashboard from './components/monitoring/SystemHealthDashboard';

// Auth
import { checkAuth } from './store/slices/authSlice';

// Main App component with theme context
function AppContent() {
  const dispatch = useDispatch();
  const { isAuthenticated, loading } = useSelector((state) => state.auth);

  useEffect(() => {
    // Check authentication status when app loads
    dispatch(checkAuth());
  }, [dispatch]);

  // Protected route component
  const ProtectedRoute = ({ children }) => {
    if (loading) return <div>Loading...</div>;
    if (!isAuthenticated) return <Navigate to="/login" />;
    return children;
  };

  return (
    <>
      <CssBaseline />
      <Routes>
        <Route path="/login" element={
          isAuthenticated ? <Navigate to="/" /> : <Login />
        } />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Layout />
            </ProtectedRoute>
          }
        >
          <Route index element={<Dashboard />} />
          <Route path="supply-chain-data" element={<SupplyChainData />} />
          <Route path="anomaly-detection" element={<AnomalyDetection />} />
          <Route path="blockchain-privacy" element={<BlockchainPrivacy />} />
          <Route path="system-health" element={<SystemHealthDashboard />} />
          <Route path="explainability" element={<Explainability />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </>
  );
}

function App() {
  return (
    <CustomThemeProvider>
      <AppContent />
    </CustomThemeProvider>
  );
}

export default App;