import React from 'react';
import { useSelector } from 'react-redux';

const SimpleReduxViewer = () => {
  const anomalyState = useSelector((state) => state.anomaly);
  
  return (
    <div style={{ padding: '20px', border: '2px solid orange', margin: '10px' }}>
      <h3>🔍 Simple Redux Viewer</h3>
      <p>Anomalies Type: {typeof anomalyState.anomalies}</p>
      <p>Anomalies Is Array: {Array.isArray(anomalyState.anomalies) ? 'Yes' : 'No'}</p>
      <p>Anomalies Length: {anomalyState.anomalies?.length || 0}</p>
      <p>Loading: {String(anomalyState.loading)}</p>
      <p>Error: {anomalyState.error || 'None'}</p>
      <p>Success: {String(anomalyState.success)}</p>
      
      {anomalyState.anomalies && anomalyState.anomalies.length > 0 && (
        <div>
          <h4>First Anomaly Keys:</h4>
          <p>{Object.keys(anomalyState.anomalies[0] || {}).join(', ')}</p>
        </div>
      )}
    </div>
  );
};

export default SimpleReduxViewer;
