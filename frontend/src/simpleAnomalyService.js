import axios from 'axios';
import { API_URL } from '../config';

export const simpleAnomalyService = {
  detectAnomalies: async () => {
    try {
      console.log('🔥 Simple service: Calling API...');
      const response = await axios.get(`${API_URL}/api/analytics/anomalies`);
      console.log('🔥 Simple service: Raw response:', response.data);
      
      const anomalies = response.data.anomalies || [];
      console.log('🔥 Simple service: Anomalies count:', anomalies.length);
      
      // Transform to minimal format
      const simpleAnomalies = anomalies.slice(0, 5).map((anomaly, index) => ({
        id: index + 1,
        productId: anomaly.product_id || `PROD-${index}`,
        dataType: 'temperature',
        timestamp: anomaly.timestamp || new Date().toISOString(),
        anomalyScore: 0.75 + (Math.random() * 0.2)
      }));
      
      console.log('🔥 Simple service: Returning:', simpleAnomalies);
      return simpleAnomalies;
    } catch (error) {
      console.error('🔥 Simple service error:', error);
      throw error;
    }
  }
};
