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
  Slider,
  Box,
  CircularProgress,
  Snackbar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  IconButton,
  Card,
  CardContent,
} from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import { Visibility, Search, InfoOutlined } from '@material-ui/icons';
import { detectAnomalies, getAnomalyExplanation, clearError, clearSuccess, setSelectedAnomaly, clearSelectedAnomaly } from '../store/slices/anomalySlice';

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
  slider: {
    width: '100%',
    padding: theme.spacing(0, 2),
  },
  tableContainer: {
    marginTop: theme.spacing(2),
  },
  loadingContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    padding: theme.spacing(4),
  },
  anomalyCard: {
    backgroundColor: theme.palette.error.light,
    marginBottom: theme.spacing(2),
  },
  explanationCard: {
    marginTop: theme.spacing(2),
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
}));

const AnomalyDetection = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const { anomalies, selectedAnomaly, explanation, loading, error, success } = useSelector((state) => state.anomaly);
  const { user } = useSelector((state) => state.auth);
  const [queryParams, setQueryParams] = useState({
    dataType: 'all',
    startTime: '',
    endTime: '',
    threshold: 0.5,
  });
  const [explanationOpen, setExplanationOpen] = useState(false);

  useEffect(() => {
    // Set default date range to last 7 days
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 7);
    
    setQueryParams({
      ...queryParams,
      startTime: startDate.toISOString().split('T')[0],
      endTime: endDate.toISOString().split('T')[0],
    });
  }, []);

  const handleQueryChange = (e) => {
    setQueryParams({
      ...queryParams,
      [e.target.name]: e.target.value,
    });
  };

  const handleThresholdChange = (event, newValue) => {
    setQueryParams({
      ...queryParams,
      threshold: newValue,
    });
  };

  const handleDetectAnomalies = (e) => {
    e.preventDefault();
    dispatch(detectAnomalies({
      organizationId: user?.organization || 'Org1MSP',
      ...queryParams,
    }));
  };

  const handleViewExplanation = (anomalyId) => {
    dispatch(getAnomalyExplanation({
      anomalyId,
      organizationId: user?.organization || 'Org1MSP',
    }));
    setExplanationOpen(true);
  };

  const handleCloseExplanation = () => {
    setExplanationOpen(false);
    dispatch(clearSelectedAnomaly());
  };

  const handleCloseSnackbar = () => {
    dispatch(clearError());
    dispatch(clearSuccess());
  };

  // Function to render feature importance bars
  const renderFeatureImportance = (features) => {
    if (!features || features.length === 0) return null;
    
    // Find the maximum importance value for scaling
    const maxImportance = Math.max(...features.map(f => Math.abs(f.importance)));
    
    return (
      <div className={classes.featureImportance}>
        <Typography variant="h6">Feature Importance</Typography>
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

  return (
    <div className={classes.root}>
      <Typography variant="h4" gutterBottom>
        Anomaly Detection
      </Typography>

      <Paper className={classes.paper}>
        <Typography variant="h6" gutterBottom>
          Detect Anomalies in Supply Chain Data
        </Typography>
        <form onSubmit={handleDetectAnomalies}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <FormControl fullWidth variant="outlined" className={classes.formControl}>
                <InputLabel id="data-type-label">Data Type</InputLabel>
                <Select
                  labelId="data-type-label"
                  id="dataType"
                  name="dataType"
                  value={queryParams.dataType}
                  onChange={handleQueryChange}
                  label="Data Type"
                >
                  <MenuItem value="all">All</MenuItem>
                  <MenuItem value="temperature">Temperature</MenuItem>
                  <MenuItem value="humidity">Humidity</MenuItem>
                  <MenuItem value="location">Location</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                id="startTime"
                name="startTime"
                label="Start Date"
                type="date"
                value={queryParams.startTime}
                onChange={handleQueryChange}
                variant="outlined"
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <TextField
                fullWidth
                id="endTime"
                name="endTime"
                label="End Date"
                type="date"
                value={queryParams.endTime}
                onChange={handleQueryChange}
                variant="outlined"
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Typography id="threshold-slider" gutterBottom>
                Anomaly Threshold: {queryParams.threshold}
              </Typography>
              <Slider
                value={queryParams.threshold}
                onChange={handleThresholdChange}
                aria-labelledby="threshold-slider"
                valueLabelDisplay="auto"
                step={0.05}
                marks
                min={0}
                max={1}
                className={classes.slider}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                startIcon={<Search />}
                disabled={loading}
              >
                Detect Anomalies
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>

      {loading ? (
        <div className={classes.loadingContainer}>
          <CircularProgress />
        </div>
      ) : (
        <>
          {anomalies && anomalies.length > 0 ? (
            <>
              <Typography variant="h6" gutterBottom>
                Detected Anomalies ({anomalies.length})
              </Typography>
              <TableContainer component={Paper} className={classes.tableContainer}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>ID</TableCell>
                      <TableCell>Product ID</TableCell>
                      <TableCell>Type</TableCell>
                      <TableCell>Timestamp</TableCell>
                      <TableCell>Anomaly Score</TableCell>
                      <TableCell>Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {anomalies.map((anomaly) => (
                      <TableRow key={anomaly.id}>
                        <TableCell>{anomaly.id}</TableCell>
                        <TableCell>{anomaly.productId}</TableCell>
                        <TableCell>{anomaly.dataType}</TableCell>
                        <TableCell>{new Date(anomaly.timestamp).toLocaleString()}</TableCell>
                        <TableCell>{anomaly.anomalyScore.toFixed(4)}</TableCell>
                        <TableCell>
                          <IconButton onClick={() => handleViewExplanation(anomaly.id)}>
                            <InfoOutlined />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </>
          ) : (
            anomalies && (
              <Paper className={classes.paper}>
                <Typography variant="body1" align="center">
                  No anomalies detected with the current threshold.
                </Typography>
              </Paper>
            )
          )}
        </>
      )}

      {/* Explanation Dialog */}
      <Dialog open={explanationOpen} onClose={handleCloseExplanation} maxWidth="md" fullWidth>
        <DialogTitle>Anomaly Explanation</DialogTitle>
        <DialogContent>
          {loading ? (
            <div className={classes.loadingContainer}>
              <CircularProgress />
            </div>
          ) : explanation ? (
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Card className={classes.anomalyCard}>
                  <CardContent>
                    <Typography variant="h6">Anomaly Details</Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="subtitle1">ID:</Typography>
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
                  </CardContent>
                </Card>
              </Grid>
              
              <Grid item xs={12}>
                <Card className={classes.explanationCard}>
                  <CardContent>
                    <Typography variant="h6">Explanation</Typography>
                    <Typography variant="body1" paragraph>
                      {explanation.summary}
                    </Typography>
                    
                    {renderFeatureImportance(explanation.featureImportance)}
                    
                    <Typography variant="subtitle1" style={{ marginTop: 16 }}>
                      Blockchain Verification:
                    </Typography>
                    <Typography variant="body2">
                      Transaction ID: {explanation.transactionId || 'N/A'}
                    </Typography>
                    <Typography variant="body2">
                      Block Number: {explanation.blockNumber || 'N/A'}
                    </Typography>
                    <Typography variant="body2">
                      Timestamp: {explanation.blockTimestamp ? new Date(explanation.blockTimestamp).toLocaleString() : 'N/A'}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
          ) : (
            <Typography variant="body1">
              No explanation available for this anomaly.
            </Typography>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseExplanation} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar open={!!error || success} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity={error ? 'error' : 'success'}>
          {error || 'Operation completed successfully'}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default AnomalyDetection;