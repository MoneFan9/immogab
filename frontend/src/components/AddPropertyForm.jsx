import { useState } from 'react';
import { X, Info, ShieldCheck, Cpu, ChevronRight, ChevronLeft } from 'lucide-react';
import { hostService } from '../services/hostService';

const AddPropertyForm = ({ onClose, onSuccess }) => {
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    property_type: 'MAISON',
    price_per_day: '',
    price_per_hour: '',
    caution_amount: '',
    province: 'ESTUAIRE',
    city: '',
    neighborhood: '',
    address: '',
    parties_allowed: false,
    jeedom_ip: '',
  });
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState({});

  const validateStep = (currentStep) => {
    const newErrors = {};
    if (currentStep === 1) {
      if (!formData.title) newErrors.title = 'Le titre est requis';
      if (!formData.description) newErrors.description = 'La description est requise';
    } else if (currentStep === 2) {
      if (!formData.city) newErrors.city = 'La ville est requise';
      if (!formData.address) newErrors.address = "L'adresse est requise";
      if (!formData.price_per_day && !formData.price_per_hour) {
        newErrors.price = 'Veuillez renseigner au moins un prix';
      }
    } else if (currentStep === 3) {
      if (formData.jeedom_ip && !/^(\d{1,3}\.){3}\d{1,3}$/.test(formData.jeedom_ip)) {
        newErrors.jeedom_ip = "L'adresse IP Jeedom n'est pas valide (ex: 192.168.1.50)";
      }
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const nextStep = () => {
    if (validateStep(step)) setStep(s => s + 1);
  };

  const prevStep = () => setStep(s => s - 1);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
    if (errors[name]) {
      setErrors(prev => {
        const newErrs = { ...prev };
        delete newErrs[name];
        return newErrs;
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validateStep(3)) return;

    setLoading(true);
    const result = await hostService.addProperty(formData);
    setLoading(false);

    if (result) {
      onSuccess();
    }
  };

  const renderStep = () => {
    switch (step) {
      case 1:
        return (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-700">Titre de l'annonce</label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleChange}
                placeholder="Ex: Belle Villa avec Piscine à Angondjé"
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.title ? 'border-red-500' : 'border-gray-300'}`}
              />
              {errors.title && <p className="text-red-500 text-xs mt-1">{errors.title}</p>}
            </div>

            <div className="space-y-4">
              <label className="block text-sm font-medium text-gray-700">Description</label>
              <textarea
                name="description"
                rows={4}
                value={formData.description}
                onChange={handleChange}
                placeholder="Décrivez votre bien en quelques lignes..."
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.description ? 'border-red-500' : 'border-gray-300'}`}
              />
              {errors.description && <p className="text-red-500 text-xs mt-1">{errors.description}</p>}
            </div>

            <div className="space-y-4">
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
        );
      case 2:
        return (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
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
                  value={formData.city}
                  onChange={handleChange}
                  placeholder="Ex: Libreville"
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.city ? 'border-red-500' : 'border-gray-300'}`}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Quartier</label>
                <input
                  type="text"
                  name="neighborhood"
                  value={formData.neighborhood}
                  onChange={handleChange}
                  placeholder="Ex: Angondjé"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Adresse précise</label>
                <input
                  type="text"
                  name="address"
                  value={formData.address}
                  onChange={handleChange}
                  placeholder="Ex: Près de l'école publique"
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.address ? 'border-red-500' : 'border-gray-300'}`}
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 border-t border-gray-100 pt-6">
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Prix / jour (FCFA)</label>
                <input
                  type="number"
                  name="price_per_day"
                  value={formData.price_per_day}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700">Prix / heure (FCFA)</label>
                <input
                  type="number"
                  name="price_per_hour"
                  value={formData.price_per_hour}
                  onChange={handleChange}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
              <div className="space-y-2">
                <label className="block text-sm font-medium text-gray-700 flex items-center gap-1">
                  Caution (FCFA)
                  <Info size={12} className="text-gray-400" />
                </label>
                <input
                  type="number"
                  name="caution_amount"
                  value={formData.caution_amount}
                  onChange={handleChange}
                  placeholder="Dépôt de garantie"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>
            {errors.price && <p className="text-red-500 text-xs">{errors.price}</p>}
          </div>
        );
      case 3:
        return (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            <div className="bg-blue-50 p-4 rounded-xl">
              <h3 className="text-sm font-bold text-blue-900 mb-4 flex items-center gap-2">
                <ShieldCheck size={18} />
                Règles de la propriété
              </h3>
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
              <p className="text-xs text-gray-500 mt-2 italic ml-8">
                Note: L'autorisation des fêtes peut attirer plus de clients mais nécessite une vigilance accrue.
              </p>
            </div>

            <div className="bg-gray-50 p-4 rounded-xl border border-gray-200">
              <h3 className="text-sm font-bold text-gray-900 mb-4 flex items-center gap-2">
                <Cpu size={18} />
                Intégration IoT Jeedom
              </h3>
              <div className="space-y-4">
                <label className="block text-sm font-medium text-gray-700">
                  Adresse IP de la box Jeedom
                </label>
                <input
                  type="text"
                  name="jeedom_ip"
                  value={formData.jeedom_ip}
                  onChange={handleChange}
                  placeholder="Ex: 192.168.1.50"
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent ${errors.jeedom_ip ? 'border-red-500' : 'border-gray-300'}`}
                />
                {errors.jeedom_ip && <p className="text-red-500 text-xs mt-1">{errors.jeedom_ip}</p>}
                <p className="text-xs text-gray-500">
                  Optionnel. Permet de générer automatiquement des codes d'accès pour vos voyageurs.
                </p>
              </div>
            </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Ajouter un bien</h2>
          <p className="text-gray-500 text-sm">Étape {step} sur 3</p>
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label="Fermer"
          className="p-2 hover:bg-gray-100 rounded-full transition-colors"
        >
          <X size={24} className="text-gray-500" />
        </button>
      </div>

      {/* Progress Bar */}
      <div className="w-full bg-gray-100 h-2 rounded-full mb-8 flex overflow-hidden">
        <div
          className="bg-blue-600 h-full transition-all duration-500 ease-out"
          style={{ width: `${(step / 3) * 100}%` }}
        />
      </div>

      <form onSubmit={handleSubmit}>
        <div className="min-h-[350px]">
          {renderStep()}
        </div>

        <div className="flex justify-between gap-4 pt-8 mt-8 border-t border-gray-100">
          <div className="flex gap-3">
            {step > 1 ? (
              <button
                type="button"
                onClick={prevStep}
                className="flex items-center gap-2 px-6 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ChevronLeft size={18} />
                Précédent
              </button>
            ) : (
              <button
                type="button"
                onClick={onClose}
                className="px-6 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100 rounded-lg transition-colors"
              >
                Annuler
              </button>
            )}
          </div>

          {step < 3 ? (
            <button
              type="button"
              onClick={nextStep}
              className="flex items-center gap-2 px-6 py-2 bg-blue-600 text-white text-sm font-bold rounded-lg hover:bg-blue-700 transition-colors"
            >
              Suivant
              <ChevronRight size={18} />
            </button>
          ) : (
            <button
              type="submit"
              disabled={loading}
              className="px-8 py-2 bg-blue-900 text-white text-sm font-bold rounded-lg hover:bg-black transition-colors disabled:opacity-50"
            >
              {loading ? 'Publication...' : 'Publier l\'annonce'}
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

export default AddPropertyForm;
