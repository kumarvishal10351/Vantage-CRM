import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';

export const Settings = () => {
  const { user } = useAuth();
  const [health, setHealth] = useState(null);
  const [healthLoading, setHealthLoading] = useState(true);

  const checkHealth = async () => {
    setHealthLoading(true);
    try {
      const res = await axios.get('http://127.0.0.1:8000/health');
      setHealth(res.data);
    } catch {
      setHealth({ status: 'offline', database: 'unreachable' });
    } finally {
      setHealthLoading(false);
    }
  };

  useEffect(() => {
    checkHealth();
  }, []);

  return (
    <div className="flex flex-col w-full max-w-4xl">
      {/* Header */}
      <div className="flex flex-col gap-space-xs mb-space-lg">
        <div className="flex items-center gap-space-xs font-label-xs-mono text-label-xs-mono uppercase tracking-wider text-secondary">
          <span>Administration</span>
          <span className="text-outline-variant">/</span>
          <span className="text-primary-container font-semibold">Settings</span>
        </div>
        <h1 className="font-display-md text-display-md text-on-surface tracking-tight">
          System &amp; API Configuration
        </h1>
        <p className="font-body-sm text-body-sm text-on-surface-variant mt-space-2xs">
          Vantage CRM platform parameters, backend endpoint telemetry, and user profile.
        </p>
      </div>

      {/* Backend API Connection Status */}
      <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs mb-space-lg">
        <div className="flex items-center justify-between pb-space-sm border-b border-outline-variant/20 mb-space-base">
          <div className="flex items-center gap-2">
            <span className="material-symbols-outlined text-[20px] text-primary-container">dns</span>
            <h2 className="font-headline-sm text-headline-sm text-on-surface">
              Backend Service Connection
            </h2>
          </div>
          <button
            onClick={checkHealth}
            className="h-7 px-3 bg-surface-container-low hover:bg-surface-container rounded text-xs text-on-surface font-semibold flex items-center gap-1 border border-outline-variant/40"
          >
            <span className="material-symbols-outlined text-[14px]">refresh</span>
            <span>Check Health</span>
          </button>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-space-md">
          <div className="p-space-sm rounded-lg bg-surface-container-low">
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">
              API Base URL
            </span>
            <span className="font-mono text-sm font-semibold text-on-surface mt-1 block">
              {import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1'}
            </span>
          </div>

          <div className="p-space-sm rounded-lg bg-surface-container-low">
            <span className="font-label-xs-mono text-label-xs-mono text-secondary uppercase block">
              Backend Server Health
            </span>
            <div className="flex items-center gap-2 mt-1">
              <span
                className={`w-2.5 h-2.5 rounded-full ${
                  health?.status === 'healthy' || health?.status === 'ok'
                    ? 'bg-tertiary-container'
                    : 'bg-error animate-pulse'
                }`}
              ></span>
              <span className="font-semibold text-sm capitalize">
                {healthLoading ? 'Pinging...' : health?.status || 'Unknown'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Current Operator Profile */}
      <div className="bg-surface-container-lowest rounded-xl p-space-lg border border-outline-variant/30 shadow-xs">
        <h2 className="font-headline-sm text-headline-sm text-on-surface mb-space-base pb-space-sm border-b border-outline-variant/20">
          Authenticated Session
        </h2>

        <div className="flex items-center gap-space-md">
          <div className="w-12 h-12 rounded-full bg-primary-container text-on-primary flex items-center justify-center font-bold text-lg shadow-xs">
            {user?.username ? user.username.substring(0, 2).toUpperCase() : 'SJ'}
          </div>
          <div>
            <div className="font-headline-sm text-headline-sm text-on-surface">
              {user?.full_name || 'Sarah Jenkins'}
            </div>
            <div className="text-secondary text-sm">
              Role: <strong className="text-on-surface">{user?.role || 'VP Sales Operations'}</strong> • Username:{' '}
              <strong className="text-on-surface">{user?.username || 'admin'}</strong>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
