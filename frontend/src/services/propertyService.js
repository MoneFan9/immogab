import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
});

export const propertyService = {
  searchProperties: async (params) => {
    try {
      const response = await api.get('/properties/search/', { params });
      return response.data;
    } catch (error) {
      console.error('Error searching properties:', error);
      // Return mock data if API fails (e.g. backend not running)
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
          images: [
            "https://images.unsplash.com/photo-1580587771525-78b9dba3b914?auto=format&fit=crop&w=800&q=80",
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=800&q=80"
          ]
        },
        {
          id: 2,
          title: "Appartement de Luxe",
          description: "Appartement moderne en plein centre.",
          property_type: "APPARTEMENT",
          price_per_day: 85000,
          province: "ESTUAIRE",
          city: "Libreville",
          neighborhood: "Centre-Ville",
          images: [
            "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?auto=format&fit=crop&w=800&q=80"
          ]
        },
        {
            id: 3,
            title: "Espace Événementiel",
            description: "Idéal pour vos réceptions et mariages.",
            property_type: "ESPACE_EVENEMENTIEL",
            price_per_hour: 25000,
            province: "OGOOUÉ_MARITIME",
            city: "Port-Gentil",
            neighborhood: "Quartier Chic",
            images: [
              "https://images.unsplash.com/photo-1519167758481-83f550bb49b3?auto=format&fit=crop&w=800&q=80"
            ]
          }
      ];
    }
  },
};
