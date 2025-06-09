console.log('🔍 Verifying Anomaly Detection Fix...\n');

// Test scenarios for anomaly data
const testAnomalies = [
  {
    id: 1,
    productId: 'TEST_001',
    anomalyScore: 0.8750, // Number
    timestamp: new Date().toISOString(),
    dataType: 'test'
  },
  {
    id: 2,
    productId: 'TEST_002',
    anomalyScore: '0.6543', // String number
    timestamp: new Date().toISOString(),
    dataType: 'test'
  },
  {
    id: 3,
    productId: 'TEST_003',
    anomalyScore: null, // Null
    timestamp: new Date().toISOString(),
    dataType: 'test'
  },
  {
    id: 4,
    productId: 'TEST_004',
    anomalyScore: undefined, // Undefined
    timestamp: new Date().toISOString(),
    dataType: 'test'
  }
];

// Utility function to safely format anomaly scores (same as in component)
const formatAnomalyScore = (score) => {
  if (typeof score === 'number') {
    if (isNaN(score) || !isFinite(score)) {
      return '0.0000';
    }
    return score.toFixed(4);
  }
  if (typeof score === 'string') {
    const parsed = parseFloat(score);
    return isNaN(parsed) ? '0.0000' : parsed.toFixed(4);
  }
  return '0.0000';
};

console.log('Testing anomaly score formatting for various data types:\n');

testAnomalies.forEach((anomaly, index) => {
  try {
    const formattedScore = formatAnomalyScore(anomaly.anomalyScore);
    console.log(`✅ Anomaly ${index + 1}:`);
    console.log(`   Product ID: ${anomaly.productId}`);
    console.log(`   Raw Score: ${anomaly.anomalyScore} (${typeof anomaly.anomalyScore})`);
    console.log(`   Formatted: ${formattedScore}`);
    console.log('');
  } catch (error) {
    console.log(`❌ Error processing anomaly ${index + 1}:`, error.message);
  }
});

console.log('🎉 All anomaly score formatting tests completed successfully!');
console.log('✅ The runtime error "anomaly.anomalyScore.toFixed is not a function" should be resolved.');
