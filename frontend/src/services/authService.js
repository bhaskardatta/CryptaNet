import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5004/api';

export const authService = {
  /**
   * Login user with username and password
   * @param {string} username - User's username
   * @param {string} password - User's password
   * @returns {Promise} - Promise with user data and token
   */
  async login(username, password) {
    try {
      const response = await axios.post(`${API_URL}/auth/login`, {
        username,
        password,
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Verify if the token is valid
   * @param {string} token - JWT token
   * @returns {Promise} - Promise with user data if token is valid
   */
  async verifyToken(token) {
    try {
      const response = await axios.get(`${API_URL}/auth/verify`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data; // Return full response data
    } catch (error) {
      return false;
    }
  },

  /**
   * Register a new user
   * @param {Object} userData - User registration data
   * @returns {Promise} - Promise with registration result
   */
  async register(userData) {
    try {
      const response = await axios.post(`${API_URL}/auth/register`, userData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Get current user profile
   * @returns {Promise} - Promise with user profile data
   */
  async getProfile() {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.get(`${API_URL}/auth/profile`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },
};