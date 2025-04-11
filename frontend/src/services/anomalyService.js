import axios from 'axios';
import { API_URL } from '../config';

export const anomalyService = {
  // Get anomalies for an organization
  getAnomalies: async (organizationId, params = {}) => {
    try {
      const response = await axios.get(`${API_URL}/api/anomalies/${organizationId}`, { 
        params,
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching anomalies:', error);
      throw error;
    }
  },

  // Get a specific anomaly by ID
  getAnomalyById: async (anomalyId) => {
    try {
      const response = await axios.get(`${API_URL}/api/anomalies/detail/${anomalyId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching anomaly details:', error);
      throw error;
    }
  },

  // Get explanation for an anomaly
  getExplanation: async (anomalyId) => {
    try {
      const response = await axios.get(`${API_URL}/api/anomalies/explanation/${anomalyId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching anomaly explanation:', error);
      throw error;
    }
  },

  // Train the anomaly detection model
  trainModel: async (organizationId, modelConfig) => {
    try {
      const response = await axios.post(
        `${API_URL}/api/anomaly-detection/train`, 
        { organizationId, ...modelConfig },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      return response.data;
    } catch (error) {
      console.error('Error training model:', error);
      throw error;
    }
  },

  // Get model performance metrics
  getModelMetrics: async (organizationId) => {
    try {
      const response = await axios.get(`${API_URL}/api/anomaly-detection/metrics/${organizationId}`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching model metrics:', error);
      throw error;
    }
  },

  // Update anomaly status (e.g., mark as reviewed)
  updateAnomalyStatus: async (anomalyId, status, notes = '') => {
    try {
      const response = await axios.put(
        `${API_URL}/api/anomalies/status/${anomalyId}`,
        { status, notes },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      return response.data;
    } catch (error) {
      console.error('Error updating anomaly status:', error);
      throw error;
    }
  }
};