import { Search, SlidersHorizontal } from 'lucide-react';

export default function SearchBar({ filters, setFilters, onSearch }) {
  const provinces = [
    { value: 'estuaire', label: 'Estuaire' },
    { value: 'haut_ogooue', label: 'Haut-Ogooué' },
    { value: 'moyen_ogooue', label: 'Moyen-Ogooué' },
    { value: 'ngounie', label: 'Ngounié' },
    { value: 'nyanga', label: 'Nyanga' },
    { value: 'ogooue_ivindo', label: 'Ogooué-Ivindo' },
    { value: 'ogooue_lolo', label: 'Ogooué-Lolo' },
    { value: 'ogooue_maritime', label: 'Ogooué-Maritime' },
    { value: 'woleu_ntem', label: 'Woleu-Ntem' }
  ];

  const types = [
    { value: 'villa', label: 'Villa' },
    { value: 'appartement', label: 'Appartement' },
    { value: 'terrain', label: 'Terrain' },
    { value: 'espace_evenementiel', label: 'Événementiel' },
  ];

  return (
    <div className="bg-white p-4 rounded-2xl shadow-xl -mt-12 relative z-10 mx-auto max-w-4xl border border-gray-100">
      <div className="flex flex-col md:flex-row gap-4">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            placeholder="Où cherchez-vous ?"
            className="w-full pl-10 pr-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            value={filters.query}
            onChange={(e) => setFilters({ ...filters, query: e.target.value })}
          />
        </div>

        <div className="flex flex-1 gap-4">
          <select
            className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
            value={filters.province}
            onChange={(e) => setFilters({ ...filters, province: e.target.value })}
          >
            <option value="">Toutes les provinces</option>
            {provinces.map(p => (
              <option key={p.value} value={p.value}>{p.label}</option>
            ))}
          </select>

          <select
            className="flex-1 px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
            value={filters.property_type}
            onChange={(e) => setFilters({ ...filters, property_type: e.target.value })}
          >
            <option value="">Tous les types</option>
            {types.map(t => (
              <option key={t.value} value={t.value}>{t.label}</option>
            ))}
          </select>
        </div>

        <button
          onClick={onSearch}
          className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-8 py-3 rounded-xl transition-all shadow-lg shadow-blue-200 flex items-center justify-center gap-2"
        >
          <Search size={20} />
          Rechercher
        </button>
      </div>
    </div>
  );
}
