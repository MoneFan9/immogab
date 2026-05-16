import { useState, useEffect } from 'react';
import { Upload, CheckCircle, AlertCircle, Clock, FileText, X, ImageIcon, FileCheck } from 'lucide-react';
import { userService } from '../services/userService';

const KYCVerification = ({ user, onUpdate, onClose }) => {
  const [file, setFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [cniNumber, setCniNumber] = useState(user?.cni_number || '');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState(null);

  useEffect(() => {
    let url;
    if (file && file.type.startsWith('image/')) {
      url = URL.createObjectURL(file);
      setPreviewUrl(url);
    } else {
      setPreviewUrl(null);
    }

    return () => {
      if (url) URL.revokeObjectURL(url);
    };
  }, [file]);

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
        <div className="flex items-center gap-2 text-emerald-700 bg-emerald-50 border border-emerald-200 px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-wider shadow-sm animate-pulse">
          <CheckCircle size={16} className="text-emerald-600" />
          Compte Certifié (Loi 025/2021)
        </div>
      );
    }
    if (user?.kyc_document) {
      return (
        <div className="flex items-center gap-2 text-amber-700 bg-amber-50 border border-amber-200 px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-wider shadow-sm">
          <Clock size={16} className="text-amber-600" />
          Examen en cours
        </div>
      );
    }
    return (
      <div className="flex items-center gap-2 text-slate-500 bg-slate-50 border border-slate-200 px-4 py-1.5 rounded-full text-xs font-black uppercase tracking-wider shadow-sm">
        <AlertCircle size={16} className="text-slate-400" />
        Action requise
      </div>
    );
  };

  return (
    <div className="p-0 overflow-hidden rounded-2xl">
      <div className="bg-slate-900 p-6 flex justify-between items-center text-white">
        <div>
          <h2 className="text-2xl font-bold">Vérification KYC</h2>
          <p className="text-slate-400 text-sm mt-1">Sécurisez vos transactions immobilières</p>
        </div>
        <button onClick={onClose} className="p-2 hover:bg-white/10 rounded-full transition-colors">
          <X size={24} />
        </button>
      </div>

      <div className="p-6">
        <div className="mb-8">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-4">
            <p className="text-gray-600 max-w-sm">
              Pour respecter la réglementation gabonaise, une pièce d'identité valide est requise pour toute activité sur ImmoGab.
            </p>
            {getStatusBadge()}
          </div>
          <div className="h-px bg-gray-100 w-full" />
        </div>

        {user?.is_kyc_verified ? (
          <div className="bg-green-50 border-2 border-green-200 rounded-2xl p-10 text-center animate-in fade-in zoom-in duration-500">
              <div className="bg-green-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6 border-4 border-white shadow-lg">
                <CheckCircle className="text-green-600" size={40} />
              </div>
              <h3 className="text-2xl font-bold text-green-900 mb-2">Félicitations, {user.username} !</h3>
              <p className="text-green-700 mb-6 max-w-xs mx-auto">Votre identité a été validée avec succès. Vous avez désormais un accès complet à la plateforme.</p>
              <button
                onClick={onClose}
                className="px-8 py-3 bg-green-600 text-white font-bold rounded-xl hover:bg-green-700 transition-all shadow-lg shadow-green-200"
              >
                Continuer
              </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="space-y-6">
              <div>
                <label className="block text-sm font-bold text-slate-700 mb-2">
                  Numéro de CNI / Passeport / Titre de Séjour
                </label>
                <div className="relative">
                  <FileText className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
                  <input
                    type="text"
                    className="w-full pl-12 pr-4 py-3.5 rounded-xl border-2 border-slate-100 focus:border-blue-500 focus:ring-0 transition-all bg-slate-50 placeholder:text-slate-400 font-medium"
                    placeholder="Entrez le numéro de votre pièce"
                    value={cniNumber}
                    onChange={(e) => setCniNumber(e.target.value)}
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-bold text-slate-700 mb-2">
                  Téléchargement du document (Recto-Verso)
                </label>
                <div
                  className={`relative border-2 border-dashed rounded-2xl transition-all duration-300 group overflow-hidden ${
                    file
                      ? 'border-blue-500 bg-blue-50/50'
                      : user?.kyc_document
                        ? 'border-amber-400 bg-amber-50/30'
                        : 'border-slate-200 hover:border-blue-500 hover:bg-blue-50/20 hover:shadow-inner'
                  }`}
                >
                  <input
                    type="file"
                    id="kyc-file"
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                    accept=".jpg,.jpeg,.png,.pdf"
                    onChange={handleFileChange}
                  />

                  <div className="p-8 text-center">
                    {file ? (
                      <div className="flex flex-col items-center animate-in fade-in slide-in-from-bottom-2 duration-300">
                        {previewUrl ? (
                          <div className="relative mb-4">
                            <img src={previewUrl} alt="Preview" className="w-32 h-32 object-cover rounded-xl shadow-md border-2 border-white" />
                            <div className="absolute -top-2 -right-2 bg-blue-600 text-white p-1 rounded-full shadow-lg">
                              <ImageIcon size={16} />
                            </div>
                          </div>
                        ) : (
                          <div className="bg-blue-100 p-5 rounded-2xl mb-4 shadow-sm">
                            <FileText className="text-blue-600" size={40} />
                          </div>
                        )}
                        <span className="text-slate-900 font-extrabold truncate max-w-xs">{file.name}</span>
                        <div className="flex items-center gap-2 mt-1">
                          <span className="text-slate-500 text-[10px] uppercase font-black tracking-widest bg-white px-2 py-0.5 rounded border border-slate-100">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                          </span>
                          <span className="text-blue-600 text-[10px] uppercase font-black tracking-widest bg-blue-50 px-2 py-0.5 rounded border border-blue-100">
                            {file.type.split('/')[1] || 'FILE'}
                          </span>
                        </div>
                        <button
                          type="button"
                          onClick={(e) => { e.preventDefault(); e.stopPropagation(); setFile(null); }}
                          className="mt-6 px-6 py-2 text-xs text-red-600 font-black uppercase tracking-widest bg-red-50 rounded-xl hover:bg-red-100 transition-all border border-red-100 hover:shadow-sm z-20 relative"
                        >
                          Changer le document
                        </button>
                      </div>
                    ) : user?.kyc_document ? (
                      <div className="flex flex-col items-center">
                        <div className="bg-amber-100 p-5 rounded-2xl mb-4 shadow-sm">
                          <Clock className="text-amber-600" size={40} />
                        </div>
                        <span className="text-slate-900 font-extrabold">Document en cours d'examen</span>
                        <p className="text-slate-500 text-xs mt-2 max-w-[200px] leading-relaxed">
                          Votre dossier est déjà dans notre file d'attente. Vous pouvez le remplacer si besoin.
                        </p>
                        <span className="mt-4 px-4 py-1.5 bg-amber-100 text-amber-700 text-[10px] font-black uppercase tracking-widest rounded-full">
                          Cliquer pour modifier
                        </span>
                      </div>
                    ) : (
                      <div className="flex flex-col items-center group-hover:transform group-hover:scale-105 transition-all duration-500">
                        <div className="bg-slate-100 p-5 rounded-2xl mb-4 group-hover:bg-blue-600 transition-colors shadow-sm">
                          <Upload className="text-slate-400 group-hover:text-white" size={40} />
                        </div>
                        <span className="text-slate-900 font-extrabold text-lg">Déposez votre pièce d'identité</span>
                        <p className="text-slate-500 text-sm mt-1 max-w-[240px]">
                          Glissez-déposez ou <span className="text-blue-600 font-bold">parcourez vos fichiers</span>
                        </p>
                        <div className="flex gap-4 mt-6">
                            <div className="flex items-center gap-1.5 text-slate-400">
                                <ImageIcon size={14} />
                                <span className="text-[10px] font-bold uppercase tracking-tight">JPG/PNG</span>
                            </div>
                            <div className="flex items-center gap-1.5 text-slate-400">
                                <FileText size={14} />
                                <span className="text-[10px] font-bold uppercase tracking-tight">PDF</span>
                            </div>
                            <div className="flex items-center gap-1.5 text-slate-400">
                                <FileCheck size={14} />
                                <span className="text-[10px] font-bold uppercase tracking-tight">MAX 5MO</span>
                            </div>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>

            {message && (
              <div className={`p-4 rounded-xl flex items-center gap-3 animate-in slide-in-from-top-2 duration-300 ${
                message.type === 'success' ? 'bg-green-50 text-green-700 border border-green-100' : 'bg-red-50 text-red-700 border border-red-100'
              }`}>
                {message.type === 'success' ? <CheckCircle size={20} className="shrink-0" /> : <AlertCircle size={20} className="shrink-0" />}
                <span className="text-sm font-bold">{message.text}</span>
              </div>
            )}

            <button
              type="submit"
              disabled={loading || (user?.kyc_document && !file)}
              className={`w-full py-4 rounded-xl font-extrabold text-white transition-all shadow-xl flex items-center justify-center gap-2 ${
                loading || (user?.kyc_document && !file)
                  ? 'bg-slate-200 cursor-not-allowed text-slate-400'
                  : 'bg-blue-600 hover:bg-blue-700 shadow-blue-200 hover:-translate-y-0.5 active:translate-y-0'
              }`}
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Traitement sécurisé...
                </>
              ) : user?.kyc_document ? (
                'Mettre à jour mes documents'
              ) : (
                'Soumettre mon dossier KYC'
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default KYCVerification;
