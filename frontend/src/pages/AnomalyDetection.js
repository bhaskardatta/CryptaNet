import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { 
  Typography, Grid, Card, CardContent, Table, TableBody, TableCell, 
  TableContainer, TableHead, TableRow, Button, Paper, FormControl, 
  InputLabel, Select, MenuItem, TextField, CircularProgress, Dialog, 
  DialogTitle, DialogContent, DialogActions, Snackbar, Alert, IconButton,
  Slider, Box, Chip, Avatar, Fade, Grow, LinearProgress, Tooltip
} from '@mui/material';
import { styled, alpha, useTheme } from '@mui/material/styles';
import { 
  Search, 
  InfoOutlined, 
  Warning, 
  Security, 
  Timeline, 
  FilterList,
  Refresh,
  TrendingUp,
  Assessment
} from '@mui/icons-material';
import { detectAnomalies, getAnomalyExplanation, clearError, clearSuccess, clearSelectedAnomaly } from '../store/slices/anomalySlice';
import { formatAnomalyScore } from '../utils/numberFormatting';
import { useTheme as useCustomTheme } from '../theme/ThemeContext';

const Root = styled('div')(({ theme }) => ({
  flexGrow: 1,
  minHeight: '100vh',
  background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.02)} 0%, ${alpha(theme.palette.secondary.main, 0.02)} 100%)`,
}));

const HeaderSection = styled(Box)(({ theme }) => ({
  background: `linear-gradient(135deg, ${theme.palette.error.main} 0%, ${theme.palette.error.dark} 100%)`,
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

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
  borderRadius: theme.spacing(2),
  boxShadow: theme.shadows[8],
  background: theme.palette.background.paper,
  border: `1px solid ${alpha(theme.palette.divider, 0.12)}`,
}));

const StyledFormControl = styled(FormControl)(({ theme }) => ({
  margin: theme.spacing(1),
  minWidth: 120,
  '& .MuiOutlinedInput-root': {
    borderRadius: theme.spacing(1),
  },
}));

const StyledSlider = styled(Slider)(({ theme }) => ({
  width: '100%',
  padding: theme.spacing(0, 2),
  '& .MuiSlider-thumb': {
    background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
    boxShadow: theme.shadows[4],
  },
  '& .MuiSlider-track': {
    background: `linear-gradient(90deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
  },
}));

const TableContainerStyled = styled(TableContainer)(({ theme }) => ({
  marginTop: theme.spacing(2),
  borderRadius: theme.spacing(2),
  boxShadow: theme.shadows[8],
  overflow: 'hidden',
  '& .MuiTableHead-root': {
    background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
    '& .MuiTableCell-root': {
      color: theme.palette.common.white,
      fontWeight: 600,
    },
  },
  '& .MuiTableRow-root:nth-of-type(even)': {
    backgroundColor: alpha(theme.palette.primary.main, 0.04),
  },
  '& .MuiTableRow-root:hover': {
    backgroundColor: alpha(theme.palette.primary.main, 0.08),
    transform: 'scale(1.01)',
    transition: 'all 0.2s ease',
  },
}));

const LoadingContainer = styled('div')(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  padding: theme.spacing(4),
}));

const AnomalyCard = styled(Card)(({ theme }) => ({
  background: `linear-gradient(135deg, ${alpha(theme.palette.error.main, 0.1)} 0%, ${alpha(theme.palette.error.dark, 0.05)} 100%)`,
  marginBottom: theme.spacing(2),
  borderRadius: theme.spacing(2),
  border: `1px solid ${alpha(theme.palette.error.main, 0.2)}`,
  boxShadow: theme.shadows[8],
}));

const ExplanationCard = styled(Card)(({ theme }) => ({
  marginTop: theme.spacing(2),
  borderRadius: theme.spacing(2),
  boxShadow: theme.shadows[8],
  background: theme.palette.background.paper,
  border: `1px solid ${alpha(theme.palette.divider, 0.12)}`,
}));

const FeatureImportanceContainer = styled('div')(({ theme }) => ({
  marginTop: theme.spacing(2),
}));

const FeatureBar = styled('div')(({ theme }) => ({
  height: 8,
  borderRadius: 4,
  marginTop: 5,
  marginBottom: 10,
  transition: 'all 0.3s ease',
  '&:hover': {
    height: 12,
    marginBottom: 8,
  },
}));

