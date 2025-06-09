import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { styled, alpha } from '@mui/material/styles';
import {
  AppBar,
  Toolbar,
  Typography,
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Divider,
  IconButton,
  Container,
  Menu,
  MenuItem,
  Avatar,
  useMediaQuery,
  useTheme,
  Box,
  Badge,
  Tooltip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Storage as StorageIcon,
  ShowChart as ShowChartIcon,
  Security as SecurityIcon,
  MonitorHeart as MonitorHeartIcon,
  Info as InfoIcon,
  Settings as SettingsIcon,
  ExitToApp as LogoutIcon,
  AccountCircle,
  Brightness4,
  Brightness7,
  NotificationsNone,
} from '@mui/icons-material';
import { logout } from '../../store/slices/authSlice';
import { useTheme as useCustomTheme } from '../../theme/ThemeContext';

const drawerWidth = 240;

const Root = styled('div')(({ theme }) => ({
  display: 'flex',
  minHeight: '100vh',
  backgroundColor: theme.palette.background.default,
}));

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  zIndex: theme.zIndex.drawer + 1,
  background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.primary.dark} 100%)`,
  boxShadow: theme.shadows[8],
  backdropFilter: 'blur(20px)',
}));

const StyledDrawer = styled(Drawer)(({ theme }) => ({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
    backgroundColor: theme.palette.background.paper,
    borderRight: `1px solid ${alpha(theme.palette.divider, 0.12)}`,
    boxShadow: theme.shadows[4],
  },
}));

const Content = styled('main')(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
  backgroundColor: theme.palette.background.default,
  minHeight: '100vh',
}));

const Toolbar2 = styled('div')(({ theme }) => ({
  ...theme.mixins.toolbar,
}));

const Title = styled(Typography)(({ theme }) => ({
  flexGrow: 1,
  fontWeight: 700,
  fontSize: '1.5rem',
  background: `linear-gradient(45deg, ${theme.palette.common.white} 30%, ${alpha(theme.palette.common.white, 0.8)} 90%)`,
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
}));

const MenuButton = styled(IconButton)(({ theme }) => ({
  marginRight: theme.spacing(2),
  [theme.breakpoints.up('md')]: {
    display: 'none',
  },
}));

const StyledAvatar = styled(Avatar)(({ theme }) => ({
  cursor: 'pointer',
  background: `linear-gradient(135deg, ${theme.palette.secondary.main} 0%, ${theme.palette.secondary.dark} 100%)`,
  boxShadow: theme.shadows[4],
  transition: 'all 0.3s ease',
  '&:hover': {
    transform: 'scale(1.1)',
    boxShadow: theme.shadows[8],
  },
}));

const ActiveListItem = styled(ListItem)(({ theme, active }) => ({
  margin: theme.spacing(0.5, 1),
  borderRadius: theme.shape.borderRadius * 2,
  transition: 'all 0.3s ease',
  cursor: 'pointer',
  '&:hover': {
    backgroundColor: alpha(theme.palette.primary.main, 0.08),
    transform: 'translateX(4px)',
  },
  ...(active && {
    backgroundColor: alpha(theme.palette.primary.main, 0.12),
    borderLeft: `4px solid ${theme.palette.primary.main}`,
    '& .MuiListItemIcon-root': {
      color: theme.palette.primary.main,
    },
    '& .MuiListItemText-primary': {
      fontWeight: 600,
      color: theme.palette.primary.main,
    },
  }),
}));

const BrandContainer = styled(Box)(({ theme }) => ({
  padding: theme.spacing(2),
  textAlign: 'center',
  borderBottom: `1px solid ${alpha(theme.palette.divider, 0.12)}`,
  background: `linear-gradient(135deg, ${alpha(theme.palette.primary.main, 0.05)} 0%, ${alpha(theme.palette.secondary.main, 0.05)} 100%)`,
}));

const BrandText = styled(Typography)(({ theme }) => ({
  fontWeight: 700,
  fontSize: '1.25rem',
  background: `linear-gradient(135deg, ${theme.palette.primary.main} 0%, ${theme.palette.secondary.main} 100%)`,
  WebkitBackgroundClip: 'text',
  WebkitTextFillColor: 'transparent',
  backgroundClip: 'text',
}));

const Layout = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { user } = useSelector((state) => state.auth);
  const { mode, toggleMode } = useCustomTheme();
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleMenuClose();
    dispatch(logout());
    navigate('/login');
  };

  const handleNavigation = (path) => {
    navigate(path);
    setMobileOpen(false);
  };

  const menuItems = [
    { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
    { text: 'Supply Chain Data', icon: <StorageIcon />, path: '/supply-chain-data' },
    { text: 'Anomaly Detection', icon: <ShowChartIcon />, path: '/anomaly-detection' },
    { text: 'Blockchain & Privacy', icon: <SecurityIcon />, path: '/blockchain-privacy' },
    { text: 'System Health', icon: <MonitorHeartIcon />, path: '/system-health' },
    { text: 'Explainability', icon: <InfoIcon />, path: '/explainability' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
  ];

  const drawer = (
    <div>
      <BrandContainer>
        <BrandText variant="h6">
          CryptaNet
        </BrandText>
        <Typography variant="caption" color="textSecondary" display="block">
          Secure Analytics Platform
        </Typography>
      </BrandContainer>
      <List sx={{ px: 1, py: 2 }}>
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <ActiveListItem
              button
              key={item.text}
              onClick={() => handleNavigation(item.path)}
              active={isActive}
            >
              <ListItemIcon sx={{ minWidth: 40 }}>{item.icon}</ListItemIcon>
              <ListItemText 
                primary={item.text} 
                primaryTypographyProps={{
                  fontSize: '0.875rem',
                  fontWeight: isActive ? 600 : 400,
                }}
              />
            </ActiveListItem>
          );
        })}
      </List>
    </div>
  );

  return (
    <Root>
      <StyledAppBar position="fixed">
        <Toolbar>
          {isMobile && (
            <MenuButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
            >
              <MenuIcon />
            </MenuButton>
          )}
          <Title variant="h6" noWrap>
            CryptaNet
          </Title>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Tooltip title={`Switch to ${mode === 'light' ? 'dark' : 'light'} mode`}>
              <IconButton
                color="inherit"
                onClick={toggleMode}
                sx={{
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    backgroundColor: alpha(theme.palette.common.white, 0.1),
                    transform: 'rotate(180deg)',
                  },
                }}
              >
                {mode === 'dark' ? <Brightness7 /> : <Brightness4 />}
              </IconButton>
            </Tooltip>
            
            <Tooltip title="Notifications">
              <IconButton color="inherit">
                <Badge badgeContent={3} color="error">
                  <NotificationsNone />
                </Badge>
              </IconButton>
            </Tooltip>

            <IconButton
              edge="end"
              aria-label="account of current user"
              aria-haspopup="true"
              onClick={handleProfileMenuOpen}
              color="inherit"
            >
              {user?.username ? (
                <StyledAvatar>
                  {user.username.charAt(0).toUpperCase()}
                </StyledAvatar>
              ) : (
                <AccountCircle />
              )}
            </IconButton>
          </Box>
          
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorEl)}
            onClose={handleMenuClose}
          >
            <MenuItem disabled>
              {user?.username ? `Logged in as ${user.username}` : 'Profile'}
            </MenuItem>
            <MenuItem onClick={handleLogout}>
              <ListItemIcon>
                <LogoutIcon fontSize="small" />
              </ListItemIcon>
              <ListItemText primary="Logout" />
            </MenuItem>
          </Menu>
        </Toolbar>
      </StyledAppBar>

      {isMobile ? (
        <StyledDrawer
          variant="temporary"
          anchor="left"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true,
          }}
        >
          {drawer}
        </StyledDrawer>
      ) : (
        <StyledDrawer variant="permanent">
          {drawer}
        </StyledDrawer>
      )}

      <Content>
        <Toolbar2 />
        <Container maxWidth="lg">
          <Outlet />
        </Container>
      </Content>
    </Root>
  );
};

export default Layout;