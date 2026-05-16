import { useState } from 'react';
import { X, MapPin, Star, Share2, Heart, ChevronLeft, ChevronRight } from 'lucide-react';
import { DayPicker } from 'react-day-picker';
import { fr } from 'date-fns/locale';
import 'react-day-picker/dist/style.css';

export default function PropertyDetails({ property, onClose }) {
  const [selectedRange, setSelectedRange] = useState();
  const [currentImage, setCurrentImage] = useState(0);
  const images = property.images || ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=800&q=80"];

  return (
    <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 backdrop-blur-sm">
      <div className="bg-white rounded-2xl w-full max-w-5xl max-h-[90vh] overflow-y-auto relative">
        <button
          onClick={onClose}
          className="absolute right-4 top-4 bg-white/80 p-2 rounded-full hover:bg-white z-10 transition-colors shadow-sm"
        >
          <X size={24} />
        </button>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-0 md:gap-8 p-0 md:p-8">
          {/* Gallery Section */}
          <div className="space-y-4">
            <div className="relative aspect-video overflow-hidden md:rounded-xl">
              <img
                src={images[currentImage]}
                alt={property.title}
                className="w-full h-full object-cover"
              />
              {images.length > 1 && (
                <>
                  <button
                    onClick={() => setCurrentImage((prev) => (prev - 1 + images.length) % images.length)}
                    className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 p-2 rounded-full hover:bg-white"
                  >
                    <ChevronLeft size={20} />
                  </button>
                  <button
                    onClick={() => setCurrentImage((prev) => (prev + 1) % images.length)}
                    className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 p-2 rounded-full hover:bg-white"
                  >
                    <ChevronRight size={20} />
                  </button>
                </>
              )}
            </div>
            <div className="hidden md:grid grid-cols-4 gap-2">
              {images.map((img, i) => (
                <button
                  key={i}
                  onClick={() => setCurrentImage(i)}
                  className={`aspect-video rounded-lg overflow-hidden border-2 transition-all ${i === currentImage ? 'border-blue-600' : 'border-transparent'}`}
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

            <p className="text-gray-600 mb-8 leading-relaxed">
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
                <h4 className="font-semibold mb-3 text-gray-900">Disponibilité</h4>
                <div className="bg-white p-4 rounded-xl shadow-sm flex justify-center">
                  <DayPicker
                    mode="range"
                    selected={selectedRange}
                    onSelect={setSelectedRange}
                    locale={fr}
                    modifiersStyles={{
                        selected: { backgroundColor: '#2563eb', color: 'white' }
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
    </div>
  );
}
