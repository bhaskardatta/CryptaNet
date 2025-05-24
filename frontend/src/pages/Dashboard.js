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

    try {
      // Get token from localStorage
      const token = localStorage.getItem('token');
      
      if (!token) {
        console.log('No token found, user needs to login');
        setLoading(false);
        return;
      }

      // Fetch data directly from the backend API
      const response = await fetch(`/api/supply-chain/query?organizationId=${user?.organization || 'Org1MSP'}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('Dashboard API response:', data);
        
        // Handle both possible response structures
        const results = data.results || data.data || [];
        const totalCount = data.count || data.total || results.length;
        
        // Update stats based on actual data
        setStats({
          totalRecords: totalCount,
          anomaliesDetected: results.filter(item => item.is_anomaly).length,
          dataProcessed: totalCount,
          systemHealth: 95
        });
        
        // Set recent anomalies
        const anomalies = results.filter(item => item.is_anomaly).slice(0, 5);
        setRecentAnomalies(anomalies);
        
        // Also dispatch Redux action to update global state
        dispatch(fetchSupplyChainData({
          organizationId: user?.organization || 'Org1MSP',
          dataType: 'all',
          includeAnomaliesOnly: false,
        }));
        
      } else {
        console.error('Failed to fetch data:', response.status, response.statusText);
      }
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
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
    if (!recentAnomalies || recentAnomalies.length === 0) {
      return (
        <Typography variant="body2" color="textSecondary">
          No anomalies detected in the last 30 days.
        </Typography>
      );
    }

    return (
      <List>
        {recentAnomalies.map((anomaly, index) => {
          // Extract data properly based on the structure
          const productId = anomaly.productId || anomaly.data?.productId || 'N/A';
          const productName = anomaly.data?.product || anomaly.product || 'Unknown Product';
          const timestamp = (() => {
            if (!anomaly.timestamp) return 'Unknown time';
            try {
              const date = new Date(anomaly.timestamp);
              return isNaN(date.getTime()) ? 'Invalid Date' : date.toLocaleString();
            } catch (e) {
              return 'Invalid Date';
            }
          })();
          const anomalyScore = anomaly.anomaly_score || anomaly.anomalyScore || 0;
          const scoreDisplay = typeof anomalyScore === 'number' ? 
            anomalyScore.toFixed(4) : 'Unknown';
          const location = anomaly.data?.location || 'Unknown location';
          const temperature = anomaly.data?.temperature || 'N/A';
          const humidity = anomaly.data?.humidity || 'N/A';
          
          return (
            <React.Fragment key={anomaly.id || index}>
              <ListItem>
                <ListItemIcon>
                  <ErrorOutline color="error" />
                </ListItemIcon>
                <ListItemText
                  primary={`${productId}: ${productName} - ${location}`}
                  secondary={
                    <>
                      <Typography component="span" variant="body2" color="error">
                        Anomaly detected!
                      </Typography>
                      <br />
                      <Typography component="span" variant="body2">
                        {timestamp} - Score: {scoreDisplay}
                      </Typography>
                      <br />
                      <Typography component="span" variant="body2">
                        Temperature: {temperature}°C, Humidity: {humidity}%
                      </Typography>
                    </>
                  }
                />
              </ListItem>
              {index < recentAnomalies.length - 1 && <Divider component="li" />}
            </React.Fragment>
          );
        })}
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