import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { styled } from '@mui/material/styles';
import { 
  Paper, Typography, Grid, Button, TextField, FormControl, InputLabel, Select, MenuItem, 
  Tabs, Tab, Box, CircularProgress, Snackbar, Dialog, DialogTitle, DialogContent, DialogActions, 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, IconButton, Checkbox, 
  FormControlLabel, FormGroup, Divider, Card, CardContent, Chip, Badge, Fade, Grow,
  LinearProgress, Avatar
} from '@mui/material';
import { Alert } from '@mui/material';
import { 
  Visibility, Add, Search, Refresh, CloudDownload, Security, Timeline, 
  VerifiedUser, Business, LocationOn, AccessTime, Speed, Assessment, Settings 
} from '@mui/icons-material';
import { fetchSupplyChainData, submitSupplyChainData, retrieveSupplyChainData, clearError, clearSuccess, clearSelectedData } from '../store/slices/supplyChainSlice';
import { formatNumber, formatTemperature } from '../utils/numberFormatting';

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

const StatsCard = styled(Card)(({ theme }) => ({
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

const StyledPaper = styled(Paper)(({ theme }) => ({
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)'
    : 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%)',
  backdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
  borderRadius: theme.spacing(2),
  padding: theme.spacing(3),
  marginBottom: theme.spacing(2),
  boxShadow: theme.palette.mode === 'dark'
    ? '0 8px 32px rgba(0,0,0,0.3)'
    : '0 8px 32px rgba(0,0,0,0.1)',
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

const ModernFormControl = styled(FormControl)(({ theme }) => ({
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

const ModernTable = styled(Table)(({ theme }) => ({
  '& .MuiTableHead-root': {
    background: theme.palette.mode === 'dark'
      ? 'linear-gradient(90deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%)'
      : 'linear-gradient(90deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%)',
  },
  '& .MuiTableHead-root .MuiTableCell-root': {
    fontWeight: 600,
    textTransform: 'uppercase',
    fontSize: '0.75rem',
    letterSpacing: '0.05em',
    borderBottom: `2px solid ${theme.palette.divider}`,
  },
  '& .MuiTableBody-root .MuiTableRow-root': {
    transition: 'all 0.2s ease-in-out',
    '&:hover': {
      background: theme.palette.mode === 'dark'
        ? 'rgba(255,255,255,0.05)'
        : 'rgba(102, 126, 234, 0.05)',
      transform: 'scale(1.01)',
    },
  },
}));

const StatusChip = styled(Chip)(({ theme, status }) => {
  const colors = {
    active: { bg: '#4caf50', color: '#fff' },
    pending: { bg: '#ff9800', color: '#fff' },
    inactive: { bg: '#f44336', color: '#fff' },
  };
  
  return {
    background: colors[status]?.bg || '#757575',
    color: colors[status]?.color || '#fff',
    fontWeight: 600,
    borderRadius: theme.spacing(1),
    '& .MuiChip-icon': {
      color: 'inherit',
    },
  };
});

const StyledFormControl = styled(FormControl)(({ theme }) => ({
  margin: theme.spacing(1),
  minWidth: 120,
}));

const SubmitButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(2, 0),
}));

const TableContainerStyled = styled(TableContainer)(({ theme }) => ({
  marginTop: theme.spacing(2),
  borderRadius: theme.spacing(2),
  background: theme.palette.mode === 'dark'
    ? 'rgba(255,255,255,0.05)'
    : 'rgba(255,255,255,0.7)',
  backdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
}));

const LoadingContainer = styled('div')(({ theme }) => ({
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  padding: theme.spacing(4),
}));

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && <Box p={3}>{children}</Box>}
    </div>
  );
}

const SupplyChainData = () => {
  const dispatch = useDispatch();
  const { data, selectedData, loading, submitting, error, success } = useSelector((state) => state.supplyChain);
  const { user } = useSelector((state) => state.auth);
  const [tabValue, setTabValue] = useState(0);
  const [queryParams, setQueryParams] = useState({
    dataType: 'all',
    startTime: '',
    endTime: '',
    productId: '',
  });
  const [newData, setNewData] = useState({
    productId: '',
    product: '',
    dataType: 'temperature',
    temperature: '',
    humidity: '',
    location: '',
    batchNumber: '',
    supplier: '',
    manufacturer: '',
    expirationDate: '',
    storageConditions: '',
    qualityMetrics: {
      pH: '',
      moisture: '',
      density: '',
    },
    certifications: [],
    transportationMethod: '',
    carbonFootprint: '',
    sustainabilityScore: '',
    traceabilityLevel: 'high',
    priority: 'medium',
    notes: '',
    accessControl: {
      isPublic: true,
      allowedOrgs: [],
    },
  });
  const [detailsOpen, setDetailsOpen] = useState(false);

  // Auto-load data when component mounts
  useEffect(() => {
    dispatch(fetchSupplyChainData({
      organizationId: user?.organization || 'Org1MSP',
      ...queryParams,
    }));
  }, [dispatch, user]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleQueryChange = (e) => {
    const { name, value } = e.target;
    setQueryParams({
      ...queryParams,
      [name]: value,
    });
  };

  const handleNewDataChange = (e) => {
    const { name, value } = e.target;
    if (name.includes('.')) {
      // Handle nested fields like qualityMetrics.pH
      const [parent, child] = name.split('.');
      setNewData({
        ...newData,
        [parent]: {
          ...newData[parent],
          [child]: value,
        },
      });
    } else {
      setNewData({
        ...newData,
        [name]: value,
      });
    }
  };

  const handleCertificationChange = (e) => {
    const { value, checked } = e.target;
    if (checked) {
      setNewData({
        ...newData,
        certifications: [...newData.certifications, value],
      });
    } else {
      setNewData({
        ...newData,
        certifications: newData.certifications.filter(cert => cert !== value),
      });
    }
  };

  const handleAccessControlChange = (e) => {
    setNewData({
      ...newData,
      accessControl: {
        ...newData.accessControl,
        [e.target.name]: e.target.value,
      },
    });
  };

  const handleQuerySubmit = (e) => {
    e.preventDefault();
    dispatch(fetchSupplyChainData({
      organizationId: user?.organization || 'Org1MSP',
      ...queryParams,
    }));
  };

  const handleDataSubmit = (e) => {
    e.preventDefault();
    dispatch(submitSupplyChainData({
      data: newData,
      organizationId: user?.organization || 'Org1MSP',
      dataType: newData.dataType,
      accessControl: newData.accessControl,
    }));
  };

  const handleViewDetails = (dataId) => {
    // Use the organizationId from the data item if available, fallback to user org
    const orgId = data.find(item => item.id === dataId)?.organizationId || user?.organization || 'DataSimulator';
    dispatch(retrieveSupplyChainData({
      dataId,
      organizationId: orgId,
    }));
    setDetailsOpen(true);
  };

  const handleCloseDetails = () => {
    setDetailsOpen(false);
    dispatch(clearSelectedData());
  };

  const handleCloseSnackbar = () => {
    dispatch(clearError());
    dispatch(clearSuccess());
  };

  // Statistics for header
  const totalRecords = data?.length || 0;
  const activeProducts = data?.filter(item => {
    const product = item.product || item.data?.product;
    return product && product !== 'Unknown';
  }).length || 0;
  const recentRecords = data?.filter(item => {
    const timestamp = item.timestamp || new Date().toISOString();
    const recordDate = new Date(timestamp);
    const oneDayAgo = new Date(Date.now() - 24 * 60 * 60 * 1000);
    return recordDate >= oneDayAgo;
  }).length || 0;

  return (
    <Root>
      <Fade in timeout={800}>
        <HeaderSection>
          <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
            <Box>
              <Typography variant="h4" component="h1" sx={{ 
                fontWeight: 700, 
                color: 'white',
                textShadow: '0 2px 4px rgba(0,0,0,0.3)',
                mb: 1
              }}>
                Supply Chain Data Management
              </Typography>
              <Typography variant="subtitle1" sx={{ 
                color: 'rgba(255,255,255,0.9)',
                fontWeight: 400
              }}>
                Track and manage your supply chain data with blockchain security
              </Typography>
            </Box>
            <GradientButton
              variant="contained"
              startIcon={<Refresh />}
              onClick={() => dispatch(fetchSupplyChainData({
                organizationId: user?.organization || 'Org1MSP',
                ...queryParams,
              }))}
              disabled={loading}
            >
              Refresh Data
            </GradientButton>
          </Box>
          
          <Grid container spacing={3}>
            <Grid item xs={12} sm={4}>
              <StatsCard>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#667eea', mb: 1 }}>
                      {totalRecords}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Total Records
                    </Typography>
                  </Box>
                  <Avatar sx={{ 
                    bgcolor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    width: 56, 
                    height: 56 
                  }}>
                    <Assessment sx={{ fontSize: 28 }} />
                  </Avatar>
                </Box>
              </StatsCard>
            </Grid>
            <Grid item xs={12} sm={4}>
              <StatsCard>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#4caf50', mb: 1 }}>
                      {activeProducts}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Active Products
                    </Typography>
                  </Box>
                  <Avatar sx={{ 
                    bgcolor: 'linear-gradient(135deg, #4caf50 0%, #45a049 100%)',
                    width: 56, 
                    height: 56 
                  }}>
                    <Business sx={{ fontSize: 28 }} />
                  </Avatar>
                </Box>
              </StatsCard>
            </Grid>
            <Grid item xs={12} sm={4}>
              <StatsCard>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h4" sx={{ fontWeight: 700, color: '#ff9800', mb: 1 }}>
                      {recentRecords}
                    </Typography>
                    <Typography variant="body2" sx={{ color: 'text.secondary' }}>
                      Recent (24h)
                    </Typography>
                  </Box>
                  <Avatar sx={{ 
                    bgcolor: 'linear-gradient(135deg, #ff9800 0%, #f57c00 100%)',
                    width: 56, 
                    height: 56 
                  }}>
                    <AccessTime sx={{ fontSize: 28 }} />
                  </Avatar>
                </Box>
              </StatsCard>
            </Grid>
          </Grid>
        </HeaderSection>
      </Fade>

      <Grow in timeout={1000}>
        <StyledPaper>
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange} 
            indicatorColor="primary" 
            textColor="primary"
            sx={{
              '& .MuiTab-root': {
                fontWeight: 600,
                textTransform: 'none',
                fontSize: '1rem',
              },
              '& .MuiTabs-indicator': {
                height: 3,
                borderRadius: '3px 3px 0 0',
                background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
              },
            }}
          >
            <Tab 
              label="Query Data" 
              icon={<Search />} 
              iconPosition="start"
              sx={{ minHeight: 64 }}
            />
            <Tab 
              label="Submit New Data" 
              icon={<CloudDownload />} 
              iconPosition="start"
              sx={{ minHeight: 64 }}
            />
          </Tabs>

        <TabPanel value={tabValue} index={0}>
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
              Query Supply Chain Data
            </Typography>
            <form onSubmit={handleQuerySubmit}>
              <Grid container spacing={3}>
                <Grid item xs={12} sm={6} md={3}>
                  <ModernFormControl fullWidth variant="outlined">
                    <InputLabel id="data-type-label">Data Type</InputLabel>
                    <Select
                      labelId="data-type-label"
                      id="dataType"
                      name="dataType"
                      value={queryParams.dataType}
                      onChange={handleQueryChange}
                      label="Data Type"
                    >
                      <MenuItem value="all">All Types</MenuItem>
                      <MenuItem value="temperature">Temperature</MenuItem>
                      <MenuItem value="humidity">Humidity</MenuItem>
                      <MenuItem value="location">Location</MenuItem>
                    </Select>
                  </ModernFormControl>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                  <ModernTextField
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
                  <ModernTextField
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
                  <GradientButton
                    type="submit"
                    variant="contained"
                    color="primary"
                    fullWidth
                    startIcon={<Search />}
                    disabled={loading}
                    sx={{ height: '56px' }}
                  >
                    {loading ? 'Querying...' : 'Query Data'}
                  </GradientButton>
                </Grid>
              </Grid>
            </form>
          </Box>

          {loading ? (
            <LoadingContainer>
              <CircularProgress size={60} thickness={4} />
              <Typography variant="h6" sx={{ mt: 2, color: 'text.secondary' }}>
                Loading supply chain data...
              </Typography>
            </LoadingContainer>
          ) : (
            <Fade in timeout={600}>
              <TableContainerStyled component={Paper}>
                <ModernTable>
                  <TableHead>
                    <TableRow>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          <VerifiedUser sx={{ mr: 1, fontSize: 18 }} />
                          ID
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          <Business sx={{ mr: 1, fontSize: 18 }} />
                          Product
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          <Timeline sx={{ mr: 1, fontSize: 18 }} />
                          Type
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          <AccessTime sx={{ mr: 1, fontSize: 18 }} />
                          Timestamp
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          <Speed sx={{ mr: 1, fontSize: 18 }} />
                          Value
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Box display="flex" alignItems="center">
                          <Security sx={{ mr: 1, fontSize: 18 }} />
                          Actions
                        </Box>
                      </TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {data && data.length > 0 ? (
                      data.map((item, index) => {
                        // Extract data properly from various possible structures
                        const productId = item.productId || item.data?.productId || 'N/A';
                        const product = item.product || item.data?.product || 'Unknown';
                        const dataType = item.dataType || 'supply_chain';
                        const timestamp = item.timestamp || new Date().toISOString();
                        
                        // Extract values based on where they might be stored
                        const temperature = item.temperature || item.data?.temperature;
                        const humidity = item.humidity || item.data?.humidity;
                        const location = item.location || item.data?.location;
                        const quantity = item.quantity || item.data?.quantity;
                        
                        return (
                          <Fade in timeout={600 + (index * 100)} key={item.id}>
                            <TableRow>
                              <TableCell>
                                <Chip 
                                  label={item.id} 
                                  size="small" 
                                  variant="outlined"
                                  sx={{ fontWeight: 600 }}
                                />
                              </TableCell>
                              <TableCell>
                                <Box>
                                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                                    {(() => {
                                      if (productId && productId !== 'N/A') {
                                        return product ? `${productId}` : productId;
                                      }
                                      return product || 'Unknown Product';
                                    })()}
                                  </Typography>
                                  {product && product !== 'Unknown' && (
                                    <Typography variant="caption" color="textSecondary">
                                      {product}
                                    </Typography>
                                  )}
                                </Box>
                              </TableCell>
                              <TableCell>
                                <StatusChip 
                                  label={dataType} 
                                  size="small"
                                  status={dataType === 'temperature' ? 'active' : dataType === 'humidity' ? 'pending' : 'inactive'}
                                />
                              </TableCell>
                              <TableCell>
                                <Box display="flex" alignItems="center">
                                  <LocationOn sx={{ mr: 1, fontSize: 16, color: 'text.secondary' }} />
                                  <Typography variant="body2">
                                    {(() => {
                                      try {
                                        return new Date(timestamp).toLocaleString();
                                      } catch (e) {
                                        return 'Invalid Date';
                                      }
                                    })()}
                                  </Typography>
                                </Box>
                              </TableCell>
                              <TableCell>
                                <Box>
                                  <Typography variant="body2" sx={{ fontWeight: 600 }}>
                                    {(() => {
                                      // More robust value display with multiple fallbacks
                                      if (temperature !== undefined && temperature !== null && temperature !== '') {
                                        return `${formatTemperature(temperature)}`;
                                      } else if (humidity !== undefined && humidity !== null && humidity !== '') {
                                        return `${formatNumber(humidity, 1)}%`;
                                      } else if (location && typeof location === 'string' && location.trim() !== '') {
                                        return location;
                                      } else if (quantity !== undefined && quantity !== null && quantity !== '') {
                                        return `${formatNumber(quantity, 2)} units`;
                                      } else if (item.value !== undefined && item.value !== null) {
                                        // Generic value field
                                        if (dataType === 'temperature') {
                                          return formatTemperature(item.value);
                                        } else if (dataType === 'humidity') {
                                          return `${formatNumber(item.value, 1)}%`;
                                        } else {
                                          return item.value;
                                        }
                                      } else {
                                        return 'No data available';
                                      }
                                    })()}
                                  </Typography>
                                  <Typography variant="caption" color="textSecondary">
                                    {dataType === 'temperature' ? 'Temperature' : 
                                     dataType === 'humidity' ? 'Humidity' : 
                                     dataType === 'location' ? 'Location' : 'Supply Chain Data'}
                                  </Typography>
                                </Box>
                              </TableCell>
                              <TableCell>
                                <GradientButton
                                  size="small"
                                  variant="contained"
                                  onClick={() => handleViewDetails(item.id)}
                                  startIcon={<Visibility />}
                                  sx={{ minWidth: 'auto', px: 2 }}
                                >
                                  View
                                </GradientButton>
                              </TableCell>
                            </TableRow>
                          </Fade>
                        );
                      })
                    ) : (
                      <TableRow>
                        <TableCell colSpan={6} align="center">
                          <Box py={4}>
                            <Assessment sx={{ fontSize: 48, color: 'text.secondary', mb: 2 }} />
                            <Typography variant="h6" color="textSecondary">
                              No data found
                            </Typography>
                            <Typography variant="body2" color="textSecondary">
                              Try adjusting your query parameters or submit new data
                            </Typography>
                          </Box>
                        </TableCell>
                      </TableRow>
                    )}
                  </TableBody>
                </ModernTable>
              </TableContainerStyled>
            </Fade>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <Box sx={{ mb: 3 }}>
            <Typography variant="h6" sx={{ mb: 2, fontWeight: 600 }}>
              Submit New Supply Chain Data
            </Typography>
          </Box>
          
          <form onSubmit={handleDataSubmit}>
            <Grid container spacing={3}>
              {/* Basic Information */}
              <Grid item xs={12}>
                <Box display="flex" alignItems="center" mb={2}>
                  <Business sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Basic Product Information
                  </Typography>
                </Box>
                <Divider sx={{ mb: 3 }} />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  required
                  id="productId"
                  name="productId"
                  label="Product ID"
                  value={newData.productId}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="Enter unique product identifier"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  required
                  id="product"
                  name="product"
                  label="Product Name"
                  value={newData.product}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="Enter product name"
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  id="batchNumber"
                  name="batchNumber"
                  label="Batch Number"
                  value={newData.batchNumber}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="Enter batch number"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  id="supplier"
                  name="supplier"
                  label="Supplier"
                  value={newData.supplier}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="Enter supplier name"
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  id="manufacturer"
                  name="manufacturer"
                  label="Manufacturer"
                  value={newData.manufacturer}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="Enter manufacturer name"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  id="expirationDate"
                  name="expirationDate"
                  label="Expiration Date"
                  type="date"
                  value={newData.expirationDate}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  InputLabelProps={{ shrink: true }}
                />
              </Grid>

              {/* Environmental Conditions */}
              <Grid item xs={12}>
                <Box display="flex" alignItems="center" mb={2} mt={3}>
                  <Speed sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Environmental Conditions
                  </Typography>
                </Box>
                <Divider sx={{ mb: 3 }} />
              </Grid>

              <Grid item xs={12} sm={6}>
                <ModernFormControl fullWidth variant="outlined">
                  <InputLabel id="new-data-type-label">Primary Data Type</InputLabel>
                  <Select
                    labelId="new-data-type-label"
                    id="dataType"
                    name="dataType"
                    value={newData.dataType}
                    onChange={handleNewDataChange}
                    label="Primary Data Type"
                  >
                    <MenuItem value="temperature">Temperature Monitoring</MenuItem>
                    <MenuItem value="humidity">Humidity Control</MenuItem>
                    <MenuItem value="location">Location Tracking</MenuItem>
                    <MenuItem value="mixed">Mixed Conditions</MenuItem>
                  </Select>
                </ModernFormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  id="temperature"
                  name="temperature"
                  label="Temperature (°C)"
                  type="number"
                  inputProps={{ step: "0.1" }}
                  value={newData.temperature}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="e.g., 2.5"
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  id="humidity"
                  name="humidity"
                  label="Humidity (%)"
                  type="number"
                  inputProps={{ step: "0.1", min: "0", max: "100" }}
                  value={newData.humidity}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="e.g., 65.0"
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  id="location"
                  name="location"
                  label="Location"
                  value={newData.location}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="e.g., Warehouse A, Sector 3"
                />
              </Grid>
              
              <Grid item xs={12}>
                <ModernTextField
                  fullWidth
                  id="storageConditions"
                  name="storageConditions"
                  label="Storage Conditions"
                  value={newData.storageConditions}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  multiline
                  rows={2}
                  placeholder="Describe storage requirements and conditions (e.g., refrigerated, dry, ventilated)"
                />
              </Grid>

              {/* Quality Metrics */}
              <Grid item xs={12}>
                <Box display="flex" alignItems="center" mb={2} mt={3}>
                  <VerifiedUser sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Quality Metrics
                  </Typography>
                </Box>
                <Divider sx={{ mb: 3 }} />
              </Grid>

              <Grid item xs={12} sm={4}>
                <ModernTextField
                  fullWidth
                  id="qualityMetrics.pH"
                  name="qualityMetrics.pH"
                  label="pH Level"
                  type="number"
                  inputProps={{ step: "0.01", min: "0", max: "14" }}
                  value={newData.qualityMetrics.pH}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="e.g., 7.2"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <ModernTextField
                  fullWidth
                  id="qualityMetrics.moisture"
                  name="qualityMetrics.moisture"
                  label="Moisture Content (%)"
                  type="number"
                  inputProps={{ step: "0.1", min: "0", max: "100" }}
                  value={newData.qualityMetrics.moisture}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="e.g., 12.5"
                />
              </Grid>
              <Grid item xs={12} sm={4}>
                <ModernTextField
                  fullWidth
                  id="qualityMetrics.density"
                  name="qualityMetrics.density"
                  label="Density (g/cm³)"
                  type="number"
                  inputProps={{ step: "0.001" }}
                  value={newData.qualityMetrics.density}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="e.g., 1.025"
                />
              </Grid>

              {/* Certifications */}
              <Grid item xs={12}>
                <Box display="flex" alignItems="center" mb={2} mt={3}>
                  <Security sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Certifications & Standards
                  </Typography>
                </Box>
                <Divider sx={{ mb: 3 }} />
                <Box sx={{ 
                  display: 'flex', 
                  flexWrap: 'wrap', 
                  gap: 2,
                  p: 2,
                  background: theme => theme.palette.mode === 'dark' 
                    ? 'rgba(255,255,255,0.05)' 
                    : 'rgba(255,255,255,0.8)',
                  borderRadius: 2,
                  backdropFilter: 'blur(10px)',
                  border: theme => `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
                }}>
                  {['ISO 9001', 'ISO 14001', 'HACCP', 'Organic', 'Fair Trade', 'FDA Approved'].map((cert) => (
                    <FormControlLabel
                      key={cert}
                      control={
                        <Checkbox
                          checked={newData.certifications.includes(cert)}
                          onChange={handleCertificationChange}
                          value={cert}
                          sx={{
                            '&.Mui-checked': {
                              color: 'primary.main',
                            },
                          }}
                        />
                      }
                      label={cert}
                      sx={{ 
                        minWidth: '200px',
                        '& .MuiFormControlLabel-label': {
                          fontWeight: 500,
                        }
                      }}
                    />
                  ))}
                </Box>
              </Grid>

              {/* Logistics & Sustainability */}
              <Grid item xs={12}>
                <Box display="flex" alignItems="center" mb={2} mt={3}>
                  <LocationOn sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    Logistics & Sustainability
                  </Typography>
                </Box>
                <Divider sx={{ mb: 3 }} />
              </Grid>

              <Grid item xs={12} sm={6}>
                <ModernFormControl fullWidth variant="outlined">
                  <InputLabel id="transportation-label">Transportation Method</InputLabel>
                  <Select
                    labelId="transportation-label"
                    id="transportationMethod"
                    name="transportationMethod"
                    value={newData.transportationMethod}
                    onChange={handleNewDataChange}
                    label="Transportation Method"
                  >
                    <MenuItem value="truck">🚛 Truck</MenuItem>
                    <MenuItem value="ship">🚢 Ship</MenuItem>
                    <MenuItem value="air">✈️ Air Freight</MenuItem>
                    <MenuItem value="rail">🚂 Rail</MenuItem>
                    <MenuItem value="multimodal">🔄 Multimodal</MenuItem>
                  </Select>
                </ModernFormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  id="carbonFootprint"
                  name="carbonFootprint"
                  label="Carbon Footprint (kg CO₂)"
                  type="number"
                  inputProps={{ step: "0.01", min: "0" }}
                  value={newData.carbonFootprint}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="e.g., 125.50"
                />
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <ModernTextField
                  fullWidth
                  id="sustainabilityScore"
                  name="sustainabilityScore"
                  label="Sustainability Score (0-100)"
                  type="number"
                  inputProps={{ min: "0", max: "100" }}
                  value={newData.sustainabilityScore}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  placeholder="e.g., 85"
                />
              </Grid>

              <Grid item xs={12} sm={6}>
                <ModernFormControl fullWidth variant="outlined">
                  <InputLabel id="traceability-label">Traceability Level</InputLabel>
                  <Select
                    labelId="traceability-label"
                    id="traceabilityLevel"
                    name="traceabilityLevel"
                    value={newData.traceabilityLevel}
                    onChange={handleNewDataChange}
                    label="Traceability Level"
                  >
                    <MenuItem value="high">🟢 High - Full traceability</MenuItem>
                    <MenuItem value="medium">🟡 Medium - Partial traceability</MenuItem>
                    <MenuItem value="low">🔴 Low - Limited traceability</MenuItem>
                  </Select>
                </ModernFormControl>
              </Grid>

              {/* System Controls */}
              <Grid item xs={12}>
                <Box display="flex" alignItems="center" mb={2} mt={3}>
                  <Settings sx={{ mr: 1, color: 'primary.main' }} />
                  <Typography variant="h6" sx={{ fontWeight: 600 }}>
                    System Controls
                  </Typography>
                </Box>
                <Divider sx={{ mb: 3 }} />
              </Grid>

              <Grid item xs={12} sm={6}>
                <ModernFormControl fullWidth variant="outlined">
                  <InputLabel id="priority-label">Priority Level</InputLabel>
                  <Select
                    labelId="priority-label"
                    id="priority"
                    name="priority"
                    value={newData.priority}
                    onChange={handleNewDataChange}
                    label="Priority Level"
                  >
                    <MenuItem value="low">🔵 Low Priority</MenuItem>
                    <MenuItem value="medium">🟡 Medium Priority</MenuItem>
                    <MenuItem value="high">🟠 High Priority</MenuItem>
                    <MenuItem value="critical">🔴 Critical Priority</MenuItem>
                  </Select>
                </ModernFormControl>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <ModernFormControl fullWidth variant="outlined">
                  <InputLabel id="access-control-label">Access Control</InputLabel>
                  <Select
                    labelId="access-control-label"
                    id="isPublic"
                    name="isPublic"
                    value={newData.accessControl.isPublic}
                    onChange={handleAccessControlChange}
                    label="Access Control"
                  >
                    <MenuItem value={true}>🌐 Public Access</MenuItem>
                    <MenuItem value={false}>🔒 Private Access</MenuItem>
                  </Select>
                </ModernFormControl>
              </Grid>
              
              <Grid item xs={12}>
                <ModernTextField
                  fullWidth
                  id="notes"
                  name="notes"
                  label="Additional Notes"
                  value={newData.notes}
                  onChange={handleNewDataChange}
                  variant="outlined"
                  multiline
                  rows={3}
                  placeholder="Enter any additional information about this product, special handling requirements, or observations..."
                />
              </Grid>
              
              <Grid item xs={12}>
                <Box display="flex" justifyContent="flex-end" mt={3}>
                  <GradientButton
                    type="submit"
                    variant="contained"
                    color="primary"
                    startIcon={<CloudDownload />}
                    disabled={submitting}
                    size="large"
                    sx={{ 
                      minWidth: '200px',
                      py: 1.5,
                      fontSize: '1.1rem',
                      fontWeight: 600,
                    }}
                  >
                    {submitting ? (
                      <>
                        <CircularProgress size={20} sx={{ mr: 1 }} />
                        Submitting...
                      </>
                    ) : (
                      'Submit Enhanced Data'
                    )}
                  </GradientButton>
                </Box>
              </Grid>
            </Grid>
          </form>
        </TabPanel>
        </StyledPaper>
      </Grow>

      {/* Details Dialog */}
      <Dialog open={detailsOpen} onClose={handleCloseDetails} maxWidth="md" fullWidth>
        <DialogTitle>Data Details</DialogTitle>
        <DialogContent>
          {selectedData ? (
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">ID:</Typography>
                <Typography variant="body1">{selectedData.id}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Product ID:</Typography>
                <Typography variant="body1">{selectedData.productId || selectedData.data?.productId || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Product:</Typography>
                <Typography variant="body1">{selectedData.product || selectedData.data?.product || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Data Type:</Typography>
                <Typography variant="body1">{selectedData.dataType || 'supply_chain'}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Timestamp:</Typography>
                <Typography variant="body1">
                  {selectedData.timestamp ? 
                    (typeof selectedData.timestamp === 'string' ? 
                      (isNaN(Date.parse(selectedData.timestamp)) ? 'Invalid Date' : new Date(selectedData.timestamp).toLocaleString()) : 
                      (selectedData.timestamp instanceof Date ? selectedData.timestamp.toLocaleString() : 'Invalid Date')) : 
                    new Date().toLocaleString()}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Temperature:</Typography>
                <Typography variant="body1">
                  {(() => {
                    const temp = selectedData.temperature || selectedData.data?.temperature;
                    return (temp !== undefined && temp !== null) ? formatTemperature(temp) : 'N/A';
                  })()}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Humidity:</Typography>
                <Typography variant="body1">
                  {(() => {
                    const humidity = selectedData.humidity || selectedData.data?.humidity;
                    return (humidity !== undefined && humidity !== null) ? `${formatNumber(humidity, 1)}%` : 'N/A';
                  })()}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Location:</Typography>
                <Typography variant="body1">{selectedData.location || selectedData.data?.location || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12}>            <Typography variant="subtitle1" sx={{ mt: 2, mb: 1, fontWeight: 'bold' }}>
              Blockchain Information:
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2">
                  <strong>Transaction ID:</strong> {selectedData.transactionId || selectedData.blockchain?.transactionId || 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Block Number:</strong> {selectedData.blockNumber || selectedData.blockchain?.blockNumber || 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Block Hash:</strong> {selectedData.blockHash || selectedData.blockchain?.blockHash ? 
                    `${(selectedData.blockHash || selectedData.blockchain.blockHash).substring(0, 12)}...` : 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Timestamp:</strong> {selectedData.blockTimestamp || selectedData.blockchain?.blockTimestamp ? 
                    new Date(selectedData.blockTimestamp || selectedData.blockchain.blockTimestamp).toLocaleString() : 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Gas Used:</strong> {selectedData.gasUsed || selectedData.blockchain?.gasUsed || 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Network Fee:</strong> {selectedData.networkFee || selectedData.blockchain?.networkFee ? 
                    `${selectedData.networkFee || selectedData.blockchain.networkFee} ETH` : 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Consensus Score:</strong> {selectedData.consensusScore || selectedData.blockchain?.consensusScore ? 
                    `${((selectedData.consensusScore || selectedData.blockchain.consensusScore) * 100).toFixed(1)}%` : 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Organization MSP:</strong> {selectedData.organizationMSP || selectedData.blockchain?.organizationMSP || 'N/A'}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="body2">
                  <strong>Validator Nodes:</strong> {selectedData.validatorNodes || selectedData.blockchain?.validatorNodes || 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Network Latency:</strong> {selectedData.networkLatency || selectedData.blockchain?.networkLatency ? 
                    `${selectedData.networkLatency || selectedData.blockchain.networkLatency}ms` : 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Data Integrity Hash:</strong> {selectedData.dataIntegrityHash || selectedData.blockchain?.dataIntegrityHash ? 
                    `${(selectedData.dataIntegrityHash || selectedData.blockchain.dataIntegrityHash).substring(0, 12)}...` : 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Encryption Type:</strong> {selectedData.encryptionType || selectedData.blockchain?.encryptionType || 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Merkle Root:</strong> {selectedData.merkleRoot || selectedData.blockchain?.merkleRoot ? 
                    `${(selectedData.merkleRoot || selectedData.blockchain.merkleRoot).substring(0, 12)}...` : 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Mining Difficulty:</strong> {selectedData.difficulty || selectedData.blockchain?.difficulty || 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Chain ID:</strong> {selectedData.chainId || selectedData.blockchain?.chainId || 'N/A'}
                </Typography>
                <Typography variant="body2">
                  <strong>Nonce:</strong> {selectedData.nonce || selectedData.blockchain?.nonce || 'N/A'}
                </Typography>
              </Grid>
            </Grid>
              </Grid>
            </Grid>
          ) : (
            <LoadingContainer>
              <CircularProgress />
            </LoadingContainer>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDetails} color="primary">
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar open={!!error || success} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert onClose={handleCloseSnackbar} severity={error ? 'error' : 'success'}>
          {error || success}
        </Alert>
      </Snackbar>
    </Root>
  );
};

export default SupplyChainData;