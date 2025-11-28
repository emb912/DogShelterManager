import { useEffect, useState } from 'react';
import { useSocket } from './hooks/useSocket';
import { fetchDogs, createDog, updateDog, deleteDog } from './api/dogs';
import type { Dog, DogCreate } from './types';
import { DogCard } from './components/DogCard';
import { StatsOverview } from './components/StatsOverview';
import { DogForm } from './components/DogForm';
import { LayoutDashboard, Wifi, WifiOff, Plus } from 'lucide-react';

function App() {
  const { stats, isConnected, lastMessageTime } = useSocket();
  const [dogs, setDogs] = useState<Dog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // stan modalu
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingDog, setEditingDog] = useState<Dog | null>(null);

  const loadDogs = async () => {
    try {
      const data = await fetchDogs();
      setDogs(data);
      setError(null);
    } catch (err) {
      console.error(err);
      setError('Nie udało się pobrać listy psów.');
    } finally {
      setLoading(false);
    }
  };

  // załadowanie psów
  useEffect(() => {
    loadDogs();
  }, []);

  // odświeżanie jak socket wysyła zmiany
  useEffect(() => {
    if (lastMessageTime > 0) {
      loadDogs();
    }
  }, [lastMessageTime]);

  const handleCreate = async (dogData: DogCreate) => {
    await createDog(dogData);
    loadDogs();
  };

  const handleUpdate = async (dogData: DogCreate) => {
    if (!editingDog) return;
    await updateDog(editingDog.id, dogData);
    loadDogs();
  };

  const handleDelete = async (id: number) => {
    try {
      await deleteDog(id);
      loadDogs();
    } catch (error) {
      console.error('Failed to delete dog:', error);
      alert('Nie udało się usunąć psa.');
    }
  };

  const openCreateModal = () => {
    setEditingDog(null);
    setIsModalOpen(true);
  };

  const openEditModal = (dog: Dog) => {
    setEditingDog(dog);
    setIsModalOpen(true);
  };

  return (
    <div className="min-h-screen bg-lime-50 font-sans text-gray-900">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="bg-lime-600 p-2 rounded-lg">
              <LayoutDashboard className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-xl font-bold text-gray-800">Schronisko</h1>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-gray-50 border border-gray-200">
              {isConnected ? (
                <>
                  <Wifi className="w-4 h-4 text-lime-500" />
                  <span className="text-xs font-medium text-lime-700">Online</span>
                </>
              ) : (
                <>
                  <WifiOff className="w-4 h-4 text-gray-400" />
                  <span className="text-xs font-medium text-gray-500">Offline</span>
                </>
              )}
            </div>
            
            <button
              onClick={openCreateModal}
              className="flex items-center gap-2 px-4 py-2 bg-lime-600 text-white rounded-lg hover:bg-lime-700 transition-colors text-sm font-medium shadow-sm"
            >
              <Plus className="w-4 h-4" />
              Dodaj psa
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <StatsOverview stats={stats} />

        {/* Content */}
        <div className="mb-6 flex items-center justify-between">
          <h2 className="text-2xl font-bold text-gray-800">Lista podopiecznych</h2>
          <span className="text-sm text-gray-500">Ostatnia aktualizacja: {new Date().toLocaleTimeString()}</span>
        </div>

        {loading && dogs.length === 0 ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-lime-600"></div>
          </div>
        ) : error ? (
          <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200">
            {error}
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {dogs.map((dog) => (
              <DogCard 
                key={dog.id} 
                dog={dog} 
                onEdit={openEditModal}
                onDelete={handleDelete}
              />
            ))}
          </div>
        )}
        
        {!loading && dogs.length === 0 && !error && (
          <div className="text-center py-12 text-gray-500">
            Brak psów w bazie danych.
          </div>
        )}
      </main>

      <DogForm
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onSubmit={editingDog ? handleUpdate : handleCreate}
        initialData={editingDog}
        title={editingDog ? 'Edytuj psa' : 'Dodaj nowego psa'}
      />
    </div>
  );
}

export default App;


