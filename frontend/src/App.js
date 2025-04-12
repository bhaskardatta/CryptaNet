import React, { useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import { useDispatch, useSelector } from 'react-redux';

// Layout components
import Layout from './components/layout/Layout';

// Pages
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import SupplyChainData from './pages/SupplyChainData';
import AnomalyDetection from './pages/AnomalyDetection';
import Explainability from './pages/Explainability';
import Settings from './pages/Settings';

// Auth
import { checkAuth } from './store/slices/authSlice';

// Create theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    fontSize: 14,
    fontWeightLight: 300,
    fontWeightRegular: 400,
    fontWeightMedium: 500,
  },
});

function App() {
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
    <ThemeProvider theme={theme}>
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
          <Route path="explainability" element={<Explainability />} />
          <Route path="settings" element={<Settings />} />
        </Route>
      </Routes>
    </ThemeProvider>
  );
}

export default App;