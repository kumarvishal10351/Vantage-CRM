import axios from 'axios';

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Attach bearer token if available
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('vantage_auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor
apiClient.interceptors.response.use(
  (response) => {
    // Automatically unwrap the standard backend envelope: { success: true, data: ... }
    if (response.data && response.data.success !== undefined && response.data.data !== undefined) {
      response.data = response.data.data;
    }
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      if (!window.location.pathname.includes('/login')) {
        localStorage.removeItem('vantage_auth_token');
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: (email, password) => apiClient.post('/auth/login', { email, password }),
  getMe: () => apiClient.get('/auth/me'),
};

export const pipelineApi = {
  getSummary: () => apiClient.get('/pipeline/summary'),
  getStages: () => apiClient.get('/pipeline/stages'),
  getProducts: () => apiClient.get('/pipeline/products'),
  getSectors: () => apiClient.get('/pipeline/sectors'),
  getAgents: () => apiClient.get('/pipeline/agents'),
  getManagers: () => apiClient.get('/pipeline/managers'),
  getRegions: () => apiClient.get('/pipeline/regions'),
};

export const opportunitiesApi = {
  list: (params = {}) => apiClient.get('/opportunities', { params }),
  getById: (id) => apiClient.get(`/opportunities/${id}`),
};

export const prioritiesApi = {
  list: (params = {}) => apiClient.get('/prioritization', { params }),
  getSummary: () => apiClient.get('/prioritization/summary'),
};

export const workQueuesApi = {
  getSummary: () => apiClient.get('/work-queues/summary'),
  getHighPriority: (params = {}) => apiClient.get('/work-queues/high-priority', { params }),
  getStalledDeals: (params = {}) => apiClient.get('/work-queues/stalled-deals', { params }),
  getUnassignedAccounts: (params = {}) => apiClient.get('/work-queues/unassigned-accounts', { params }),
};

export const accountsApi = {
  list: (params = {}) => apiClient.get('/accounts', { params }),
  getSummary: () => apiClient.get('/accounts/summary'),
  getById: (id) => apiClient.get(`/accounts/${id}`),
};

export const agentsApi = {
  list: (params = {}) => apiClient.get('/agents', { params }),
  getByName: (name) => apiClient.get(`/agents/${encodeURIComponent(name)}`),
};

export const managersApi = {
  list: (params = {}) => apiClient.get('/managers', { params }),
  getByName: (name) => apiClient.get(`/managers/${encodeURIComponent(name)}`),
};

export const productsApi = {
  list: (params = {}) => apiClient.get('/products', { params }),
  getByName: (name) => apiClient.get(`/products/${encodeURIComponent(name)}`),
};

export const agingApi = {
  getSummary: () => apiClient.get('/aging/summary'),
};

export default apiClient;
