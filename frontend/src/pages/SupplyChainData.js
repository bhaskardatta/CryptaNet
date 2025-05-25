import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { styled } from '@mui/material/styles';
import { Paper, Typography, Grid, Button, TextField, FormControl, InputLabel, Select, MenuItem, Tabs, Tab, Box, CircularProgress, Snackbar, Dialog, DialogTitle, DialogContent, DialogActions, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, IconButton,  } from '@mui/material';
import { Alert } from '@mui/material';
import { Visibility, Add, Search } from '@mui/icons-material';
import { fetchSupplyChainData, submitSupplyChainData, retrieveSupplyChainData, clearError, clearSuccess, clearSelectedData } from '../store/slices/supplyChainSlice';

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

const SubmitButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(2, 0),
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
    accessControl: {
      isPublic: true,
      allowedOrgs: [],
    },
  });
  const [detailsOpen, setDetailsOpen] = useState(false);

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
    setNewData({
      ...newData,
      [e.target.name]: e.target.value,
    });
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
    dispatch(retrieveSupplyChainData({
      dataId,
      organizationId: user?.organization || 'Org1MSP',
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

  return (
    <Root>
      <Typography variant="h4" gutterBottom>
        Supply Chain Data
      </Typography>

      <StyledPaper>
        <Tabs value={tabValue} onChange={handleTabChange} indicatorColor="primary" textColor="primary">
          <Tab label="Query Data" />
          <Tab label="Submit New Data" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <form onSubmit={handleQuerySubmit}>
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
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  fullWidth
                  startIcon={<Search />}
                  disabled={loading}
                >
                  Query
                </Button>
              </Grid>
            </Grid>
          </form>

          {loading ? (
            <LoadingContainer>
              <CircularProgress />
            </LoadingContainer>
          ) : (
            <TableContainerStyled component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>ID</TableCell>
                    <TableCell>Product ID</TableCell>
                    <TableCell>Type</TableCell>
                    <TableCell>Timestamp</TableCell>
                    <TableCell>Value</TableCell>
                    <TableCell>Actions</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data && data.length > 0 ? (
                    data.map((item) => {
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
                        <TableRow key={item.id}>
                          <TableCell>{item.id}</TableCell>
                          <TableCell>
                            {(() => {
                              if (productId && productId !== 'N/A') {
                                return product ? `${productId} - ${product}` : productId;
                              }
                              return product || 'Unknown Product';
                            })()}
                          </TableCell>
                          <TableCell>{dataType}</TableCell>
                          <TableCell>
                            {(() => {
                              try {
                                return new Date(timestamp).toLocaleString();
                              } catch (e) {
                                return 'Invalid Date';
                              }
                            })()}
                          </TableCell>
                          <TableCell>
                            {(() => {
                              // More robust value display with multiple fallbacks
                              if (temperature !== undefined && temperature !== null && temperature !== '') {
                                return `Temperature: ${temperature}°C`;
                              } else if (humidity !== undefined && humidity !== null && humidity !== '') {
                                return `Humidity: ${humidity}%`;
                              } else if (location && typeof location === 'string' && location.trim() !== '') {
                                return `Location: ${location}`;
                              } else if (quantity !== undefined && quantity !== null && quantity !== '') {
                                return `Quantity: ${quantity}`;
                              } else if (item.value !== undefined && item.value !== null) {
                                // Generic value field
                                if (dataType === 'temperature') {
                                  return `${item.value}°C`;
                                } else if (dataType === 'humidity') {
                                  return `${item.value}%`;
                                } else {
                                  return item.value;
                                }
                              } else {
                                // Try to extract any numeric value from the data object
                                const dataObj = item.data || {};
                                const numericValues = Object.entries(dataObj)
                                  .filter(([key, value]) => typeof value === 'number' && !isNaN(value))
                                  .map(([key, value]) => {
                                    if (key.toLowerCase().includes('temp')) return `${value}°C`;
                                    if (key.toLowerCase().includes('humid')) return `${value}%`;
                                    return `${key}: ${value}`;
                                  });
                                
                                return numericValues.length > 0 ? numericValues[0] : 'No data available';
                              }
                            })()}
                          </TableCell>
                          <TableCell>
                            <IconButton onClick={() => handleViewDetails(item.id)}>
                              <Visibility />
                            </IconButton>
                          </TableCell>
                        </TableRow>
                      );
                    })
                  ) : (
                    <TableRow>
                      <TableCell colSpan={6} align="center">
                        No data found
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainerStyled>
          )}
        </TabPanel>

        <TabPanel value={tabValue} index={1}>
          <form onSubmit={handleDataSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  required
                  id="productId"
                  name="productId"
                  label="Product ID"
                  value={newData.productId}
                  onChange={handleNewDataChange}
                  variant="outlined"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
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
                <StyledFormControl fullWidth variant="outlined">
                  <InputLabel id="new-data-type-label">Data Type</InputLabel>
                  <Select
                    labelId="new-data-type-label"
                    id="dataType"
                    name="dataType"
                    value={newData.dataType}
                    onChange={handleNewDataChange}
                    label="Data Type"
                  >
                    <MenuItem value="temperature">Temperature</MenuItem>
                    <MenuItem value="humidity">Humidity</MenuItem>
                    <MenuItem value="location">Location</MenuItem>
                  </Select>
                </StyledFormControl>
              </Grid>
              
              {newData.dataType === 'temperature' && (
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    required
                    id="temperature"
                    name="temperature"
                    label="Temperature (°C)"
                    type="number"
                    value={newData.temperature}
                    onChange={handleNewDataChange}
                    variant="outlined"
                  />
                </Grid>
              )}
              
              {newData.dataType === 'humidity' && (
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    required
                    id="humidity"
                    name="humidity"
                    label="Humidity (%)"
                    type="number"
                    value={newData.humidity}
                    onChange={handleNewDataChange}
                    variant="outlined"
                  />
                </Grid>
              )}
              
              {newData.dataType === 'location' && (
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    required
                    id="location"
                    name="location"
                    label="Location"
                    value={newData.location}
                    onChange={handleNewDataChange}
                    variant="outlined"
                  />
                </Grid>
              )}
              
              <Grid item xs={12} sm={6}>
                <StyledFormControl fullWidth variant="outlined">
                  <InputLabel id="access-control-label">Access Control</InputLabel>
                  <Select
                    labelId="access-control-label"
                    id="isPublic"
                    name="isPublic"
                    value={newData.accessControl.isPublic}
                    onChange={handleAccessControlChange}
                    label="Access Control"
                  >
                    <MenuItem value={true}>Public</MenuItem>
                    <MenuItem value={false}>Private</MenuItem>
                  </Select>
                </StyledFormControl>
              </Grid>
              
              <Grid item xs={12}>
                <SubmitButton
                  type="submit"
                  variant="contained"
                  color="primary"
                  startIcon={<Add />}
                  disabled={submitting}
                >
                  {submitting ? 'Submitting...' : 'Submit Data'}
                </SubmitButton>
              </Grid>
            </Grid>
          </form>
        </TabPanel>
      </StyledPaper>

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
                    return (temp !== undefined && temp !== null) ? `${temp}°C` : 'N/A';
                  })()}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Humidity:</Typography>
                <Typography variant="body1">
                  {(() => {
                    const humidity = selectedData.humidity || selectedData.data?.humidity;
                    return (humidity !== undefined && humidity !== null) ? `${humidity}%` : 'N/A';
                  })()}
                </Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Location:</Typography>
                <Typography variant="body1">{selectedData.location || selectedData.data?.location || 'N/A'}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1">Blockchain Information:</Typography>
                <Typography variant="body2">Transaction ID: {selectedData.transactionId || 'N/A'}</Typography>
                <Typography variant="body2">Block Number: {selectedData.blockNumber || 'N/A'}</Typography>
                <Typography variant="body2">Timestamp: {selectedData.blockTimestamp ? new Date(selectedData.blockTimestamp).toLocaleString() : 'N/A'}</Typography>
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