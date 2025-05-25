import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { Grid, Typography, CircularProgress, Card, CardContent } from '@mui/material';
import { styled } from '@mui/material/styles';
import ListIcon from '@mui/icons-material/List';
import WarningIcon from '@mui/icons-material/Warning';
import UpdateIcon from '@mui/icons-material/Update';
import axios from 'axios';
import { API_URL } from '../config';
import { fetchSupplyChainData } from '../store/slices/supplyChainSlice';

// Styled components
const Root = styled('div')(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
}));

const StyledCard = styled(Card)(({ theme }) => ({
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
}));

const StyledCardContent = styled(CardContent)({
  flexGrow: 1,
});

const StatValue = styled(Typography)(({ theme }) => ({
  fontSize: '2.5rem',
  fontWeight: 'bold',
  marginTop: theme.spacing(1),
  marginBottom: theme.spacing(1),
}));

const Dashboard = () => {
  const dispatch = useDispatch();
  const [analyticsData, setAnalyticsData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdated, setLastUpdated] = useState(new Date());

  const fetchAnalyticsData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`${API_URL}/api/analytics/comprehensive`, {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      });
      
      if (response.data) {
        setAnalyticsData(response.data);
        setLastUpdated(new Date());
      }
      setLoading(false);
    } catch (err) {
      console.error('Error fetching analytics:', err);
      setError(err.message);
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalyticsData();
    // Fetch data every 30 seconds
    const intervalId = setInterval(fetchAnalyticsData, 30000);
    return () => clearInterval(intervalId);
  }, []);

  if (loading && !analyticsData) {
    return (
      <Root>
        <Typography variant="h4" gutterBottom>Dashboard</Typography>
        <CircularProgress />
      </Root>
    );
  }

  const analytics = analyticsData?.analytics || {};
  const totalRecords = analytics.total_records || 0;
  const anomalies = analytics.anomaly_detection?.anomalies || [];
  const anomalyCount = anomalies.length || 0;

  return (
    <Root>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Grid container spacing={3}>
        {/* Total Records Card */}
        <Grid item xs={12} md={4}>
          <StyledCard>
            <StyledCardContent>
              <Typography variant="h6" color="textSecondary" gutterBottom>
                <ListIcon fontSize="small" style={{ verticalAlign: 'middle', marginRight: 8 }} /> 
                Total Records
              </Typography>
              <StatValue color="primary">{totalRecords}</StatValue>
              <Typography variant="body2" color="textSecondary">
                Last 30 days
              </Typography>
            </StyledCardContent>
          </StyledCard>
        </Grid>
        
        {/* Anomalies Detected Card */}
        <Grid item xs={12} md={4}>
          <StyledCard>
            <StyledCardContent>
              <Typography variant="h6" color="textSecondary" gutterBottom>
                <WarningIcon fontSize="small" style={{ verticalAlign: 'middle', marginRight: 8 }} /> 
                Anomalies Detected
              </Typography>
              <StatValue color="error">{anomalyCount}</StatValue>
              <Typography variant="body2" color="textSecondary">
                Last 30 days
              </Typography>
            </StyledCardContent>
          </StyledCard>
        </Grid>
        
        {/* Last Updated Card */}
        <Grid item xs={12} md={4}>
          <StyledCard>
            <StyledCardContent>
              <Typography variant="h6" color="textSecondary" gutterBottom>
                <UpdateIcon fontSize="small" style={{ verticalAlign: 'middle', marginRight: 8 }} /> 
                Last Updated
              </Typography>
              <StatValue>{lastUpdated.toLocaleTimeString()}</StatValue>
              <Typography variant="body2" color="textSecondary">
                {lastUpdated.toLocaleDateString()}
              </Typography>
            </StyledCardContent>
          </StyledCard>
        </Grid>

        {/* Recent Anomalies Section */}
        <Grid item xs={12}>
          <StyledCard>
            <StyledCardContent>
              <Typography variant="h6" gutterBottom>
                <WarningIcon fontSize="small" style={{ verticalAlign: 'middle', marginRight: 8 }} />
                Recent Anomalies
              </Typography>
              
              {anomalies && anomalies.length > 0 ? (
                anomalies.slice(0, 5).map(anomaly => (
                  <Card key={anomaly.index} sx={{ mb: 2, borderLeft: '4px solid red' }}>
                    <CardContent>
                      <Typography variant="h6">{anomaly.product_id}</Typography>
                      <Typography variant="body2" color="textSecondary">
                        {new Date(anomaly.timestamp).toLocaleString()}
                      </Typography>
                      <Typography variant="body2">
                        Temperature: {anomaly.temperature}°C, Humidity: {anomaly.humidity}%
                      </Typography>
                      {anomaly.reasons && (
                        <Typography variant="body2" color="error">
                          Reasons: {anomaly.reasons.join(', ')}
                        </Typography>
                      )}
                    </CardContent>
                  </Card>
                ))
              ) : (
                <Typography>No recent anomalies detected</Typography>
              )}
              
              <Typography 
                variant="body2" 
                align="right" 
                color="primary" 
                sx={{ mt: 1, cursor: 'pointer' }}
                onClick={() => window.location.href = '/anomaly-detection'}
              >
                VIEW ALL ANOMALIES
              </Typography>
            </StyledCardContent>
          </StyledCard>
        </Grid>
      </Grid>
    </Root>
  );
};

export default Dashboard;