import axios from 'axios';

const API_BASE_URL = 'https://beautiful-thread-production.up.railway.app/api';

// Criar instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token de autenticação
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar respostas e erros
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado ou inválido
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Funções de autenticação
export const authAPI = {
  register: (userData) => api.post('/auth/register', userData),
  login: (credentials) => api.post('/auth/login', credentials),
  getProfile: () => api.get('/auth/profile'),
  updateProfile: (userData) => api.put('/auth/profile', userData),
};

// Funções de serviços
export const serviceAPI = {
  getCategories: () => api.get('/services/categories'),
  createCategory: (categoryData) => api.post('/services/categories', categoryData),
  addProviderService: (serviceData) => api.post('/services/provider-services', serviceData),
  getProviderServices: () => api.get('/services/provider-services'),
  searchProviders: (params) => api.get('/services/search', { params }),
};

// Funções de pedidos
export const requestAPI = {
  createRequest: (requestData) => api.post('/orders', requestData),
  getRequests: () => api.get('/orders'),
  getRequestDetail: (requestId) => api.get(`/orders/${requestId}`),
  updateRequest: (requestId, requestData) => api.put(`/orders/${requestId}`, requestData),
  deleteRequest: (requestId) => api.delete(`/orders/${requestId}`),
};

// Funções de propostas
export const proposalAPI = {
  createProposal: (proposalData) => api.post('/proposals', proposalData),
  getProposalsByRequest: (requestId) => api.get(`/proposals/request/${requestId}`),
  acceptProposal: (proposalId) => api.post(`/proposals/${proposalId}/accept`),
  rejectProposal: (proposalId) => api.post(`/proposals/${proposalId}/reject`),
  getMyProposals: () => api.get('/proposals/my-proposals'),
};

// Funções de avaliações
export const evaluationAPI = {
  createEvaluation: (evaluationData) => api.post('/evaluations', evaluationData),
  getUserEvaluations: (userId) => api.get(`/evaluations/user/${userId}`),
  getRequestEvaluations: (requestId) => api.get(`/evaluations/request/${requestId}`),
  getMyEvaluations: () => api.get('/evaluations/my-evaluations'),
};

export default api;

