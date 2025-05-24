import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { makeStyles } from '@material-ui/core/styles';
import {
  Paper,
  Typography,
  Grid,
  Button,
  TextField,
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
} from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import { Save, Refresh } from '@material-ui/icons';
import { anomalyService } from '../services/anomalyService';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  formControl: {
    margin: theme.spacing(1),
    minWidth: 120,
  },
  tabContent: {
    padding: theme.spacing(2),
  },
  slider: {
    width: '100%',
    padding: theme.spacing(0, 2),
  },
  divider: {
    margin: theme.spacing(2, 0),
  },
  saveButton: {
    marginTop: theme.spacing(2),
  },
  card: {
    marginBottom: theme.spacing(2),
  },
  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing(4),
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
  const classes = useStyles();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const [tabValue, setTabValue] = useState(0);
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [error, setError] = useState(null);
  
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

  useEffect(() => {
    // Fetch user settings
    fetchSettings();
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

  const handleAnomalySettingsChange = (e) => {
    const { name, value, checked } = e.target;
    setAnomalySettings({
      ...anomalySettings,
      [name]: e.target.type === 'checkbox' ? checked : value,
    });
  };

  const handleThresholdChange = (event, newValue) => {
    setAnomalySettings({
      ...anomalySettings,
      defaultThreshold: newValue,
    });
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

  const handleTrainModel = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('Starting model training with settings:', {
        threshold: anomalySettings.defaultThreshold,
        auto_train: anomalySettings.autoTrain,
        model_type: anomalySettings.modelType
      });
      
      // Call the anomaly service to train the model
      const response = await fetch('http://localhost:5002/train', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          threshold: anomalySettings.defaultThreshold,
          auto_train: anomalySettings.autoTrain,
          model_type: anomalySettings.modelType,
          n_estimators: 100,
          // Add feature count based on model type
          feature_count: anomalySettings.modelType === 'comprehensive' ? 5 : 3,
          samples: 1000 // Increase sample size for better training
        })
      });
      
      if (response.ok) {
        const result = await response.json();
        console.log('Model training result:', result);
        if (result.success) {
          setSuccess(true);
          // Set a more descriptive success message
          setSuccessMessage(`Model trained successfully with ${result.details?.samples || 'unknown'} samples and ${result.details?.features || 'unknown'} features.`);
        } else {
          throw new Error(result.message || 'Training completed with errors');
        }
      } else {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`Failed to train model: ${errorData.message || response.statusText}`);
      }
      setLoading(false);
    } catch (err) {
      console.error('Error training model:', err);
      setError(`Failed to train model: ${err.message || 'Unknown error'}`);
      setLoading(false);
    }
  };

  const handleCloseSnackbar = () => {
    setSuccess(false);
    setError(null);
  };

  return (
    <div className={classes.root}>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <Paper className={classes.paper}>
        <Tabs value={tabValue} onChange={handleTabChange} indicatorColor="primary" textColor="primary">
          <Tab label="Anomaly Detection" />
          <Tab label="Privacy" />
          <Tab label="User Preferences" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Typography variant="h6" gutterBottom>
            Anomaly Detection Settings
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <Typography id="threshold-slider" gutterBottom>
                Default Anomaly Threshold: {anomalySettings.defaultThreshold}
              </Typography>
              <Slider
                value={anomalySettings.defaultThreshold}
                onChange={handleThresholdChange}
                aria-labelledby="threshold-slider"
                valueLabelDisplay="auto"
                step={0.05}
                marks
                min={0}
                max={1}
                className={classes.slider}
              />
              <Typography variant="body2" color="textSecondary">
                Higher values detect fewer anomalies but with higher confidence.
              </Typography>
            </Grid>

            <Grid item xs={12} sm={6}>
              <FormControl fullWidth variant="outlined" className={classes.formControl}>
                <InputLabel id="model-type-label">Model Type</InputLabel>
                <Select
                  labelId="model-type-label"
                  id="modelType"
                  name="modelType"
                  value={anomalySettings.modelType}
                  onChange={handleAnomalySettingsChange}
                  label="Model Type"
                >
                  <MenuItem value="isolation_forest">Isolation Forest</MenuItem>
                  <MenuItem value="one_class_svm">One-Class SVM</MenuItem>
                  <MenuItem value="local_outlier_factor">Local Outlier Factor</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <FormControlLabel
                control={
                  <Switch
                    checked={anomalySettings.autoTrain}
                    onChange={handleAnomalySettingsChange}
                    name="autoTrain"
                    color="primary"
                  />
                }
                label="Auto-train model with new data"
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <FormControl fullWidth variant="outlined" className={classes.formControl}>
                <InputLabel id="training-frequency-label">Training Frequency</InputLabel>
                <Select
                  labelId="training-frequency-label"
                  id="trainingFrequency"
                  name="trainingFrequency"
                  value={anomalySettings.trainingFrequency}
                  onChange={handleAnomalySettingsChange}
                  label="Training Frequency"
                  disabled={!anomalySettings.autoTrain}
                >
                  <MenuItem value="daily">Daily</MenuItem>
                  <MenuItem value="weekly">Weekly</MenuItem>
                  <MenuItem value="monthly">Monthly</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Switch
                    checked={anomalySettings.notificationsEnabled}
                    onChange={handleAnomalySettingsChange}
                    name="notificationsEnabled"
                    color="primary"
                  />
                }
                label="Enable anomaly detection notifications"
              />
            </Grid>

            <Grid item xs={12}>
              <Button
                variant="contained"
                color="secondary"
                onClick={handleTrainModel}
                disabled={loading}
                startIcon={<Refresh />}
              >
                {loading ? <CircularProgress size={24} /> : 'Train Model Now'}
              </Button>
            </Grid>
          </Grid>
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Typography variant="h6" gutterBottom>
            Privacy Settings
          </Typography>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth variant="outlined" className={classes.formControl}>
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
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <FormControl fullWidth variant="outlined" className={classes.formControl}>
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
              </FormControl>
            </Grid>

            <Grid item xs={12}>
              <Typography id="retention-slider" gutterBottom>
                Data Retention Period: {privacySettings.dataRetentionPeriod} days
              </Typography>
              <Slider
                value={privacySettings.dataRetentionPeriod}
                onChange={handleRetentionPeriodChange}
                aria-labelledby="retention-slider"
                valueLabelDisplay="auto"
                step={30}
                marks
                min={30}
                max={365}
                className={classes.slider}
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
              <FormControl fullWidth variant="outlined" className={classes.formControl}>
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
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <FormControl fullWidth variant="outlined" className={classes.formControl}>
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
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6}>
              <Typography id="refresh-rate-slider" gutterBottom>
                Dashboard Refresh Rate: {userPreferences.dashboardRefreshRate} minutes
              </Typography>
              <Slider
                value={userPreferences.dashboardRefreshRate}
                onChange={handleRefreshRateChange}
                aria-labelledby="refresh-rate-slider"
                valueLabelDisplay="auto"
                step={1}
                marks
                min={1}
                max={30}
                className={classes.slider}
              />
            </Grid>

            <Grid item xs={12} sm={6}>
              <FormControl fullWidth variant="outlined" className={classes.formControl}>
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
              </FormControl>
            </Grid>
          </Grid>
        </TabPanel>

        <Divider className={classes.divider} />

        <Button
          variant="contained"
          color="primary"
          onClick={handleSaveSettings}
          disabled={loading}
          className={classes.saveButton}
          startIcon={<Save />}
        >
          {loading ? <CircularProgress size={24} /> : 'Save Settings'}
        </Button>
      </Paper>

      {/* Snackbar for notifications */}
      <Snackbar open={!!error || success} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity={error ? 'error' : 'success'}>
          {error || successMessage || 'Settings saved successfully'}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default Settings;