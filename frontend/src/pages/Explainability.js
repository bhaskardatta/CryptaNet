import React, { useState, useEffect, useCallback } from 'react';
import { useSelector } from 'react-redux';
import { styled } from '@mui/material/styles';
import { 
  Paper, Typography, Grid, Button, TextField, CircularProgress, Card, CardContent, 
  Divider, Alert, Box, Chip, LinearProgress, Avatar, Fade, Grow, Tooltip
} from '@mui/material';
import { 
  Psychology, Science, Analytics, Timeline, VerifiedUser, TrendingUp, 
  Assignment, Security, Speed, Memory, Assessment, BugReport, Insights
} from '@mui/icons-material';
import { anomalyService } from '../services/anomalyService';
import { formatAnomalyScore } from '../utils/numberFormatting';

const Root = styled('div')(({ theme }) => ({
  flexGrow: 1,
  background: theme.palette.mode === 'dark' 
    ? 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)'
    : 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%)',
  minHeight: '100vh',
  padding: theme.spacing(3),
}));

const HeaderSection = styled(Card)(({ theme }) => ({
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)'
    : 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%)',
  backdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
  borderRadius: theme.spacing(2),
  marginBottom: theme.spacing(3),
  padding: theme.spacing(3),
  boxShadow: theme.palette.mode === 'dark'
    ? '0 8px 32px rgba(0,0,0,0.3)'
    : '0 8px 32px rgba(0,0,0,0.1)',
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)'
    : 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%)',
  backdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
  borderRadius: theme.spacing(2),
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
  boxShadow: theme.palette.mode === 'dark'
    ? '0 8px 32px rgba(0,0,0,0.3)'
    : '0 8px 32px rgba(0,0,0,0.1)',
}));

const StyledCard = styled(Card)(({ theme }) => ({
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)'
    : 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%)',
  backdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
  borderRadius: theme.spacing(2),
  marginBottom: theme.spacing(3),
  boxShadow: theme.palette.mode === 'dark'
    ? '0 8px 32px rgba(0,0,0,0.3)'
    : '0 8px 32px rgba(0,0,0,0.1)',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.palette.mode === 'dark'
      ? '0 12px 40px rgba(0,0,0,0.4)'
      : '0 12px 40px rgba(0,0,0,0.15)',
  },
}));

const GradientButton = styled(Button)(({ theme }) => ({
  background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
  borderRadius: theme.spacing(1),
  border: 0,
  color: 'white',
  height: 48,
  padding: '0 30px',
  boxShadow: '0 3px 5px 2px rgba(102, 126, 234, .3)',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    background: 'linear-gradient(45deg, #764ba2 30%, #667eea 90%)',
    transform: 'translateY(-2px)',
    boxShadow: '0 6px 20px 2px rgba(102, 126, 234, .4)',
  },
  '&:disabled': {
    background: 'linear-gradient(45deg, #ccc 30%, #999 90%)',
    transform: 'none',
    boxShadow: 'none',
  },
}));

const ModernTextField = styled(TextField)(({ theme }) => ({
  '& .MuiOutlinedInput-root': {
    borderRadius: theme.spacing(1),
    background: theme.palette.mode === 'dark'
      ? 'rgba(255,255,255,0.05)'
      : 'rgba(255,255,255,0.7)',
    backdropFilter: 'blur(10px)',
    transition: 'all 0.3s ease-in-out',
    '&:hover': {
      background: theme.palette.mode === 'dark'
        ? 'rgba(255,255,255,0.08)'
        : 'rgba(255,255,255,0.9)',
    },
    '&.Mui-focused': {
      background: theme.palette.mode === 'dark'
        ? 'rgba(255,255,255,0.1)'
        : 'rgba(255,255,255,1)',
    },
  },
}));

const MetricCard = styled(Card)(({ theme }) => ({
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)'
    : 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%)',
  backdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
  borderRadius: theme.spacing(2),
  padding: theme.spacing(2),
  height: '100%',
  transition: 'all 0.3s ease-in-out',
  cursor: 'pointer',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.palette.mode === 'dark'
      ? '0 12px 40px rgba(0,0,0,0.4)'
      : '0 12px 40px rgba(0,0,0,0.15)',
  },
}));

