// Manual test of the complete flow
// Run this in the browser console

// Test 1: Direct service call
console.log('🔬 TEST 1: Direct Service Call');
fetch('http://localhost:5004/api/analytics/anomalies')
  .then(response => response.json())
  .then(data => {
    console.log('✅ Direct API Response:', data);
    console.log(`✅ Anomalies count: ${data.anomalies?.length || 0}`);
    console.log('✅ First anomaly:', data.anomalies?.[0]);
  })
  .catch(error => {
    console.error('❌ Direct API Error:', error);
  });

// Test 2: Service transformation
console.log('🔬 TEST 2: Service Transformation');
import('./services/anomalyService.js').then(({ anomalyService }) => {
  anomalyService.detectAnomalies('Org1MSP', 'all', '', '', 0.5)
    .then(result => {
      console.log('✅ Service Result:', result);
      console.log(`✅ Transformed anomalies: ${result.results?.length || 0}`);
      console.log('✅ First transformed:', result.results?.[0]);
    })
    .catch(error => {
      console.error('❌ Service Error:', error);
    });
});

// Test 3: Redux dispatch (if store is available)
if (window.__REDUX_STORE__) {
  console.log('🔬 TEST 3: Redux Dispatch');
  const store = window.__REDUX_STORE__;
  store.dispatch({
    type: 'anomaly/detectAnomalies/pending'
  });
}
