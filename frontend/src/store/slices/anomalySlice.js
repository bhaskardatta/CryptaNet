import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { anomalyService } from '../../services/anomalyService';

// Async thunks
export const detectAnomalies = createAsyncThunk(
  'anomaly/detectAnomalies',
  async ({ organizationId, dataType, startTime, endTime, threshold }, { rejectWithValue }) => {
    try {
      const response = await anomalyService.detectAnomalies(
        organizationId,
        dataType,
        startTime,
        endTime,
        threshold
      );
      return response.results;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to detect anomalies');
    }
  }
);

export const getAnomalyExplanation = createAsyncThunk(
  'anomaly/getExplanation',
  async ({ anomalyId, organizationId }, { rejectWithValue }) => {
    try {
      const response = await anomalyService.getExplanation(anomalyId, organizationId);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to get anomaly explanation');
    }
  }
);

const initialState = {
  anomalies: [],
  selectedAnomaly: null,
  explanation: null,
  loading: false,
  error: null,
  success: false,
};

const anomalySlice = createSlice({
  name: 'anomaly',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearSuccess: (state) => {
      state.success = false;
    },
    setSelectedAnomaly: (state, action) => {
      state.selectedAnomaly = action.payload;
    },
    clearSelectedAnomaly: (state) => {
      state.selectedAnomaly = null;
      state.explanation = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Detect anomalies
      .addCase(detectAnomalies.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(detectAnomalies.fulfilled, (state, action) => {
        state.loading = false;
        state.anomalies = action.payload;
        state.success = true;
      })
      .addCase(detectAnomalies.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Get anomaly explanation
      .addCase(getAnomalyExplanation.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(getAnomalyExplanation.fulfilled, (state, action) => {
        state.loading = false;
        state.explanation = action.payload;
      })
      .addCase(getAnomalyExplanation.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError, clearSuccess, setSelectedAnomaly, clearSelectedAnomaly } = anomalySlice.actions;

export default anomalySlice.reducer;