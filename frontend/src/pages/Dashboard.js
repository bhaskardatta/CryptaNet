import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { makeStyles } from '@material-ui/core/styles';
import {
  Grid,
  Paper,
  Typography,
  Card,
  CardContent,
  CircularProgress,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Divider,
} from '@material-ui/core';
import {
  Timeline,
  ErrorOutline,
  CheckCircleOutline,
  Storage,
  Security,
  ShowChart,
  Info,
} from '@material-ui/icons';
import { fetchSupplyChainData } from '../store/slices/supplyChainSlice';
import { detectAnomalies } from '../store/slices/anomalySlice';
import { anomalyService } from '../services/anomalyService';
import { supplyChainService } from '../services/supplyChainService';

const useStyles = makeStyles((theme) => ({
  root: {
    flexGrow: 1,
  },
  paper: {
    padding: theme.spacing(2),
    display: 'flex',
    overflow: 'auto',
    flexDirection: 'column',
  },
  fixedHeight: {
    height: 240,
  },
  statsCard: {
    height: '100%',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
  },
  statsValue: {
    fontSize: '2rem',
    fontWeight: 'bold',
    marginTop: theme.spacing(1),
    marginBottom: theme.spacing(1),
  },
  anomalyCard: {
    backgroundColor: theme.palette.error.light,
  },
  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100%',
  },
  statusIcon: {
    marginRight: theme.spacing(1),
  },
  statusItem: {
    marginBottom: theme.spacing(1),
  },
  divider: {
    margin: theme.spacing(2, 0),
  },
  cardHeader: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: theme.spacing(2),
  },
  headerIcon: {
    marginRight: theme.spacing(1),
    color: theme.palette.primary.main,
  },
}));

