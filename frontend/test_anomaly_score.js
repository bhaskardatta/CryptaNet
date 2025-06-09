// Test script to verify anomaly score formatting works correctly

// Utility function to safely format anomaly scores
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

// Test cases
console.log('🧪 Testing Anomaly Score Formatting...\n');

const testCases = [
  { input: 0.8750, expected: '0.8750', description: 'Number input' },
  { input: '0.8750', expected: '0.8750', description: 'String number input' },
  { input: 'invalid', expected: '0.0000', description: 'Invalid string input' },
  { input: null, expected: '0.0000', description: 'Null input' },
  { input: undefined, expected: '0.0000', description: 'Undefined input' },
  { input: NaN, expected: '0.0000', description: 'NaN input' },
  { input: Infinity, expected: '0.0000', description: 'Infinity input' },
  { input: 1.23456789, expected: '1.2346', description: 'High precision number' },
];

let passedTests = 0;
let totalTests = testCases.length;

testCases.forEach((testCase, index) => {
  const result = formatAnomalyScore(testCase.input);
  const passed = result === testCase.expected;
  
  console.log(`Test ${index + 1}: ${testCase.description}`);
  console.log(`  Input: ${testCase.input} (${typeof testCase.input})`);
  console.log(`  Expected: ${testCase.expected}`);
  console.log(`  Actual: ${result}`);
  console.log(`  Status: ${passed ? '✅ PASS' : '❌ FAIL'}\n`);
  
  if (passed) passedTests++;
});

console.log(`\n📊 Test Results: ${passedTests}/${totalTests} tests passed`);

if (passedTests === totalTests) {
  console.log('🎉 All tests passed! Anomaly score formatting is working correctly.');
} else {
  console.log('⚠️  Some tests failed. Please review the implementation.');
}
