import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { supplyChainService } from '../../services/supplyChainService';

// Async thunks
export const fetchSupplyChainData = createAsyncThunk(
  'supplyChain/fetchData',
  async ({ organizationId, dataType, startTime, endTime, includeAnomaliesOnly }, { rejectWithValue }) => {
    try {
      const response = await supplyChainService.queryData(
        organizationId,
        dataType,
        startTime,
        endTime,
        includeAnomaliesOnly
      );
      return response.results;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to fetch supply chain data');
    }
  }
);

export const submitSupplyChainData = createAsyncThunk(
  'supplyChain/submitData',
  async ({ data, organizationId, dataType, accessControl }, { rejectWithValue }) => {
    try {
      const response = await supplyChainService.submitData(
        data,
        organizationId,
        dataType,
        accessControl
      );
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to submit supply chain data');
    }
  }
);

export const retrieveSupplyChainData = createAsyncThunk(
  'supplyChain/retrieveData',
  async ({ dataId, organizationId }, { rejectWithValue }) => {
    try {
      const response = await supplyChainService.retrieveData(dataId, organizationId);
      return response;
    } catch (error) {
      return rejectWithValue(error.response?.data?.message || 'Failed to retrieve supply chain data');
    }
  }
);

const initialState = {
  data: [],
  selectedData: null,
  loading: false,
  submitting: false,
  error: null,
  success: false,
};

const supplyChainSlice = createSlice({
  name: 'supplyChain',
  initialState,
  reducers: {
    clearError: (state) => {
      state.error = null;
    },
    clearSuccess: (state) => {
      state.success = false;
    },
    setSelectedData: (state, action) => {
      state.selectedData = action.payload;
    },
    clearSelectedData: (state) => {
      state.selectedData = null;
    },
  },
  extraReducers: (builder) => {
    builder
      // Fetch supply chain data
      .addCase(fetchSupplyChainData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchSupplyChainData.fulfilled, (state, action) => {
        state.loading = false;
        state.data = action.payload;
      })
      .addCase(fetchSupplyChainData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      })
      // Submit supply chain data
      .addCase(submitSupplyChainData.pending, (state) => {
        state.submitting = true;
        state.error = null;
        state.success = false;
      })
      .addCase(submitSupplyChainData.fulfilled, (state) => {
        state.submitting = false;
        state.success = true;
      })
      .addCase(submitSupplyChainData.rejected, (state, action) => {
        state.submitting = false;
        state.error = action.payload;
      })
      // Retrieve supply chain data
      .addCase(retrieveSupplyChainData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(retrieveSupplyChainData.fulfilled, (state, action) => {
        state.loading = false;
        state.selectedData = action.payload;
      })
      .addCase(retrieveSupplyChainData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
      });
  },
});

export const { clearError, clearSuccess, setSelectedData, clearSelectedData } = supplyChainSlice.actions;

export default supplyChainSlice.reducer;