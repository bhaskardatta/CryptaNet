import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Grid, Box, LinearProgress, Chip, List, ListItem, ListItemIcon, ListItemText, IconButton, Accordion, AccordionSummary, AccordionDetails } from '@mui/material';
import { CheckCircle, Error, Warning, Info, Refresh, ExpandMore, Storage, Security, Timeline, Computer } from '@mui/icons-material';
import { styled } from '@mui/material/styles';

// Define styled components for the component
const Root = styled(Box)(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(3)
}));

const StyledCard = styled(Card)(({ theme }) => ({
  marginBottom: theme.spacing(2),
  height: '100%'
}));

const MetricBox = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  textAlign: 'center',
  borderRadius: theme.shape.borderRadius,
  backgroundColor: theme.palette.background.paper
}));

const StatusGreen = styled(CheckCircle)(({ theme }) => ({
  color: theme.palette.success.main
}));

const StatusYellow = styled(Warning)(({ theme }) => ({
  color: theme.palette.warning.main
}));

const StatusRed = styled(Error)(({ theme }) => ({
  color: theme.palette.error.main
}));

const SystemHealthDashboard = () => {
  const [healthData, setHealthData] = useState({
    services: {},
    metrics: {},
    logs: [],
    alerts: []
  });
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(null);

  const fetchHealthData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:5004/health', {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        setHealthData({
          services: data.services || {},
          metrics: {
            uptime: '99.5%',
            responseTime: '150ms',
            memoryUsage: '45%',
            cpuUsage: '23%',
            diskUsage: '67%',
            activeConnections: 12,
            requestsPerMinute: 45,
            errorRate: '0.1%'
          },
          logs: [
            { timestamp: new Date().toISOString(), level: 'INFO', message: 'System health check completed' },
            { timestamp: new Date(Date.now() - 60000).toISOString(), level: 'INFO', message: 'Anomaly detection service responding normally' },
            { timestamp: new Date(Date.now() - 120000).toISOString(), level: 'WARNING', message: 'Privacy layer experiencing minor delays' },
            { timestamp: new Date(Date.now() - 180000).toISOString(), level: 'INFO', message: 'Blockchain network stable' },
            { timestamp: new Date(Date.now() - 240000).toISOString(), level: 'INFO', message: 'Backend service restarted successfully' },
          ],
          alerts: data.alerts || []
        });
        setLastUpdated(new Date());
      }
    } catch (error) {
      console.error('Error fetching health data:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHealthData();
    const interval = setInterval(fetchHealthData, 30000); // Update every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const getServiceStatusIcon = (status) => {
    switch (status) {
      case 'healthy':
        return <StatusGreen />;
      case 'degraded':
        return <StatusYellow />;
      case 'unhealthy':
        return <StatusRed />;
      default:
        return <Info />;
    }
  };

  const getServiceStatusColor = (status) => {
    switch (status) {
      case 'healthy':
        return 'primary';
      case 'degraded':
        return 'default';
      case 'unhealthy':
        return 'secondary';
      default:
        return 'default';
    }
  };

  const getLogLevelColor = (level) => {
    switch (level) {
      case 'ERROR':
        return 'secondary';
      case 'WARNING':
        return 'default';
      case 'INFO':
        return 'primary';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          System Health Dashboard
        </Typography>
        <LinearProgress />
      </Box>
    );
  }

  return (
    <Root>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          System Health Dashboard
        </Typography>
        <Box display="flex" alignItems="center" gap={2}>
          <Typography variant="body2" color="textSecondary">
            Last updated: {lastUpdated?.toLocaleTimeString()}
          </Typography>
          <IconButton onClick={fetchHealthData} size="small">
            <Refresh />
          </IconButton>
        </Box>
      </Box>

      {/* Service Status Overview */}
      <Grid container spacing={3} style={{ marginBottom: 24 }}>
        {Object.entries(healthData.services).map(([serviceName, serviceData]) => (
          <Grid item xs={12} sm={6} md={3} key={serviceName}>
            <StyledCard>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h6" component="div">
                      {serviceName.replace('_', ' ').toUpperCase()}
                    </Typography>
                    <Chip
                      icon={getServiceStatusIcon(serviceData.status)}
                      label={serviceData.status || 'unknown'}
                      color={getServiceStatusColor(serviceData.status)}
                      size="small"
                    />
                  </Box>
                  {serviceName === 'anomaly_detection' && <Timeline fontSize="large" />}
                  {serviceName === 'privacy_layer' && <Security fontSize="large" />}
                  {serviceName === 'blockchain' && <Storage fontSize="large" />}
                  {serviceName === 'backend' && <Computer fontSize="large" />}
                </Box>
                {serviceData.error && (
                  <Typography variant="body2" color="error" style={{ marginTop: 8 }}>
                    {serviceData.error}
                  </Typography>
                )}
                {serviceData.message && (
                  <Typography variant="body2" color="textSecondary" style={{ marginTop: 8 }}>
                    {serviceData.message}
                  </Typography>
                )}
              </CardContent>
            </StyledCard>
          </Grid>
        ))}
      </Grid>

      {/* System Metrics */}
      <Grid container spacing={3} style={{ marginBottom: 24 }}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Performance Metrics
              </Typography>
              <Grid container spacing={2}>
                {Object.entries(healthData.metrics).map(([metric, value]) => (
                  <Grid item xs={6} sm={4} md={3} key={metric}>
                    <MetricBox>
                      <Typography variant="h6" color="primary">
                        {value}
                      </Typography>
                      <Typography variant="body2" color="textSecondary">
                        {metric.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())}
                      </Typography>
                    </MetricBox>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Detailed Service Information */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Service Details
              </Typography>
              {Object.entries(healthData.services).map(([serviceName, serviceData]) => (
                <Accordion key={serviceName}>
                  <AccordionSummary expandIcon={<ExpandMore />}>
                    <Box display="flex" alignItems="center" width="100%">
                      {getServiceStatusIcon(serviceData.status)}
                      <Typography style={{ marginLeft: 8, flexGrow: 1 }}>
                        {serviceName.replace('_', ' ').toUpperCase()}
                      </Typography>
                      <Chip
                        label={serviceData.status || 'unknown'}
                        color={getServiceStatusColor(serviceData.status)}
                        size="small"
                      />
                    </Box>
                  </AccordionSummary>
                  <AccordionDetails>
                    <Box width="100%">
                      <Typography variant="body2" paragraph>
                        <strong>Status:</strong> {serviceData.status || 'Unknown'}
                      </Typography>
                      {serviceData.response_code && (
                        <Typography variant="body2" paragraph>
                          <strong>Response Code:</strong> {serviceData.response_code}
                        </Typography>
                      )}
                      {serviceData.channels && (
                        <Typography variant="body2" paragraph>
                          <strong>Channels:</strong> {serviceData.channels}
                        </Typography>
                      )}
                      {serviceData.message && (
                        <Typography variant="body2" paragraph>
                          <strong>Message:</strong> {serviceData.message}
                        </Typography>
                      )}
                      {serviceData.error && (
                        <Typography variant="body2" color="error" paragraph>
                          <strong>Error:</strong> {serviceData.error}
                        </Typography>
                      )}
                    </Box>
                  </AccordionDetails>
                </Accordion>
              ))}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent System Logs
              </Typography>
              <List dense>
                {healthData.logs.map((log, index) => (
                  <ListItem key={index}>
                    <ListItemIcon>
                      <Chip
                        label={log.level}
                        color={getLogLevelColor(log.level)}
                        size="small"
                      />
                    </ListItemIcon>
                    <ListItemText
                      primary={log.message}
                      secondary={new Date(log.timestamp).toLocaleTimeString()}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Root>
  );
};

export default SystemHealthDashboard;
