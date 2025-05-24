// Configuration for different environments
const configs = {
  development: {
    API_URL: 'http://localhost:5004',
    BLOCKCHAIN_EXPLORER_URL: 'http://localhost:8080',
    DEBUG: true
  },
  test: {
    API_URL: 'http://localhost:5004',
    BLOCKCHAIN_EXPLORER_URL: 'http://localhost:8080',
    DEBUG: true
  },
  production: {
    API_URL: '/api',
    BLOCKCHAIN_EXPLORER_URL: '/explorer',
    DEBUG: false
  }
};

// Determine current environment
const ENV = process.env.REACT_APP_ENV || 'development';

// Export configuration for current environment
export const API_URL = configs[ENV].API_URL;
export const BLOCKCHAIN_EXPLORER_URL = configs[ENV].BLOCKCHAIN_EXPLORER_URL;
export const DEBUG = configs[ENV].DEBUG;

export default configs[ENV];

export const API_CONFIG = {
  BASE_URL: 'http://localhost:5004',
  ENDPOINTS: {
    AUTH: {
      LOGIN: '/api/auth/login',
      LOGOUT: '/api/auth/logout',
      VERIFY: '/api/auth/verify'
    },
    SUPPLY_CHAIN: {
      SUBMIT: '/api/supply-chain/submit',
      QUERY: '/api/supply-chain/query',
      RETRIEVE: '/api/supply-chain/retrieve',
      VERIFY: '/api/supply-chain/verify'
    },
    ANOMALIES: {
      GET: '/api/anomalies',
      DETAIL: '/api/anomalies/detail',
      EXPLANATION: '/api/anomalies/explanation',
      STATUS: '/api/anomalies/status'
    },
    ANALYTICS: {
      SUMMARY: '/api/analytics/summary'
    },
    MODEL: {
      METRICS: '/api/anomaly-detection/metrics',
      TRAIN: '/api/anomaly-detection/train'
    }
  }
};

// Default login credentials for testing
export const DEFAULT_CREDENTIALS = {
  admin: { username: 'admin', password: 'admin123' },
  user1: { username: 'user1', password: 'password123' },
  org2admin: { username: 'org2admin', password: 'org2pass' }
};