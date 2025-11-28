import React from 'react';
import { DogStatus, DogSize, type Dog } from '../types';
import { Calendar, PawPrint, Activity, Syringe, Pencil, Trash2 } from 'lucide-react';
import { format } from 'date-fns';

interface DogCardProps {
  dog: Dog;
  onEdit: (dog: Dog) => void;
  onDelete: (id: number) => void;
}

const statusColors = {
  [DogStatus.arrived]: 'bg-emerald-100 text-emerald-800 border-emerald-200',
  [DogStatus.adopted]: 'bg-rose-100 text-rose-600 border-rose-200',
  [DogStatus.returned]: 'bg-amber-100 text-amber-800 border-amber-200',
};

const sizeLabels = {
  [DogSize.small]: 'Mały',
  [DogSize.medium]: 'Średni',
  [DogSize.large]: 'Duży',
};

export const DogCard: React.FC<DogCardProps> = ({ dog, onEdit, onDelete }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 border border-gray-100 flex flex-col">
      <div className="p-5 flex-1">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <PawPrint className="w-5 h-5 text-lime-600" />
            {dog.name}
          </h3>
          <span className={`px-3 py-1 rounded-full text-xs font-semibold border ${statusColors[dog.status]}`}>
            {dog.status === DogStatus.arrived ? 'W schronisku' : 
             dog.status === DogStatus.adopted ? 'Adoptowany' : 'Zwrócony'}
          </span>
        </div>

        <div className="space-y-3 text-sm text-gray-600">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-gray-400" />
            <span>Rozmiar: <span className="font-medium text-gray-800">{sizeLabels[dog.size]}</span></span>
          </div>
          
          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-gray-400" />
            <span>Przyjęty: <span className="font-medium text-gray-800">{format(new Date(dog.admitted_date), 'dd.MM.yyyy')}</span></span>
          </div>

          {dog.birth_date && (
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-gray-400" />
              <span>Urodzony: <span className="font-medium text-gray-800">{format(new Date(dog.birth_date), 'dd.MM.yyyy')}</span></span>
            </div>
          )}

          <div className="flex items-center gap-2">
             <Syringe className={`w-4 h-4 ${dog.neutered ? 'text-lime-500' : 'text-gray-400'}`} />
             <span>Kastracja: <span className="font-medium text-gray-800">{dog.neutered ? 'Tak' : 'Nie'}</span></span>
          </div>
        </div>
      </div>
      
      <div className="bg-gray-50 px-5 py-3 border-t border-gray-100 flex justify-between items-center text-xs text-gray-500">
        <div className="flex gap-2">
          <span>ID: #{dog.id}</span>
          <span>•</span>
          <span>{dog.sex === 'male' ? 'Samiec' : dog.sex === 'female' ? 'Samica' : 'Płeć nieznana'}</span>
        </div>
        <div className="flex gap-2">
          <button 
            onClick={() => onEdit(dog)}
            className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
            title="Edytuj"
          >
            <Pencil className="w-4 h-4" />
          </button>
          <button 
            onClick={() => {
              if (window.confirm('Czy na pewno chcesz usunąć tego psa?')) {
                onDelete(dog.id);
              }
            }}
            className="p-1.5 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
            title="Usuń"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
