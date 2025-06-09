import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { styled, useTheme } from '@mui/material/styles';
import { 
  Paper, 
  Typography, 
  Grid, 
  Button, 
  FormControl, 
  InputLabel, 
  Select, 
  MenuItem, 
  Tabs, 
  Tab, 
  Box, 
  CircularProgress, 
  Snackbar, 
  Switch, 
  FormControlLabel, 
  Slider, 
  Divider,
  Card,
  CardContent,
  IconButton,
  Chip,
  LinearProgress,
  Tooltip,
  Avatar,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  alpha
} from '@mui/material';
import { Alert } from '@mui/material';
import { 
  Save, 
  Security, 
  Settings as SettingsIcon, 
  Palette, 
  TrendingUp, 
  Speed, 
  Shield, 
  Visibility, 
  Timer, 
  CheckCircle, 
  Warning,
  LightMode,
  DarkMode,
  Language,
  DateRange,
  Refresh,
  Lock,
  Group,
  Public,
  Storage
} from '@mui/icons-material';
import { API_URL } from '../config';
import { useTheme as useCustomTheme } from '../theme/ThemeContext';

const Root = styled('div')(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  backgroundColor: theme.palette.background.default,
  minHeight: '100vh',
}));

const HeaderCard = styled(Card)(({ theme }) => ({
  background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
  color: 'white',
  marginBottom: theme.spacing(3),
  borderRadius: 20,
  overflow: 'hidden',
  position: 'relative',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'url("data:image/svg+xml,%3Csvg width="20" height="20" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="%23ffffff" fill-opacity="0.05"%3E%3Ccircle cx="3" cy="3" r="3"/%3E%3Ccircle cx="13" cy="13" r="3"/%3E%3C/g%3E%3C/svg%3E")',
  },
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
  borderRadius: 16,
  border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
  background: theme.palette.mode === 'dark' 
    ? `linear-gradient(145deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.primary.main, 0.02)} 100%)`
    : theme.palette.background.paper,
  boxShadow: theme.palette.mode === 'dark' 
    ? '0 8px 32px rgba(0, 0, 0, 0.3)'
    : '0 2px 20px rgba(0, 0, 0, 0.08)',
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.palette.mode === 'dark' 
      ? '0 12px 40px rgba(0, 0, 0, 0.4)'
      : '0 8px 30px rgba(0, 0, 0, 0.12)',
  },
}));

const StatCard = styled(Card)(({ theme }) => ({
  padding: theme.spacing(2),
  borderRadius: 16,
  background: theme.palette.mode === 'dark'
    ? `linear-gradient(145deg, ${alpha(theme.palette.background.paper, 0.8)} 0%, ${alpha(theme.palette.primary.main, 0.05)} 100%)`
    : `linear-gradient(145deg, ${theme.palette.background.paper} 0%, ${alpha(theme.palette.primary.main, 0.02)} 100%)`,
  border: `1px solid ${alpha(theme.palette.primary.main, 0.1)}`,
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  position: 'relative',
  overflow: 'hidden',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.palette.mode === 'dark' 
      ? `0 12px 40px ${alpha(theme.palette.primary.main, 0.3)}`
      : `0 8px 30px ${alpha(theme.palette.primary.main, 0.15)}`,
    '&::before': {
      opacity: 1,
    },
  },
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 4,
    background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.secondary.main})`,
    opacity: 0.7,
    transition: 'opacity 0.3s ease',
  },
}));

const StyledFormControl = styled(FormControl)(({ theme }) => ({
  margin: theme.spacing(1, 0),
  '& .MuiOutlinedInput-root': {
    borderRadius: 12,
    transition: 'all 0.3s ease',
    '&:hover': {
      boxShadow: `0 0 0 2px ${alpha(theme.palette.primary.main, 0.1)}`,
    },
    '&.Mui-focused': {
      boxShadow: `0 0 0 2px ${alpha(theme.palette.primary.main, 0.2)}`,
    },
  },
  '& .MuiInputLabel-root': {
    fontWeight: 500,
  },
}));

const ModernSlider = styled(Slider)(({ theme }) => ({
  '& .MuiSlider-rail': {
    backgroundColor: alpha(theme.palette.primary.main, 0.1),
    height: 8,
    borderRadius: 4,
  },
  '& .MuiSlider-track': {
    background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.primary.light})`,
    height: 8,
    borderRadius: 4,
    border: 'none',
  },
  '& .MuiSlider-thumb': {
    width: 20,
    height: 20,
    backgroundColor: theme.palette.background.paper,
    border: `3px solid ${theme.palette.primary.main}`,
    boxShadow: '0 4px 12px rgba(0, 0, 0, 0.15)',
    '&:hover': {
      boxShadow: `0 6px 20px ${alpha(theme.palette.primary.main, 0.4)}`,
    },
  },
  '& .MuiSlider-mark': {
    backgroundColor: alpha(theme.palette.primary.main, 0.3),
    height: 8,
    width: 2,
    borderRadius: 1,
  },
  '& .MuiSlider-markActive': {
    backgroundColor: theme.palette.primary.main,
  },
}));

