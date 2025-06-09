// Test script to verify frontend API integration
const axios = require('axios');

async function testAnomalyAPI() {
  try {
    console.log('Testing frontend API integration...');
    
    // Test the analytics endpoint
    const response = await axios.get('http://localhost:5004/api/analytics/anomalies');
    
    console.log('✅ API Response Status:', response.status);
    console.log('✅ API Response Data Type:', typeof response.data);
    console.log('✅ Anomalies Array Length:', response.data.anomalies?.length || 0);
    
    if (response.data.anomalies && response.data.anomalies.length > 0) {
      console.log('✅ First Anomaly Sample:');
      console.log(JSON.stringify(response.data.anomalies[0], null, 2));
      
      // Test the transformation logic
      const anomaly = response.data.anomalies[0];
      const severityMap = {
        'high': 0.8,
        'medium': 0.5,
        'low': 0.2,
        'critical': 0.9
      };
      
      const severity = (anomaly.severity || 'medium').toLowerCase();
      const anomalyScore = severityMap[severity] || 0.5;
      
      console.log('✅ Transformed Anomaly:');
      console.log({
        id: anomaly.index,
        productId: anomaly.product_id,
        severity: anomaly.severity,
        temperature: anomaly.temperature,
        humidity: anomaly.humidity,
        anomalyScore: anomalyScore,
        reasons: anomaly.reasons
      });
    }
    
  } catch (error) {
    console.error('❌ API Test Failed:', error.message);
    console.error('❌ Error Details:', error.response?.data || error.code);
  }
}

testAnomalyAPI();
