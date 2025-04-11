import { configureStore } from '@reduxjs/toolkit';
import authReducer from './slices/authSlice';
import supplyChainReducer from './slices/supplyChainSlice';
import anomalyReducer from './slices/anomalySlice';

const store = configureStore({
  reducer: {
    auth: authReducer,
    supplyChain: supplyChainReducer,
    anomaly: anomalyReducer,
  },
});

export default store;