const StyledDivider = styled(Divider)(({ theme }) => ({
  margin: theme.spacing(3, 0),
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent)'
    : 'linear-gradient(90deg, transparent, rgba(0,0,0,0.1), transparent)',
  height: 2,
}));

const Explainability = () => {
  const { user } = useSelector((state) => state.auth);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modelMetrics, setModelMetrics] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [anomalyId, setAnomalyId] = useState('');

  const fetchModelMetrics = useCallback(async () => {
    try {
      setLoading(true);
      const response = await anomalyService.getModelMetrics(user?.organizationId || 'org1');
      setModelMetrics(response);
      setLoading(false);
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to fetch model metrics');
      setLoading(false);
    }
  }, [user?.organizationId]);

  useEffect(() => {
    // Fetch model metrics when component mounts
    fetchModelMetrics();
  }, [fetchModelMetrics]);

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
      <Box sx={{ mt: 4 }}>
        <Box display="flex" alignItems="center" mb={2}>
          <TrendingUp sx={{ color: 'primary.main', mr: 1 }} />
          <Typography variant="h6" fontWeight="bold">
            Feature Importance Analysis
          </Typography>
        </Box>
        <Typography variant="body2" color="text.secondary" paragraph>
          Features that contributed to the anomaly detection are shown below. Positive values (red) indicate features that increased the anomaly score, while negative values (blue) indicate features that decreased it.
        </Typography>
        
        <Box sx={{ 
          bgcolor: 'action.hover', 
          borderRadius: 2, 
          p: 3,
          border: '1px solid',
          borderColor: 'divider'
        }}>
          {features.map((feature, index) => {
            const importance = feature.importance || 0;
            const width = `${Math.abs(importance) / (maxImportance || 1) * 100}%`;
            const color = importance > 0 ? '#f44336' : '#2196f3';
            const isPositive = importance > 0;
            
            return (
              <Fade in timeout={500 + index * 100} key={index}>
                <Box sx={{ mb: 3, '&:last-child': { mb: 0 } }}>
                  <Box display="flex" justifyContent="space-between" alignItems="center" mb={1}>
                    <Box display="flex" alignItems="center">
                      <Chip
                        label={feature.name || 'Unknown Feature'}
                        size="small"
                        sx={{ 
                          mr: 2,
                          bgcolor: isPositive ? 'error.light' : 'info.light',
                          color: isPositive ? 'error.contrastText' : 'info.contrastText'
                        }}
                      />
                    </Box>
                    <Tooltip title={`Impact: ${isPositive ? 'Increases' : 'Decreases'} anomaly score`}>
                      <Chip
                        label={typeof importance === 'number' ? importance.toFixed(4) : 'N/A'}
                        size="small"
                        variant="outlined"
                        sx={{ 
                          fontFamily: 'monospace',
                          borderColor: color
                        }}
                      />
                    </Tooltip>
                  </Box>
                  <Box sx={{ position: 'relative', height: 8, bgcolor: 'grey.200', borderRadius: 4, overflow: 'hidden' }}>
                    <Box
                      sx={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        height: '100%',
                        width: width,
                        backgroundColor: color,
                        borderRadius: 4,
                        transition: 'width 0.6s ease-in-out',
                        background: isPositive 
                          ? 'linear-gradient(90deg, #f44336, #ff7961)'
                          : 'linear-gradient(90deg, #2196f3, #64b5f6)'
                      }}
                    />
                  </Box>
                </Box>
              </Fade>
            );
          })}
        </Box>
      </Box>
    );
  };

  // Function to render blockchain verification information
  const renderBlockchainVerification = (data) => {
    if (!data || !data.verification) {
      return (
        <Box sx={{ mt: 4 }}>
          <Box display="flex" alignItems="center" mb={2}>
            <Security sx={{ color: 'warning.main', mr: 1 }} />
            <Typography variant="h6" fontWeight="bold">
              Blockchain Verification
            </Typography>
          </Box>
          <Alert severity="warning" sx={{ borderRadius: 2 }}>
            Verification data unavailable for this anomaly
          </Alert>
        </Box>
      );
    }

    const verification = data.verification;
    const consensusPercentage = verification.consensus != null && typeof verification.consensus === 'number' 
      ? (verification.consensus * 100).toFixed(2) 
      : 'N/A';
    
    return (
      <Box sx={{ mt: 4 }}>
        <Box display="flex" alignItems="center" mb={2}>
          <Security sx={{ color: 'success.main', mr: 1 }} />
          <Typography variant="h6" fontWeight="bold">
            🔐 Blockchain Verification
          </Typography>
        </Box>
        
        <Grid container spacing={3}>
          <Grid item xs={12} sm={6}>
            <Box sx={{ 
              p: 2, 
              borderRadius: 2, 
              bgcolor: 'success.light', 
              color: 'success.contrastText',
              textAlign: 'center'
            }}>
              <VerifiedUser sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h6" fontWeight="bold">
                {verification.status || 'Unknown'}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Verification Status
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Box sx={{ 
              p: 2, 
              borderRadius: 2, 
              bgcolor: 'info.light', 
              color: 'info.contrastText',
              textAlign: 'center'
            }}>
              <Assessment sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h6" fontWeight="bold">
                {consensusPercentage !== 'N/A' ? `${consensusPercentage}%` : 'N/A'}
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                Network Consensus
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12}>
            <Box sx={{ 
              p: 3, 
              borderRadius: 2, 
              bgcolor: 'action.hover',
              border: '1px solid',
              borderColor: 'divider'
            }}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Block Height
                  </Typography>
                  <Typography variant="body1" fontWeight="medium" sx={{ fontFamily: 'monospace' }}>
                    #{verification.blockHeight || 'Unknown'}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Transaction ID
                  </Typography>
                  <Tooltip title={verification.txId || 'Unknown'}>
                    <Typography 
                      variant="body1" 
                      fontWeight="medium" 
                      sx={{ 
                        fontFamily: 'monospace',
                        cursor: 'pointer',
                        '&:hover': { color: 'primary.main' }
                      }}
                    >
                      {verification.txId ? `${verification.txId.substring(0, 16)}...` : 'Unknown'}
                    </Typography>
                  </Tooltip>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Timestamp
                  </Typography>
                  <Typography variant="body1" fontWeight="medium">
                    {verification.timestamp ? new Date(verification.timestamp).toLocaleString() : 'Unknown'}
                  </Typography>
                </Grid>
                <Grid item xs={12} sm={6}>
                  <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                    Block Hash
                  </Typography>
                  <Tooltip title={verification.hash || 'Unknown'}>
                    <Typography 
                      variant="body1" 
                      fontWeight="medium" 
                      sx={{ 
                        fontFamily: 'monospace',
                        cursor: 'pointer',
                        '&:hover': { color: 'primary.main' }
                      }}
                    >
                      {verification.hash ? `${verification.hash.substring(0, 16)}...` : 'Unknown'}
                    </Typography>
                  </Tooltip>
                </Grid>
              </Grid>
            </Box>
          </Grid>
        </Grid>
      </Box>
    );
  };

  return (
    <Root>
      <Fade in timeout={800}>
        <HeaderSection>
          <Box display="flex" alignItems="center" mb={2}>
            <Avatar sx={{ 
              bgcolor: 'primary.main', 
              mr: 2, 
              width: 56, 
              height: 56,
              background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)'
            }}>
              <Psychology fontSize="large" />
            </Avatar>
            <Box>
              <Typography variant="h4" component="h1" fontWeight="bold" color="primary">
                AI Model Explainability
              </Typography>
              <Typography variant="subtitle1" color="text.secondary">
                Understand and interpret AI-driven anomaly detection results
              </Typography>
            </Box>
          </Box>
          
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard>
                <Box display="flex" alignItems="center">
                  <Analytics sx={{ color: '#667eea', mr: 2 }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {modelMetrics?.totalExplanations || '0'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Total Explanations
                    </Typography>
                  </Box>
                </Box>
              </MetricCard>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard>
                <Box display="flex" alignItems="center">
                  <TrendingUp sx={{ color: '#764ba2', mr: 2 }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {modelMetrics?.accuracy ? `${(modelMetrics.accuracy * 100).toFixed(1)}%` : 'N/A'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Model Accuracy
                    </Typography>
                  </Box>
                </Box>
              </MetricCard>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard>
                <Box display="flex" alignItems="center">
                  <Speed sx={{ color: '#f44336', mr: 2 }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {modelMetrics?.avgResponseTime || '< 1s'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Avg Response Time
                    </Typography>
                  </Box>
                </Box>
              </MetricCard>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard>
                <Box display="flex" alignItems="center">
                  <VerifiedUser sx={{ color: '#2196f3', mr: 2 }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {modelMetrics?.trustScore ? `${(modelMetrics.trustScore * 100).toFixed(0)}%` : '95%'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Trust Score
                    </Typography>
                  </Box>
                </Box>
              </MetricCard>
            </Grid>
          </Grid>
        </HeaderSection>
      </Fade>

      <Grow in timeout={1000}>
        <StyledPaper>
          <Box display="flex" alignItems="center" mb={3}>
            <Assignment sx={{ color: 'primary.main', mr: 2 }} />
            <Typography variant="h6" fontWeight="bold">
              Explain Anomaly Detection Results
            </Typography>
          </Box>
          
          <Grid container spacing={3}>
            <Grid item xs={12} sm={8}>
              <ModernTextField
                fullWidth
                id="anomalyId"
                name="anomalyId"
                label="🔍 Anomaly ID"
                value={anomalyId}
                onChange={handleAnomalyIdChange}
                variant="outlined"
                placeholder="Enter the ID of the anomaly to explain"
                helperText="Enter a valid anomaly ID to get detailed explanation"
              />
            </Grid>
            <Grid item xs={12} sm={4}>
              <GradientButton
                onClick={handleExplainAnomaly}
                disabled={loading || !anomalyId}
                fullWidth
                sx={{ height: 56 }}
                startIcon={loading ? <CircularProgress size={20} color="inherit" /> : <Science />}
              >
                {loading ? 'Analyzing...' : 'Explain Anomaly'}
              </GradientButton>
            </Grid>
          </Grid>
        </StyledPaper>
      </Grow>

      {error && (
        <Fade in>
          <Alert 
            severity="error" 
            sx={{ 
              mb: 3,
              borderRadius: 2,
              backdropFilter: 'blur(10px)',
            }}
            icon={<BugReport />}
          >
            {error}
          </Alert>
        </Fade>
      )}

      {loading && !explanation && (
        <Fade in>
          <StyledCard>
            <Box 
              display="flex" 
              flexDirection="column" 
              alignItems="center" 
              justifyContent="center" 
              py={6}
            >
              <CircularProgress size={60} sx={{ mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                Analyzing anomaly data...
              </Typography>
              <Typography variant="body2" color="text.secondary" textAlign="center" sx={{ mt: 1 }}>
                Our AI is processing the anomaly to provide detailed explanations
              </Typography>
            </Box>
          </StyledCard>
        </Fade>
      )}

      {explanation && (
        <Fade in timeout={1200}>
          <StyledCard>
            <CardContent sx={{ p: 4 }}>
              <Box display="flex" alignItems="center" mb={3}>
                <Insights sx={{ color: 'primary.main', mr: 2 }} />
                <Typography variant="h5" fontWeight="bold">
                  Anomaly Explanation Report
                </Typography>
              </Box>
              
              <Grid container spacing={3} sx={{ mb: 4 }}>
                <Grid item xs={12} sm={6} md={4}>
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Anomaly ID
                    </Typography>
                    <Chip 
                      label={explanation.anomalyId} 
                      color="primary" 
                      variant="outlined"
                      sx={{ fontFamily: 'monospace' }}
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Product ID
                    </Typography>
                    <Chip 
                      label={explanation.productId} 
                      color="secondary" 
                      variant="outlined"
                      sx={{ fontFamily: 'monospace' }}
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Data Type
                    </Typography>
                    <Chip 
                      label={explanation.dataType} 
                      sx={{ 
                        background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                        color: 'white'
                      }}
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Timestamp
                    </Typography>
                    <Typography variant="body1" fontWeight="medium">
                      {new Date(explanation.timestamp).toLocaleString()}
                    </Typography>
                  </Box>
                </Grid>
                <Grid item xs={12} sm={6} md={4}>
                  <Box>
                    <Typography variant="subtitle2" color="text.secondary" gutterBottom>
                      Anomaly Score
                    </Typography>
                    <Box display="flex" alignItems="center">
                      <Typography variant="h6" fontWeight="bold" color="error.main">
                        {formatAnomalyScore(explanation.anomalyScore)}
                      </Typography>
                      <LinearProgress 
                        variant="determinate" 
                        value={explanation.anomalyScore * 100} 
                        sx={{ ml: 2, flex: 1, height: 8, borderRadius: 4 }}
                        color="error"
                      />
                    </Box>
                  </Box>
                </Grid>
              </Grid>

              <StyledDivider />

              <Box mb={4}>
                <Typography variant="h6" gutterBottom fontWeight="bold">
                  📋 Summary Analysis
                </Typography>
                <Typography variant="body1" sx={{ 
                  p: 2, 
                  borderLeft: '4px solid',
                  borderColor: 'primary.main',
                  bgcolor: 'action.hover',
                  borderRadius: 1
                }}>
                  {explanation.summary}
                </Typography>
              </Box>

              {renderFeatureImportance(explanation.featureImportance)}

              <StyledDivider />

              {renderBlockchainVerification(explanation)}
            </CardContent>
          </StyledCard>
        </Fade>
      )}

      {modelMetrics && (
        <Fade in timeout={1400}>
          <StyledCard>
            <CardContent sx={{ p: 4 }}>
              <Box display="flex" alignItems="center" mb={3}>
                <Assessment sx={{ color: 'primary.main', mr: 2 }} />
                <Typography variant="h5" fontWeight="bold">
                  Model Performance Metrics
                </Typography>
              </Box>
              
              <Grid container spacing={4}>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Memory sx={{ fontSize: 48, color: '#667eea', mb: 1 }} />
                    <Typography variant="h4" fontWeight="bold" color="primary">
                      {(modelMetrics.precision || 0).toFixed(3)}
                    </Typography>
                    <Typography variant="subtitle1" color="text.secondary">
                      Precision
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={(modelMetrics.precision || 0) * 100} 
                      sx={{ mt: 1, height: 6, borderRadius: 3 }}
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <Timeline sx={{ fontSize: 48, color: '#764ba2', mb: 1 }} />
                    <Typography variant="h4" fontWeight="bold" color="secondary">
                      {(modelMetrics.recall || 0).toFixed(3)}
                    </Typography>
                    <Typography variant="subtitle1" color="text.secondary">
                      Recall
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={(modelMetrics.recall || 0) * 100} 
                      sx={{ mt: 1, height: 6, borderRadius: 3 }}
                      color="secondary"
                    />
                  </Box>
                </Grid>
                <Grid item xs={12} sm={4}>
                  <Box textAlign="center">
                    <TrendingUp sx={{ fontSize: 48, color: '#f44336', mb: 1 }} />
                    <Typography variant="h4" fontWeight="bold" sx={{ color: '#f44336' }}>
                      {(modelMetrics.f1Score || 0).toFixed(3)}
                    </Typography>
                    <Typography variant="subtitle1" color="text.secondary">
                      F1 Score
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={(modelMetrics.f1Score || 0) * 100} 
                      sx={{ 
                        mt: 1, 
                        height: 6, 
                        borderRadius: 3,
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: '#f44336'
                        }
                      }}
                    />
                  </Box>
                </Grid>
                <Grid item xs={12}>
                  <Box sx={{ 
                    p: 3, 
                    borderRadius: 2, 
                    bgcolor: 'action.hover',
                    border: '1px solid',
                    borderColor: 'divider'
                  }}>
                    <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                      🤖 Model Description
                    </Typography>
                    <Typography variant="body1">
                      {modelMetrics.modelDescription || 'Advanced AI model for supply chain anomaly detection using ensemble methods and deep learning techniques.'}
                    </Typography>
                  </Box>
                </Grid>
              </Grid>
            </CardContent>
          </StyledCard>
        </Fade>
      )}
    </Root>
  );
};

export default Explainability;