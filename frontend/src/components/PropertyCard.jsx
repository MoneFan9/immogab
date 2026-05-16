import { useState } from 'react';
import { ChevronLeft, ChevronRight, MapPin, Calendar } from 'lucide-react';

export default function PropertyCard({ property, onClick }) {
  const [currentImage, setCurrentImage] = useState(0);

  const images = property.images || ["https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=800&q=80"];

  const nextImage = (e) => {
    e.stopPropagation();
    setCurrentImage((prev) => (prev + 1) % images.length);
  };

  const prevImage = (e) => {
    e.stopPropagation();
    setCurrentImage((prev) => (prev - 1 + images.length) % images.length);
  };

  return (
    <div
      className="bg-white rounded-xl shadow-md overflow-hidden cursor-pointer hover:shadow-lg transition-shadow group"
      onClick={() => onClick(property)}
    >
      <div className="relative h-64 overflow-hidden">
        <img
          src={images[currentImage]}
          alt={property.title}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
        />

        {images.length > 1 && (
          <>
            <button
              onClick={prevImage}
              className="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 p-1 rounded-full hover:bg-white transition-colors"
            >
              <ChevronLeft size={20} />
            </button>
            <button
              onClick={nextImage}
              className="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 p-1 rounded-full hover:bg-white transition-colors"
            >
              <ChevronRight size={20} />
            </button>
          </>
        )}

        <div className="absolute bottom-2 left-1/2 -translate-x-1/2 flex gap-1">
          {images.map((_, i) => (
            <div
              key={i}
              className={`w-1.5 h-1.5 rounded-full ${i === currentImage ? 'bg-white' : 'bg-white/50'}`}
            />
          ))}
        </div>

        <div className="absolute top-2 right-2 bg-blue-600 text-white text-xs font-bold px-2 py-1 rounded">
          {property.property_type}
        </div>
      </div>

      <div className="p-4">
        <div className="flex justify-between items-start mb-2">
          <h3 className="font-bold text-lg text-gray-800 line-clamp-1">{property.title}</h3>
          <div className="text-right">
            <span className="text-blue-600 font-bold">
              {property.price_per_day ? `${property.price_per_day.toLocaleString()} FCFA` : `${property.price_per_hour.toLocaleString()} FCFA`}
            </span>
            <span className="text-gray-500 text-xs block">
              {property.price_per_day ? '/ jour' : '/ heure'}
            </span>
          </div>
        </div>

        <div className="flex items-center text-gray-500 text-sm mb-4">
          <MapPin size={16} className="mr-1" />
          <span>{property.city}, {property.province}</span>
        </div>

        <button className="w-full bg-gray-50 hover:bg-blue-50 text-blue-600 font-semibold py-2 rounded-lg transition-colors flex items-center justify-center gap-2 border border-blue-100">
          <Calendar size={18} />
          Vérifier la disponibilité
        </button>
      </div>
    </div>
  );
}
