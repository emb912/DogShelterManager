import React, { useState, useEffect } from "react";
import { DogSize, DogStatus, type Dog, type DogCreate } from "../types";
import { X } from "lucide-react";

interface DogFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (dog: DogCreate) => Promise<void>;
  initialData?: Dog | null;
  title: string;
}

const initialFormState: DogCreate = {
  name: "",
  size: DogSize.medium,
  birth_date: null,
  sex: "",
  neutered: false,
  admitted_date: new Date().toISOString().split("T")[0],
  released_date: null,
  status: DogStatus.arrived,
};

const sizeLabels = {
  [DogSize.small]: "Mały",
  [DogSize.medium]: "Średni",
  [DogSize.large]: "Duży",
};

const statusLabels = {
  [DogStatus.arrived]: "W schronisku",
  [DogStatus.adopted]: "Adoptowany",
  [DogStatus.returned]: "Zwrócony",
};

export const DogForm: React.FC<DogFormProps> = ({
  isOpen,
  onClose,
  onSubmit,
  initialData,
  title,
}) => {
  const [formData, setFormData] = useState<DogCreate>(initialFormState);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (initialData) {
      setFormData({
        ...initialData,
        birth_date: initialData.birth_date || null,
        released_date: initialData.released_date || null,
      });
    } else {
      setFormData(initialFormState);
    }
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    try {
      await onSubmit(formData);
      onClose();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm">
      <div className="bg-white rounded-xl shadow-2xl w-full max-w-md overflow-hidden">
        <div className="flex justify-between items-center p-4 border-b border-gray-100">
          <h2 className="text-xl font-bold text-gray-800">{title}</h2>
          <button
            onClick={onClose}
            className="p-1 hover:bg-gray-100 rounded-full transition-colors"
          >
            <X className="w-5 h-5 text-gray-500" />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Imię
            </label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) =>
                setFormData({ ...formData, name: e.target.value })
              }
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-lime-500 focus:border-lime-500 outline-none transition-all"
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Rozmiar
              </label>
              <select
                value={formData.size}
                onChange={(e) =>
                  setFormData({ ...formData, size: e.target.value as DogSize })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-lime-500 outline-none"
              >
                {Object.values(DogSize).map((size) => (
                  <option key={size} value={size}>
                    {sizeLabels[size]}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Status
              </label>
              <select
                value={formData.status}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    status: e.target.value as DogStatus,
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none"
              >
                {Object.values(DogStatus).map((status) => (
                  <option key={status} value={status}>
                    {statusLabels[status]}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Data przyjęcia
              </label>
              <input
                type="date"
                required
                value={formData.admitted_date}
                onChange={(e) =>
                  setFormData({ ...formData, admitted_date: e.target.value })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-lime-500 outline-none"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Data urodzenia
              </label>
              <input
                type="date"
                value={formData.birth_date || ""}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    birth_date: e.target.value || null,
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-lime-500 outline-none"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Płeć
              </label>
              <select
                required
                value={formData.sex || ""}
                onChange={(e) =>
                  setFormData({ ...formData, sex: e.target.value || null })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-lime-500 outline-none"
              >
                <option value="">Wybierz płeć</option>
                <option value="male">Samiec</option>
                <option value="female">Samica</option>
              </select>
            </div>

            <div className="flex items-center pt-6">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={formData.neutered}
                  onChange={(e) =>
                    setFormData({ ...formData, neutered: e.target.checked })
                  }
                  className="w-4 h-4 text-lime-600 rounded focus:ring-lime-500 border-gray-300"
                />
                <span className="text-sm font-medium text-gray-700">
                  Wykastrowany
                </span>
              </label>
            </div>
          </div>

          <div className="pt-4 flex justify-end gap-3">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 transition-colors"
            >
              Anuluj
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 text-sm font-medium text-white bg-lime-600 rounded-lg hover:bg-lime-700 transition-colors disabled:opacity-50"
            >
              {loading ? "Zapisywanie..." : "Zapisz"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
