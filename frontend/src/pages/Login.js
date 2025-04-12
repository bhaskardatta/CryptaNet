import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Snackbar,
  Grid,
  Box,
} from '@material-ui/core';
import { Alert } from '@material-ui/lab';
import { LockOutlined } from '@material-ui/icons';
import { login, clearError } from '../store/slices/authSlice';

const useStyles = makeStyles((theme) => ({
  root: {
    height: '100vh',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: theme.palette.background.default,
  },
  paper: {
    padding: theme.spacing(4),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    maxWidth: 400,
    width: '100%',
  },
  logo: {
    marginBottom: theme.spacing(2),
  },
  form: {
    width: '100%',
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
  lockIcon: {
    fontSize: 40,
    padding: theme.spacing(1),
    backgroundColor: theme.palette.primary.main,
    color: 'white',
    borderRadius: '50%',
    marginBottom: theme.spacing(2),
  },
}));

const Login = () => {
  const classes = useStyles();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state) => state.auth);
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  });

  const handleChange = (e) => {
    setCredentials({
      ...credentials,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const result = await dispatch(login(credentials));
    if (!result.error) {
      navigate('/');
    }
  };

  const handleCloseSnackbar = () => {
    dispatch(clearError());
  };

  return (
    <div className={classes.root}>
      <Container component="main" maxWidth="xs">
        <Paper className={classes.paper} elevation={3}>
          <Box display="flex" flexDirection="column" alignItems="center">
            <LockOutlined className={classes.lockIcon} />
            <Typography component="h1" variant="h5">
              CryptaNet
            </Typography>
            <Typography variant="subtitle1" color="textSecondary" gutterBottom>
              Privacy-Preserving & Explainable AI for Supply Chain
            </Typography>
          </Box>

          <form className={classes.form} onSubmit={handleSubmit}>
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              value={credentials.username}
              onChange={handleChange}
            />
            <TextField
              variant="outlined"
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              value={credentials.password}
              onChange={handleChange}
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              className={classes.submit}
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Sign In'}
            </Button>
          </form>

          <Snackbar open={!!error} autoHideDuration={6000} onClose={handleCloseSnackbar}>
            <Alert onClose={handleCloseSnackbar} severity="error">
              {error}
            </Alert>
          </Snackbar>
        </Paper>
      </Container>
    </div>
  );
};

export default Login;