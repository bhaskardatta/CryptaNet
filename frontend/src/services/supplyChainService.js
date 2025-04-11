import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

export const supplyChainService = {
  /**
   * Query supply chain data based on parameters
   * @param {string} organizationId - Organization ID
   * @param {string} dataType - Type of data to query
   * @param {string} startTime - Start time for query range
   * @param {string} endTime - End time for query range
   * @param {boolean} includeAnomaliesOnly - Whether to include only anomalies
   * @returns {Promise} - Promise with query results
   */
  async queryData(organizationId, dataType, startTime, endTime, includeAnomaliesOnly = false) {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.get(`${API_URL}/supply-chain/query`, {
        params: {
          organizationId,
          dataType,
          startTime,
          endTime,
          includeAnomaliesOnly
        },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Submit supply chain data to the blockchain
   * @param {Object} data - Supply chain data to submit
   * @param {string} organizationId - Organization ID
   * @param {string} dataType - Type of data being submitted
   * @param {Object} accessControl - Access control settings
   * @returns {Promise} - Promise with submission result
   */
  async submitData(data, organizationId, dataType, accessControl = {}) {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.post(`${API_URL}/supply-chain/submit`, {
        data,
        organizationId,
        dataType,
        accessControl
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Retrieve specific supply chain data by ID
   * @param {string} dataId - ID of the data to retrieve
   * @param {string} organizationId - Organization ID
   * @returns {Promise} - Promise with retrieved data
   */
  async retrieveData(dataId, organizationId) {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.get(`${API_URL}/supply-chain/retrieve/${dataId}`, {
        params: {
          organizationId
        },
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  /**
   * Verify the integrity of supply chain data on the blockchain
   * @param {string} dataId - ID of the data to verify
   * @returns {Promise} - Promise with verification result
   */
  async verifyDataIntegrity(dataId) {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.get(`${API_URL}/supply-chain/verify/${dataId}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};