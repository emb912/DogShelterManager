import { useEffect, useState } from "react";
import { useSocket } from "./hooks/useSocket";
import { useCatSocket } from "./hooks/useCatSocket";
import { useServerStatus } from "./hooks/useServerStatus";
import { fetchDogs, createDog, updateDog, deleteDog } from "./api/dogs";
import { fetchCats, createCat, updateCat, deleteCat } from "./api/cats";
import type { Dog, DogCreate, Cat, CatCreate } from "./types";
import { DogCard } from "./components/DogCard";
import { CatCard } from "./components/CatCard";
import { StatsOverview } from "./components/StatsOverview";
import { CatStatsOverview } from "./components/CatStatsOverview";
import { DogForm } from "./components/DogForm";
import { CatForm } from "./components/CatForm";
import { ServerStatusPanel } from "./components/ServerStatusPanel";
import {
  LayoutDashboard,
  Plus,
  Dog as DogIcon,
  Cat as CatIcon,
  PawPrint,
} from "lucide-react";

type ActiveTab = "all" | "dogs" | "cats";

function App() {
  const {
    stats: dogStats,
    isConnected: isDogConnected,
    lastMessageTime: dogLastMessage,
  } = useSocket();
  const {
    stats: catStats,
    isConnected: isCatConnected,
    lastMessageTime: catLastMessage,
  } = useCatSocket();
  const { serverStatus, isConnected: isStatusConnected } = useServerStatus();

  const [activeTab, setActiveTab] = useState<ActiveTab>("all");

  // Stan dla psów
  const [dogs, setDogs] = useState<Dog[]>([]);
  const [loadingDogs, setLoadingDogs] = useState(true);
  const [dogError, setDogError] = useState<string | null>(null);
  const [isDogModalOpen, setIsDogModalOpen] = useState(false);
  const [editingDog, setEditingDog] = useState<Dog | null>(null);

  // Stan dla kotów
  const [cats, setCats] = useState<Cat[]>([]);
  const [loadingCats, setLoadingCats] = useState(true);
  const [catError, setCatError] = useState<string | null>(null);
  const [isCatModalOpen, setIsCatModalOpen] = useState(false);
  const [editingCat, setEditingCat] = useState<Cat | null>(null);

  const isConnected = isDogConnected || isCatConnected || isStatusConnected;

  const loadDogs = async () => {
    try {
      const data = await fetchDogs();
      setDogs(data);
      setDogError(null);
    } catch (err) {
      console.error(err);
      setDogError("Nie udało się pobrać listy psów.");
    } finally {
      setLoadingDogs(false);
    }
  };

  const loadCats = async () => {
    try {
      const data = await fetchCats();
      setCats(data);
      setCatError(null);
    } catch (err) {
      console.error(err);
      setCatError("Nie udało się pobrać listy kotów.");
    } finally {
      setLoadingCats(false);
    }
  };

  // załadowanie psów i kotów
  useEffect(() => {
    loadDogs();
    loadCats();
  }, []);

  // odświeżanie jak socket wysyła zmiany dla psów
  useEffect(() => {
    if (dogLastMessage > 0) {
      loadDogs();
    }
  }, [dogLastMessage]);

  // odświeżanie jak socket wysyła zmiany dla kotów
  useEffect(() => {
    if (catLastMessage > 0) {
      loadCats();
    }
  }, [catLastMessage]);

  // Handlery dla psów
  const handleCreateDog = async (dogData: DogCreate) => {
    await createDog(dogData);
    loadDogs();
  };

  const handleUpdateDog = async (dogData: DogCreate) => {
    if (!editingDog) return;
    await updateDog(editingDog.id, dogData);
    loadDogs();
  };

  const handleDeleteDog = async (id: number) => {
    try {
      await deleteDog(id);
      loadDogs();
    } catch (error) {
      console.error("Failed to delete dog:", error);
      alert("Nie udało się usunąć psa.");
    }
  };

  // Handlery dla kotów
  const handleCreateCat = async (catData: CatCreate) => {
    await createCat(catData);
    loadCats();
  };

  const handleUpdateCat = async (catData: CatCreate) => {
    if (!editingCat) return;
    await updateCat(editingCat.id, catData);
    loadCats();
  };

  const handleDeleteCat = async (id: number) => {
    try {
      await deleteCat(id);
      loadCats();
    } catch (error) {
      console.error("Failed to delete cat:", error);
      alert("Nie udało się usunąć kota.");
    }
  };

  const openCreateDogModal = () => {
    setEditingDog(null);
    setIsDogModalOpen(true);
  };

  const openEditDogModal = (dog: Dog) => {
    setEditingDog(dog);
    setIsDogModalOpen(true);
  };

  const openCreateCatModal = () => {
    setEditingCat(null);
    setIsCatModalOpen(true);
  };

  const openEditCatModal = (cat: Cat) => {
    setEditingCat(cat);
    setIsCatModalOpen(true);
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

          <div className="flex items-center gap-3">
            <button
              onClick={openCreateDogModal}
              className="flex items-center gap-2 px-4 py-2 bg-lime-600 text-white rounded-lg hover:bg-lime-700 transition-colors text-sm font-medium shadow-sm"
            >
              <Plus className="w-4 h-4" />
              Dodaj psa
            </button>
            <button
              onClick={openCreateCatModal}
              className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors text-sm font-medium shadow-sm"
            >
              <Plus className="w-4 h-4" />
              Dodaj kota
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Server Status Panel */}
        <ServerStatusPanel status={serverStatus} isConnected={isConnected} />

        {/* Tabs */}
        <div className="flex gap-2 mb-6">
          <button
            onClick={() => setActiveTab("all")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === "all"
                ? "bg-blue-600 text-white"
                : "bg-white text-gray-600 hover:bg-gray-100 border border-gray-200"
            }`}
          >
            <PawPrint className="w-5 h-5" />
            Wszystkie ({dogs.length + cats.length})
          </button>
          <button
            onClick={() => setActiveTab("dogs")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === "dogs"
                ? "bg-lime-600 text-white"
                : "bg-white text-gray-600 hover:bg-gray-100 border border-gray-200"
            }`}
          >
            <DogIcon className="w-5 h-5" />
            Psy ({dogs.length})
          </button>
          <button
            onClick={() => setActiveTab("cats")}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-medium transition-colors ${
              activeTab === "cats"
                ? "bg-purple-600 text-white"
                : "bg-white text-gray-600 hover:bg-gray-100 border border-gray-200"
            }`}
          >
            <CatIcon className="w-5 h-5" />
            Koty ({cats.length})
          </button>
        </div>

        {/* All Animals Tab */}
        {activeTab === "all" && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
              <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
                <div className="p-3 rounded-lg bg-rose-100">
                  <svg
                    className="w-6 h-6 text-rose-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
                    />
                  </svg>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Adoptowane</p>
                  <p className="text-2xl font-bold text-gray-800">
                    {(dogStats?.adopted_total ?? 0) +
                      (catStats?.adopted_total ?? 0)}
                  </p>
                </div>
              </div>
              <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
                <div className="p-3 rounded-lg bg-amber-100">
                  <svg
                    className="w-6 h-6 text-amber-600"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
                    />
                  </svg>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Zwrócone właścicielom</p>
                  <p className="text-2xl font-bold text-gray-800">
                    {(dogStats?.returned_total ?? 0) +
                      (catStats?.returned_total ?? 0)}
                  </p>
                </div>
              </div>
              <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
                <div className="p-3 rounded-lg bg-lime-100">
                  <DogIcon className="w-6 h-6 text-lime-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Psy w schronisku</p>
                  <p className="text-2xl font-bold text-gray-800">
                    {dogStats?.current_in_shelter ?? 0}
                  </p>
                </div>
              </div>
              <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
                <div className="p-3 rounded-lg bg-purple-100">
                  <CatIcon className="w-6 h-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm text-gray-500">Koty w schronisku</p>
                  <p className="text-2xl font-bold text-gray-800">
                    {catStats?.current_in_shelter ?? 0}
                  </p>
                </div>
              </div>
            </div>

            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Wszystkie zwierzęta
            </h2>

            {(loadingDogs || loadingCats) &&
            dogs.length === 0 &&
            cats.length === 0 ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
              </div>
            ) : dogError || catError ? (
              <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200">
                {dogError || catError}
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {dogs.map((dog) => (
                  <DogCard
                    key={`dog-${dog.id}`}
                    dog={dog}
                    onEdit={openEditDogModal}
                    onDelete={handleDeleteDog}
                  />
                ))}
                {cats.map((cat) => (
                  <CatCard
                    key={`cat-${cat.id}`}
                    cat={cat}
                    onEdit={openEditCatModal}
                    onDelete={handleDeleteCat}
                  />
                ))}
              </div>
            )}

            {!loadingDogs &&
              !loadingCats &&
              dogs.length === 0 &&
              cats.length === 0 &&
              !dogError &&
              !catError && (
                <div className="text-center py-12 text-gray-500">
                  Brak zwierząt w bazie danych.
                </div>
              )}
          </>
        )}

        {/* Dogs Tab */}
        {activeTab === "dogs" && (
          <>
            <StatsOverview stats={dogStats} />

            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Lista psów
            </h2>

            {loadingDogs && dogs.length === 0 ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-lime-600"></div>
              </div>
            ) : dogError ? (
              <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200">
                {dogError}
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {dogs.map((dog) => (
                  <DogCard
                    key={dog.id}
                    dog={dog}
                    onEdit={openEditDogModal}
                    onDelete={handleDeleteDog}
                  />
                ))}
              </div>
            )}

            {!loadingDogs && dogs.length === 0 && !dogError && (
              <div className="text-center py-12 text-gray-500">
                Brak psów w bazie danych.
              </div>
            )}
          </>
        )}

        {/* Cats Tab */}
        {activeTab === "cats" && (
          <>
            <CatStatsOverview stats={catStats} />

            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              Lista kotów
            </h2>

            {loadingCats && cats.length === 0 ? (
              <div className="flex justify-center items-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-600"></div>
              </div>
            ) : catError ? (
              <div className="bg-red-50 text-red-600 p-4 rounded-lg border border-red-200">
                {catError}
              </div>
            ) : (
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                {cats.map((cat) => (
                  <CatCard
                    key={cat.id}
                    cat={cat}
                    onEdit={openEditCatModal}
                    onDelete={handleDeleteCat}
                  />
                ))}
              </div>
            )}

            {!loadingCats && cats.length === 0 && !catError && (
              <div className="text-center py-12 text-gray-500">
                Brak kotów w bazie danych.
              </div>
            )}
          </>
        )}
      </main>

      <DogForm
        isOpen={isDogModalOpen}
        onClose={() => setIsDogModalOpen(false)}
        onSubmit={editingDog ? handleUpdateDog : handleCreateDog}
        initialData={editingDog}
        title={editingDog ? "Edytuj psa" : "Dodaj nowego psa"}
      />

      <CatForm
        isOpen={isCatModalOpen}
        onClose={() => setIsCatModalOpen(false)}
        onSubmit={editingCat ? handleUpdateCat : handleCreateCat}
        initialData={editingCat}
        title={editingCat ? "Edytuj kota" : "Dodaj nowego kota"}
      />
    </div>
  );
}

export default App;
