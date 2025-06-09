import React, { useState } from 'react';
import { simpleAnomalyService } from './simpleAnomalyService';

const MinimalAnomalyTest = () => {
  const [anomalies, setAnomalies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchAnomalies = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await simpleAnomalyService.detectAnomalies();
      setAnomalies(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px', border: '3px solid red', margin: '10px' }}>
      <h3>🔥 Minimal Anomaly Test</h3>
      <button onClick={fetchAnomalies} disabled={loading}>
        {loading ? 'Fetching...' : 'Fetch Anomalies'}
      </button>
      
      {error && <p style={{ color: 'red' }}>Error: {error}</p>}
      
      <p>Anomalies Count: {anomalies.length}</p>
      
      {anomalies.length > 0 && (
        <div>
          <h4>Anomalies:</h4>
          <table style={{ border: '1px solid black', borderCollapse: 'collapse' }}>
            <thead>
              <tr>
                <th style={{ border: '1px solid black', padding: '5px' }}>ID</th>
                <th style={{ border: '1px solid black', padding: '5px' }}>Product ID</th>
                <th style={{ border: '1px solid black', padding: '5px' }}>Score</th>
              </tr>
            </thead>
            <tbody>
              {anomalies.map(anomaly => (
                <tr key={anomaly.id}>
                  <td style={{ border: '1px solid black', padding: '5px' }}>{anomaly.id}</td>
                  <td style={{ border: '1px solid black', padding: '5px' }}>{anomaly.productId}</td>
                  <td style={{ border: '1px solid black', padding: '5px' }}>{anomaly.anomalyScore.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default MinimalAnomalyTest;
