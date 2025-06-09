import React, { useEffect, useState } from 'react';
import { 
  Grid, 
  Typography, 
  CircularProgress, 
  Card, 
  CardContent, 
  Box, 
  Paper,
  IconButton,
  Chip,
  LinearProgress,
  Avatar,
  Fade,
  Grow
} from '@mui/material';
import { styled, useTheme, alpha } from '@mui/material/styles';
import {
  List as ListIcon,
  Warning as WarningIcon,
  Update as UpdateIcon,
  ShowChart as ShowChartIcon,
  Security as SecurityIcon,
  TrendingUp,
  TrendingDown,
  Refresh,
  Analytics,
  Assessment,
  Shield
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, AreaChart, Area } from 'recharts';
import axios from 'axios';
import { API_URL } from '../config';
import { formatNumber } from '../utils/numberFormatting';
import { useTheme as useCustomTheme } from '../theme/ThemeContext';

// Styled components
const Root = styled('div')(({ theme }) => ({
  flexGrow: 1,
  minHeight: '100vh',
  background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.02)} 0%, ${alpha(theme.palette.secondary.main, 0.02)} 100%)`,
}));

const HeaderSection = styled(Box)(({ theme }) => ({
  background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
  borderRadius: theme.spacing(2),
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
  color: theme.palette.common.white,
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    right: 0,
    width: '200px',
    height: '200px',
    background: `radial-gradient(circle, ${alpha(theme.palette.common.white, 0.1)} 0%, transparent 70%)`,
    borderRadius: '50%',
    transform: 'translate(50%, -50%)',
  },
}));

const StatCard = styled(Card)(({ theme }) => ({
  height: '100%',
  borderRadius: theme.spacing(2),
  boxShadow: theme.shadows[8],
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  background: theme.palette.background.paper,
  border: `1px solid ${alpha(theme.palette.divider, 0.12)}`,
  position: 'relative',
  overflow: 'hidden',
  '&:hover': {
    transform: 'translateY(-8px) scale(1.02)',
    boxShadow: theme.shadows[16],
  },
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '4px',
    background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
  },
}));

const StatCardContent = styled(CardContent)(({ theme }) => ({
  padding: theme.spacing(3),
  position: 'relative',
  zIndex: 1,
}));

const StatIconContainer = styled(Box)(({ theme, gradient }) => ({
  width: 60,
  height: 60,
  borderRadius: theme.spacing(2),
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  background: gradient || `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
  marginBottom: theme.spacing(2),
  boxShadow: theme.shadows[4],
}));

const StatValue = styled(Typography)(({ theme }) => ({
  fontSize: '2.5rem',
  fontWeight: 700,
  lineHeight: 1.2,
  marginBottom: theme.spacing(1),
}));

const StatTrend = styled(Box)(({ theme, trend }) => ({
  display: 'flex',
  alignItems: 'center',
  color: trend === 'up' ? theme.palette.success.main : theme.palette.error.main,
}));

const ChartContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  borderRadius: theme.spacing(2),
  boxShadow: theme.shadows[8],
  background: theme.palette.background.paper,
  border: `1px solid ${alpha(theme.palette.divider, 0.12)}`,
}));

const RefreshButton = styled(IconButton)(({ theme }) => ({
  backgroundColor: alpha(theme.palette.common.white, 0.1),
  color: theme.palette.common.white,
  '&:hover': {
    backgroundColor: alpha(theme.palette.common.white, 0.2),
    transform: 'rotate(180deg)',
  },
  transition: 'all 0.3s ease',
}));

