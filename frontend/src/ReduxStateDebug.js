import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { detectAnomalies } from './store/slices/anomalySlice';

const ReduxStateDebug = () => {
  const dispatch = useDispatch();
  const anomalyState = useSelector((state) => state.anomaly);
  const authState = useSelector((state) => state.auth);
  const [logs, setLogs] = useState([]);

  const addLog = (message) => {
    setLogs(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  useEffect(() => {
    addLog(`Redux state initialized. Anomalies: ${anomalyState?.anomalies?.length || 0}`);
  }, []);

  useEffect(() => {
    addLog(`Anomalies state changed. Count: ${anomalyState?.anomalies?.length || 0}, Loading: ${anomalyState?.loading}, Error: ${anomalyState?.error || 'none'}`);
  }, [anomalyState]);

  const testReduxDispatch = async () => {
    addLog('Starting Redux dispatch test...');
    try {
      const resultAction = await dispatch(detectAnomalies({
        organizationId: 'Org1MSP',
        dataType: 'all',
        startTime: '',
        endTime: '',
        threshold: 0.5,
      }));
      addLog(`Dispatch completed. Type: ${resultAction.type}, Payload length: ${resultAction.payload?.length || 0}`);
    } catch (error) {
      addLog(`Dispatch error: ${error.message}`);
    }
  };

  return (
    <div style={{ padding: '20px', border: '3px solid purple', margin: '10px' }}>
      <h3>🔮 Redux State Debug</h3>
      <button onClick={testReduxDispatch}>Test Redux Dispatch</button>
      
      <div style={{ marginTop: '20px' }}>
        <h4>Current Redux State:</h4>
        <pre style={{ background: '#f0f0f0', padding: '10px', fontSize: '12px', maxHeight: '200px', overflow: 'auto' }}>
          {JSON.stringify({
            anomalies: {
              count: anomalyState?.anomalies?.length || 0,
              isArray: Array.isArray(anomalyState?.anomalies),
              loading: anomalyState?.loading,
              error: anomalyState?.error,
              success: anomalyState?.success
            },
            auth: {
              user: authState?.user?.organization || 'No user'
            }
          }, null, 2)}
        </pre>
      </div>
      
      <div style={{ marginTop: '20px' }}>
        <h4>Debug Logs:</h4>
        <div style={{ background: '#f0f0f0', padding: '10px', maxHeight: '200px', overflow: 'auto' }}>
          {logs.map((log, index) => (
            <div key={index} style={{ fontSize: '12px', marginBottom: '5px' }}>
              {log}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default ReduxStateDebug;
