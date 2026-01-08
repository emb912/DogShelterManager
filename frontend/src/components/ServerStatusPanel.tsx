import React from "react";
import type { ServerStatus } from "../types";
import { Server, Clock, Activity, Wifi, WifiOff } from "lucide-react";
import { format } from "date-fns";

interface ServerStatusPanelProps {
  status: ServerStatus | null;
  isConnected: boolean;
}

export const ServerStatusPanel: React.FC<ServerStatusPanelProps> = ({
  status,
  isConnected,
}) => {
  if (!status) {
    return (
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-gray-500">
            <Server className="w-5 h-5" />
            <span className="text-sm">Ładowanie statusu serwera...</span>
          </div>
          <div
            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
              isConnected
                ? "bg-green-100 text-green-700"
                : "bg-red-100 text-red-700"
            }`}
          >
            {isConnected ? (
              <>
                <Wifi className="w-3.5 h-3.5" /> Online
              </>
            ) : (
              <>
                <WifiOff className="w-3.5 h-3.5" /> Offline
              </>
            )}
          </div>
        </div>
        {!isConnected && (
          <p className="text-sm text-gray-500 mt-2">
            Brak połączenia z serwerem. Próba ponownego połączenia...
          </p>
        )}
      </div>
    );
  }

  const formatDate = (dateString: string | null) => {
    if (!dateString) return "Brak";
    try {
      return format(new Date(dateString), "dd.MM.yyyy HH:mm:ss");
    } catch {
      return dateString;
    }
  };

  return (
    <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-6">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Server className="w-5 h-5 text-gray-700" />
          <h3 className="font-semibold text-gray-800">Status serwera</h3>
        </div>
        <div
          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
            isConnected
              ? "bg-green-100 text-green-700"
              : "bg-red-100 text-red-700"
          }`}
        >
          {isConnected ? (
            <>
              <Wifi className="w-3.5 h-3.5" /> Online
            </>
          ) : (
            <>
              <WifiOff className="w-3.5 h-3.5" /> Offline
            </>
          )}
        </div>
      </div>
      {!isConnected && (
        <p className="text-sm text-red-500 mb-4">
          Brak połączenia z serwerem. Próba ponownego połączenia...
        </p>
      )}

      <div className="flex items-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <Clock className="w-4 h-4 text-blue-500" />
          <div>
            <p className="text-gray-500 text-xs">Uruchomiony</p>
            <p className="font-medium text-gray-800">
              {formatDate(status.started_at)}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Activity className="w-4 h-4 text-emerald-500" />
          <div>
            <p className="text-gray-500 text-xs">Ostatnia aktywność</p>
            <p className="font-medium text-gray-800">
              {formatDate(status.last_activity)}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
