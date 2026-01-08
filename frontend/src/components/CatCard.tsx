import React from "react";
import { CatStatus, CatSize, type Cat } from "../types";
import {
  Calendar,
  Cat as CatIcon,
  Activity,
  Syringe,
  Pencil,
  Trash2,
  Home,
} from "lucide-react";
import { format } from "date-fns";

interface CatCardProps {
  cat: Cat;
  onEdit: (cat: Cat) => void;
  onDelete: (id: number) => void;
}

const statusColors = {
  [CatStatus.arrived]: "bg-emerald-100 text-emerald-800 border-emerald-200",
  [CatStatus.adopted]: "bg-rose-100 text-rose-600 border-rose-200",
  [CatStatus.returned]: "bg-amber-100 text-amber-800 border-amber-200",
};

const sizeLabels = {
  [CatSize.small]: "Mały",
  [CatSize.medium]: "Średni",
  [CatSize.large]: "Duży",
};

export const CatCard: React.FC<CatCardProps> = ({ cat, onEdit, onDelete }) => {
  return (
    <div className="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 border border-gray-100 flex flex-col">
      <div className="p-5 flex-1">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
            <CatIcon className="w-5 h-5 text-purple-600" />
            {cat.name}
          </h3>
          <span
            className={`px-3 py-1 rounded-full text-xs font-semibold border ${
              statusColors[cat.status]
            }`}
          >
            {cat.status === CatStatus.arrived
              ? "W schronisku"
              : cat.status === CatStatus.adopted
              ? "Adoptowany"
              : "Zwrócony"}
          </span>
        </div>

        <div className="space-y-3 text-sm text-gray-600">
          <div className="flex items-center gap-2">
            <Activity className="w-4 h-4 text-gray-400" />
            <span>
              Rozmiar:{" "}
              <span className="font-medium text-gray-800">
                {sizeLabels[cat.size]}
              </span>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <Calendar className="w-4 h-4 text-gray-400" />
            <span>
              Przyjęty:{" "}
              <span className="font-medium text-gray-800">
                {format(new Date(cat.admitted_date), "dd.MM.yyyy")}
              </span>
            </span>
          </div>

          {cat.birth_date && (
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-gray-400" />
              <span>
                Urodzony:{" "}
                <span className="font-medium text-gray-800">
                  {format(new Date(cat.birth_date), "dd.MM.yyyy")}
                </span>
              </span>
            </div>
          )}

          <div className="flex items-center gap-2">
            <Syringe
              className={`w-4 h-4 ${
                cat.neutered ? "text-purple-500" : "text-gray-400"
              }`}
            />
            <span>
              Kastracja:{" "}
              <span className="font-medium text-gray-800">
                {cat.neutered ? "Tak" : "Nie"}
              </span>
            </span>
          </div>

          <div className="flex items-center gap-2">
            <Home
              className={`w-4 h-4 ${
                cat.indoor_only ? "text-purple-500" : "text-gray-400"
              }`}
            />
            <span>
              Tylko dom:{" "}
              <span className="font-medium text-gray-800">
                {cat.indoor_only ? "Tak" : "Nie"}
              </span>
            </span>
          </div>
        </div>
      </div>

      <div className="bg-gray-50 px-5 py-3 border-t border-gray-100 flex justify-between items-center text-xs text-gray-500">
        <div className="flex gap-2">
          <span>ID: #{cat.id}</span>
          <span>•</span>
          <span>
            {cat.sex === "male"
              ? "Kocur"
              : cat.sex === "female"
              ? "Kotka"
              : "Płeć nieznana"}
          </span>
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => onEdit(cat)}
            className="p-1.5 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
            title="Edytuj"
          >
            <Pencil className="w-4 h-4" />
          </button>
          <button
            onClick={() => {
              if (window.confirm("Czy na pewno chcesz usunąć tego kota?")) {
                onDelete(cat.id);
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
