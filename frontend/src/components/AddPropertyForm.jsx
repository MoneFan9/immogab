import { useState } from 'react';
import { X, Info, ShieldCheck, Cpu } from 'lucide-react';
import { hostService } from '../services/hostService';

const AddPropertyForm = ({ onClose, onSuccess }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    property_type: 'MAISON',
    price_per_day: '',
    price_per_hour: '',
    province: 'ESTUAIRE',
    city: '',
    neighborhood: '',
    parties_allowed: false,
    jeedom_ip: '',
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const validateIP = (ip) => {
    if (!ip) return true;
    const regex = /^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$/;
    return regex.test(ip);
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};

    if (formData.jeedom_ip && !validateIP(formData.jeedom_ip)) {
      newErrors.jeedom_ip = "Format d'adresse IP invalide (ex: 192.168.1.50)";
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});
    setLoading(true);

    // Simulate API call
    const result = await hostService.addProperty(formData);
    setLoading(false);

    if (result) {
      onSuccess();
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Ajouter une propriété</h2>
        <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
          <X size={24} className="text-gray-500" />
        </button>
      </div>

      <form onSubmit={handleSubmit} className="space-y-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-8">
          {/* Section 1: Informations Générales */}
          <div className="col-span-full">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Info className="text-blue-600" size={20} />
              Informations Générales
            </h3>
            <div className="space-y-6">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Titre de l'annonce</label>
                <input
                  type="text"
                  name="title"
                  required
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="Ex: Belle Villa avec Piscine à Angondjé"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Description</label>
                <textarea
                  name="description"
                  required
                  rows={3}
                  value={formData.description}
                  onChange={handleChange}
                  placeholder="Décrivez votre bien en quelques lignes..."
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="space-y-2 w-full md:w-1/2">
                <label className="block text-sm font-medium text-gray-700">Type de bien</label>
                <select
                  name="property_type"
                  value={formData.property_type}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="MAISON">Maison</option>
                  <option value="APPARTEMENT">Appartement</option>
                  <option value="TERRAIN">Terrain</option>
                  <option value="ESPACE_EVENEMENTIEL">Espace Événementiel</option>
                </select>
              </div>
            </div>
          </div>

          {/* Section 2: Localisation */}
          <div className="col-span-full border-t border-gray-100 pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Localisation</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Province</label>
                <select
                  name="province"
                  value={formData.province}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="ESTUAIRE">Estuaire</option>
                  <option value="HAUT-OGOOUÉ">Haut-Ogooué</option>
                  <option value="MOYEN-OGOOUÉ">Moyen-Ogooué</option>
                  <option value="NGOUNIÉ">Ngounié</option>
                  <option value="NYANGA">Nyanga</option>
                  <option value="OGOOUÉ-IVINDO">Ogooué-Ivindo</option>
                  <option value="OGOOUÉ-LOLO">Ogooué-Lolo</option>
                  <option value="OGOOUÉ-MARITIME">Ogooué-Maritime</option>
                  <option value="WOLEU-NTEM">Woleu-Ntem</option>
                </select>
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Ville</label>
                <input
                  type="text"
                  name="city"
                  required
                  value={formData.city}
                  onChange={handleChange}
                  placeholder="Ex: Libreville"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Quartier</label>
                <input
                  type="text"
                  name="neighborhood"
                  required
                  value={formData.neighborhood}
                  onChange={handleChange}
                  placeholder="Ex: Sablière"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>

          {/* Section 3: Tarification */}
          <div className="col-span-full border-t border-gray-100 pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Tarification</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Prix par jour (FCFA)</label>
                <input
                  type="number"
                  name="price_per_day"
                  value={formData.price_per_day}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Prix par heure (FCFA)</label>
                <input
                  type="number"
                  name="price_per_hour"
                  value={formData.price_per_hour}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
          </div>

          <div className="col-span-full border-t border-gray-100 pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <ShieldCheck className="text-blue-600" size={20} />
              Règles et Sécurité
            </h3>
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <input
                  type="checkbox"
                  id="parties_allowed"
                  name="parties_allowed"
                  checked={formData.parties_allowed}
                  onChange={handleChange}
                  className="w-5 h-5 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
                />
                <label htmlFor="parties_allowed" className="text-sm font-medium text-gray-700">
                  Fêtes et événements autorisés
                </label>
              </div>
              <p className="text-xs text-gray-500 ml-8 italic">
                Note: Des cautions supplémentaires peuvent être appliquées pour les événements.
              </p>
            </div>
          </div>

          <div className="col-span-full border-t border-gray-100 pt-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center gap-2">
              <Cpu className="text-blue-600" size={20} />
              Intégration Domotique (Jeedom)
            </h3>
            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-700 flex items-center gap-2">
                Adresse IP de votre box Jeedom
                <Info size={14} className="text-gray-400" />
              </label>
              <input
                type="text"
                name="jeedom_ip"
                value={formData.jeedom_ip}
                onChange={handleChange}
                placeholder="Ex: 192.168.1.50"
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${
                  errors.jeedom_ip ? 'border-red-500 bg-red-50' : 'border-gray-300'
                }`}
              />
              {errors.jeedom_ip && (
                <p className="text-red-500 text-xs mt-1 font-medium">{errors.jeedom_ip}</p>
              )}
              <p className="text-xs text-gray-500">
                L'IP permet de synchroniser les accès temporaires via vos serrures connectées.
              </p>
            </div>
          </div>
        </div>

        <div className="flex justify-end gap-4 pt-6 border-t border-gray-100">
          <button
            type="button"
            onClick={onClose}
            className="px-6 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
          >
            Annuler
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-6 py-2 bg-blue-600 text-white text-sm font-bold rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
          >
            {loading ? 'Création...' : 'Publier l\'annonce'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default AddPropertyForm;
