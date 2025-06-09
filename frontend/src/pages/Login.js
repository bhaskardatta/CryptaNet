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
  Avatar,
  Fade,
  Grow,
  IconButton,
  InputAdornment,
} from '@mui/material';
import { 
  LockOutlined, 
  Person, 
  Security, 
  Visibility, 
  VisibilityOff,
  Shield,
  AccountTree 
} from '@mui/icons-material';
import { login, clearError } from '../store/slices/authSlice';

const Root = styled('div')(({ theme }) => ({
  height: '100vh',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  background: theme.palette.mode === 'dark' 
    ? 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)'
    : 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #667eea 100%)',
  position: 'relative',
  overflow: 'hidden',
  '&::before': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='m36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
  },
}));

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(6),
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  maxWidth: 480,
  width: '100%',
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)'
    : 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%)',
  backdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
  borderRadius: theme.spacing(3),
  boxShadow: theme.palette.mode === 'dark'
    ? '0 16px 48px rgba(0,0,0,0.4)'
    : '0 16px 48px rgba(0,0,0,0.15)',
  position: 'relative',
  zIndex: 1,
}));

const Form = styled('form')(({ theme }) => ({
  width: '100%',
  marginTop: theme.spacing(3),
}));

const GradientButton = styled(Button)(({ theme }) => ({
  background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
  borderRadius: theme.spacing(2),
  border: 0,
  color: 'white',
  height: 56,
  padding: '0 30px',
  boxShadow: '0 6px 20px 2px rgba(102, 126, 234, .3)',
  fontSize: '1.1rem',
  fontWeight: 'bold',
  margin: theme.spacing(3, 0, 2),
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    background: 'linear-gradient(45deg, #764ba2 30%, #667eea 90%)',
    transform: 'translateY(-2px)',
    boxShadow: '0 8px 25px 2px rgba(102, 126, 234, .4)',
  },
  '&:disabled': {
    background: 'linear-gradient(45deg, #ccc 30%, #999 90%)',
    transform: 'none',
    boxShadow: 'none',
  },
}));

const ModernTextField = styled(TextField)(({ theme }) => ({
  '& .MuiOutlinedInput-root': {
    borderRadius: theme.spacing(2),
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
  '& .MuiInputLabel-root': {
    fontWeight: 500,
  },
}));

const Login = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const { loading, error } = useSelector((state) => state.auth);
  const [credentials, setCredentials] = useState({
    username: '',
    password: '',
  });
  const [showPassword, setShowPassword] = useState(false);

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

  const togglePasswordVisibility = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Root>
      <Container component="main" maxWidth="sm">
        <Fade in timeout={1000}>
          <StyledPaper elevation={0}>
            <Grow in timeout={800}>
              <Box display="flex" flexDirection="column" alignItems="center" mb={2}>
                <Avatar sx={{ 
                  width: 80, 
                  height: 80, 
                  mb: 2,
                  background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                  boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)'
                }}>
                  <Shield sx={{ fontSize: 40 }} />
                </Avatar>
                
                <Typography 
                  component="h1" 
                  variant="h3" 
                  fontWeight="bold"
                  sx={{
                    background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
                    backgroundClip: 'text',
                    WebkitBackgroundClip: 'text',
                    WebkitTextFillColor: 'transparent',
                    mb: 1
                  }}
                >
                  CryptaNet
                </Typography>
                
                <Typography 
                  variant="h6" 
                  color="text.secondary" 
                  textAlign="center"
                  sx={{ mb: 1, fontWeight: 500 }}
                >
                  Privacy-Preserving & Explainable AI
                </Typography>
                
                <Typography 
                  variant="body1" 
                  color="text.secondary" 
                  textAlign="center"
                  sx={{ opacity: 0.8 }}
                >
                  Secure Supply Chain Intelligence Platform
                </Typography>

                {/* Feature Icons */}
                <Box display="flex" gap={2} mt={3} mb={2}>
                  <Avatar sx={{ bgcolor: 'rgba(102, 126, 234, 0.1)', color: 'primary.main' }}>
                    <Security />
                  </Avatar>
                  <Avatar sx={{ bgcolor: 'rgba(102, 126, 234, 0.1)', color: 'primary.main' }}>
                    <AccountTree />
                  </Avatar>
                  <Avatar sx={{ bgcolor: 'rgba(102, 126, 234, 0.1)', color: 'primary.main' }}>
                    <LockOutlined />
                  </Avatar>
                </Box>
              </Box>
            </Grow>

            <Form onSubmit={handleSubmit}>
              <ModernTextField
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
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <Person color="action" />
                    </InputAdornment>
                  ),
                }}
              />
              
              <ModernTextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="password"
                label="Password"
                type={showPassword ? 'text' : 'password'}
                id="password"
                autoComplete="current-password"
                value={credentials.password}
                onChange={handleChange}
                InputProps={{
                  startAdornment: (
                    <InputAdornment position="start">
                      <LockOutlined color="action" />
                    </InputAdornment>
                  ),
                  endAdornment: (
                    <InputAdornment position="end">
                      <IconButton
                        aria-label="toggle password visibility"
                        onClick={togglePasswordVisibility}
                        edge="end"
                      >
                        {showPassword ? <VisibilityOff /> : <Visibility />}
                      </IconButton>
                    </InputAdornment>
                  ),
                }}
              />
              
              <GradientButton
                type="submit"
                fullWidth
                variant="contained"
                disabled={loading}
                startIcon={loading ? null : <Security />}
              >
                {loading ? (
                  <Box display="flex" alignItems="center" gap={1}>
                    <CircularProgress size={24} color="inherit" />
                    <span>Authenticating...</span>
                  </Box>
                ) : (
                  'Secure Sign In'
                )}
              </GradientButton>
            </Form>

            <Snackbar 
              open={!!error} 
              autoHideDuration={6000} 
              onClose={handleCloseSnackbar}
              anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
            >
              <Alert 
                onClose={handleCloseSnackbar} 
                severity="error"
                sx={{ 
                  background: 'linear-gradient(135deg, #f44336 0%, #d32f2f 100%)',
                  color: 'white',
                  '& .MuiAlert-icon': { color: 'white' }
                }}
              >
                {error}
              </Alert>
            </Snackbar>
          </StyledPaper>
        </Fade>
      </Container>
    </Root>
  );
};

export default Login;