const StatChip = styled(Chip)(({ theme, severity }) => {
  const getColor = () => {
    switch (severity) {
      case 'high': return theme.palette.error.main;
      case 'medium': return theme.palette.warning.main;
      case 'low': return theme.palette.success.main;
      default: return theme.palette.info.main;
    }
  };
  
  return {
    background: `linear-gradient(135deg, ${getColor()} 0%, ${alpha(getColor(), 0.8)} 100%)`,
    color: theme.palette.common.white,
    fontWeight: 600,
    boxShadow: theme.shadows[4],
    '&:hover': {
      transform: 'scale(1.05)',
    },
  };
});

const AnomalyDetection = () => {
  const dispatch = useDispatch();
  const { anomalies, explanation, loading, error, success } = useSelector((state) => state.anomaly);
  const { user } = useSelector((state) => state.auth);
  const theme = useTheme();
  const { mode } = useCustomTheme();
  
  // Debug logging
  console.log('🚨 AnomalyDetection component state:', { 
    anomalies: anomalies?.length || 0, 
    anomaliesType: typeof anomalies,
    anomaliesIsArray: Array.isArray(anomalies),
    loading, 
    error, 
    success,
    firstAnomaly: anomalies?.[0] ? 'exists' : 'null'
  });
  
  // Log every time anomalies changes
  React.useEffect(() => {
    console.log('🚨 Anomalies changed:', { 
      count: anomalies?.length || 0, 
      type: typeof anomalies,
      isArray: Array.isArray(anomalies),
      content: anomalies 
    });
  }, [anomalies]);
  
  const [queryParams, setQueryParams] = useState({
    dataType: 'all',
    startTime: '',
    endTime: '',
    threshold: 0.5,
  });
  const [explanationOpen, setExplanationOpen] = useState(false);

  useEffect(() => {
    // Initial data fetch
    const fetchData = async () => {
      try {
        await dispatch(detectAnomalies({
          organizationId: user?.organization || 'Org1MSP',
          ...queryParams,
        }));
      } catch (error) {
        console.error('Error fetching anomaly data:', error);
      }
    };
    
    fetchData();
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
    console.log('🚨 Manual detect anomalies triggered');
    dispatch(detectAnomalies({
      organizationId: user?.organization || 'Org1MSP',
      ...queryParams,
    }));
  };

  const manualTestRedux = () => {
    console.log('🚨 Manual Redux test triggered');
    dispatch(detectAnomalies({
      organizationId: 'Org1MSP',
      dataType: 'all',
      startTime: '',
      endTime: '',
      threshold: 0.5,
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

  // Function to get severity based on anomaly score
  const getSeverity = (score) => {
    if (score >= 0.8) return 'high';
    if (score >= 0.6) return 'medium';
    if (score >= 0.4) return 'low';
    return 'info';
  };

  // Function to render feature importance bars
  const renderFeatureImportance = (features) => {
    if (!features || features.length === 0) return null;
    
    // Find the maximum importance value for scaling
    const maxImportance = Math.max(...features.map(f => Math.abs(f.importance)));
    
    return (
      <FeatureImportanceContainer>
        <Typography variant="h6" sx={{ mb: 2, display: 'flex', alignItems: 'center' }}>
          <Assessment sx={{ mr: 1, color: theme.palette.primary.main }} />
          Feature Importance Analysis
        </Typography>
        {features.map((feature, index) => {
          const importance = feature.importance;
          const width = `${Math.abs(importance) / maxImportance * 100}%`;
          const color = importance > 0 ? theme.palette.error.main : theme.palette.info.main;
          
          return (
            <Box key={index} sx={{ mb: 2 }}>
              <Grid container justifyContent="space-between" alignItems="center">
                <Grid item>
                  <Typography variant="body2" sx={{ fontWeight: 500 }}>
                    {feature.name}
                  </Typography>
                </Grid>
                <Grid item>
                  <Typography 
                    variant="body2" 
                    sx={{ 
                      fontWeight: 600,
                      color: importance > 0 ? theme.palette.error.main : theme.palette.info.main
                    }}
                  >
                    {importance > 0 ? '+' : ''}{importance.toFixed(4)}
                  </Typography>
                </Grid>
              </Grid>
              <FeatureBar 
                sx={{ 
                  width, 
                  backgroundColor: color,
                  background: `linear-gradient(90deg, ${color} 0%, ${alpha(color, 0.6)} 100%)`
                }}
              />
            </Box>
          );
        })}
      </FeatureImportanceContainer>
    );
  };

  return (
    <Root>
      {/* Header Section */}
      <HeaderSection>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography variant="h3" sx={{ fontWeight: 700, mb: 1 }}>
              Anomaly Detection
            </Typography>
            <Typography variant="h6" sx={{ opacity: 0.9, mb: 2 }}>
              AI-Powered Security Threat Detection
            </Typography>
            <Box display="flex" alignItems="center" gap={2}>
              <Chip 
                label={`${anomalies?.length || 0} Active Threats`}
                sx={{ 
                  bgcolor: alpha(theme.palette.common.white, 0.2),
                  color: 'white',
                  fontWeight: 500
                }}
              />
              <Chip 
                label="Real-time Monitoring"
                color="success"
                sx={{ fontWeight: 500 }}
              />
            </Box>
          </Box>
          <Avatar sx={{ width: 80, height: 80, bgcolor: alpha(theme.palette.common.white, 0.2) }}>
            <Warning sx={{ fontSize: 40 }} />
          </Avatar>
        </Box>
      </HeaderSection>

      {/* Detection Controls */}
      <StyledPaper>
        <Box display="flex" alignItems="center" sx={{ mb: 3 }}>
          <FilterList sx={{ color: theme.palette.primary.main, mr: 1 }} />
          <Typography variant="h6" sx={{ fontWeight: 600 }}>
            Detection Parameters
          </Typography>
        </Box>
        
        <form onSubmit={handleDetectAnomalies}>
          <Grid container spacing={3}>
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
                  <MenuItem value="all">All Data Types</MenuItem>
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
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 1,
                  },
                }}
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
                sx={{
                  '& .MuiOutlinedInput-root': {
                    borderRadius: 1,
                  },
                }}
              />
            </Grid>
            
            <Grid item xs={12} sm={6} md={3}>
              <Box sx={{ px: 2 }}>
                <Typography variant="subtitle2" gutterBottom sx={{ fontWeight: 600 }}>
                  Sensitivity Threshold: {queryParams.threshold}
                </Typography>
                <StyledSlider
                  value={queryParams.threshold}
                  onChange={handleThresholdChange}
                  aria-labelledby="threshold-slider"
                  valueLabelDisplay="auto"
                  step={0.05}
                  marks={[
                    { value: 0, label: 'Low' },
                    { value: 0.5, label: 'Medium' },
                    { value: 1, label: 'High' }
                  ]}
                  min={0}
                  max={1}
                />
              </Box>
            </Grid>
            
            <Grid item xs={12}>
              <Box display="flex" gap={2}>
                <Button
                  type="submit"
                  variant="contained"
                  size="large"
                  startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <Search />}
                  disabled={loading}
                  sx={{
                    borderRadius: 2,
                    px: 4,
                    py: 1.5,
                    background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
                    boxShadow: theme.shadows[8],
                    '&:hover': {
                      transform: 'translateY(-2px)',
                      boxShadow: theme.shadows[12],
                    },
                  }}
                >
                  {loading ? 'Scanning...' : 'Detect Anomalies'}
                </Button>
                
                <Button
                  variant="outlined"
                  size="large"
                  startIcon={<Refresh />}
                  onClick={() => window.location.reload()}
                  sx={{
                    borderRadius: 2,
                    px: 3,
                  }}
                >
                  Reset
                </Button>
              </Box>
            </Grid>
          </Grid>
        </form>
      </StyledPaper>

      {/* Error and Success Messages */}
      {error && (
        <Fade in>
          <Alert 
            severity="error" 
            sx={{ 
              marginBottom: 2, 
              borderRadius: 2,
              boxShadow: theme.shadows[4]
            }}
          >
            {error}
          </Alert>
        </Fade>
      )}

      {success && (
        <Fade in>
          <Alert 
            severity="success" 
            sx={{ 
              marginBottom: 2, 
              borderRadius: 2,
              boxShadow: theme.shadows[4]
            }}
          >
            {success}
          </Alert>
        </Fade>
      )}

      {/* Results Section */}
      {loading ? (
        <StyledPaper>
          <LoadingContainer>
            <Box textAlign="center">
              <CircularProgress size={60} thickness={4} />
              <Typography variant="h6" sx={{ mt: 2, color: theme.palette.text.secondary }}>
                Analyzing Data for Anomalies...
              </Typography>
              <Typography variant="body2" color="textSecondary">
                This may take a few moments
              </Typography>
            </Box>
          </LoadingContainer>
        </StyledPaper>
      ) : (
        <>
          {anomalies && anomalies.length > 0 ? (
            <Fade in timeout={600}>
              <Box>
                <Box display="flex" alignItems="center" justifyContent="between" sx={{ mb: 3 }}>
                  <Box display="flex" alignItems="center">
                    <Timeline sx={{ color: theme.palette.primary.main, mr: 1 }} />
                    <Typography variant="h5" sx={{ fontWeight: 600 }}>
                      Detected Anomalies
                    </Typography>
                    <StatChip 
                      label={`${anomalies.length} Found`}
                      severity={anomalies.length > 10 ? 'high' : anomalies.length > 5 ? 'medium' : 'low'}
                      sx={{ ml: 2 }}
                    />
                  </Box>
                </Box>
                
                <TableContainerStyled component={Paper}>
                  <Table>
                    <TableHead>
                      <TableRow>
                        <TableCell>Threat ID</TableCell>
                        <TableCell>Product ID</TableCell>
                        <TableCell>Data Type</TableCell>
                        <TableCell>Timestamp</TableCell>
                        <TableCell>Severity</TableCell>
                        <TableCell>Risk Score</TableCell>
                        <TableCell>Actions</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {anomalies.map((anomaly, index) => {
                        const severity = getSeverity(anomaly.anomalyScore);
                        return (
                          <Grow in timeout={300 + index * 100} key={anomaly.id}>
                            <TableRow>
                              <TableCell sx={{ fontWeight: 600 }}>
                                {anomaly.id}
                              </TableCell>
                              <TableCell>{anomaly.productId}</TableCell>
                              <TableCell>
                                <Chip 
                                  label={anomaly.dataType} 
                                  size="small" 
                                  variant="outlined"
                                  sx={{ fontWeight: 500 }}
                                />
                              </TableCell>
                              <TableCell>
                                {new Date(anomaly.timestamp).toLocaleString()}
                              </TableCell>
                              <TableCell>
                                <StatChip 
                                  label={severity.toUpperCase()} 
                                  severity={severity}
                                  size="small"
                                />
                              </TableCell>
                              <TableCell>
                                <Box display="flex" alignItems="center" gap={1}>
                                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                                    {formatAnomalyScore(anomaly.anomalyScore)}
                                  </Typography>
                                  <LinearProgress
                                    variant="determinate"
                                    value={anomaly.anomalyScore * 100}
                                    sx={{
                                      width: 60,
                                      height: 6,
                                      borderRadius: 3,
                                      '& .MuiLinearProgress-bar': {
                                        backgroundColor: severity === 'high' ? theme.palette.error.main :
                                                        severity === 'medium' ? theme.palette.warning.main :
                                                        theme.palette.success.main
                                      }
                                    }}
                                  />
                                </Box>
                              </TableCell>
                              <TableCell>
                                <Tooltip title="View Detailed Analysis">
                                  <IconButton 
                                    onClick={() => handleViewExplanation(anomaly.id)}
                                    sx={{
                                      color: theme.palette.primary.main,
                                      '&:hover': {
                                        backgroundColor: alpha(theme.palette.primary.main, 0.1),
                                        transform: 'scale(1.1)',
                                      },
                                    }}
                                  >
                                    <InfoOutlined />
                                  </IconButton>
                                </Tooltip>
                              </TableCell>
                            </TableRow>
                          </Grow>
                        );
                      })}
                    </TableBody>
                  </Table>
                </TableContainerStyled>
              </Box>
            </Fade>
          ) : (
            anomalies && (
              <Fade in timeout={400}>
                <StyledPaper>
                  <Box textAlign="center" py={4}>
                    <Security sx={{ fontSize: 80, color: theme.palette.success.main, mb: 2 }} />
                    <Typography variant="h5" sx={{ fontWeight: 600, mb: 1 }}>
                      No Threats Detected
                    </Typography>
                    <Typography variant="body1" color="textSecondary">
                      Your system appears secure with the current threshold settings.
                    </Typography>
                    <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                      Try adjusting the sensitivity threshold to detect more subtle anomalies.
                    </Typography>
                  </Box>
                </StyledPaper>
              </Fade>
            )
          )}
        </>
      )}

      {/* Explanation Dialog */}
      <Dialog 
        open={explanationOpen} 
        onClose={handleCloseExplanation} 
        maxWidth="md" 
        fullWidth
        PaperProps={{
          sx: {
            borderRadius: 2,
            boxShadow: theme.shadows[16],
          }
        }}
      >
        <DialogTitle sx={{ 
          background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
          color: 'white',
          fontWeight: 600
        }}>
          <Box display="flex" alignItems="center">
            <Assessment sx={{ mr: 1 }} />
            Anomaly Analysis Report
          </Box>
        </DialogTitle>
        <DialogContent sx={{ p: 3 }}>
          {loading ? (
            <LoadingContainer>
              <CircularProgress />
            </LoadingContainer>
          ) : explanation ? (
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <AnomalyCard>
                  <CardContent>
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                      Threat Details
                    </Typography>
                    <Grid container spacing={2}>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="subtitle2" color="textSecondary">Threat ID:</Typography>
                        <Typography variant="body1" sx={{ fontWeight: 600 }}>
                          {explanation.anomalyId}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="subtitle2" color="textSecondary">Product ID:</Typography>
                        <Typography variant="body1" sx={{ fontWeight: 600 }}>
                          {explanation.productId}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="subtitle2" color="textSecondary">Data Type:</Typography>
                        <Chip 
                          label={explanation.dataType} 
                          size="small" 
                          color="primary"
                          sx={{ fontWeight: 500 }}
                        />
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="subtitle2" color="textSecondary">Timestamp:</Typography>
                        <Typography variant="body1" sx={{ fontWeight: 600 }}>
                          {new Date(explanation.timestamp).toLocaleString()}
                        </Typography>
                      </Grid>
                      <Grid item xs={12} sm={6}>
                        <Typography variant="subtitle2" color="textSecondary">Risk Score:</Typography>
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="body1" sx={{ fontWeight: 600 }}>
                            {formatAnomalyScore(explanation.anomalyScore)}
                          </Typography>
                          <StatChip 
                            label={getSeverity(explanation.anomalyScore).toUpperCase()} 
                            severity={getSeverity(explanation.anomalyScore)}
                            size="small"
                          />
                        </Box>
                      </Grid>
                    </Grid>
                  </CardContent>
                </AnomalyCard>
              </Grid>
              
              <Grid item xs={12}>
                <ExplanationCard>
                  <CardContent>
                    <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
                      Analysis Summary
                    </Typography>
                    <Typography variant="body1" paragraph sx={{ lineHeight: 1.6 }}>
                      {explanation.summary}
                    </Typography>
                    
                    {renderFeatureImportance(explanation.featureImportance)}
                    
                    <Box sx={{ mt: 3, p: 2, bgcolor: alpha(theme.palette.info.main, 0.05), borderRadius: 2 }}>
                      <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 1, display: 'flex', alignItems: 'center' }}>
                        <Security sx={{ mr: 1, color: theme.palette.info.main }} />
                        Blockchain Verification
                      </Typography>
                      <Grid container spacing={2}>
                        <Grid item xs={12} sm={4}>
                          <Typography variant="body2" color="textSecondary">Transaction ID:</Typography>
                          <Typography variant="body2" sx={{ fontFamily: 'monospace', fontWeight: 500 }}>
                            {explanation.transactionId || 'N/A'}
                          </Typography>
                        </Grid>
                        <Grid item xs={12} sm={4}>
                          <Typography variant="body2" color="textSecondary">Block Number:</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 500 }}>
                            {explanation.blockNumber || 'N/A'}
                          </Typography>
                        </Grid>
                        <Grid item xs={12} sm={4}>
                          <Typography variant="body2" color="textSecondary">Block Timestamp:</Typography>
                          <Typography variant="body2" sx={{ fontWeight: 500 }}>
                            {explanation.blockTimestamp ? new Date(explanation.blockTimestamp).toLocaleString() : 'N/A'}
                          </Typography>
                        </Grid>
                      </Grid>
                    </Box>
                  </CardContent>
                </ExplanationCard>
              </Grid>
            </Grid>
          ) : (
            <Box textAlign="center" py={4}>
              <Typography variant="body1" color="textSecondary">
                No detailed analysis available for this anomaly.
              </Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions sx={{ p: 3 }}>
          <Button 
            onClick={handleCloseExplanation} 
            variant="contained"
            sx={{ borderRadius: 2, px: 3 }}
          >
            Close Report
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar open={!!error || success} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert 
          onClose={handleCloseSnackbar} 
          severity={error ? 'error' : 'success'}
          sx={{ borderRadius: 2 }}
        >
          {error || 'Operation completed successfully'}
        </Alert>
      </Snackbar>
    </Root>
  );
};

export default AnomalyDetection;