const ModernTabs = styled(Tabs)(({ theme }) => ({
  '& .MuiTabs-indicator': {
    height: 3,
    borderRadius: '3px 3px 0 0',
    background: `linear-gradient(90deg, ${theme.palette.primary.main}, ${theme.palette.primary.light})`,
  },
  '& .MuiTab-root': {
    textTransform: 'none',
    fontWeight: 600,
    fontSize: '1rem',
    minHeight: 64,
    padding: theme.spacing(2, 3),
    borderRadius: '12px 12px 0 0',
    marginRight: theme.spacing(1),
    transition: 'all 0.3s ease',
    '&:hover': {
      backgroundColor: alpha(theme.palette.primary.main, 0.05),
      color: theme.palette.primary.main,
    },
    '&.Mui-selected': {
      color: theme.palette.primary.main,
      backgroundColor: alpha(theme.palette.primary.main, 0.08),
    },
  },
}));

const ModernSwitch = styled(Switch)(({ theme }) => ({
  width: 58,
  height: 32,
  padding: 7,
  '& .MuiSwitch-switchBase': {
    margin: 1,
    padding: 0,
    transform: 'translateX(6px)',
    '&.Mui-checked': {
      color: '#fff',
      transform: 'translateX(22px)',
      '& .MuiSwitch-thumb:before': {
        backgroundImage: `url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 20 20"><path fill="${encodeURIComponent(
          '#fff',
        )}" d="m8.229 14.062-3.521-3.541L5.75 9.479l2.479 2.459 6.021-6L15.292 7Z"/></svg>')`,
      },
      '& + .MuiSwitch-track': {
        opacity: 1,
        backgroundColor: theme.palette.primary.main,
      },
    },
  },
  '& .MuiSwitch-thumb': {
    backgroundColor: '#fff',
    width: 26,
    height: 26,
    '&::before': {
      content: "''",
      position: 'absolute',
      width: '100%',
      height: '100%',
      left: 0,
      top: 0,
      backgroundRepeat: 'no-repeat',
      backgroundPosition: 'center',
      backgroundImage: `url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" height="20" width="20" viewBox="0 0 20 20"><path fill="${encodeURIComponent(
        '#999',
      )}" d="M9.305 1.667V3.75h1.389V1.667h-1.39zm-4.707 1.95-1.214 1.214a5.5 5.5 0 00-.828 6.4c.157.359.452.67.749.749l.084.033.054.018a5.5 5.5 0 006.4-.828l1.214-1.214a5.5 5.5 0 00.828-6.4c-.157-.359-.452-.67-.749-.749l-.084-.033-.054-.018a5.5 5.5 0 00-6.4.828zm4.249 8.583a4.5 4.5 0 01-3.32 1.39 4.5 4.5 0 113.32-1.39z"/></svg>')`,
    },
  },
  '& .MuiSwitch-track': {
    opacity: 1,
    backgroundColor: alpha(theme.palette.text.primary, 0.25),
    borderRadius: 20 / 2,
  },
}));

