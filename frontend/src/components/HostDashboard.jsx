import { useState, useEffect, useCallback } from 'react';
import { PlusCircle, Home, Settings } from 'lucide-react';
import AddPropertyForm from './AddPropertyForm';
import IncomeHistory from './IncomeHistory';
import { hostService } from '../services/hostService';

const HostDashboard = () => {
  const [activeTab, setActiveTab] = useState('properties');
  const [properties, setProperties] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showAddForm, setShowAddForm] = useState(false);

  const fetchHostData = useCallback(async () => {
    setLoading(true);
    const data = await hostService.getHostProperties();
    setProperties(data);
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchHostData();
  }, [fetchHostData]);

  const handlePropertyAdded = () => {
    setShowAddForm(false);
    fetchHostData();
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Espace Hôte</h1>
        <button
          onClick={() => setShowAddForm(true)}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
        >
          <PlusCircle size={20} />
          Ajouter un bien
        </button>
      </div>

      <div className="flex border-b border-gray-200 mb-8">
        <button
          onClick={() => setActiveTab('properties')}
          className={`px-6 py-3 font-medium text-sm transition-colors relative ${
            activeTab === 'properties' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Mes Biens
          {activeTab === 'properties' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />}
        </button>
        <button
          onClick={() => setActiveTab('income')}
          className={`px-6 py-3 font-medium text-sm transition-colors relative ${
            activeTab === 'income' ? 'text-blue-600' : 'text-gray-500 hover:text-gray-700'
          }`}
        >
          Historique des Revenus
          {activeTab === 'income' && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-600" />}
        </button>
      </div>

      {activeTab === 'properties' && (
        <div>
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2].map(i => (
                <div key={i} className="bg-gray-100 h-64 rounded-xl animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {properties.map(property => (
                <div key={property.id} className="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
                  <div className="h-48 bg-gray-200 relative">
                    {property.images && property.images[0] ? (
                      <img src={property.images[0]} alt={property.title} className="w-full h-full object-cover" />
                    ) : (
                      <div className="w-full h-full flex items-center justify-center text-gray-400">
                        <Home size={48} />
                      </div>
                    )}
                    <div className="absolute top-2 right-2 bg-white/90 backdrop-blur px-2 py-1 rounded text-xs font-bold text-blue-600 uppercase">
                      {property.property_type}
                    </div>
                  </div>
                  <div className="p-4">
                    <h3 className="font-bold text-lg mb-1 truncate">{property.title}</h3>
                    <p className="text-gray-500 text-sm mb-4">{property.city}, {property.province}</p>
                    <div className="flex justify-between items-center text-sm font-medium">
                      <span className="text-gray-900">
                        {property.price_per_day ? `${property.price_per_day.toLocaleString()} FCFA / jour` : `${property.price_per_hour.toLocaleString()} FCFA / heure`}
                      </span>
                      <div className="flex gap-2">
                        <button className="p-2 text-gray-400 hover:text-blue-600 transition-colors">
                          <Settings size={18} />
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
              {properties.length === 0 && (
                <div className="col-span-full text-center py-12 bg-gray-50 rounded-xl border-2 border-dashed border-gray-200">
                  <Home className="mx-auto text-gray-400 mb-4" size={48} />
                  <p className="text-gray-500 font-medium">Vous n'avez pas encore de biens.</p>
                  <button
                    onClick={() => setShowAddForm(true)}
                    className="mt-4 text-blue-600 font-bold hover:underline"
                  >
                    Ajouter votre premier bien
                  </button>
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {activeTab === 'income' && <IncomeHistory />}

      {showAddForm && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto shadow-2xl">
            <AddPropertyForm
              onClose={() => setShowAddForm(false)}
              onSuccess={handlePropertyAdded}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default HostDashboard;
