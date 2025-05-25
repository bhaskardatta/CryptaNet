import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { styled } from '@mui/material/styles';
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
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard as DashboardIcon,
  Storage as StorageIcon,
  ShowChart as ShowChartIcon,
  Timeline as TimelineIcon,
  MonitorHeart as MonitorHeartIcon,
  Info as InfoIcon,
  Settings as SettingsIcon,
  ExitToApp as LogoutIcon,
  AccountCircle,
} from '@mui/icons-material';
import { logout } from '../../store/slices/authSlice';

const drawerWidth = 240;

const Root = styled('div')({
  display: 'flex',
});

const StyledAppBar = styled(AppBar)(({ theme }) => ({
  zIndex: theme.zIndex.drawer + 1,
}));

const StyledDrawer = styled(Drawer)({
  width: drawerWidth,
  flexShrink: 0,
  '& .MuiDrawer-paper': {
    width: drawerWidth,
  },
});

const Content = styled('main')(({ theme }) => ({
  flexGrow: 1,
  padding: theme.spacing(3),
}));

const Toolbar2 = styled('div')(({ theme }) => ({
  ...theme.mixins.toolbar,
}));

const Title = styled(Typography)({
  flexGrow: 1,
});

const MenuButton = styled(IconButton)(({ theme }) => ({
  marginRight: theme.spacing(2),
  [theme.breakpoints.up('md')]: {
    display: 'none',
  },
}));

const StyledAvatar = styled(Avatar)(({ theme }) => ({
  cursor: 'pointer',
  backgroundColor: theme.palette.primary.main,
}));

const ActiveListItem = styled(ListItem)(({ theme, active }) => ({
  ...(active && {
    backgroundColor: theme.palette.action.selected,
    '& .MuiListItemIcon-root': {
      color: theme.palette.primary.main,
    },
    '& .MuiListItemText-primary': {
      fontWeight: 'bold',
      color: theme.palette.primary.main,
    },
  }),
}));

const Layout = () => {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { user } = useSelector((state) => state.auth);
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
    { text: 'Real-Time Analytics', icon: <TimelineIcon />, path: '/analytics' },
    { text: 'System Health', icon: <MonitorHeartIcon />, path: '/system-health' },
    { text: 'Explainability', icon: <InfoIcon />, path: '/explainability' },
    { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
  ];

  const drawer = (
    <div>
      <Toolbar2 />
      <Divider />
      <List>
        {menuItems.map((item) => {
          const isActive = location.pathname === item.path;
          return (
            <ActiveListItem
              button
              key={item.text}
              onClick={() => handleNavigation(item.path)}
              active={isActive}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
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
          <div>
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
          </div>
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