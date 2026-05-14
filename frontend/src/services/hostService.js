import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const hostService = {
  getHostProperties: async () => {
    try {
      const response = await api.get('/host/properties/');
      return response.data;
    } catch (error) {
      console.error('Error fetching host properties:', error);
      // Mock data fallback
      return [
        {
          id: 1,
          title: "Villa Bord de Mer",
          description: "Magnifique villa avec vue sur l'océan.",
          property_type: "MAISON",
          price_per_day: 150000,
          province: "ESTUAIRE",
          city: "Libreville",
          neighborhood: "Sablière",
          images: ["https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=800&q=80"]
        },
        {
          id: 4,
          title: "Studio Moderne",
          description: "Studio équipé au centre de Franceville.",
          property_type: "APPARTEMENT",
          price_per_day: 45000,
          province: "HAUT-OGOOUÉ",
          city: "Franceville",
          neighborhood: "Potos",
          images: ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?auto=format&fit=crop&w=800&q=80"]
        }
      ];
    }
  },

  addProperty: async (propertyData) => {
    try {
      const response = await api.post('/host/properties/', propertyData);
      return response.data;
    } catch (error) {
      console.error('Error adding property:', error);
      // Simulate success for demo purposes
      return new Promise((resolve) => {
        setTimeout(() => resolve({ id: Date.now(), ...propertyData }), 1000);
      });
    }
  },

  getIncomeHistory: async () => {
    try {
      const response = await api.get('/host/income/');
      return response.data;
    } catch (error) {
      console.error('Error fetching income history:', error);
      // Mock data fallback
      return {
        stats: {
          total: 1250000,
          pending: 125000,
          thisMonth: 450000
        },
        transactions: [
          {
            id: 101,
            property_title: "Villa Bord de Mer",
            date: "2026-05-15",
            type: "Location Journalière",
            amount: 150000,
            status: "COMPLETED"
          },
          {
            id: 102,
            property_title: "Studio Moderne",
            date: "2026-05-14",
            type: "Location Horaire",
            amount: 15000,
            status: "COMPLETED"
          },
          {
            id: 103,
            property_title: "Villa Bord de Mer",
            date: "2026-05-20",
            type: "Location Journalière",
            amount: 150000,
            status: "PENDING"
          }
        ]
      };
    }
  }
};
