import { useState } from 'react';
import { X, MapPin, Star, Share2, Heart, ChevronLeft, ChevronRight, Clock, ShieldCheck, CheckCircle, Loader2, Smartphone } from 'lucide-react';
import { DayPicker } from 'react-day-picker';
import { fr } from 'date-fns/locale';
import 'react-day-picker/dist/style.css';

export default function PropertyDetails({ property, onClose }) {
  const [step, setStep] = useState('details'); // 'details', 'payment', 'success'
  const [selectedRange, setSelectedRange] = useState();
  const [startTime, setStartTime] = useState('08:00');
  const [endTime, setEndTime] = useState('18:00');
  const [agreedToNoisePolicy, setAgreedToNoisePolicy] = useState(false);
  const [paymentLoading, setPaymentLoading] = useState(false);
  const [paymentMessage, setPaymentMessage] = useState('');
  const [selectedProvider, setSelectedProvider] = useState(null);
  const [bookingReference, setBookingReference] = useState('');
  const [currentImage, setCurrentImage] = useState(0);
  const [isFullScreen, setIsFullScreen] = useState(false);

  const images = property.images || ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=800&q=80"];

  const handlePayment = async (provider) => {
    setBookingReference(`GAB-${Math.random().toString(36).substr(2, 9).toUpperCase()}`);
    setSelectedProvider(provider);
    setPaymentLoading(true);

    const messages = [
      "Initialisation de la transaction sécurisée...",
      `Connexion à l'interface ${provider === 'airtel' ? 'Airtel Money' : 'Moov Money'}...`,
      "En attente de la validation OTP sur votre mobile...",
      "Traitement de l'autorisation de prélèvement...",
      "Paiement confirmé par l'opérateur !"
    ];

    for (const msg of messages) {
      setPaymentMessage(msg);
      await new Promise(resolve => setTimeout(resolve, 1500));
    }

    setPaymentLoading(false);
    setStep('success');
  };

  const isBookingValid = () => {
    if (!selectedRange || !selectedRange.from) return false;
    if (property.price_per_hour && (!startTime || !endTime)) return false;
    if (!agreedToNoisePolicy) return false;
    return true;
  };

  return (
    <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4 backdrop-blur-md">
      <div className="bg-white rounded-3xl w-full max-w-6xl max-h-[95vh] overflow-y-auto relative shadow-2xl animate-in fade-in zoom-in duration-300">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 bg-white/80 p-2 rounded-full hover:bg-white z-10 transition-colors shadow-sm"
        >
          <X size={24} />
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-0 md:gap-8 p-0 md:p-8">
          {/* Gallery Section */}
          <div className="space-y-4">
            <div className="relative aspect-[16/10] overflow-hidden md:rounded-2xl shadow-inner group bg-gray-100">
              <img
                src={images[currentImage]}
                alt={property.title}
                className="w-full h-full object-cover cursor-zoom-in transition-transform duration-500 hover:scale-105"
                onClick={() => setIsFullScreen(true)}
              />
              {images.length > 1 && (
                <>
                  <button
                    onClick={() => setCurrentImage((prev) => (prev - 1 + images.length) % images.length)}
                    className="absolute left-4 top-1/2 -translate-y-1/2 bg-white/90 p-3 rounded-full hover:bg-white transition-all shadow-lg opacity-0 group-hover:opacity-100"
                  >
                    <ChevronLeft size={24} />
                  </button>
                  <button
                    onClick={() => setCurrentImage((prev) => (prev + 1) % images.length)}
                    className="absolute right-4 top-1/2 -translate-y-1/2 bg-white/90 p-3 rounded-full hover:bg-white transition-all shadow-lg opacity-0 group-hover:opacity-100"
                  >
                    <ChevronRight size={24} />
                  </button>
                </>
              )}
              <div className="absolute bottom-4 right-4 bg-black/60 text-white px-3 py-1 rounded-full text-sm backdrop-blur-sm">
                {currentImage + 1} / {images.length}
              </div>
            </div>
            <div className="hidden md:grid grid-cols-5 gap-3">
              {images.map((img, i) => (
                <button
                  key={i}
                  onClick={() => setCurrentImage(i)}
                  className={`aspect-video rounded-xl overflow-hidden border-4 transition-all duration-200 ${i === currentImage ? 'border-blue-600 scale-95 shadow-md' : 'border-transparent hover:border-blue-200'}`}
                >
                  <img src={img} className="w-full h-full object-cover" alt="" />
                </button>
              ))}
            </div>
          </div>

          {/* Info Section */}
          <div className="p-6 md:p-0 flex flex-col">
            {step === 'details' && (
              <>
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="text-3xl font-bold text-gray-900 mb-2">{property.title}</h2>
                    <div className="flex items-center text-gray-600 gap-1 mb-2">
                      <MapPin size={18} />
                      <span>{property.neighborhood}, {property.city}, {property.province}</span>
                    </div>
                    <div className="flex items-center gap-4">
                        <span className="bg-blue-100 text-blue-700 text-sm font-semibold px-3 py-1 rounded-full">
                            {property.property_type}
                        </span>
                        <div className="flex items-center gap-1 text-yellow-500 font-bold">
                            <Star size={18} fill="currentColor" />
                            <span>4.8</span>
                        </div>
                    </div>
                  </div>
                  <div className="flex gap-2">
                    <button className="p-2 hover:bg-gray-100 rounded-full transition-colors"><Share2 size={20} /></button>
                    <button className="p-2 hover:bg-gray-100 rounded-full transition-colors"><Heart size={20} /></button>
                  </div>
                </div>

                <p className="text-gray-600 mb-6 leading-relaxed">
                  {property.description}
                </p>

                <div className="bg-gray-50 p-6 rounded-2xl border border-gray-100">
                  <div className="flex justify-between items-end mb-6">
                    <div>
                      <span className="text-2xl font-bold text-blue-600">
                        {property.price_per_day ? `${property.price_per_day.toLocaleString()} FCFA` : `${property.price_per_hour.toLocaleString()} FCFA`}
                      </span>
                      <span className="text-gray-500 ml-1">
                        {property.price_per_day ? '/ jour' : '/ heure'}
                      </span>
                    </div>
                  </div>

                  <div className="mb-6">
                    <h4 className="font-semibold mb-3 text-gray-900">1. Choisissez vos dates</h4>
                    <div className="bg-white p-4 rounded-xl shadow-sm flex justify-center border border-gray-100">
                      <DayPicker
                        mode="range"
                        selected={selectedRange}
                        onSelect={setSelectedRange}
                        locale={fr}
                        className="rdp-custom"
                        modifiersStyles={{
                            selected: { backgroundColor: '#2563eb', color: 'white' },
                            today: { color: '#2563eb', fontWeight: 'bold' }
                        }}
                      />
                    </div>
                  </div>

                  {property.price_per_hour && (
                    <div className="mb-6">
                      <h4 className="font-semibold mb-3 text-gray-900">2. Créneaux horaires</h4>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-1">
                          <label className="text-xs text-gray-500 font-medium">Début</label>
                          <div className="relative">
                            <Clock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={16} />
                            <input
                              type="time"
                              value={startTime}
                              onChange={(e) => setStartTime(e.target.value)}
                              className="w-full pl-10 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                          </div>
                        </div>
                        <div className="space-y-1">
                          <label className="text-xs text-gray-500 font-medium">Fin</label>
                          <div className="relative">
                            <Clock className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={16} />
                            <input
                              type="time"
                              value={endTime}
                              onChange={(e) => setEndTime(e.target.value)}
                              className="w-full pl-10 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
                            />
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  <div className="mb-6 p-4 bg-amber-50 border border-amber-100 rounded-xl">
                    <div className="flex gap-3">
                      <input
                        type="checkbox"
                        id="noise-policy"
                        checked={agreedToNoisePolicy}
                        onChange={(e) => setAgreedToNoisePolicy(e.target.checked)}
                        className="mt-1 w-5 h-5 rounded border-amber-300 text-amber-600 focus:ring-amber-500"
                      />
                      <label htmlFor="noise-policy" className="text-sm text-amber-900 leading-tight">
                        <span className="font-bold block mb-1">Clause de Tapage Nocturne</span>
                        J'accepte de respecter le voisinage. En cas de tapage nocturne avéré, ma caution de 100 000 FCFA pourra être retenue.
                      </label>
                    </div>
                  </div>

                  <button
                    disabled={!isBookingValid()}
                    onClick={() => setStep('payment')}
                    className={`w-full font-bold py-4 rounded-xl transition-all shadow-lg ${
                      isBookingValid()
                        ? 'bg-blue-600 hover:bg-blue-700 text-white shadow-blue-200'
                        : 'bg-gray-200 text-gray-400 cursor-not-allowed shadow-none'
                    }`}
                  >
                    Procéder au paiement
                  </button>
                </div>
              </>
            )}

            {step === 'payment' && (
              <div className="flex flex-col h-full animate-in slide-in-from-right duration-300">
                <button
                  onClick={() => setStep('details')}
                  className="flex items-center gap-2 text-gray-500 hover:text-blue-600 mb-6 transition-colors font-medium"
                >
                  <ChevronLeft size={20} />
                  Retour aux détails
                </button>

                <h2 className="text-3xl font-bold text-gray-900 mb-2">Paiement Mobile Money</h2>
                <p className="text-gray-600 mb-8">Sélectionnez votre opérateur pour finaliser la réservation.</p>

                <div className="bg-blue-50 p-6 rounded-2xl mb-8 border border-blue-100">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 font-medium">Total à régler</span>
                    <span className="text-2xl font-bold text-blue-700">
                       {property.price_per_day ? `${property.price_per_day.toLocaleString()} FCFA` : `${property.price_per_hour.toLocaleString()} FCFA`}
                    </span>
                  </div>
                </div>

                <div className="grid grid-cols-1 gap-4 mb-8">
                  <button
                    onClick={() => handlePayment('airtel')}
                    className="flex items-center justify-between p-5 border-2 border-gray-100 rounded-2xl hover:border-red-500 hover:bg-red-50 transition-all group"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-red-600 rounded-xl flex items-center justify-center text-white font-black text-xl italic">A</div>
                      <div className="text-left">
                        <p className="font-bold text-gray-900 group-hover:text-red-700">Airtel Money</p>
                        <p className="text-sm text-gray-500">Paiement instantané</p>
                      </div>
                    </div>
                    <Smartphone className="text-gray-300 group-hover:text-red-500" />
                  </button>

                  <button
                    onClick={() => handlePayment('moov')}
                    className="flex items-center justify-between p-5 border-2 border-gray-100 rounded-2xl hover:border-blue-500 hover:bg-blue-50 transition-all group"
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-blue-500 rounded-xl flex items-center justify-center text-white font-black text-xl italic">M</div>
                      <div className="text-left">
                        <p className="font-bold text-gray-900 group-hover:text-blue-700">Moov Money</p>
                        <p className="text-sm text-gray-500">Sécurisé par Moov</p>
                      </div>
                    </div>
                    <Smartphone className="text-gray-300 group-hover:text-blue-500" />
                  </button>
                </div>

                <div className="mt-auto flex items-center gap-3 p-4 bg-gray-50 rounded-xl text-gray-500 text-sm">
                  <ShieldCheck className="text-green-600 shrink-0" size={20} />
                  Paiement sécurisé conforme aux normes de la DIGIEG et de l'ANINF.
                </div>
              </div>
            )}

            {step === 'success' && (
              <div className="flex flex-col items-center justify-center h-full text-center py-12 animate-in zoom-in duration-500">
                <div className="w-24 h-24 bg-green-100 text-green-600 rounded-full flex items-center justify-center mb-6 shadow-lg shadow-green-100">
                  <CheckCircle size={56} />
                </div>
                <h2 className="text-3xl font-bold text-gray-900 mb-2">Réservation Confirmée !</h2>
                <p className="text-gray-600 mb-8 max-w-sm">
                  Votre paiement a été validé avec succès. Vous recevrez un SMS avec le code d'accès Jeedom 15 minutes avant votre arrivée.
                </p>

                <div className="w-full bg-gray-50 p-6 rounded-2xl border border-gray-100 mb-8 text-left space-y-3">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Référence</span>
                    <span className="font-mono font-bold text-gray-900">{bookingReference}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Bien</span>
                    <span className="font-bold text-gray-900">{property.title}</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Opérateur</span>
                    <span className="font-bold text-gray-900 capitalize">{selectedProvider} Money</span>
                  </div>
                </div>

                <button
                  onClick={onClose}
                  className="w-full bg-gray-900 hover:bg-black text-white font-bold py-4 rounded-xl transition-all shadow-xl"
                >
                  Fermer
                </button>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Payment Loading Overlay */}
      {paymentLoading && (
        <div className="fixed inset-0 bg-white/90 z-[70] backdrop-blur-sm flex flex-col items-center justify-center p-6 text-center animate-in fade-in duration-300">
          <div className="relative mb-8">
            <div className="w-20 h-20 border-4 border-blue-100 rounded-full" />
            <div className="w-20 h-20 border-4 border-blue-600 rounded-full border-t-transparent animate-spin absolute top-0 left-0" />
            <Loader2 className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-blue-600" size={32} />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Traitement en cours...</h3>
          <p className="text-blue-600 font-medium animate-pulse">{paymentMessage}</p>
          <p className="mt-8 text-xs text-gray-400 italic">Ne fermez pas cette fenêtre pendant la validation.</p>
        </div>
      )}

      {/* Full Screen Overlay */}
      {isFullScreen && (
        <div
            className="fixed inset-0 bg-black/95 z-[60] flex items-center justify-center animate-in fade-in duration-300"
            onClick={() => setIsFullScreen(false)}
        >
            <button className="absolute top-6 right-6 text-white hover:scale-110 transition-transform bg-white/10 p-2 rounded-full">
                <X size={32} />
            </button>

            <div className="relative max-w-5xl max-h-[85vh] group px-4">
                <img src={images[currentImage]} className="w-full h-full object-contain rounded-lg shadow-2xl" alt="" />

                {images.length > 1 && (
                    <>
                        <button
                            onClick={(e) => { e.stopPropagation(); setCurrentImage((prev) => (prev - 1 + images.length) % images.length); }}
                            className="absolute left-[-4rem] top-1/2 -translate-y-1/2 text-white/50 hover:text-white transition-colors p-4"
                        >
                            <ChevronLeft size={64} />
                        </button>
                        <button
                            onClick={(e) => { e.stopPropagation(); setCurrentImage((prev) => (prev + 1) % images.length); }}
                            className="absolute right-[-4rem] top-1/2 -translate-y-1/2 text-white/50 hover:text-white transition-colors p-4"
                        >
                            <ChevronRight size={64} />
                        </button>
                    </>
                )}
            </div>

            <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex gap-3 overflow-x-auto max-w-full px-4 no-scrollbar">
                {images.map((img, i) => (
                    <button
                        key={i}
                        onClick={(e) => { e.stopPropagation(); setCurrentImage(i); }}
                        className={`w-20 aspect-video rounded-md overflow-hidden border-2 transition-all shrink-0 ${i === currentImage ? 'border-blue-500 scale-110 shadow-lg' : 'border-white/20 hover:border-white/50'}`}
                    >
                        <img src={img} className="w-full h-full object-cover" alt="" />
                    </button>
                ))}
            </div>
        </div>
      )}
    </div>
  );
}
