import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Box,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  LinearProgress,
  CircularProgress,
  Alert,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  IconButton,
  Tooltip,
  Tabs,
  Tab,
  Avatar,
  Fade,
  Grow,
  Badge
} from '@mui/material';
import { styled } from '@mui/material/styles';
import {
  Security,
  Lock,
  Verified,
  Block,
  Visibility,
  VisibilityOff,
  Refresh,
  Info,
  ExpandMore,
  Key,
  Shield,
  AccountTree,
  Storage,
  Timeline,
  VpnKey,
  PolicyOutlined,
  DataUsage,
  Speed,
  Assessment,
  NetworkCheck,
  CellTower,
  Public,
  VerifiedUser,
  AdminPanelSettings
} from '@mui/icons-material';
import axios from 'axios';
import { API_URL } from '../../config';

const Root = styled(Box)(({ theme }) => ({
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

const StyledCard = styled(Card)(({ theme }) => ({
  background: theme.palette.mode === 'dark'
    ? 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)'
    : 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%)',
  backdropFilter: 'blur(20px)',
  border: `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
  borderRadius: theme.spacing(2),
  marginBottom: theme.spacing(3),
  boxShadow: theme.palette.mode === 'dark'
    ? '0 8px 32px rgba(0,0,0,0.3)'
    : '0 8px 32px rgba(0,0,0,0.1)',
  transition: 'all 0.3s ease-in-out',
  '&:hover': {
    transform: 'translateY(-2px)',
    boxShadow: theme.palette.mode === 'dark'
      ? '0 12px 40px rgba(0,0,0,0.4)'
      : '0 12px 40px rgba(0,0,0,0.15)',
  },
}));

const MetricCard = styled(Card)(({ theme }) => ({
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

const BlockchainCard = styled(Card)(({ theme }) => ({
  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  color: 'white',
  borderRadius: theme.spacing(2),
  padding: theme.spacing(2),
  height: '100%',
  transition: 'all 0.3s ease-in-out',
  cursor: 'pointer',
  boxShadow: '0 8px 32px rgba(102, 126, 234, 0.3)',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: '0 12px 40px rgba(102, 126, 234, 0.4)',
  },
}));

const PrivacyCard = styled(Card)(({ theme }) => ({
  background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  color: 'white',
  borderRadius: theme.spacing(2),
  padding: theme.spacing(2),
  height: '100%',
  transition: 'all 0.3s ease-in-out',
  cursor: 'pointer',
  boxShadow: '0 8px 32px rgba(240, 147, 251, 0.3)',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: '0 12px 40px rgba(240, 147, 251, 0.4)',
  },
}));

const SecurityCard = styled(Card)(({ theme }) => ({
  background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  color: 'white',
  borderRadius: theme.spacing(2),
  padding: theme.spacing(2),
  height: '100%',
  transition: 'all 0.3s ease-in-out',
  cursor: 'pointer',
  boxShadow: '0 8px 32px rgba(79, 172, 254, 0.3)',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: '0 12px 40px rgba(79, 172, 254, 0.4)',
  },
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

const ModernTabs = styled(Tabs)(({ theme }) => ({
  marginBottom: theme.spacing(3),
  '& .MuiTabs-indicator': {
    background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)',
    height: 3,
    borderRadius: '3px 3px 0 0',
  },
  '& .MuiTab-root': {
    borderRadius: '8px 8px 0 0',
    marginRight: theme.spacing(1),
    transition: 'all 0.3s ease-in-out',
    '&:hover': {
      background: theme.palette.mode === 'dark'
        ? 'rgba(255,255,255,0.05)'
        : 'rgba(255,255,255,0.1)',
    },
    '&.Mui-selected': {
      background: theme.palette.mode === 'dark'
        ? 'rgba(255,255,255,0.1)'
        : 'rgba(255,255,255,0.2)',
    },
  },
}));

function TabPanel({ children, value, index, ...other }) {
  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`blockchain-privacy-tabpanel-${index}`}
      aria-labelledby={`blockchain-privacy-tab-${index}`}
      {...other}
    >
      {value === index && <Box sx={{ p: 3 }}>{children}</Box>}
    </div>
  );
}

const BlockchainPrivacy = () => {
  const [loading, setLoading] = useState(true);
  const [blockchainData, setBlockchainData] = useState(null);
  const [privacyData, setPrivacyData] = useState(null);
  const [selectedTransaction, setSelectedTransaction] = useState(null);
  const [dialogOpen, setDialogOpen] = useState(false);
  const [encryptionDialogOpen, setEncryptionDialogOpen] = useState(false);
  const [tabValue, setTabValue] = useState(0);
  const [encryptionInput, setEncryptionInput] = useState('');
  const [encryptionResult, setEncryptionResult] = useState('');
  const [decryptionInput, setDecryptionInput] = useState('');
  const [decryptionResult, setDecryptionResult] = useState('');
  const [lastUpdated, setLastUpdated] = useState(new Date());

  const fetchBlockchainData = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Simulate blockchain data - in a real app, this would come from your blockchain API
      const blockchainResponse = {
        networkStatus: 'healthy',
        totalBlocks: 1247,
        totalTransactions: 3456,
        consensusNodes: 4,
        activeChannels: 2,
        networkLatency: '45ms',
        throughput: '250 TPS',
        recentBlocks: [
          {
            blockNumber: 1247,
            hash: '0x7c9f4b2e8a3d5c6e9f1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e',
            timestamp: new Date(Date.now() - 60000).toISOString(),
            transactions: 12,
            validator: 'peer0.org1.example.com'
          },
          {
            blockNumber: 1246,
            hash: '0x6b8e3a1d7c2f5b9e8a4d6c1f3b7a9e2d5c8f1a4b6e9d2f5a8c1e4b7d0f3a6c9e',
            timestamp: new Date(Date.now() - 120000).toISOString(),
            transactions: 8,
            validator: 'peer0.org2.example.com'
          },
          {
            blockNumber: 1245,
            hash: '0x5a7d2c9f6b1e4a8d3c7f0b9e5a2d8c6f1b4e7a0d3c9f6b2e5a8d1c4f7b0e3a6d',
            timestamp: new Date(Date.now() - 180000).toISOString(),
            transactions: 15,
            validator: 'peer0.org3.example.com'
          }
        ],
        channels: [
          {
            name: 'supplychainchannel',
            organizations: ['Org1MSP', 'Org2MSP', 'Org3MSP'],
            status: 'active',
            blockHeight: 1247
          },
          {
            name: 'privacychannel',
            organizations: ['Org1MSP', 'Org2MSP'],
            status: 'active',
            blockHeight: 892
          }
        ]
      };

      setBlockchainData(blockchainResponse);
      setLastUpdated(new Date());
    } catch (error) {
      console.error('Error fetching blockchain data:', error);
    }
  };

  const fetchPrivacyData = async () => {
    try {
      const token = localStorage.getItem('token');
      
      // Simulate privacy data - in a real app, this would come from your privacy API
      const privacyResponse = {
        encryptionStatus: 'active',
        totalEncryptedRecords: 2834,
        encryptionLevel: 'AES-256',
        zkProofsGenerated: 1456,
        privacyCompliance: 'GDPR',
        dataRetentionPeriod: '90 days',
        accessControls: {
          publicData: 12,
          organizationData: 2134,
          privateData: 688
        },
        encryptionMetrics: {
          encryptionTime: '2.3ms',
          decryptionTime: '1.8ms',
          keyRotationInterval: '30 days',
          lastKeyRotation: new Date(Date.now() - 15 * 24 * 60 * 60 * 1000).toISOString()
        },
        recentActivities: [
          {
            action: 'Data Encrypted',
            timestamp: new Date(Date.now() - 30000).toISOString(),
            dataType: 'Supply Chain Record',
            recordId: 'SC-2024-001234'
          },
          {
            action: 'ZK Proof Generated',
            timestamp: new Date(Date.now() - 90000).toISOString(),
            dataType: 'Temperature Verification',
            recordId: 'SC-2024-001233'
          },
          {
            action: 'Access Control Updated',
            timestamp: new Date(Date.now() - 150000).toISOString(),
            dataType: 'Organization Settings',
            recordId: 'AC-2024-000456'
          }
        ]
      };

      setPrivacyData(privacyResponse);
    } catch (error) {
      console.error('Error fetching privacy data:', error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      await Promise.all([fetchBlockchainData(), fetchPrivacyData()]);
      setLoading(false);
    };

    fetchData();
    const interval = setInterval(fetchData, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleTransactionClick = (transaction) => {
    setSelectedTransaction(transaction);
    setDialogOpen(true);
  };

  const handleEncryptData = async () => {
    if (!encryptionInput.trim()) return;

    try {
      // Simulate encryption - in a real app, this would call your encryption API
      const mockEncrypted = btoa(encryptionInput + '_encrypted_' + Date.now());
      setEncryptionResult(mockEncrypted);
    } catch (error) {
      console.error('Encryption error:', error);
    }
  };

  const handleDecryptData = async () => {
    if (!decryptionInput.trim()) return;

    try {
      // Simulate decryption - in a real app, this would call your decryption API
      const mockDecrypted = atob(decryptionInput).split('_encrypted_')[0];
      setDecryptionResult(mockDecrypted);
    } catch (error) {
      setDecryptionResult('Invalid encrypted data');
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'healthy':
      case 'active':
        return 'success';
      case 'degraded':
        return 'warning';
      case 'unhealthy':
        return 'error';
      default:
        return 'default';
    }
  };

  if (loading) {
    return (
      <Root>
        <Fade in>
          <StyledCard>
            <Box 
              display="flex" 
              flexDirection="column" 
              alignItems="center" 
              justifyContent="center" 
              py={6}
            >
              <CircularProgress size={60} sx={{ mb: 2 }} />
              <Typography variant="h6" color="text.secondary">
                Loading blockchain & privacy data...
              </Typography>
              <Typography variant="body2" color="text.secondary" textAlign="center" sx={{ mt: 1 }}>
                Connecting to secure networks and privacy layers
              </Typography>
            </Box>
          </StyledCard>
        </Fade>
      </Root>
    );
  }

  return (
    <Root>
      <Fade in timeout={800}>
        <HeaderSection>
          <Box display="flex" alignItems="center" mb={2}>
            <Avatar sx={{ 
              bgcolor: 'primary.main', 
              mr: 2, 
              width: 56, 
              height: 56,
              background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)'
            }}>
              <Shield fontSize="large" />
            </Avatar>
            <Box>
              <Typography variant="h4" component="h1" fontWeight="bold" color="primary">
                Blockchain & Privacy Control Center
              </Typography>
              <Typography variant="subtitle1" color="text.secondary">
                Monitor blockchain network health and privacy layer security
              </Typography>
            </Box>
            <Box ml="auto">
              <GradientButton
                startIcon={<Refresh />}
                onClick={() => {
                  setLoading(true);
                  Promise.all([fetchBlockchainData(), fetchPrivacyData()]).then(() => setLoading(false));
                }}
              >
                Refresh Data
              </GradientButton>
            </Box>
          </Box>
          
          <Grid container spacing={3} sx={{ mt: 2 }}>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard>
                <Box display="flex" alignItems="center">
                  <NetworkCheck sx={{ color: '#667eea', mr: 2 }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {blockchainData?.networkStatus === 'healthy' ? 'Healthy' : blockchainData?.networkStatus}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Network Status
                    </Typography>
                  </Box>
                </Box>
              </MetricCard>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard>
                <Box display="flex" alignItems="center">
                  <CellTower sx={{ color: '#764ba2', mr: 2 }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {blockchainData?.consensusNodes || 4}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Active Nodes
                    </Typography>
                  </Box>
                </Box>
              </MetricCard>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard>
                <Box display="flex" alignItems="center">
                  <Speed sx={{ color: '#f44336', mr: 2 }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {blockchainData?.throughput || '250 TPS'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Throughput
                    </Typography>
                  </Box>
                </Box>
              </MetricCard>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <MetricCard>
                <Box display="flex" alignItems="center">
                  <VerifiedUser sx={{ color: '#2196f3', mr: 2 }} />
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      {privacyData?.encryptionLevel || 'AES-256'}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Encryption Level
                    </Typography>
                  </Box>
                </Box>
              </MetricCard>
            </Grid>
          </Grid>
        </HeaderSection>
      </Fade>

      <ModernTabs value={tabValue} onChange={handleTabChange}>
        <Tab 
          label="🔗 Blockchain Network" 
          icon={<Block />} 
          iconPosition="start"
        />
        <Tab 
          label="🔐 Privacy Layer" 
          icon={<Security />} 
          iconPosition="start"
        />
        <Tab 
          label="🛡️ Security Tools" 
          icon={<AdminPanelSettings />} 
          iconPosition="start"
        />
      </ModernTabs>

      <TabPanel value={tabValue} index={0}>
        {/* Blockchain Overview */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={3}>
            <BlockchainCard>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h6">Network Status</Typography>
                    <Typography variant="h4">{blockchainData?.networkStatus}</Typography>
                  </Box>
                  <Verified fontSize="large" />
                </Box>
              </CardContent>
            </BlockchainCard>
          </Grid>
          <Grid item xs={12} md={3}>
            <BlockchainCard>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h6">Total Blocks</Typography>
                    <Typography variant="h4">{blockchainData?.totalBlocks}</Typography>
                  </Box>
                  <Block fontSize="large" />
                </Box>
              </CardContent>
            </BlockchainCard>
          </Grid>
          <Grid item xs={12} md={3}>
            <BlockchainCard>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h6">Transactions</Typography>
                    <Typography variant="h4">{blockchainData?.totalTransactions}</Typography>
                  </Box>
                  <AccountTree fontSize="large" />
                </Box>
              </CardContent>
            </BlockchainCard>
          </Grid>
          <Grid item xs={12} md={3}>
            <BlockchainCard>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h6">Throughput</Typography>
                    <Typography variant="h4">{blockchainData?.throughput}</Typography>
                  </Box>
                  <Timeline fontSize="large" />
                </Box>
              </CardContent>
            </BlockchainCard>
          </Grid>
        </Grid>

        {/* Network Details */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <StyledCard>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <Storage sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Network Details
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">Consensus Nodes</Typography>
                    <Typography variant="h6">{blockchainData?.consensusNodes}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">Active Channels</Typography>
                    <Typography variant="h6">{blockchainData?.activeChannels}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">Network Latency</Typography>
                    <Typography variant="h6">{blockchainData?.networkLatency}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">Last Updated</Typography>
                    <Typography variant="h6">{lastUpdated.toLocaleTimeString()}</Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </StyledCard>
          </Grid>

          <Grid item xs={12} md={6}>
            <StyledCard>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Channels
                </Typography>
                {blockchainData?.channels?.map((channel, index) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Box display="flex" justifyContent="space-between" alignItems="center">
                      <Typography variant="subtitle1">{channel.name}</Typography>
                      <Chip 
                        label={channel.status} 
                        color={getStatusColor(channel.status)}
                        size="small"
                      />
                    </Box>
                    <Typography variant="body2" color="textSecondary">
                      Organizations: {channel.organizations.join(', ')}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      Block Height: {channel.blockHeight}
                    </Typography>
                  </Box>
                ))}
              </CardContent>
            </StyledCard>
          </Grid>
        </Grid>

        {/* Recent Blocks */}
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12}>
            <StyledCard>
              <CardContent>
                <Box display="flex" alignItems="center" mb={3}>
                  <Avatar sx={{ 
                    bgcolor: 'primary.main', 
                    mr: 2,
                    width: 48,
                    height: 48,
                    background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)'
                  }}>
                    <Timeline />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      Recent Blockchain Activity
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Latest blocks and transactions on the network
                    </Typography>
                  </Box>
                  <Box ml="auto">
                    <Chip 
                      icon={<NetworkCheck />}
                      label="Live Data" 
                      color="success"
                      variant="outlined"
                      sx={{ 
                        animation: 'pulse 2s infinite',
                        '@keyframes pulse': {
                          '0%': { opacity: 1 },
                          '50%': { opacity: 0.7 },
                          '100%': { opacity: 1 }
                        }
                      }}
                    />
                  </Box>
                </Box>
                
                <TableContainer component={Paper} sx={{ 
                  background: 'transparent',
                  boxShadow: 'none'
                }}>
                  <Table>
                    <TableHead>
                      <TableRow sx={{ 
                        '& .MuiTableCell-head': { 
                          fontWeight: 'bold',
                          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                          color: 'white'
                        }
                      }}>
                        <TableCell>🧱 Block #</TableCell>
                        <TableCell>🔗 Hash</TableCell>
                        <TableCell>📊 Transactions</TableCell>
                        <TableCell>⚡ Validator</TableCell>
                        <TableCell>⏰ Timestamp</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {blockchainData?.recentBlocks?.map((block, index) => (
                        <TableRow 
                          key={index} 
                          hover 
                          sx={{ 
                            cursor: 'pointer',
                            transition: 'all 0.3s ease-in-out',
                            '&:hover': {
                              backgroundColor: (theme) => theme.palette.mode === 'dark' 
                                ? 'rgba(255,255,255,0.05)' 
                                : 'rgba(102, 126, 234, 0.08)',
                              transform: 'scale(1.01)'
                            }
                          }}
                          onClick={() => handleTransactionClick(block)}
                        >
                          <TableCell>
                            <Box display="flex" alignItems="center">
                              <Chip 
                                label={block.blockNumber} 
                                size="small" 
                                color="primary"
                                sx={{ fontWeight: 'bold' }}
                              />
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Tooltip title={block.hash} arrow>
                              <Box sx={{ 
                                fontFamily: 'monospace',
                                fontSize: '0.85rem',
                                color: 'text.secondary'
                              }}>
                                {block.hash.substring(0, 20)}...
                              </Box>
                            </Tooltip>
                          </TableCell>
                          <TableCell>
                            <Badge badgeContent={block.transactions} color="primary">
                              <AccountTree color="action" />
                            </Badge>
                          </TableCell>
                          <TableCell>
                            <Chip 
                              label={block.validator.split('.')[0]} 
                              size="small" 
                              variant="outlined"
                              color="secondary"
                            />
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" color="text.secondary">
                              {new Date(block.timestamp).toLocaleString()}
                            </Typography>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </StyledCard>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={1}>
        {/* Privacy Overview */}
        <Grid container spacing={3} sx={{ mb: 3 }}>
          <Grid item xs={12} md={3}>
            <PrivacyCard>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h6">Encryption Status</Typography>
                    <Typography variant="h4">{privacyData?.encryptionStatus}</Typography>
                  </Box>
                  <Lock fontSize="large" />
                </Box>
              </CardContent>
            </PrivacyCard>
          </Grid>
          <Grid item xs={12} md={3}>
            <PrivacyCard>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h6">Encrypted Records</Typography>
                    <Typography variant="h4">{privacyData?.totalEncryptedRecords}</Typography>
                  </Box>
                  <Security fontSize="large" />
                </Box>
              </CardContent>
            </PrivacyCard>
          </Grid>
          <Grid item xs={12} md={3}>
            <PrivacyCard>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h6">ZK Proofs</Typography>
                    <Typography variant="h4">{privacyData?.zkProofsGenerated}</Typography>
                  </Box>
                  <Shield fontSize="large" />
                </Box>
              </CardContent>
            </PrivacyCard>
          </Grid>
          <Grid item xs={12} md={3}>
            <PrivacyCard>
              <CardContent>
                <Box display="flex" alignItems="center" justifyContent="space-between">
                  <Box>
                    <Typography variant="h6">Encryption Level</Typography>
                    <Typography variant="h4">{privacyData?.encryptionLevel}</Typography>
                  </Box>
                  <Key fontSize="large" />
                </Box>
              </CardContent>
            </PrivacyCard>
          </Grid>
        </Grid>

        {/* Privacy Details */}
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <StyledCard>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Access Control Distribution
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={4}>
                    <Box textAlign="center">
                      <Typography variant="h4" color="primary">{privacyData?.accessControls?.publicData}</Typography>
                      <Typography variant="body2">Public Data</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={4}>
                    <Box textAlign="center">
                      <Typography variant="h4" color="warning.main">{privacyData?.accessControls?.organizationData}</Typography>
                      <Typography variant="body2">Organization Data</Typography>
                    </Box>
                  </Grid>
                  <Grid item xs={4}>
                    <Box textAlign="center">
                      <Typography variant="h4" color="error.main">{privacyData?.accessControls?.privateData}</Typography>
                      <Typography variant="body2">Private Data</Typography>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </StyledCard>
          </Grid>

          <Grid item xs={12} md={6}>
            <StyledCard>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Encryption Metrics
                </Typography>
                <Grid container spacing={2}>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">Encryption Time</Typography>
                    <Typography variant="h6">{privacyData?.encryptionMetrics?.encryptionTime}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">Decryption Time</Typography>
                    <Typography variant="h6">{privacyData?.encryptionMetrics?.decryptionTime}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">Key Rotation</Typography>
                    <Typography variant="h6">{privacyData?.encryptionMetrics?.keyRotationInterval}</Typography>
                  </Grid>
                  <Grid item xs={6}>
                    <Typography variant="body2" color="textSecondary">Last Rotation</Typography>
                    <Typography variant="h6">
                      {new Date(privacyData?.encryptionMetrics?.lastKeyRotation).toLocaleDateString()}
                    </Typography>
                  </Grid>
                </Grid>
              </CardContent>
            </StyledCard>
          </Grid>
        </Grid>

        {/* Recent Privacy Activities */}
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12}>
            <StyledCard>
              <CardContent>
                <Box display="flex" alignItems="center" mb={3}>
                  <Avatar sx={{ 
                    bgcolor: 'primary.main', 
                    mr: 2,
                    width: 48,
                    height: 48,
                    background: 'linear-gradient(45deg, #f093fb 30%, #f5576c 90%)'
                  }}>
                    <Security />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      Recent Privacy Activities
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Monitor all privacy-related operations and compliance activities
                    </Typography>
                  </Box>
                  <Box ml="auto">
                    <Chip 
                      icon={<Shield />}
                      label="Secure" 
                      color="success"
                      variant="outlined"
                    />
                  </Box>
                </Box>
                
                <TableContainer component={Paper} sx={{ 
                  background: 'transparent',
                  boxShadow: 'none'
                }}>
                  <Table>
                    <TableHead>
                      <TableRow sx={{ 
                        '& .MuiTableCell-head': { 
                          fontWeight: 'bold',
                          background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                          color: 'white'
                        }
                      }}>
                        <TableCell>🔐 Action</TableCell>
                        <TableCell>📋 Data Type</TableCell>
                        <TableCell>🆔 Record ID</TableCell>
                        <TableCell>⏰ Timestamp</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {privacyData?.recentActivities?.map((activity, index) => (
                        <TableRow 
                          key={index} 
                          hover
                          sx={{ 
                            transition: 'all 0.3s ease-in-out',
                            '&:hover': {
                              backgroundColor: (theme) => theme.palette.mode === 'dark' 
                                ? 'rgba(255,255,255,0.05)' 
                                : 'rgba(240, 147, 251, 0.08)',
                              transform: 'scale(1.01)'
                            }
                          }}
                        >
                          <TableCell>
                            <Chip 
                              label={activity.action} 
                              size="small" 
                              variant="outlined"
                              color={
                                activity.action.includes('Encrypted') ? 'success' :
                                activity.action.includes('ZK Proof') ? 'info' :
                                activity.action.includes('Access') ? 'warning' : 'default'
                              }
                              icon={
                                activity.action.includes('Encrypted') ? <Lock /> :
                                activity.action.includes('ZK Proof') ? <VerifiedUser /> :
                                activity.action.includes('Access') ? <AdminPanelSettings /> : <Security />
                              }
                            />
                          </TableCell>
                          <TableCell>
                            <Box display="flex" alignItems="center">
                              <DataUsage sx={{ mr: 1, color: 'text.secondary' }} />
                              <Typography variant="body2">
                                {activity.dataType}
                              </Typography>
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Box sx={{ 
                              fontFamily: 'monospace',
                              fontSize: '0.85rem',
                              color: 'primary.main',
                              fontWeight: 'bold'
                            }}>
                              {activity.recordId}
                            </Box>
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" color="text.secondary">
                              {new Date(activity.timestamp).toLocaleString()}
                            </Typography>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </StyledCard>
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={tabValue} index={2}>
        {/* Security Tools */}
        <Grow in timeout={600}>
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <SecurityCard>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Avatar sx={{ 
                      bgcolor: 'rgba(255,255,255,0.2)', 
                      mr: 2,
                      width: 48,
                      height: 48 
                    }}>
                      <Lock />
                    </Avatar>
                    <Box>
                      <Typography variant="h6" color="white" fontWeight="bold">
                        Data Encryption Tool
                      </Typography>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                        Secure your sensitive data with AES-256 encryption
                      </Typography>
                    </Box>
                  </Box>
                  <ModernTextField
                    fullWidth
                    multiline
                    rows={4}
                    label="Data to Encrypt"
                    value={encryptionInput}
                    onChange={(e) => setEncryptionInput(e.target.value)}
                    sx={{ mb: 2 }}
                    placeholder="Enter sensitive data to encrypt..."
                  />
                  <GradientButton
                    fullWidth
                    onClick={handleEncryptData}
                    disabled={!encryptionInput.trim()}
                    sx={{ mb: 2 }}
                    startIcon={<Lock />}
                  >
                    🔒 Encrypt Data
                  </GradientButton>
                  {encryptionResult && (
                    <Fade in>
                      <Box>
                        <ModernTextField
                          fullWidth
                          multiline
                          rows={3}
                          label="🔐 Encrypted Result"
                          value={encryptionResult}
                          InputProps={{ readOnly: true }}
                        />
                        <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)', mt: 1, display: 'block' }}>
                          ✅ Data encrypted successfully with AES-256
                        </Typography>
                      </Box>
                    </Fade>
                  )}
                </CardContent>
              </SecurityCard>
            </Grid>

            <Grid item xs={12} md={6}>
              <PrivacyCard>
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Avatar sx={{ 
                      bgcolor: 'rgba(255,255,255,0.2)', 
                      mr: 2,
                      width: 48,
                      height: 48 
                    }}>
                      <Key />
                    </Avatar>
                    <Box>
                      <Typography variant="h6" color="white" fontWeight="bold">
                        Data Decryption Tool
                      </Typography>
                      <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.8)' }}>
                        Decrypt your secured data with authorized access
                      </Typography>
                    </Box>
                  </Box>
                  <ModernTextField
                    fullWidth
                    multiline
                    rows={4}
                    label="Encrypted Data"
                    value={decryptionInput}
                    onChange={(e) => setDecryptionInput(e.target.value)}
                    sx={{ mb: 2 }}
                    placeholder="Paste encrypted data here..."
                  />
                  <GradientButton
                    fullWidth
                    onClick={handleDecryptData}
                    disabled={!decryptionInput.trim()}
                    sx={{ mb: 2 }}
                    startIcon={<Key />}
                  >
                    🔓 Decrypt Data
                  </GradientButton>
                  {decryptionResult && (
                    <Fade in>
                      <Box>
                        <ModernTextField
                          fullWidth
                          multiline
                          rows={3}
                          label="🔓 Decrypted Result"
                          value={decryptionResult}
                          InputProps={{ readOnly: true }}
                        />
                        <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)', mt: 1, display: 'block' }}>
                          {decryptionResult === 'Invalid encrypted data' ? '❌ Invalid encrypted data format' : '✅ Data decrypted successfully'}
                        </Typography>
                      </Box>
                    </Fade>
                  )}
                </CardContent>
              </PrivacyCard>
            </Grid>
          </Grid>
        </Grow>

        {/* Privacy Compliance */}
        <Grid container spacing={3} sx={{ mt: 1 }}>
          <Grid item xs={12}>
            <StyledCard>
              <CardContent>
                <Box display="flex" alignItems="center" mb={3}>
                  <Avatar sx={{ 
                    bgcolor: 'primary.main', 
                    mr: 2,
                    width: 48,
                    height: 48,
                    background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)'
                  }}>
                    <Shield />
                  </Avatar>
                  <Box>
                    <Typography variant="h6" fontWeight="bold">
                      Privacy Compliance Dashboard
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Monitor compliance with global privacy regulations
                    </Typography>
                  </Box>
                </Box>
                
                <Grid container spacing={3}>
                  <Grid item xs={12} md={4}>
                    <Box 
                      sx={{ 
                        textAlign: 'center', 
                        p: 3,
                        background: 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)',
                        borderRadius: 2,
                        color: 'white',
                        transition: 'all 0.3s ease-in-out',
                        '&:hover': { transform: 'translateY(-2px)' }
                      }}
                    >
                      <VerifiedUser sx={{ fontSize: 40, mb: 1 }} />
                      <Typography variant="h6" fontWeight="bold">GDPR Compliant</Typography>
                      <Typography variant="body2" sx={{ opacity: 0.9, mt: 1 }}>
                        Data retention: {privacyData?.dataRetentionPeriod}
                      </Typography>
                      <Box sx={{ mt: 2 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={100} 
                          sx={{ 
                            backgroundColor: 'rgba(255,255,255,0.3)',
                            '& .MuiLinearProgress-bar': { backgroundColor: 'rgba(255,255,255,0.8)' }
                          }} 
                        />
                        <Typography variant="caption" sx={{ mt: 0.5, display: 'block' }}>
                          100% Compliant
                        </Typography>
                      </Box>
                    </Box>
                  </Grid>
                  
                  <Grid item xs={12} md={4}>
                    <Box 
                      sx={{ 
                        textAlign: 'center', 
                        p: 3,
                        background: 'linear-gradient(135deg, #2196F3 0%, #1976D2 100%)',
                        borderRadius: 2,
                        color: 'white',
                        transition: 'all 0.3s ease-in-out',
                        '&:hover': { transform: 'translateY(-2px)' }
                      }}
                    >
                      <PolicyOutlined sx={{ fontSize: 40, mb: 1 }} />
                      <Typography variant="h6" fontWeight="bold">CCPA Compliant</Typography>
                      <Typography variant="body2" sx={{ opacity: 0.9, mt: 1 }}>
                        Right to delete implemented
                      </Typography>
                      <Box sx={{ mt: 2 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={100} 
                          sx={{ 
                            backgroundColor: 'rgba(255,255,255,0.3)',
                            '& .MuiLinearProgress-bar': { backgroundColor: 'rgba(255,255,255,0.8)' }
                          }} 
                        />
                        <Typography variant="caption" sx={{ mt: 0.5, display: 'block' }}>
                          100% Compliant
                        </Typography>
                      </Box>
                    </Box>
                  </Grid>
                  
                  <Grid item xs={12} md={4}>
                    <Box 
                      sx={{ 
                        textAlign: 'center', 
                        p: 3,
                        background: 'linear-gradient(135deg, #FF9800 0%, #F57C00 100%)',
                        borderRadius: 2,
                        color: 'white',
                        transition: 'all 0.3s ease-in-out',
                        '&:hover': { transform: 'translateY(-2px)' }
                      }}
                    >
                      <Assessment sx={{ fontSize: 40, mb: 1 }} />
                      <Typography variant="h6" fontWeight="bold">SOC 2 Type II</Typography>
                      <Typography variant="body2" sx={{ opacity: 0.9, mt: 1 }}>
                        Security controls verified
                      </Typography>
                      <Box sx={{ mt: 2 }}>
                        <LinearProgress 
                          variant="determinate" 
                          value={100} 
                          sx={{ 
                            backgroundColor: 'rgba(255,255,255,0.3)',
                            '& .MuiLinearProgress-bar': { backgroundColor: 'rgba(255,255,255,0.8)' }
                          }} 
                        />
                        <Typography variant="caption" sx={{ mt: 0.5, display: 'block' }}>
                          100% Compliant
                        </Typography>
                      </Box>
                    </Box>
                  </Grid>
                </Grid>

                {/* Additional Compliance Metrics */}
                <Box sx={{ mt: 4 }}>
                  <Typography variant="h6" gutterBottom>
                    Compliance Metrics
                  </Typography>
                  <Grid container spacing={2}>
                    <Grid item xs={12} sm={6} md={3}>
                      <Box sx={{ textAlign: 'center', p: 2 }}>
                        <Typography variant="h4" color="success.main">98.5%</Typography>
                        <Typography variant="body2" color="text.secondary">Data Integrity</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <Box sx={{ textAlign: 'center', p: 2 }}>
                        <Typography variant="h4" color="primary.main">24/7</Typography>
                        <Typography variant="body2" color="text.secondary">Monitoring</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <Box sx={{ textAlign: 'center', p: 2 }}>
                        <Typography variant="h4" color="warning.main">&lt; 2min</Typography>
                        <Typography variant="body2" color="text.secondary">Incident Response</Typography>
                      </Box>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                      <Box sx={{ textAlign: 'center', p: 2 }}>
                        <Typography variant="h4" color="info.main">99.9%</Typography>
                        <Typography variant="body2" color="text.secondary">Uptime SLA</Typography>
                      </Box>
                    </Grid>
                  </Grid>
                </Box>
              </CardContent>
            </StyledCard>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Transaction Details Dialog */}
      <Dialog 
        open={dialogOpen} 
        onClose={() => setDialogOpen(false)} 
        maxWidth="md" 
        fullWidth
        PaperProps={{
          sx: {
            background: (theme) => theme.palette.mode === 'dark'
              ? 'linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)'
              : 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.8) 100%)',
            backdropFilter: 'blur(20px)',
            border: (theme) => `1px solid ${theme.palette.mode === 'dark' ? 'rgba(255,255,255,0.1)' : 'rgba(255,255,255,0.3)'}`,
            borderRadius: 2,
          }
        }}
      >
        <DialogTitle>
          <Box display="flex" alignItems="center">
            <Avatar sx={{ 
              bgcolor: 'primary.main', 
              mr: 2,
              background: 'linear-gradient(45deg, #667eea 30%, #764ba2 90%)'
            }}>
              <Block />
            </Avatar>
            <Box>
              <Typography variant="h6" fontWeight="bold">Block Details</Typography>
              <Typography variant="body2" color="text.secondary">
                Detailed blockchain transaction information
              </Typography>
            </Box>
          </Box>
        </DialogTitle>
        <DialogContent>
          {selectedTransaction && (
            <Grid container spacing={3} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <Box sx={{ 
                  p: 2, 
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  borderRadius: 2,
                  color: 'white',
                  mb: 3
                }}>
                  <Typography variant="h6" align="center">
                    Block #{selectedTransaction.blockNumber}
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Box sx={{ p: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    🧱 Block Number
                  </Typography>
                  <Typography variant="h6" fontWeight="bold">
                    {selectedTransaction.blockNumber}
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Box sx={{ p: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    📊 Transactions Count
                  </Typography>
                  <Typography variant="h6" fontWeight="bold">
                    {selectedTransaction.transactions}
                  </Typography>
                </Box>
              </Grid>
              
              <Grid item xs={12}>
                <Box sx={{ p: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    🔗 Block Hash
                  </Typography>
                  <Box sx={{ 
                    p: 2, 
                    bgcolor: 'background.paper',
                    borderRadius: 1,
                    fontFamily: 'monospace',
                    wordBreak: 'break-all',
                    fontSize: '0.9rem',
                    border: '1px solid',
                    borderColor: 'divider'
                  }}>
                    {selectedTransaction.hash}
                  </Box>
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Box sx={{ p: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    ⚡ Validator Node
                  </Typography>
                  <Chip 
                    label={selectedTransaction.validator} 
                    color="primary" 
                    variant="outlined"
                    sx={{ fontWeight: 'bold' }}
                  />
                </Box>
              </Grid>
              
              <Grid item xs={12} sm={6}>
                <Box sx={{ p: 2 }}>
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    ⏰ Block Timestamp
                  </Typography>
                  <Typography variant="body1" fontWeight="bold">
                    {new Date(selectedTransaction.timestamp).toLocaleString()}
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          )}
        </DialogContent>
        <DialogActions sx={{ p: 3 }}>
          <GradientButton onClick={() => setDialogOpen(false)} startIcon={<Info />}>
            Close Details
          </GradientButton>
        </DialogActions>
      </Dialog>
    </Root>
  );
};

export default BlockchainPrivacy;
