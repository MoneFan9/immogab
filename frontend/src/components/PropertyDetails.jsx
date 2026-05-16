import { useState } from 'react';
import { X, MapPin, Star, Share2, Heart, ChevronLeft, ChevronRight } from 'lucide-react';
import { DayPicker } from 'react-day-picker';
import { fr } from 'date-fns/locale';
import 'react-day-picker/dist/style.css';

export default function PropertyDetails({ property, onClose }) {
  const [selectedRange, setSelectedRange] = useState();
  const [currentImage, setCurrentImage] = useState(0);
  const [isFullScreen, setIsFullScreen] = useState(false);
  const images = property.images || ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=800&q=80"];

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
                key={currentImage}
                src={images[currentImage]}
                alt={property.title}
                className="w-full h-full object-cover cursor-zoom-in transition-all duration-500 ease-in-out hover:scale-105 animate-in fade-in"
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

            <div className="mb-8 bg-blue-50/50 p-4 rounded-2xl border border-blue-100">
              <h4 className="font-bold text-blue-900 mb-3 flex items-center gap-2">
                <Star size={18} className="text-blue-600" />
                Règlement de la maison
              </h4>
              <ul className="text-sm text-blue-800 space-y-2">
                <li className="flex items-start gap-2">
                  <span className="w-1.5 h-1.5 bg-blue-600 rounded-full mt-1.5 shrink-0" />
                  Respect du voisinage : Tapage nocturne strictement interdit sous peine d'amende (Loi Gabonaise).
                </li>
                <li className="flex items-start gap-2">
                  <span className="w-1.5 h-1.5 bg-blue-600 rounded-full mt-1.5 shrink-0" />
                  Accès autonome : Check-in via serrure connectée IoT à l'heure exacte de début.
                </li>
                <li className="flex items-start gap-2">
                  <span className="w-1.5 h-1.5 bg-blue-600 rounded-full mt-1.5 shrink-0" />
                  Caution : Dépôt de garantie géré par le système Escrow d'ImmoGab.
                </li>
              </ul>
            </div>

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
                <h4 className="font-semibold mb-3 text-gray-900">Disponibilité</h4>
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

              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-4 rounded-xl transition-all shadow-lg shadow-blue-200">
                Réserver maintenant
              </button>
              <p className="text-center text-gray-400 text-xs mt-4 italic">
                Aucun paiement n'est requis à cette étape
              </p>
            </div>
          </div>
        </div>
      </div>
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
