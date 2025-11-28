import React from 'react';
import type { DogStats } from '../types';
import { Home, Heart, RotateCcw, Dog } from 'lucide-react';

interface StatsOverviewProps {
  stats: DogStats | null;
}

export const StatsOverview: React.FC<StatsOverviewProps> = ({ stats }) => {
  if (!stats) return null;

  const items = [
    { label: 'Adoptowane', value: stats.adopted_total, icon: Heart, color: 'text-rose-600', bg: 'bg-rose-100' },
    { label: 'W schronisku', value: stats.current_in_shelter, icon: Home, color: 'text-emerald-600', bg: 'bg-emerald-100' },
    { label: 'Zwrócone właścicielom', value: stats.returned_total, icon: RotateCcw, color: 'text-amber-600', bg: 'bg-amber-100' },
    { label: 'Wszystkie', value: stats.all_dogs_total, icon: Dog, color: 'text-blue-600', bg: 'bg-blue-100' },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {items.map((item, index) => (
        <div key={index} className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 flex items-center gap-4">
          <div className={`p-3 rounded-lg ${item.bg}`}>
            <item.icon className={`w-6 h-6 ${item.color}`} />
          </div>
          <div>
            <p className="text-sm text-gray-500">{item.label}</p>
            <p className="text-2xl font-bold text-gray-800">{item.value}</p>
          </div>
        </div>
      ))}
    </div>
  );
};
