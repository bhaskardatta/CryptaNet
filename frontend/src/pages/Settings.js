import React, { useState, useEffect } from 'react';
import { useSelector } from 'react-redux';
import { styled } from '@mui/material/styles';
import { Paper, Typography, Grid, Button, FormControl, InputLabel, Select, MenuItem, Tabs, Tab, Box, CircularProgress, Snackbar, Switch, FormControlLabel, Slider, Divider } from '@mui/material';
import { Alert } from '@mui/material';
import { Save } from '@mui/icons-material';
import { API_URL } from '../config';

const Root = styled('div')(({ theme }) => ({
  flexGrow: 1,
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const StyledFormControl = styled(FormControl)(({ theme }) => ({
  margin: theme.spacing(1),
  minWidth: 120,
}));

const StyledSlider = styled(Slider)(({ theme }) => ({
  width: '100%',
  padding: theme.spacing(0, 2),
}));

const StyledDivider = styled(Divider)(({ theme }) => ({
  margin: theme.spacing(2, 0),
}));

const SaveButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(2),
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
  const { anomalies } = useSelector((state) => state.anomaly);
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState(null);
  const [stats, setStats] = useState({
    totalRecords: 0,
    modelAccuracy: 0.95,
    averageResponseTime: 2.5
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
    theme: 'light',
    dashboardRefreshRate: 5,
    language: 'en',
    dateFormat: 'MM/DD/YYYY',
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
          setStats({
            totalRecords: data.analytics?.total_records || 0,
            modelAccuracy: data.analytics?.model_metrics?.accuracy || 0.95,
            averageResponseTime: data.analytics?.response_metrics?.average_time || 2.5
          });
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
    const { name, value } = e.target;
    setUserPreferences({
      ...userPreferences,
      [name]: value,
    });
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
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <StyledPaper>
        <Tabs value={tabValue} onChange={handleTabChange} indicatorColor="primary" textColor="primary">
          <Tab label="Anomaly Detection" />
          <Tab label="Privacy" />
          <Tab label="User Preferences" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Typography variant="h6" gutterBottom>
            Anomaly Detection Statistics
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <StyledPaper>
                <Typography variant="subtitle1" gutterBottom>
                  Recent Anomalies
                </Typography>
                <Typography variant="h3" align="center" color="primary">
                  {anomalies?.length || 0}
                </Typography>
                <Typography variant="body2" color="textSecondary" align="center">
                  Last 24 hours
                </Typography>
              </StyledPaper>
            </Grid>
            
            <Grid item xs={12} sm={6}>
              <StyledPaper>
                <Typography variant="subtitle1" gutterBottom>
                  Detection Rate
                </Typography>
                <Typography variant="h3" align="center" color="primary">
                  {((anomalies?.length || 0) / (stats?.totalRecords || 1) * 100).toFixed(1)}%
                </Typography>
                <Typography variant="body2" color="textSecondary" align="center">
                  Percentage of anomalous events
                </Typography>
              </StyledPaper>
            </Grid>

            <Grid item xs={12} sm={6}>
              <StyledPaper>
                <Typography variant="subtitle1" gutterBottom>
                  Average Response Time
                </Typography>
                <Typography variant="h3" align="center" color="warning">
                  {stats?.averageResponseTime || '< 1'} min
                </Typography>
                <Typography variant="body2" color="textSecondary" align="center">
                  Time to detect anomalies
                </Typography>
              </StyledPaper>
            </Grid>

            <Grid item xs={12} sm={6}>
              <StyledPaper>
                <Typography variant="subtitle1" gutterBottom>
                  Model Accuracy
                </Typography>
                <Typography variant="h3" align="center" color="success">
                  {(stats?.modelAccuracy || 0.95 * 100).toFixed(1)}%
                </Typography>
                <Typography variant="body2" color="textSecondary" align="center">
                  Based on validated predictions
                </Typography>
              </StyledPaper>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Typography variant="h6" gutterBottom>
            Privacy Settings
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="data-visibility-label">Default Data Visibility</InputLabel>
                <Select
                  labelId="data-visibility-label"
                  id="defaultDataVisibility"
                  name="defaultDataVisibility"
                  value={privacySettings.defaultDataVisibility}
                  onChange={handlePrivacySettingsChange}
                  label="Default Data Visibility"
                >
                  <MenuItem value="private">Private (Only You)</MenuItem>
                  <MenuItem value="organization">Organization</MenuItem>
                  <MenuItem value="partners">Partners</MenuItem>
                  <MenuItem value="public">Public</MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="encryption-level-label">Encryption Level</InputLabel>
                <Select
                  labelId="encryption-level-label"
                  id="encryptionLevel"
                  name="encryptionLevel"
                  value={privacySettings.encryptionLevel}
                  onChange={handlePrivacySettingsChange}
                  label="Encryption Level"
                >
                  <MenuItem value="standard">Standard</MenuItem>
                  <MenuItem value="high">High</MenuItem>
                  <MenuItem value="very-high">Very High</MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>

            <Grid item xs={12}>
              <Typography id="retention-slider" gutterBottom>
                Data Retention Period: {privacySettings.dataRetentionPeriod} days
              </Typography>
              <StyledSlider
                value={privacySettings.dataRetentionPeriod}
                onChange={handleRetentionPeriodChange}
                aria-labelledby="retention-slider"
                valueLabelDisplay="auto"
                step={30}
                marks
                min={30}
                max={365}
                
              />
            </Grid>

            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={privacySettings.allowDataSharing}
                    onChange={handlePrivacySettingsChange}
                    name="allowDataSharing"
                    color="primary"
                  />
                }
                label="Allow data sharing with trusted partners"
              />
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={2}>
          <Typography variant="h6" gutterBottom>
            User Preferences
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="theme-label">Theme</InputLabel>
                <Select
                  labelId="theme-label"
                  id="theme"
                  name="theme"
                  value={userPreferences.theme}
                  onChange={handleUserPreferencesChange}
                  label="Theme"
                >
                  <MenuItem value="light">Light</MenuItem>
                  <MenuItem value="dark">Dark</MenuItem>
                  <MenuItem value="system">System Default</MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="language-label">Language</InputLabel>
                <Select
                  labelId="language-label"
                  id="language"
                  name="language"
                  value={userPreferences.language}
                  onChange={handleUserPreferencesChange}
                  label="Language"
                >
                  <MenuItem value="en">English</MenuItem>
                  <MenuItem value="es">Spanish</MenuItem>
                  <MenuItem value="fr">French</MenuItem>
                  <MenuItem value="de">German</MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography id="refresh-rate-slider" gutterBottom>
                Dashboard Refresh Rate: {userPreferences.dashboardRefreshRate} minutes
              </Typography>
              <StyledSlider
                value={userPreferences.dashboardRefreshRate}
                onChange={handleRefreshRateChange}
                aria-labelledby="refresh-rate-slider"
                valueLabelDisplay="auto"
                step={1}
                marks
                min={1}
                max={30}
                
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <StyledFormControl fullWidth variant="outlined">
                <InputLabel id="date-format-label">Date Format</InputLabel>
                <Select
                  labelId="date-format-label"
                  id="dateFormat"
                  name="dateFormat"
                  value={userPreferences.dateFormat}
                  onChange={handleUserPreferencesChange}
                  label="Date Format"
                >
                  <MenuItem value="MM/DD/YYYY">MM/DD/YYYY</MenuItem>
                  <MenuItem value="DD/MM/YYYY">DD/MM/YYYY</MenuItem>
                  <MenuItem value="YYYY-MM-DD">YYYY-MM-DD</MenuItem>
                </Select>
              </StyledFormControl>
            </Grid>
          </Grid>
        </TabPanel>

        <StyledDivider />

        <SaveButton
          variant="contained"
          color="primary"
          onClick={handleSaveSettings}
          disabled={loading}
          startIcon={<Save />}
        >
          {loading ? <CircularProgress size={24} /> : 'Save Settings'}
        </SaveButton>
      </StyledPaper>

      {/* Snackbar for notifications */}
      <Snackbar open={!!error || success} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity={error ? 'error' : 'success'}>
          {error || 'Settings saved successfully'}
        </Alert>
      </Snackbar>
    </Root>
  );
};

export default Settings;