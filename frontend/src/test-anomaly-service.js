// Test the frontend anomaly service directly
// This can be run in the browser console to test the integration

console.log('🔍 Testing Frontend Anomaly Service...');

// Test the anomaly service
import { anomalyService } from './services/anomalyService.js';

async function testAnomalyService() {
  try {
    console.log('📡 Calling anomalyService.detectAnomalies...');
    
    const result = await anomalyService.detectAnomalies(
      'Org1MSP',
      'all',
      '',
      '',
      0.5
    );
    
    console.log('✅ Service Response:', result);
    console.log('✅ Success:', result.success);
    console.log('✅ Anomalies Count:', result.results?.length || 0);
    console.log('✅ Message:', result.message);
    
    if (result.results && result.results.length > 0) {
      console.log('✅ First Transformed Anomaly:');
      console.log(result.results[0]);
    }
    
    return result;
  } catch (error) {
    console.error('❌ Service Test Failed:', error);
    throw error;
  }
}

// Run the test
testAnomalyService()
  .then(result => {
    console.log('🎯 Frontend Service Test Complete!');
    console.log(`Found ${result.results?.length || 0} anomalies`);
  })
  .catch(error => {
    console.error('💥 Test Failed:', error);
  });
