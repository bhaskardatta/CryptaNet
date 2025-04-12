// Configuration for different environments
const configs = {
  development: {
    API_URL: 'http://localhost:5001',
    BLOCKCHAIN_EXPLORER_URL: 'http://localhost:8080',
    DEBUG: true
  },
  test: {
    API_URL: 'http://localhost:5001',
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