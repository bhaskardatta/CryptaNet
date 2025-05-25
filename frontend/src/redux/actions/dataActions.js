import axios from 'axios';
import { API_URL } from '../../config';

// Supply Chain Data Actions
export const FETCH_SUPPLY_CHAIN_DATA_REQUEST = 'FETCH_SUPPLY_CHAIN_DATA_REQUEST';
export const FETCH_SUPPLY_CHAIN_DATA_SUCCESS = 'FETCH_SUPPLY_CHAIN_DATA_SUCCESS';
export const FETCH_SUPPLY_CHAIN_DATA_FAILURE = 'FETCH_SUPPLY_CHAIN_DATA_FAILURE';

export const FETCH_ANOMALIES_REQUEST = 'FETCH_ANOMALIES_REQUEST';
export const FETCH_ANOMALIES_SUCCESS = 'FETCH_ANOMALIES_SUCCESS';
export const FETCH_ANOMALIES_FAILURE = 'FETCH_ANOMALIES_FAILURE';

// Get supply chain data
export const getSupplyChainData = () => async (dispatch, getState) => {
  try {
    dispatch({ type: FETCH_SUPPLY_CHAIN_DATA_REQUEST });
    
    const { auth } = getState();
    const token = auth.token;
    
    const response = await axios.get(`${API_URL}/api/supply-chain/query`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    dispatch({ 
      type: FETCH_SUPPLY_CHAIN_DATA_SUCCESS, 
      payload: response.data 
    });
  } catch (error) {
    dispatch({ 
      type: FETCH_SUPPLY_CHAIN_DATA_FAILURE, 
      payload: error.message 
    });
  }
};

// Get recent anomalies
export const getRecentAnomalies = () => async (dispatch, getState) => {
  try {
    dispatch({ type: FETCH_ANOMALIES_REQUEST });
    
    const { auth } = getState();
    const token = auth.token;
    
    const response = await axios.get(`${API_URL}/api/anomalies`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    dispatch({ 
      type: FETCH_ANOMALIES_SUCCESS, 
      payload: response.data 
    });
  } catch (error) {
    dispatch({ 
      type: FETCH_ANOMALIES_FAILURE, 
      payload: error.message 
    });
  }
};