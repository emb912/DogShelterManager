import React, { useState, useEffect } from "react";
import { CatSize, CatStatus, type Cat, type CatCreate } from "../types";
import { X } from "lucide-react";

interface CatFormProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (cat: CatCreate) => Promise<void>;
  initialData?: Cat | null;
  title: string;
}

const initialFormState: CatCreate = {
  name: "",
  size: CatSize.medium,
  birth_date: null,
  sex: "",
  neutered: false,
  admitted_date: new Date().toISOString().split("T")[0],
  released_date: null,
  status: CatStatus.arrived,
  indoor_only: false,
};

const sizeLabels = {
  [CatSize.small]: "Mały",
  [CatSize.medium]: "Średni",
  [CatSize.large]: "Duży",
};

const statusLabels = {
  [CatStatus.arrived]: "W schronisku",
  [CatStatus.adopted]: "Adoptowany",
  [CatStatus.returned]: "Zwrócony",
};

export const CatForm: React.FC<CatFormProps> = ({
  isOpen,
  onClose,
  onSubmit,
  initialData,
  title,
}) => {
  const [formData, setFormData] = useState<CatCreate>(initialFormState);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

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
      setError(null);
      await onSubmit(formData);
      onClose();
    } catch (error: any) {
      console.error(error);
      setError("Wystąpił błąd, sprawdź poprawność danych.");
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
          {error && <div className="text-red-500 text-sm mb-2">{error}</div>}
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
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-purple-500 outline-none transition-all"
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
                  setFormData({ ...formData, size: e.target.value as CatSize })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none"
              >
                {Object.values(CatSize).map((size) => (
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
                    status: e.target.value as CatStatus,
                  })
                }
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-emerald-500 outline-none"
              >
                {Object.values(CatStatus).map((status) => (
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
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none"
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
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none"
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
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 outline-none"
              >
                <option value="">Wybierz płeć</option>
                <option value="male">Kocur</option>
                <option value="female">Kotka</option>
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
                  className="w-4 h-4 text-purple-600 rounded focus:ring-purple-500 border-gray-300"
                />
                <span className="text-sm font-medium text-gray-700">
                  Wykastrowany
                </span>
              </label>
            </div>
          </div>

          <div className="flex items-center">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.indoor_only}
                onChange={(e) =>
                  setFormData({ ...formData, indoor_only: e.target.checked })
                }
                className="w-4 h-4 text-purple-600 rounded focus:ring-purple-500 border-gray-300"
              />
              <span className="text-sm font-medium text-gray-700">
                Tylko do domu (bez wychodzenia)
              </span>
            </label>
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
              className="px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors disabled:opacity-50"
            >
              {loading ? "Zapisywanie..." : "Zapisz"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
