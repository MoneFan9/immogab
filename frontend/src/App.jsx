import { useState, useEffect, useCallback } from 'react';
import { Home, Search, User, Menu, LayoutDashboard, SwitchCamera, ShieldCheck, ShieldAlert, ShieldEllipsis } from 'lucide-react';
import { propertyService } from './services/propertyService';
import { userService } from './services/userService';
import SearchBar from './components/SearchBar';
import PropertyCard from './components/PropertyCard';
import PropertyDetails from './components/PropertyDetails';
import HostDashboard from './components/HostDashboard';
import KYCVerification from './components/KYCVerification';

function App() {
  const [view, setView] = useState('guest'); // 'guest' or 'host'
  const [properties, setProperties] = useState([]);
  const [filters, setFilters] = useState({ query: '', province: '', property_type: '' });
  const [selectedProperty, setSelectedProperty] = useState(null);
  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState(null);
  const [showKYC, setShowKYC] = useState(false);

  const fetchUser = useCallback(async () => {
    const userData = await userService.getUserProfile();
    setUser(userData);
  }, []);

  const fetchProperties = useCallback(async () => {
    setLoading(true);
    const data = await propertyService.searchProperties(filters);
    setProperties(data);
    setLoading(false);
  }, [filters]);

  useEffect(() => {
    fetchProperties();
    fetchUser();
  }, [fetchProperties, fetchUser]);

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
              <button
                onClick={() => setView('guest')}
                className={view === 'guest' ? 'text-blue-600 font-bold' : 'hover:text-blue-600 transition-colors'}
              >
                Accueil
              </button>
              <a href="#" className="hover:text-blue-600 transition-colors">Explorer</a>
              <a href="#" className="hover:text-blue-600 transition-colors">Mes Réservations</a>
            </div>

            <div className="flex items-center gap-4">
              {user && (
                <button
                  onClick={() => setShowKYC(true)}
                  className={`hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold transition-all ${
                    user.is_kyc_verified
                      ? 'bg-green-50 text-green-600 hover:bg-green-100'
                      : user.kyc_document
                        ? 'bg-amber-50 text-amber-600 hover:bg-amber-100'
                        : 'bg-red-50 text-red-600 hover:bg-red-100'
                  }`}
                >
                  {user.is_kyc_verified ? <ShieldCheck size={14} /> : user.kyc_document ? <ShieldEllipsis size={14} /> : <ShieldAlert size={14} />}
                  {user.is_kyc_verified ? 'Vérifié' : user.kyc_document ? 'En attente' : 'Non vérifié'}
                </button>
              )}
              <button
                onClick={() => setView(view === 'guest' ? 'host' : 'guest')}
                className="flex items-center gap-2 bg-gray-900 text-white px-4 py-2 rounded-lg text-sm font-bold hover:bg-gray-800 transition-all shadow-sm"
              >
                {view === 'guest' ? (
                  <>
                    <LayoutDashboard size={18} />
                    Mode Hôte
                  </>
                ) : (
                  <>
                    <SwitchCamera size={18} />
                    Vue Voyageur
                  </>
                )}
              </button>
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

      {view === 'guest' ? (
        <>
          {/* Hero Section */}
          <header className="bg-blue-900 py-20 px-4">
            <div className="max-w-7xl mx-auto text-center">
              <h1 className="text-4xl md:text-6xl font-extrabold text-white mb-6">
                Trouvez votre maison idéale au Gabon
              </h1>
              <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
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
              <div className="flex justify-between items-center mb-8">
                <h2 className="text-2xl font-bold text-gray-900">Propriétés populaires</h2>
                <button className="text-blue-600 font-semibold hover:underline">Voir tout</button>
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
        </>
      ) : (
        <HostDashboard />
      )}

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

      {/* KYC Modal */}
      {showKYC && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-lg shadow-2xl overflow-hidden">
            <KYCVerification
              user={user}
              onUpdate={(updatedUser) => {
                setUser(updatedUser);
              }}
              onClose={() => setShowKYC(false)}
            />
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
