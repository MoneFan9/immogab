import { useState } from 'react';
import { Upload, CheckCircle, AlertCircle, Clock, FileText, X } from 'lucide-react';
import { userService } from '../services/userService';

const KYCVerification = ({ user, onUpdate, onClose }) => {
  const [file, setFile] = useState(null);
  const [cniNumber, setCniNumber] = useState(user?.cni_number || '');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.size > 5 * 1024 * 1024) {
        setMessage({ type: 'error', text: 'Le fichier est trop volumineux (max 5 Mo).' });
        return;
      }
      setFile(selectedFile);
      setMessage(null);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file && !user.kyc_document) {
      setMessage({ type: 'error', text: 'Veuillez sélectionner une pièce d\'identité.' });
      return;
    }
    if (!cniNumber) {
        setMessage({ type: 'error', text: 'Veuillez entrer votre numéro de CNI.' });
        return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('cni_number', cniNumber);
    if (file) {
      formData.append('kyc_document', file);
    }

    const updatedUser = await userService.submitKYC(formData);
    setLoading(false);

    if (updatedUser) {
      setMessage({ type: 'success', text: 'Documents soumis avec succès ! Notre équipe va les vérifier.' });
      onUpdate(updatedUser);
    } else {
      setMessage({ type: 'error', text: 'Une erreur est survenue lors de la soumission.' });
    }
  };

  const getStatusBadge = () => {
    if (user?.is_kyc_verified) {
      return (
        <div className="flex items-center gap-2 text-green-600 bg-green-50 px-3 py-1 rounded-full text-sm font-bold">
          <CheckCircle size={16} />
          Compte Vérifié
        </div>
      );
    }
    if (user?.kyc_document) {
      return (
        <div className="flex items-center gap-2 text-amber-600 bg-amber-50 px-3 py-1 rounded-full text-sm font-bold">
          <Clock size={16} />
          Vérification en cours
        </div>
      );
    }
    return (
      <div className="flex items-center gap-2 text-red-600 bg-red-50 px-3 py-1 rounded-full text-sm font-bold">
        <AlertCircle size={16} />
        Non Vérifié
      </div>
    );
  };

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">Vérification d'identité (KYC)</h2>
        <button onClick={onClose} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
          <X size={20} />
        </button>
      </div>

      <div className="mb-8">
        <p className="text-gray-600 mb-4">
          Conformément à la Loi 025/2021 de la République Gabonaise, vous devez vérifier votre identité pour louer ou mettre en location des biens.
        </p>
        <div className="flex justify-start">
          {getStatusBadge()}
        </div>
      </div>

      {user?.is_kyc_verified ? (
        <div className="bg-green-50 border border-green-200 rounded-xl p-6 text-center">
            <CheckCircle className="text-green-500 mx-auto mb-3" size={48} />
            <h3 className="text-lg font-bold text-green-900 mb-1">Votre compte est certifié</h3>
            <p className="text-green-700">Merci d'avoir complété votre profil ImmoGab.</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">
              Numéro de CNI / Passeport
            </label>
            <input
              type="text"
              className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all"
              placeholder="Ex: 123456789"
              value={cniNumber}
              onChange={(e) => setCniNumber(e.target.value)}
              required
            />
          </div>

          <div>
            <label className="block text-sm font-bold text-gray-700 mb-2">
              Pièce d'identité (Recto-Verso ou Passeport)
            </label>
            <div
              className={`border-2 border-dashed rounded-2xl p-8 text-center transition-all ${
                file ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-blue-400'
              }`}
            >
              <input
                type="file"
                id="kyc-file"
                className="hidden"
                accept=".jpg,.jpeg,.png,.pdf"
                onChange={handleFileChange}
              />
              <label htmlFor="kyc-file" className="cursor-pointer">
                {file ? (
                  <div className="flex flex-col items-center">
                    <FileText className="text-blue-500 mb-2" size={40} />
                    <span className="text-blue-900 font-medium">{file.name}</span>
                    <span className="text-blue-600 text-xs mt-1">{(file.size / 1024 / 1024).toFixed(2)} Mo</span>
                    <button
                      type="button"
                      onClick={(e) => { e.preventDefault(); setFile(null); }}
                      className="mt-4 text-sm text-red-500 font-bold hover:underline"
                    >
                      Supprimer
                    </button>
                  </div>
                ) : (
                  <div className="flex flex-col items-center">
                    <Upload className="text-gray-400 mb-2" size={40} />
                    <span className="text-gray-900 font-bold">Cliquez pour télécharger</span>
                    <span className="text-gray-500 text-sm mt-1">Format JPG, PNG ou PDF (Max 5 Mo)</span>
                  </div>
                )}
              </label>
            </div>
          </div>

          {message && (
            <div className={`p-4 rounded-xl flex items-center gap-3 ${
              message.type === 'success' ? 'bg-green-50 text-green-700 border border-green-100' : 'bg-red-50 text-red-700 border border-red-100'
            }`}>
              {message.type === 'success' ? <CheckCircle size={20} /> : <AlertCircle size={20} />}
              <span className="text-sm font-medium">{message.text}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={loading || (user?.kyc_document && !file)}
            className={`w-full py-4 rounded-xl font-bold text-white transition-all shadow-lg ${
              loading || (user?.kyc_document && !file)
                ? 'bg-gray-300 cursor-not-allowed shadow-none'
                : 'bg-blue-600 hover:bg-blue-700 shadow-blue-200'
            }`}
          >
            {loading ? 'Soumission en cours...' : user?.kyc_document ? 'Mettre à jour les documents' : 'Soumettre pour vérification'}
          </button>
        </form>
      )}
    </div>
  );
};

export default KYCVerification;