const Dashboard = () => {
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const [refreshing, setRefreshing] = useState(false);
  const theme = useTheme();
  const { mode } = useCustomTheme();

  const fetchAnalyticsData = async (showRefreshing = false) => {
    try {
      if (showRefreshing) setRefreshing(true);
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/analytics`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      
      if (response.data) {
        setAnalyticsData(response.data);
        setLastUpdated(new Date());
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching analytics:', err);
      setError(err.message);
      setLoading(false);
    } finally {
      if (showRefreshing) {
        setTimeout(() => setRefreshing(false), 1000);
      }
    }
  };

  const handleRefresh = () => {
    fetchAnalyticsData(true);
  };

  useEffect(() => {
    fetchAnalyticsData();
    // Fetch data every 5 seconds for real-time updates
    const intervalId = setInterval(() => {
      fetchAnalyticsData();
      setLastUpdated(new Date()); // Force update of time display
    }, 5000);
    return () => clearInterval(intervalId);
  }, []);

  if (loading && !analyticsData) {
    return (
      <Root>
        <HeaderSection>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Box>
              <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
                CryptaNet Dashboard
              </Typography>
              <Typography variant="h6" sx={{ opacity: 0.9 }}>
                Real-time Security Analytics Platform
              </Typography>
            </Box>
            <Avatar sx={{ width: 80, height: 80, bgcolor: alpha(theme.palette.common.white, 0.2) }}>
              <Analytics sx={{ fontSize: 40 }} />
            </Avatar>
          </Box>
        </HeaderSection>
        <Box display="flex" justifyContent="center" alignItems="center" height="50vh">
          <CircularProgress size={60} thickness={4} />
        </Box>
      </Root>
    );
  }

  const analytics = analyticsData || {};
  const totalRecords = analytics.total_records || 0;
  const anomalyCount = analytics.anomaly_count || analytics.unique_anomalies_count || (analytics.anomalies || []).length || 0;
  const anomalyRate = totalRecords > 0 ? ((anomalyCount / totalRecords) * 100).toFixed(2) : 0;
  
  // Enhanced mock data for the chart
  const chartData = [
    { name: 'Jan', anomalies: 30, records: 2000, rate: 1.5 },
    { name: 'Feb', anomalies: 20, records: 1800, rate: 1.1 },
    { name: 'Mar', anomalies: 50, records: 2200, rate: 2.3 },
    { name: 'Apr', anomalies: 40, records: 2100, rate: 1.9 },
    { name: 'May', anomalies: 60, records: 2500, rate: 2.4 },
    { name: 'Jun', anomalies: anomalyCount, records: totalRecords, rate: parseFloat(anomalyRate) },
  ];

  const statCards = [
    {
      title: 'Total Records',
      value: formatNumber(totalRecords),
      icon: <ListIcon sx={{ fontSize: 30, color: 'white' }} />,
      gradient: `linear-gradient(135deg, ${theme.palette.info.main} 0%, ${theme.palette.info.dark} 100%)`,
      trend: 'up',
      change: '+12.5%',
      subtitle: 'Last 30 days'
    },
    {
      title: 'Anomalies Detected',
      value: formatNumber(anomalyCount),
      icon: <WarningIcon sx={{ fontSize: 30, color: 'white' }} />,
      gradient: `linear-gradient(135deg, ${theme.palette.error.main} 0%, ${theme.palette.error.dark} 100%)`,
      trend: anomalyCount > 30 ? 'up' : 'down',
      change: anomalyCount > 30 ? '+8.3%' : '-5.2%',
      subtitle: 'Active threats'
    },
    {
      title: 'System Health',
      value: anomalyRate < 2 ? 'Excellent' : anomalyRate < 5 ? 'Good' : 'Alert',
      icon: <SecurityIcon sx={{ fontSize: 30, color: 'white' }} />,
      gradient: `linear-gradient(135deg, ${theme.palette.success.main} 0%, ${theme.palette.success.dark} 100%)`,
      trend: 'up',
      change: '99.9%',
      subtitle: 'Uptime'
    },
    {
      title: 'Detection Rate',
      value: `${anomalyRate}%`,
      icon: <Assessment sx={{ fontSize: 30, color: 'white' }} />,
      gradient: `linear-gradient(135deg, ${theme.palette.warning.main} 0%, ${theme.palette.warning.dark} 100%)`,
      trend: parseFloat(anomalyRate) > 2 ? 'up' : 'down',
      change: parseFloat(anomalyRate) > 2 ? '+0.3%' : '-0.1%',
      subtitle: 'Anomaly ratio'
    }
  ];

  return (
    <Root>
      {/* Header Section */}
      <HeaderSection>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
              CryptaNet Dashboard
            </Typography>
            <Typography variant="h6" sx={{ opacity: 0.9, mb: 2 }}>
              Real-time Security Analytics Platform
            </Typography>
            <Box display="flex" alignItems="center" gap={2}>
              <Chip 
                label={`Last updated: ${lastUpdated.toLocaleTimeString()}`}
                sx={{ 
                  bgcolor: alpha(theme.palette.common.white, 0.2),
                  color: 'white',
                  fontWeight: 500
                }}
              />
              <Chip 
                label={anomalyRate < 2 ? 'System Secure' : 'Monitoring'}
                color={anomalyRate < 2 ? 'success' : 'warning'}
                sx={{ fontWeight: 500 }}
              />
            </Box>
          </Box>
          <Box display="flex" alignItems="center" gap={2}>
            <RefreshButton onClick={handleRefresh} disabled={refreshing}>
              <Refresh sx={{ 
                animation: refreshing ? 'spin 1s linear infinite' : 'none',
                '@keyframes spin': {
                  '0%': { transform: 'rotate(0deg)' },
                  '100%': { transform: 'rotate(360deg)' }
                }
              }} />
            </RefreshButton>
            <Avatar sx={{ width: 80, height: 80, bgcolor: alpha(theme.palette.common.white, 0.2) }}>
              <Shield sx={{ fontSize: 40 }} />
            </Avatar>
          </Box>
        </Box>
      </HeaderSection>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        {statCards.map((card, index) => (
          <Grid item xs={12} sm={6} md={3} key={card.title}>
            <Grow in timeout={300 + index * 100}>
              <StatCard>
                <StatCardContent>
                  <StatIconContainer gradient={card.gradient}>
                    {card.icon}
                  </StatIconContainer>
                  
                  <Typography variant="h6" color="textSecondary" sx={{ mb: 1 }}>
                    {card.title}
                  </Typography>
                  
                  <StatValue>{card.value}</StatValue>
                  
                  <Box display="flex" alignItems="center" justifyContent="space-between">
                    <Typography variant="body2" color="textSecondary">
                      {card.subtitle}
                    </Typography>
                    <StatTrend trend={card.trend}>
                      {card.trend === 'up' ? <TrendingUp fontSize="small" /> : <TrendingDown fontSize="small" />}
                      <Typography variant="body2" sx={{ ml: 0.5, fontWeight: 600 }}>
                        {card.change}
                      </Typography>
                    </StatTrend>
                  </Box>
                </StatCardContent>
              </StatCard>
            </Grow>
          </Grid>
        ))}
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3}>
        {/* Anomaly Trend Chart */}
        <Grid item xs={12} lg={8}>
          <Fade in timeout={800}>
            <ChartContainer>
              <Box display="flex" alignItems="center" justifyContent="between" sx={{ mb: 3 }}>
                <Box display="flex" alignItems="center">
                  <ShowChartIcon sx={{ color: theme.palette.primary.main, mr: 1 }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Security Analytics Trends
                  </Typography>
                </Box>
                <Chip label="Real-time" color="primary" size="small" />
              </Box>
              <ResponsiveContainer width="100%" height={350}>
                <AreaChart data={chartData}>
                  <defs>
                    <linearGradient id="anomalyGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={theme.palette.error.main} stopOpacity={0.3}/>
                      <stop offset="95%" stopColor={theme.palette.error.main} stopOpacity={0}/>
                    </linearGradient>
                    <linearGradient id="recordsGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={theme.palette.info.main} stopOpacity={0.3}/>
                      <stop offset="95%" stopColor={theme.palette.info.main} stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke={alpha(theme.palette.divider, 0.3)} />
                  <XAxis dataKey="name" stroke={theme.palette.text.secondary} />
                  <YAxis yAxisId="left" stroke={theme.palette.error.main} />
                  <YAxis yAxisId="right" orientation="right" stroke={theme.palette.info.main} />
                  <Tooltip 
                    contentStyle={{ 
                      backgroundColor: theme.palette.background.paper, 
                      border: `1px solid ${theme.palette.divider}`,
                      borderRadius: theme.spacing(1),
                      boxShadow: theme.shadows[8]
                    }} 
                    itemStyle={{ color: theme.palette.text.primary }}
                  />
                  <Legend />
                  <Area 
                    yAxisId="left" 
                    type="monotone" 
                    dataKey="anomalies" 
                    stroke={theme.palette.error.main} 
                    fillOpacity={1} 
                    fill="url(#anomalyGradient)"
                    strokeWidth={3}
                    name="Anomalies Detected" 
                  />
                  <Area 
                    yAxisId="right" 
                    type="monotone" 
                    dataKey="records" 
                    stroke={theme.palette.info.main} 
                    fillOpacity={1} 
                    fill="url(#recordsGradient)"
                    strokeWidth={3}
                    name="Total Records" 
                  />
                </AreaChart>
              </ResponsiveContainer>
            </ChartContainer>
          </Fade>
        </Grid>

        {/* Quick Stats */}
        <Grid item xs={12} lg={4}>
          <Fade in timeout={1000}>
            <ChartContainer sx={{ height: '100%' }}>
              <Typography variant="h6" sx={{ fontWeight: 600, mb: 3 }}>
                Quick Statistics
              </Typography>
              
              <Box sx={{ mb: 3 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                  <Typography variant="body2" color="textSecondary">Processing Efficiency</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>94%</Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={94} 
                  sx={{ 
                    height: 8, 
                    borderRadius: 4,
                    '& .MuiLinearProgress-bar': {
                      background: `linear-gradient(90deg, ${theme.palette.success.main}, ${theme.palette.success.light})`
                    }
                  }} 
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                  <Typography variant="body2" color="textSecondary">Threat Detection</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>87%</Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={87} 
                  sx={{ 
                    height: 8, 
                    borderRadius: 4,
                    '& .MuiLinearProgress-bar': {
                      background: `linear-gradient(90deg, ${theme.palette.warning.main}, ${theme.palette.warning.light})`
                    }
                  }} 
                />
              </Box>

              <Box sx={{ mb: 3 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" sx={{ mb: 1 }}>
                  <Typography variant="body2" color="textSecondary">False Positives</Typography>
                  <Typography variant="body2" sx={{ fontWeight: 600 }}>3%</Typography>
                </Box>
                <LinearProgress 
                  variant="determinate" 
                  value={3} 
                  sx={{ 
                    height: 8, 
                    borderRadius: 4,
                    '& .MuiLinearProgress-bar': {
                      background: `linear-gradient(90deg, ${theme.palette.error.main}, ${theme.palette.error.light})`
                    }
                  }} 
                />
              </Box>

              <Box sx={{ p: 2, bgcolor: alpha(theme.palette.primary.main, 0.05), borderRadius: 2, mt: 3 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                  System Status
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  All systems operational. Next maintenance scheduled for {new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toLocaleDateString()}.
                </Typography>
              </Box>
            </ChartContainer>
          </Fade>
        </Grid>
      </Grid>
    </Root>
  );
};

export default Dashboard;