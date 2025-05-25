import React, { useState, useEffect, useCallback } from 'react';
import { useSelector } from 'react-redux';
import { styled } from '@mui/material/styles';
import { Paper, Typography, Grid, Button, TextField, CircularProgress, Card, CardContent, Divider, Alert } from '@mui/material';
import { anomalyService } from '../services/anomalyService';

const Root = styled('div')(({ theme }) => ({
  flexGrow: 1,
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(2),
  marginBottom: theme.spacing(2),
}));

const LoadingContainer = styled('div')(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  padding: theme.spacing(4),
}));

const StyledCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(2),
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

const StyledDivider = styled(Divider)(({ theme }) => ({
  margin: theme.spacing(2, 0),
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
      <FeatureImportanceContainer>
        <Typography variant="h6">Feature Importance</Typography>
        <Typography variant="body2" paragraph>
          Features that contributed to the anomaly detection are shown below. Positive values (red) indicate features that increased the anomaly score, while negative values (blue) indicate features that decreased it.
        </Typography>
        {features.map((feature, index) => {
          const importance = feature.importance || 0;
          const width = `${Math.abs(importance) / maxImportance * 100}%`;
          const color = importance > 0 ? '#f44336' : '#2196f3'; // Red for positive, blue for negative
          
          return (
            <div key={index}>
              <Grid container justifyContent="space-between">
                <Grid item>
                  <Typography variant="body2">{feature.name || 'Unknown Feature'}</Typography>
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

  // Function to render blockchain verification information
  const renderBlockchainVerification = (data) => {
    if (!data || !data.verification) {
      return <Typography>Verification data unavailable</Typography>;
    }

    const verification = data.verification;
    
    return (
      <div>
        <Typography variant="h6" gutterBottom>Blockchain Verification</Typography>
        <Typography variant="body1">
          <strong>Status:</strong> {verification.status || 'Unknown'}
        </Typography>
        <Typography variant="body1">
          <strong>Consensus:</strong> {verification.consensus != null ? `${(verification.consensus * 100).toFixed(2)}%` : 'N/A'}
        </Typography>
        <Typography variant="body1">
          <strong>Block Height:</strong> {verification.blockHeight || 'Unknown'}
        </Typography>
        <Typography variant="body1">
          <strong>Transaction ID:</strong> {verification.txId || 'Unknown'}
        </Typography>
        <Typography variant="body1">
          <strong>Timestamp:</strong> {verification.timestamp ? new Date(verification.timestamp).toLocaleString() : 'Unknown'}
        </Typography>
        <Typography variant="body1">
          <strong>Hash:</strong> {verification.hash ? verification.hash.substring(0, 16) + '...' : 'Unknown'}
        </Typography>
      </div>
    );
  };

  return (
    <Root>
      <Typography variant="h4" gutterBottom>
        Explainability
      </Typography>

      <StyledPaper>
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
              sx={{ height: '100%' }}
            >
              {loading ? <CircularProgress size={24} /> : 'Explain'}
            </Button>
          </Grid>
        </Grid>
      </StyledPaper>

      {error && (
        <Alert severity="error" sx={{ marginBottom: 2 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <LoadingContainer>
          <CircularProgress />
        </LoadingContainer>
      ) : explanation ? (
        <>
          <StyledCard>
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

              <StyledDivider />

              <Typography variant="h6">Summary</Typography>
              <Typography variant="body1" paragraph>
                {explanation.summary}
              </Typography>

              {renderFeatureImportance(explanation.featureImportance)}

              {renderBlockchainVerification(explanation)}
            </CardContent>
          </StyledCard>

          {modelMetrics && (
            <StyledCard>
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
            </StyledCard>
          )}
        </>
      ) : null}
    </Root>
  );
};

export default Explainability;