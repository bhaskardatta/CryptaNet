// Test the frontend anomaly service
const axios = require('axios');

// Simulate the exact call the frontend makes
async function testFrontendService() {
  try {
    console.log('🔍 Testing frontend service logic...');
    
    // 1. Test direct API call
    const response = await axios.get('http://localhost:5004/api/analytics/anomalies', {
      headers: {
        'Content-Type': 'application/json'
      }
    });
    
    console.log('✅ API Response Status:', response.status);
    console.log('✅ API Response Keys:', Object.keys(response.data));
    
    const detectedAnomalies = response.data.anomalies || [];
    console.log('✅ Detected anomalies count:', detectedAnomalies.length);
    
    if (detectedAnomalies.length > 0) {
      console.log('✅ First anomaly structure:');
      const firstAnomaly = detectedAnomalies[0];
      console.log('  - Keys:', Object.keys(firstAnomaly));
      console.log('  - Product ID:', firstAnomaly.product_id);
      console.log('  - Index:', firstAnomaly.index);
      console.log('  - Type:', firstAnomaly.type);
      console.log('  - Severity:', firstAnomaly.severity);
      console.log('  - Scores:', firstAnomaly.scores);
      console.log('  - Algorithms:', firstAnomaly.algorithms);
      
      // 2. Test transformation logic
      console.log('\n🔄 Testing transformation logic...');
      
      const scores = firstAnomaly.scores || {};
      const isolationScore = Math.abs(scores.isolation_forest || 0);
      const svmScore = Math.abs(scores.one_class_svm || 0);
      const dbscanScore = Math.abs(scores.dbscan || 0);
      
      console.log('  - Isolation Score:', isolationScore);
      console.log('  - SVM Score:', svmScore);
      console.log('  - DBSCAN Score:', dbscanScore);
      
      // Normalization
      const normalizeScore = (score) => {
        const absScore = Math.abs(score);
        return Math.min(Math.max(1 / (1 + Math.exp(-absScore * 2)), 0), 1);
      };
      
      const normalizedSvm = normalizeScore(svmScore);
      console.log('  - Normalized SVM:', normalizedSvm);
      
      let anomalyScore = Math.max(normalizeScore(isolationScore), normalizedSvm, normalizeScore(dbscanScore));
      
      if (anomalyScore === 0 || isNaN(anomalyScore) || !isFinite(anomalyScore)) {
        const severityMap = {
          'high': 0.8,
          'medium': 0.5,
          'low': 0.2,
          'critical': 0.9
        };
        anomalyScore = severityMap[firstAnomaly.severity] || 0.5;
      }
      
      console.log('  - Final Anomaly Score:', anomalyScore);
      
      // 3. Test final transformation
      const transformedAnomaly = {
        id: firstAnomaly.index !== undefined ? firstAnomaly.index + 1 : 1,
        productId: firstAnomaly.product_id,
        dataType: firstAnomaly.type === 'ml_based' ? 'supply_chain_ml' : 'environmental',
        timestamp: firstAnomaly.timestamp,
        anomalyScore: anomalyScore,
        severity: firstAnomaly.severity,
        temperature: firstAnomaly.temperature,
        humidity: firstAnomaly.humidity
      };
      
      console.log('✅ Transformed anomaly sample:');
      console.log(transformedAnomaly);
    }
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    if (error.response) {
      console.error('❌ Response status:', error.response.status);
      console.error('❌ Response data:', error.response.data);
    }
  }
}

testFrontendService();