const ActionButton = styled(Button)(({ theme }) => ({
  borderRadius: 12,
  padding: theme.spacing(1.5, 3),
  fontWeight: 600,
  textTransform: 'none',
  fontSize: '1rem',
  boxShadow: 'none',
  background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
  transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
  '&:hover': {
    background: `linear-gradient(135deg, ${theme.palette.primary.dark} 0%, ${theme.palette.primary.main} 100%)`,
    transform: 'translateY(-2px)',
    boxShadow: `0 8px 25px ${alpha(theme.palette.primary.main, 0.3)}`,
  },
  '&:active': {
    transform: 'translateY(0px)',
  },
}));

const ThemeToggleButton = styled(IconButton)(({ theme }) => ({
  borderRadius: 12,
  padding: theme.spacing(1),
  backgroundColor: alpha(theme.palette.primary.main, 0.1),
  color: theme.palette.primary.main,
  transition: 'all 0.3s ease',
  '&:hover': {
    backgroundColor: alpha(theme.palette.primary.main, 0.2),
    transform: 'scale(1.05)',
  },
}));

const FeatureListItem = styled(ListItem)(({ theme }) => ({
  borderRadius: 12,
  marginBottom: theme.spacing(1),
  backgroundColor: alpha(theme.palette.background.paper, 0.5),
  border: `1px solid ${alpha(theme.palette.divider, 0.1)}`,
  transition: 'all 0.3s ease',
  '&:hover': {
    backgroundColor: alpha(theme.palette.primary.main, 0.05),
    transform: 'translateX(4px)',
  },
}));

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </div>
  );
}

