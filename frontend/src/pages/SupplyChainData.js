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
  Tabs,
  Tab,
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
} from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import { Visibility, Add, Search } from '@material-ui/icons';
import { fetchSupplyChainData, submitSupplyChainData, retrieveSupplyChainData, clearError, clearSuccess, setSelectedData, clearSelectedData } from '../store/slices/supplyChainSlice';

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
  submitButton: {
    margin: theme.spacing(2, 0),
  },
  tabContent: {
    padding: theme.spacing(2),
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
  const classes = useStyles();
  const dispatch = useDispatch();
  const { data, selectedData, loading, submitting, error, success } = useSelector((state) => state.supplyChain);
  const { user } = useSelector((state) => state.auth);
  const [tabValue, setTabValue] = useState(0);
  const [queryParams, setQueryParams] = useState({
    dataType: 'all',
    startTime: '',
    endTime: '',
    includeAnomaliesOnly: false,
  });
  const [newData, setNewData] = useState({
    productId: '',
    timestamp: new Date().toISOString(),
    location: '',
    temperature: '',
    humidity: '',
    dataType: 'temperature',
    accessControl: {
      isPublic: true,
      authorizedOrgs: [],
    },
  });
  const [detailsOpen, setDetailsOpen] = useState(false);

  useEffect(() => {
    // Set default date range to last 7 days
    const endDate = new Date();
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - 7);
    
    setQueryParams(prevParams => ({
      ...prevParams,
      startTime: startDate.toISOString().split('T')[0],
      endTime: endDate.toISOString().split('T')[0],
    }));
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleQueryChange = (e) => {
    setQueryParams({
      ...queryParams,
      [e.target.name]: e.target.value,
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
      organizationId: user?.organizationId || 'org1',
      ...queryParams,
    }));
  };

  const handleDataSubmit = (e) => {
    e.preventDefault();
    dispatch(submitSupplyChainData({
      data: newData,
      organizationId: user?.organizationId || 'org1',
      dataType: newData.dataType,
      accessControl: newData.accessControl,
    }));
  };

  const handleViewDetails = (dataId) => {
    dispatch(retrieveSupplyChainData({
      dataId,
      organizationId: user?.organizationId || 'org1',
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
    <div className={classes.root}>
      <Typography variant="h4" gutterBottom>
        Supply Chain Data
      </Typography>

      <Paper className={classes.paper}>
        <Tabs value={tabValue} onChange={handleTabChange} indicatorColor="primary" textColor="primary">
          <Tab label="Query Data" />
          <Tab label="Submit New Data" />
        </Tabs>

        <TabPanel value={tabValue} index={0}>
          <form onSubmit={handleQuerySubmit}>
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
            <div className={classes.loadingContainer}>
              <CircularProgress />
            </div>
          ) : (
            <TableContainer component={Paper} className={classes.tableContainer}>
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
                    data.map((item) => (
                      <TableRow key={item.id}>
                        <TableCell>{item.id}</TableCell>
                        <TableCell>{item.productId}</TableCell>
                        <TableCell>{item.dataType}</TableCell>
                        <TableCell>{new Date(item.timestamp).toLocaleString()}</TableCell>
                        <TableCell>
                          {item.dataType === 'temperature' && `${item.temperature}°C`}
                          {item.dataType === 'humidity' && `${item.humidity}%`}
                          {item.dataType === 'location' && item.location}
                        </TableCell>
                        <TableCell>
                          <IconButton onClick={() => handleViewDetails(item.id)}>
                            <Visibility />
                          </IconButton>
                        </TableCell>
                      </TableRow>
                    ))
                  ) : (
                    <TableRow>
                      <TableCell colSpan={6} align="center">
                        No data found
                      </TableCell>
                    </TableRow>
                  )}
                </TableBody>
              </Table>
            </TableContainer>
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
                <FormControl fullWidth variant="outlined">
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
                </FormControl>
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
                <FormControl fullWidth variant="outlined">
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
                </FormControl>
              </Grid>
              
              <Grid item xs={12}>
                <Button
                  type="submit"
                  variant="contained"
                  color="primary"
                  className={classes.submitButton}
                  startIcon={<Add />}
                  disabled={submitting}
                >
                  {submitting ? 'Submitting...' : 'Submit Data'}
                </Button>
              </Grid>
            </Grid>
          </form>
        </TabPanel>
      </Paper>

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
                <Typography variant="body1">{selectedData.productId}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Data Type:</Typography>
                <Typography variant="body1">{selectedData.dataType}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Timestamp:</Typography>
                <Typography variant="body1">{new Date(selectedData.timestamp).toLocaleString()}</Typography>
              </Grid>
              <Grid item xs={12} sm={6}>
                <Typography variant="subtitle1">Value:</Typography>
                <Typography variant="body1">
                  {selectedData.dataType === 'temperature' && `${selectedData.temperature}°C`}
                  {selectedData.dataType === 'humidity' && `${selectedData.humidity}%`}
                  {selectedData.dataType === 'location' && selectedData.location}
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle1">Blockchain Information:</Typography>
                <Typography variant="body2">Transaction ID: {selectedData.transactionId || 'N/A'}</Typography>
                <Typography variant="body2">Block Number: {selectedData.blockNumber || 'N/A'}</Typography>
                <Typography variant="body2">Timestamp: {selectedData.blockTimestamp ? new Date(selectedData.blockTimestamp).toLocaleString() : 'N/A'}</Typography>
              </Grid>
            </Grid>
          ) : (
            <div className={classes.loadingContainer}>
              <CircularProgress />
            </div>
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
          {error || 'Operation completed successfully'}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default SupplyChainData;