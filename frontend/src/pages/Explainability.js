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
  Box,
  CircularProgress,
  Card,
  CardContent,
  Divider,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
} from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import { InfoOutlined, ErrorOutline, CheckCircleOutline } from '@material-ui/icons';
import { getAnomalyExplanation } from '../store/slices/anomalySlice';
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
  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing(4),
  },
  card: {
    marginBottom: theme.spacing(2),
  },
  featureImportance: {
    marginTop: theme.spacing(2),
  },
  featureBar: {
    height: 20,
    borderRadius: 5,
    marginTop: 5,
    marginBottom: 10,
  },
  positiveBar: {
    backgroundColor: theme.palette.success.main,
  },
  negativeBar: {
    backgroundColor: theme.palette.error.main,
  },
  chartContainer: {
    height: 400,
    marginTop: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  divider: {
    margin: theme.spacing(2, 0),
  },
  blockchainVerification: {
    backgroundColor: theme.palette.info.light,
    padding: theme.spacing(2),
    borderRadius: theme.shape.borderRadius,
    marginTop: theme.spacing(2),
  },
}));

const Explainability = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const { user } = useSelector((state) => state.auth);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modelMetrics, setModelMetrics] = useState(null);
  const [selectedAnomaly, setSelectedAnomaly] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [anomalyId, setAnomalyId] = useState('');

  useEffect(() => {
    // Fetch model metrics when component mounts
    fetchModelMetrics();
  }, []);

  const fetchModelMetrics = async () => {
    try {
      setLoading(true);
      const response = await anomalyService.getModelMetrics(user?.organizationId || 'org1');
      setModelMetrics(response);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch model metrics');
      setLoading(false);
    }
  };

  const handleAnomalyIdChange = (e) => {
    setAnomalyId(e.target.value);
  };

  const handleExplainAnomaly = async () => {
    if (!anomalyId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const response = await anomalyService.getExplanation(anomalyId, user?.organizationId || 'org1');
      setExplanation(response);
      setSelectedAnomaly(response);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to get anomaly explanation');
      setLoading(false);
    }
  };

  // Function to render feature importance bars
  const renderFeatureImportance = (features) => {
    if (!features || features.length === 0) return null;
    
    // Find the maximum importance value for scaling
    const maxImportance = Math.max(...features.map(f => Math.abs(f.importance)));
    
    return (
      <div className={classes.featureImportance}>
        <Typography variant="h6">Feature Importance</Typography>
        <Typography variant="body2" paragraph>
          Features that contributed to the anomaly detection are shown below. Positive values (red) indicate features that increased the anomaly score, while negative values (blue) indicate features that decreased it.
        </Typography>
        {features.map((feature, index) => {
          const importance = feature.importance;
          const width = `${Math.abs(importance) / maxImportance * 100}%`;
          const color = importance > 0 ? '#f44336' : '#2196f3'; // Red for positive, blue for negative
          
          return (
            <div key={index}>
              <Grid container justifyContent="space-between">
                <Grid item>
                  <Typography variant="body2">{feature.name}</Typography>
                </Grid>
                <Grid item>
                  <Typography variant="body2">{importance.toFixed(4)}</Typography>
                </Grid>
              </Grid>
              <div 
                className={classes.featureBar} 
                style={{ width, backgroundColor: color }}
              />
            </div>
          );
        })}
      </div>
    );
  };

  // Function to render blockchain verification information
  const renderBlockchainVerification = (data) => {
    if (!data) return null;
    
    return (
      <div className={classes.blockchainVerification}>
        <Typography variant="h6">Blockchain Verification</Typography>
        <List dense>
          <ListItem>
            <ListItemIcon>
              <InfoOutlined />
            </ListItemIcon>
            <ListItemText 
              primary="Transaction ID" 
              secondary={data.transactionId || 'N/A'} 
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <InfoOutlined />
            </ListItemIcon>
            <ListItemText 
              primary="Block Number" 
              secondary={data.blockNumber || 'N/A'} 
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              <InfoOutlined />
            </ListItemIcon>
            <ListItemText 
              primary="Block Timestamp" 
              secondary={data.blockTimestamp ? new Date(data.blockTimestamp).toLocaleString() : 'N/A'} 
            />
          </ListItem>
          <ListItem>
            <ListItemIcon>
              {data.verified ? <CheckCircleOutline color="primary" /> : <ErrorOutline color="error" />}
            </ListItemIcon>
            <ListItemText 
              primary="Verification Status" 
              secondary={data.verified ? 'Verified on blockchain' : 'Not verified'} 
            />
          </ListItem>
        </List>
      </div>
    );
  };

  return (
    <div className={classes.root}>
      <Typography variant="h4" gutterBottom>
        Explainability
      </Typography>

      <Paper className={classes.paper}>
        <Typography variant="h6" gutterBottom>
          Explain Anomaly Detection Results
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={8}>
            <TextField
              fullWidth
              id="anomalyId"
              name="anomalyId"
              label="Anomaly ID"
              value={anomalyId}
              onChange={handleAnomalyIdChange}
              variant="outlined"
              placeholder="Enter the ID of the anomaly to explain"
            />
          </Grid>
          <Grid item xs={12} sm={4}>
            <Button
              variant="contained"
              color="primary"
              onClick={handleExplainAnomaly}
              disabled={loading || !anomalyId}
              fullWidth
              style={{ height: '100%' }}
            >
              {loading ? <CircularProgress size={24} /> : 'Explain'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {error && (
        <Alert severity="error" style={{ marginBottom: 16 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <div className={classes.loadingContainer}>
          <CircularProgress />
        </div>
      ) : explanation ? (
        <>
          <Card className={classes.card}>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Anomaly Explanation
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1">Anomaly ID:</Typography>
                  <Typography variant="body1">{explanation.anomalyId}</Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1">Product ID:</Typography>
                  <Typography variant="body1">{explanation.productId}</Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1">Data Type:</Typography>
                  <Typography variant="body1">{explanation.dataType}</Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1">Timestamp:</Typography>
                  <Typography variant="body1">{new Date(explanation.timestamp).toLocaleString()}</Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle1">Anomaly Score:</Typography>
                  <Typography variant="body1">{explanation.anomalyScore.toFixed(4)}</Typography>
                </Grid>
              </Grid>

              <Divider className={classes.divider} />

              <Typography variant="h6">Summary</Typography>
              <Typography variant="body1" paragraph>
                {explanation.summary}
              </Typography>

              {renderFeatureImportance(explanation.featureImportance)}

              {renderBlockchainVerification(explanation)}
            </CardContent>
          </Card>

          {modelMetrics && (
            <Card className={classes.card}>
              <CardContent>
                <Typography variant="h5" gutterBottom>
                  Model Performance Metrics
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle1">Precision:</Typography>
                    <Typography variant="body1">{modelMetrics.precision.toFixed(4)}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle1">Recall:</Typography>
                    <Typography variant="body1">{modelMetrics.recall.toFixed(4)}</Typography>
                  </Grid>
                  <Grid item xs={12} sm={4}>
                    <Typography variant="subtitle1">F1 Score:</Typography>
                    <Typography variant="body1">{modelMetrics.f1Score.toFixed(4)}</Typography>
                  </Grid>
                  <Grid item xs={12}>
                    <Typography variant="subtitle1">Model Description:</Typography>
                    <Typography variant="body1">{modelMetrics.modelDescription}</Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          )}
        </>
      ) : null}
    </div>
  );
};

export default Explainability;