const Settings = () => {
  const theme = useTheme();
  const { themeMode, toggleTheme, setTheme } = useCustomTheme();
  const { anomalies } = useSelector((state) => state.anomaly);
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    totalRecords: 0,
    modelAccuracy: 0.95,
    averageResponseTime: 2.5,
    systemHealth: 'Excellent',
    dataProcessed: 15420,
    securityLevel: 'High',
    uptime: 99.8
  });
  
  // Anomaly Detection Settings
  const [anomalySettings, setAnomalySettings] = useState({
    defaultThreshold: 0.5,
    modelType: 'isolation_forest',
    autoTrain: true,
    trainingFrequency: 'weekly',
    notificationsEnabled: true,
  });

  // Privacy Settings
  const [privacySettings, setPrivacySettings] = useState({
    defaultDataVisibility: 'organization',
    encryptionLevel: 'high',
    dataRetentionPeriod: 90,
    allowDataSharing: false,
  });

  // User Preferences
  const [userPreferences, setUserPreferences] = useState({
    theme: themeMode,
    dashboardRefreshRate: 5,
    language: 'en',
    dateFormat: 'MM/DD/YYYY',
    enableAnimations: true,
    compactMode: false,
    showNotifications: true,
  });

  // Stats will be fetched from API

  useEffect(() => {
    // Fetch user settings and analytics data
    fetchSettings();
    
    // Fetch analytics data
    const fetchAnalytics = async () => {
      try {
        const response = await fetch(`${API_URL}/api/analytics/comprehensive`);
        if (response.ok) {
          const data = await response.json();
          setStats(prevStats => ({
            ...prevStats,
            totalRecords: data.analytics?.total_records || prevStats.totalRecords,
            modelAccuracy: data.analytics?.model_metrics?.accuracy || prevStats.modelAccuracy,
            averageResponseTime: data.analytics?.response_metrics?.average_time || prevStats.averageResponseTime,
            dataProcessed: data.analytics?.data_processed || prevStats.dataProcessed,
            systemHealth: data.analytics?.system_health || prevStats.systemHealth,
            securityLevel: data.analytics?.security_level || prevStats.securityLevel,
            uptime: data.analytics?.uptime || prevStats.uptime
          }));
        }
      } catch (error) {
        console.error('Failed to fetch analytics:', error);
      }
    };
    fetchAnalytics();
  }, []);

  const fetchSettings = async () => {
    setLoading(true);
    try {
      // In a real application, these would be API calls to fetch user settings
      // For now, we'll simulate with a timeout
      setTimeout(() => {
        // Simulated response
        const response = {
          anomalySettings: {
            defaultThreshold: 0.6,
            modelType: 'isolation_forest',
            autoTrain: true,
            trainingFrequency: 'weekly',
            notificationsEnabled: true,
          },
          privacySettings: {
            defaultDataVisibility: 'organization',
            encryptionLevel: 'high',
            dataRetentionPeriod: 90,
            allowDataSharing: false,
          },
          userPreferences: {
            theme: 'light',
            dashboardRefreshRate: 5,
            language: 'en',
            dateFormat: 'MM/DD/YYYY',
          },
        };

        setAnomalySettings(response.anomalySettings);
        setPrivacySettings(response.privacySettings);
        setUserPreferences(response.userPreferences);
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('Failed to fetch settings. Please try again.');
      setLoading(false);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handlePrivacySettingsChange = (e) => {
    const { name, value, checked } = e.target;
    setPrivacySettings({
      ...privacySettings,
      [name]: e.target.type === 'checkbox' ? checked : value,
    });
  };

  const handleRetentionPeriodChange = (event, newValue) => {
    setPrivacySettings({
      ...privacySettings,
      dataRetentionPeriod: newValue,
    });
  };

  const handleUserPreferencesChange = (e) => {
    const { name, value, checked } = e.target;
    const newValue = e.target.type === 'checkbox' ? checked : value;
    
    setUserPreferences({
      ...userPreferences,
      [name]: newValue,
    });

    // Handle theme changes immediately
    if (name === 'theme') {
      setTheme(value);
    }
  };

  const handleRefreshRateChange = (event, newValue) => {
    setUserPreferences({
      ...userPreferences,
      dashboardRefreshRate: newValue,
    });
  };

  const handleSaveSettings = async () => {
    setLoading(true);
    setError(null);
    try {
      // In a real application, this would be an API call to save settings
      // For now, we'll simulate with a timeout
      setTimeout(() => {
        console.log('Saving settings:', {
          anomalySettings,
          privacySettings,
          userPreferences,
        });
        setSuccess(true);
        setLoading(false);
      }, 1000);
    } catch (err) {
      setError('Failed to save settings. Please try again.');
      setLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSuccess(false);
    setError(null);
  };

  return (
    <Root>
      {/* Header Section */}
      <HeaderCard>
        <CardContent sx={{ position: 'relative', zIndex: 1 }}>
          <Box display="flex" alignItems="center" justifyContent="space-between">
            <Box display="flex" alignItems="center" gap={2}>
              <Avatar sx={{ width: 56, height: 56, bgcolor: 'rgba(255,255,255,0.2)' }}>
                <SettingsIcon fontSize="large" />
              </Avatar>
              <Box>
                <Typography variant="h3" fontWeight="700" gutterBottom>
                  Settings & Configuration
                </Typography>
                <Typography variant="h6" sx={{ opacity: 0.9 }}>
                  Manage your CryptaNet experience with advanced controls
                </Typography>
              </Box>
            </Box>
            <ThemeToggleButton onClick={toggleTheme}>
              {themeMode === 'light' ? <DarkMode /> : <LightMode />}
            </ThemeToggleButton>
          </Box>
        </CardContent>
      </HeaderCard>

      <StyledPaper>
        <ModernTabs 
          value={tabValue} 
          onChange={handleTabChange} 
          indicatorColor="primary" 
          textColor="primary"
          variant="fullWidth"
        >
          <Tab 
            icon={<TrendingUp />} 
            iconPosition="start"
            label="Analytics & Performance" 
          />
          <Tab 
            icon={<Security />} 
            iconPosition="start"
            label="Privacy & Security" 
          />
          <Tab 
            icon={<Palette />} 
            iconPosition="start"
            label="Appearance & Preferences" 
          />
        </ModernTabs>

        <TabPanel value={tabValue} index={0}>
          <Box mb={3}>
            <Typography variant="h5" fontWeight="600" gutterBottom>
              🚀 System Performance Dashboard
            </Typography>
            <Typography variant="body1" color="textSecondary" paragraph>
              Real-time insights into your CryptaNet system performance and anomaly detection capabilities
            </Typography>
          </Box>

          <Grid container spacing={3}>
            {/* Enhanced Statistics Cards */}
            <Grid item xs={12} sm={6} lg={3}>
              <StatCard>
                <CardContent>
                  <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                    <TrendingUp color="primary" fontSize="large" />
                    <Chip 
                      label="Live" 
                      color="success" 
                      size="small" 
                      icon={<CheckCircle />}
                    />
                  </Box>
                  <Typography variant="h3" fontWeight="700" color="primary" gutterBottom>
                    {anomalies?.length || 0}
                  </Typography>
                  <Typography variant="subtitle1" fontWeight="600" gutterBottom>
                    Recent Anomalies
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Detected in the last 24 hours
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={Math.min((anomalies?.length || 0) / 10 * 100, 100)} 
                    sx={{ mt: 2, borderRadius: 2, height: 8 }}
                  />
                </CardContent>
              </StatCard>
            </Grid>

            <Grid item xs={12} sm={6} lg={3}>
              <StatCard>
                <CardContent>
                  <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                    <Speed color="warning" fontSize="large" />
                    <Chip 
                      label={stats.averageResponseTime < 3 ? "Fast" : "Normal"} 
                      color={stats.averageResponseTime < 3 ? "success" : "warning"}
                      size="small" 
                    />
                  </Box>
                  <Typography variant="h3" fontWeight="700" color="warning.main" gutterBottom>
                    {(() => {
                      try {
                        const anomalyCount = anomalies?.length || 0;
                        const totalRecords = stats?.totalRecords || 1;
                        return ((anomalyCount / totalRecords) * 100).toFixed(1);
                      } catch (e) {
                        return '0.0';
                      }
                    })()}%
                  </Typography>
                  <Typography variant="subtitle1" fontWeight="600" gutterBottom>
                    Detection Rate
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Percentage of anomalous events
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={(() => {
                      try {
                        const anomalyCount = anomalies?.length || 0;
                        const totalRecords = stats?.totalRecords || 1;
                        return (anomalyCount / totalRecords) * 100;
                      } catch (e) {
                        return 0;
                      }
                    })()} 
                    color="warning"
                    sx={{ mt: 2, borderRadius: 2, height: 8 }}
                  />
                </CardContent>
              </StatCard>
            </Grid>

            <Grid item xs={12} sm={6} lg={3}>
              <StatCard>
                <CardContent>
                  <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                    <Timer color="info" fontSize="large" />
                    <Chip label="Optimized" color="info" size="small" />
                  </Box>
                  <Typography variant="h3" fontWeight="700" color="info.main" gutterBottom>
                    {stats?.averageResponseTime || '< 1'} min
                  </Typography>
                  <Typography variant="subtitle1" fontWeight="600" gutterBottom>
                    Response Time
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Average anomaly detection time
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={Math.max(100 - (stats?.averageResponseTime || 1) * 20, 20)} 
                    color="info"
                    sx={{ mt: 2, borderRadius: 2, height: 8 }}
                  />
                </CardContent>
              </StatCard>
            </Grid>

            <Grid item xs={12} sm={6} lg={3}>
              <StatCard>
                <CardContent>
                  <Box display="flex" alignItems="center" justifyContent="space-between" mb={2}>
                    <CheckCircle color="success" fontSize="large" />
                    <Chip label="Excellent" color="success" size="small" />
                  </Box>
                  <Typography variant="h3" fontWeight="700" color="success.main" gutterBottom>
                    {(() => {
                      try {
                        const accuracy = stats?.modelAccuracy || 0.95;
                        return (accuracy * 100).toFixed(1);
                      } catch (e) {
                        return '95.0';
                      }
                    })()}%
                  </Typography>
                  <Typography variant="subtitle1" fontWeight="600" gutterBottom>
                    Model Accuracy
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Based on validated predictions
                  </Typography>
                  <LinearProgress 
                    variant="determinate" 
                    value={(() => {
                      try {
                        const accuracy = stats?.modelAccuracy || 0.95;
                        return accuracy * 100;
                      } catch (e) {
                        return 95;
                      }
                    })()} 
                    color="success"
                    sx={{ mt: 2, borderRadius: 2, height: 8 }}
                  />
                </CardContent>
              </StatCard>
            </Grid>

            {/* Additional Performance Metrics */}
            <Grid item xs={12} sm={6}>
              <StatCard>
                <CardContent>
                  <Typography variant="h6" fontWeight="600" gutterBottom>
                    📊 System Health Overview
                  </Typography>
                  <Box display="flex" alignItems="center" gap={2} mb={2}>
                    <Shield color="success" />
                    <Typography variant="body1" fontWeight="500">
                      Status: {stats.systemHealth}
                    </Typography>
                    <Chip label={`${stats.uptime}% Uptime`} color="success" size="small" />
                  </Box>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    All systems operational. Security protocols active.
                  </Typography>
                  <List dense>
                    <FeatureListItem>
                      <ListItemIcon><Storage color="primary" /></ListItemIcon>
                      <ListItemText 
                        primary="Data Processed" 
                        secondary={`${(stats.dataProcessed || 0).toLocaleString()} records`}
                      />
                    </FeatureListItem>
                    <FeatureListItem>
                      <ListItemIcon><Shield color="success" /></ListItemIcon>
                      <ListItemText 
                        primary="Security Level" 
                        secondary={stats.securityLevel}
                      />
                    </FeatureListItem>
                  </List>
                </CardContent>
              </StatCard>
            </Grid>

            <Grid item xs={12} sm={6}>
              <StatCard>
                <CardContent>
                  <Typography variant="h6" fontWeight="600" gutterBottom>
                    ⚡ Real-time Analytics
                  </Typography>
                  <Typography variant="body2" color="textSecondary" paragraph>
                    Monitor live data streams and anomaly detection patterns
                  </Typography>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="body2">Active Connections</Typography>
                    <Chip label="24 Active" color="primary" size="small" />
                  </Box>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="body2">Data Streams</Typography>
                    <Chip label="12 Sources" color="info" size="small" />
                  </Box>
                  <Box display="flex" justifyContent="space-between" alignItems="center">
                    <Typography variant="body2">Processing Queue</Typography>
                    <Chip label="Empty" color="success" size="small" />
                  </Box>
                </CardContent>
              </StatCard>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Box mb={3}>
            <Typography variant="h5" fontWeight="600" gutterBottom>
              🔒 Privacy & Security Controls
            </Typography>
            <Typography variant="body1" color="textSecondary" paragraph>
              Configure your data privacy preferences and security settings for optimal protection
            </Typography>
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="data-visibility-label">
                  <Box display="flex" alignItems="center" gap={1}>
                    <Visibility fontSize="small" />
                    Default Data Visibility
                  </Box>
                </InputLabel>
                <Select
                  labelId="data-visibility-label"
                  id="defaultDataVisibility"
                  name="defaultDataVisibility"
                  value={privacySettings.defaultDataVisibility}
                  onChange={handlePrivacySettingsChange}
                  label="Default Data Visibility"
                >
                  <MenuItem value="private">
                    <Box display="flex" alignItems="center" gap={1}>
                      <Lock fontSize="small" />
                      Private (Only You)
                    </Box>
                  </MenuItem>
                  <MenuItem value="organization">
                    <Box display="flex" alignItems="center" gap={1}>
                      <Group fontSize="small" />
                      Organization
                    </Box>
                  </MenuItem>
                  <MenuItem value="partners">
                    <Box display="flex" alignItems="center" gap={1}>
                      <Group fontSize="small" />
                      Partners
                    </Box>
                  </MenuItem>
                  <MenuItem value="public">
                    <Box display="flex" alignItems="center" gap={1}>
                      <Public fontSize="small" />
                      Public
                    </Box>
                  </MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="encryption-level-label">
                  <Box display="flex" alignItems="center" gap={1}>
                    <Shield fontSize="small" />
                    Encryption Level
                  </Box>
                </InputLabel>
                <Select
                  labelId="encryption-level-label"
                  id="encryptionLevel"
                  name="encryptionLevel"
                  value={privacySettings.encryptionLevel}
                  onChange={handlePrivacySettingsChange}
                  label="Encryption Level"
                >
                  <MenuItem value="standard">Standard (AES-128)</MenuItem>
                  <MenuItem value="high">High (AES-256)</MenuItem>
                  <MenuItem value="very-high">Very High (AES-256 + RSA)</MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>

            <Grid item xs={12}>
              <Box mb={2}>
                <Typography variant="h6" fontWeight="600" gutterBottom>
                  📅 Data Retention Policy
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Configure how long your data is stored: {privacySettings.dataRetentionPeriod} days
                </Typography>
              </Box>
              <ModernSlider
                value={privacySettings.dataRetentionPeriod}
                onChange={handleRetentionPeriodChange}
                aria-labelledby="retention-slider"
                valueLabelDisplay="auto"
                step={30}
                marks={[
                  { value: 30, label: '30d' },
                  { value: 90, label: '90d' },
                  { value: 180, label: '6m' },
                  { value: 365, label: '1y' },
                ]}
                min={30}
                max={365}
              />
            </Grid>

            <Grid item xs={12}>
              <Box p={3} borderRadius={2} bgcolor={alpha(theme.palette.primary.main, 0.05)}>
                <FormControlLabel
                  control={
                    <ModernSwitch
                      checked={privacySettings.allowDataSharing}
                      onChange={handlePrivacySettingsChange}
                      name="allowDataSharing"
                      color="primary"
                    />
                  }
                  label={
                    <Box>
                      <Typography variant="subtitle1" fontWeight="600">
                        🤝 Trusted Partner Data Sharing
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        Allow secure data sharing with verified blockchain partners for enhanced supply chain visibility
                      </Typography>
                    </Box>
                  }
                />
              </Box>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Box mb={3}>
            <Typography variant="h5" fontWeight="600" gutterBottom>
              🎨 Appearance & User Preferences
            </Typography>
            <Typography variant="body1" color="textSecondary" paragraph>
              Customize your CryptaNet interface to match your workflow and preferences
            </Typography>
          </Box>

          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="theme-label">
                  <Box display="flex" alignItems="center" gap={1}>
                    <Palette fontSize="small" />
                    Theme Mode
                  </Box>
                </InputLabel>
                <Select
                  labelId="theme-label"
                  id="theme"
                  name="theme"
                  value={userPreferences.theme}
                  onChange={handleUserPreferencesChange}
                  label="Theme Mode"
                >
                  <MenuItem value="light">
                    <Box display="flex" alignItems="center" gap={1}>
                      <LightMode fontSize="small" />
                      Light Mode
                    </Box>
                  </MenuItem>
                  <MenuItem value="dark">
                    <Box display="flex" alignItems="center" gap={1}>
                      <DarkMode fontSize="small" />
                      Dark Mode
                    </Box>
                  </MenuItem>
                  <MenuItem value="system">
                    <Box display="flex" alignItems="center" gap={1}>
                      <SettingsIcon fontSize="small" />
                      System Default
                    </Box>
                  </MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="language-label">
                  <Box display="flex" alignItems="center" gap={1}>
                    <Language fontSize="small" />
                    Language
                  </Box>
                </InputLabel>
                <Select
                  labelId="language-label"
                  id="language"
                  name="language"
                  value={userPreferences.language}
                  onChange={handleUserPreferencesChange}
                  label="Language"
                >
                  <MenuItem value="en">🇺🇸 English</MenuItem>
                  <MenuItem value="es">🇪🇸 Español</MenuItem>
                  <MenuItem value="fr">🇫🇷 Français</MenuItem>
                  <MenuItem value="de">🇩🇪 Deutsch</MenuItem>
                  <MenuItem value="zh">🇨🇳 中文</MenuItem>
                  <MenuItem value="ja">🇯🇵 日本語</MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>

            <Grid item xs={12} md={6}>
              <Box>
                <Typography variant="h6" fontWeight="600" gutterBottom>
                  <Refresh fontSize="small" sx={{ verticalAlign: 'middle', mr: 1 }} />
                  Dashboard Refresh Rate: {userPreferences.dashboardRefreshRate} minutes
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  How often the dashboard updates with new data
                </Typography>
                <ModernSlider
                  value={userPreferences.dashboardRefreshRate}
                  onChange={handleRefreshRateChange}
                  aria-labelledby="refresh-rate-slider"
                  valueLabelDisplay="auto"
                  step={1}
                  marks={[
                    { value: 1, label: '1m' },
                    { value: 5, label: '5m' },
                    { value: 15, label: '15m' },
                    { value: 30, label: '30m' },
                  ]}
                  min={1}
                  max={30}
                />
              </Box>
            </Grid>

            <Grid item xs={12} md={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="date-format-label">
                  <Box display="flex" alignItems="center" gap={1}>
                    <DateRange fontSize="small" />
                    Date Format
                  </Box>
                </InputLabel>
                <Select
                  labelId="date-format-label"
                  id="dateFormat"
                  name="dateFormat"
                  value={userPreferences.dateFormat}
                  onChange={handleUserPreferencesChange}
                  label="Date Format"
                >
                  <MenuItem value="MM/DD/YYYY">MM/DD/YYYY (US)</MenuItem>
                  <MenuItem value="DD/MM/YYYY">DD/MM/YYYY (EU)</MenuItem>
                  <MenuItem value="YYYY-MM-DD">YYYY-MM-DD (ISO)</MenuItem>
                  <MenuItem value="DD MMM YYYY">DD MMM YYYY</MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>

            {/* Additional Preference Toggles */}
            <Grid item xs={12}>
              <Box p={3} borderRadius={2} bgcolor={alpha(theme.palette.primary.main, 0.05)}>
                <Typography variant="h6" fontWeight="600" gutterBottom>
                  ⚙️ Interface Preferences
                </Typography>
                
                <Box display="flex" flexDirection="column" gap={2}>
                  <FormControlLabel
                    control={
                      <ModernSwitch
                        checked={userPreferences.enableAnimations}
                        onChange={handleUserPreferencesChange}
                        name="enableAnimations"
                      />
                    }
                    label={
                      <Box>
                        <Typography variant="subtitle1" fontWeight="500">
                          Enable Animations
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          Smooth transitions and visual effects
                        </Typography>
                      </Box>
                    }
                  />
                  
                  <FormControlLabel
                    control={
                      <ModernSwitch
                        checked={userPreferences.compactMode}
                        onChange={handleUserPreferencesChange}
                        name="compactMode"
                      />
                    }
                    label={
                      <Box>
                        <Typography variant="subtitle1" fontWeight="500">
                          Compact Mode
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          Reduce spacing for more content density
                        </Typography>
                      </Box>
                    }
                  />
                  
                  <FormControlLabel
                    control={
                      <ModernSwitch
                        checked={userPreferences.showNotifications}
                        onChange={handleUserPreferencesChange}
                        name="showNotifications"
                      />
                    }
                    label={
                      <Box>
                        <Typography variant="subtitle1" fontWeight="500">
                          Show Notifications
                        </Typography>
                        <Typography variant="body2" color="textSecondary">
                          Display system alerts and updates
                        </Typography>
                      </Box>
                    }
                  />
                </Box>
              </Box>
            </Grid>
          </Grid>
        </TabPanel>

        <Divider sx={{ my: 4 }} />

        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Typography variant="body2" color="textSecondary">
            Last saved: {(() => {
              try {
                return new Date().toLocaleString();
              } catch (e) {
                return 'Unknown';
              }
            })()}
          </Typography>
          <ActionButton
            variant="contained"
            onClick={handleSaveSettings}
            disabled={loading}
            startIcon={loading ? <CircularProgress size={20} /> : <Save />}
          >
            {loading ? 'Saving...' : 'Save All Settings'}
          </ActionButton>
        </Box>
      </StyledPaper>

      {/* Enhanced Snackbar */}
      <Snackbar 
        open={!!error || success} 
        autoHideDuration={6000} 
        onClose={handleCloseSnackbar}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={handleCloseSnackbar} 
          severity={error ? 'error' : 'success'}
          variant="filled"
          sx={{ 
            borderRadius: 2,
            fontWeight: 500,
          }}
        >
          {error || 'Settings saved successfully! 🎉'}
        </Alert>
      </Snackbar>
    </Root>
  );
};

export default Settings;