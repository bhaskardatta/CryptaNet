import React, { useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { detectAnomalies } from './store/slices/anomalySlice';

const DebugAnomaly = () => {
  const dispatch = useDispatch();
  const { anomalies, loading, error } = useSelector((state) => state.anomaly);
  const { user } = useSelector((state) => state.auth);
  
  const [debugInfo, setDebugInfo] = useState({});

  useEffect(() => {
    setDebugInfo({
      reduxAnomalies: anomalies,
      reduxAnomaliesLength: anomalies?.length || 0,
      reduxLoading: loading,
      reduxError: error,
      user: user
    });
  }, [anomalies, loading, error, user]);

  const testReduxFlow = async () => {
    console.log('🧪 Testing Redux flow...');
    try {
      const result = await dispatch(detectAnomalies({
        organizationId: 'Org1MSP',
        dataType: 'all',
        startTime: '',
        endTime: '',
        threshold: 0.5,
      }));
      console.log('🧪 Redux dispatch result:', result);
      setDebugInfo(prev => ({...prev, dispatchResult: result}));
    } catch (err) {
      console.error('🧪 Redux dispatch error:', err);
      setDebugInfo(prev => ({...prev, dispatchError: err}));
    }
  };

  return (
    <div style={{ padding: '20px', border: '2px solid blue', margin: '10px' }}>
      <h3>🧪 Redux Anomaly Debug</h3>
      <button onClick={testReduxFlow}>Test Redux Flow</button>
      
      <div style={{ marginTop: '20px' }}>
        <h4>Current Redux State:</h4>
        <pre style={{ background: '#f0f0f0', padding: '10px', overflow: 'auto' }}>
          {JSON.stringify(debugInfo, null, 2)}
        </pre>
      </div>
      
      <div style={{ marginTop: '20px' }}>
        <h4>Anomalies Array Debug:</h4>
        <p>Type: {typeof anomalies}</p>
        <p>Is Array: {Array.isArray(anomalies)}</p>
        <p>Length: {anomalies?.length || 0}</p>
        <p>First Item: {anomalies && anomalies[0] ? JSON.stringify(anomalies[0], null, 2) : 'None'}</p>
      </div>
    </div>
  );
};

export default DebugAnomaly;
