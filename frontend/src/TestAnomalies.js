import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { API_URL } from './config';

const TestAnomalies = () => {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const testDirectAPI = async () => {
    setLoading(true);
    setError(null);
    try {
      console.log('🔥 Testing direct API call to:', `${API_URL}/api/analytics/anomalies`);
      const response = await axios.get(`${API_URL}/api/analytics/anomalies`);
      console.log('🔥 Direct API response:', response.data);
      setData(response.data);
    } catch (err) {
      console.error('🔥 Direct API error:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    testDirectAPI();
  }, []);

  return (
    <div style={{ padding: '20px', border: '1px solid red', margin: '10px' }}>
      <h3>🔥 Direct API Test</h3>
      <button onClick={testDirectAPI}>Test API Call</button>
      
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      {data && (
        <div>
          <p>✅ API Response received!</p>
          <p>Anomalies count: {data.anomalies?.length || 0}</p>
          <p>Total unique anomalies: {data.unique_anomalies_count || 0}</p>
          <p>Success: {String(data.success)}</p>
        </div>
      )}
    </div>
  );
};

export default TestAnomalies;
