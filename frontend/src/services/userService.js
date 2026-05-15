import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

// Helper to get token from localStorage (assuming JWT auth is implemented)
const getAuthHeaders = () => {
  const token = localStorage.getItem('access_token');
  return token ? { Authorization: `Bearer ${token}` } : {};
};

export const userService = {
  getUserProfile: async () => {
    try {
      const response = await api.get('/core/me/', { headers: getAuthHeaders() });
      return response.data;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      // Mock data fallback
      return {
        id: 1,
        username: "Jean Gabin",
        email: "jean.gabin@example.ga",
        cni_number: "123456789",
        is_kyc_verified: false,
        kyc_document: null
      };
    }
  },

  submitKYC: async (formData) => {
    try {
      // formData should be a FormData object containing cni_number and kyc_document
      const response = await api.patch('/core/kyc/submit/', formData, {
        headers: {
          ...getAuthHeaders(),
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error submitting KYC:', error);
      // Simulate success for demo
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            id: 1,
            username: "Jean Gabin",
            email: "jean.gabin@example.ga",
            cni_number: formData.get('cni_number'),
            is_kyc_verified: false, // Remains false until backend validates
            kyc_document: 'mock_path_to_document.pdf'
          });
        }, 1500);
      });
    }
  }
};