const Dashboard = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const { data: supplyChainData, loading: supplyChainLoading } = useSelector((state) => state.supplyChain);
  const { anomalies, loading: anomalyLoading } = useSelector((state) => state.anomaly);
  const { user } = useSelector((state) => state.auth);
  const [systemStatus, setSystemStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [recentAnomalies, setRecentAnomalies] = useState([]);
  const [stats, setStats] = useState({
    totalRecords: 0,
    anomalyCount: 0,
    lastUpdated: null,
  });

  useEffect(() => {
    // Fetch initial data
    fetchDashboardData();

    // Set up interval to refresh data every 5 minutes
    const interval = setInterval(() => {
      fetchDashboardData();
    }, 5 * 60 * 1000);

    return () => clearInterval(interval);
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);

    // Set date range for last 30 days
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 30);

    // Fetch supply chain data
    dispatch(fetchSupplyChainData({
      organizationId: user?.organizationId || 'org1',
      dataType: 'all',
      startTime: startDate.toISOString(),
      endTime: endDate.toISOString(),
      includeAnomaliesOnly: false,
    }));

    // Fetch anomalies
    dispatch(detectAnomalies({
      organizationId: user?.organizationId || 'org1',
      dataType: 'all',
      startTime: startDate.toISOString(),
      endTime: endDate.toISOString(),
      threshold: 0.5,
    }));

    try {
      // Fetch system status
      const response = await fetch('/api/system/status', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`,
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        setSystemStatus(data);
      }
    } catch (error) {
      console.error('Error fetching system status:', error);
      // Set default status if API fails
      setSystemStatus({
        blockchain: 'available',
        anomaly_detection: 'available',
        explainability: 'available',
        privacy_layer: 'available',
      });
    }

    setLoading(false);
  };

  useEffect(() => {
    // Update stats when data changes
    if (supplyChainData) {
      setStats({
        totalRecords: supplyChainData.length,
        anomalyCount: anomalies ? anomalies.length : 0,
        lastUpdated: new Date(),
      });
    }

    // Get most recent anomalies
    if (anomalies && anomalies.length > 0) {
      // Sort by timestamp (newest first) and take top 5
      const sorted = [...anomalies].sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp)).slice(0, 5);
      setRecentAnomalies(sorted);
    }
  }, [supplyChainData, anomalies]);

  const renderSystemStatus = () => {
    if (!systemStatus) return null;

    const statusItems = [
      { name: 'Blockchain Network', status: systemStatus.blockchain },
      { name: 'Anomaly Detection', status: systemStatus.anomaly_detection },
      { name: 'Explainability Module', status: systemStatus.explainability },
      { name: 'Privacy Layer', status: systemStatus.privacy_layer },
    ];

    return (
      <List>
        {statusItems.map((item, index) => (
          <React.Fragment key={index}>
            <ListItem className={classes.statusItem}>
              <ListItemIcon>
                {item.status === 'available' ? (
                  <CheckCircleOutline style={{ color: 'green' }} />
                ) : (
                  <ErrorOutline color="error" />
                )}
              </ListItemIcon>
              <ListItemText
                primary={item.name}
                secondary={item.status === 'available' ? 'Operational' : 'Not Available'}
              />
            </ListItem>
            {index < statusItems.length - 1 && <Divider component="li" />}
          </React.Fragment>
        ))}
      </List>
    );
  };

  const renderRecentAnomalies = () => {
    if (recentAnomalies.length === 0) {
      return (
        <Typography variant="body2" color="textSecondary">
          No anomalies detected in the last 30 days.
        </Typography>
      );
    }

    return (
      <List>
        {recentAnomalies.map((anomaly, index) => (
          <React.Fragment key={anomaly.id}>
            <ListItem>
              <ListItemIcon>
                <ErrorOutline color="error" />
              </ListItemIcon>
              <ListItemText
                primary={`${anomaly.dataType} anomaly in product ${anomaly.productId}`}
                secondary={`Detected on ${new Date(anomaly.timestamp).toLocaleString()} - Score: ${anomaly.anomalyScore.toFixed(4)}`}
              />
            </ListItem>
            {index < recentAnomalies.length - 1 && <Divider component="li" />}
          </React.Fragment>
        ))}
      </List>
    );
  };

  if (loading || supplyChainLoading || anomalyLoading) {
    return (
      <div className={classes.loadingContainer}>
        <CircularProgress />
      </div>
    );
  }

  return (
    <div className={classes.root}>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* Stats Cards */}
        <Grid item xs={12} md={4}>
          <Paper className={classes.paper}>
            <Card className={classes.statsCard}>
              <CardContent>
                <div className={classes.cardHeader}>
                  <Storage className={classes.headerIcon} />
                  <Typography variant="h6" component="h2">
                    Total Records
                  </Typography>
                </div>
                <Typography className={classes.statsValue} color="textPrimary">
                  {stats.totalRecords}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Last 30 days
                </Typography>
              </CardContent>
            </Card>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper className={classes.paper}>
            <Card className={classes.statsCard}>
              <CardContent>
                <div className={classes.cardHeader}>
                  <ErrorOutline className={classes.headerIcon} />
                  <Typography variant="h6" component="h2">
                    Anomalies Detected
                  </Typography>
                </div>
                <Typography className={classes.statsValue} color="error">
                  {stats.anomalyCount}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Last 30 days
                </Typography>
              </CardContent>
            </Card>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper className={classes.paper}>
            <Card className={classes.statsCard}>
              <CardContent>
                <div className={classes.cardHeader}>
                  <Timeline className={classes.headerIcon} />
                  <Typography variant="h6" component="h2">
                    Last Updated
                  </Typography>
                </div>
                <Typography className={classes.statsValue} color="textPrimary">
                  {stats.lastUpdated ? new Date(stats.lastUpdated).toLocaleTimeString() : 'N/A'}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {stats.lastUpdated ? new Date(stats.lastUpdated).toLocaleDateString() : ''}
                </Typography>
              </CardContent>
            </Card>
          </Paper>
        </Grid>

        {/* System Status */}
        <Grid item xs={12} md={6}>
          <Paper className={classes.paper}>
            <div className={classes.cardHeader}>
              <Info className={classes.headerIcon} />
              <Typography variant="h6" component="h2">
                System Status
              </Typography>
            </div>
            {renderSystemStatus()}
            <Button 
              variant="outlined" 
              color="primary" 
              onClick={fetchDashboardData}
              style={{ marginTop: 16 }}
            >
              Refresh Status
            </Button>
          </Paper>
        </Grid>

        {/* Recent Anomalies */}
        <Grid item xs={12} md={6}>
          <Paper className={classes.paper}>
            <div className={classes.cardHeader}>
              <ShowChart className={classes.headerIcon} />
              <Typography variant="h6" component="h2">
                Recent Anomalies
              </Typography>
            </div>
            {renderRecentAnomalies()}
            <Button 
              variant="outlined" 
              color="primary" 
              href="/anomaly-detection"
              style={{ marginTop: 16 }}
            >
              View All Anomalies
            </Button>
          </Paper>
        </Grid>
      </Grid>
    </div>
  );
};

export default Dashboard;