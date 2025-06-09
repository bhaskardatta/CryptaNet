import React from 'react';

const QuickAnomalyTest = () => {
  const [testResult, setTestResult] = React.useState(null);
  const [loading, setLoading] = React.useState(false);

  const testDirectAPI = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5004/api/analytics/anomalies');
      const data = await response.json();
      setTestResult({
        success: true,
        count: data.anomalies?.length || 0,
        totalRecords: data.total_records || 0,
        firstAnomaly: data.anomalies?.[0] || null
      });
    } catch (error) {
      setTestResult({
        success: false,
        error: error.message
      });
    }
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', border: '2px solid #007bff', margin: '20px', borderRadius: '8px' }}>
      <h3>🔍 Quick Anomaly API Test</h3>
      <button 
        onClick={testDirectAPI} 
        disabled={loading}
        style={{ 
          padding: '10px 20px', 
          backgroundColor: '#007bff', 
          color: 'white', 
          border: 'none', 
          borderRadius: '4px',
          cursor: 'pointer'
        }}
      >
        {loading ? 'Testing...' : 'Test Direct API Call'}
      </button>
      
      {testResult && (
        <div style={{ marginTop: '15px', padding: '10px', backgroundColor: '#f8f9fa', borderRadius: '4px' }}>
          <h4>Results:</h4>
          <pre style={{ fontSize: '12px', overflow: 'auto' }}>
            {JSON.stringify(testResult, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
};

export default QuickAnomalyTest;
