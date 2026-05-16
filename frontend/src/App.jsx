import { useState, useEffect } from 'react';
import { Home, Search, Calendar, User, Menu, X } from 'lucide-react';
import { propertyService } from './services/propertyService';
import SearchBar from './components/SearchBar';
import PropertyCard from './components/PropertyCard';
import PropertyDetails from './components/PropertyDetails';

function App() {
  const [properties, setProperties] = useState([]);
  const [filters, setFilters] = useState({ query: '', province: '', property_type: '' });
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchProperties = async () => {
    setLoading(true);
    const data = await propertyService.searchProperties(filters);
    setProperties(data);
    setLoading(false);
  };

  useEffect(() => {
    fetchProperties();
  }, []);

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white border-b border-gray-100 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <div className="flex items-center gap-2">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Home className="text-white" size={24} />
              </div>
              <span className="text-2xl font-bold text-gray-900 tracking-tight">Immo<span className="text-blue-600">Gab</span></span>
            </div>

            <div className="hidden md:flex items-center gap-8 text-gray-600 font-medium">
              <a href="#" className="text-blue-600">Accueil</a>
              <a href="#" className="hover:text-blue-600 transition-colors">Explorer</a>
              <a href="#" className="hover:text-blue-600 transition-colors">Mes Réservations</a>
            </div>

            <div className="flex items-center gap-4">
              <button className="flex items-center gap-2 border border-gray-200 rounded-full py-1.5 px-3 hover:shadow-md transition-all">
                <Menu size={18} />
                <div className="bg-gray-200 p-1 rounded-full">
                  <User size={18} className="text-gray-600" />
                </div>
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="bg-blue-900 py-28 px-4 relative overflow-hidden">
        <div className="absolute inset-0 opacity-20">
            <div className="absolute -right-20 -top-20 w-96 h-96 bg-blue-400 rounded-full blur-3xl" />
            <div className="absolute -left-20 -bottom-20 w-96 h-96 bg-blue-600 rounded-full blur-3xl" />
        </div>
        <div className="max-w-7xl mx-auto text-center relative z-10">
          <h1 className="text-5xl md:text-7xl font-extrabold text-white mb-6 tracking-tight">
            Trouvez votre maison <br className="hidden md:block" /> idéale au <span className="text-blue-400">Gabon</span>
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 mb-8 max-w-3xl mx-auto leading-relaxed">
            De Libreville à Franceville, découvrez des milliers d'annonces de vente et location, même à l'heure !
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-20">
        <SearchBar
          filters={filters}
          setFilters={setFilters}
          onSearch={fetchProperties}
        />

        <section className="mt-16">
          <div className="flex flex-col md:flex-row justify-between items-center mb-8 gap-6">
            <h2 className="text-3xl font-extrabold text-gray-900">Propriétés populaires</h2>

            <div className="flex gap-4 overflow-x-auto pb-2 w-full md:w-auto no-scrollbar">
                {[
                    { id: 'all', label: 'Tout', value: '' },
                    { id: 'villa', label: 'Villas', value: 'villa' },
                    { id: 'appartement', label: 'Appartements', value: 'appartement' },
                    { id: 'terrain', label: 'Terrains', value: 'terrain' },
                    { id: 'espace_evenementiel', label: 'Événements', value: 'espace_evenementiel' },
                ].map((cat) => (
                    <button
                        key={cat.id}
                        onClick={() => {
                            const newFilters = { ...filters, property_type: cat.value };
                            setFilters(newFilters);
                            propertyService.searchProperties(newFilters).then(setProperties);
                        }}
                        className={`whitespace-nowrap px-6 py-2 rounded-full font-semibold transition-all ${
                            filters.property_type === cat.value
                            ? 'bg-blue-600 text-white shadow-lg shadow-blue-200'
                            : 'bg-white text-gray-600 border border-gray-100 hover:border-blue-200 hover:text-blue-600'
                        }`}
                    >
                        {cat.label}
                    </button>
                ))}
            </div>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
              {[1, 2, 3].map(i => (
                <div key={i} className="bg-gray-200 rounded-xl h-96 animate-pulse" />
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
              {properties.map(property => (
                <PropertyCard
                  key={property.id}
                  property={property}
                  onClick={setSelectedProperty}
                />
              ))}
            </div>
          )}

          {!loading && properties.length === 0 && (
            <div className="text-center py-20 bg-white rounded-2xl border border-dashed border-gray-300">
                <div className="bg-gray-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                    <Search className="text-gray-400" size={32} />
                </div>
                <h3 className="text-xl font-bold text-gray-900">Aucun résultat trouvé</h3>
                <p className="text-gray-500">Essayez de modifier vos filtres de recherche.</p>
            </div>
          )}
        </section>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-100 py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-8">
            <div className="flex items-center gap-2">
              <div className="bg-blue-600 p-2 rounded-lg">
                <Home className="text-white" size={20} />
              </div>
              <span className="text-xl font-bold text-gray-900">ImmoGab</span>
            </div>
            <p className="text-gray-500">© 2026 ImmoGab SAS. Tous droits réservés.</p>
            <div className="flex gap-6 text-gray-500">
              <a href="#" className="hover:text-blue-600">Conditions</a>
              <a href="#" className="hover:text-blue-600">Confidentialité</a>
              <a href="#" className="hover:text-blue-600">Aide</a>
            </div>
          </div>
        </div>
      </footer>

      {/* Details Modal */}
      {selectedProperty && (
        <PropertyDetails
          property={selectedProperty}
          onClose={() => setSelectedProperty(null)}
        />
      )}
    </div>
  );
}

export default App;
