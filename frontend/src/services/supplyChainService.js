import axios from 'axios';
import { API_URL } from '../config';

export const supplyChainService = {
  /**
   * Query supply chain data from the blockchain
   * @param {string} organizationId - Organization ID
   * @param {string} dataType - Type of data to query
   * @param {string} startTime - Start time for query range
   * @param {string} endTime - End time for query range
   * @param {boolean} includeAnomaliesOnly - Whether to include only anomalies
   * @returns {Promise} - Promise with query results
   */
  async queryData(organizationId, dataType, startTime, endTime, includeAnomaliesOnly = false) {
    const token = localStorage.getItem('token');
    console.log('Querying supply chain data with token:', token ? token.substring(0, 10) + '...' : 'none');
    try {
      // Use the correct backend endpoint
      const params = new URLSearchParams();
      if (organizationId) params.append('organizationId', organizationId);
      if (dataType && dataType !== 'all') params.append('dataType', dataType);
      if (startTime) params.append('startTime', startTime);
      if (endTime) params.append('endTime', endTime);
      if (includeAnomaliesOnly) params.append('includeAnomaliesOnly', 'true');

      const response = await axios.get(`${API_URL}/api/supply-chain/query?${params}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      });
      
      console.log('Supply chain data response:', response.data);
      
      // Process the data to ensure all fields are filled
      const results = response.data.results || response.data.data || [];
      const processedResults = results.map(item => {
        // Add product ID if missing
        if (!item.productId && item.data && item.data.product) {
          item.productId = item.data.product;
        }
        
        // Add missing fields with default values
        return {
          ...item,
          id: item.id || Math.floor(Math.random() * 10000),
          productId: item.productId || item.data?.product || 'Unknown Product',
          dataType: item.dataType || 'supply_chain',
          anomalyScore: item.anomalyScore || 0,
          is_anomaly: item.is_anomaly || false,
          risk_level: item.risk_level || 'NORMAL'
        };
      });
      
      // Return the results in the expected format
      return {
        success: true,
        results: processedResults,
        count: processedResults.length,
        total: processedResults.length
      };
    } catch (error) {
      console.error('Error querying supply chain data:', error);
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
      const response = await axios.post(`${API_URL}/api/supply-chain/submit`, {
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
      console.error('Error submitting supply chain data:', error);
      throw error;
    }
  },

  /**
   * Retrieve specific supply chain data by ID
   * @param {string} dataId - Data ID to retrieve
   * @param {string} organizationId - Organization ID
   * @returns {Promise} - Promise with data details
   */
  async retrieveData(dataId, organizationId) {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.get(`${API_URL}/api/supply-chain/retrieve/${dataId}`, {
        params: { organizationId },
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error retrieving supply chain data:', error);
      throw error;
    }
  },

  /**
   * Verify supply chain data on blockchain
   * @param {string} dataId - Data ID to verify
   * @param {string} organizationId - Organization ID
   * @returns {Promise} - Promise with verification result
   */
  async verifyData(dataId, organizationId) {
    const token = localStorage.getItem('token');
    try {
      const response = await axios.get(`${API_URL}/api/supply-chain/verify/${dataId}`, {
        params: { organizationId },
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error verifying supply chain data:', error);
      throw error;
    }
  }
};