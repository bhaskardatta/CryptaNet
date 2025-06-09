import React, { useState } from 'react';
import { anomalyService } from './services/anomalyService';

const SimpleAnomalyTest = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const testAnomalyService = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    try {
      console.log('🧪 Starting simple anomaly service test...');
      const response = await anomalyService.detectAnomalies('Org1MSP', 'all', '', '', 0.5);
      console.log('🧪 Service response:', response);
      setResult(response);
    } catch (err) {
      console.error('🧪 Service error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', border: '3px solid green', margin: '10px' }}>
      <h3>🧪 Simple Anomaly Service Test</h3>
      <button onClick={testAnomalyService} disabled={loading}>
        {loading ? 'Testing...' : 'Test Anomaly Service'}
      </button>
      
      {loading && <p>⏳ Loading...</p>}
      {error && <p style={{ color: 'red' }}>❌ Error: {error}</p>}
      {result && (
        <div style={{ marginTop: '20px' }}>
          <h4>✅ Service Result:</h4>
          <p>Success: {String(result.success)}</p>
          <p>Count: {result.count}</p>
          <p>Results Array Length: {result.results?.length || 0}</p>
          <p>Anomalies Array Length: {result.anomalies?.length || 0}</p>
          {result.results && result.results.length > 0 && (
            <div>
              <h5>First Result:</h5>
              <pre style={{ background: '#f0f0f0', padding: '10px', fontSize: '12px' }}>
                {JSON.stringify(result.results[0], null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SimpleAnomalyTest;
