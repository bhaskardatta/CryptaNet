import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { 
  Typography, Grid, Card, CardContent, Table, TableBody, TableCell, 
  TableContainer, TableHead, TableRow, Button, Paper, FormControl, 
  InputLabel, Select, MenuItem, TextField, CircularProgress, Dialog, 
  DialogTitle, DialogContent, DialogActions, Snackbar, Alert, IconButton,
  Slider
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { Search, InfoOutlined } from '@mui/icons-material';
import { detectAnomalies, getAnomalyExplanation, clearError, clearSuccess, clearSelectedAnomaly } from '../store/slices/anomalySlice';

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

const TableContainerStyled = styled(TableContainer)(({ theme }) => ({
  marginTop: theme.spacing(2),
}));

const LoadingContainer = styled('div')(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  padding: theme.spacing(4),
}));

const AnomalyCard = styled(Card)(({ theme }) => ({
  backgroundColor: theme.palette.error.light,
  marginBottom: theme.spacing(2),
}));

const ExplanationCard = styled(Card)(({ theme }) => ({
  marginTop: theme.spacing(2),
}));

const FeatureImportanceContainer = styled('div')(({ theme }) => ({
  marginTop: theme.spacing(2),
}));

const FeatureBar = styled('div')({
  height: 20,
  borderRadius: 5,
  marginTop: 5,
  marginBottom: 10,
});

const AnomalyDetection = () => {
  const dispatch = useDispatch();
  const { anomalies, explanation, loading, error, success } = useSelector((state) => state.anomaly);
  const { user } = useSelector((state) => state.auth);
  const [queryParams, setQueryParams] = useState({
    dataType: 'all',
    startTime: '',
    endTime: '',
    threshold: 0.5,
  });
  const [explanationOpen, setExplanationOpen] = useState(false);

  useEffect(() => {
    // Initial data fetch
    dispatch(detectAnomalies({
      organizationId: user?.organization || 'Org1MSP',
      ...queryParams,
    }));
  }, [dispatch, user]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleQueryChange = (e) => {
    const { name, value } = e.target;
    setQueryParams({
      ...queryParams,
      [name]: value,
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
      <FeatureImportanceContainer>
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
              <FeatureBar 
                sx={{ width, backgroundColor: color }}
              />
            </div>
          );
        })}
      </FeatureImportanceContainer>
    );
  };

  return (
    <Root>
      <Typography variant="h4" gutterBottom>
        Anomaly Detection
      </Typography>

      <StyledPaper>
        <Typography variant="h6" gutterBottom>
          Detect Anomalies in Supply Chain Data
        </Typography>
        <form onSubmit={handleDetectAnomalies}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <StyledFormControl fullWidth variant="outlined">
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
              </StyledFormControl>
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
              <StyledSlider
                value={queryParams.threshold}
                onChange={handleThresholdChange}
                aria-labelledby="threshold-slider"
                valueLabelDisplay="auto"
                step={0.05}
                marks
                min={0}
                max={1}
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
                {loading ? <CircularProgress size={24} /> : 'Detect Anomalies'}
              </Button>
            </Grid>
          </Grid>
        </form>
      </StyledPaper>

      {error && (
        <Alert severity="error" sx={{ marginBottom: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ marginBottom: 2 }}>
          {success}
        </Alert>
      )}

      {loading ? (
        <LoadingContainer>
          <CircularProgress />
        </LoadingContainer>
      ) : (
        <>
          {anomalies && anomalies.length > 0 ? (
            <>
              <Typography variant="h6" gutterBottom>
                Detected Anomalies ({anomalies.length})
              </Typography>
              <TableContainerStyled component={Paper}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>ID</TableCell>
                      <TableCell>Product ID</TableCell>
                      <TableCell>Data Type</TableCell>
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
              </TableContainerStyled>
            </>
          ) : (
            anomalies && (
              <StyledPaper>
                <Typography variant="body1" align="center">
                  No anomalies detected with the current threshold.
                </Typography>
              </StyledPaper>
            )
          )}
        </>
      )}

      {/* Explanation Dialog */}
      <Dialog open={explanationOpen} onClose={handleCloseExplanation} maxWidth="md" fullWidth>
        <DialogTitle>Anomaly Explanation</DialogTitle>
        <DialogContent>
          {loading ? (
            <LoadingContainer>
              <CircularProgress />
            </LoadingContainer>
          ) : explanation ? (
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <AnomalyCard>
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
                </AnomalyCard>
              </Grid>
              
              <Grid item xs={12}>
                <ExplanationCard>
                  <CardContent>
                    <Typography variant="h6">Explanation</Typography>
                    <Typography variant="body1" paragraph>
                      {explanation.summary}
                    </Typography>
                    
                    {renderFeatureImportance(explanation.featureImportance)}
                    
                    <Typography variant="subtitle1" sx={{ marginTop: 2 }}>
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
                </ExplanationCard>
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
    </Root>
  );
};

export default AnomalyDetection;