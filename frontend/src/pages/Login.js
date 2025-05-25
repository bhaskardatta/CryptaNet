import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useNavigate } from 'react-router-dom';
import { styled } from '@mui/material/styles';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Snackbar,
  Box,
  Alert,
} from '@mui/material';
import { LockOutlined } from '@mui/icons-material';
import { login, clearError } from '../store/slices/authSlice';

const Root = styled('div')(({ theme }) => ({
  height: '100vh',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: theme.palette.background.default,
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  maxWidth: 400,
  width: '100%',
}));

const Form = styled('form')(({ theme }) => ({
  width: '100%',
  marginTop: theme.spacing(1),
}));

const SubmitButton = styled(Button)(({ theme }) => ({
  margin: theme.spacing(3, 0, 2),
}));

const LockIcon = styled(LockOutlined)(({ theme }) => ({
  fontSize: 40,
  padding: theme.spacing(1),
  backgroundColor: theme.palette.primary.main,
  color: 'white',
  borderRadius: '50%',
  marginBottom: theme.spacing(2),
}));

const Login = () => {
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
    <Root>
      <Container component="main" maxWidth="xs">
        <StyledPaper elevation={3}>
          <Box display="flex" flexDirection="column" alignItems="center">
            <LockIcon />
            <Typography component="h1" variant="h5">
              CryptaNet
            </Typography>
            <Typography variant="subtitle1" color="textSecondary" gutterBottom>
              Privacy-Preserving & Explainable AI for Supply Chain
            </Typography>
          </Box>

          <Form onSubmit={handleSubmit}>
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
            <SubmitButton
              type="submit"
              fullWidth
              variant="contained"
              color="primary"
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Sign In'}
            </SubmitButton>
          </Form>

          <Snackbar open={!!error} autoHideDuration={6000} onClose={handleCloseSnackbar}>
            <Alert onClose={handleCloseSnackbar} severity="error">
              {error}
            </Alert>
          </Snackbar>
        </StyledPaper>
      </Container>
    </Root>
  );
};

export default Login;